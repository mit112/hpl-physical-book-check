import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT if (ROOT/'scripts').exists() else ROOT/'skills/hpl-physical-book-check'
sys.path.insert(0, str(SKILL_ROOT/'scripts'))
import hpl_evidence as h

URL = 'https://halan.sdp.sirsi.net/client/en_US/hou/search/detailnonmodal/ent:$002f$002fSD_ILS$002f0$002fSD_ILS:662664/ada?qu=Dune+Frank+Herbert&te=ILS'
STAMP = '2026-10-13T05:09:28+00:00'
HEAD = ['Library', 'Audience', 'Home Location', 'Material Type', 'Shelf Number', 'Status']


def record(status='Available', branch='Looscan', **extra):
    value = dict(record_id='662664', url=URL, title='Dune', author='Frank Herbert',
                 format='Books', edition='Regular print', language='English',
                 match_state='exact', holdings_complete=True, checked_at=STAMP,
                 run_id='run-1', query='Dune Frank Herbert', items=[dict(
                     branch=branch, material_type='Book', call_number='HERBE', raw_status=status)])
    value.update(extra)
    if 'record_id' in extra and 'url' not in extra:
        value['url'] = URL.replace(':662664/', ':' + extra['record_id'] + '/')
    return value


def entry(*records, **extra):
    value = dict(key='dune', title='Dune', author='Frank Herbert',
                 search_complete=True, fallback_complete=True, editions_complete=True,
                 records=list(records), issues=[])
    value.update(extra)
    return value


class EvidenceTests(unittest.TestCase):
    def result(self, e, **kw):
        return h.classify(e, branch=kw.pop('branch', 'Looscan'), run_id='run-1', not_before='2026-10-13T05:00:00+00:00', **kw)

    def test_live_columns_preserve_distinct_identical_copy_rows(self):
        rows = [['Looscan', 'Adult', 'Fiction', 'Book', 'WEIR', 'Checked out']] * 2
        items = h.normalize_table([HEAD, *rows])
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]['branch'], 'Looscan')
        self.assertEqual(items[0]['call_number'], 'WEIR')

    def test_header_order_is_not_assumed(self):
        items = h.normalize_table([['Status', 'Library', 'Material Type', 'Call Number'],
                                   ['Available', 'Heights', 'Book', 'HERBE']])
        self.assertEqual(items[0]['branch'], 'Heights')

    def test_missing_required_column_fails_closed(self):
        with self.assertRaises(ValueError):
            h.normalize_table([['Library', 'Material Type'], ['Looscan', 'Book']])

    def test_ragged_row_fails_closed(self):
        with self.assertRaises(ValueError):
            h.normalize_table([HEAD, ['Looscan']])

    def test_available_item_is_positive_evidence(self):
        r = self.result(entry(record()))
        self.assertEqual((r['status_code'], r['confirmed_available'], r['total']), ('available', 1, 1))

    def test_branch_is_selected_exactly(self):
        r = self.result(entry(record(branch='Heights')))
        self.assertEqual(r['status_code'], 'no_branch_copy')
        self.assertEqual(r['other_available_branches'], ['Heights'])

    def test_raw_unavailable_statuses_remain_distinct(self):
        for status in ['Checked out', 'On hold for someone', 'Due 10/28/26', 'Being transferred between libraries', 'Being shipped to library', 'Missing', 'In processing']:
            with self.subTest(status=status):
                r = self.result(entry(record(status)))
                self.assertEqual(r['status_code'], 'held_unavailable')
                self.assertEqual(r['editions'][0]['items'][0]['raw_status'], status)

    def test_unknown_status_is_not_unavailable(self):
        self.assertEqual(self.result(entry(record('Mystery status')))['status_code'], 'unable_to_verify')

    def test_loading_branch_is_not_an_absent_branch(self):
        self.assertEqual(self.result(entry(record('Searching...', branch='Searching...')))['status_code'], 'unable_to_verify')

    def test_positive_evidence_survives_partial_check(self):
        r = self.result(entry(record(), editions_complete=False))
        self.assertEqual((r['status_code'], r['completeness'], r['total']), ('available', 'partial', None))

    def test_quick_mode_never_claims_exhaustive_total(self):
        r = self.result(entry(record()), mode='quick')
        self.assertEqual((r['status_code'], r['completeness'], r['total']), ('available', 'partial', None))

    def test_quick_negative_requires_thorough_coverage(self):
        r = self.result(entry(record('Checked out'), search_complete=False), mode='quick')
        self.assertEqual(r['status_code'], 'unable_to_verify')

    def test_quick_negative_can_finish_exhaustive_check(self):
        r = self.result(entry(record('Checked out')), mode='quick')
        self.assertEqual((r['status_code'], r['completeness'], r['total']),
                         ('held_unavailable', 'complete', 1))

    def test_quick_absent_branch_can_finish_exhaustive_check(self):
        r = self.result(entry(record(branch='Heights')), mode='quick')
        self.assertEqual((r['status_code'], r['completeness'], r['total']),
                         ('no_branch_copy', 'complete', 0))

    def test_all_branches_counts_available_items(self):
        r = self.result(entry(record(branch='Heights')), branch=None)
        self.assertEqual((r['status_code'], r['confirmed_available']), ('available', 1))

    def test_floating_collection_is_not_a_pickup_branch(self):
        r = self.result(entry(record(branch='Floating Collection')), branch=None)
        self.assertEqual(r['status_code'], 'unable_to_verify')
        self.assertNotIn('Floating Collection', r['other_available_branches'])

    def test_audio_record_is_excluded(self):
        r = self.result(entry(record(format='Audio Disc')))
        self.assertEqual(r['status_code'], 'no_print_match')

    def test_wrong_language_is_excluded(self):
        self.assertEqual(self.result(entry(record(language='French')))['status_code'], 'no_print_match')

    def test_unverified_language_is_unresolved(self):
        self.assertEqual(self.result(entry(record(language='')))['status_code'], 'unable_to_verify')

    def test_same_author_unrelated_title_is_excluded(self):
        self.assertEqual(self.result(entry(record(title='Dune Messiah', match_state='excluded')))['status_code'], 'no_print_match')

    def test_unresolved_identity_cannot_create_positive_result(self):
        self.assertEqual(self.result(entry(record(match_state='unresolved')))['status_code'], 'unable_to_verify')

    def test_book_club_kit_is_excluded(self):
        self.assertEqual(self.result(entry(record(format='Kit')))['status_code'], 'no_print_match')

    def test_no_match_requires_fallback(self):
        self.assertEqual(self.result(entry(fallback_complete=False))['status_code'], 'unable_to_verify')
        self.assertEqual(self.result(entry())['status_code'], 'no_print_match')

    def test_aggregate_conflict_cannot_create_available_item(self):
        r = self.result(entry(record('Checked out', aggregate_available=3)))
        self.assertEqual((r['status_code'], r['completeness']), ('unable_to_verify', 'partial'))
        self.assertTrue(any('aggregate' in x for x in r['gaps']))

    def test_global_available_count_does_not_conflict_with_branch_zero(self):
        items = [dict(branch='Looscan', material_type='Book', raw_status=s)
                 for s in ['Due 10/20/26', 'Due 10/21/26', 'Due 10/22/26',
                           'Being transferred between libraries']]
        items += [dict(branch=b, material_type='Book', raw_status='Available')
                  for b in ['Heights', 'Central', 'Walker']]
        r = self.result(entry(record(items=items, expected_copies=7, aggregate_available=3)))
        self.assertEqual((r['status_code'], r['completeness'], r['confirmed_available'], r['total']),
                         ('held_unavailable', 'complete', 0, 4))
        self.assertEqual(r['gaps'], [])
        self.assertEqual(r['other_available_branches'], ['Central', 'Heights', 'Walker'])

    def test_actual_global_mismatch_keeps_branch_negative_unverified(self):
        items = [dict(branch='Looscan', material_type='Book', raw_status='Checked out')]*4
        items += [dict(branch='Heights', material_type='Book', raw_status='Available')]
        items += [dict(branch='Central', material_type='Book', raw_status='Checked out')]*2
        r = self.result(entry(record(items=items, expected_copies=7, aggregate_available=3)))
        self.assertEqual((r['status_code'], r['completeness'], r['total']),
                         ('unable_to_verify', 'partial', None))
        self.assertTrue(any('aggregate' in x for x in r['gaps']))

    def test_copy_count_conflict_is_partial(self):
        self.assertEqual(self.result(entry(record(expected_copies=2)))['total'], None)

    def test_lucky_day_item_in_verified_book_record_counts_as_print(self):
        for material in ['Lucky Day Collection', 'Family Place Parenting Collection']:
            with self.subTest(material=material):
                item = dict(branch='Central', material_type=material, raw_status='Available')
                r = self.result(entry(record(items=[item], expected_copies=1)), branch='Central')
                self.assertEqual((r['status_code'], r['completeness'], r['confirmed_available'], r['total']),
                                 ('available', 'complete', 1, 1))
                digital = self.result(entry(record(format='DVD', items=[item])))
                self.assertEqual(digital['status_code'], 'no_print_match')

    def test_explicit_float_hub_unavailable_status_keeps_its_detail(self):
        r = self.result(entry(record('Unavailable – item sent to float hub')))
        self.assertEqual((r['status_code'], r['completeness']), ('held_unavailable', 'complete'))
        self.assertEqual(r['editions'][0]['items'][0]['raw_status'], 'Unavailable – item sent to float hub')

    def test_large_print_is_separate_even_when_format_books(self):
        r = self.result(entry(record(), record(record_id='1001', edition='Large print')))
        self.assertEqual(len(r['editions']), 2)
        self.assertEqual(r['confirmed_available'], 2)

    def test_observed_regular_print_record_format_is_eligible(self):
        r = self.result(entry(record(format='Regular print')))
        self.assertEqual((r['status_code'], r['completeness'], r['confirmed_available']),
                         ('available', 'complete', 1))

    def test_observed_teen_book_materials_are_print(self):
        for material in ['Teen Book', 'Notable Teen book', 'New teen books']:
            with self.subTest(material=material):
                r = self.result(entry(record(items=[dict(branch='Looscan', material_type=material, raw_status='Available')])))
                self.assertEqual((r['status_code'], r['completeness']), ('available', 'complete'))

    def test_item_id_deduplication_across_records(self):
        a = record(); a['items'][0]['item_id'] = 'copy-1'
        b = record(record_id='1002'); b['items'][0]['item_id'] = 'copy-1'
        self.assertEqual(self.result(entry(a, b))['confirmed_available'], 1)

    def test_duplicate_record_is_replaced_not_appended(self):
        e = entry(record())
        h.upsert_record(e, record('Checked out'))
        self.assertEqual(len(e['records']), 1)
        self.assertEqual(self.result(e)['confirmed_available'], 0)

    def test_old_run_availability_is_not_current(self):
        r = self.result(entry(record(run_id='old')))
        self.assertEqual((r['status_code'], r['completeness']), ('unable_to_verify', 'unverified'))

    def test_source_query_mismatch_is_rejected(self):
        with self.assertRaises(ValueError):
            h.validate_record(record(query='Piranesi Susanna Clarke'))

    def test_non_catalog_url_is_rejected(self):
        with self.assertRaises(ValueError):
            h.validate_record(record(url='https://example.com/book'))

    def test_timestamp_requires_timezone(self):
        with self.assertRaises(ValueError):
            h.validate_record(record(checked_at='2026-10-13T05:00:00'))

    def test_boolean_fields_cannot_be_truthy_strings(self):
        with self.assertRaises(ValueError):
            h.validate_record(record(holdings_complete='false'))

    def test_report_buckets_reconcile(self):
        ledger = dict(schema_version=1, run_id='run-1', started_at='2026-10-13T05:00:00+00:00', branch='Looscan', language='English', mode='thorough',
                      titles=[entry(record()), entry(), entry(search_complete=False, fallback_complete=False)])
        report = h.summarize(ledger)
        self.assertEqual(sum(report['status_counts'].values()), 3)
        self.assertEqual(sum(report['coverage_counts'].values()), 3)

    def test_resume_only_unfinished_titles(self):
        ledger = dict(schema_version=1, run_id='run-1', started_at='2026-10-13T05:00:00+00:00', branch='Looscan', language='English', mode='thorough',
                      titles=[entry(record()), entry(search_complete=False)])
        self.assertEqual(h.pending_keys(ledger), ['dune'])

    def test_refresh_invalidates_previous_status_and_coverage(self):
        ledger = dict(schema_version=1, run_id='run-1', started_at='2026-10-13T05:00:00+00:00', branch='Looscan', language='English', mode='thorough',
                      titles=[entry(record())])
        h.refresh_ledger(ledger)
        self.assertNotEqual(ledger['run_id'], 'run-1')
        self.assertEqual(h.summarize(ledger)['results'][0]['completeness'], 'unverified')

    def test_live_fixture_parses_available_branches_and_copy_counts(self):
        fixture = json.loads((ROOT / 'tests/fixtures/dune-live.json').read_text())
        items = h.normalize_table(fixture['table'])
        r = self.result(entry(record(items=items, expected_copies=13, aggregate_available=2)), branch='Heights')
        self.assertEqual((r['status_code'], r['confirmed_available'], r['total']), ('held_unavailable', 0, 3))
        self.assertEqual(r['other_available_branches'], ['BOOKLink at One Allen Center', 'Freed-Montrose'])

    def test_cli_init_and_report_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)/'titles.json'; target=Path(tmp)/'ledger.json'
            source.write_text(json.dumps([{'title':'Dune','author':'Frank Herbert'}]))
            script=SKILL_ROOT/'scripts/hpl_evidence.py'
            subprocess.run([sys.executable,str(script),'init','--titles',str(source),'--output',str(target),'--branch','Looscan'],check=True,capture_output=True)
            result=subprocess.run([sys.executable,str(script),'report',str(target)],check=True,capture_output=True,text=True)
            self.assertEqual(json.loads(result.stdout)['status_counts']['unable_to_verify'],1)

    def test_loading_branch_cannot_be_available_systemwide(self):
        r = self.result(entry(record(branch='Searching...')), branch=None)
        self.assertEqual((r['status_code'], r['confirmed_available']), ('unable_to_verify', 0))
        self.assertNotIn('Searching...', r['other_available_branches'])

    def test_record_id_must_match_observed_url(self):
        with self.assertRaises(ValueError):
            h.validate_record(record(record_id='1002', url=URL))

    def test_conflicting_copy_has_no_positive_edition_count(self):
        a = record(); a['items'][0]['item_id'] = 'same-copy'
        b = record('Checked out', record_id='1002'); b['items'][0]['item_id'] = 'same-copy'
        r = self.result(entry(a, b))
        self.assertEqual(r['confirmed_available'], 0)
        self.assertTrue(all(x['confirmed_available'] == 0 for x in r['editions']))

    def test_evidence_predating_run_is_not_fresh(self):
        r = self.result(entry(record(checked_at='2020-01-01T00:00:00+00:00')))
        self.assertEqual((r['status_code'], r['confirmed_available']), ('unable_to_verify', 0))

    def test_invalid_due_date_is_unknown(self):
        self.assertEqual(self.result(entry(record('Due 99/99/26')))['status_code'], 'unable_to_verify')

    def test_unknown_language_labels_are_unresolved(self):
        for language in [' ', 'Unknown', 'Searching...', 'Undetermined']:
            with self.subTest(language=language):
                self.assertEqual(self.result(entry(record(language=language)))['status_code'], 'unable_to_verify')

    def test_duplicate_item_id_within_record_has_consistent_counts(self):
        a = record(); a['items'][0]['item_id'] = 'copy-1'
        a['items'].append(copy.deepcopy(a['items'][0]))
        r = self.result(entry(a))
        self.assertEqual(r['confirmed_available'], 1)
        self.assertEqual(r['editions'][0]['confirmed_available'], 1)

    def test_cli_ingest_mark_resume_and_refresh(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'titles.json'; path=Path(tmp)/'ledger.json'; evidence=Path(tmp)/'record.json'
            source.write_text(json.dumps([{'title':'Dune','author':'Frank Herbert'}]))
            script=SKILL_ROOT/'scripts/hpl_evidence.py'
            def cli(*args):
                return subprocess.run([sys.executable,str(script),*map(str,args)],check=True,capture_output=True,text=True)
            cli('init','--titles',source,'--output',path,'--branch','Looscan')
            ledger=json.loads(path.read_text()); key=ledger['titles'][0]['key']
            from datetime import datetime, timezone
            evidence.write_text(json.dumps(record(run_id=ledger['run_id'], checked_at=datetime.now(timezone.utc).isoformat())))
            cli('ingest',path,'--key',key,'--record',evidence)
            cli('mark',path,'--key',key,'--search-complete','--editions-complete')
            self.assertEqual(json.loads(cli('pending',path).stdout), [])
            self.assertEqual(json.loads(cli('report',path).stdout)['results'][0]['status_code'],'available')
            cli('refresh',path)
            self.assertEqual(json.loads(cli('pending',path).stdout), [key])
            self.assertEqual(json.loads(cli('report',path).stdout)['results'][0]['confirmed_available'],0)
            before=path.read_bytes()
            attempt=subprocess.run([sys.executable,str(script),'ingest',str(path),'--key',key,'--record',str(evidence)],capture_output=True,text=True)
            self.assertEqual(attempt.returncode,2)
            self.assertEqual(path.read_bytes(),before)

    def test_blank_selected_scope_is_rejected(self):
        with self.assertRaises(ValueError):
            h.initialize([{'title':'Dune'}], ' ', 'English', 'thorough')

    def test_aggregate_reconciliation_uses_unique_item_ids(self):
        a = record(expected_copies=1, aggregate_available=1)
        a['items'][0]['item_id']='copy-1'; a['items'].append(copy.deepcopy(a['items'][0]))
        r = self.result(entry(a))
        self.assertEqual((r['completeness'], r['confirmed_available'], r['total']), ('complete',1,1))

    def test_edition_label_is_required(self):
        a=record(); del a['edition']
        with self.assertRaises(ValueError):
            h.validate_record(a)

    def test_query_provenance_is_required_when_url_has_query(self):
        a=record(); del a['query']
        with self.assertRaises(ValueError):
            h.validate_record(a)

    def test_unknown_edition_keeps_positive_evidence_partial(self):
        r=self.result(entry(record(edition='Unknown')))
        self.assertEqual((r['status_code'],r['completeness']),('available','partial'))

    def test_live_same_author_fixture_does_not_create_looscan_holding(self):
        fixture=json.loads((ROOT/'tests/fixtures/employees-live.json').read_text())
        a=record(record_id=fixture['matching_record_id'],title=fixture['matching_title'],author='Olga Ravn',items=h.normalize_table(fixture['matching_table']))
        b=record(record_id=fixture['unrelated_record_id'],title=fixture['unrelated_title'],author='Olga Ravn',match_state='excluded',items=h.normalize_table(fixture['unrelated_table']))
        r=self.result(entry(a,b,title='The Employees',author='Olga Ravn'))
        self.assertEqual((r['status_code'],r['confirmed_available'],r['total']),('no_branch_copy',0,0))
        self.assertEqual(r['other_available_branches'],['Heights','Kendall','Oak Forest'])


if __name__ == '__main__':
    unittest.main()
