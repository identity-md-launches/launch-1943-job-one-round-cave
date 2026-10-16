#!/usr/bin/env python3
"""Compare static Python re-export evidence with exact keyed CSV differences."""
import argparse
import collections
import csv
import io
import json
import sys

import budget
import origins
import reconcile
import transitions

KEYS = ('path', 'line', 'site_index')
COLUMNS = KEYS + ('module', 'name', 'imported_name', 'target_module', 'status',
                  'reason', 'chain', 'origins', 'source_sha256')
SCOPE = ('Static module-body from-import candidates, not verified runtime bindings. '
         'Keys are source coordinates plus occurrence index, not semantic identity. '
         'Line shifts appear as removals/additions. Conditional/nested imports and '
         'runtime rebinding are outside the tracer. Keep snapshot stderr evidence: '
         'CSV equality does not certify complete, safe or warning-free source. '
         'Inputs must remain stable during collection and comparison.')


def canonical(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':'))


def snapshot(root, limits=None):
    report = origins.analyze(root, limits)
    hashes = {item['path']: item['sha256'] for item in report['inventory']['manifest']}
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=COLUMNS, lineterminator='\n')
    writer.writeheader()
    occurrences = collections.Counter()
    statuses = collections.Counter()
    for site in report['sites']:
        coordinate = (site['path'], site['line'])
        index = occurrences[coordinate]
        occurrences[coordinate] += 1
        statuses[site['status']] += 1
        linked = [dict(origin, source_sha256=hashes.get(origin['path']))
                  for origin in site['origins']]
        writer.writerow({**{k: site.get(k, '') for k in
                            ('path', 'line', 'module', 'name', 'imported_name',
                             'target_module', 'status', 'reason')},
                         'site_index': index, 'chain': canonical(site['chain']),
                         'origins': canonical(linked),
                         'source_sha256': hashes[site['path']]})
    evidence = dict(report, schema='origin-csv/v1', scope=SCOPE,
                    status_counts=dict(sorted(statuses.items())),
                    collection_scope=budget.SCOPE)
    return stream.getvalue(), evidence


def compare(before, after):
    for path in (before, after):
        columns, groups, _ = reconcile.load_table(path, KEYS)
        if columns != list(COLUMNS):
            raise ValueError('expected origin-csv/v1 columns')
        for key, rows in groups.items():
            if not key[0] or len(rows) != 1:
                raise ValueError('source coordinate keys must be unique and nonempty')
            for number, minimum in zip(key[1:], (1, 0)):
                if (not number.isascii() or not number.isdecimal() or
                        str(int(number)) != number or int(number) < minimum):
                    raise ValueError('invalid source coordinate')
    return {'schema': 'origin-review/v1',
            'comparison': reconcile.reconcile(before, after, KEYS),
            'status_transitions': transitions.transitions(
                before, after, KEYS, ['status'], include_records=True),
            'scope': SCOPE}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    commands = parser.add_subparsers(dest='command', required=True)
    snap = commands.add_parser('snapshot')
    snap.add_argument('root')
    for name, default in budget.DEFAULTS.items():
        snap.add_argument('--max-' + name.replace('_', '-'), dest=name, type=int, default=default)
    diff = commands.add_parser('compare')
    diff.add_argument('before')
    diff.add_argument('after')
    args = parser.parse_args(argv)
    try:
        if args.command == 'snapshot':
            text, evidence = snapshot(args.root, {k: getattr(args, k) for k in budget.DEFAULTS})
            print(canonical(evidence), file=sys.stderr)
            sys.stdout.write(text)
            return int(bool(evidence['issues'] or evidence['cycles'] or any(
                site['status'] in ('unresolved', 'ambiguous', 'cycle') for site in evidence['sites'])))
        result = compare(args.before, args.after)
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return int(not result['comparison']['equal'])
    except (OSError, ValueError, RuntimeError, RecursionError) as error:
        print(canonical({'schema': 'origin-csv/v1', 'status': 'refused',
                         'error': str(error)}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
