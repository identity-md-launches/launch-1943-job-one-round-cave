import csv
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import origin_csv as tool


class OriginCSVTests(unittest.TestCase):
    def setUp(self):
        Path('test/scratch').mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir='test/scratch')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source'
        self.source.mkdir()

    def put(self, name, text):
        path = self.source / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def save(self, name, text):
        path = self.root / name
        path.write_text(text)
        return path

    def test_origin_edit_changes_hash_without_running_source(self):
        self.put('app.py', 'raise RuntimeError("never run")\nfrom facade import launch\n')
        self.put('facade.py', 'from impl import run as launch\n')
        impl = self.put('impl.py', 'def run(): return 1\n')
        before, evidence = tool.snapshot(self.source)
        impl.write_text('def run(): return 2\n')
        after, _ = tool.snapshot(self.source)
        result = tool.compare(self.save('b.csv', before), self.save('a.csv', after))
        self.assertFalse(result['comparison']['equal'])
        self.assertEqual(result['comparison']['summary']['changed'], 2)
        self.assertTrue(all('origins' in row['fields'] for row in result['comparison']['changed']))
        self.assertEqual(result['status_transitions']['columns'][0]['changed_rows'], 0)
        self.assertEqual(evidence['status_counts'], {'resolved': 2})

    def test_resolution_transition_retains_exact_records(self):
        self.put('app.py', 'from impl import run\n')
        impl = self.put('impl.py', 'other = 1\n')
        before, _ = tool.snapshot(self.source)
        impl.write_text('def run(): pass\n')
        after, _ = tool.snapshot(self.source)
        r = tool.compare(self.save('b.csv', before), self.save('a.csv', after))
        group = r['status_transitions']['columns'][0]['transitions'][0]
        self.assertEqual((group['before'], group['after'], group['rows']), ('unresolved', 'resolved', 1))
        self.assertEqual(group['records'], [{'key': {'path': 'app.py', 'line': '1', 'site_index': '0'}, 'before_record': 2, 'after_record': 2}])

    def test_duplicate_import_names_keep_separate_coordinate_keys(self):
        app = self.put('app.py', 'from impl import run, run; from impl import run\n')
        self.put('impl.py', 'def run(): pass\n')
        before, _ = tool.snapshot(self.source)
        rows = list(csv.DictReader(io.StringIO(before)))
        self.assertEqual([r['site_index'] for r in rows], ['0', '1', '2'])
        app.write_text('\n' + app.read_text())
        after, _ = tool.snapshot(self.source)
        r = tool.compare(self.save('b.csv', before), self.save('a.csv', after))
        self.assertEqual(r['comparison']['summary']['added'], 3)
        self.assertEqual(r['comparison']['summary']['removed'], 3)

    def test_wildcards_parse_issues_and_self_equality_keep_limits(self):
        self.put('app.py', 'from impl import *\n')
        self.put('broken.py', 'def broken(\n')
        text, evidence = tool.snapshot(self.source)
        self.assertEqual(evidence['status_counts'], {'unresolved': 1})
        self.assertEqual(len(evidence['issues']), 1)
        path = self.save('same.csv', text)
        result = tool.compare(path, path)
        self.assertTrue(result['comparison']['equal'])
        self.assertIn('does not certify', result['scope'])
        row = next(csv.DictReader(io.StringIO(text)))
        self.assertEqual(row['reason'], 'wildcard_import')

    def test_duplicate_invalid_keys_and_schema_refused(self):
        self.put('app.py', 'from os import path\n')
        text, _ = tool.snapshot(self.source)
        row = next(csv.DictReader(io.StringIO(text)))
        for key, value in [('path', ''), ('line', '0'), ('line', '01'), ('site_index', '-1')]:
            stream = io.StringIO(); writer = csv.DictWriter(stream, tool.COLUMNS)
            writer.writeheader(); writer.writerow(dict(row, **{key: value}))
            p = self.save('bad.csv', stream.getvalue())
            with self.assertRaises(ValueError): tool.compare(p, p)
        p = self.save('dup.csv', text + text.splitlines(keepends=True)[1])
        with self.assertRaises(ValueError): tool.compare(p, p)
        p = self.save('schema.csv', 'path,line,site_index\na,1,0\n')
        with self.assertRaises(ValueError): tool.compare(p, p)

    def test_cli_warning_and_budget_refusal_have_no_partial_csv(self):
        self.put('app.py', 'from missing import name\n')
        self.put('other.py', '')
        command = [sys.executable, '-B', str(Path(tool.__file__)), 'snapshot', str(self.source)]
        r = subprocess.run(command, capture_output=True, text=True, timeout=10)
        self.assertEqual(r.returncode, 1)
        self.assertTrue(r.stdout.startswith(','.join(tool.COLUMNS)))
        self.assertEqual(json.loads(r.stderr)['status_counts'], {'unresolved': 1})
        r = subprocess.run(command + ['--max-files', '1'], capture_output=True, text=True, timeout=10)
        self.assertEqual(r.returncode, 2)
        self.assertEqual(r.stdout, '')
        self.assertEqual(json.loads(r.stderr)['status'], 'refused')

    def test_empty_snapshot_comparison(self):
        text, evidence = tool.snapshot(self.source)
        self.assertEqual(evidence['status_counts'], {})
        path = self.save('empty.csv', text)
        self.assertTrue(tool.compare(path, path)['comparison']['equal'])


if __name__ == '__main__':
    unittest.main()
