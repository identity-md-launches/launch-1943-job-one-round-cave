#!/usr/bin/env python3
"""Trace explicit local ``from ... import name`` re-exports to source definitions."""
import argparse
import ast
import importlib.util
import json
from pathlib import Path
import sys


def load_budget():
    path = Path(__file__).resolve().with_name('budget.py')
    spec = importlib.util.spec_from_file_location('line3_origin_budget', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_bindings(sources, map_report, mapper):
    """Index module-scope names from one bounded snapshot; never execute source."""
    records = {record['module']: record for record in map_report['modules']}
    modules = set(records)
    bindings = {}
    parse_failures = {item['path'] for item in map_report['issues']
                      if item['type'] == 'parse_error'}
    for module, record in sorted(records.items()):
        if record['path'] in parse_failures:
            continue
        tree = ast.parse(sources[record['path']], filename=record['path'])
        is_package = Path(record['path']).name == '__init__.py'
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                add(bindings, module, node.name, {'kind': 'definition', 'line': node.lineno,
                    'path': record['path'], 'definition': type(node).__name__})
            elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for target in targets:
                    for name in target_names(target):
                        add(bindings, module, name, {'kind': 'definition',
                            'line': node.lineno, 'path': record['path'],
                            'definition': type(node).__name__})
            elif isinstance(node, ast.ImportFrom):
                anchor = (mapper.relative_anchor(module, is_package, node.level, node.module)
                          if node.level else node.module)
                for alias in node.names:
                    name = alias.asname or alias.name
                    if alias.name == '*':
                        add(bindings, module, '*', {'kind': 'wildcard', 'line': node.lineno,
                            'path': record['path'], 'target': anchor})
                    elif anchor in modules:
                        child = anchor + '.' + alias.name
                        target_module = child if child in modules else anchor
                        add(bindings, module, name, {'kind': 'reexport',
                            'line': node.lineno, 'path': record['path'],
                            'target_module': target_module,
                            'target_symbol': None if target_module == child else alias.name,
                            'spelling': ('.' * node.level) + (node.module or '') +
                                        ' import ' + alias.name})
                    else:
                        add(bindings, module, name, {'kind': 'unresolved_import',
                            'line': node.lineno, 'path': record['path'],
                            'target_module': anchor, 'target_symbol': alias.name,
                            'spelling': ('.' * node.level) + (node.module or '') +
                                        ' import ' + alias.name})
    return bindings, {name: record['path'] for name, record in records.items()}


def add(bindings, module, name, item):
    bindings.setdefault((module, name), []).append(item)


def target_names(node):
    if isinstance(node, ast.Name):
        return [node.id]
    if isinstance(node, (ast.Tuple, ast.List)):
        return [name for child in node.elts for name in target_names(child)]
    return []


def trace(module, symbol, bindings, module_paths=None, seen=()):
    key = (module, symbol)
    step = {'module': module, 'symbol': symbol}
    if key in seen:
        return {'status': 'cycle', 'chain': [{'module': m, 'symbol': s}
                for m, s in seen] + [step], 'origins': []}
    choices = bindings.get(key, [])
    if len(choices) != 1:
        status = 'unresolved' if not choices else 'ambiguous'
        return {'status': status, 'reason': 'no_module_scope_binding' if not choices else
                'multiple_module_scope_bindings', 'chain': [
                    {'module': m, 'symbol': s} for m, s in seen] + [step], 'origins': []}
    item = choices[0]
    chain = [{'module': m, 'symbol': s} for m, s in seen] + [step]
    if item['kind'] == 'definition':
        return {'status': 'resolved', 'chain': chain,
                'origins': [{'module': module, 'symbol': symbol, 'path': item['path'],
                             'line': item['line'], 'kind': item['definition']}]}
    if item['kind'] == 'wildcard':
        return {'status': 'unresolved', 'reason': 'wildcard_import',
                'chain': chain, 'origins': []}
    target_module, target_symbol = item['target_module'], item['target_symbol']
    if item['kind'] == 'unresolved_import':
        return {'status': 'unresolved', 'reason': 'nonlocal_or_unresolved_import',
                'chain': chain + [{'module': target_module, 'symbol': target_symbol}],
                'origins': []}
    if target_symbol is None:
        target_path = (module_paths or {}).get(target_module)
        return {'status': 'resolved_module', 'chain': chain,
                'origins': [{'module': target_module, 'symbol': None,
                             'path': target_path, 'line': item['line'],
                             'kind': 'module_import'}]}
    return trace(target_module, target_symbol, bindings, module_paths, seen + (key,))


def analyze(root, limits=None):
    budget = load_budget()
    mapper = budget.load_mapper()
    limits = dict(budget.DEFAULTS if limits is None else limits)
    sources, inventory = budget.collect(root, limits, mapper.SKIP_DIRS)
    report = mapper.inspect(Path(root), source_bytes=sources)
    bindings, module_paths = build_bindings(sources, report, mapper)
    sites = []
    parse_failures = {item['path'] for item in report['issues']
                      if item['type'] == 'parse_error'}
    for module, record in sorted({r['module']: r for r in report['modules']}.items()):
        if record['path'] in parse_failures:
            continue
        tree = ast.parse(sources[record['path']], filename=record['path'])
        for node in tree.body:
            if not isinstance(node, ast.ImportFrom):
                continue
            anchor = (mapper.relative_anchor(module, Path(record['path']).name == '__init__.py',
                      node.level, node.module) if node.level else node.module)
            for alias in node.names:
                if alias.name == '*':
                    sites.append({'module': module, 'path': record['path'], 'line': node.lineno,
                        'name': '*', 'status': 'unresolved', 'reason': 'wildcard_import',
                        'chain': [{'module': module, 'symbol': '*'}], 'origins': []})
                    continue
                child = anchor + '.' + alias.name if anchor else None
                if child in {r['module'] for r in report['modules']}:
                    outcome = {'status': 'resolved_module',
                               'chain': [{'module': module, 'symbol': alias.asname or alias.name}],
                               'origins': [{'module': child, 'symbol': None,
                                            'path': next(r['path'] for r in report['modules']
                                                         if r['module'] == child),
                                            'line': node.lineno, 'kind': 'module_import'}]}
                elif anchor in {r['module'] for r in report['modules']}:
                    outcome = trace(anchor, alias.name, bindings, module_paths)
                    outcome['chain'].insert(0, {'module': module,
                                                'symbol': alias.asname or alias.name})
                else:
                    outcome = {'status': 'unresolved', 'reason': 'nonlocal_or_unresolved_import',
                        'chain': [{'module': module, 'symbol': alias.asname or alias.name},
                                  {'module': anchor, 'symbol': alias.name}], 'origins': []}
                sites.append({'module': module, 'path': record['path'], 'line': node.lineno,
                    'name': alias.asname or alias.name, 'imported_name': alias.name,
                    'target_module': anchor, **outcome})
    return {'status': 'complete', 'limits': limits, 'inventory': inventory,
            'map_summary': report['summary'], 'issues': report['issues'],
            'cycles': report['cycles'], 'sites': sites}


def format_text(result):
    lines = [f"{result['map_summary']['module_count']} modules; {len(result['sites'])} from-import names"]
    for site in result['sites']:
        origin = ', '.join(f"{o['module']}.{o['symbol']} ({o['path']}:{o['line']})"
                           for o in site['origins']) or site.get('reason', 'no static origin')
        lines.append(f"{site['path']}:{site['line']} {site['module']}.{site['name']}: "
                     f"{site['status']} — {origin}")
    for issue in result['issues']:
        lines.append('Issue: ' + json.dumps(issue, ensure_ascii=False, sort_keys=True))
    for cycle in result['cycles']:
        lines.append('Cycle: ' + ', '.join(cycle))
    return '\n'.join(lines)


def main(argv=None):
    budget = load_budget()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path, help='explicit Python import root inside current workspace')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--strict', action='store_true', help='exit 1 on unresolved/ambiguous traces or scan warnings')
    for name, value in budget.DEFAULTS.items():
        parser.add_argument('--max-' + name.replace('_', '-'), type=int, default=value, dest=name)
    args = parser.parse_args(argv)
    try:
        result = analyze(args.root, {name: getattr(args, name) for name in budget.DEFAULTS})
    except (OSError, ValueError, RuntimeError, RecursionError) as exc:
        error = getattr(exc, 'evidence', {'type': 'scan_error', 'detail': str(exc)})
        if args.json:
            print(json.dumps({'status': 'refused', 'error': error}, indent=2))
        else:
            print('import-origin-trace: ' + str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False) if args.json else format_text(result))
    warnings = (result['issues'] or result['cycles'] or
                any(site['status'] in ('unresolved', 'ambiguous', 'cycle')
                    for site in result['sites']))
    return int(args.strict and bool(warnings))


if __name__ == '__main__':
    sys.exit(main())
