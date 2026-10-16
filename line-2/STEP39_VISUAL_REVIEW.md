# Pepe 39 — The Traced Pebbles

Improved CSV Transitions with `--include-records`: exact keys and logical
before/after record numbers explain every counted transition. The existing
summary output and global verdicts remain unchanged by default. The tool's
README gives the working command, observed result and limitations.

The exact inherited wall, `artifacts/line-2/wall-v18.png`, matched record 38's
SHA-256 `dbc4fb9a0032237508fe3b4639ff064b946af84309ddc4ea4c3ec7c4b393d749`.
No restoration download was needed. Built-in imagegen generated the new motif
with this prompt:

> Create an isolated small prehistoric pigment motif for addition to an existing cave painting. A short uneven charcoal branching trail connects a single red ochre pebble above to two small yellow ochre pebbles below, representing tracing a grouped count back to its members. Simple hand-daubed worn flat earth pigment, Lascaux cave art. Transparent background. Centered with generous transparent margin. No text, letters, numerals, arrows, logos, watermarks, border, hands, people or frogs. Only the tiny pebble-and-trail motif. The existing cave painting and Pepe figures will remain untouched.

Consumed returned image bytes directly, without reading generated files outside
the workspace. A scratch Node compositor used the read repository-local PNG
reader and JPEG encoder, transferred only the generated pigment silhouette,
flattened it to earth pigments, and blended it into previously bare left rock.
The staging image was replaced with the final wall; no extra image is retained.

Final files:

- `artifacts/line-2/wall-v19.png` and identical continuation `wall.png`:
  **1254 × 1254 RGB PNG**, preserving the inherited square framing.
- `dist/line-2/39.jpg`: **512 × 512 JPEG**, **75,212 bytes**.
- `dist/line-2/39.json`: the requested metadata shape, with full-wall SHA-256 URL.

Local visual review: opened both final PNG and JPEG. The branching motif is
contained in x=65..169, y=790..924. All **4,328 changed pixels** lie in that
rectangle; **zero pixels outside changed**. Ancestor figures and markings,
rock texture, cracks, colour, light and framing remain intact. The principal
Pepe retains his wide mouth, heavy-lidded eyes and two five-digit hands (four
fingers and a thumb). The two raised right-hand ancestor hands also retain
five digits. No hands or stencils were added. Small folded/occluded limbs
remain as inherited. No writing, logo, watermark, frame, political or hateful
symbol was observed. **No unmet visual requirement found in local review.**
The charcoal connection is faint in the small preview; this review does not
constitute independent artistic approval. Machine measurements are retained
in `step39-image-checks.json`.
