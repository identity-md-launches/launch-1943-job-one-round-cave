# The Returning Pebbles — Line 4, record 39

[Read Batch](tools/read-batch/README.md) prepares ABI-encoded read-call batches
and interprets saved JSON-RPC responses in request order, matching IDs rather
than response positions. It retains missing replies, RPC errors and malformed
returns beside successful decodes, and refuses duplicate or unexpected IDs.
It extends the unchanged offline calldata/return interpretation goal.

```sh
python3 -B line-4/tools/read-batch/read_batch.py demo
```

Tried: exit 0, a prepared request exactly matching the retained real ZTO
`totalSupply()` call at block `0x18fd343`, decoded as raw uint256 `10^27`.
This is historical evidence, not a fresh query or current supply claim. The
tool sends nothing, reads no keys or environment values and installs nothing.
Its standard-library implementation reuses four existing sibling tools.
All 16 new behavioral tests and 117 dependency tests passed. Commands and
results are in [checks39.json](checks39.json); the demo is retained in
[demo-checks39.json](demo-checks39.json).

The new mark is three pairs of ochre pebbles connected by crooked charcoal
trails: replies find their own origins. Built-in imagegen produced the motif
in an edit of the verified record-38 wall. Only generated pigment in the
reviewed motif silhouette was transferred onto previously bare upper-right
rock. All 2,775 changed pixels lie inside x=990..1093, y=185..284;
every pixel outside remains exactly equal to the ancestor. Existing figures,
paintings and handprint were not moved, erased or redrawn.

Required `artifacts/line-4/wall-v19.png` and continuation `wall.png` contain
identical 1254 × 1254 RGB PNG bytes. `dist/line-4/39.jpg` is a 512 × 512 JPEG,
74,464 bytes. Record 39 follows 38 existing records and references the full
PNG's SHA-256. All older records and previews remain unchanged. The PNG
outputs remain untracked for daemon upload.

Opened the final PNG and JPEG for local visual review. The inherited Pepe
figures retain their wide mouths, heavy-lidded eyes and five-digit hands.
The four figure hands and upper handprint have four fingers and one thumb
each; no hands were added. Warm cave rock, cracks, light, colour and framing
remain. No letters, numbers, captions, signatures, logos, watermarks, borders,
real people or prohibited symbols were observed. No unmet visual requirement
was found locally. The tiny new trails are faint at preview size; this review
is not independent visual certification. Dimensions, hashes, preservation
checks and limitations are retained in [image-checks39.json](image-checks39.json).

[finish_wall39.js](finish_wall39.js) documents the one-time composition/export;
it requires the original generated candidate and rejects a finished-wall rerun.
[IMAGE_PROMPT39.md](IMAGE_PROMPT39.md) retains the prompt and selected review.
The reusable worker command is the Python demo above.
