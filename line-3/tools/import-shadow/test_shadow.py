import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
import shadow


class ShadowTests(unittest.TestCase):
    def inspect(self, sources, names=('json',)):
        return shadow.inspect_sources(sources, shadow.load_budget().load_mapper(), names)

    def test_links_aliases_from_and_dotted_imports(self):
        r = self.inspect({'app.py': b'import json as j, json.decoder\nfrom json import loads, dumps',
                          'json.py': b'raise RuntimeError("never execute")'})
        self.assertEqual(r['summary']['linked_sites'], 4)
        self.assertEqual([s['alias_index'] for s in r['candidates'][0]['sites']], [0, 1, 0, 1])

    def test_relative_and_unrelated_imports_excluded(self):
        r = self.inspect({'pkg/app.py': b'from . import json\nfrom .json import x\nimport other',
                          'json.py': b''})
        self.assertEqual(r['summary']['linked_sites'], 0)

    def test_nested_names_are_not_top_level_collisions(self):
        r = self.inspect({'pkg/json.py': b'', 'app.py': b'import json'})
        self.assertEqual(r['candidates'], [])

    def test_namespace_not_reported_as_regular_shadow(self):
        r = self.inspect({'json/custom.py': b'', 'app.py': b'import json'})
        self.assertEqual(r['candidates'], [])
        self.assertEqual(r['namespace_only'][0]['name'], 'json')

    def test_regular_package_wins_collision_and_shadowed_not_parsed(self):
        r = self.inspect({'json.py': b'bad syntax ?!', 'json/__init__.py': b'',
                          'app.py': b'import json'})
        self.assertEqual(r['candidates'][0]['selected'], 'json/__init__.py')
        self.assertEqual([i['type'] for i in r['issues']], ['module_collision'])

    def test_parse_errors_retained_and_unused_candidates_visible(self):
        r = self.inspect({'json.py': b'', 'app.py': b'bad syntax ?!'})
        self.assertEqual(r['summary']['candidates'], 1)
        self.assertEqual(r['issues'][0]['type'], 'parse_error')

    def test_nested_condition_and_encoding(self):
        r = self.inspect({'json.py': b'', 'app.py': b'# coding: latin-1\n# caf\xe9\nif False:\n import json'})
        self.assertEqual(r['candidates'][0]['sites'][0]['line'], 4)

    def test_catalog_replacement_and_validation(self):
        r = self.inspect({'vendor.py': b'', 'json.py': b''}, ('vendor',))
        self.assertEqual([c['name'] for c in r['candidates']], ['vendor'])
        for names in ([], [''], ['pkg.child'], ['bad-name']):
            with self.assertRaises(ValueError):
                self.inspect({}, names)

    def test_root_initializer_ignored(self):
        self.assertEqual(self.inspect({'__init__.py': b'import json', 'json.py': b''})['summary']['linked_sites'], 0)

    def test_cli_manifest_strict_budget_and_symlinks(self):
        scratch = Path('test/scratch/import-shadow')
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as tmp:
            root = Path(tmp)
            (root / 'json.py').write_text('raise RuntimeError("must not execute")\n')
            (root / 'app.py').write_text('import json\n')
            (root / 'link.py').symlink_to('json.py')
            def run(args):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    code = shadow.main([str(root), '--json'] + args)
                return code, json.loads(out.getvalue())
            code, result = run(['--strict'])
            self.assertEqual(code, 1)
            self.assertEqual(result['inventory']['files'], 2)
            self.assertEqual(result['inventory']['skipped_symlinks'], 1)
            self.assertEqual(len(result['inventory']['manifest'][0]['sha256']), 64)
            code, refused = run(['--max-files', '1'])
            self.assertEqual(code, 2)
            self.assertEqual(refused['status'], 'refused')
            self.assertNotIn('candidates', refused)
            self.assertEqual(run(['--names', 'other'])[0], 0)


if __name__ == '__main__':
    unittest.main()
