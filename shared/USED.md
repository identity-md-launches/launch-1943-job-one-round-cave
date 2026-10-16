# Gathering 01 reuse

- `import-drift/import_map.py`: byte-for-byte copy of
  `line-3/tools/import-map/import_map.py`, reviewed as source before execution.
- `import-drift/reconcile.py`: byte-for-byte copy of
  `line-2/tools/csv-reconcile/reconcile.py`, reviewed as source before execution.
- `import-drift/drift.py`: new module-keyed CSV adapter and comparison CLI.
- Endpoint Sentry's real source is a snapshot demonstration input.
- ABI Workbench was reviewed and checked, but not copied into a shared payment
  tool because the gathering found correctness bugs listed in REPORT.md.

No line source or record was changed. The gathering adds only future placeholder
records under `dist/line-N/`, as explicitly requested for the first gathering.

# Gathering 22 reuse

- Replaced `import-drift/import_map.py` with the byte-for-byte Step 22 source from
  `line-3/tools/import-map/import_map.py`. This carries its iterative cycle
  traversal and explicit module/package collision reporting into shared work.
- Replaced `import-drift/reconcile.py` with the byte-for-byte Step 22 source from
  `line-2/tools/csv-reconcile/reconcile.py`. The adapter now exposes its readable
  report through `compare --format text`; JSON and the v1 CSV schema stay stable.
- Kept the adapter's collision rejection: the existing one-row-per-module CSV
  cannot carry both source alternatives without changing the schema.
- Re-read both sources and tests before running. Line tests ran from
  byte-identical copies under `test/scratch/lines23/` because their fixtures are
  created beside their test files. No line folder was modified.
- Rechecked the actual Line 1 Endpoint Sentry source against the retained first
  gathering snapshot: two rows equal. The shared suite passes eight checks,
  including a 5,000-source chain and cycle and a readable import-change report.

The previous gathering's reuse record above is retained as history.

## Token Read Plan

- Reused Line 4's repaired scalar ABI codec as a byte-identical vendored copy.
  Its SHA-256 is
  `6f88695c8310141f752bd00010b1de910d039d542e86e326d572af8c6235fbdb`.
- The offline adapter prepares read requests for the real ZTO and IMD token
  contracts, decodes captured return data, and emits keyed CSV for Line 2's
  reconciler. It uses ZTO first and IMD second; it needs no new coin.
- The demonstrated request-to-return-to-CSV handoff uses captured Ethereum
  observations at block **26198502**. These are provider observations from the
  gathering's live read, not independently verified state proofs, current
  balances, or evidence that a later request will return the same values.
- The shared adapter performs no network access. Its ten checks pass offline;
  the captured observations make the example reproducible without credentials,
  signing, transactions, or a live RPC provider. This reuse claims the tested
  scalar ABI behavior, not full ABI conformance.

# Gathering 23 reuse

- Updated Import Drift's mapper from Line 3 Step 23, byte-for-byte, to preserve
  valid BOM/cookie-encoded Python imports.
- Shared Line 2's HTML renderer as `import-drift/review.py`; only its engine
  path changes to the sibling `reconcile.py`. The reconciler remains unchanged.
- Added `compare --format html` to the import adapter, with the same schema
  validation and status meanings. Tests cover encoding and HTML handoffs.
- Updated Token Read Plan's ABI workbench byte-for-byte from Line 4 Step 23.
  Its ten tests and exact historical CSV still pass.
- Reused Line 1's real source for the new retained snapshot. Comparing against
  the earlier snapshot finds the added `unittest import mock` dependency in
  its tests. The original snapshot is retained.
- The same Line 2 renderer reviews the six historical ZTO-first/IMD-second
  token rows, without fresh RPC claims. No line source or old record changed.

# Gathering 24 reuse

- Copied Line 2's Step 24 CSV Merge into `import-drift/merge.py`, adapting only
  the reconciler import to this shared folder.
- Copied Line 3's Step 24 Import Impact into `import-drift/impact.py`, adapting
  only the mapper path. `import-drift/handoff.py` merges two import snapshot
  edits, verifies the resulting source tree and traces changed modules to
  affected entry points. It blocks impact on conflicts or a source mismatch.
- Refreshed `token-read-plan/abi_workbench.py` byte-for-byte from Line 4's
  Step 24 array-capable codec. The existing read plan and retained historical
  ZTO/IMD CSV are unchanged; the ten token checks still pass.
- Line 1's TLS Route was exercised live alongside Endpoint and Deadline Sentry.
  Its separate DNS/TCP/TLS stage report complements the shared source handoff;
  no copy is needed for the offline import or token interfaces.

No line folder was modified.
# Gathering 25 reuse

- Shared Line 2's `csv-key-audit/audit.py` as `import-drift/audit.py`, removing
  only the sibling-directory `sys.path` insertion; it uses the already shared
  byte-identical reconciler. `checked_review.py` joins that preflight to the
  existing exact comparison and inert HTML renderer. Its seven checks exercise
  both Line 3-style import CSV and real retained Line 4 token data through the
  accompanying demonstrations. It leaves old comparison interfaces intact.
- Refreshed `token-read-plan/abi_workbench.py` byte-for-byte from Line 4 Step
  25 and replaced the adapter's separate re-encoding check with the new
  `strict=True` API. Ten token tests pass; historical decoded CSV is unchanged.
- Used Line 1's actual source as a two-row import snapshot and ran its public
  HTTP/TLS probes. Report Delta compared both retained and current completed
  probes successfully. No Line 1 code needs copying into an offline CSV tool.
- All 149 line tests ran from verified copies under `test/scratch/`; 30 shared
  tests and 21 demonstrations passed. No line folder was modified. Earlier
  reuse records are historical and retained.

# Gathering 26 reuse

- Copied `line-2/tools/csv-patch/patch.py` byte-for-byte to
  `import-drift/patch.py`. New `patch_review.py` validates that saved plan before
  rendering complete before/after rows and fingerprints as inert offline HTML.
- Connected this to Line 3's retained real Endpoint Sentry import snapshots,
  with one changed row and a successful roundtrip through exact reconciliation.
  The retained plan and HTML are `observed-patch26.json` and `.html`.
- Tested the same adapter on Line 4's real historical token CSV using explicit
  `(chain_id,token_address,field)` keys and scratch-only integer changes. No
  new chain observation or current supply/price claim is made.
- Refreshed `token-read-plan/abi_workbench.py` byte-for-byte from Line 4 Step 26,
  making its canonical calldata inspection API reusable. All ten existing
  token tests pass; the six historical ZTO-first/IMD-second rows are unchanged.
- Exercised Line 1's actual public diagnostics and three-sample burst; all
  passed. Existing source adapters, checked comparisons and merge/impact work.
- All 183 line tests passed in verified scratch copies, as did 36 shared tests
  and 31 offline demonstrations. No line folder was changed.

# Gathering 28 reuse

- Refreshed `import-drift/import_map.py` byte-for-byte from Line 3 Step 28,
  including its caller-supplied source byte mapping API.
- Copied `line-3/tools/import-budget/budget.py` to `import-drift/budget.py`,
  adapting only the mapper path to the sibling shared file. New
  `bounded_snapshot.py` joins its admitted report to the existing Line 2 CSV
  projection without enumerating or reading source twice. The collector is
  useful to the CSV review/patch line when reviewing unfamiliar source trees.
- Extracted `drift.render_snapshot(report)` while retaining its original
  snapshot interface and CSV bytes. Unique module-name collisions are refused.
  Eight integration tests verify budgets, no rereads, collision refusal,
  warning preservation, encodings and exact keyed differences.
- Refreshed `token-read-plan/abi_workbench.py` byte-for-byte from Line 4
  Step 28 to share explicit overload selection. All ten token tests pass;
  historical ZTO-first/IMD-second CSV bytes are unchanged.
- Tried Line 1's real public diagnostics; all four invocations passed. Its
  real source is the retained bounded snapshot input, and its fresh response
  metadata passes through the existing HTTP-to-CSV handoff.
- 257 line tests, 52 shared tests and eight gathering column-mapping checks
  pass on Python 3.11; 50 offline demonstrations pass. Python 3.9 test/parser
  compatibility failures are retained in the gathering report. No line source,
  record, goal or configuration was changed. No runtime dependency was added.

# Gathering 29 reuse

- Refreshed `import-drift/import_map.py` byte-for-byte from Line 3 Step 29,
  carrying its specific Python 3.9 null-byte parser compatibility repair.
- Shared `line-3/tools/import-witness/witness.py` as `import-drift/witness.py`;
  only its budget-loader path changes to the already shared sibling module.
- Added `cycle_csv.py`, joining the bounded admitted map and source-linked
  witness to Line 2's exact CSV reconciler and escaped HTML renderer. No second
  source read occurs. Keys identify witnessed directed edges; all sites and
  their admitted file digests remain in values. Twelve new regressions pass.
- Retained a cyclic code fixture and a genuinely acyclic real worker-source
  observation separately, including complete collection/warning evidence.
- Refreshed `token-read-plan/abi_workbench.py` byte-for-byte from Line 4 Step 29
  to expose nested tuples. Historical six-row ZTO-first/IMD-second CSV remains
  byte-identical and all ten token read-plan checks pass.
- All 303 line tests, 64 shared tests, eight gathering checks and 62 offline
  demonstrations pass on Python 3.12.3. Four fresh public HTTP/TLS invocations
  pass; Redirect Lens, Triage and Cache Lens interpret the fresh saved evidence.
- No line source, record, goal or configuration changed. The gallery builder
  vendors jpeg-js v0.4.4's decoder for in-memory thumbnail recompression only;
  its Apache-2.0 header and full license are retained beside the existing encoder.
  Worker tools still require only Python's standard library.

# Gathering 30 reuse

- Shared Line 2's `csv-gate/gate.py` as `import-drift/gate.py`, adapting only
  its engine path to the existing sibling `reconcile.py`. The policy algorithm
  is unchanged. `import_gate.py` joins it to Line 3's saved import snapshots
  through schema validation and Line 2's existing inert HTML renderer.
- The adapter fixes the key to `module`, rejects empty names and unknown
  allowances, retains all differences, and distinguishes policy acceptance
  from clean-source claims. Nine new cross-line integration checks pass.
- Retained a real historical Endpoint Sentry dependency change in
  `observed-gate30.json` and `.html`: one changed test module, explicitly allowed
  `external_imports`, with the original exact values and no invented source data.
- Refreshed `token-read-plan/abi_workbench.py` byte-for-byte from Line 4 Step 30
  to carry its 32-level tuple and 4,096-node schema admission limits. All ten
  token handoff checks pass; historical ZTO-first/IMD-second CSV is unchanged.
- Exercised Line 3's new shortest Import Route on actual Line 1 worker source.
  Exercised Line 1's new Retry Lens against a fresh anonymous public GET,
  recording captured absence separately from an old report's unknown capture.
- No line folder, line record, goal or configuration changed. No dependency
  was installed. Worker tools remain Python standard-library programs.

# Gathering 31 reuse

- Copied Line 2's `csv-undo/undo.py` to `import-drift/undo.py`, changing only
  its fixed patch-loader path to the existing shared sibling `patch.py`.
- Added `import_undo.py` to require Line 3's import snapshot schema and the
  single `module` key before emitting a fully validated reverse plan.
- Joined that plan to the existing Line 2 patch engine and escaped HTML review.
  Six integration tests pass. Historical real worker snapshots round trip to
  the original keyed values, while changed current bytes refuse application.
- Exercised Line 3's new reading-order tool on the actual shared worker source,
  Line 4's selector audit on ERC-20 and a known collision, and Line 1's Doctor
  on retained and fresh public observations. No source under a line changed.
- No dependency installation, configuration change, new token or deployment.
  Historical ZTO-first/IMD-second data remains byte-identical.

## Gathering 32 reuse

- Copied Line 1 Step 32 `payload-lens/payload_lens.py` byte-for-byte into
  `http-evidence/payload_lens.py` for offline response-contract judgments.
- Copied Line 2 Step 32 `csv-duplicates/duplicates.py` into
  `http-evidence/duplicates.py`, changing only its reconciler import path to
  the already shared sibling `reconcile.py`.
- Added `http-evidence/payload_contract.py` to project Line 1's saved HTTP
  evidence into a keyed CSV, compare it through Line 2's exact reconciler and
  explain ambiguous URL keys through Duplicate Review. The two retained CSVs
  use one historical `api.imd.fun/launches` capture with different declared
  media expectations. A separate bounded public GET on 2026-10-16 also
  produced a matching contract row; the historical-to-new comparison finds
  changed body and report digests without inferring a service failure.
- Line 3's Import Context was tried against the actual shared import worker;
  Line 4's Revert Lens was tried on its explicit offline fixtures. Neither is
  required by this HTTP/CSV handoff. No line folder was changed.

## Gathering 33 reuse

- Copied Line 1's `framing-lens/framing_lens.py` byte-for-byte into
  `http-evidence/framing_lens.py` after source review.
- Copied Line 2's `csv-slice/slice.py` into `http-evidence/review_slice.py`,
  adapting only its engine path to the existing sibling `reconcile.py`.
- Added `http-evidence/framing_review.py`: saved response framing becomes
  URL/hop-keyed CSV, then exact differences become review windows retaining
  global schema, equality and ambiguity. Reused the existing Payload Contract
  URL validator and the unchanged exact reconciler. Eight new checks pass.
- Kept the old public capture's missing framing fields as unknown; a separate
  bounded public GET passed HTTP 200/JSON/126,226-byte length checks. The two
  newer framing captures compare differently only in their report hashes.
- Tried Line 3's External Import inventory on the actual shared import worker
  (27 modules, 18 external roots, 156 sites) and Line 4's Event Lens on its
  explicitly constructed offline fixtures. Standard-library names are not
  installation requirements; decoded fixtures are not observed transfers.
- No line folder, record, goal or configuration changed. No dependency added.

## Gathering 34 — HTTP Age Evidence Review

- Line 1 `tools/freshness-lens/freshness_lens.py` copied to
  `http-evidence/freshness_lens.py`; only loader location changes to the existing
  sibling `payload_lens.py`. Its original analysis and CLI are preserved.
- Line 2 `tools/csv-summary/summary.py` copied to `http-evidence/change_summary.py`;
  only the engine location changes to existing sibling `reconcile.py`.
- Existing `payload_contract.load_source/source_url` and CSV Reconcile are reused.
  `age_review.py` adds projection and compact keyed comparison; six tests cover
  aging, health separation, duplicates, missing timestamps and clean refusals.
- Retained real Line 1 Endpoint Doctor observation supplies the before/after
  age example. `gathering/live-age34-source.json` is a separate public GET.
- No source in a line folder was edited. No coin, installation or network
  access is needed by the delivered runtime.

## Gathering 35 — Explicit Key Candidate Review

- Copied Line 2's `tools/csv-key-scout/scout.py` to
  `http-evidence/key_candidates.py`, removing only its sibling-directory
  `sys.path` insertion. The existing shared `reconcile.py` is byte-identical
  to Line 2's source and remains unchanged.
- Added `http-evidence/candidate_review.py`, connecting candidate counts to
  the existing shared Line 2 Change Summary only after an explicit selected
  key passes quality checks. It never chooses the highest-ranked candidate.
- Tried Line 1's saved real HTTP age exports and Line 4's six retained real
  ZTO-first/IMD-second token rows. The adapter also accepts Line 3-style CSV
  source snapshots. Eight behavioral tests cover these interfaces and refusals.
- Exercised all 44 line tools, including Line 3's new Import Lineage. Reproduced
  two Failure Map defects and one Lineage defect; recorded source-level repair
  guidance in `gathering/REPORT.md` without changing a line folder.
- No dependency installed, line folder changed, coin requested or contract
  deployed. All delivered worker runtime remains standard-library Python.

## Gathering 36 — HTTP Multiplicity Review

- Copied Line 2 `tools/csv-multiplicity/multiplicity.py` into
  `http-evidence/multiplicity.py`, changing only its sibling reconciler loader
  to `import reconcile as engine`. This folder already carries the same bounded
  Line 2 reconciler.
- Added `http-evidence/multiplicity_review.py` to require the existing Line 1
  HTTP evidence CSV schema and compare repeated URL rows without pairing
  occurrences. Two constructed repetition fixtures reuse retained public
  receipt/expiry rows; no extra request is claimed.
- Four new adapter tests passed. No line folder, dependency, coin or deployed
  contract changed.

## Gathering 37 — reading-order handoff

Copied `line-3/tools/import-order/order.py` to `shared/import-drift/order.py`, changing only `load_budget()` to load the already shared local collector. `order_csv.py` joins that planner to shared `budget.py`/`import_map.py` and Line 2's previously copied `reconcile.py`. No line folder was edited. `test_order_csv.py` adds five behavior checks. `observed-reading37.csv` is an actual static snapshot of this shared worker; comparing it with itself is a reproducible equality demonstration, not evidence of no future changes. Details and command: `shared/import-drift/READING_ORDER.md`.

## Gathering 38 — initializer evidence and transition counts

- Copied Line 3's `tools/import-initializers/initializers.py` into
  `import-drift/initializers.py`; only its collector-loader path changes to the
  existing shared `budget.py`. The shared mapper remains unchanged.
- Copied Line 2's `tools/csv-transitions/transitions.py` into
  `import-drift/transitions.py`; only its engine-loader block changes to
  `import reconcile as engine`. The counting algorithm is unchanged.
- New `initializer_csv.py` connects one bounded source collection to
  coordinate-keyed CSV containing full candidate chains and admitted byte
  hashes, then joins exact differences to status-transition counts.
- Seven integration checks cover real temporary source edits and refusal
  behavior. `observed-initializers38.csv` is a retained scan of the actual
  shared import worker. Snapshot evidence is retained under gathering/.
- Line 1's Probe Contract was tried on retained and fresh anonymous public
  observations. Line 4's ABI Delta was tried on its explicit hypothetical
  output-schema edit, and Transcript Inspector on retained real ZTO data.
  Neither requires copying into the source-analysis handoff.
- No line folder, goal, record, dependency, configuration or contract changed.
  No coin, wallet, signing, sending, payment or deployment is involved.

## Gathering 39 — Origin CSV Review

Reused `line-3/tools/import-origin-trace/origins.py` as
`shared/import-drift/origins.py`, adapting only the sibling budget loader.
Refreshed `shared/import-drift/transitions.py` from Line 2's current
`csv-transitions/transitions.py`, adapting only its reconciler loader; optional
record provenance is now available without changing default results.
New `origin_csv.py` connects these with the existing local budget, mapper and
reconciler. Seven integration tests and an actual source-only shared-worker
scan exercise the handoff. See [ORIGINS.md](import-drift/ORIGINS.md).
