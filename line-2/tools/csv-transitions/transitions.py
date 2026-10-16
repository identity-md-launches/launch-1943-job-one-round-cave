#!/usr/bin/env python3
"""Explain exact old-to-new values in uniquely keyed CSV row changes."""
import argparse
from collections import Counter
import importlib.util
import json
from pathlib import Path
import sys

source = Path(__file__).resolve().parents[1] / 'csv-reconcile' / 'reconcile.py'
spec = importlib.util.spec_from_file_location('csv_transitions_engine', source)
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)


def transitions(before, after, keys, columns, include_records=False):
    """Recompute the comparison; selected columns never narrow global verdicts."""
    if not columns or len(set(columns)) != len(columns) or set(columns) & set(keys):
        raise engine.InputError('select distinct non-key columns')
    # Load once per input: unlike filtering an external report, this retains the
    # engine's parser, ambiguity and global verdict guarantees.
    result = engine.reconcile(before, after, keys)
    # A column can exist without appearing in a delta. Read headers from the
    # already bounded parser; files must remain stable throughout this command.
    bh, _, _ = engine.load_table(before, keys)
    ah, _, _ = engine.load_table(after, keys)
    if not set(columns) <= (set(bh) & set(ah)):
        raise engine.InputError('selected columns must exist in both inputs')
    reports = []
    for column in columns:
        counts = Counter((r['fields'][column]['before'], r['fields'][column]['after'])
                         for r in result['changed'] if column in r['fields'])
        members = {}
        if include_records:
            for row in result['changed']:
                if column in row['fields']:
                    delta = row['fields'][column]
                    pair = (delta['before'], delta['after'])
                    members.setdefault(pair, []).append({
                        'key': row['key'],
                        'before_record': row['before_record'],
                        'after_record': row['after_record']})
        groups = []
        for (b, a), n in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
            group = {'before': b, 'after': a, 'rows': n}
            if include_records:
                group['records'] = members[(b, a)]
            groups.append(group)
        reports.append({'column': column, 'changed_rows': sum(counts.values()),
                        'transitions': groups})
    return {'format': 'csv-transitions/v1', 'equal': result['equal'],
            'complete': result['complete'], 'keys': result['keys'],
            'schema': result['schema'], 'summary': result['summary'],
            'unpaired_records': {side: sum(len(g[side]) for g in result['ambiguous'])
                                 for side in ('before', 'after')},
            'columns': reports}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before')
    parser.add_argument('after')
    parser.add_argument('--key', action='append', required=True)
    parser.add_argument('--column', action='append', required=True)
    parser.add_argument('--include-records', action='store_true',
                        help='include exact keys and logical CSV record numbers in each transition')
    args = parser.parse_args(argv)
    try:
        report = transitions(args.before, args.after, args.key, args.column, args.include_records)
    except (OSError, ValueError):
        print(json.dumps({'error': 'Check workspace-local CSVs, distinct keys and common non-key columns.'}), file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return 0 if report['equal'] else 1


if __name__ == '__main__':
    sys.exit(main())
