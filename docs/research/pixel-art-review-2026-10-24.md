# Review: Procedural Pixel Art Simulation Research (Gemini prompt 6)

Reviewed 2026-10-24. Source: Project file `Procedural Pixel Art Simulation Research.pdf`.

**Status (2026-10-28):** partly adopted. In the decision log (rev 8): palette-index terrain + palette-swap seasons, dithering rules, terrace/light/orphan-pixel recipe, no mixed pixel scales, semantic-zoom band markers and lineage badges, Endesga 32 (tested against the muted Earth palette and chosen), snowline winter instead of 75% Bayer snow, colour-blind safety not a v1 requirement. **Not yet decided** (carry into the spec as presentation defaults, each to be approved): outline rule, fire scars, trail decals, BitmapText labels + HTML Legends, ParticleContainer for crowds/smoke/fire, readability debug keys, Kenney CC0 glyphs, age-bracket bars on badges (lean skip), starvation shiver/thriving glow. Fire scars and trails need fields outside the slice (fire age, trail history).

## Verdict
The most directly useful report so far. Its rendering pipeline is sound and specific. Three things need correcting before adoption:
1. Its world-size maths is wrong for us.
2. Its snow recommendation is the "speckle" look Jordan already rejected.
3. Its colour-blind safety claim is broken by its own palette mapping.

## Spot-checks
| Claim | Result | How |
|---|---|---|
| Endesga 32 hex codes (all 32) | **Verified**, exact match | Lospec palette page |
| PixiJS v8 ParticleContainer uses `addParticle(new Particle())`, needs `boundsArea`, `dynamicProperties` flags | **Verified** | PixiJS docs via Context7 |
| `TextureStyle.defaultOptions.scaleMode = 'nearest'` + `roundPixels` for pixel art | **Verified** (note: not on `TextureSource.defaultOptions`) | PixiJS source via Context7 |
| Paul Tol "bright" scheme hex codes | Consistent with what I know; not re-fetched | Knowledge |
| Colour-blind matrices attributed to Viénot, Brettel & Mollon (1999) | **Misattributed** (inference from knowledge): the numbers match Machado et al. (2009) full-severity matrices. Still usable; they need linear RGB input | Knowledge |
| "v8.19 changed particle blend modes; v8.20 made ParticleContainer inherit tint/alpha" | Unverified (after my cutoff). Check the changelog when installing | - |
| Fantasy Map Simulator EA date, Noita chunk sizes, reviewer praise/criticism | Unverified; low stakes | - |
| Kenney Micro Roguelike, 1-Bit Pack, Tiny Town are CC0 | Consistent with what I know; check each licence file on download | Knowledge |

## Corrections
- **World size.** The report assumes a world of 8×8 to 16×16 regions of 192×192 pixels. Ours is 256×256 cells at 2 terrain pixels per cell, so about 512×512 terrain pixels for the whole world; the 192-pixel prototype is one region view. Band density per screen is therefore higher than it computed, which makes its clutter-culling advice more important, not less.
- **Snow.** It recommends Bayer-dithered snow filling up to 75% of lowland pixels. That is round one's "speckle", which Jordan called noisy. Keep palette-swap seasons plus snowline or drift clumps, with dither only at edges. Its point about the "winter flash" is valid: with seasonal ticks, snow should fade in over the season's playback in the viewer.
- **Colour-blind safety.** It takes Tol's safe colours and maps them to the nearest Endesga 32 colours (e.g. #4477AA → #0099db). The safety guarantee belongs to Tol's exact colours, so it doesn't survive the swap. The fix is in the report itself: run the colour-blind distance check on whatever colours we actually use.
- **Where palette indices are computed.** It puts terrain index generation "in the Web Worker". That's presentation; it belongs in the viewer or a separate render worker, not sim-core.
- **Rivers.** Its river technique is good, but rivers are deferred in v1 worldgen.

## Adopt (proposed; see status above for what has been adopted)
| Item | Why |
|---|---|
| Terrain stored as palette indices (one byte per pixel); seasons as palette rows swapped by a shader (CLUT) | Seasons read by colour, no overlays, no noise; one texture update per dirty region |
| Dithering rules: ordered 4×4 Bayer only for gradients (water depth, edges); clustered/stipple for vegetation and soil; never error diffusion on anything that changes | Prevents "boiling" when fields change each season |
| Terrain recipe: 4-6 elevation terraces, 1-step palette shift for NW light / SE shadow, orphan-pixel cleanup pass | Makes code-generated terrain look hand-placed |
| Outline rule: near-black outlines only on bands, herds, camps and event glyphs; terrain uses the darkest shade of its own ramp | Living things stand out; no "pixel soup" |
| Semantic zoom for bands: World = small abstract markers with priority culling (one marker per 16×16 screen pixels, stack shadow for hidden ones); Region = lineage badge; Close-up = camp plus a swarm of tiny figures | Resolves the camp/swarm/standard choice: each one wins at a different zoom |
| Lineage badges: two-tone split keeps the parent's colour in one half, plus a 1-bit glyph | Kinship stays readable after many splits; works for colour-blind viewers through shape |
| Fire scars: fresh burn charcoal, green shoots dithering back over several seasons (driven by fire age) | The land shows its history, as in the brainstorm |
| Trails as fading footpath decals that build up into corridors where bands keep walking | Visible migration routes; presentation-only |
| BitmapText for map labels; Legends as an HTML panel | Crisp labels; readable long text |
| ParticleContainer for crowds, smoke, fire; normal Sprites for band badges | Verified API; fits the counts |
| Readability debug keys: blur (squint), greyscale, colour-blind views, worst-case stress scene | Cheap, objective checks for a solo dev |
| Kenney CC0 1-bit / Micro Roguelike as the glyph source, recoloured in code | Consistent, free, no drawing |

## Test before adopting
- **Endesga 32 as the master palette.** Done: tested in look test v3; Endesga 32 chosen (decision log rev 8).
- **Age-bracket bars on a 10×10 badge** (1-4 px per edge). Probably too fine to read; lean skip.
- **Starvation "shiver" and desaturation, thriving glow.** Fine as presentation; low priority.

## Not adopted
- Error-diffusion dithering anywhere dynamic.
- Rotating pixel sprites (use flips).
- Full-screen tint overlays for seasons (round one did this in tabletop; it muddies everything).
- Mixed pixel scales on screen at once ("mixels"). Round one scaled tokens 1.7× in tabletop; pixel mode must not.
