---
Title: Living mythos: success-test slice
Type: Tech Spec
Version: 0.3
Status: Draft (Phase 2; open questions being grilled in order, section 20)
Owner: Jordan
Created: 2026-10-30
Last Updated: 2026-10-30
Approvers: Jordan
---

# Living mythos: success-test slice (spec v0.3 draft)

## Executive summary
This spec defines the smallest simulation that passes the v1 success test: "I trigger a drought and can read in the Legends why one band migrated and another died out." It covers worldgen (heightmap + biomes), a seeded climate regime, two fields (vegetation, large fauna), bands with food balance and 4 age brackets, migration and die-out, the drought nudge, caused events and templated Legends (decision log rev 9). Every tunable is tagged with its source. Nothing here overrides `design/decision-log.md`; where they disagree, the log wins and this spec gets a `[CONFLICT]` tag.

Tag key: **[R: source]** research-backed range · **[P]** placeholder, set by batch tuning · **[NEED: Jordan]** design choice · **[UNCERTAIN]** unverified · **[CONFLICT]** disagrees with the log.

Code facts below were checked against the repo on 2026-10-30 (tick loop built, 67 tests + 1 todo). A rough alternative draft written by a Gemini agent is archived at `archive/design/spec-rough-draft-gemini-2026-10-30.md`; it is input to the grilling, not a decision.

## 1. Goals / non-goals
**Goals**
- G1. A seeded world where bands forage, go hungry, migrate or die out for traceable reasons.
- G2. A drought command that can be applied at a tick boundary and logged with a cause ID.
- G3. A Legends "why" chain from `band_migrated` / `band_died_out` back to the drought in at most 3 hops.
- G4. Same seed + same command log → identical state hash on Windows/Chrome and Linux/Node.

**Non-goals (later spec versions)**
Techniques, farming, soil, small fauna, water, fire age, crop domestication, band fission/fusion, relations, notable individuals, lore, bloom, forks and fork UI, viewer polish beyond the slice's consumers (glance word, band card, Legends why chains, lab-coat heatmaps for the 2 fields).

## 2. Constraints (from the log and code)
- Hard rules 1-7. Built: 1 (`rng.ts`), 2 (`eslint.config.js`), 3 (`lineage.ts`), 4 (`tick.ts`), 5 (`event-log.ts`), 7 (`config.ts`). Not built: 6 (command log, keyframes), entity registry.
- RNG key `(seed, season, entity, entityHi, purpose)`, all uint32. Purposes 1-5 exist (ForageYield, Migration, Birth, Death, Invention); new codes are appended. Cell-keyed draws use the cell index in `entity`, `entityHi = 0`, and purposes no lineage entity uses (rev 13).
- Banned in sim-core: Math.random, trig, exp/log, pow, cbrt, hypot, `**`, Date, performance.now. Allowed: `+ − × ÷`, Math.sqrt, integer bit ops.
- `SimConfig` is flat safe integers; fractional tunables are scaled integers (rev 12). Real tunables replace the placeholders and change the config-hash golden value once (no saves exist).
- Events: snake_case type; `tick` = absolute season; ≤3 causes (event or command); flat integer payload; content key `type:tick:primary:ordinal`; `primary` is an `EntityId`.
- Tick loop: one tick = one season; systems in fixed array order with `period`, `offset`, `substeps` (1-1024); schedule never depends on state.

## 3. Number representation (decided rev 15: option A)
| Option | What it means | Cost | Risk |
|---|---|---|---|
| A. Doubles in state, basic ops only (lean) | Field and band state in `Float64Array`/numbers; config scaled integers divided once at load; payloads rounded to integers at emission | Least code; normal formulas | NaN/±0 must be guarded before state hashing; operation order must stay fixed (no parallel reductions) |
| B. Fixed-point integers everywhere | Every quantity a scaled integer with a stated scale, rounding rule and max intermediate < 2^53 | Every formula needs scale bookkeeping; small growth terms can round to 0 | Silent stalls from rounding; harder to read and tune |

Known: ECMAScript Number arithmetic is IEEE 754 double with round-to-nearest, and engines may not fuse operations, so `+ − × ÷` and `sqrt` give the same results everywhere. Inferred: Float32Array storage is also deterministic (rounding to float32 is specified), but it adds a second precision to reason about, so the lean is Float64Array. External check: the cross-engine state-hash test (benchmark step 5), run once the tick loop drives fields.

Decided (Jordan 2026-10-30, rev 15): option A. Rules: the state hash rejects NaN and ±Infinity and normalizes -0; sums over cells or bands run in a fixed order (row-major, band ID order); config scaled integers are divided once at load; event payloads are rounded to integers at emission. Formulas below are plain arithmetic.

## 4. World
| Item | Value | Tag |
|---|---|---|
| Map size | Setting (`worldWidth`, `worldHeight`); slice default 128×128 (~385 km); v1 working size 256×256; property tests may use 32×32 | Decided rev 16 (Q1) |
| Cell size | ~3 km (presentation only; the sim uses cells) | [R: log] |
| Seasons per year | 4 | [R: log, seasonal ticks] |

### 4.1 Worldgen (once, at season 0)
- Heightmap: hash-based value noise (lattice values from `hashKey` with a new purpose `WorldgenHeight`, cell index in `entity`), smoothstep interpolation `t·t·(3−2t)`, `octaves` summed with halving amplitude. No trig, so Perlin/simplex gradients are out.
- Moisture base: same method, purpose `WorldgenMoisture`.
- Sea level: the height value at the `seaLevelPercent` quantile (sorted; ties broken by cell index), so the land fraction is exact per seed.
- Biome = lookup table over (height band × moisture band). Each biome carries a vegetation carrying capacity `Kveg[biome]` and a fauna capacity factor.

| Tunable | Value | Tag |
|---|---|---|
| `octaves` | 4 | [P] |
| `seaLevelPercent` | 35 | [P] |
| Biome table | 4 height bands × 3 moisture bands → ~8 biomes | [NEED: Jordan] (question 12); later look tests already use Endesga ramps |
| `Kveg[biome]` | relative 0-1 per biome | [P] |

## 5. Systems and run order
All systems run every season in the slice (period 1, offset 0). Slow-system periods come with later fields.

| # | System | Substeps | Reads | Writes |
|---|---|---|---|---|
| 1 | apply_commands | 1 | command log | active nudges |
| 2 | climate | 1 | seed, dials, active nudges | per-cell moisture anomaly |
| 3 | vegetation | 1 | anomaly, biome, grazing, harvest | vegetation |
| 4 | large_fauna | n_f (from stability limit) | vegetation, hunting | fauna |
| 5 | forage | 1 | catchment fields, labour | band yield, stash, food balance |
| 6 | demography | 1 | food state, brackets | brackets (births, deaths, aging) |
| 7 | migration | 1 | hunger history, catchment scores | band camp cell |
| 8 | emit_events | 1 | this season's transition records, event log | events |
| 9 | snapshot | 1 | sim state | camp snapshot (read-only copy) |

Decided (Jordan 2026-10-30, rev 17: option C). Systems 1-7 never append events. Each writes transition records to a per-season buffer (e.g. `command_applied`, `dry_spell_crossed`, `balance_turned_negative`, `hunger_changed`, `moved {from, to}`, `population_zero`). Each record carries its subject (band `EntityId` or `ROOT_ID`) and the facts the emitter needs to pick causes. `emit_events` (#8) sorts records by subject (`ROOT_ID` first, then band ID order), keeps record order within a subject, turns each into an event, and attaches causes by looking up earlier events in the log. The buffer is cleared after emission and is not part of saved state. A new system adds record types and emitter rules; existing systems don't change.

## 6. Climate regime
Per season, per cell: `anomaly = seasonal[season mod 4] + volatility · temporalNoise(season) + regional(cell) − droughtMagnitude(cell, season)`.
- `seasonal[4]`: a 4-entry lookup table, so no trig is needed.
- `temporalNoise`: 1D value noise over the season index (lattice every `climateLatticeSeasons`), purpose `ClimateTemporal`; smoothstep between lattice points.
- `regional`: coarse 2D value noise, fixed per world, purpose `ClimateRegional`.
- `severity` dial: scales the tails (anomaly is clamped to ±`anomalyClamp`).
- A natural dry spell starts when the regional mean anomaly stays below `dryThreshold` for `dryMinSeasons`; it emits `dry_spell_began` / `dry_spell_ended` (primary `ROOT_ID`).

| Tunable | Tag |
|---|---|
| `seasonal[4]`, `volatility`, `severity`, `climateLatticeSeasons`, `anomalyClamp`, `dryThreshold`, `dryMinSeasons` | [P] all; dials exposed as world settings (log "Climate" row) |

## 7. Vegetation
`V' = V + rV · V · (1 − V / K) − grazing − harvest`, with `K = Kveg[biome] · moistureFactor(anomaly)`, clamped to `[0, K]`.
- `moistureFactor`: piecewise-linear from anomaly (lookup with linear interpolation), floor `minMoistureFactor` so ground cover never vanishes entirely.
- A seed term `vegSeed` added when V is 0 so a cell can recover.

| Tunable | Tag |
|---|---|
| `rV`, `moistureFactor` breakpoints, `minMoistureFactor`, `vegSeed` | [P]; no research basis for a procedural world; tuned so a 4-8 season drought visibly drops vegetation and recovery takes longer than the drought [UNCERTAIN: target shape is Jordan's call] |

## 8. Large fauna
Per substep, with `h = 1 / n_f` (fraction of a season):
`F' = F + h · (growth(F, KF) − hunting) + h · D · Laplacian(F)`, then clamp `F ≥ 0`.
- `KF = cF · V` (fauna carrying capacity of the cell).
- `growth = rF · F · (1 − F / KF)` when `KF > epsK`; otherwise `growth = −mF · F` (the herd starves off a barren or ocean cell). This removes the divide-by-zero when `V = 0` or `cF = 0`. (Bug fixed in v0.2.)
- Every rate is scaled by `h`, so `n_f` substeps add up to exactly one season of growth, hunting and diffusion. (Bug fixed in v0.2: v0.1 scaled hunting only.)
- Laplacian: 4-neighbour; a sea neighbour contributes the cell's own value (zero-flux boundary), so fauna never diffuses into the sea.
- Stability (explicit diffusion, 2D): `h · D ≤ 1/4`, so `n_f = max(1, ceil(4 · D))` [R: standard FTCS stability limit].
- Grazing removes vegetation in proportion to F (`grazeRate`).
- Iteration order: row-major with a double buffer, so update order can't change results.

| Tunable | Tag |
|---|---|
| `rF`, `cF`, `D`, `grazeRate`, `mF`, `epsK` | [P]. Report 3's overkill/regeneration ranges are a starting band, not values [R: report 3 ranges, equations rejected] |

## 9. Bands and food balance
Band state (log Q1, slice subset): `EntityId`, name, camp cell, 4 bracket counts, stash, food balance history (last 4 seasons), hunger seasons counter, alive flag.

| Bracket | Span | Tag |
|---|---|---|
| children | 0-14 yr (0-59 seasons) | [P]; report 3 l15 ≈ 0.57 implies the 15-year cut [R: report 3] |
| young adults | 15-24 yr | [NEED: Jordan] (cut points) |
| adults | 25-49 yr | [NEED: Jordan] |
| elders | 50+ yr | [NEED: Jordan] |

Forage per season:
- Catchment = Euclidean disc around the camp, dx² + dy² ≤ `catchment`² (29 cells at r = 3), from a precomputed offset list sorted by (dy, dx); off-map and sea cells excluded (decided rev 16).
- Labour `L = adults + 0.5·youngAdults` (weights [P]).
- Yield = `L · (gatherEff · ΣV_share + huntEff · ΣF_share) · yieldNoise`, where `yieldNoise` comes from `rand01` with purpose `ForageYield`, entity = band. Harvest and hunting are subtracted from the cells the band forages, split evenly across the catchment ([P]; a nearest-first split is the alternative).
- Consumption = `Σ bracket · need[bracket]`.
- Stash: `stash = min(stashCap · population, (stash + yield − consumption) · (1 − spoilage))`, floored at 0.
- Food balance = yield − consumption. Food trend = mean of the last 4 balances, as a sign word: rising / flat / falling (band `flatBand` [P]).
- Hunger state: `hungry` when stash is 0 and balance < 0; `starving` after `starvingSeasons` consecutive hungry seasons.

| Tunable | Tag |
|---|---|
| `catchment` | 3 cells, Euclidean (rev 16) [R: log 3-5 cells; report 3 catchment 5-12 km at ~3 km/cell] |
| Starting band size | 25 (range 15-50) [R: report 3] |
| `gatherEff`, `huntEff`, `need[4]`, `stashCap`, `spoilage`, `starvingSeasons`, `flatBand` | [P] |

## 10. Demography (per season, per band)
**[CONFLICT]** The log's Demography row says "births/deaths via per-member hash draws". The key has no member index (`rng.ts`), so per-member draws need either a new key field or a different method. Proposal (only valid under number option A): one draw per bracket and outcome, sampling the exact binomial `Bin(n, q)` by inverse CDF with one uniform `u`:
  - `q ≤ 0` → 0 events; `q ≥ 1` → n events (no division).
  - If `q > 0.5`, sample `X' ~ Bin(n, 1−q)` with the same `u` and return `n − X'`. The recurrence below then always has `1 − q ≥ 0.5` in its denominator. (Bug fixed in v0.2: v0.1 divided by zero at `q = 1`.)
  - `p(0) = (1−q)^n` by a multiply loop (`intPow`, n multiplications; `Math.pow` and `**` are banned). With n ≤ ~60 and `1−q ≥ 0.5`, `p(0) ≥ 2^-60`, far above double underflow.
  - Walk `k = 0, 1, …` accumulating `p(k+1) = p(k) · (n−k)/(k+1) · q/(1−q)` until the cumulative sum exceeds `u`; if rounding leaves `u` above the final sum, return n.
  It uses only `× ÷ + −`, so it's allowed, and it matches per-member draws in distribution. Draws use the start-of-season counts, so one outcome can't shift another. Proposed log edit: "Births/deaths via one binomial draw per bracket (inverse CDF, basic arithmetic only)". Under option B this would need a fixed-point CDF table.
- Deaths: per bracket, `q = baseMortality[bracket] + hungerMortality[bracket, hungerState]`. Purpose `Death`, entity = band; the bracket index is folded into the purpose space via new codes `DeathChild` … `DeathElder` ([NEED: Jordan] new codes vs a sub-purpose convention).
- Births: `n = round(adults_and_young_adults / 2)` (fertile women, [UNCERTAIN] simplification), `q = birthRate · fertilityFactor(hungerState)`. Purpose `Birth`.
- Aging: a fixed fraction of each bracket moves up each season (`1 / span_in_seasons`), using deterministic rounding with a carried remainder per band, so no draw is needed.

| Tunable | Tag |
|---|---|
| Base mortality by bracket | calibrate to l15 ≈ 0.57, modal adult death ~72 [R: report 3; Gurven & Kaplan 2007 per batch review] |
| Birth rate | TFR 4.5-6, interbirth interval ~3.5 yr [R: report 3] |
| `hungerMortality`, `fertilityFactor` | [P] |

## 11. Migration
- Trigger: hunger state `hungry` or worse for `migrateAfter` consecutive seasons.
- Target search: land cells within `searchRadius` of the camp; score = expected catchment yield at the target (current fields) − `travelCost · distance`. Move only if the best score beats the current camp by `migrateMargin`.
- Tie-break: lowest cell index (deterministic).
- Randomness: none in the slice (lean), so "why it moved" stays a pure function of state. [NEED: Jordan] if a `Migration` draw should add variety.
- A band that finds no better target stays and keeps starving; that difference is what makes the success test readable (one migrates, one dies out).

| Tunable | Tag |
|---|---|
| `migrateAfter`, `searchRadius`, `travelCost`, `migrateMargin` | [P] |

## 12. Die-out
- A band dies out when its total population reaches 0, or falls below `minViable` (survivors are lost; joining a neighbour is out of scope). [NEED: Jordan] floor value or zero.
- Emits `band_died_out`; the band entity stays in the registry as a history record.

## 13. Drought command
Fields: `sign` (−1 drought, +1 rain; one command type, rev 11), `magnitude` (anomaly units, scaled integer), `durationSeasons`, `centerCell`, `radius` (cells; 0 = whole map). Applied at the start of the next tick boundary (log "Nudges" row); recorded in the command log with a command ID that events can cite as a cause.

| Field | Tag |
|---|---|
| magnitude units, default duration, area model | [NEED: Jordan] (question 2) |

## 14. Events (slice set)
| Type | Primary | Emitted when | Causes (≤3) |
|---|---|---|---|
| `drought_began` | `ROOT_ID` | a drought command takes effect | the command |
| `drought_ended` | `ROOT_ID` | duration elapses | `drought_began` |
| `dry_spell_began` / `dry_spell_ended` | `ROOT_ID` | natural regime crossing (§6) | none / `dry_spell_began` |
| `forage_failed` | band | food balance first turns negative after ≥`stableSeasons` non-negative | active drought or dry spell over the catchment, if any |
| `band_hunger_began` | band | hunger state enters `hungry` | `forage_failed` |
| `band_starving` | band | hunger state enters `starving` | `band_hunger_began`, `forage_failed` |
| `band_migrated` | band | migration executes | `band_hunger_began` (or `band_starving`), `forage_failed` |
| `band_died_out` | band | die-out | `band_starving`, `forage_failed` |

- World/region events use `ROOT_ID` as primary, with cell and radius in the payload; same-tick collisions use the ordinal (decided rev 17). Synthetic IDs may replace `ROOT_ID` when forks are worked on.
- Payloads: integers only (cell indices, rounded population, scaled magnitudes).
- Every band outcome cites `forage_failed` directly, so `band_migrated` and `band_died_out` reach `drought_began` in 2 hops (outcome → `forage_failed` → `drought_began`), inside the 3-hop limit. (Bug fixed in v0.2: v0.1's die-out chain was 4 hops.) The intermediate hunger events stay as causes for the fuller "why" walk.

## 15. Legends (templated)
- One `first_valid` template list per event type, filled from payload and band name; seeded by the content key (log "Narration pipeline").
- "Why?" on an event walks causes back to a root (command or root event), max 4 levels shown.
- Pass sentence pattern [NEED: Jordan] (question 11), e.g. "The Ash band left the valley in the spring of year 12. Why? The drought that began in year 11 withered its foraging grounds, and hunger set in."

## 16. Camp snapshot and glance words
Snapshot fields (log rev 11): food balance and trend, stash level, hunger state, 4 bracket counts, season, last foraging trip outcome. "Last foraging trip outcome" = yield vs consumption this season as `good / poor / failed` ([P] thresholds).

| Glance word | Rule | Tag |
|---|---|---|
| thriving | trend rising and stash ≥ `thrivingStash` | [P] |
| settled | trend flat, not hungry | [P] |
| hungry | hunger state hungry | from §9 |
| starving | hunger state starving | from §9 |
| restless | migration triggered but no target yet | [P] |

## 17. Config
All tunables above become `SimConfig` fields with integer values and a stated scale (e.g. `rVPer10000`). The placeholders `seasonsPerYear` and `startingBandSize` are replaced; the config-hash golden value changes once.

## 18. Testing plan
- Unit: each formula (clamping, stability, conservation where it applies, no NaN). Edge cases fixed in v0.2 get named tests: `V = 0` and ocean fauna cells, `n_f > 1` gives the same one-season totals as `n_f = 1` within rounding for small `D`, binomial at `q = 0`, `0.5`, `1` and `n = 0`.
- Property (fast-check, rev 14): every event's causes appear earlier in the log; band outcomes reach a root in ≤3 hops; emission order identical across two runs; same seed + commands → same state hash; populations never negative; vegetation in `[0, K]`.
- Determinism: state hash every 100 seasons, Node (Linux) vs Chrome (Windows) [R: timescale report].
- Acceptance (success test): a fixed seed and scenario with two bands; a drought at season S; run to S + N. Pass when one band has `band_migrated` and the other `band_died_out`, each with a cause chain reaching `drought_began` in ≤3 hops, and the Legends template renders the pass sentence. Scenario values [NEED: Jordan] (question 11).

## 19. Alternatives considered
| Topic | Options | Pick | Why |
|---|---|---|---|
| Number representation | doubles / fixed-point | doubles (rev 15) | §3 |
| Demography draws | per-member + new key field / binomial per bracket | binomial per bracket (lean) | no RNG change; same distribution |
| Event emission | in systems / state-diff detector / transition records + emitter | transition records + emitter (rev 17) | §5; no actions inferred from diffs |
| Migration randomness | none / `Migration` draw | none (lean) | keeps "why" a pure function of state |

## 20. Open questions (grill order)
Ordered so each answer only depends on earlier ones. The rough Gemini draft's pick is noted for each as input, not as a decision.

| # | Question | Depends on | Rough draft's pick |
|---|---|---|---|
| 0 | Number representation (§3) — **settled rev 15: doubles** | — | doubles |
| 1 | Map size and catchment metric (§4, §9) — **settled rev 16: 128×128 default, Euclidean r = 3** | 0 | 128×128, Chebyshev radius 3 |
| 2 | Event emission model and world-event primary (§5, §14) — **settled rev 17: transition records + emitter, `ROOT_ID`** | — | detector pass, `ROOT_ID` |
| 3 | Worldgen and biome table (§4.1) | 0, 1 | 4×3 bands, 8 biomes + ocean |
| 4 | Climate regime shape and dials (§6) | 0, 3 | seasonal table + temporal + regional noise |
| 5 | Drought command fields and area model (§13) | 4 | one signed command, radius 0 = whole map |
| 6 | Vegetation response and recovery targets (§7) | 3, 4, 5 | 50-70% drop in 2-3 seasons; recovery 1.5-2× drought length |
| 7 | Large fauna: grazing, hunting, diffusion (§8) | 6 | lag 1-2 seasons behind vegetation |
| 8 | Food balance: yield, consumption, stash, hunger states (§9) | 6, 7 | (not covered) |
| 9 | Demography: draws, brackets, rates (§10) | 0, 8 | binomial per bracket; 0-14/15-24/25-49/50+ |
| 10 | Migration trigger, search and scoring (§11) | 8 | radius 8, +25% margin, no draw |
| 11 | Die-out floor (§12) | 9 | zero |
| 12 | Event set, thresholds and causes (§14) | 2, 8-11 | as §14 |
| 13 | Glance words and precedence (§16) | 8, 10 | restless ranked first [CONFLICT: hides "starving" on the dying band] |
| 14 | Test scenario and pass sentence (§15, §18) | all | seed `0xDEADBEEF` [UNCERTAIN: worldgen doesn't exist; its geometry is unknown] |

## Changelog
### v0.3 - 2026-10-30
- Decided: Q2 event emission (§5, §14, §19): transition records + one emitter pass; `ROOT_ID` primary for world events.
- Fixed: stale "PBT skill choice still open" in §18 (settled rev 14).
### v0.2 - 2026-10-30
- Fixed: large-fauna divide by zero on barren/ocean cells (§8); rates not scaled per substep (§8); binomial divide by zero at q = 1 (§10); die-out cause chain over 3 hops (§14). Found by the rough Gemini draft's review, verified here.
- Updated: section 20 reordered by dependency, with the rough draft's picks as input.
### v0.1 - 2026-10-30
- Added: first draft from the laptop session's brief and decision log rev 13.
