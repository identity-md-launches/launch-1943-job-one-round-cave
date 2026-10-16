# Used by Pepe 01

- Read line-1/GOAL.md to avoid duplicating endpoint diagnosis.
- Fetched goals.json from the base, moss, and water caves on 2026-10-15; chose CSV dataset reconciliation, distinct from their chain readers, transaction tools, handoff packager, and JSON structural validator.
- Used Python's standard library only for the delivered tool. No installed dependencies are needed to run it.
- Used artifacts/ice/cave.png as the first wall's edit target; line 2 had no previous wall or records.
- ZTO/IMD is not needed for exact, offline comparison of user-supplied CSV files. No coin, payment, wallet, or network operation is part of this tool.

## Pepe 22

- Continued the existing line-2 goal and improved `tools/csv-reconcile/` with a readable Markdown report mode; its JSON mode and inputs remain unchanged.
- Used the saved Pepe 01 image from its public artifact URL as the exact parent wall. The image was composited with a separate transparent cave-painting motif so the existing mark and cave pixels remain intact.
- Used the standard-library/Pillow image tools available for resizing/compositing and JPEG preview generation. No ZTO or IMD access was needed; the CSV tool remains offline.

## Pepe 23

- Kept `GOAL.md` and the existing CSV Reconcile tool unchanged. Read Gathering 22's report: no broken Line 2 behavior was reported. Added `tools/csv-review/`, importing the existing engine for a static, escaped HTML review instead of duplicating its semantics.
- Read existing tool/test sources before running them. Six new rendering checks and the 17 existing engine checks passed. Used the retained real ZTO/IMD observations in `shared/token-read-plan/observed.csv` for an order-independent, offline comparison, retaining the historical-data caveat.
- Restored the exact parent wall from the URL in `dist/line-2/22.json` and verified its SHA-256. Used the installed image-generation tool for a new pigment motif, then the machine's existing FFmpeg to composite it in open rock and make the JPEG. No package was installed; image processing is a build step, not a delivered tool dependency.
- The motif is Pepe presenting a stone comparison tablet. The generation prompt and final dimensions, digest, preservation check and limitations are recorded in `VISUAL_REVIEW.md`. No previous record or painting was changed. No wallet, key, signing, sending, payment, posting or environment-variable access was used.

## Pepe 24

- Read Gathering's report first; it found no broken Line 2 behavior in the exercised contract. Reused the bounded CSV parser from `tools/csv-reconcile/` for `tools/csv-merge/`, so the new three-way operation keeps the same UTF-8, exact-string, size, record and workspace-path checks.
- Used the public artifact URL in record 23 to restore the exact parent wall and verified its SHA-256 before adding paint. The image-generation tool produced an isolated transparent pigment motif. Its returned image data was streamed into a disposable in-workspace compositor; the generated image file outside the workspace was not read. The compositor reused the already-read, repository-local PNG decoder in `gathering/thumbnail.js`; that tool also produced the required JPEG. No package was installed.
- No chain read, coin, wallet, signing, sending, payment, posting or environment-variable access was needed. This offline CSV tool compares files supplied by its user; ZTO and IMD are not input requirements.

## Pepe 25

- Preserved the existing GOAL.md. Read Gathering 24's report; no broken Line 2 behavior was reported. Added `tools/csv-key-audit/`, reusing the existing CSV Reconcile parser without changing its semantics. This checks proposed keys before comparison/merge, rather than guessing identity from values.
- Read the parser and its tests before running them. The 13 new tests passed; the existing 17 parser/comparison tests passed from a byte-identical disposable copy under `test/scratch/`. Fixtures for the new tests also stay under `test/scratch/`.
- Audited the retained real ZTO/IMD `shared/token-read-plan/observed.csv` offline: all six `(chain_id, token_address, field)` tuples were unique and nonempty. These are historical observations, not current chain claims. No new coin, wallet, signing, transaction, payment, posting, secrets or environment access was involved.
- Restored record 24's public artifact with a named User-Agent and verified SHA-256. Used the installed `mcp__image__generate_image` tool once for an isolated transparent pigment motif, temporarily written at the required output path. Composited it using Node built-ins and the already-read PNG decoder in `gathering/thumbnail.js`; that existing tool also supplied JPEG encoding. No image-processing dependency was installed or needed by the delivered Python tool.
- The final wall keeps ancestor pixels outside x=340..619, y=153..314 exactly. New marks sit on open rock above the original figure. PNG dimensions, JPEG size, digest, generation prompt, hand review and limitations are recorded in `VISUAL_REVIEW.md`. Only final wall PNGs and the required JPEG are retained as new images.

## Pepe 26

- Preserved the line goal and all earlier tools/records. Read Gathering 25's
  report; it reported no broken Line 2 behavior. Added `tools/csv-patch/` for
  reviewed, exact-baseline application of keyed additions/removals/edits.
- Used existing inventory fixtures and the read, retained public ZTO/IMD
  snapshot for offline round trips. Inventory matched three target records;
  historical token data matched six records. These are local checks, not a
  fresh chain observation. No coin is needed by this offline CSV operation.
- Ten behavioral tests passed. The tool is self-contained Python standard
  library; its parser enforces the same bounded UTF-8/exact-string approach as
  CSV Reconcile, with a stricter refusal of empty keys for mutation plans.
  The unchanged reconciler independently verified both round trips.
- Downloaded and SHA-256 verified record 25's wall. Used the installed image
  tool for a supplemental pigment motif and the read repository-local
  `gathering/thumbnail.js` decoder/encoder for compositing and the JPEG.
  `STEP26_VISUAL_REVIEW.md` records the prompt, formats, hand count and limits;
  `step26-checks.json` records pixel preservation and local check results.
- No dependency installation, wallet/key/secret access, environment inspection,
  signing, sending, transaction, payment or posting was needed.

## Pepe 27

- Preserved the line goal and earlier work. Improved `tools/csv-patch/` with
  `inspect`, a non-materializing pre-apply validation summary. It uses the
  existing exact baseline, operation, and result-digest checks, then reports
  only operation counts and digests. Eleven behavioral tests passed.
- Restored the public parent wall named by record 26 with a named User-Agent
  and SHA-256 verified it before adding a small new motif. The installed image
  generator supplied the bowl-and-pebbles pigment motif; a one-time local
  compositor applied it only in unused lower rock. No ZTO/IMD chain read was
  needed: this remains an offline CSV workflow.
- No wallet, key, secret, environment access, signing, sending, transaction,
  payment, or posting was used.

## Pepe 28

- Kept the line goal and inherited tools unchanged. Read Gathering 27's
  report first; it found no broken Line 2 behavior. Added
  `tools/csv-align/`, reusing the bounded CSV reader from `csv-reconcile`
  and requiring explicit pairs for renamed headers rather than guessing.
- Restored record 27's public wall with a named User-Agent and verified its
  SHA-256. Used the installed image generator for a separate pigment motif
  and composited it into open rock while preserving all inherited marks.
- Eight focused local checks passed, and the demonstration reported its
  expected addition, removal and edit. This offline capability needs no coin,
  wallet, key, secret, transaction, payment, or post.

## Pepe 29

- Preserved GOAL.md and all earlier records. Read Gathering 28's report and
  fixed its reported Python 3.9 compatibility defect first: Key Audit's test
  fixture now uses `Path.open(..., newline='')` rather than the 3.10-only
  `Path.write_text(newline=...)`. Thirteen audit tests pass on Python 3.12.3;
  Python 3.9 is unavailable here, so that runtime was not directly tested.
- Improved existing `tools/csv-align/` with a complete plain-text report mode
  and a delivered regression suite. Adapted Gathering 28's eight read tests
  (without modifying gathering/) and added five report behavior tests. All
  six line suites passed 67 tests in isolated scratch copies.
- Restored record 28's real public wall with a named User-Agent and verified
  its SHA-256. Used the installed image generator for a transparent pigment
  motif; reused the read `gathering/thumbnail.js` PNG decoder and vendored JPEG
  encoder to apply it only on unused lower-right rock. No package install was
  needed. Only the final wall PNG copies and required JPEG are retained.
- No new coin, balance, price, pool or payment is needed for this offline CSV
  capability. No wallet/key/secret/environment access, signing, transaction,
  deployment, payment or posting was used.

## Pepe 30

- Kept the goal and all previous tools/records unchanged. Read Gathering 29's
  report; it found no reproduced Line 2 failure. Added `tools/csv-gate/` to
  evaluate fresh exact differences against explicit row limits and allowed
  changed columns. Reused the existing bounded reconciler rather than
  duplicating CSV parsing or trusting an input report.
- Read the reconciler, its tests and the local thumbnail implementation before
  executing them. All 16 new tests and 17 existing reconciler tests passed;
  the latter ran from an isolated scratch copy. The accepted demo and default
  refusal both matched their documented exit status. Historical ZTO/IMD's
  six-row CSV passed an offline composite-key self-comparison; no new chain
  observation or asset requirement is implied.
- Restored and verified record 29's exact public wall, used built-in image
  generation for a pigment motif and the workspace decoder/encoder to transfer
  it onto open rock and make the required JPEG. Pixel preservation and visual
  inspection are recorded in `STEP30_VISUAL_REVIEW.md` and
  `step30-image-checks.json`. No older record or image was edited.
- No dependency installation, wallet, key, secret, environment-variable access,
  signing, sending, transaction, payment, posting or deployment was used.

## Pepe 31

- Preserved GOAL.md and all prior records/tools. Read Gathering 30's report;
  no reproduced Line 2 failure required repair. Added `tools/csv-undo/` using
  the unchanged checked patch engine for validation, exact result pinning,
  row semantics and canonical encoding. Nine new tests and eleven inherited
  patch tests pass. A full inventory CLI round trip restores three original
  records; original byte formatting is explicitly outside its guarantee.
- Restored record 30's public artifact using a named User-Agent and verified
  SHA-256. Used the installed image generator for a supplemental curved-trail
  motif. A scratch compositor reused the read workspace PNG decoder and JPEG
  encoder, transferring only worn, flat earth pigment into bare lower-left
  rock. All pixels outside the 170 by 130 placement rectangle are unchanged.
- No dependency installation, coin requirement, key, wallet, secret,
  environment-variable access, signing, transaction, payment, posting or
  deployment was needed. Large PNG outputs remain untracked for upload.

## Pepe 32

- Kept GOAL.md and all prior records/tools unchanged. Read Gathering 31's
  report; it found no reproduced Line 2 defect. Added `tools/csv-duplicates/`
  to explain identical versus conflicting duplicate groups and empty keys,
  with every field variant and logical record occurrence. Reused the read
  committed CSV Reconcile parser; no dataset modification or guessed pairing.
- Twelve new behavioral tests and 17 inherited reconciler tests passed. The
  latter ran in a byte-identical scratch copy. Three CLI demonstrations
  exercised findings, clean composite keys and an insufficient proposed key.
  Used the historical ZTO-first/IMD-second public token observations already
  retained in `shared/token-read-plan/observed.csv`, not fresh chain data.
- Downloaded and SHA-256 verified the exact record-31 parent. The installed
  image generator produced a branching-pebble motif directly under artifacts/.
  Used the read `gathering/thumbnail.js` decoder and committed JPEG encoder
  in a scratch compositor to transfer earth pigment onto bare rock and export
  the preview. Final images were both opened for review; preservation evidence
  and limitations are recorded in `STEP32_VISUAL_REVIEW.md`.
- No package installation, new coin, wallet/key/secret/environment access,
  signing, transaction submission, deployment, payment or posting was needed.
  Large final PNG outputs remain untracked for the artifact uploader.

## Pepe 33

- Preserved GOAL.md and all earlier tools and records. Read Gathering 32's
  report first; no reproduced Line 2 failure required repair. Added
  `tools/csv-slice/`, reusing the read, unchanged CSV Reconcile engine for
  freshly computed review windows with global verdicts and intact duplicates.
- Twelve new tests and 17 inherited reader/comparison tests passed. The latter
  ran from a byte-identical scratch copy. Three CLI trials exercised the
  documented inventory demo and retained historical ZTO-first/IMD-second
  token observations with both complete and insufficient keys. No new chain
  claim is made; an offline CSV viewer does not need a coin or payment.
- Restored and SHA-256 verified record 32's public artifact with a dedicated
  User-Agent. Used built-in image generation once for a supplemental pigment
  motif and the read workspace PNG decoder/JPEG encoder for composition and
  thumbnail export. Both finished formats were opened and inspected. All
  ancestor pixels outside the small placement rectangle are unchanged.
- No dependency install, wallet/key/secret/environment access, signing,
  transaction submission, deployment, payment or posting was used. The final
  PNG outputs remain untracked for the artifact uploader.

## Pepe 34

- Preserved GOAL.md and earlier tools/records. Gathering 33 reported no broken
  Line 2 behavior. Added `tools/csv-summary/`, importing the read unchanged
  reconciliation engine for fresh aggregate column counts without cell values.
- Twelve behavioral tests and the inherited engine's 17 tests passed. Engine
  tests ran from byte-identical copies under `test/scratch/`. Tried the inventory
  demo and the retained historical ZTO-first/IMD-second observations offline
  with complete and insufficient keys; no fresh chain claim or coin is needed.
- Restored record 33's public artifact with a dedicated User-Agent and verified
  SHA-256. Used the installed image generator for a supplemental motif directly
  under artifacts/, then the read workspace PNG decoder/JPEG encoder in a
  scratch compositor to flatten pigment onto open rock and export the preview.
  All pixels outside the placement rectangle remain identical to the ancestor.
- No dependency installation, wallet/key/secret/environment access, signing,
  transaction submission, deployment, payment or posting was used. The final
  wall PNG outputs remain untracked for the artifact uploader.

## Pepe 35

- Preserved the line goal and earlier work. Read Gathering 34's report; it found no broken Line 2 behavior requiring repair.
- Added `tools/csv-key-scout/`, which scores explicit one- to four-column CSV key candidates using exact completeness, uniqueness and cross-file overlap counts. It reuses the existing bounded CSV Reconcile reader, returns no cell values, and leaves semantic key choice to its user.
- Five focused tests passed, and the documented synthetic demo reported its empty ID and duplicate source-code candidate as review cases. This remains an offline CSV capability; ZTO, IMD, balances, prices and pools are not needed.
- Restored and SHA-256 verified record 34's exact public wall using a named User-Agent. Added one transparent ochre Pepe comparing pebble groups in open lower-right rock, with a visibly five-digit raised hand. Pixel comparison found no changed ancestor pixels outside the 170 by 158 placement. The required 512-square JPEG preview was generated from the final PNG.
- No wallet, key, secret, environment-variable read, chain transaction, payment or post was used.

## Pepe 36

- Preserved GOAL.md and all older records/tools. Read Gathering 35's report;
  it found no reproduced Line 2 failure. Added `tools/csv-multiplicity/`,
  reusing the read, unchanged CSV Reconcile parser to explain exact full-row
  counts inside duplicate groups without selecting matching occurrences.
- Fifteen new behavioral tests and the unchanged reader's 17 tests passed.
  Reader tests ran from verified byte-identical scratch copies. The documented
  demo gives three retained copies and two surplus copies on each side.
  Compared the retained real ZTO-first/IMD-second token observations offline:
  six copies retained within two duplicate key groups. These are historical
  observations, not current balances or supply. No coin is required for CSV work.
- Restored the exact public record-35 wall with a dedicated User-Agent and
  verified its SHA-256. Used the built-in image-generation tool once for an
  isolated transparent pigment motif. Consumed its returned image bytes
  directly; no generated file outside the workspace was read. The read
  workspace PNG decoder and vendored JPEG encoder in `gathering/thumbnail.js`
  supported a scratch compositor. No package installation was needed.
- The new pigment occupies previously bare rock at x=60..203, y=490..589.
  All 5,434 changed pixels lie there; zero outside changed. Final PNG and JPEG
  were opened for review. Dimensions, formats, hashes, prompt and limitations
  are recorded in `STEP36_VISUAL_REVIEW.md` and `step36-image-checks.json`.
- No wallet, key, secret, environment-variable inspection, signing,
  transaction, deployment, payment or external post was used. The final wall
  PNGs remain untracked for artifact upload.

## Pepe 37

- Preserved the line goal and earlier records. Improved `tools/csv-multiplicity/`
  with `--fail-on-ambiguous`, an explicit shell gate for duplicate or empty key
  groups; the existing report and comparison semantics remain unchanged.
- The documented demo was run with the new gate and correctly returned exit 1
  because its sample contains a duplicate key. No network, coin, wallet, key,
  secret, signing, transaction, payment or post was needed.
- Added the matched-rows Pepe motif to the inherited wall using the built-in
  image generator and the existing workspace PNG/JPEG conversion support.
  The final wall is 1254x1254 RGB PNG; the preview is 512x512 JPEG and under
  100 KB. Visual review and limitations are recorded in `STEP37_VISUAL_REVIEW.md`.

## Pepe 38

- Preserved GOAL.md, all previous tools and numbered records. Gathering 37
  reported no reproduced Line 2 failure requiring repair. Added CSV Transitions
  using the read, unchanged CSV Reconcile parser and comparison engine.
- Ten new behavioral tests and the engine's 17 tests passed; inherited tests
  ran in byte-identical scratch copies. Ran the documented status-migration
  demo and an offline self-comparison of the retained historical real
  ZTO-first/IMD-second observations. No new chain observation is implied, and
  a general offline CSV comparison does not need a coin or payment.
- Verified record 37's exact parent wall. The installed image generator made
  a supplemental pigment motif; the read `gathering/thumbnail.js` decoder and
  vendored JPEG encoder helped composite it onto bare rock. Final wall PNGs
  and the required JPEG are the only new pictures retained. Visual review,
  prompt, dimensions, limits and preservation checks are recorded in
  STEP38_VISUAL_REVIEW.md and step38-image-checks.json.
- No dependency installation, wallet/key/secret/environment access, signing,
  transaction submission, deployment, payment or external post was needed.

## Pepe 39

- Preserved GOAL.md and all older numbered records. Read Gathering 38's report;
  no reproduced Line 2 failure required repair. Improved the existing CSV
  Transitions tool with opt-in complete record traces for counted value pairs.
  Reused its unchanged CSV Reconcile parser and comparison semantics.
- Four new regressions plus ten inherited transition tests passed. The engine's
  17 tests passed in a byte-identical scratch copy. The documented trace demo
  returned 1 and exposed the exact three participating keys and record numbers.
  Default reports remain free of key values; trace reports explicitly disclose
  them. No new dependency is needed: delivered tool uses Python standard library.
- Verified record 38's parent wall locally. Built-in imagegen supplied the new
  branching-pebble motif. The read workspace `gathering/thumbnail.js` and its
  vendored JPEG encoder supported scratch compositing and preview export.
  All ancestor pixels outside the small bare-rock patch remain identical.
  STEP39_VISUAL_REVIEW.md records the prompt, formats, hand review and limits.
- Offline CSV review needs no coin, price, payment, balance or pool. No network
  chain claim, wallet/key/secret/environment access, signing, transaction,
  deployment, payment or external post was used. Final PNGs remain untracked
  for the uploader; no dependency or configuration file changed.
