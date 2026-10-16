import contextlib
import csv
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('transitions_tool', Path(__file__).with_name('transitions.py'))
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


class TransitionTests(unittest.TestCase):
    def setUp(self):
        scratch = Path('test/scratch')
        scratch.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def write(self, name, rows):
        path = self.root / name
        with path.open('w', encoding='utf-8', newline='') as f:
            csv.writer(f).writerows(rows)
        return path

    def compare(self, b, a, keys=('id',), columns=('v',)):
        return tool.transitions(self.write('b.csv', b), self.write('a.csv', a), keys, columns)

    def test_counts_order_and_no_key_values(self):
        r = self.compare([['id','v'],['private1','z'],['private2','x'],['private3','z']],
                         [['id','v'],['private3','a'],['private1','a'],['private2','b']])
        self.assertEqual(r['columns'][0]['transitions'], [
            {'before':'z','after':'a','rows':2}, {'before':'x','after':'b','rows':1}])
        self.assertNotIn('private', json.dumps(r))
        self.assertEqual(r['columns'][0]['changed_rows'], 3)

    def test_tie_sort_and_literal_values(self):
        r = self.compare([['id','v'],['1','01'],['2','a\nb']],
                         [['id','v'],['1','1'],['2','a\nb ']])
        self.assertEqual([t['before'] for t in r['columns'][0]['transitions']], ['01','a\nb'])
        self.assertEqual(r['summary']['changed'], 2)

    def test_ambiguity_never_pairs(self):
        r = self.compare([['id','v'],['x','a'],['x','a'],['y','b']],
                         [['id','v'],['x','c'],['y','c'],['y','c']])
        self.assertFalse(r['complete'])
        self.assertEqual(r['unpaired_records'], {'before':3,'after':3})
        self.assertEqual(r['columns'][0]['transitions'], [])

    def test_add_remove_are_not_transitions(self):
        r = self.compare([['id','v'],['x','a']], [['id','v'],['y','b']])
        self.assertEqual(r['columns'][0]['changed_rows'], 0)
        self.assertEqual((r['summary']['added'],r['summary']['removed']), (1,1))
        self.assertFalse(r['equal'])

    def test_unselected_edits_and_schema_keep_global_verdict(self):
        r = self.compare([['id','v','other'],['x','a','b']],
                         [['id','v','other','new'],['x','a','c','d']])
        self.assertFalse(r['equal'])
        self.assertEqual(r['summary']['changed'], 1)
        self.assertEqual(r['columns'][0]['transitions'], [])
        self.assertEqual(r['schema']['added_columns'], ['new'])

    def test_composite_keys_and_multiple_columns(self):
        r = self.compare([['id','part','v','w'],['a','1','x','y'],['a','2','z','y']],
                         [['id','part','v','w'],['a','1','z','q'],['a','2','z','q']],
                         ('id','part'), ('w','v'))
        self.assertTrue(r['complete'])
        self.assertEqual([c['changed_rows'] for c in r['columns']], [2,1])
        self.assertEqual(sum(c['changed_rows'] for c in r['columns']), 3)
        self.assertEqual(r['summary']['changed'], 2)

    def test_empty_key_retains_literal_semantics(self):
        r = self.compare([['id','v'],['','']], [['id','v'],['','x']])
        self.assertTrue(r['complete'])
        self.assertEqual(r['columns'][0]['transitions'][0]['before'], '')

    def test_equal_reorder_and_header_only(self):
        r = self.compare([['id','v'],['a','x'],['b','y']], [['v','id'],['y','b'],['x','a']])
        self.assertTrue(r['equal'])
        self.assertTrue(self.compare([['id','v']], [['v','id']])['equal'])

    def test_invalid_selection_and_input(self):
        b = self.write('b.csv', [['id','v'],['a','x']])
        a = self.write('a.csv', [['id','v'],['a','y']])
        for keys, cols in [(('id',),()),(('id',),('id',)),(('id',),('v','v')),
                           (('id',),('missing',)),(('id','id'),('v',))]:
            with self.assertRaises(ValueError):
                tool.transitions(b,a,keys,cols)
        malformed = self.write('bad.csv', [['id','v'],['too-short']])
        with self.assertRaises(ValueError):
            tool.transitions(b,malformed,('id',),('v',))
        schema = self.write('schema.csv', [['id','other']])
        with self.assertRaises(ValueError):
            tool.transitions(b,schema,('id',),('v',))

    def test_cli_statuses_no_partial_output_and_escaped_controls(self):
        b = self.write('b.csv', [['id','v'],['x','\x1b[31m']])
        a = self.write('a.csv', [['id','v'],['x','y']])
        for candidate, status in [(b,0),(a,1),(self.root/'missing',2)]:
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = tool.main([str(b),str(candidate),'--key','id','--column','v'])
            self.assertEqual(code,status)
            self.assertNotIn('\x1b', out.getvalue()+err.getvalue())
            if status == 2:
                self.assertEqual(out.getvalue(),'')
            else:
                json.loads(out.getvalue())

    def test_trace_composite_keys_reordering_and_multiline_records(self):
        b = self.write('b.csv', [['id','part','v'],['b','2','old\nvalue'],['a','1','old\nvalue']])
        a = self.write('a.csv', [['part','v','id'],['1','new','a'],['2','new','b']])
        report = tool.transitions(b, a, ('id','part'), ('v',), include_records=True)
        group = report['columns'][0]['transitions'][0]
        self.assertEqual(group['rows'], len(group['records']))
        self.assertEqual(group['records'], [
            {'key':{'id':'a','part':'1'},'before_record':3,'after_record':2},
            {'key':{'id':'b','part':'2'},'before_record':2,'after_record':3}])
        default = tool.transitions(b, a, ('id','part'), ('v',))
        del group['records']
        self.assertEqual(report, default)

    def test_trace_excludes_duplicates_and_unselected_changes(self):
        b = self.write('b.csv', [['id','v','w'],['dup','a','x'],['dup','a','x'],['ok','a','x'],['other','a','x']])
        a = self.write('a.csv', [['id','v','w'],['dup','b','y'],['ok','b','y'],['other','a','y']])
        r = tool.transitions(b, a, ('id',), ('v','w'), True)
        self.assertFalse(r['complete'])
        self.assertEqual(r['columns'][0]['transitions'][0]['records'], [
            {'key':{'id':'ok'},'before_record':4,'after_record':3}])
        self.assertEqual([m['key']['id'] for m in r['columns'][1]['transitions'][0]['records']], ['ok','other'])

    def test_trace_cli_escapes_keys_and_keeps_global_verdict(self):
        b = self.write('b.csv', [['id','v'],['\x1b[31m','a'],['removed','z']])
        a = self.write('a.csv', [['id','v'],['\x1b[31m','b']])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = tool.main([str(b), str(a), '--key','id','--column','v','--include-records'])
        self.assertEqual(code, 1)
        self.assertNotIn('\x1b', out.getvalue())
        r = json.loads(out.getvalue())
        self.assertEqual(r['summary']['removed'], 1)
        self.assertEqual(r['columns'][0]['transitions'][0]['records'][0]['key'], {'id':'\x1b[31m'})

    def test_trace_empty_transition_list(self):
        b = self.write('b.csv', [['id','v'],['x','a']])
        r = tool.transitions(b,b,('id',),('v',),True)
        self.assertTrue(r['equal'])
        self.assertEqual(r['columns'][0]['transitions'], [])


if __name__ == '__main__':
    unittest.main()
