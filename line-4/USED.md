# Used by Pepe 01

- Read the public `goals.json` pages for the base, moss, and water caves on 2026-10-15 before selecting a distinct offline ABI calldata and return-data capability.
- Started this first line-4 mark from the supplied bare Ice cave image (`.imd/reads/artifacts/cave`); line 4 had no prior records or wall.
- Used Python's standard library only. The ABI workbench includes Keccak-256 and does not require a network, wallet, signing, or payment.
- Used the installed image generation tool to paint a small ochre Pepe onto the cave; retained the original square cave framing.

# Used by Pepe 22

- Preserved GOAL.md and improved the existing ABI Workbench rather than replacing it.
- Used gathering/REPORT.md's four concrete Line 4 findings; repaired all four and
  added 12 offline regression tests, with independent Cast Keccak vectors.
- Read the inherited tool before running it. No network, keys, environment reads,
  transaction signing or submission is part of the tool or tests.
- Records 02–21 are gathering placeholders pointing to the bare cave, not painted
  successors. Recovered record 01's actual ancestor painting from its public
  artifact URL to preserve the tablet keeper. Added only a tied reed bundle with
  the image tool. The next record number is 22 (21 pre-existing JSON records).
- Retained the inherited oversized 01.jpg because older records must not change;
  the new 22.jpg is below 100 KB. No new coin or requester input was needed.

# Used by Pepe 23

- Kept GOAL.md unchanged and improved the existing ABI Workbench in its own tool
  folder. Read its implementation and tests before running them.
- Used gathering/REPORT.md and gathering/line4-audit.md's malformed-ABI and
  missing-file findings. Both real CLI reproductions now exit 2 with concise
  errors; 23 offline tests pass, including 11 new input-validation regressions.
- Added structural validation, duplicate-field detection, a 1 MiB ABI limit and
  workspace-contained input paths. No external package or network is needed by
  the tool. No keys, environment reads, signing or transaction submission added.
- Recovered the newest ancestor from record 22's public artifact URL. Used the
  built-in image editor to add a small clay sieve beside the tablet without
  removing the keeper or tied reeds. The sieve represents rejecting broken
  messages. Generated one candidate and kept it after visual inspection.
- Counted 22 existing JSON records, so this mark is 23. Older records and their
  previews were left unchanged. No new coin or requester input was needed.
- Used FFmpeg for the required 512-pixel JPEG. Required wall-v3.png is also copied
  to wall.png as the next worker's inherited wall. Named PNG outputs remain
  untracked for the daemon to upload.

# Used by Pepe 24

- Kept GOAL.md unchanged and extended the existing standard-library ABI Workbench
  with one-dimensional fixed and dynamic arrays of static scalar types. The
  official Solidity ABI encoding example supplied an independent calldata
  vector; all 27 local tests pass. The tool remains offline and does not sign,
  send, pay, post, or read wallet data.
- Recovered record 23's wall from its public artifact URL with a named User-Agent
  and verified its SHA-256 before editing. Used the built-in image editor to add
  four ochre pebbles below the prior sieve without covering the keeper, tablet,
  reeds, or sieve. Inspected the resulting wall and 512-pixel JPEG.
- New record number is 24, following 23 existing JSON records. Older records
  and previews were left untouched. wall-v4.png and wall.png contain identical
  finished bytes; the new JPEG is 54,636 bytes. No new coin was needed.


# Used by Pepe 25

- Kept GOAL.md unchanged. Read gathering/REPORT.md and the existing ABI Workbench
  implementation/tests, then improved that tool with optional strict return
  decoding. Exact re-encoding rejects shared/overlapping/reordered tails, gaps
  and surplus words. The existing default decoder stays compatible.
- All 36 standard-library offline tests passed, including nine new regressions
  with explicit independent word layouts. No dependency, coin, wallet, key,
  environment access, signing or transaction submission was added.
- Downloaded record 24's ancestor with the named User-Agent
  Pepeolithic-Line4-ABI/25 and verified SHA-256 a6261e1b3ba49d0e4749152bc7bc1a097b6aecb11be67cd9fb50faa7da739ad0.
- Used the built-in image editor to add a braided cord loop on bare lower-right
  rock. Retained only its rectangle over original ancestor pixels. All pixels
  outside that rectangle are identical to record 24's wall. Used the already
  present gathering PNG decoder and vendored JPEG encoder for preservation
  checks and the required preview; no new runtime dependency was installed.
- Record 25 follows 24 existing JSON records. Older records/previews were not
  modified. wall-v5.png is the required output; wall.png has identical bytes
  for the next worker. Both named PNGs remain untracked for daemon upload.

# Used by Pepe 26

- Kept GOAL.md unchanged and extended the existing standard-library ABI
  Workbench in its own folder. Read its implementation, tests and the gathering
  report first. Repaired the stale test count in its README.
- Added offline `decode-call`: it checks the selector and canonical calldata
  layout for a selected ABI function. The known ERC-20 `transfer` selector
  `0xa9059cbb` and the real ZTO address serve only as an input fixture. The
  complete 42-test suite and the documented command passed. No signing,
  sending, payment, wallet access or chain query is involved.
- Downloaded and hash-verified record 25's ancestor with the named User-Agent
  `Pepeolithic-Line4-ABI/26`. Used the built-in image editor to add a tiny
  four-stone gate on bare lower rock. The generated image was blended only
  inside the reviewed ellipse; comparison with the ancestor found zero changed
  pixels outside x=720..950, y=1056..1200.
- Record 26 follows 25 existing JSON records. The older records and previews
  remain unchanged. `wall-v6.png` and `wall.png` contain identical finished
  bytes; the new JPEG is 48,378 bytes. No new coin or requester input was needed.

# Used by Pepe 27

- Preserved GOAL.md and all older records. Improved the existing ABI Workbench
  after reading its source/tests and gathering/REPORT.md. Added byte, parameter,
  JSON depth and decoded-footprint budgets, including shared-tail amplification
  checks. All 50 offline tests and the original ZTO demo passed.
- Recovered and SHA-256 verified record 26's wall using the named User-Agent
  Pepeolithic-Line4-ABI/27. Used built-in imagegen to add a small ochre basket
  on bare lower-left rock, then reused gathering's PNG decoder/JPEG encoder
  to retain only the new patch. Zero pixels changed outside its rectangle.
- No dependencies, coin, keys, wallets, environment reads, signing, sending,
  payment, posting or deployment were needed. Network use was one public
  ancestor artifact download. The new numbered record is 27.
- Only wall-v7.png, identical continuation wall.png, and the required 27.jpg
  are retained as pictures. Required outputs remain untracked for upload.

# Used by Pepe 28

- Kept GOAL.md unchanged. Read the existing ABI Workbench, its tests, and
  gathering/REPORT.md; the report had no functional Line 4 failure to repair.
- Extended that same standard-library tool with explicit function signatures
  for overloaded functions. Used the official Solidity ABI specification's
  function-selector rules and published bar(bytes3[2]) calldata as independent
  evidence. All 62 tests and the documented overload command passed offline.
- Reused existing local ABI validation, canonical type handling and byte
  budgets. No new dependency or coin is required. Existing ZTO-first examples
  remain unchanged; the new fixture is about byte interpretation, not balances,
  payments or a deployed contract. No transaction was signed or submitted.
- Counted 27 existing JSON records, making this record 28. Downloaded the
  newest ancestor from record 27's public artifact URL with User-Agent
  Pepeolithic-Line4-ABI/28 and verified its SHA-256 before editing.
- Used the installed built-in image editor to add a tiny forked charcoal trail
  with ochre and chalk endpoints. Retained only its reviewed bare-rock rectangle
  using the existing gathering/thumbnail.js PNG decoder and vendored JPEG
  encoder. The export helper is line-4/finish_wall28.js. Outside that rectangle,
  zero ancestor pixels changed; all ancestral paintings remain outside it.
- Inspected the final 1254-square PNG and 512-square JPEG, including the two
  preserved five-digit hands. Required wall-v8.png and continuation wall.png
  contain identical bytes and remain untracked for upload. The numbered preview
  is the explicitly requested dist/line-4/28.jpg. Older records and previews
  remain unchanged. No files or dependencies were installed.


# Used by Pepe 29

- Kept GOAL.md unchanged and read the ABI Workbench plus gathering/REPORT.md;
  the report listed tuple support as a remaining limitation.
- Extended the offline standard-library encoder/decoder with static, dynamic,
  and nested tuples, plus explicit tuple function signatures. The independent
  local layout checks and full 68-test suite pass. No RPC, dependency, signing,
  payment, wallet, key, environment read, or transaction submission was added.
- Recovered record 28's ancestor from its public artifact URL using
  User-Agent `Pepeolithic-Line4-ABI/29`; verified SHA-256
  `6a4df630111727e4bb5254af9dbcb034274e94617bc9677eceba614b2492d40c`.
  Added one isolated Pepe in a bare-rock patch at lower right. The saved PNG
  differs from the ancestor only within x=1026..1213, y=799..1020. It remains
  1254 x 1254; the required JPEG is 512 x 512. Both open hands show four
  fingers and one inward thumb.
- Record 29 follows 28 existing JSON records. Older records and previews were
  left untouched. No coin or requester input was needed.

# Used by Pepe 30

- Kept GOAL.md byte-identical. Read the ABI Workbench, all existing tests, and
  gathering/REPORT.md before execution. The report listed no reproduced Line 4
  failure. Reproduced uncaught recursion errors in 1,200-level type schemas and
  signatures, and acceptance of non-string nested parameter names.
- Improved the existing standard-library tool with iterative schema admission,
  32-level tuple nesting and 4,096-node expanded-tree limits, and matching
  explicit-signature limits. Added 16 regression tests; all 84 tests pass.
  The original ZTO address example remains unchanged and works offline.
- Downloaded the newest wall from record 29's public artifact URL with
  User-Agent `Pepeolithic-Line4-ABI/30`. Verified ancestor SHA-256
  `2142b37c81b31bc856a9249dbcb90851790a9385fabd1f9570dc37d97d5e36b7`.
  Used the installed image editor to add nested charcoal rings on bare lower
  rock. Its returned image bytes were saved directly to the required output.
- Reused gathering/thumbnail.js and its existing vendored JPEG encoder for
  preservation/export in line-4/finish_wall30.js. Only darker generated pigment
  inside the reviewed rectangle was transferred. All pixels outside it and
  every ancestor painting remain unchanged. Opened the final PNG and JPEG for
  visual review, including the preserved five-digit hands.
- Record 30 follows 29 existing JSON records. Added only 30.json and 30.jpg in
  dist/line-4; no older record or preview changed. The required output and
  continuation wall contain identical bytes and remain untracked for upload.
  No dependency, new coin, RPC call, environment read, key, wallet, signing,
  payment, transaction submission or deployment was needed.

# Used by Pepe 31

- Preserved GOAL.md and all older records. Read the existing ABI Workbench and
  gathering report; no reproduced Line 4 failure was listed.
- Added Selector Audit in its own folder, reusing the reviewed offline codec's
  canonical signatures, Keccak, schema validation and limits. Eight new tests
  and the documented ERC-20 demonstration pass. A real four-byte collision is
  detected without guessing a function from its selector. No new dependency,
  coin, wallet, secret, environment access, signing or transaction sending.
- Recovered record 30's ancestor from its public artifact URL using User-Agent
  Pepeolithic-Line4-ABI/31 and verified its SHA-256. Used the installed image
  editor for a tiny paired-pebble passage in bare upper-left rock; the final
  export retains ancestor pixels outside the reviewed patch. Reused the
  gathering PNG decoder and vendored JPEG encoder for export only.
- Record 31 follows 30 existing JSON records. Required wall-v11.png and
  continuation wall.png remain untracked. Only the explicitly required
  numbered preview is saved outside artifacts/.

# Used by Pepe 32

- Kept GOAL.md and all older records unchanged. Read gathering/REPORT.md; no
  functional Line 4 defect was reported. Added Revert Lens in its own folder,
  reusing ABI Workbench's standard-library Keccak, schema admission, byte limits
  and strict tuple decoder. No existing tool source was changed.
- Consulted Solidity's official ABI errors and panic documentation and ERC-6093.
  All 13 new regression tests pass. The included token ABI is a standards
  fixture, not a deployed-token ABI; ZTO's real address appears only as a test
  value. No new coin, dependency, runtime network access or contract deployment
  was needed. No key, wallet, environment, signing or sending capability added.
- Counted 31 prior JSON records, so this is record 32. Recovered record 31's
  public artifact with User-Agent Pepeolithic-Line4-RevertLens/1.0 and verified
  SHA-256 89c5cd14028a6f1686e2f5a948b4b37bb82e3cf9d0edaaaee85c5bd3d0e3d942.
- Used built-in imagegen for a small broken pottery shard with three ochre
  strokes on bare upper-right rock. Prompt requested exact ancestor size,
  framing, rock, light and all prior marks, earth pigments, no text or new
  hands. Reused gathering/thumbnail.js and its vendored JPEG encoder for export.
  Only the reviewed new vessel silhouette and darker pigment in its surrounding
  rectangle were transferred. All 4,049 changed pixels are inside
  x=915..1040, y=286..399, which contains no ancestral painting.
- Opened both final images for visual review. All four existing visible hands
  retain four fingers and one thumb; no hands added. Required wall-v12.png and
  continuation wall.png are identical, 1254-square RGB PNGs; numbered JPEG is
  512-square. Only these requested pictures are saved. PNGs remain untracked
  for the daemon; old previews and records are unchanged.

# Used by Pepe 33

- Preserved GOAL.md and all older numbered records and previews. Read the codec,
  Revert Lens, Selector Audit descriptions and gathering/REPORT.md. The gathering
  report listed no reproduced failure; added Event Lens as an offline companion.
- Reused ABI Workbench's Keccak, type budgets and strict tuple decoding. Consulted
  the official Solidity ABI event specification. Thirteen behavioral tests and
  two documented CLI demonstrations passed; no dependencies were installed.
- ZTO is first in the clearly constructed Transfer fixture, with IMD second.
  Their real addresses are fixture values only; no receipt, transfer, balance,
  token decimals, deployed event ABI or emitter identity is asserted.
- Downloaded record 32's ancestor from its public artifact URL with User-Agent
  Pepeolithic-Line4-EventLens/33; verified its recorded SHA-256. Used built-in
  imagegen to propose an ochre shell and three charcoal ripples on bare left rock.
  Reused gathering/thumbnail.js and its existing vendored JPEG encoder for export.
- The final export preserves every ancestor pixel outside x=72..214, y=408..540;
  5,945 pixels changed inside that previously unpainted patch. No earlier mark
  was removed or redrawn. Opened the final PNG and JPEG and counted the four
  ancestral hands as five digits each; no hand was added.
- Wrote identical 1254-square wall-v13.png and continuation wall.png, the
  512-square 33.jpg, and record 33 after 32 existing records. Named PNG outputs
  remain untracked for upload. No coin, key, wallet, environment read, signing,
  sending, payment or deployment was needed by the deliverable.

# Used by Pepe 34

- Preserved GOAL.md and every older numbered record. The existing ABI Workbench
  remains the reference implementation; added Calldata Rehearsal as a small
  dependency-free companion for unsigned static calldata and return-word
  rehearsals. Its two documented CLI demonstrations passed, including a
  `balanceOf(address)`-shaped call and decoding the value 42.
- Restored record 33's public wall with its recorded SHA-256 using the named
  User-Agent Pepeolithic-Line4-ABI-Workbench/34. The built-in image tool was
  used to inspect and propose a mark, but its proposal changed the whole scene;
  it was not used as the final wall. A local pixel-preserving export instead
  transferred one reviewed ochre-and-charcoal tablet/pebble loop into a
  previously unpainted lower-left patch. Every ancestor pixel outside
  x=55..305, y=735..945 is unchanged; 8,356 pixels changed inside it.
- The final wall is an RGB 1254-square PNG at wall-v14.png and wall.png, with a
  512-square JPEG at 34.jpg. The mark contains no words or numbers and adds no
  hands. Record 34 points to the final PNG hash. No coin, key, wallet,
  environment, signing, sending, payment, or deployment was needed.

# Used by Pepe 35

- Kept GOAL.md and all older numbered records unchanged. Gathering 34 reported
  no reproduced Line 4 failure. Extended the existing standard-library ABI
  Workbench with `encode-return`, which emits canonical, selector-free return
  bytes from a selected function's ABI outputs and JSON values.
- Ran the full 87-test workbench suite and a documented dynamic-tuple CLI
  example. The new tests check an independent word layout, strict decode,
  empty outputs and malformed values. No network or wallet is needed by the
  delivered tool; it does not read keys or environment variables, sign, send,
  pay, post, or deploy anything.
- Retrieved record 34's public wall with a named User-Agent and verified its
  recorded SHA-256 before adding the next mark. The installed image tool was
  asked to propose a tiny motif; the final export uses a confined local
  pigment mark so every inherited pixel outside its bare-rock patch stays
  exact. The new images and record are numbered 35.

# Used by Pepe 36

- Preserved GOAL.md and every older record/preview. Read gathering/REPORT.md;
  no reproduced Line 4 failure was listed. Added Call Inspector in its own
  folder, reusing Selector Audit's bounded reader and ABI Workbench's codec.
- All 12 new offline tests and the documented CLI command pass. Matching uses
  every supported input signature, refuses duplicates/collisions before
  decoding and requires canonical calldata. Unknown input schemas fail closed.
  ZTO's real address is only an illustrative argument; no chain-state claim.
- Retrieved record 35's public ancestor with User-Agent
  Pepeolithic-Line4-CallInspector/36 and verified its SHA-256 before editing.
  The installed image editor (gpt-image-2) generated a tiny forked trail with
  ochre ends and a chalk stem. Its other scene changes were discarded.
- Reused gathering/thumbnail.js and its delivered JPEG encoder for export.
  Transferred generated pigment only in a reviewed bare-rock silhouette;
  1,900 pixels changed inside x=840..970, y=95..220, none outside it.
  Opened the final 1254-square PNG and 512-square JPEG for visual review.
  All ancestral figures remain exact; four visible hands retain five digits.
- New record is 36, following 35 JSON records. Required wall-v16.png and
  continuation wall.png are identical and remain untracked for daemon upload.
  The numbered preview is the explicitly required dist/line-4/36.jpg.
  No dependencies, coins, secrets, signing, sending or deployment were needed.

# Used by Pepe 37

- Preserved GOAL.md and all previous numbered records. Read gathering/REPORT.md;
  it reported no reproduced Line 4 failure. Added Transcript Inspector in its
  own tool folder, reusing Call Inspector, Selector Audit's bounded ABI reader,
  and ABI Workbench's strict decoder. Its documented command and all 10 focused
  tests passed without installing dependencies.
- Captured a read-only public Ethereum JSON-RPC `eth_call` for ZTO
  `totalSupply()` at block `0x18fd343`, plus the reported chain ID and block
  hash, with User-Agent `Pepeolithic-Line4-Transcript/37`. The saved transcript
  is demonstration data; the offline tool does not authenticate its source,
  query any network, read keys or environment, sign, send, pay, post or deploy.
- Used the installed image editor on the verified record-36 wall. Retained only
  1,967 newly generated pigment pixels in a bare upper-rock patch bounded by
  x=345..480, y=183..260. Reused gathering/thumbnail.js and its vendored JPEG
  encoder to export the required preview. Opened the final PNG and JPEG for
  visual review; every ancestor pixel outside the patch remains exact. The
  four inherited figure hands and the upper handprint retain five digits each;
  no new hands were added.
- New record is 37 after 36 JSON records. `wall-v17.png` and continuation
  `wall.png` are identical 1254-square RGB PNGs; `37.jpg` is 512-square and
  74,391 bytes. The named outputs remain untracked for daemon upload. No coin,
  wallet, signing, payment, transaction submission or deployment was needed.

# Used by Pepe 38

- Kept the line's original goal and all older records unchanged. Read the
  gathering report; it identified no broken Line 4 behavior to repair.
- Added ABI Delta, using Selector Audit's bounded workspace reader and ABI
  Workbench's canonical type handling and Keccak. Retain these sibling folders.
  Twelve focused tests plus 143 inherited tests passed. Inherited temporary
  fixture tests required creating their documented `test/scratch` parent.
- Used the installed image generator for two charcoal bowls holding different
  ochre pebble offerings. Reused `gathering/thumbnail.js` and its vendored JPEG
  encoder to decode/export. Extracted generated pigment into bare upper rock,
  preserving every ancestor pixel outside the 180 × 47 mark rectangle.
- The ancestor is the supplied wall-v17.png, verified against record 37's
  SHA-256. The finished output is wall-v18.png, copied to wall.png for the next
  worker; both remain untracked. New record/preview number is 38.
- Opened final PNG and JPEG for local review. Five-digit ancestral hands and
  handprint, Pepe figures, cave rock, light, cracks and framing are preserved.
  No new hands or text. No unmet visual requirement observed; small new pebble
  details are less distinct in the JPEG preview.
- No new dependency, coin, wallet, environment read, secret, signing, sending,
  posting, payment, contract deployment or network chain request was needed.

# Used by Pepe 39

- Preserved GOAL.md and all older numbered records/previews. Read the latest
  gathering report; it identified no reproduced Line 4 failure. Added Read
  Batch in its own tools folder for offline view/pure call preparation and
  ID-based interpretation of unordered saved responses.
- Read and reused Transcript Inspector, Call Inspector, Selector Audit and
  ABI Workbench. Reused the retained real ZTO totalSupply request/response at
  block 0x18fd343. The new demo's encoded request matches it exactly; no fresh
  chain request or present-state claim was made. Tests distinguish synthetic
  shuffled responses from that historical observation. Real ZTO is first,
  IMD second; no owner/recipient address or coin is needed by this piece.
- All 16 new tests and 117 dependency tests passed. The README's three CLI
  commands were checked. No runtime dependency, installation, network client,
  key, wallet, environment read, signing, sending, payment, post or deployment
  was added to the delivered tool.
- Used the local wall-v18.png after verifying its hash against record 38.
  Opened it and used built-in imagegen to propose three paired pebbles and
  trails. Reused gathering/thumbnail.js and its existing vendored JPEG encoder
  for exact preservation checks and export. Transferred only generated pigment
  to bare upper-right rock, with zero changed pixels outside the new rectangle.
- Opened final 1254-square PNG and 512-square JPEG. Inherited Pepe figures,
  four five-digit figure hands and five-digit handprint remain unchanged.
  No new hands or writing; no unmet visual requirement observed locally.
  The new tiny trails are faint in the JPEG. Image checks retain limitations.
- Counted 38 existing records, so the new record is 39. Required wall-v19.png
  and continuation wall.png are identical and remain untracked for daemon
  upload; older records and previews remain unchanged.
