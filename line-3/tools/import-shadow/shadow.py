#!/usr/bin/env python3
"""Find local sources sharing names with an explicit reserved-name catalog."""
import argparse
import ast
import importlib.util
import json
from pathlib import Path
import sys

# Deliberately fixed, portable review baseline, not an inventory of this machine.
DEFAULT_NAMES = frozenset('argparse ast asyncio collections concurrent contextlib copy csv dataclasses datetime decimal email enum fractions functools hashlib heapq http importlib inspect io itertools json logging math multiprocessing operator os pathlib pickle platform queue random re secrets shutil signal socket sqlite3 ssl statistics string subprocess sys tempfile threading time tkinter tokenize traceback types typing unittest urllib uuid warnings weakref xml zipfile zoneinfo'.split())
SCOPE = ('Name collisions are review candidates, not runtime resolution. The explicit '
         'root is an import search root. Only top-level .py modules and regular packages '
         'can shadow a reserved name; namespace-only directories are reported separately '
         'because a later regular package can take precedence. Absolute import syntax '
         'is linked to candidates; relative imports are excluded. No source is executed. '
         'sys.modules, built-in/frozen precedence, loaders and actual sys.path are unknown. '
         'The fixed catalog is a common standard-library subset, not an exhaustive '
         'Python-version inventory. --names replaces it for other review catalogs.')


def load_budget():
    path = Path(__file__).resolve().parents[1] / 'import-budget' / 'budget.py'
    spec = importlib.util.spec_from_file_location('line3_shadow_budget', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def inspect_sources(sources, mapper, names=DEFAULT_NAMES):
    names = sorted(set(names))
    if not names or any(not n.isidentifier() or '.' in n for n in names):
        raise ValueError('catalog needs one or more top-level Python identifiers')
    catalog = {}
    for path in sorted(sources):
        module = mapper.module_name(Path(path))
        if module:
            catalog.setdefault(module, []).append(path)
    candidates, namespaces = [], []
    for name in names:
        paths = catalog.get(name, [])
        if paths:
            selected = min(paths, key=lambda p: (Path(p).name != '__init__.py', p))
            candidates.append({'name': name, 'selected': selected,
                               'source_paths': paths, 'sites': []})
        elif any(module.startswith(name + '.') for module in catalog):
            namespaces.append({'name': name, 'descendants': sorted(
                module for module in catalog if module.startswith(name + '.'))})
    lookup = {c['name']: c for c in candidates}
    issues = []
    for module, paths in sorted(catalog.items()):
        path = min(paths, key=lambda p: (Path(p).name != '__init__.py', p))
        if len(paths) > 1:
            issues.append({'type': 'module_collision', 'path': path,
                           'module': module, 'source_paths': paths})
        try:
            tree = ast.parse(sources[path], filename=path)
        except (SyntaxError, UnicodeError, ValueError) as exc:
            issues.append({'type': 'parse_error', 'path': path,
                           'line': getattr(exc, 'lineno', None), 'detail': str(exc)})
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                requests = [(i, alias.name) for i, alias in enumerate(node.names)]
            elif isinstance(node, ast.ImportFrom) and not node.level and node.module:
                requests = [(i, node.module) for i, _ in enumerate(node.names)]
            else:
                continue
            for index, target in requests:
                name = target.split('.')[0]
                if name in lookup:
                    lookup[name]['sites'].append({'path': path, 'module': module,
                        'line': node.lineno, 'column': node.col_offset,
                        'alias_index': index, 'target': target,
                        'imported_name': node.names[index].name,
                        'kind': 'from' if isinstance(node, ast.ImportFrom) else 'import'})
    for candidate in candidates:
        candidate['sites'].sort(key=lambda s: (s['path'], s['line'], s['column'], s['alias_index']))
    return {'catalog': names, 'candidates': candidates, 'namespace_only': namespaces,
            'issues': issues, 'summary': {'candidates': len(candidates),
                'linked_sites': sum(len(c['sites']) for c in candidates),
                'namespace_only': len(namespaces), 'issues': len(issues)}}


def analyze(root, limits=None, names=DEFAULT_NAMES):
    budget = load_budget()
    mapper = budget.load_mapper()
    limits = dict(budget.DEFAULTS if limits is None else limits)
    sources, inventory = budget.collect(root, limits, mapper.SKIP_DIRS)
    return dict(inspect_sources(sources, mapper, names), status='complete',
                limits=limits, inventory=inventory, scope=SCOPE,
                collection_scope=budget.SCOPE)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--names', help='replace catalog with comma-separated top-level names')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--strict', action='store_true', help='exit 1 on candidates or source issues')
    budget = load_budget()
    for key, default in budget.DEFAULTS.items():
        parser.add_argument('--max-' + key.replace('_', '-'), dest=key, type=int, default=default)
    args = parser.parse_args(argv)
    try:
        names = DEFAULT_NAMES if args.names is None else [n.strip() for n in args.names.split(',')]
        # Validate even for empty source trees, before collection.
        inspect_sources({}, budget.load_mapper(), names)
        result = analyze(args.root, {k: getattr(args, k) for k in budget.DEFAULTS}, names)
    except (OSError, ValueError, RuntimeError, RecursionError) as exc:
        print(json.dumps({'status': 'refused', 'error': getattr(exc, 'evidence',
                         {'type': 'scan_error', 'detail': str(exc)})}, indent=2))
        return 2
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        for c in result['candidates']:
            print(f"Review {c['name']}: {c['selected']} ({len(c['sites'])} absolute import sites)")
            for s in c['sites']:
                print(f"  {s['path']}:{s['line']}:{s['column']} {s['kind']} {s['target']}")
        for n in result['namespace_only']:
            print('Namespace only (not a regular shadow): ' + n['name'])
        for issue in result['issues']:
            print('Issue: ' + json.dumps(issue))
        print(json.dumps(result['summary'], sort_keys=True))
        print(SCOPE)
    return int(bool(args.strict and (result['candidates'] or result['issues'])))


if __name__ == '__main__':
    sys.exit(main())
