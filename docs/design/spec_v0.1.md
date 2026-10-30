---
Title: Living mythos: success-test slice
Type: Tech Spec
Version: 0.1
Status: Draft (Phase 2; tags under grilling)
Owner: Jordan
Created: 2026-10-30
Last Updated: 2026-10-30
Approvers: Jordan
---

# Living mythos: success-test slice (spec v0.1)

## Executive summary
This spec defines the smallest simulation that passes the v1 success test: "I trigger a drought and can read in the Legends why one band migrated and another died out." It covers worldgen (heightmap + biomes), a seeded climate regime, two fields (vegetation, large fauna), bands with food balance and 4 age brackets, migration and die-out, the drought nudge, caused events and templated Legends (decision log rev 9). Every tunable is tagged with its source. Nothing here overrides `design/decision-log.md`; where they disagree, the log wins and this spec gets a `[CONFLICT]` tag.

Tag key: **[R: source]** research-backed range · **[P]** placeholder, set by batch tuning · **[NEED: Jordan]** design choice · **[UNCERTAIN]** unverified · **[CONFLICT]** disagrees with the log.

Code facts below were checked against the repo on 2026-10-30 (laptop commit `09dee57`, tick loop, not yet pushed).

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

## 3. Number representation (open: question 0)
| Option | What it means | Cost | Risk |
|---|---|---|---|
| A. Doubles in state, basic ops only (lean) | Field and band state in `Float64Array`/numbers; config scaled integers divided once at load; payloads rounded to integers at emission | Least code; normal formulas | NaN/±0 must be guarded before state hashing; operation order must stay fixed (no parallel reductions) |
| B. Fixed-point integers everywhere | Every quantity a scaled integer with a stated scale, rounding rule and max intermediate < 2^53 | Every formula needs scale bookkeeping; small growth terms can round to 0 | Silent stalls from rounding; harder to read and tune |

Known: ECMAScript Number arithmetic is IEEE 754 double with round-to-nearest, and engines may not fuse operations, so `+ − × ÷` and `sqrt` give the same results everywhere. Inferred: Float32Array storage is also deterministic (rounding to float32 is specified), but it adds a second precision to reason about, so the lean is Float64Array. External check: the cross-engine state-hash test (benchmark step 5), run once the tick loop drives fields.

The rest of this spec writes formulas as plain arithmetic. Under option B each would also need its scale, rounding and bounds; those get added only if B is picked.

## 4. World
| Item | Value | Tag |
|---|---|---|
| Map size | 128×128 cells for the slice; 256×256 stays the v1 working size | [NEED: Jordan] (question 1). 256×256 ≈ 770 km at ~3 km/cell [R: report 3 catchment 5-12 km; log "Cell size" row] |
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
| 8 | regime_detector | 1 | previous vs current regime per band/region | events |
| 9 | snapshot | 1 | sim state | camp snapshot (read-only copy) |

[NEED: Jordan] whether events are emitted inside each system or by one detector pass (#8). Lean: detector pass, because it compares start-of-season and end-of-season regimes in one place, which keeps causes consistent and keeps logging out of the field code.

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
Per substep: `F' = F + rF · F · (1 − F / (cF · V)) − hunting/n_f + D · Laplacian(F)`, 4-neighbour Laplacian, closed boundaries at sea.
- Stability (explicit diffusion, 2D): `D · dt / dx² ≤ 1/4` per substep, so `n_f = ceil(4 · D)` with `dt = 1 season`, `dx = 1 cell` [R: standard FTCS stability limit].
- Grazing removes vegetation in proportion to F (`grazeRate`).
- Iteration order: row-major with a double buffer, so update order can't change results.

| Tunable | Tag |
|---|---|
| `rF`, `cF`, `D`, `grazeRate` | [P]. Report 3's overkill/regeneration ranges are a starting band, not values [R: report 3 ranges, equations rejected] |

## 9. Bands and food balance
Band state (log Q1, slice subset): `EntityId`, name, camp cell, 4 bracket counts, stash, food balance history (last 4 seasons), hunger seasons counter, alive flag.

| Bracket | Span | Tag |
|---|---|---|
| children | 0-14 yr (0-59 seasons) | [P]; report 3 l15 ≈ 0.57 implies the 15-year cut [R: report 3] |
| young adults | 15-24 yr | [NEED: Jordan] (cut points) |
| adults | 25-49 yr | [NEED: Jordan] |
| elders | 50+ yr | [NEED: Jordan] |

Forage per season:
- Catchment = cells within radius `catchment` of the camp (Chebyshev or Euclidean: [NEED: Jordan]; lean Chebyshev for simplicity), land only.
- Labour `L = adults + 0.5·youngAdults` (weights [P]).
- Yield = `L · (gatherEff · ΣV_share + huntEff · ΣF_share) · yieldNoise`, where `yieldNoise` comes from `rand01` with purpose `ForageYield`, entity = band. Harvest and hunting are subtracted from the cells the band forages, split evenly across the catchment ([P]; a nearest-first split is the alternative).
- Consumption = `Σ bracket · need[bracket]`.
- Stash: `stash = min(stashCap · population, (stash + yield − consumption) · (1 − spoilage))`, floored at 0.
- Food balance = yield − consumption. Food trend = mean of the last 4 balances, as a sign word: rising / flat / falling (band `flatBand` [P]).
- Hunger state: `hungry` when stash is 0 and balance < 0; `starving` after `starvingSeasons` consecutive hungry seasons.

| Tunable | Tag |
|---|---|
| `catchment` | 3 cells [R: log 3-5 cells; report 3 catchment 5-12 km at ~3 km/cell] |
| Starting band size | 25 (range 15-50) [R: report 3] |
| `gatherEff`, `huntEff`, `need[4]`, `stashCap`, `spoilage`, `starvingSeasons`, `flatBand` | [P] |

## 10. Demography (per season, per band)
**[CONFLICT]** The log's Demography row says "births/deaths via per-member hash draws". The key has no member index (`rng.ts`), so per-member draws need either a new key field or a different method. Proposal (only valid under number option A): one draw per bracket and outcome, sampling the exact binomial by inverse CDF. The pmf recurrence `p(k+1) = p(k) · (n−k)/(k+1) · q/(1−q)` from `p(0) = (1−q)^n` (n repeated multiplications) uses only `× ÷`, so it's allowed, and it reproduces per-member results in distribution with n ≤ ~60. Draws use the start-of-season counts, so one outcome can't shift another. Proposed log edit: "Births/deaths via one binomial draw per bracket (inverse CDF, basic arithmetic only)". Under option B this would need a fixed-point CDF table.
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
| `band_starving` | band | hunger state enters `starving` | `band_hunger_began` |
| `band_migrated` | band | migration executes | `band_hunger_began` (or `band_starving`) |
| `band_died_out` | band | die-out | `band_starving` |

- World/region events use `ROOT_ID` as primary [NEED: Jordan] (question 9; lean accept).
- Payloads: integers only (cell indices, rounded population, scaled magnitudes).
- Example chain [UNCERTAIN: illustration]: command → `drought_began` → `forage_failed` → `band_hunger_began` → `band_migrated` (3 hops from the migration back to the drought event).

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
- Unit: each formula (clamping, stability, conservation where it applies, no NaN).
- Property (PBT skill choice still open): same seed + commands → same state hash; populations never negative; vegetation in `[0, K]`.
- Determinism: state hash every 100 seasons, Node (Linux) vs Chrome (Windows) [R: timescale report].
- Acceptance (success test): a fixed seed and scenario with two bands; a drought at season S; run to S + N. Pass when one band has `band_migrated` and the other `band_died_out`, each with a cause chain reaching `drought_began` in ≤3 hops, and the Legends template renders the pass sentence. Scenario values [NEED: Jordan] (question 11).

## 19. Alternatives considered
| Topic | Options | Pick | Why |
|---|---|---|---|
| Number representation | doubles / fixed-point | open (lean doubles) | §3 |
| Demography draws | per-member + new key field / binomial per bracket | binomial per bracket (lean) | no RNG change; same distribution |
| Event emission | in systems / detector pass | detector pass (lean) | one place compares regimes |
| Migration randomness | none / `Migration` draw | none (lean) | keeps "why" a pure function of state |

## 20. Open questions (grill order)
0. Number representation (§3).
1. Map size and catchment metric.
2. Drought command fields.
3. Demography draws ([CONFLICT] with the log's wording) and bracket cut points.
4. Event emission model and `ROOT_ID` primary.
5. Climate regime shape.
6. Vegetation and fauna targets (what a drought should look like over time).
7. Migration rules and randomness.
8. Die-out floor.
9. Glance-word thresholds.
10. Test scenario and pass sentence.
11. Worldgen biome table.

## Changelog
### v0.1 - 2026-10-30
- Added: first draft from the laptop session's brief and decision log rev 13.
