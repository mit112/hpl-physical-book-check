"""Synthetic batch execution; these records are not live HPL observations."""
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/hpl-physical-book-check/scripts'))
import hpl_evidence as h


class WorkQueueTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / 'ledger.json'

    def cli(self, *args: object) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(Path(h.__file__)), *map(str, args)],
            capture_output=True, text=True, check=False)

    def initialize(self, count: int = 3, *options: str) -> dict:
        source = self.path.with_name('titles.json')
        source.write_text(json.dumps([
            dict(title=f'Simulated winner {i}', author=f'Simulated author {i}',
                 labels=[f'Simulated award {i}']) for i in range(count)]))
        result = self.cli('init', '--titles', source, '--output', self.path,
                          '--branch', 'Looscan', *options)
        self.assertEqual(result.returncode, 0, result.stderr)
        return h.read_json(self.path)

    def ingest(self, index: int, *, complete: bool = True,
               status: str = 'Available') -> None:
        ledger = h.read_json(self.path)
        title = ledger['titles'][index]
        evidence = self.path.with_name('record.json')
        evidence.write_text(json.dumps(dict(
            record_id=str(index + 1),
            url=f'https://halan.sdp.sirsi.net/client/en_US/hou/search/detailnonmodal/ent:$002f$002fSD_ILS$002f0$002fSD_ILS:{index + 1}/ada',
            title=title['title'], author=title['author'], format='Books',
            edition='Regular print', language='English', match_state='exact',
            holdings_complete=complete, run_id=ledger['run_id'],
            checked_at=datetime.now(timezone.utc).isoformat(),
            items=[dict(branch='Looscan', material_type='Book', raw_status=status)])))
        result = self.cli('ingest', self.path, '--key', title['key'], '--record', evidence)
        self.assertEqual(result.returncode, 0, result.stderr)
        if complete:
            result = self.cli('mark', self.path, '--key', title['key'],
                              '--search-complete', '--editions-complete')
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_79_work_run_rejects_two_title_sample_and_resumes_to_completion(self) -> None:
        ledger = self.initialize(79)
        self.ingest(0, complete=False)
        self.ingest(1, complete=False, status='Checked out')
        before = self.path.read_bytes()
        result = self.cli('finalize', self.path)
        self.assertEqual(result.returncode, 1, result.stderr)
        gate = json.loads(result.stdout)
        self.assertEqual((gate['state'], gate['remaining'], gate['satisfied']),
                         ('continue', 79, 0))
        self.assertEqual(gate['report']['coverage_counts'],
                         dict(complete=0, partial=2, unverified=77))
        self.assertEqual(self.path.read_bytes(), before)
        first = self.cli('next', self.path)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(self.cli('next', self.path).stdout, first.stdout)
        self.assertEqual(self.path.read_bytes(), before)
        indices = {title['key']: index for index, title in enumerate(ledger['titles'])}
        visited = []
        for expected_size in [10, 10, 10, 10, 10, 10, 10, 9]:
            result = self.cli('next', self.path)
            self.assertEqual(result.returncode, 0, result.stderr)
            batch = json.loads(result.stdout)['next_batch']
            self.assertEqual(len(batch), expected_size)
            for title in batch:
                self.assertNotIn(title['key'], visited)
                visited.append(title['key'])
                self.ingest(indices[title['key']])
        result = self.cli('finalize', self.path)
        self.assertEqual(result.returncode, 0, result.stderr)
        gate = json.loads(result.stdout)
        self.assertEqual((gate['state'], gate['remaining'], gate['satisfied']),
                         ('complete', 0, 79))
        self.assertEqual(len(visited), 79)
        self.assertEqual(gate['report']['results'][0]['labels'], ['Simulated award 0'])

    def test_isolated_blocker_does_not_starve_other_titles_and_can_resume(self) -> None:
        ledger = self.initialize()
        key = ledger['titles'][0]['key']
        result = self.cli('checkpoint', self.path, '--key', key, '--kind', 'access',
                          '--detail', 'One record still fails after permitted recovery.',
                          '--evidence', 'Simulated holdings-view timeout after reopen.')
        self.assertEqual(result.returncode, 0, result.stderr)
        queue = json.loads(self.cli('next', self.path).stdout)
        self.assertEqual(queue['state'], 'continue')
        self.assertEqual([x['title'] for x in queue['next_batch']],
                         ['Simulated winner 1', 'Simulated winner 2'])
        self.ingest(1)
        self.ingest(2)
        result = self.cli('finalize', self.path)
        self.assertEqual(result.returncode, 1, result.stderr)
        gate = json.loads(result.stdout)
        self.assertEqual((gate['state'], gate['remaining']), ('blocked', 1))
        self.assertEqual(gate['blockers'][0]['key'], key)
        self.assertIn('timeout', gate['blockers'][0]['evidence'])
        self.assertEqual(self.cli('resume', self.path, '--key', key).returncode, 0)
        queue = json.loads(self.cli('next', self.path).stdout)
        self.assertEqual([x['key'] for x in queue['next_batch']], [key])

    def test_global_checkpoint_preserves_partial_results_without_passing_gate(self) -> None:
        self.initialize()
        self.ingest(0, complete=False)
        result = self.cli('checkpoint', self.path, '--kind', 'host_limit',
                          '--detail', 'Host disallowed further browser calls.',
                          '--evidence', 'Simulated tool response: session action limit reached.')
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.cli('finalize', self.path)
        self.assertEqual(result.returncode, 1, result.stderr)
        gate = json.loads(result.stdout)
        self.assertEqual((gate['state'], gate['remaining']), ('blocked', 3))
        self.assertEqual(gate['next_batch'], [])
        self.assertEqual(gate['report']['results'][0]['confirmed_available'], 1)
        self.assertEqual(len(gate['blockers']), 3)
        self.assertEqual(self.cli('resume', self.path).returncode, 0)
        self.assertEqual(json.loads(self.cli('next', self.path).stdout)['state'], 'continue')

    def test_checkpoint_requires_observed_evidence_and_does_not_mutate_on_error(self) -> None:
        self.initialize()
        before = self.path.read_bytes()
        result = self.cli('checkpoint', self.path, '--kind', 'access',
                          '--detail', 'Cannot load holdings.', '--evidence', ' ')
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn('evidence', result.stderr.lower())
        self.assertEqual(self.path.read_bytes(), before)

    def test_quick_positive_satisfies_one_title_without_hiding_partial_coverage(self) -> None:
        self.initialize(2, '--mode', 'quick')
        self.ingest(0, complete=False)
        self.ingest(1, complete=False, status='Checked out')
        self.assertEqual(self.cli('finalize', self.path).returncode, 1)
        queue = json.loads(self.cli('next', self.path).stdout)
        self.assertEqual([x['title'] for x in queue['next_batch']], ['Simulated winner 1'])
        self.ingest(1, status='Checked out')
        result = self.cli('finalize', self.path)
        self.assertEqual(result.returncode, 0, result.stderr)
        gate = json.loads(result.stdout)
        self.assertEqual(gate['state'], 'complete')
        self.assertEqual(gate['report']['coverage_counts']['partial'], 1)

    def test_any_one_quick_request_stops_whole_queue_after_positive(self) -> None:
        self.initialize(3, '--mode', 'quick', '--any-one')
        self.ingest(1, complete=False)
        result = self.cli('finalize', self.path)
        self.assertEqual(result.returncode, 0, result.stderr)
        gate = json.loads(result.stdout)
        self.assertEqual((gate['state'], gate['remaining'], gate['next_batch']),
                         ('complete', 0, []))
        self.assertEqual(gate['report']['coverage_counts']['unverified'], 2)

    def test_refresh_invalidates_blockers_and_quick_success(self) -> None:
        self.initialize(2, '--mode', 'quick')
        self.ingest(0, complete=False)
        self.assertEqual(self.cli('checkpoint', self.path, '--kind', 'access',
                                 '--detail', 'Site blocked.', '--evidence',
                                 'Simulated challenge after recovery.').returncode, 0)
        self.assertEqual(json.loads(self.cli('finalize', self.path).stdout)['state'], 'blocked')
        self.assertEqual(self.cli('refresh', self.path).returncode, 0)
        result = self.cli('finalize', self.path)
        self.assertEqual(result.returncode, 1, result.stderr)
        gate = json.loads(result.stdout)
        self.assertEqual((gate['state'], gate['remaining'], gate['blockers']),
                         ('continue', 2, []))
        self.assertEqual(gate['report']['results'][0]['confirmed_available'], 0)

    def test_empty_request_cannot_pass_completion_gate(self) -> None:
        ledger = self.initialize()
        ledger['titles'] = []
        h.write_json(self.path, ledger)
        result = self.cli('finalize', self.path)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn('empty', result.stderr.lower())

    def test_any_one_requires_explicit_quick_mode(self) -> None:
        self.initialize()
        target = self.path.with_name('invalid-ledger.json')
        result = self.cli('init', '--titles', self.path.with_name('titles.json'),
                          '--output', target, '--branch', 'Looscan', '--any-one')
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn('quick', result.stderr.lower())
        self.assertFalse(target.exists())

    def test_duplicate_work_preserves_all_award_labels(self) -> None:
        ledger = h.initialize([
            dict(title='A winner', author='An author', labels=['2024 Fiction']),
            dict(title='A winner', author='An author', labels=['2025 Audiobook'])
        ], 'Looscan', 'English', 'thorough')
        self.assertEqual(len(ledger['titles']), 1)
        self.assertEqual(ledger['titles'][0].get('labels'),
                         ['2024 Fiction', '2025 Audiobook'])

    def test_malformed_title_keys_cannot_hide_unfinished_work(self) -> None:
        base = self.initialize()
        for mutation in ['duplicate', 'blank', 'missing']:
            with self.subTest(mutation=mutation):
                ledger = json.loads(json.dumps(base))
                if mutation == 'duplicate':
                    ledger['titles'][1]['key'] = ledger['titles'][0]['key']
                elif mutation == 'blank':
                    ledger['titles'][0]['key'] = ' '
                else:
                    ledger['titles'][0].pop('key')
                h.write_json(self.path, ledger)
                before = self.path.read_bytes()
                result = self.cli('finalize', self.path)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn('key', result.stderr.lower())
                self.assertEqual(self.path.read_bytes(), before)

    def test_nonobject_ledger_is_invalid_input_without_traceback(self) -> None:
        for value in [None, [], 'ledger']:
            with self.subTest(value=value):
                h.write_json(self.path, value)
                before = self.path.read_bytes()
                result = self.cli('finalize', self.path)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertNotIn('Traceback', result.stderr)
                self.assertEqual(self.path.read_bytes(), before)

    def test_malformed_blocker_cannot_excuse_unfinished_work(self) -> None:
        base = self.initialize()
        valid = dict(kind='access', detail='Catalog blocked.', evidence='Simulated challenge.',
                     run_id=base['run_id'], checked_at=datetime.now(timezone.utc).isoformat())
        for field, value in [('kind', 'too_many_books'), ('detail', ' '),
                             ('evidence', ' '), ('run_id', 'another-run'),
                             ('checked_at', '2026-10-16T12:00:00'),
                             ('checked_at', '2020-01-01T00:00:00+00:00'),
                             ('checked_at', '2999-01-01T00:00:00+00:00')]:
            with self.subTest(field=field, value=value):
                ledger = json.loads(json.dumps(base))
                ledger['blocker'] = dict(valid, **{field: value})
                h.write_json(self.path, ledger)
                before = self.path.read_bytes()
                result = self.cli('finalize', self.path)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(self.path.read_bytes(), before)
        base['blocker'] = valid
        h.write_json(self.path, base)
        result = self.cli('finalize', self.path)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(result.stdout)['state'], 'blocked')


if __name__ == '__main__':
    unittest.main()
