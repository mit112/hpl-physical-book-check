"""Offline HPL evidence processor. No network, login, holds, or API guessing.

Consumes observed catalog table cells and an explicitly verified identity/scope.
The browser or connector supplies evidence; this module makes conservative counts
and maintains a resumable ledger. Python 3.10+, standard library only.
"""
import argparse
import copy
import hashlib
import json
import re
import sys
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse, unquote

PRINT_FORMATS = {'books', 'book', 'large print'}
NONPRINT_FORMATS = {'audio disc', 'audiobook', 'ebook', 'e-book', 'electronic resource',
                    'dvd', 'blu-ray', 'blu ray', 'kit', 'video', 'sound recording'}
PRINT_ITEMS = {'book', 'books', 'paperback', 'new books', 'notable book',
               'large print', 'large print book', 'graphic novel', 'new book'}
LOADING = {'', 'searching...', 'loading...', 'searching', 'loading', 'unknown'}
NON_BRANCH = {'floating collection'}
UNAVAILABLE = {'checked out', 'on hold for someone', 'being transferred between libraries',
               'being shipped to library', 'in transit', 'in processing', 'processing',
               'missing', 'lost', 'on order', 'unavailable', 'not available'}
BUCKETS = ['available', 'unable_to_verify', 'held_unavailable', 'no_branch_copy', 'no_print_match']


def norm(value):
    return ' '.join(str(value).split()).casefold()


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError('checked_at must be an ISO timestamp with a timezone')
    try:
        result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as exc:
        raise ValueError('Invalid checked_at timestamp') from exc
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError('checked_at requires a timezone')
    return result


def normalize_table(table):
    """Use cell boundaries rather than splitting the concatenated row text."""
    if not isinstance(table, list) or not table or not isinstance(table[0], list):
        raise ValueError('Expected a table of header and cell arrays')
    aliases = {'library': 'branch', 'branch': 'branch', 'material type': 'material_type',
               'shelf number': 'call_number', 'call number': 'call_number',
               'status': 'raw_status', 'item id': 'item_id', 'barcode': 'item_id'}
    columns = {}
    for index, header in enumerate(table[0]):
        field = aliases.get(norm(header))
        if field:
            if field in columns:
                raise ValueError('Duplicate evidence column: ' + field)
            columns[field] = index
    if not {'branch', 'material_type', 'raw_status'} <= columns.keys():
        raise ValueError('Table requires Library/Branch, Material Type, and Status columns')
    result = []
    for row in table[1:]:
        if not isinstance(row, list) or len(row) != len(table[0]) or any(not isinstance(x, str) for x in row):
            raise ValueError('Ragged or non-text table row')
        result.append({field: row[index].strip() for field, index in columns.items()})
    return result


def validate_record(record):
    for field in ['record_id', 'url', 'title', 'author', 'format', 'edition', 'language', 'checked_at', 'run_id']:
        if not isinstance(record.get(field), str) or (not record[field].strip() and field != 'language'):
            raise ValueError('Record requires text field: ' + field)
    url = urlparse(record['url'])
    if url.scheme != 'https' or url.hostname != 'halan.sdp.sirsi.net' or url.username or url.password:
        raise ValueError('Expected an observed HTTPS HPL catalog record URL')
    if '/search/detailnonmodal/' not in url.path:
        raise ValueError('A search URL cannot stand in for a record URL')
    record_id = re.search(r'SD_ILS:(\d+)(?:/|$)', unquote(url.path))
    if record_id is None or record_id.group(1) != record['record_id']:
        raise ValueError('record_id must match the observed catalog URL')
    query = parse_qs(url.query).get('qu', [])
    if query and (not isinstance(record.get('query'), str) or not record['query'].strip()):
        raise ValueError('Record URL has qu; require the submitted query for provenance')
    if record.get('query') and query and norm(record['query']) not in [norm(q) for q in query]:
        raise ValueError('Source URL query differs from the submitted query')
    timestamp(record['checked_at'])
    if timestamp(record['checked_at']) > datetime.now(timezone.utc):
        raise ValueError('Evidence timestamp cannot be in the future')
    if record.get('match_state') not in {'exact', 'excluded', 'unresolved'}:
        raise ValueError('match_state must be exact, excluded, or unresolved')
    if type(record.get('holdings_complete')) is not bool:
        raise ValueError('holdings_complete must be a JSON boolean')
    if not isinstance(record.get('items'), list):
        raise ValueError('Record requires an items array')
    for item in record['items']:
        if not isinstance(item, dict):
            raise ValueError('Each item must be an object')
        for field in ['branch', 'material_type', 'raw_status']:
            if not isinstance(item.get(field), str):
                raise ValueError('Each item requires text field: ' + field)
        for field in ['call_number', 'item_id']:
            if field in item and not isinstance(item[field], str):
                raise ValueError(field + ' must be text')
    for field in ['expected_copies', 'aggregate_available']:
        if field in record and record[field] is not None and (type(record[field]) is not int or record[field] < 0):
            raise ValueError(field + ' must be a nonnegative integer or null')


def status_kind(raw):
    value = norm(raw)
    if value == 'available':
        return 'available'
    if value in UNAVAILABLE:
        return 'unavailable'
    due = re.fullmatch(r'due\s+(\d{1,2})/(\d{1,2})(?:/(\d{2}|\d{4}))?', value)
    if due:
        try:
            year = int(due.group(3)) if due.group(3) else 2000
            if year < 100:
                year += 2000
            datetime(year, int(due.group(1)), int(due.group(2)))
            return 'unavailable'
        except ValueError:
            pass
    return 'unknown'


def upsert_record(entry, record):
    validate_record(record)
    records = entry.setdefault('records', [])
    for i, old in enumerate(records):
        if old['record_id'] == record['record_id']:
            if timestamp(record['checked_at']) < timestamp(old['checked_at']):
                raise ValueError('Older evidence cannot replace a newer observation')
            records[i] = copy.deepcopy(record)
            return
    records.append(copy.deepcopy(record))


def classify(entry, branch, run_id, language='English', mode='thorough', not_before=None):
    if mode not in {'quick', 'thorough'}:
        raise ValueError('mode must be quick or thorough')
    label = branch or 'HPL'
    gaps = list(entry.get('issues', []))
    scoped = []
    seen_records = set()
    for raw in entry.get('records', []):
        try:
            validate_record(raw)
        except (ValueError, TypeError) as exc:
            gaps.append('Invalid record evidence: ' + str(exc))
            continue
        if raw['run_id'] != run_id:
            gaps.append('Earlier-run evidence requires refresh')
            continue
        if not_before and timestamp(raw['checked_at']) < timestamp(not_before):
            gaps.append('Observation predates this run and requires refresh')
            continue
        if raw['record_id'] in seen_records:
            gaps.append('Duplicate record observation requires reconciliation')
            continue
        seen_records.add(raw['record_id'])
        if raw['match_state'] == 'excluded' or norm(raw['format']) in NONPRINT_FORMATS:
            continue
        if raw['match_state'] == 'unresolved' or norm(raw['format']) not in PRINT_FORMATS:
            gaps.append('Unresolved identity or format for record ' + raw['record_id'])
            continue
        if norm(raw['language']) in LOADING:
            gaps.append('Unknown language for record ' + raw['record_id'])
            continue
        if language and norm(raw['language']) != norm(language):
            continue
        if norm(raw['edition']) in LOADING:
            gaps.append('Unresolved edition label for record ' + raw['record_id'])
        scoped.append(raw)

    editions = []
    all_items = []
    known_item_ids = {}
    for rec in scoped:
        rid = rec['record_id']
        if not rec['holdings_complete']:
            gaps.append('Unchecked holdings for record ' + rid)
        eligible = []
        record_ids = set()
        for index, item in enumerate(rec['items']):
            material = norm(item['material_type'])
            if material not in PRINT_ITEMS:
                gaps.append('Unresolved/non-print item type in print record ' + rid)
                continue
            value = copy.deepcopy(item)
            value['record_id'] = rid
            value['kind'] = status_kind(item['raw_status'])
            value['counted'] = True
            if norm(item['branch']) in LOADING or value['kind'] == 'unknown':
                gaps.append('Unresolved branch/status in record ' + rid)
                value['kind'] = 'unknown'
            eligible.append(value)
            identity = item.get('item_id')
            record_ids.add(identity or ('row:' + str(index)))
            if identity:
                if identity in known_item_ids:
                    old = known_item_ids[identity]
                    if (norm(old['raw_status']), norm(old['branch'])) != (norm(value['raw_status']), norm(value['branch'])):
                        old['kind'] = 'unknown'
                        value['kind'] = 'unknown'
                        gaps.append('Conflicting observations for item ' + identity)
                    value['counted'] = False
                    continue
                known_item_ids[identity] = value
            all_items.append(value)
        if rec.get('expected_copies') is not None and rec['expected_copies'] != len(record_ids):
            gaps.append('Copy count differs from inspected rows for record ' + rid)
        unique_record_items = {}
        for index, item in enumerate(eligible):
            unique_record_items.setdefault(item.get('item_id') or ('row:' + str(index)), item)
        record_available = sum(item['kind'] == 'available' for item in unique_record_items.values())
        if rec.get('aggregate_available') is not None and rec['aggregate_available'] != record_available:
            gaps.append('Availability aggregate differs from item rows for record ' + rid)
        selected = [x for x in eligible if branch is None or norm(x['branch']) == norm(branch)]
        editions.append(dict(record_id=rid, url=rec['url'], edition=rec.get('edition', rec['format']),
                             checked_at=rec['checked_at'], items=selected,
                             confirmed_available=0,
                             inspected_copies=sum(x['counted'] for x in selected)))

    for edition in editions:
        edition['confirmed_available'] = sum(x['counted'] and x['kind'] == 'available' and norm(x['branch']) not in NON_BRANCH for x in edition['items'])

    complete = (entry.get('search_complete') is True and entry.get('editions_complete') is True and not gaps)
    if not entry.get('search_complete'):
        gaps.append('Search pages not completed')
    if not entry.get('editions_complete'):
        gaps.append('Matching print editions not completed')
    if not scoped and entry.get('fallback_complete') is not True:
        gaps.append('No-match fallback not completed')
        complete = False
    if mode == 'quick' and any(
            x['kind'] == 'available' and norm(x['branch']) not in NON_BRANCH
            and (branch is None or norm(x['branch']) == norm(branch))
            for x in all_items):
        complete = False
        gaps.append('Quick mode does not establish exhaustive totals')
    selected = [x for x in all_items if (branch is None or norm(x['branch']) == norm(branch))]
    if any(norm(x['branch']) in NON_BRANCH and x['kind'] == 'available' for x in selected):
        complete = False
        gaps.append('Floating Collection availability has no verified pickup branch')
    available = [x for x in selected if x['kind'] == 'available' and norm(x['branch']) not in NON_BRANCH]
    usable = any(norm(x['branch']) not in LOADING and x['kind'] != 'unknown' for x in all_items)
    coverage = 'complete' if complete else ('partial' if usable else 'unverified')
    if available:
        code = 'available'
    elif not complete:
        code = 'unable_to_verify'
    elif not scoped:
        code = 'no_print_match'
    elif selected:
        code = 'held_unavailable'
    else:
        code = 'no_branch_copy'
    labels = dict(available='Available at ' + label, unable_to_verify='Unable to verify',
                  held_unavailable='Held at ' + label + ', none available',
                  no_branch_copy='No ' + label + ' copy shown', no_print_match='No matching print record found')
    other = sorted({x['branch'] for x in all_items if x['kind'] == 'available' and norm(x['branch']) not in NON_BRANCH
                    and (branch is None or norm(x['branch']) != norm(branch))})
    return dict(key=entry.get('key'), title=entry.get('title'), author=entry.get('author'),
                status_code=code, status=labels[code], completeness=coverage,
                confirmed_available=len(available), total=len(selected) if complete and scoped else None,
                editions=editions, other_available_branches=other, gaps=list(dict.fromkeys(gaps)))


def summarize(ledger):
    if ledger.get('schema_version') != 1:
        raise ValueError('Unsupported ledger schema')
    timestamp(ledger['started_at'])
    results = [classify(x, branch=ledger['branch'], run_id=ledger['run_id'],
                        language=ledger.get('language', 'English'), mode=ledger.get('mode', 'thorough'), not_before=ledger['started_at'])
               for x in ledger['titles']]
    counts = Counter(x['status_code'] for x in results)
    coverage = Counter(x['completeness'] for x in results)
    return dict(run_id=ledger['run_id'], branch=ledger['branch'], language=ledger.get('language'),
                mode=ledger.get('mode', 'thorough'), requested=len(results),
                status_counts={k: counts[k] for k in BUCKETS},
                coverage_counts={k: coverage[k] for k in ['complete', 'partial', 'unverified']}, results=results)


def pending_keys(ledger):
    return [r['key'] for r in summarize(ledger)['results'] if r['completeness'] != 'complete']


def refresh_ledger(ledger):
    ledger['run_id'] = str(uuid.uuid4())
    ledger['started_at'] = datetime.now(timezone.utc).isoformat()
    for title in ledger['titles']:
        for flag in ['search_complete', 'fallback_complete', 'editions_complete']:
            title[flag] = False
        title['issues'] = []


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    try:
        temp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        temp.replace(path)
    finally:
        if temp.exists():
            temp.unlink()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def initialize(titles, branch, language, mode):
    if branch is not None and (not isinstance(branch, str) or not branch.strip()):
        raise ValueError('Choose a nonblank branch or --all-branches')
    if not isinstance(language, str) or not language.strip() or norm(language) in LOADING:
        raise ValueError('Choose an explicit scope language')
    if mode not in {'quick', 'thorough'}:
        raise ValueError('Choose quick or thorough mode')
    if not isinstance(titles, list) or not titles:
        raise ValueError('Provide a nonempty array of title/author objects')
    entries = []
    seen = set()
    for book in titles:
        if not isinstance(book, dict) or not isinstance(book.get('title'), str) or not book['title'].strip():
            raise ValueError('Each title requires a nonblank title string')
        if not isinstance(book.get('author', ''), str):
            raise ValueError('author must be text')
        identity = norm(book['title']) + '\0' + norm(book.get('author', ''))
        if identity in seen:
            continue
        seen.add(identity)
        entries.append(dict(key=hashlib.sha256(identity.encode()).hexdigest()[:16], title=book['title'].strip(),
                            author=book.get('author', '').strip(), search_complete=False, fallback_complete=False,
                            editions_complete=False, records=[], issues=[]))
    return dict(schema_version=1, run_id=str(uuid.uuid4()), started_at=datetime.now(timezone.utc).isoformat(),
                branch=branch, language=language, mode=mode, titles=entries)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    init = commands.add_parser('init'); init.add_argument('--titles', required=True); init.add_argument('--output', required=True)
    scope = init.add_mutually_exclusive_group(required=True); scope.add_argument('--branch'); scope.add_argument('--all-branches', action='store_true')
    init.add_argument('--language', default='English'); init.add_argument('--mode', choices=['quick', 'thorough'], default='thorough')
    init.add_argument('--force', action='store_true')
    report = commands.add_parser('report'); report.add_argument('ledger')
    queue = commands.add_parser('pending'); queue.add_argument('ledger')
    refresh = commands.add_parser('refresh'); refresh.add_argument('ledger')
    ingest = commands.add_parser('ingest'); ingest.add_argument('ledger'); ingest.add_argument('--key', required=True); ingest.add_argument('--record', required=True)
    mark = commands.add_parser('mark'); mark.add_argument('ledger'); mark.add_argument('--key', required=True)
    for flag in ['search-complete', 'fallback-complete', 'editions-complete']:
        mark.add_argument('--' + flag, action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.command == 'init':
            if Path(args.output).exists() and not args.force:
                raise ValueError('Output exists; choose a new path or explicitly pass --force')
            value = initialize(read_json(args.titles), args.branch, args.language, args.mode)
            write_json(args.output, value)
            print(json.dumps({'run_id': value['run_id'], 'titles': [{'key': x['key'], 'title': x['title']} for x in value['titles']]}))
            return
        ledger = read_json(args.ledger)
        if args.command == 'report':
            print(json.dumps(summarize(ledger), ensure_ascii=False, indent=2))
        elif args.command == 'pending':
            print(json.dumps(pending_keys(ledger)))
        elif args.command == 'refresh':
            refresh_ledger(ledger); write_json(args.ledger, ledger)
            print(json.dumps({'run_id': ledger['run_id'], 'pending': pending_keys(ledger)}))
        else:
            title = next((x for x in ledger['titles'] if x['key'] == args.key), None)
            if title is None:
                raise ValueError('Unknown title key')
            if args.command == 'ingest':
                record = read_json(args.record)
                if 'table' in record:
                    record['items'] = normalize_table(record.pop('table'))
                if record.get('run_id') != ledger['run_id']:
                    raise ValueError('Record belongs to a different run; refresh live evidence')
                if timestamp(record['checked_at']) < timestamp(ledger['started_at']):
                    raise ValueError('Observation predates this run; refresh live evidence')
                upsert_record(title, record)
            else:
                for flag in ['search_complete', 'fallback_complete', 'editions_complete']:
                    if getattr(args, flag):
                        title[flag] = True
            write_json(args.ledger, ledger)
            print(json.dumps({'key': args.key, 'pending': pending_keys(ledger)}))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, 'Evidence error: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
