---
Title: Living mythos: success-test slice
Type: Tech Spec
Version: 0.17
Status: Draft (Phase 2; open questions being grilled in order, section 20)
Owner: Jordan
Created: 2026-10-30
Last Updated: 2026-11-01
Approvers: Jordan
---

# Living mythos: success-test slice (spec v0.17 draft)

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
Techniques, farming, soil, small fauna, water, fire age, crop domestication, band fusion and seasonal aggregation, relations, notable individuals, lore, bloom, forks and fork UI, viewer polish beyond the slice's consumers (glance word, band card, Legends why chains, lab-coat heatmaps for the 2 fields).

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
Decided rev 18 (Q3, option C + both defaults).
- Heightmap: 2D gradient noise. Each lattice point picks one of 8 integer gradients (±1,±1), (±1,0), (0,±1) via `hashKey` (new purpose `WorldgenHeight`, lattice index in `entity`, `entityHi = 0`); quintic fade `t·t·t·(t·(6t−15)+10)`; `octaves` summed with halving amplitude. No trig needed. (v0.3 wrongly said gradient noise needs trig.)
- Edge falloff: subtract `falloff · d²`, d = distance from the map centre normalised to the half-width (`sqrt` only), so the map edge is sea.
- Moisture base: same method, purpose `WorldgenMoisture`; no falloff.
- Sea level: the height value at the `seaLevelPercent` quantile (sorted; ties broken by cell index).
- One landmass (slice only): flood-fill land 4-connected in row-major seed order; keep the largest component (ties: lowest first cell index), set the rest to sea. Islands return when sea travel exists, as a world setting.
- Vegetation capacity: `Kveg(cell) = moistureCurve(baseMoisture) · heightPenalty(height)`, both piecewise-linear lookups. Inferred, unverified: plant productivity rises with rainfall then saturates (Lieth's Miami model), so `moistureCurve` should flatten at the wet end.
- Biome = 4 height bands × 3 moisture bands → ~8 named biomes + ocean, read from the same height and moisture values. Labels only: palette and Legends wording. Biomes are fixed at worldgen; droughts act through the moisture anomaly (§7).

| Tunable | Value | Tag |
|---|---|---|
| `octaves` | 4 | [P] |
| `seaLevelPercent` | 35 | [P] |
| `falloff` | [P] |
| Biome table | 4 height × 3 moisture bands → ~8 biomes + ocean; labels only (rev 18); band cut points and names [P], Endesga ramps from the look tests |
| `moistureCurve`, `heightPenalty` breakpoints | [P]; ~5-6 values total |

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
Decided rev 19 (Q4, option B). Per season, per cell:
`anomaly = clamp(seasonal[season mod 4] + volatility · spaceTimeNoise(x, y, season), ±anomalyClamp) − droughtMagnitude(cell, season)`. Only the natural part is clamped (rev 20), so a drought still bites during a natural dry spell; `minMoistureFactor` (§7) bounds the effect.
- `seasonal[4]`: a 4-entry lookup table, so no trig is needed.
- `spaceTimeNoise`: gradient noise on a coarse lattice in (x, y, season), one lattice point every `climateLatticeCells` cells and every `climateLatticeSeasons` seasons; quintic fade in all three axes; lattice values from `hashKey`, purpose `ClimateSpaceTime`, lattice index in `entity`, `entityHi = 0`. Replaces v0.4's global temporal noise and fixed regional offset, which made every natural dry spell world-wide.
- `severity` dial: sets `anomalyClamp`.
- Regions: climate-lattice blocks (`climateLatticeCells` square). Region mean = mean anomaly over its land cells, row-major order.
- Dry spell: begins when the region mean stays below `dryThreshold` for `dryMinSeasons`; ends only when it rises above `dryThreshold + dryExitGap` (hysteresis). Emits `dry_spell_began` / `dry_spell_ended` with the region index in the payload, primary `ROOT_ID`. A band's catchment counts as in a dry spell when its camp cell's region is.
- Target (Jordan, rev 19): about 15% of seasons in a dry spell per region, averaged over seeds; tune within 12-18%. Tune `dryThreshold` and `volatility` against it. `volatility = 0` gives a nudge-only climate for the test scenario.

| Tunable | Tag |
|---|---|
| `seasonal[4]`, `volatility`, `anomalyClamp`, `climateLatticeCells`, `climateLatticeSeasons`, `dryThreshold`, `dryMinSeasons`, `dryExitGap` | [P]; dials exposed as world settings (log "Climate" row); dry share 12-18% (rev 19) |

## 7. Vegetation
Decided rev 21 (Q6, option B2). Per season, per cell, with `K = Kveg(cell) · moistureFactor(anomaly)` (Kveg from §4.1):
- If `V ≤ K`: `V' = V + rV · V · (1 − V / K) − grazing − harvest`.
- If `V > K` (a drought lowered K): `V' = K + (V − K) · (1 − dieBack) − grazing − harvest`. Decays toward K, never below it from die-back alone. No drought flag: natural dry spells and nudges act the same way, through K.
- Then floor at 0; grazing and harvest removal are capped upstream (§8, §9) so the clamp is a guard, not a mechanism.
- `rV(m)` and `dieBack(m)`: piecewise-linear over base moisture m. Dry (grass-like) = fast drop and fast recovery; wet (forest-like) = slow both.
- `moistureFactor`: piecewise-linear from anomaly, floor `minMoistureFactor`.
- `vegSeed` added when V is 0 so a cell can recover.

| Tunable | Value | Tag |
|---|---|---|
| `dieBack` endpoints | dry 0.40-0.60, wet 0.10-0.20 per season | [P] start (prompt 7 review, shape only) |
| `rV` endpoints | dry 0.60-0.80, wet 0.10-0.25 per season | [P] start |
| `moistureFactor` breakpoints, `minMoistureFactor`, `vegSeed` | | [P] |

Targets [P], severe drought: dry cells drop 45-70% within 1-2 seasons and recover to 90% within 0.5-1.2× drought length; wet cells drop 25-45% over 2-5 seasons and recover within 1.5-2.5×. Grass recovers about as fast as the drought ends, so the lasting shortage that separates "migrated" from "died out" must come from game (§8, Q7), not from slowing plants (no drama tuning).

## 8. Large fauna
Decided rev 22 (Q7, option C + `mDens`). Per cell: herd density `F` and condition `c` (0-1). Per substep, with `h = 1 / n_f`, double-buffered, row-major:
- Intake demand `= F · gMax · V/(V + halfSat) · h` (Type II). Removal `= min(demand, maxGrazeFraction · h · V)`; subtract from V.
- Satisfaction `s = min(1, removal / (F · need · h))` (`s = 1` when `F = 0`).
- Condition `c += condRate · h · (s − c)`. Condition falls over 1-2 dry seasons, which produces the herd lag.
- Births `= rMax · max(0, (c − cBreed)/(1 − cBreed)) · F · h`.
- Deaths `= (mBase + mDens · F + mStarve · max(0, (cStarve − c)/cStarve)) · F · h`. `mDens` (stand-in for predators, disease, crowding) is required: without it the model cycles on rich land (paradox of enrichment; reproduced in a prototype, removed at `mDens ≥ 0.05`).
- Diffusion: `h · Dc · Laplacian(F)` with `Dc = D · (1 + roam · (1 − c))`, so hungry herds spread out of drought. 4-neighbour; sea neighbours contribute the cell's own value (zero flux). Condition moves with the herd as a density-weighted mix.
- Stability: `n_f = max(1, ceil(4 · D · (1 + roam)))` from the maximum possible rate, fixed per config, so the schedule never depends on state (hard rule 4) [verified numerically: stable at h·D = 1/4, unstable at 0.26].
- Capacity emerges from food; `cF`, `rF`, `epsK` from v0.7 are removed. Very poor cells hold no herds.
- Hunting: the large-game guild (§9, rev 23). Food stock per cell = `F · foodPerHerd`; per-season take capped at `maxHuntFraction · F`, with `maxHuntFraction = huntShare · rMax` (rev 29; `huntShare` 0.2 [P], ≈ 0.01).

| Tunable | Value | Tag |
|---|---|---|
| `rMax` | 0.04-0.06 per season | [R: allometry, rmax = 1.375·W^-0.315 (Sinclair 2003): wildebeest 0.248/yr, buffalo 0.208, eland 0.150] |
| `gMax`, `halfSat`, `need`, `maxGrazeFraction`, `condRate`, `cBreed`, `mBase`, `mDens`, `mStarve`, `cStarve`, `D`, `roam`, `huntEff`, `huntHalf`, `maxHuntFraction` | | [P]; `mDens ≥ 0.05` in prototype units |

Targets [P], severe drought (rev 30): herds fall 25-75%; deaths start 1-3 seasons after onset; no cell extinction; back above 50% within 200 seasons. Recovery to 90% is a diagnostic, not a target (prototype 21-194 seasons; rev 22's 30-50 retired). The report's 12-28 seasons was relaxed: in a 576-setting prototype sweep no stable setting with ≥25% crash recovered in under 30. Stability (no self-sustaining boom-bust) is the hard requirement, because cycling herds write false Legends events.

## 9. Bands and food balance
Band state (log Q1, slice subset): `EntityId`, name, camp cell, 4 bracket counts, stash, food balance history (last 4 seasons), hunger seasons counter, alive flag.

| Bracket | Span | Tag |
|---|---|---|
| children | 0-14 yr (0-59 seasons) | [P]; report 3 l15 ≈ 0.57 implies the 15-year cut [R: report 3] |
| young adults | 15-24 yr | [NEED: Jordan] (cut points) |
| adults | 25-49 yr | [NEED: Jordan] |
| elders | 50+ yr | [NEED: Jordan] |

Food (decided rev 23, whole-system review R1, option B): resource guilds.
- Guild interface: per-cell stock in food units (1 = one adult's needs for a season); capacity from fields; regrowth rule (continuous logistic, herd model, or pulsed); per-worker Type II return `a·S/(1 + a·h·S)` on the mean catchment stock S; per-season take cap as a fraction of stock; seasonal factor. Energy only; a protein/fat budget comes with farming.
- Slice guilds: large game (stock `F · foodPerHerd`, regrowth = rev 22 herd model, cap `maxHuntFraction`) and plant foods (capacity tied to V, logistic regrowth, cap `maxGatherFraction`). V is herbivore forage; people never eat it directly (v0.8 gathered ΣV, which fed people grass).
- Catchment = Euclidean disc around the camp, dx² + dy² ≤ `catchment`² (29 cells at r = 3), offsets sorted by (dy, dx); off-map and sea excluded (rev 16).
- Home range and camp (decided rev 24, R2 option B + margin): the band has a home range of radius `homeRange` (5 [P]) around its home cell. Each season, before foraging, it scores every land cell in the home range by expected catchment return (same allocation as below, current stocks); it moves its camp only if the best cell beats the current camp by `campMoveMargin` (fraction [P]); ties go to the lowest cell index. Camp moves are snapshot state, not events. Prey depression deferred.
- Return anchor (rev 28, R4c): per-guild `a` and `h` are scaled so a band on unforaged land of median `Kveg` (median over land cells at worldgen) meets consumption with `effortFull` of its labour (§10). Targets, not fit parameters: density 0.45-1.35 per land cell, bands 25-50, background hunger ≤ 3%.
- Labour `L = Σ bracket · labour[bracket]` (children 0.25, young adults 0.75, adults 1, elders 0.5 [P]).
- Allocation: guilds in rank order (game, then plants); each takes `min(L_left · return, cap, need_left)`; stops at consumption + stash top-up. Removal split evenly across catchment cells (nearest-first deferred). `yieldNoise` from `rand01`, purpose `ForageYield`, entity = band [P].
- Consumption = `Σ bracket · need[bracket]` (0.6 / 1 / 1 / 0.8 [P]).
- Stash: one pooled store, `stash = min(stashSeasons · consumption, (stash + yield − consumption) · (1 − spoilage))`, floored at 0. `stashSeasons` is a world setting (default ≤ 0.5), spoilage 0.15-0.25 per season [P] (prompt 9).
- Food balance = yield − consumption. Food trend = mean of the last 4 balances ÷ consumption, as rising / flat / falling (flat within ±`flatBand`, 5% [P]).
- Hunger state: `hungry` when stash is 0 and balance < 0; `starving` after `starvingSeasons` (2 [P]) consecutive hungry seasons. Q9-Q13 may revise these after R2-R3.
- Diet shifts (meat share) are snapshot state, not events.

| Tunable | Tag |
|---|---|
| `catchment` | 3 cells, Euclidean (rev 16) [R: log 3-5 cells; report 3 catchment 5-12 km at ~3 km/cell] |
| Starting band size | 25 (range 15-50) [R: report 3] |
| per-guild `a`, `h`, `foodPerHerd`, `maxHuntFraction` (≈ 0.01/season), `maxGatherFraction`, `labour[4]`, `need[4]`, `stashSeasons`, `spoilage`, `starvingSeasons`, `flatBand` | [P]; targets in R4 |

## 10. Demography (per season, per band)
Draws (decided rev 31, Q9a option A): one draw per bracket and outcome, sampling the exact binomial `Bin(n, q)` by inverse CDF with one uniform `u = rand01(key)`:
  - `q ≤ 0` → 0 events; `q ≥ 1` → n events (no division).
  - If `q > 0.5`, sample `X' ~ Bin(n, 1−q)` with `1 − u` and return `n − X'`. Using `1 − u` (not `u`, as v0.16 had) keeps draws monotone in q for a fixed key: a harsher season never gives fewer events from the same draw (v0.16's form failed 2,838 of 1.19M prototype checks). The recurrence below then always has `1 − q ≥ 0.5` in its denominator.
  - `p(0) = (1−q)^n` by a multiply loop (`intPow`, n multiplications; `Math.pow` and `**` are banned). With n ≤ ~60 and `1−q ≥ 0.5`, `p(0) ≥ 2^-60`, far above double underflow.
  - Walk `k = 0, 1, …` accumulating `p(k+1) = p(k) · (n−k)/(k+1) · q/(1−q)` until the cumulative sum exceeds `u`; if rounding leaves `u` above the final sum, return n. Inferred: for n ≤ 60 the rounding shortfall (~1e-14) is below `rand01`'s 2^-32 step, so this fallback is unreachable; a property test pins it.
  It uses only `× ÷ + −` and matches per-member draws in distribution (prototype: total-variation distance 8.2e-5, the test grid's resolution). Draws use the start-of-season counts, so one outcome can't shift another. Purposes (appended, rev 31): `DeathChild`, `DeathYoungAdult`, `DeathAdult`, `DeathElder`; `Birth` unchanged; `Death` (4) retired. Entity = band.
- Deaths: per bracket, `q = baseMortality[bracket] + hungerMortality[bracket, hungerState]`. Purpose `Death<Bracket>` (rev 31), entity = band.
- Births: `n = round(adults_and_young_adults / 2)` (fertile women, [UNCERTAIN] simplification), `q = birthRate · fertilityFactor(hungerState) · effortFactor`. Purpose `Birth`.
- Effort (rev 27, R4b): the share of the band's labour needed to meet consumption this season (stash top-up excluded), from the §9 allocation. `effortFactor` = 1 at effort ≤ `effortFull` (0.5 [P]), falling linearly to 0 at effort 1. Regulates population before hunger; hunger mortality is the backstop.
- Aging: a fixed fraction of each bracket moves up each season (`1 / span_in_seasons`), using deterministic rounding with a carried remainder per band, so no draw is needed.

| Tunable | Tag |
|---|---|
| Base mortality by bracket | calibrate to l15 ≈ 0.57, modal adult death ~72 [R: report 3; Gurven & Kaplan 2007 per batch review] |
| Birth rate | TFR 4.5-6, interbirth interval ~3.5 yr [R: report 3] |
| `hungerMortality`, `fertilityFactor` | [P] |
| `effortFull` | 0.5 [P] (rev 27) |

## 11. Migration
- Trigger: hunger state `hungry` or worse for `migrateAfter` consecutive seasons.
- Target search: land cells within `searchRadius` of the camp; score = expected catchment yield at the target (current fields) − `travelCost · distance`. Move only if the best score beats the current camp by `migrateMargin`.
- Tie-break: lowest cell index (deterministic).
- Randomness: none in the slice (lean), so "why it moved" stays a pure function of state. [NEED: Jordan] if a `Migration` draw should add variety.
- A band that finds no better target stays and keeps starving; that difference is what makes the success test readable (one migrates, one dies out).

| Tunable | Tag |
|---|---|
| `migrateAfter`, `searchRadius`, `travelCost`, `migrateMargin` | [P] |

## 12. Band lifecycle and die-out
Decided rev 25 (review R3, option C).
- Fission: a band with hunger state none and population above `fissionAt` (50 [P]) splits in half (floor per bracket; the parent keeps the remainder). The daughter founds a home range at the best free land cell within `searchRadius` whose home cell is at least `homeRange` from every living band's home cell (rev 27; was 2·`homeRange`). The split happens only if that site's expected catchment return covers the daughter's consumption × (1 + `fissionMargin`, 0.2 [P]); otherwise no split this season. Ties: lowest cell index. The daughter gets a lineage ID (parent, tick, sibling index; hard rule 3) and needs the entity registry.
- Dissolution: after `dissolveAfter` (3 [P]) consecutive hungry seasons, a band that has not migrated joins the nearest band with hunger state none within `hostRange` (15 cells [P]) whose current camp's expected catchment return covers host + refugee consumption × (1 + `fissionMargin`) (host guard, rev 26; ties: lowest band ID). Its bracket counts add to the host's. The band ends. With no qualifying host it stays (see perishing).
- Perishing: a band with no host and no migration target stays; it ends when its population falls below `minViable` ([NEED: Jordan] value, Q11).
- Both endings emit `band_died_out` with `outcome` (perished / dissolved) and, when dissolved, the host band ID in the payload. The band entity stays in the registry as a history record.
- Fusion of small healthy bands and seasonal aggregation are deferred.

## 13. Drought command
Decided rev 20 (Q5, option B). Fields: `sign` (−1 drought, +1 rain; one command type, rev 11), `magnitude` (anomaly units, scaled integer), `durationSeasons`, `centerCell`, `radius` (cells; 0 = whole map). Applied at the next tick boundary and recorded in the command log with a command ID that events cite as a cause (confirms rev 12).
- Area: with d = Euclidean distance from `centerCell` (`sqrt`), strength = 1 for d ≤ radius/2, `2·(1 − d/radius)` for radius/2 < d < radius, 0 for d ≥ radius.
- `droughtMagnitude(cell, season)` = Σ over active commands of `sign`-adjusted `magnitude · strength`, in command ID order. Commands stack; no clamp after (§6).
- Onset is instant; vegetation response supplies the lag.
- A whole-map drought leaves no refuge; the test scenario uses a local drought.
- The viewer draws the full-strength core and the fade ring (so radius isn't misread as full-strength area).

| Field | Value | Tag |
|---|---|---|
| magnitude presets | `droughtMild`, `droughtSevere` in anomaly units | [P] |
| default `durationSeasons` | 8 | [P] |

## 14. Events (slice set)
| Type | Primary | Emitted when | Causes (≤3) |
|---|---|---|---|
| `drought_began` | `ROOT_ID` | a drought command takes effect | the command |
| `drought_ended` | `ROOT_ID` | duration elapses | `drought_began` |
| `dry_spell_began` / `dry_spell_ended` | `ROOT_ID` (region index in payload) | natural regime crossing with hysteresis (§6) | none / `dry_spell_began` |
| `forage_failed` | band | food balance first turns negative after ≥`stableSeasons` non-negative | active drought or dry spell over the catchment, if any |
| `band_hunger_began` | band | hunger state enters `hungry` | `forage_failed` |
| `band_starving` | band | hunger state enters `starving` | `band_hunger_began`, `forage_failed` |
| `band_migrated` | band | migration executes | `band_hunger_began` (or `band_starving`), `forage_failed` |
| `band_died_out` | band | perished or dissolved (§12; `outcome` and host ID in payload) | `band_starving` or `band_hunger_began`, `forage_failed` |
| `band_split` | parent band | fission (§12; daughter ID in payload) [P: Q12 confirms] | none |

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
- Unit: each formula (clamping, stability, conservation where it applies, no NaN). Fauna: no-drought stability across vegetation richness 1-8 (no self-sustaining cycles). Edge cases fixed in v0.2 get named tests: `V = 0` and ocean fauna cells, `n_f > 1` gives the same one-season totals as `n_f = 1` within rounding for small `D`, binomial at `q = 0`, `0.5`, `1` and `n = 0`.
- Property (fast-check, rev 14): every event's causes appear earlier in the log; band outcomes reach a root in ≤3 hops; emission order identical across two runs; same seed + commands → same state hash; populations never negative; vegetation in `[0, K]`.
- Determinism: state hash every 100 seasons, Node (Linux) vs Chrome (Windows) [R: timescale report].
- Acceptance (success test): a fixed seed and scenario with two bands; a drought at season S; run to S + N. Pass when one band has `band_migrated` and the other `band_died_out`, each with a cause chain reaching `drought_began` in ≤3 hops, and the Legends template renders the pass sentence. Scenario values [NEED: Jordan] (question 11).

## 19. Alternatives considered
| Topic | Options | Pick | Why |
|---|---|---|---|
| Number representation | doubles / fixed-point | doubles (rev 15) | §3 |
| Demography draws | per-member + new key field / binomial per bracket / expected value + remainder | binomial per bracket, 1 − u flip (rev 31) | §10; no key change; same distribution; deterministic option erased seed variety |
| Event emission | in systems / state-diff detector / transition records + emitter | transition records + emitter (rev 17) | §5; no actions inferred from diffs |
| Migration randomness | none / `Migration` draw | none (lean) | keeps "why" a pure function of state |

## 20. Open questions (grill order)
Ordered so each answer only depends on earlier ones. The rough Gemini draft's pick is noted for each as input, not as a decision.

| # | Question | Depends on | Rough draft's pick |
|---|---|---|---|
| 0 | Number representation (§3) — **settled rev 15: doubles** | — | doubles |
| 1 | Map size and catchment metric (§4, §9) — **settled rev 16: 128×128 default, Euclidean r = 3** | 0 | 128×128, Chebyshev radius 3 |
| 2 | Event emission model and world-event primary (§5, §14) — **settled rev 17: transition records + emitter, `ROOT_ID`** | — | detector pass, `ROOT_ID` |
| 3 | Worldgen and biome table (§4.1) — **settled rev 18: gradient noise, one landmass, continuous capacity, biomes as labels** | 0, 1 | 4×3 bands, 8 biomes + ocean |
| 4 | Climate regime shape and dials (§6) — **settled rev 19: space-time noise, hysteresis, ~15% dry (12-18%)** | 0, 3 | seasonal table + temporal + regional noise |
| 5 | Drought command fields and area model (§13) — **settled rev 20: core-and-fade disc, stacking after the natural clamp** | 4 | one signed command, radius 0 = whole map |
| 6 | Vegetation response and recovery targets (§7) — **settled rev 21: die-back toward K, moisture-dependent rates** | 3, 4, 5 | 50-70% drop in 2-3 seasons; recovery 1.5-2× drought length |
| 7 | Large fauna: grazing, hunting, diffusion (§8) — **settled rev 22: herd-condition model, Type II, required mDens** | 6 | lag 1-2 seasons behind vegetation |
| 8 | Food balance (§9) — **reframed by the whole-system review; R1 settled rev 23: resource guilds** | 6, 7 | (not covered) |
| R2 | Home range + seasonal camp (§9, §11) — **settled rev 24: seasonal camp with a move margin; migration shifts the home range; prey depression deferred** | 8 | — |
| R3 | Band lifecycle (§12) — **settled rev 25: fission with a viability guard, dissolution into a fed neighbour, outcome on `band_died_out`** | R2 | — |
| R4a | Host guard for dissolution (§12) — **settled rev 26: host must feed host + refugees × 1.2** | R3 | — |
| R4b | Population regulation; band size vs density vs home-range spacing (§9-§12) — **settled rev 27: effort-scaled fertility, homes ≥ `homeRange` apart** | R4a | — |
| R4c | Per-worker return anchor (food unit vs need) (§9) — **settled rev 28: fresh effort = `effortFull` on median land** | R4b | — |
| R4d | Hunt cap basis and meat share (§8, §9) — **settled rev 29: `huntShare` × `rMax`** | R4c | — |
| R4e | Herd recovery target (§8) — **settled rev 30: recovery time is a diagnostic** | R4d | — |
| 9a | Demography draws and purpose codes (§10) — **settled rev 31: binomial per bracket, inverse CDF, 1 − u flip, four death purposes** | 0, 8 | binomial per bracket |
| 9b | Bracket cut points and base rates (base mortality to l15 ≈ 0.57, birth rate to TFR 4.5-6) (§9, §10) | 9a | 0-14/15-24/25-49/50+ |
| 9c | Hunger mortality by age; how `effortFactor` and `fertilityFactor(hungerState)` combine (§10) | 9b, R4b | — |
| 10 | Migration trigger, search and scoring (§11) | 8 | radius 8, +25% margin, no draw |
| 11 | Die-out floor `minViable` for perishing bands (§12) | 9, R3 | zero |
| 12 | Event set, thresholds and causes (§14) | 2, 8-11 | as §14 |
| 13 | Glance words and precedence (§16) | 8, 10 | restless ranked first [CONFLICT: hides "starving" on the dying band] |
| 14 | Test scenario and pass sentence (§15, §18) | all | seed `0xDEADBEEF` [UNCERTAIN: worldgen doesn't exist; its geometry is unknown] |

## Changelog
### v0.17 - 2026-11-01
- Decided: Q9a demography draws (§10). Fixed: the q > 0.5 flip now uses 1 − u (monotone in q). Q9 split into Q9a-Q9c (§20).
### v0.16 - 2026-11-01
- Decided: R4e herd recovery target (§8). Whole-system review closed; Q9 next.
### v0.15 - 2026-11-01
- Decided: R4d hunt cap basis (§8).
### v0.14 - 2026-11-01
- Decided: R4c return anchor (§9).
### v0.13 - 2026-11-01
- Decided: R4b population regulation (§10 effort factor; §12 fission spacing `homeRange`).
### v0.12 - 2026-11-01
- Decided: R4a host guard (§12). R4 split into R4a-R4e (§20). Rev 25's quiet-baseline evidence corrected (growth-phase snapshot).
### v0.11 - 2026-11-01
- Decided: R3 band lifecycle (§12): fission, dissolution, perishing; `band_died_out` gains `outcome`; `band_split` added for Q12. Non-goals (§1) now exclude only fusion and aggregation.
### v0.10 - 2026-11-01
- Decided: R2 home range and seasonal camp (§9). Migration (§11) now shifts the home range; its search and scoring stay Q10.
### v0.9 - 2026-10-31
- Decided: R1 resource guilds (§9; whole-system review, `design/integration-review-2026-10-30.md`). Hunting moved from §8 into the large-game guild.
- Fixed: v0.8 §9 fed people vegetation V directly.
- Added: R2-R4 to the grill order (§20), ahead of Q9.
### v0.8 - 2026-10-30
- Decided: Q7 large fauna (§8): herd-condition model, Type II intake with cap, required density mortality, condition-scaled diffusion with fixed substeps.
- Removed: v0.7's `cF·V` capacity and its divide-by-zero guard (`epsK`), superseded.
### v0.7 - 2026-10-30
- Decided: Q6 vegetation (§7): die-back toward K, rV and dieBack over base moisture, targets from the prompt 7 review.
- Noted for Q7: grazing is Type I and fauna capacity follows V instantly, so herds crash with the grass (no lag).
### v0.6 - 2026-10-30
- Decided: Q5 drought command (§13): core-and-fade area, stacking, presets; clamp moved to the natural anomaly only (§6).
### v0.5 - 2026-10-30
- Decided: Q4 climate (§6): space-time noise, regional dry spells with hysteresis, dry-share target 15% (12-18%).
### v0.4 - 2026-10-30
- Decided: Q3 worldgen (§4.1): gradient noise, edge falloff, largest landmass kept, continuous vegetation capacity; biomes are labels.
- Fixed: claim that gradient noise needs trig.
### v0.3 - 2026-10-30
- Decided: Q2 event emission (§5, §14, §19): transition records + one emitter pass; `ROOT_ID` primary for world events.
- Fixed: stale "PBT skill choice still open" in §18 (settled rev 14).
### v0.2 - 2026-10-30
- Fixed: large-fauna divide by zero on barren/ocean cells (§8); rates not scaled per substep (§8); binomial divide by zero at q = 1 (§10); die-out cause chain over 3 hops (§14). Found by the rough Gemini draft's review, verified here.
- Updated: section 20 reordered by dependency, with the rough draft's picks as input.
### v0.1 - 2026-10-30
- Added: first draft from the laptop session's brief and decision log rev 13.
