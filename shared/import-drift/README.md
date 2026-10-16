# Import Drift

Compare the import structure of two Python source trees without executing their
code. Python 3.10+ and its standard library are sufficient. No installation,
network, wallet, configuration discovery, or environment-variable access.
Run from the workspace root; all input paths must resolve inside it.

Gathering 30 adds [Import Change Gate](CHANGE_GATE.md), joining bounded source
exports to explicit changed-row and column limits with full JSON/HTML review.
Default policy rejects all differences. Accepted differences remain visible.
The new nine integration checks pass; use the gathering report for current totals.

This joins Line 3's Import Map to Line 2's CSV Reconcile. Their reviewed versions are copied here unchanged as `import_map.py` and `reconcile.py`, so this
folder can be reused independently. `drift.py` supplies the adapter. Gathering 22
brings Line 3's deep-graph fix and Line 2's readable report into this shared tool.

One command to see it working on the actual delivered worker tools:

```sh
python3 -B shared/import-drift/drift.py snapshot line-1/tools/endpoint-sentry
```

It emits two module rows and one local import link, with no cycles or issues.
CSV goes to stdout; scan summary JSON goes to stderr. To review a source change,
save a snapshot before and after that change, then compare:

```sh
python3 -B shared/import-drift/drift.py snapshot line-1/tools/endpoint-sentry > shared/before.csv
# Take another snapshot after the source change, or repeat now to check equality.
python3 -B shared/import-drift/drift.py snapshot line-1/tools/endpoint-sentry > shared/after.csv
python3 -B shared/import-drift/drift.py compare shared/before.csv shared/after.csv
```

Add `--format text` to `compare` for a readable Markdown report. JSON remains the
default and both formats have the same exit status. For example, this one command
reviews the retained real Endpoint Sentry snapshot against itself:

```sh
python3 -B shared/import-drift/drift.py compare shared/import-drift/observed-sentry.csv shared/import-drift/observed-sentry.csv --format text
```

Exit codes: snapshot 0 means no reported cycles/issues, 1 means a usable snapshot
with cycles/issues; compare 0 means equal, 1 means differences or ambiguous module
keys; both use 2 for input/scan errors. A snapshot with exit 1 is deliberately
retained for review. A failed parse appears in its module's `parse_errors` cell;
it is never silently treated as a clean empty module.

The v1 CSV key is `module`. It records path, main-guard entrypoint, sorted unique
local and external targets, unresolved targets, dynamic-import line numbers, and
parse errors. Lists are JSON strings inside CSV cells. Ordinary import line
shifts and repeated imports do not create changes; dynamic-import positions and
parse-error locations do. Paths are relative to each scanned import root, so
two checkout locations compare consistently. This is a structural projection,
not a source-code diff, a runtime import trace, or a proof of correct resolution.
The stderr summary preserves cycle counts; use Import Map's full JSON to inspect
cycle membership. The adapter does not add cycle membership to CSV rows.

Inherited limits: external imports cannot be proved installed, attribute imports
are conservative, dynamic targets are not resolved, and source scanning has no
total byte/file budget. Python source encodings (including UTF-8 BOMs and encoding cookies) are
honored by the Step 23 mapper, using Python's AST parser on original bytes. AST parsing still has Python's parser limits. Compare inputs
have the reconciler's 16 MiB/100,000-row limits. Scan only trusted, reasonably sized
workspace source trees. Cycle detection now uses an iterative traversal, tested
on a 5,000-module source chain and cycle. The v1 snapshot still rejects
module/package name collisions with exit 2: one row per name cannot faithfully
represent both alternatives. Line 3 now reports collisions and selects the
regular package; use its complete report when reviewing those alternatives.

Check:

```sh
python3 -B -m unittest discover -s shared/import-drift -p 'test_*.py' -v
```

All eight checks passed in Gathering 22. They create fixtures only under
`test/scratch/`, scan a file containing a deliberate execution trap without
executing it, and test dependency changes, unchanged line shifts, parse failures,
duplicate keys, workspace/schema validation, collision rejection, deep source
graphs, and readable comparison exit statuses. The old shared mapper failed a
1,500-module chain with `maximum recursion depth exceeded`; the upgraded mapper
handles it. A fresh snapshot of the actual Endpoint Sentry source compared equal
to `observed-sentry.csv`: two modules, one local edge, no cycles or issues.


## Gathering 23: readable HTML handoff

The current mapper is copied byte-for-byte from Line 3's Step 23 repair.
Line 2's HTML renderer is now `review.py`; its only adaptation is loading the
sibling `reconcile.py`. `drift.py compare --format html` validates the import
snapshot schema, then hands the exact comparison to that renderer. All data
is escaped; the report has no scripts, remote assets or active data fields.
Exit 0 means equal, 1 means differences/ambiguity, 2 means invalid input with
no partial HTML. Python standard library only, no dependencies to install.

One command using real source snapshots:

```sh
python3 -B shared/import-drift/drift.py compare shared/import-drift/observed-sentry.csv shared/import-drift/observed-sentry23.csv --format html
```

Redirect stdout to a workspace `.html` file to open it in a browser. Tried:
exit **1**, one changed module (`test_sentry` now imports `unittest.mock`), one
unchanged module, no ambiguous keys. The retained result is
[observed-review23.html](observed-review23.html). Snapshots compare structural
imports only: the port-validation behavior change itself is not inferred.

The same shared renderer accepts Line 4's token CSV via explicit composite keys:

```sh
python3 -B shared/import-drift/review.py shared/token-read-plan/observed.csv shared/token-read-plan/observed.csv --key chain_id --key token_address --key field
```

Tried: exit 0, six unchanged historical ZTO/IMD rows, identical output to Line 2's
original renderer. The delivered result is
[the token review](../token-read-plan/observed-review23.html).

All **10 shared checks** pass, including Python source encodings and HTML
handoff statuses/inert parse errors. Line 2's six renderer tests also pass on
the shared copy. Rendering inherits whole-table memory use and has no output
size cap; use modest snapshots. `--ignore` in the standalone renderer is not
redaction: ambiguous rows retain original ignored values.

## Gathering 24: merge changes, then trace impact

`merge.py` adapts Line 2's CSV Merge with only its reconciler import changed;
`impact.py` adapts Line 3's Import Impact with only its mapper path changed.
`handoff.py` joins them. Give it a baseline snapshot, two edited snapshots, and
the current source tree. It merges exact `module` rows, refuses to trace an
unresolved conflict, then requires the merged snapshot to match the current
source exactly before identifying affected entry points. It reports removed
modules separately because a removed module has no current reverse path.
No inspected Python source is executed.

This command checks an actual retained Endpoint Sentry snapshot against the
current source without creating a file:

```sh
python3 -B shared/import-drift/handoff.py shared/import-drift/observed-sentry23.csv shared/import-drift/observed-sentry23.csv shared/import-drift/observed-sentry23.csv line-1/tools/endpoint-sentry
```

Observed: `ready: true`, two unchanged modules, no changed modules, no
conflicts, no scan issues; exit 0. The end-to-end checks create independent
edits to temporary Python modules: a changed helper leads to the `main`
entry point through `main -> helper`, while a conflict produces no impact
claim and a mismatched source tree is rejected. Run:

```sh
python3 -B -m unittest discover -s shared/import-drift -p 'test_*.py' -q
```

All 13 checks passed. CLI exit codes: 0 complete, 1 merge conflict, 2 invalid
input or source mismatch. The input CSVs retain the reconciler's bounds; source
scanning has no total file or byte budget. Static local imports can miss runtime
hooks and implicit package behavior. This tool does not repair conflicts or
prove that an entry point will execute.
# Gathering 25: checked comparison

[Checked CSV Review](CHECKED_REVIEW.md) reuses Line 2's new key auditor to
withhold comparisons when keys are duplicate, empty, or lack data evidence.
It accepts both this folder's import snapshots and the ZTO/IMD CSV emitted by
the shared token adapter. Seven new handoff tests pass; the full suite has 20.

## Gathering 26: carry a reviewed exact change

[Validated CSV Patch Review](PATCH_REVIEW.md) shares Line 2's unchanged guarded
patch engine. Saved plans can carry an import snapshot change or token CSV
change to another worker while pinning exact baseline and result fingerprints.
The new renderer validates the complete patch before displaying inert HTML.
Stale baselines and altered operations are refused without a partial page.
Six new tests pass; this shared folder now has 26 passing tests. The retained
real import change and a scratch-only exact token integer change both work.

## Gathering 28: bounded CSV source handoff

[Bounded Import CSV Handoff](BOUNDED.md) adds an explicit bounded collection
entry point, reusing Line 3 Step 28 and this folder's Line 2-backed review.
It emits the same CSV schema from exactly the admitted source bytes, with a
per-file manifest on stderr. Budget/read/collision refusals emit no CSV.
Legacy snapshot/merge/impact interfaces remain unbounded. The shared mapper
now matches Line 3 Step 28 byte-for-byte. Eight new integration checks pass;
the complete shared import suite has 34 tests. **Use Python 3.10+** (verified
on 3.11); Python 3.9 has inherited null-byte parser/test compatibility defects.
See the gathering report for the observed failures and limits.

## Reviewed reversal of saved import changes

[Import Snapshot Undo](UNDO.md) connects checked CSV undo to module-keyed snapshots, with exact forward-result fingerprints and an offline HTML review. It reverts saved table values, never Python files.

Gathering 37 adds [Reading Order CSV](READING_ORDER.md): source-linked dependency reading waves exported for exact keyed comparison of revisions.

Gathering 38 adds [Initializer CSV Review](INITIALIZERS.md): source-linked package initialization candidates, exact coordinate-keyed differences and status-transition counts.

Gathering 39 adds [Origin CSV Review](ORIGINS.md): static re-export chains and
origin-byte hashes become keyed CSV evidence, with exact record-linked status
transitions and complete differences retained.
