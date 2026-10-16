# Origin CSV Review

Line 3's source-only re-export tracer meets Line 2's exact CSV reconciliation
and record-linked status transitions. Python standard library only; keep this
folder together. No installation, network, source execution or remote write.

From the repository root, one command reviews the retained actual worker scan:

```sh
python3 -B shared/import-drift/origin_csv.py compare shared/import-drift/observed-origins39.csv shared/import-drift/observed-origins39.csv
```

This exits 0 with exact equality and no status transitions. It compares a saved
snapshot to itself; it is a reproducible demonstration, not evidence of source
stability over time. Seven integration tests separately exercise changed
definitions, unresolved-to-resolved transitions with exact keys and CSV record
numbers, repeated names, line shifts, parse/wildcard warnings, invalid keys,
budget refusal with no partial CSV, and an empty tree:

```sh
python3 -B -m unittest discover -s shared/import-drift -p test_origin_csv.py -v
```

Make a fresh source snapshot, preserving the evidence on stderr:

```sh
python3 -B shared/import-drift/origin_csv.py snapshot shared/import-drift > test/scratch/origins.csv 2> test/scratch/origins-evidence.json
```

Create `test/scratch` first if necessary. Snapshot exits 0 on a complete scan
without warnings, 1 for unresolved/ambiguous/cyclic sites or map warnings, and
2 on refusal. Exit 1 still produces the complete admitted CSV and evidence;
it commonly occurs for standard-library imports outside the declared root.
Collection defaults and `--max-*` switches are those of Import Budget.
Compare exits 0 for equality, 1 for differences, 2 for invalid input.

Each module-body from-import occurrence gets `(path, line, site_index)` as its
key. Occurrence indexes distinguish repeated names even on the same line.
Rows retain the chain, static origins, origin-byte hashes and importing-file
hash. Editing an origin's body remains visible even when the resolution status
does not change. Comparison keeps all row and schema differences beside status
counts; each count links to its exact keys and logical CSV record numbers.
It never treats an unchanged status as unchanged evidence.

The actual worker was scanned without executing its code. Full source hashes,
issues and status counts are in `gathering/origin-evidence39.json`; the compact
self-comparison is in `gathering/origin-review39.json`. The seven focused tests
passed locally. The gathering report gives complete suite results.

Limits: coordinate keys are not semantic identity across edits. Line shifts
become removals/additions. Only explicit module-body from-imports are traced;
conditional/nested imports, dynamic loading and runtime rebinding are not
resolved. Wildcards and nonlocal imports remain unresolved. A source candidate
is not a runtime binding proof. Keep stderr evidence: self-equality can coexist
with parse errors, unresolved sites or cycles. Supplied CSVs and source hashes
are unauthenticated. Inputs must remain stable while read. No coin is needed.

Provenance: `origins.py` copies Line 3's Import Origin Trace with only its
dependency path adapted to this folder. `transitions.py` refreshes the existing
Line 2 copy to support optional record provenance, retaining default behavior.
`origin_csv.py` is the new glue; existing mapper, budget and reconciler are reused.
