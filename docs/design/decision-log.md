# Living mythos: decision log

Last updated: 2026-10-31 (rev 23). Sources: planning chats, handoffs #1-#7, research/stack-and-prior-projects-report.md, research/timescale-report.md, research/novelty-report-gemini.txt, research/tooling-report.md, research/pixel-art-review-2026-10-24.md, research/vegetation-drought-review-2026-10-30.md, research/forager-reports-review-2026-10-31.md, design/integration-review-2026-10-30.md, archive/research/batch-review-2026-10-23.md (Gemini reports 2-5 + repos). This is the record of what's settled; the spec builds on it.

Rev 9 (2026-10-24): forks recorded as a v1 stretch goal (option C); first spec scoped to the success-test slice.
Rev 10 (2026-10-28): cloud sessions for tests and tooling only; information default is investigate-to-learn with a lab coat toggle (brainstorm Q3 resolved).
Rev 11 (2026-10-28): v1 god tools = rain/drought + bloom; camp diorama folded into Close-up, reading a read-only camp snapshot (brainstorm Q4, Q5 resolved). All brainstorm questions closed.
Rev 12 (2026-10-30): implementation state recorded for hard rules 3, 5, 7 (built on the laptop); event content key gains an ordinal; causes may be events or nudge commands; config and event payloads are integer-only; repo mirrors the Project docs in `docs/`; Windows `pnpm check` passed.
Rev 13 (2026-10-30): RNG keys use the full 64-bit entity ID (`entityHi` field); fixes the 32-bit entity-key collision risk.
Rev 14 (2026-10-30): primary PBT skill settled (fast-check). Slice spec at v0.2 draft; its open questions are grilled one at a time and land here as they settle.
Rev 15 (2026-10-30): number representation (spec Q0): doubles in sim state, basic arithmetic only.
Rev 16 (2026-10-30): map size and catchment (spec Q1): 128×128 slice default, Euclidean disc catchment r = 3.
Rev 17 (2026-10-30): event emission (spec Q2): transition records + one emitter pass; world events use ROOT_ID; ordinal (rev 12) confirmed.
Rev 18 (2026-10-30): worldgen and capacity (spec Q3): gradient noise, one landmass for the slice, continuous vegetation capacity; biomes are labels.
Rev 19 (2026-10-30): climate regime shape (spec Q4): space-time noise, regional dry spells with hysteresis; target ~15% of seasons dry per region (tuning band 12-18%).
Rev 20 (2026-10-30): drought command (spec Q5): core-and-fade disc, stacking after the natural clamp; command causes (rev 12) confirmed.
Rev 21 (2026-10-30): vegetation response (spec Q6): die-back toward K, rates vary with base moisture; targets from the prompt 7 review.
Rev 22 (2026-10-30): large fauna (spec Q7): herd-condition model with Type II intake and required density mortality (prototype-verified).
Rev 23 (2026-10-31): whole-system review opened during spec Q8 (`design/integration-review-2026-10-30.md`); R1 settled: food comes from resource guilds behind one interface, energy-only currency. Replaces Q8's framing; R2-R4 are grilled before spec Q9-Q14.

## Vision
A terrarium you poke: an observational god-view sandbox where bands of people develop, change the land and each other, and make history in unexpected, funny and exciting ways. You watch, read the history, zoom in, and nudge things to alter the course. Jordan's framing: "like a kid with an ant colony." It is not a game to win, and it is not a copy of Earth's timeline.

**Positioning (working label):** "a terrarium you poke" / emergent history sandbox. (Replaces "interactive prehistoric documentary + butterfly-effect sandbox", rev 4.)

**Realism stance:** plausible mechanisms (scarcity, hunting, skill decay, scalar stress, diet breadth), not Earth fidelity. No Earth dates, no Earth climate curve.

**Long-term vision:** from simple bands to a Roman-Empire-like civilization. Later eras plug in as new systems on the same core, not rewrites.

## Scope (v1)
- Arc: simple hunter-gatherer bands to the first farming villages, on one procedurally generated landmass. Time counts from year 0 of the world.
- Version 1 must be worth watching on its own.

## Core loop (v1)
Live nudge and watch. Counterfactual forks are a v1 stretch goal (see Decisions).

## Success test (v1)
"I trigger a drought and can read in the Legends why one band migrated and another died out." Stretch: "...fork the world" before the drought and compare outcomes. v1 passes without the fork.
Use this to judge every "should we add X?" question.

## Decisions
| Area | Decision | Basis |
|---|---|---|
| First spec scope (rev 9) | Success-test slice only: worldgen (heightmap + biomes), climate regime, 2 fields (vegetation, large fauna), bands with food balance and 4 age brackets, migration and die-out, drought nudge, events with causes, templated Legends. Techniques, farming, other fields come in later spec versions | Jordan 2026-10-24 (option A): avoid stacking feedback loops before the core loop is tuned |
| Cloud sessions (rev 10) | Claude Code cloud sessions (mobile Code tab) may write tests and tooling only: hard-rule tests 3/5/6/7, hooks, read-only determinism-reviewer subagent, determinism skill. No sim logic in the cloud until Windows `pnpm check` passes. Repo work starts after the open questions are finished | Jordan 2026-10-28 (option C); Code tab confirmed to see the repo. Linux VM does not verify Windows |
| Information default (rev 10) | Investigate-to-learn: ambient map, glance status word, band card with bars, Legends "why" chains; lab coat toggle (off by default) shows exact numbers and field heatmaps. Every glance word comes from a named threshold in the versioned config, and lab coat shows the number behind it. Slice builds only: glance word, band card (population bars, food trend), Legends "why" chains, lab coat heatmaps for vegetation and large fauna | Brainstorm Q3; Jordan 2026-10-28 (option A) |
| God tools (rev 11) | v1 ships rain/drought (one typed command with a sign, acting on the climate anomaly layer) and bloom (temporary fertility boost on a patch, acting on vegetation). The slice ships drought. A tool ships with its mechanism, never before: spark waits for the fire-age field, herd for named herd entities; later biological/cultural tools follow the same rule | Brainstorm Q4; Jordan 2026-10-28 (option B) |
| Close-up / camp snapshot (rev 11) | No separate diorama view; the diorama is the Close-up zoom. Views read a read-only camp snapshot built from sim state, never sim internals. Slice snapshot fields: food balance and trend, stash level, hunger state, 4 bracket counts, season, last foraging trip outcome. One field per thing a view actually draws. Technique objects (spears, baskets, grindstone) are added to the snapshot only when techniques exist. Snapshot consumers in the slice: Region badge, glance word, band card, Close-up | Brainstorm Q5; Jordan 2026-10-28 (option A + snapshot boundary) |
| Stack | pnpm monorepo, strict TypeScript: `sim-core` (pure TS, no DOM, Vitest), `sim-worker` (thin wrapper), `viewer` (PixiJS v8 + UI + charts, main thread) | Stack report; PixiJS v8.22.0 (1 Oct 2026) verified. Re-check at install |
| Repo | github.com/shadepants/the-living-mythos, default branch `Main-REPO`. TS pinned 6.0.x (typescript-eslint 8.x supports <6.1). `docs/` holds a mirror of the Project docs and research (rev 12); the Project stays the source of truth and the mirror is re-synced after each decision-log revision | Rev 4; mirror added 2026-10-30 at Jordan's request (settles handoff #4 question 2.6) |
| Integer-only config and payloads (rev 12) | Config values and event payloads are integers only; floats never enter the config hash or the log. Fractional tunables (rates, thresholds) are stored as scaled integers (fixed-point) | Float-to-text formatting is not guaranteed identical across engines (hard rule 2 reasoning). Built in `config.ts` and `event-log.ts`, 2026-10-30 |
| Threading | Sim in a plain Web Worker; renderer and UI on the main thread. OffscreenCanvas only if profiling demands it | Verified that Workers lose DOM interaction; the arrangement is inference |
| Data layout | Structure-of-arrays typed arrays; bitECS only if needed. Zero allocation in hot loops | Judgment; batch review (Songs of Syx, Victoria 3) |
| Granularity | Group-level (bands/villages); notable individuals as history records (name, lineage, traits, deeds), not simulated minds | Victoria 3, Artificial Anasazi; Songs of the Eons stalled on per-person granularity |
| Group model | Band is the first form of a general "group" that can later become village, chiefdom, state | Keeps later eras additive |
| Band state (Q1) | Lineage ID + name, home range (cells), population by age bracket, food balance, known techniques, relations, notable member refs | Grilling Q1 |
| Age brackets (Q1) | 4: children (consume, vulnerable), young adults (mobile: marriage exchange, founding bands, migration), adults (main producers), elders (keep techniques alive) | Grilling Q1 |
| Catchment | Bands forage a 3–5 cell catchment radius around camp/village | Novelty review addition (b); report 3 catchment 5-12 km |
| Cell size | Working assumption ~3 km per cell (catchment 3 cells ≈ 9 km). 256×256 ≈ 770 km square ≈ 350-2,800 bands at forager densities | Rev 4; report 3 + computed |
| Techniques (Q2, refined rev 4) | Integer level (0-3) plus a progress accumulator. Grows with use; decays as a forgetting time τ (years) driven by intervals between uses; elders lengthen τ | Grilling Q2; EMBERS (verified: τ 1-16 yr, use variability dominates). Report 3's 0.03/0.08 decay defaults rejected as unsupported |
| Technique origin (Q3) | Invention (need, opportunity, population) + contact (relations, proximity) + shallow prerequisites (max 1–2, physical necessity only). Geography/opportunity dominates; invention rare, contact common. No scripted tech tree; stagnation and collapse allowed. Emergence uses bias weights, never hard threshold gates | Grilling Q3; batch review |
| Farming emergence | Farming favoured in ecological "crucibles" (circumscribed river valleys under climate/density stress) as a tunable bias, not a hard gate. Diet breadth drives it: grain enters the diet when large-game returns fall | Novelty review (d); report 3 |
| Demography | Report 3 ranges are sane defaults (band 15-50, l15 ≈ 0.57, TFR 4.5-6, IBI ~3.5 yr), not its equations (inconsistent). Births/deaths via per-member hash draws (bands ≤ ~50; no exp/log) | Batch review section 2; hard rules 1-2 |
| Balance and tuning targets | Balance lives in data; tune via headless batch runs over many seeds. Targets are eventfulness (notable events per century) and variety of outcomes across seeds, not matching Earth. Choosing lively world settings is fine; a drama director is not | Rev 4 |
| Time (Q4) | Seasonal ticks always. Run-ahead history buffer: worker simulates ahead, viewer plays back, pacing driven by the event log (fast through quiet stretches). Fixed multi-rate schedule for slow systems | Grilling Q4; timescale report |
| No state-adaptive compression | No quiescence skipping, ABM/ODE switching or projective integration in v1. Playback pacing is fine | Keeps replay exact (timescale report) |
| Environment fields (rev 4) | Vegetation, soil, large fauna, small fauna, water, fire age (fire risk derived from fire age + vegetation), crop domestication. Elevation static. Two-way coupling with people. Fields computed on CPU in sim-core | Report 3 (diet breadth, fire mosaic); GPU fields rejected for determinism |
| Large fauna (rev 22) | Herd-condition model per cell. Intake per animal Type II `gMax·V/(V+halfSat)`; total removal capped at `maxGrazeFraction·V` per substep. Condition (0-1) moves toward intake satisfaction at `condRate`. Births `rMax·max(0,(c−cBreed)/(1−cBreed))·F`, `rMax` 0.04-0.06 per season. Deaths `(mBase + mDens·F + starvation below cStarve)·F`; `mDens` (stand-in for predators, disease, crowding) is required. Capacity emerges from food (replaces `cF·V`). Diffusion scales up as condition falls; substep count fixed from the maximum possible rate (hard rule 4). Hunting: Type II on F with a capped take (yield side: resource guilds, rev 23). Targets [P]: crash 25-75% under severe drought, deaths start 1-3 seasons after onset, recovery to 90% in 30-50 seasons [UNCERTAIN] | Jordan 2026-10-30 (spec Q7, option C + mDens). Verified: paradox of enrichment (Rosenzweig 1971) reproduced in a throwaway prototype, removed by mDens ≥ 0.05; rMax by allometry (wildebeest 0.248/yr, buffalo 0.208, eland 0.150); 2D explicit diffusion stable at h·D ≤ 1/4 (numerical). Prototype: 576 settings, none stable with ≥25% crash recovered in under 30 seasons, so the report's 12-28 seasons was relaxed. Check: no-drought stability over richness 1-8; half-strip drought scenario (lag, herds drift out); 20 seeds × 200 yr, no boom-bust, no map-wide extinction |
| Resource guilds (rev 23) | Food comes from guilds behind one interface: per-cell stock in food units (1 = one adult's needs for a season), capacity from fields, a per-guild regrowth rule (continuous, herd model, or pulsed), a per-worker Type II return a·S/(1 + a·h·S), a per-season take cap as a fraction of stock, and a seasonal factor. Energy is the only currency in the slice; a protein/fat budget comes with farming. Slice guilds: large game (rev 22 herds × food per herd) and plant foods (capacity tied to V). V stays herbivore forage and is never eaten by people directly. Labour goes by rank, each guild capped, until need plus stash top-up is met. One pooled stash with spoilage proportional to its size; stash size is a world setting until a temperature or seasonality field exists. Diet shifts are snapshot state, not events. Starting values [P]: hunt cap ≈ 1% of stock per season, stash ≤ 0.5 seasons of consumption, spoilage 0.15-0.25 per season | Jordan 2026-10-31 (whole-system review R1, option B). Basis: Q8 prototypes (`research/prototypes/q8-system/`): a fixed hunt/gather split went chronically hungry on depleted game; a hunt cap of 1.5%/season collapsed game with no drought, 1% held. Prompt 11: VEP, Alroy and OFT models hunted game to extinction once people were fed by other food; Artificial Anasazi's 2-year storage expiry caused cliffs (verified, Janssen 2009). Prompt 9 spoilage ranges. Hunt cap ≈ 4%/yr sits inside the reported 2.5-5.5%/yr sustainable band [UNCERTAIN] (prompt 10). Behavioural prey depression tested, no clear effect; moved to R2. Check: no-drought run over 20 seeds keeps herds above zero in every cell |
| Vegetation response (rev 21) | Below K: logistic growth at `rV`. Above K: V' = K + (V − K)·(1 − `dieBack`), never below K (no instant clamp, no drought flag in field code). `rV` and `dieBack` are piecewise-linear over base moisture; starting [P] endpoints: dry `dieBack` 0.40-0.60, `rV` 0.60-0.80; wet `dieBack` 0.10-0.20, `rV` 0.10-0.25. Targets [P], severe drought: dry cells drop 45-70% in 1-2 seasons and recover to 90% in 0.5-1.2× drought length; wet cells drop 25-45% over 2-5 seasons and recover in 1.5-2.5×. Grass recovers about as fast as the drought, so a lasting post-drought shortage must come from game (Q7). [Rev 23: the Q8 prototypes did not bear this out: plant foods backfilled and bands barely felt the herd lag. Outcomes depend on band size, migration scoring, hunger mortality and refuge occupancy; see the integration review] Permanent-loss tipping points wait for soil/fire fields | Jordan 2026-10-30 (spec Q6, option B2). Basis: prompt 7 review (`research/vegetation-drought-review-2026-10-30.md`), shape only; numbers unverified. Check: single-cell drought test at three moisture levels against the targets |
| Climate regime shape (rev 19) | anomaly = clamp(seasonal[season mod 4] + volatility · spaceTimeNoise(x, y, season)) − active droughts (clamp revised rev 20). Noise lattice every `climateLatticeCells` cells and `climateLatticeSeasons` seasons, interpolated in space and time; clamped to ±`anomalyClamp` (severity dial). Regions = climate-lattice blocks. Dry spells use hysteresis: enter below `dryThreshold` for `dryMinSeasons`, exit above `dryThreshold + dryExitGap`. Events carry the region index, primary `ROOT_ID`; a band cites the region of its camp cell. Target: ~15% of seasons in a dry spell per region, tuned within 12-18% (lower if too much, higher if too little). volatility 0 gives a nudge-only climate (usable for the test scenario) | Jordan 2026-10-30 (spec Q4, option B; target set by Jordan). The v0.4 formula's global temporal noise made every natural dry spell world-wide. Check: 20 seeds × 200 yr with no nudges, dry share in 12-18%; property test: no spell shorter than `dryMinSeasons` |
| Climate | World-seeded climate: deterministic generated regime (temperature/moisture anomaly per season) with world dials (volatility, severity). Stored/derived from config + seed. Not a climate simulation and not Earth's curve. Drought nudges layer on top | Rev 4 |
| Variable discipline | Every field and band attribute must feed a threshold the Legends can report; no unobservable trivia | Novelty review addition (e), lesson from Hennepin |
| World | Procedural, square grid. v1 worldgen = noise heightmap + biome lookup; rivers deferred | Scope control |
| Worldgen and capacity (rev 18) | Heightmap and base moisture from hash-keyed gradient noise (fixed integer gradient table, quintic fade, 4 octaves); radial edge falloff; sea level at the 35% height quantile; only the largest connected land area is kept (slice only: islands come back when sea travel exists, as a world setting). Vegetation capacity is continuous: a piecewise-linear curve over base moisture times a height penalty. A 4×3 height × moisture table names ~8 biomes + ocean for palette and Legends wording only. Biomes are fixed at worldgen; droughts change capacity through the moisture anomaly, not the biome | Jordan 2026-10-30 (spec Q3, option C + both defaults). Per-biome capacities (option A) rejected: ~16 untuned values and step changes at borders. Gradient noise needs no trig. Check: 20 seeds at 128, no biome <3% or >50% of land, one landmass, ≥5 seeds pass the rev 16 refuge check |
| Event emission | Emit history events only when a regime threshold is crossed; each event records at most 3 enabling causes | Novelty review addition (a); counters "diffuse causality" (James Ryan) |
| Event emission model (rev 17) | Systems write per-season transition records (e.g. moved A→B, hunger none→hungry, command applied) and never append events directly. One emitter pass at the end of the season turns records into events in fixed order (band ID order, then record order) and attaches causes. New systems add record types, not logging code. World/region events use `ROOT_ID` as primary, with cell and radius in the payload; same-tick collisions use the ordinal. Synthetic IDs (command/region `EntityId`s) may replace `ROOT_ID` when forks are worked on; that changes content keys, so decide before saves exist | Jordan 2026-10-30 (spec Q2, option C + P1). A pure state-diff detector rejected: it must infer discrete actions from diffs and can order causes wrongly. Check: property test over random seeds and command logs: causes precede events, band outcomes reach a root in ≤3 hops, emission order identical across runs |
| Event identity | Each event has a content key (type, tick, primary lineage ID, ordinal), written `type:tick:primary:ordinal`. The ordinal counts earlier events with the same type, tick and primary in that run; almost always 0. Sequential IDs are local to a run. Narration seeding (and any future fork matching) uses the content key | Batch review (reports 4-5); ordinal added rev 12 (Claude Code proposal, 2026-10-30); confirmed by Jordan rev 17 |
| RNG entity key (rev 13) | `RngKey` gains a required `entityHi` (uint32): `entity` holds the low 32 bits of the 64-bit `EntityId`, `entityHi` the high 32 bits. Non-lineage keys (e.g. grid cells) set `entityHi` to 0 and must not share a `Purpose` code with lineage entities. Changes the RNG golden values once, before any saves exist | Jordan 2026-10-30 (option A). Option B (hash 64 bits into the 32-bit field) rejected: same collision rate |
| Map size and catchment (rev 16) | World size is a setting (`worldWidth`, `worldHeight`); slice default 128×128 (~385 km), v1 working size stays 256×256; property tests may use 32×32. Catchment is a Euclidean disc, dx² + dy² ≤ r², r = 3 (29 cells, ≤ 9 km), from a precomputed offset list in fixed order; off-map and sea cells are excluded | Jordan 2026-10-30 (spec Q1). Report 3 catchment 5-12 km; a radius-3 square overstates the area by ~1.7×. Check: 20 seeds at 128, need ≥5 with a drought region and a refuge within migration search range |
| Number representation (rev 15) | Sim state holds IEEE 754 doubles (`Float64Array` and numbers) using only `+ − × ÷` and `Math.sqrt`. The state hash rejects NaN and ±Infinity and normalizes -0 to 0. Sums over cells or bands run in a fixed order (row-major, band ID order); no parallel reductions. Config stays scaled integers converted once at load; event payloads are rounded to integers at emission | Jordan 2026-10-30 (spec Q0, option A). Basic IEEE 754 operations are exact across engines; fixed-point would double formula code and risk small terms rounding to zero. Check: cross-engine state-hash test (benchmark step 5) once a field runs |
| Primary PBT skill (rev 14) | fast-check `javascript-testing-expert`, pinned to commit `fd17f486fc`, with fast-check 4.10.2 and @fast-check/vitest 0.5.0; Trail of Bits not installed (two PBT skills give conflicting advice) | Jordan 2026-10-30, by running Prompt A (`claude/next-steps-prompts.md`); installed and vetted on the laptop |
| Drought command (rev 20) | One signed command (rev 11): `sign`, `magnitude`, `durationSeasons`, `centerCell`, `radius`. Area: full magnitude within radius/2, linear fade to 0 at radius (Euclidean, `sqrt`); radius 0 = whole map. Magnitude in anomaly units with two config presets (mild, severe); default 8 seasons; instant onset. The natural anomaly is clamped to ±`anomalyClamp` first; active commands are subtracted after and add up; `minMoistureFactor` bounds the effect. `drought_began` cites the command. A whole-map drought leaves no refuge, so the test scenario uses a local one | Jordan 2026-10-30 (spec Q5, option B, defaults [P]). Check: unit test of the fade profile (full at ≤ r/2, half at 0.75r, 0 at ≥ r); property test: a drought never raises moisture |
| Event causes (rev 12) | A cause is either an earlier event or a nudge command, max 3. Event causes are checked against the log; command causes are only shape-checked until the command log exists (hard rule 6) | Claude Code proposal, 2026-10-30; confirmed by Jordan rev 20 (Q5). Nudges were already "logged with cause IDs" |
| Salience | Computed in the narration layer; never decides what the sim logs | Batch review: resolves report 2 vs event emission |
| Narration pipeline | Event collections (DF-style) → incremental sifting patterns (Winnow-style ideas, own implementation) → salience + quiet-epoch compression → first_valid conditional templates + seeded lexical grammar. LLM later, closed-world packets only | Report 4 |
| Nudges | Typed commands applied at tick boundaries, logged with cause IDs. Environmental first, then biological, then cultural | Stack report (Azgaar "controlled mutations"); visibility of effects |
| Lore (beliefs with mechanical effects) | Deferred until the food web and demography are stable and tuned. v1 stays compatible: events keep causes, bands have room for traits, but no belief system ships in v1 | Brainstorm Q1, 2026-10-24: Jordan chose B (avoid stacking feedback loops on an untuned ecology) |
| Counterfactual forks | v1 stretch goal, not a pass condition. Determinism rules keep it reachable; no fork-comparison UI is required for v1 | Jordan 2026-10-24 (option C); replaces rev 4 "deferred, no commitment" |
| Pacing | Session-length runs at top speed, with pause, fast-forward and scrub | Judgment |
| Visual style | Pixel art: terrain stored as palette indices, seasons as palette swaps, ordered dither only for gradients, stipple for vegetation, orphan-pixel cleanup, terraces with 1-step light/shade. Sprite tokens, nearest-neighbour scaling, no mixed pixel scales. Resembling WorldBox is acceptable | Look tests v1-v3 (2026-10-24); research/pixel-art-review-2026-10-24.md |
| Palette | Endesga 32 as the master palette (easier to tell apart than the muted Earth set). Autumn: only forest groves turn; grass stays green | Look test v3, Jordan 2026-10-24 |
| Winter | Snowline: snow above a line that creeps down over the winter and melts through spring; cold palette below; frozen shallows | Look test v3, Jordan 2026-10-24 |
| Band markers by zoom | World: small lineage-colour diamonds with crowd culling. Region: lineage badge (founding colour + own colour, inherited symbol, size dots), confirmed readable. Close-up: hut, fire and a tight crowd; foragers and hunters walk out in parties, work, and return carrying food or a kill (empty-handed when the band is hungry); a stash by the hut grows and shrinks with real food; a returning load thickens the cooking smoke; most people huddle by the fire in winter. All of it reads the camp snapshot (rev 11), never fed back; figures per camp capped, motion scripted from snapshot state. Whether it gives the ant-farm feel is pending Jordan's rewatch | Look test v3 (Jordan 2026-10-24); v5 close-up changes from Jordan's approval of the lever table |
| Colour-blind accessibility | Not a v1 requirement. The colour-check tooling stays available for later | Jordan 2026-10-24 |
| Screen | Map with switchable layers (vegetation, fauna, territory) + Legends panel | Judgment; refined by brainstorm |

## Hard rules (write tests before sim code)
1. **Hash-based randomness** keyed on (seed, absolute season index, entity, purpose), never a shared sequential stream. Test: replaying the same seed and nudge log produces an identical world (state hash). Implemented: `sim-core/src/rng.ts`.
2. **No platform-dependent math in sim-core.** Lint-ban Math.random, trig/exp/pow/log, `**`, Date, performance.now; use own implementations. Math.sqrt and basic arithmetic are fine (IEEE 754). Verified: ECMAScript lets the others vary by implementation. Implemented: `eslint.config.js`.
3. **Stable lineage-derived IDs** (parent, birth tick, sibling index), so entities stay identifiable across replays, saves and any future forks. Implemented: `sim-core/src/lineage.ts` (64-bit IDs as 16 hex chars, branded `EntityId`). The ID does not encode the parent: the future entity registry must store it and assert uniqueness on registration (not built yet).
4. **Fixed internal substeps for environment fields; schedules never depend on state.**
5. **Causal event log from day one.** Every event records its parent-cause IDs (max 3). Implemented: `sim-core/src/event-log.ts` (append-only, ticks non-decreasing, no event taxonomy yet).
6. **Snapshots are keyframes + command log + replay.** Scrubbing backward is a real system with memory cost, not free.
7. **All tunables in a versioned config;** saves record the config hash. Implemented: `sim-core/src/config.ts` (`hashConfig`, golden-value test). Fields are placeholders (`seasonsPerYear`, `startingBandSize`) until the slice spec names the real tunables.

Implementation status (2026-10-30, laptop, not yet pushed): rules 1, 2, 3, 5, 7 built with tests; 43 tests pass on Windows. Rules 4 and 6 wait for the tick loop and command log.

## Rejected
- Godot 4 / Unity DOTS / Bevy (hardware, language, iteration; Godot C# can't export to web)
- PixiJS in an OffscreenCanvas Worker from the start
- Variable tick length per era
- Rome as v1 target (long-term only)
- Earth's timeline, Earth dates and Earth's climate curve as targets (rev 4)
- Single head count or full age pyramid (use 4 brackets); technique flags (use skill levels)
- Deep tech-prerequisite trees; hard-gated technique emergence thresholds (report 3)
- State-adaptive time compression in v1
- Tuning the simulation itself for drama; a drama director inside the sim (RimWorld storyteller). Presentation-side nudge suggestions are fine
- Salience-gated logging
- GPU-computed simulation fields (driver-dependent floats)
- LLM-driven population agents (cost; not deterministic). LLM may only narrate logged events, later
- Voronoi mesh (dual-mesh), compromise NLP, Trrack, gitgraph.js (archived)
- Reusing Winnow code (no license); Viv as a dependency (source-available, non-commercial)
- Unity skills, spritecook, magicweave, playdrop, third-party Vitest skills
- Numbers visible by default; shipping v1 with no raw-number view (rev 10)
- God tools shipping before their mechanism (spark, herd in the slice) (rev 11)
- A separate camp diorama view in v1; no Close-up figures in the slice (rev 11)
- Views reading sim internals directly (rev 11)
- Hard-coded food channels special-cased in forage, migration and events; people eating vegetation V directly (rev 23)

## Known risks
- Hunt cap deciding outcomes (rev 23): the per-season take cap is a balancing knob; keep it inside the sustainable-offtake band and watch whether outcomes swing on it in batch runs.
- Game extinction once other food feeds people (prompt 11; VEP, Alroy): the take cap guards the slice; farming needs the protein/fat budget or prey depression.
- Fauna boom-bust (rev 22): Type II grazing cycles on rich land without density mortality (prototype-verified); keep the no-drought stability test in the suite.
- Feedback loops that collapse or explode under tuning: invariant tests (no negative biomass, population bounded by carrying capacity).
- Teleology: progress rules that quietly force development. Crucible bias must stay a bias.
- Bimodal tech outcomes: no band ever farms, or all farm at once. Tune with batch runs.
- Arbitrariness: with no Earth anchor, rules can drift toward dice rolls. Keep mechanisms plausible; every event needs recorded causes.
- Legends readability over thousands of years: templated narration and summarization.
- Frontier stall: sim throughput falling below playback in dense eras.
- Search/pathfinding cost (Ultima Online lesson): spatial hashing, budgeted per-tick work.
- Silent cross-browser divergence: CI state-hash check on two engines.
- Log and keyframe memory blow-up: keyframe sparsely; regime-threshold emission keeps the log small.
- World generation growing into its own project.
- Third-party skill/plugin supply-chain risk (tooling report): vet before install; prefer own determinism skill/hooks.
- Glance words drifting from state (rev 10): mistuned thresholds make the glance layer lie. Mitigation: named config thresholds, lab coat shows the number.
- Lab coat becoming the real UI while tuning, so glance/inspect/Legends layers get neglected (rev 10).
- Camp snapshot growing into a second copy of sim state (rev 11). Rule: one field per thing a view draws.
- Close-up turning into a crowd sim (rev 11): cap figures, script motion from snapshot state.
- Look-test artifact code ported into the viewer (rev 11): it is a visual reference only; likely uses Math.random (unverified). Rewrite, don't port.
- [UNCERTAIN] Novelty-report claims: Euca Engine not found (do not rely); ActiveGraph exists but report's framing uncertain; "LogicTale" mismatches its cited source; sales figures are third-party estimates.
- Hardware benchmark: the laptop is back (linked 2026-10-30); not run yet. Needs a tick loop and fields to measure.
- RNG entity-key collisions (rev 12, decided rev 13): `entityKey()` truncated the 64-bit entity ID to 32 bits, about a 4.5% chance of at least one colliding pair at 20,000 entities (birthday bound, computed, not tested); colliding entities would share every draw. Fix decided rev 13 (see Decisions); open until the laptop commit lands. Hashing 64 bits into one 32-bit field was rejected: any 32-bit field collides at the same rate.

## Open questions (to grill)
- Whole-system review (`design/integration-review-2026-10-30.md`), in order: R2 home range + seasonal camp (prey depression belongs here), R3 band lifecycle (fission, dissolution), R4 calibration anchors; then spec Q9-Q14.
- Cloud-session gate (rev 10): Windows `pnpm check` passed on 2026-10-30 (laptop, Node 25.3.0). Does the gate lift as written, stay (sim logic only on the laptop), or lift with a Windows check required before each sim merge? Lean: the last option.
- Brainstorm questions: all closed (Q1 lore deferred; Q2 pixel; Q3 rev 10; Q4, Q5 rev 11). Brainstorm archived at `archive/design/depth-and-visuals-brainstorm.md`.
- Close-up view: does look test v5 (trips, stash, cooking smoke, tighter crowd) give the ant-farm feel? Jordan to rewatch. Known weak spot: a camp whose lineage colour is pale on sand is hard to see.
- Property norm (Bowles & Choi) as a band attribute: defer until batch runs show farming needs it (lean).
- Tooling adoption, remaining: which other tooling-report items to install (PixiJS skills wait for the viewer). PBT skill settled rev 14; cloud sessions rev 10.
- Pixel-art review items not yet decided (outline rule, fire scars, trails, BitmapText/HTML Legends, ParticleContainer, debug keys, Kenney glyphs): settle during the spec, slice-relevant items only.

## Research
- Done: forager reports (prompts 8-11, reviewed 2026-10-31, `research/forager-reports-review-2026-10-31.md`; R1 adopted rev 23); vegetation drought report (prompt 7, reviewed 2026-10-30; shape adopted rev 21); novelty report (prompt 1); Gemini reports 2-5 + repos report (batch-reviewed 2026-10-23, review archived); pixel-art report (prompt 6, reviewed 2026-10-24); stack and prior-projects report (13 projects); timescale report; tooling report (cloud-sessions item decided rev 10; rest under review). All prompts in `research/gemini-prompts.md`; none pending.
- Shelved: fork-comparison ideas (prompt 5) until forks are worked on as the stretch goal.

## Benchmark order (laptop is back; run once the tick loop and fields exist)
1. Field cost per season (256×256 and 512×512, 7 fields, real substeps; warm and after 5 minutes sustained).
2. Group cost at 1,000 / 5,000 / 20,000 groups.
3. Run-ahead ratio by era.
4. Snapshot and replay cost.
5. Cross-browser state-hash check.
6. Only then WASM or multi-worker on the hottest kernel.

## Tooling noted (not yet adopted)
- Official PixiJS skill pack (25 skills: 24 topic + `pixijs` router): in Claude Code, `/plugin marketplace add pixijs/pixijs-skills`.
- Context7 connector for live library docs (covers bitECS).
- Skills in use: spec-developer, grill, engineering:testing-strategy, algorithmic-art (worldgen prototyping on phone), active-memory:amhandoff.
