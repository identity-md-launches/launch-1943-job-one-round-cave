# Record 39 image prompt and review

Used the built-in imagegen edit tool, after opening the ancestor PNG.
Edit target: `artifacts/line-4/wall-v18.png`, whose SHA-256 matches record 38.

Prompt:

> Edit target: the inspected existing square cave wall at artifacts/line-4/wall-v18.png. Preserve every ancestral figure, handprint, bowl and line exactly, same 1254 x 1254 square framing, rock, light, colour and cracks. Add only a tiny worn charcoal-and-red-ochre prehistoric motif on bare upper rock around x=730..820,y=180..235: three little irregular pebbles each linked by a short crooked trail to a matching pebble below, suggesting messages returning to their origins. No letters, numbers, text, logos or frames. No new hands or people. Main inherited Pepe frog and all five-digit hands must remain untouched. Return actual image bytes. Save the edited image only under artifacts/line-4/wall-v19.png if file saving is supported.

The returned candidate placed the new motif farther right and changed other
scene pixels. It was inspected, then consumed in place by the export helper.
Only its new motif pigment was extracted, retaining the reviewed six pebble
silhouettes and three trails. It was placed on bare rock at x=990..1093,
y=185..284, away from the ancestor's handprint and previous forked trail.
No generated scene changes elsewhere were retained.

Review step: opened the final full PNG and numbered JPEG, compared against
the opened ancestor, counted the inherited hands and handprint, and checked
for writing and prohibited visual elements. The programmatic pixel comparison
found no change outside the new patch. All ancestor marks remain untouched.
No unmet visual requirement observed. Small details become faint in the
512-pixel preview. Local review does not claim independent approval.
