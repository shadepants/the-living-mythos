---
Title: Living mythos: success-test slice
Type: Tech Spec
Version: 0.27
Status: Draft, v1.0 proposed (Phase 3 finalize complete: revs 39-41; awaiting Jordan's approval)
Owner: Jordan
Created: 2026-10-30
Last Updated: 2026-11-02
Approvers: Jordan
---

# Living mythos: success-test slice (spec v0.27 draft, v1.0 proposed)

## Executive summary
This spec defines the smallest simulation that passes the v1 success test: "I trigger a drought and can read in the Legends why one band migrated and another died out." It covers worldgen (heightmap + biomes), a seeded climate regime, two fields (vegetation, large fauna) plus a plant-food stock, bands with food balance and 4 age brackets, migration, fission and die-out, the drought nudge, caused events and templated Legends (decision log rev 9, extended by revs 23-38). Every tunable is listed in §17 with its scale and tag. Nothing here overrides `design/decision-log.md`; where they disagree, the log wins and this spec gets a `[CONFLICT]` tag.

Tag key: **[R: source]** research-backed range · **[P]** placeholder, set by batch tuning · **[NEED: Jordan]** design choice · **[UNCERTAIN]** unverified · **[CONFLICT]** disagrees with the log. Requirement words MUST / MUST NOT / SHOULD / MAY follow RFC 2119.

Code facts were checked against the repo on 2026-11-01 (`packages/sim-core`: rng, config, lineage, event log, tick loop; 67 tests + 1 todo; `Purpose` codes 1-5).

## Contents
1 Goals · 2 Constraints · 3 Numbers · 4 World · 5 Systems, state and run order · 6 Climate · 7 Vegetation and plant food · 8 Large fauna · 9 Bands and food · 10 Demography · 11 Migration · 12 Lifecycle · 13 Drought command · 14 Events · 15 Legends · 16 Snapshot and glance · 17 Config · 18 Testing · 19 Alternatives · 20 Errors, build order, rollback · 21 Decision trace · 22 Future consideration · Changelog

## 1. Goals / non-goals
**Goals**
- G1. A seeded world where bands forage, go hungry, migrate or die out for traceable reasons.
- G2. A drought command applied at a tick boundary and logged with a command ID that events cite.
- G3. A Legends "why" chain from `band_migrated` / `band_died_out` back to `drought_began` in at most 3 hops.
- G4. Same seed + same command log → identical state hash on Windows/Chrome and Linux/Node.

**Non-goals (later spec versions)**
Techniques, farming, soil, small fauna, water, fire age, crop domestication, band fusion and seasonal aggregation, relations, notable individuals, lore, bloom, forks and fork UI, viewer polish beyond the slice's consumers (glance word, band card, Legends why chains, lab-coat heatmaps for the 2 fields).

## 2. Constraints (from the log and code)
- Hard rules 1-7. Built: 1 (`rng.ts`), 2 (`eslint.config.js`), 3 (`lineage.ts`), 4 (`tick.ts`), 5 (`event-log.ts`), 7 (`config.ts`). Not built: 6 (command log, keyframes), entity registry.
- RNG key `(seed, season, entity, entityHi, purpose)`, all uint32. `Purpose` codes, append only, never renumbered:

| Code | Name | Keyed on | Status |
|---|---|---|---|
| 1 | `ForageYield` | band | used (§9 yield noise) |
| 2 | `Migration` | band | reserved, unused in the slice (migration has no draw, rev 34) |
| 3 | `Birth` | band | used (§10) |
| 4 | `Death` | band | retired (rev 31), never reused |
| 5 | `Invention` | band | reserved (techniques) |
| 6-9 | `DeathChild`, `DeathYoungAdult`, `DeathAdult`, `DeathElder` | band | used (§10, rev 31) |
| 10 | `WorldgenHeight` | lattice index, `entityHi = 0` | used (§4.1) |
| 11 | `WorldgenMoisture` | lattice index, `entityHi = 0` | used (§4.1) |
| 12 | `ClimateSpaceTime` | lattice index, `entityHi = 0` | used (§6) |

  Appending codes leaves the RNG golden values unchanged. Codes 10-12 are cell-keyed and no lineage entity uses them (rev 13).
- Banned in sim-core: Math.random, trig, exp/log, pow, cbrt, hypot, `**`, Date, performance.now. Allowed: `+ − × ÷`, Math.sqrt, integer bit ops.
- `SimConfig` is flat safe integers; fractional tunables are scaled integers (rev 12; scale rule in §17). Real tunables replace the placeholders and change the config-hash golden value once (no saves exist).
- Events: snake_case type; `tick` = absolute season; ≤ 3 causes (event or command); flat integer payload; content key `type:tick:primary:ordinal`; `primary` is an `EntityId`.
- Where code is written (rev 42): sim-core changes merge into `Main-REPO` only after `pnpm check` passes on Windows (CI `windows-latest` or the laptop). Interim (rev 43): while neither is available, a green Linux `pnpm check` plus a clean determinism review; Windows check first when the laptop returns.
- Tick loop: one tick = one season; systems in fixed array order with `period`, `offset`, `substeps` (1-1024); the schedule never depends on state.

## 3. Number representation (decided rev 15: option A)
Sim state holds IEEE 754 doubles (`Float64Array` and numbers) using only `+ − × ÷` and `Math.sqrt`. The state hash rejects NaN and ±Infinity and normalizes -0 to 0. Sums over cells or bands run in a fixed order (row-major, band ID order); no parallel reductions. Config scaled integers are divided once at load; event payloads are rounded to integers at emission, half away from zero. Basic IEEE 754 operations are exact across engines; the cross-engine state-hash test (benchmark step 5) is the external check. Fixed-point everywhere was rejected (scale bookkeeping in every formula; small terms round to 0).

## 4. World
| Item | Value | Tag |
|---|---|---|
| Map size | `worldWidth` × `worldHeight`; slice default 128×128 (~385 km); v1 working size 256×256; property tests MAY use 32×32 | Decided rev 16 |
| Cell size | ~3 km (presentation only: Legends km = round(cells × `cellKm`)) | [R: log] |
| Seasons per year | 4 | [R: log] |

### 4.1 Worldgen (once, at season 0)
Decided rev 18 (Q3, option C + both defaults).
- Heightmap: 2D gradient noise. Each lattice point picks one of 8 integer gradients (±1,±1), (±1,0), (0,±1) via `hashKey` (purpose `WorldgenHeight`, lattice index in `entity`, `entityHi = 0`); quintic fade `t·t·t·(t·(6t−15)+10)`; `octaves` summed with halving amplitude. No trig.
- Edge falloff: subtract `falloff · d²`, d = distance from the map centre normalised to the half-width (`sqrt` only), so the map edge is sea.
- Moisture base: same method, purpose `WorldgenMoisture`; no falloff.
- Sea level: the height value at the `seaLevelPercent` quantile (sorted; ties broken by cell index).
- One landmass (slice only): flood-fill land 4-connected in row-major seed order; keep the largest component (ties: lowest first cell index); set the rest to sea. Islands return with sea travel, as a world setting.
- Vegetation capacity: `Kveg(cell) = moistureCurve(baseMoisture) · heightPenalty(height)`, both piecewise-linear lookups. Inferred, unverified: plant productivity rises with rainfall then saturates (Lieth's Miami model), so `moistureCurve` should flatten at the wet end.
- Biome = 4 height bands × 3 moisture bands → ~8 named biomes + ocean, read from the same height and moisture values. Labels only (palette and Legends wording). Fixed at worldgen; droughts act through the moisture anomaly (§6).
- Return anchor input: the median `Kveg` over land cells, computed once here (§9).

## 5. Systems, state and run order
All systems run every season in the slice (period 1, offset 0). Slow-system periods come with later fields.

| # | System | Substeps | Reads | Writes |
|---|---|---|---|---|
| 1 | apply_commands | 1 | command log | active nudges |
| 2 | climate | 1 | seed, dials, active nudges | per-cell moisture anomaly; region dry-spell state |
| 3 | vegetation | 1 | anomaly, base moisture, `Kveg`, last season's grazing | V; plant-food stock P (§7) |
| 4 | large_fauna | `n_f` (stability limit, fixed per config) | V | F, condition c, grazing removal |
| 5 | forage | 1 | P, F, band labour and need | camp choice, guild removal, yield, stash, balance, effort, shortfall, hunger counter |
| 6 | demography | 1 | brackets, effort, shortfall | brackets (births, deaths, aging) |
| 7 | migration | 1 | hunger counter, P, F, other bands' camps and labour | home cell, camp cell, `searchFailed` |
| 8 | lifecycle | 1 | hunger counter, population, P, F, other bands | dissolution, perishing, fission (§12); entity registry |
| 9 | emit_events | 1 | this season's transition records, event log | events |
| 10 | snapshot | 1 | sim state | camp snapshot (read-only copy) |

Lifecycle runs after migration, so a band that migrated this season is not dissolved in the same season (§12). Hunting and gathering removals from forage (#5) act on stocks that vegetation (#3) and large_fauna (#4) regrow next season.

Decided (rev 17, option C): systems 1-8 never append events. Each writes transition records to a per-season buffer (e.g. `command_applied`, `dry_spell_crossed`, `balance_turned_negative`, `hunger_changed`, `moved {from, to}`, `ended {outcome, host}`, `split {daughter}`). Each record carries its subject (band `EntityId` or `ROOT_ID`) and the facts the emitter needs. `emit_events` sorts records by subject (`ROOT_ID` first, then band ID order), keeps record order within a subject, turns each into an event and attaches causes by looking up earlier events. The buffer is cleared after emission and is not saved state. A new system adds record types and emitter rules; existing systems don't change.

### 5.1 State (slice)
| Owner | Field | Type | Notes |
|---|---|---|---|
| World | `height`, `baseMoisture`, `Kveg`, `biome`, `isLand` | `Float64Array` / `Uint8Array` per cell | fixed at worldgen |
| World | `medianKveg` | number | return anchor input (§9) |
| World | `anomaly` | `Float64Array` | rewritten each season |
| World | per-region dry-spell flag, below/above-threshold counters, open `dry_spell_began` event ID | small arrays | hysteresis (§6) |
| World | `V`, `P`, `F`, `c` | `Float64Array` per cell | V vegetation, P plant-food stock, F herd density, c herd condition |
| World | active nudges | list ordered by command ID | from the command log |
| Band | `EntityId`, alive flag, name index | | name is presentation only |
| Band | `homeCell`, `campCell` | cell index | |
| Band | bracket counts ×4, aging remainders ×3 | numbers | §10 |
| Band | `stash`, `balance`, `effort`, `shortfall` | numbers | this season (§9, §10) |
| Band | `hungerSeasons`, `nonNegSeasons` | integers | hunger state and episode closing (§9, §14) |
| Band | open episode `forage_failed` event ID or none | event ID | §14 |
| Band | last season inside a drought or dry spell, and that event's ID | integer, event ID | climate lookback (§14) |
| Band | pressure ring (4 entries) | numbers | food trend (§16, rev 40); snapshot only |
| Band | `searchFailed` | boolean | band-card line (§16) |
| Band | parent `EntityId`, founding tick | | entity registry (hard rule 3) |
| Command | `id`, `tick`, `sign`, `magnitude`, `durationSeasons`, `centerCell`, `radius` | integers | §13 |

## 6. Climate regime
Decided rev 19 (Q4, option B). Per season, per cell:
`anomaly = clamp(seasonal[season mod 4] + volatility · spaceTimeNoise(x, y, season), ±anomalyClamp) − droughtMagnitude(cell, season)`. Only the natural part is clamped (rev 20), so a drought still bites during a natural dry spell; `minMoistureFactor` (§7) bounds the effect.
- `seasonal[4]`: a 4-entry lookup table (no trig).
- `spaceTimeNoise`: gradient noise on a coarse lattice in (x, y, season), one lattice point every `climateLatticeCells` cells and every `climateLatticeSeasons` seasons; quintic fade in all three axes; lattice values from `hashKey`, purpose `ClimateSpaceTime`, lattice index in `entity`, `entityHi = 0`.
- `severity` dial sets `anomalyClamp`.
- Regions: climate-lattice blocks (`climateLatticeCells` square). Region mean = mean anomaly over its land cells, row-major order.
- Dry spell: begins when the region mean stays below `dryThreshold` for `dryMinSeasons`; ends only when it rises above `dryThreshold + dryExitGap`. Emits `dry_spell_began` / `dry_spell_ended` with the region index in the payload, primary `ROOT_ID`. A band's camp counts as in a dry spell when its camp cell's region is.
- Target (rev 19): about 15% of seasons in a dry spell per region, averaged over seeds; tune within 12-18% via `dryThreshold` and `volatility`. `volatility = 0` gives a nudge-only climate.

## 7. Vegetation and plant food
Decided rev 21 (Q6, option B2). Per season, per cell, with `K = Kveg(cell) · moistureFactor(anomaly)`:
- If `V ≤ K`: `V' = V + rV · V · (1 − V/K)`.
- If `V > K` (a drought lowered K): `V' = K + (V − K) · (1 − dieBack)`. Decays toward K, never below it from die-back alone. No drought flag: dry spells and nudges act the same way, through K.
- Then subtract last season's herd grazing (§8, capped upstream) and floor at 0; add `vegSeed` when V is 0 so a cell can recover.
- `rV(m)` and `dieBack(m)`: piecewise-linear over base moisture m between `moistureDry` and `moistureWet`. Dry (grass-like) = fast drop and fast recovery; wet (forest-like) = slow both.
- `moistureFactor`: piecewise-linear from anomaly, floor `minMoistureFactor`.

Plant-food stock P (the plant guild, rev 23; people never eat V): capacity `Pcap = pFrac · V'` (current vegetation, so a drought cuts plant food through V). Below `Pcap`: `P' = P + rP · P · (1 − P/Pcap)`; above: `P' = Pcap + (P − Pcap) · (1 − dieBack(m))`; then add `pSeed`. Gathering removes from P in forage (§9).

Targets [P], severe drought (rev 21): dry cells drop 45-70% within 1-2 seasons and recover to 90% within 0.5-1.2× drought length; wet cells drop 25-45% over 2-5 seasons and recover within 1.5-2.5×. Prototypes (rev 23) showed plant foods backfill quickly; whether a band migrates or dies out depends on band density, the herd lag, migration scoring and refuge occupancy, not on slow plants. Plant recovery MUST NOT be slowed for drama.

## 8. Large fauna
Decided rev 22 (Q7, option C + `mDens`). Per cell: herd density `F` and condition `c` (0-1). Per substep, with `h = 1 / n_f`, double-buffered, row-major:
- Intake demand `= F · gMax · V/(V + halfSat) · h` (Type II). Removal `= min(demand, maxGrazeFraction · h · V)`; subtract from V.
- Satisfaction `s = min(1, removal / (F · herdNeed · h))` (`s = 1` when `F = 0`).
- Condition `c += condRate · h · (s − c)`. Condition falls over 1-2 dry seasons, which produces the herd lag.
- Births `= rMax · max(0, (c − cBreed)/(1 − cBreed)) · F · h`.
- Deaths `= (mBase + mDens · F + mStarve · max(0, (cStarve − c)/cStarve)) · F · h`. `mDens` (stand-in for predators, disease, crowding) is required: without it the model cycles on rich land (paradox of enrichment, reproduced in a prototype; removed at `mDens ≥ 0.05` in prototype units).
- Diffusion: `h · Dc · Laplacian(F)` with `Dc = D · (1 + roam · (1 − c))`. 4-neighbour; sea neighbours contribute the cell's own value (zero flux). Condition moves with the herd as a density-weighted mix.
- Stability: `n_f = max(1, ceil(4 · D · (1 + roam)))`, fixed per config (hard rule 4) [verified numerically: stable at h·D = 1/4, unstable at 0.26].
- Capacity emerges from food; very poor cells hold no herds.
- Hunting: the large-game guild (§9). Food stock per cell = `F · foodPerHerd`; per-season take capped at `maxHuntFraction · F`, `maxHuntFraction = huntShare · rMax` (rev 29; ≈ 0.01).

Targets [P], severe drought (rev 30): herds fall 25-75%; deaths start 1-3 seasons after onset; no cell extinction; back above 50% within 200 seasons; no self-sustaining boom-bust (cycling herds write false Legends events). Recovery to 90% is a diagnostic (prototype 21-194 seasons).

## 9. Bands and food balance
Brackets (decided rev 32, Q9b option C):

| Bracket | Span | Labour | Need | Notes |
|---|---|---|---|---|
| children | 0-14 yr (60 seasons) | 0.25 | 0.6 | l15 ≈ 0.57 [R: Gurven & Kaplan 2007, verified] |
| young adults | 15-19 yr (20 seasons) | 0.75 | 1 | fertile; mobile bracket |
| adults | 20-44 yr (100 seasons) | 1 | 1 | fertile; main producers |
| elders | 45+ yr | 0.5 | 0.8 | leave by death only |

One aging stage per bracket, so real ages blur (median entry to young adults ~6 yr, to elders ~28 yr; prototype). Three hidden stages per bracket is the upgrade path when a system reads true age.

Food (decided rev 23, R1 option B): resource guilds behind one interface.
- Guild interface: per-cell stock in food units (1 = one adult's needs for one season); a regrowth rule (§7 plant logistic, §8 herd model); a per-worker Type II return `maxReturn · S/(S + halfStock)` on the mean catchment stock S (equivalent to `a·S/(1 + a·h·S)` with `maxReturn = 1/h`, `halfStock = 1/(a·h)`; renamed so `h` means only the fauna substep); a per-season take cap as a fraction of stock; a seasonal factor (1 in all seasons until a field needs otherwise [P]). Energy only; a protein/fat budget comes with farming.
- Slice guilds, in rank order: large game (stock `F · foodPerHerd`, cap `maxHuntFraction`), then plant foods (stock P, cap `maxGatherFraction`).
- Catchment: Euclidean disc around the camp, dx² + dy² ≤ `catchment`² (29 cells at r = 3), offsets sorted by (dy, dx); off-map and sea cells excluded (rev 16).
- Home range and camp (rev 24): radius `homeRange` around the home cell. Each season, before foraging, the band scores every land cell in the home range by expected catchment return (allocation below, current stocks) and moves its camp only if the best cell beats the current camp by more than `campMoveMargin` (fraction); ties go to the lowest cell index. Camp moves are snapshot state, not events.
- Return anchor (rev 28): returns are scaled so a band on unforaged land of median `Kveg` meets its consumption with `effortFull` of its labour. Density 0.45-1.35 per land cell, bands 25-50 and background hunger ≤ 3% are acceptance targets, not fit parameters. Calibration (decided rev 41): the four return constants are written into config by an offline tool that runs the fields with no bands for ≥ 200 seasons on reference seeds at default settings, then solves the scale so a reference band (25 people, starting bracket mix) on median-`Kveg` land meets consumption at `effortFull`. It is a config constant, not computed per world, so seeds keep their richness differences. Herd stock does not scale with `Kveg` (probe: F/K 0.02-0.12) and takes 37-173 seasons to settle, which is why the anchor needs a burn-in and not a formula.
- Labour `L = Σ count[b] · labour[b]`. Consumption `C = Σ count[b] · need[b]`.
- Allocation: guilds in rank order; each takes `min(L_left · return, cap, need_left)`, using labour `need_left / return`; stops at `C` + stash top-up (`max(0, stashSeasons · C − stash)`). Removal is split evenly across the catchment's cells. Yield is multiplied by `1 + yieldNoise · (2u − 1)`, `u = rand01` with purpose `ForageYield`, entity = band; `yieldNoise` defaults to 0 (the prototypes ran without it).
- Effort = labour used to cover `C` ÷ L, capped at 1; 1 whenever yield < C (rev 27).
- Stash: `stash = min(stashSeasons · C, (stash + yield − C) · (1 − spoilage))`, floored at 0. `stashSeasons` is a world setting.
- Balance = yield − C. Shortfall = `1 − min(C, stash_before + yield) / C`.
- Hunger: `hungerSeasons` += 1 when stash is 0 and balance < 0, else resets to 0. State `hungry` at ≥ 1, `starving` at ≥ `starvingSeasons`.
- Diet shifts (meat share) are snapshot state, not events.

## 10. Demography (per season, per band)
Draws (decided rev 31, Q9a option A): one draw per bracket and outcome, sampling the exact binomial `Bin(n, q)` by inverse CDF with one uniform `u = rand01(key)`:
  - `q ≤ 0` → 0 events; `q ≥ 1` → n events (no division).
  - If `q > 0.5`, sample `X' ~ Bin(n, 1−q)` with `1 − u` and return `n − X'`, so draws are monotone in q for a fixed key (v0.16's same-u flip failed 2,838 of 1.19M prototype checks).
  - `p(0) = (1−q)^n` by a multiply loop (`intPow`; `Math.pow` and `**` are banned). With n ≤ ~60 and `1−q ≥ 0.5`, `p(0) ≥ 2^-60`, far above double underflow.
  - Walk `k = 0, 1, …` accumulating `p(k+1) = p(k) · (n−k)/(k+1) · q/(1−q)` until the cumulative sum exceeds `u`; if rounding leaves `u` above the final sum, return n. Inferred: for n ≤ 60 this fallback is unreachable (rounding ~1e-14 < 2^-32); a property test pins it.
  Draws use start-of-season counts, so one outcome can't shift another.
- Deaths: per bracket, `q = baseMortality[b] + shortfall · hungerMortality[b]` (rev 33). Purpose `Death<Bracket>`, entity = band.
- Births: `n = round((youngAdults + adults) / 2)` (fertile women; [UNCERTAIN] simplification), `q = birthRate · effortFactor`, purpose `Birth`. `effortFactor` = 1 at effort ≤ `effortFull`, falling linearly to 0 at effort 1 (rev 27). No hunger fertility factor (rev 33).
- Aging: `count[b] / span[b]` moves up each season, with a carried remainder per band and bracket (deterministic, no draw).

## 11. Migration
Decided rev 34 (Q10, option C).
- Trigger: `hungerSeasons ≥ migrateAfter`.
- Target search: land cells within `searchRadius` of the home cell (Euclidean). Score = expected catchment return with each guild's stock scaled by `share`, minus `travelCost · distance`. `share = L_self / (L_self + Σ L_o · w_o)` over other living bands o, `w_o = max(0, 1 − d_o / (2·catchment))`, d_o = distance from o's camp to the candidate cell [UNCERTAIN: linear overlap stand-in]; sum in band ID order. `share = 0` when `L_self = 0` (rev 35).
- The current range is scored the same way (best camp in the home range, no travel cost). Move only if the best target beats it by more than `migrateMargin` (fraction). The move sets home and camp to the target. If triggered and no target qualifies, set `searchFailed`.
- No spacing rule: targets MAY lie inside other bands' home ranges; occupied land is discounted by `share` (integration review I7).
- Ties: lowest cell index. No draw: "why it moved" stays a pure function of state.

## 12. Band lifecycle and die-out
Decided rev 25, host guard rev 26, spacing rev 27, floor rev 35. Run in this order, in band ID order, after migration:
1. Dissolution: a band with `hungerSeasons ≥ dissolveAfter` that did not migrate this season joins the nearest band (home-to-home distance ≤ `hostRange`) whose hunger state is none and whose current camp's expected catchment return covers host + refugee consumption × (1 + `fissionMargin`); ties lowest band ID. Its bracket counts add to the host's; the band ends with outcome `dissolved` and the host ID.
2. Perishing: a band with no qualifying host whose population is below `minViable` ends with outcome `perished`, or `dwindled` when `hungerSeasons = 0` (rev 36).
3. Fission: a band with hunger state none and population above `fissionAt` splits in half (floor per bracket; the parent keeps the remainder). The daughter founds a home range at the best land cell within `searchRadius` of the parent's home whose distance to every living band's home cell is ≥ `homeRange`, only if that site's expected catchment return covers the daughter's consumption × (1 + `fissionMargin`); otherwise no split this season. Ties: lowest cell index. The daughter gets a lineage ID (parent, tick, sibling index) registered in the entity registry.
- Ended bands stay in the registry as history records.
- Die-out in the slice is mostly dissolution: perishing in place needs a near-total food failure that the slice drought doesn't produce (prototype: cut-off bands settle at 12-24 people). Floors and drought caps MUST NOT be tuned to manufacture perishing (rev 35).

## 13. Drought command
Decided rev 20 (Q5, option B). Fields: `sign` (−1 drought, +1 rain; one command type, rev 11), `magnitude` (anomaly units, scaled integer), `durationSeasons`, `centerCell`, `radius` (cells; 0 = whole map). Applied at the next tick boundary and recorded in the command log with a command ID that events cite.
- Area: with d = Euclidean distance from `centerCell`, strength = 1 for d ≤ radius/2, `2·(1 − d/radius)` for radius/2 < d < radius, 0 for d ≥ radius.
- `droughtMagnitude(cell, season)` = Σ over active commands of `−sign · magnitude · strength`, in command ID order. Commands stack; no clamp after (§6).
- Onset is instant; vegetation response supplies the lag.
- A whole-map drought leaves no refuge; the test scenario uses a local drought.
- The viewer draws the full-strength core and the fade ring.

## 14. Events (slice set)
Decided rev 36 (Q12, option B).

| Type | Primary | Emitted when | Causes (≤ 3) |
|---|---|---|---|
| `drought_began` | `ROOT_ID` | a drought command takes effect | the command |
| `drought_ended` | `ROOT_ID` | duration elapses | `drought_began` |
| `dry_spell_began` / `dry_spell_ended` | `ROOT_ID` (region index in payload) | regime crossing with hysteresis (§6) | none / `dry_spell_began` |
| `forage_failed` | band | balance turns negative after ≥ `stableSeasons` non-negative seasons; payload `stockPct`, `sharePct` | `drought_began` / `dry_spell_began` if the band's camp was inside it at any season within `causeWindow`; else none |
| `band_hunger_began` | band | hunger state enters `hungry` | the episode's `forage_failed` |
| `band_starving` | band | hunger state enters `starving` | `band_hunger_began`, the episode's `forage_failed` |
| `band_migrated` | band | migration executes (payload from/to cells) | `band_starving` (or `band_hunger_began`), the episode's `forage_failed` |
| `band_died_out` | band | dissolved, perished or dwindled (§12); payload `outcome`, host ID when dissolved | `band_starving` or `band_hunger_began`, the episode's `forage_failed`; `dwindled` has none |
| `band_split` | parent band | fission (§12); daughter ID in payload | none |

- `stockPct` = plant-food stock summed over the camp catchment ÷ base plant capacity summed over the same cells (`pFrac · Kveg`, no drought), × 100, rounded (rev 38; the prototype basis). Game is excluded: herds have no fixed capacity. `sharePct` = own labour share (§11 weighting) × 100.
- Shortfall episode: opened by a `forage_failed`; closed once the band has had `stableSeasons` non-negative seasons and is not hungry. Hunger and outcome events cite only the open episode's `forage_failed`. Every hunger event has one (prototype: 0 exceptions).
- Climate lookback: each band keeps the last season its camp cell was inside an active drought (strength > 0) or dry spell, and that event's ID. Attribution is by proximity in time, not mechanism; `stockPct` is the reader's check.
- `dwindled` = perished with no current hunger streak; the Legends say it dwindled and broke up.
- Reason wording (depleted, crowded, drought) is chosen by narration from the payload; the sim holds no reason threshold.
- World/region events use `ROOT_ID` with cell and radius in the payload; same-tick collisions use the ordinal (rev 17).
- Payloads: integers only.
- Every non-`dwindled` band outcome cites `forage_failed` directly, so outcomes reach `drought_began` in 2 hops.

## 15. Legends (templated)
- One `first_valid` template list per event type, filled from payload and band name; seeded by the content key.
- "Why?" on an event walks causes back to a root (command or root event), max 4 levels shown.
- Pass sentence templates (decided rev 38), filled from the outcome event, its episode's `forage_failed` payload and the cited hunger event:
  - `band_migrated`: "The {band} band left its lands in the {season} of year {y} and walked {km} km to new ground. Why? The drought that began in the {season} of year {y} cut its foraging grounds to {stockPct}% of their usual yield; hunger began in the {season} of year {y}."
  - `band_died_out` dissolved: "The {band} band broke up in the {season} of year {y}; its last people joined the {host} band. Why? The drought that began … ; hunger began …, and no better land lay within reach."
  - `band_died_out` dwindled: worded as dwindling and breaking up, never as starvation (prompt 12 review).
- Rendered from a prototype chain (seed 1, magnitude 1.5): "The Ash band left its lands in the summer of year 1201 and walked 42 km to new ground. Why? The drought that began in the spring of year 1200 cut its foraging grounds to 10% of their usual yield; hunger began in the summer of year 1201." Band names are presentation only.

## 16. Camp snapshot and glance words
Snapshot fields (rev 11, rev 37): food balance and trend, stash level, hunger state, 4 bracket counts, season, last foraging trip outcome, `effort`, `searchFailed`. Last foraging trip outcome = yield ÷ C as `good` (≥ `tripGoodPct`), `poor` (≥ `tripPoorPct`), else `failed`.

Glance words (decided rev 37): one word per band, first match wins.

| # | Glance word | Rule |
|---|---|---|
| 1 | starving | hunger state starving |
| 2 | hungry | hunger state hungry |
| 3 | well-fed | effort ≤ `effortFull` |
| 4 | settled | otherwise |

- `restless` is a band-card line ("searching; no better land within reach") when `searchFailed`.
- No hysteresis (flicker 0.06 word changes per band-year in the prototype).
- "well-fed" claims food, not fate: a band drifting toward `dwindled` can read well-fed to the end.
- Band-card food trend (decided rev 40): pressure = effort while fed, 1 + shortfall otherwise; trend = pressure now − pressure 4 seasons ago; `easing` below −`trendBand`, `worsening` above +`trendBand`, else `steady`. Fewer than 4 seasons of history reads `steady`. Snapshot-only: no sim system reads it. Prototype: calm 99.8% steady, flicker 0.01 per band-year, every map hunger onset preceded by `worsening` (median 4 seasons ahead). The v0.24 mean-balance trend read "rising" at steady state (stash upkeep) and is replaced.
- The card can show `worsening` beside `well-fed` (effort rising but still ≤ `effortFull`) or `easing` beside `starving` (recovering): both are true statements, not contradictions.

## 17. Config
Scale rule: integer counts (cells, seasons, people, percent) are stored as-is; every other tunable is stored × 10,000 with the suffix `Per10k` (e.g. `rVDryPer10k = 7000`). Piecewise-linear tables are flat numbered fields (`moistureCurveX0Per10k`, `moistureCurveY0Per10k`, …). Prototype starting values are in prototype units (rich land `Kveg` = 2) and MUST be rescaled with `Kveg`. Presentation values (`cellKm`, names) and test-scenario parameters are not `SimConfig` and stay out of the config hash.

| Group | Field | Scale | Value / range | Tag |
|---|---|---|---|---|
| World | `worldWidth`, `worldHeight` | cells | 128, 128 | decided rev 16 |
| Worldgen | `octaves` | count | 4 | [P] |
| Worldgen | `seaLevelPercent` | % | 35 | [P] |
| Worldgen | `falloff` | Per10k | — | [P] |
| Worldgen | biome cut points (3 height, 2 moisture) | Per10k | — | [P] |
| Worldgen | `moistureCurve`, `heightPenalty` breakpoints | Per10k pairs | ~5-6 values | [P] |
| Climate | `seasonal0`-`seasonal3` | Per10k | — | [P] |
| Climate | `volatility`, `anomalyClamp` (severity), `dryThreshold`, `dryExitGap` | Per10k | — | [P]; dry share 12-18% (rev 19) |
| Climate | `climateLatticeCells`, `climateLatticeSeasons`, `dryMinSeasons` | cells / seasons | — | [P] |
| Vegetation | `dieBackDry`, `dieBackWet` | Per10k | 0.40-0.60, 0.10-0.20 | [P] (prompt 7 shape) |
| Vegetation | `rVDry`, `rVWet` | Per10k | 0.60-0.80, 0.10-0.25 | [P] |
| Vegetation | `moistureDry`, `moistureWet` (rate endpoints) | Per10k | — | [P] |
| Vegetation | `moistureFactor` breakpoints | Per10k pairs | prototype `1 + 0.8·a`, clamp 0.2-1.2 | [P] |
| Vegetation | `minMoistureFactor` | Per10k | prototype 0.2 | [P] |
| Vegetation | `vegSeed` | Per10k | — | [P] |
| Plant food | `pFrac`, `rP`, `pSeed` | Per10k | prototype 1.8, 0.8, 0.01 | [P] |
| Fauna | `rMax` | Per10k | 0.04-0.06 per season | [R: Sinclair 2003 allometry] |
| Fauna | `gMax`, `halfSat`, `herdNeed`, `maxGrazeFraction`, `condRate`, `cBreed`, `mBase`, `mDens`, `mStarve`, `cStarve`, `D`, `roam` | Per10k | prototype 1.0, 0.3, 1.0, 0.5, 0.6, 0.5, 0.02, 0.1 (≥ 0.05), 0.25, 0.4, 0.1, 2.0 | [P] |
| Fauna | `foodPerHerd` | Per10k | prototype 300 | [P] |
| Fauna | `huntShare` | Per10k | 0.2 (cap ≈ 0.01) | [P] (rev 29) |
| Foraging | `catchment` | cells | 3 | decided rev 16 |
| Foraging | `homeRange` | cells | 5 | [P] (rev 24) |
| Foraging | `campMoveMargin` | Per10k | prototype 0.1 | [P] |
| Foraging | `gameMaxReturn`, `gameHalfStock`, `plantMaxReturn`, `plantHalfStock` | Per10k | written by the calibration tool (rev 41); prototype 5.25, 0.10, 2.7, 1.5 | calibrated (revs 28, 41) |
| Foraging | `maxGatherFraction` | Per10k | prototype uncapped | [P] |
| Foraging | `labourChild`…`labourElder`, `needChild`…`needElder` | Per10k | 0.25/0.75/1/0.5; 0.6/1/1/0.8 | [P] |
| Foraging | `stashSeasons` (world setting) | Per10k | ≤ 0.5 | [P] |
| Foraging | `spoilage` | Per10k | 0.15-0.25 (prototype 0.25) | [P] (prompt 9) |
| Foraging | `yieldNoise` | Per10k | 0 | [P] |
| Foraging | `starvingSeasons` | seasons | 2 | [P] |
| Demography | `childSeasons`, `youngAdultSeasons`, `adultSeasons` | seasons | 60, 20, 100 | decided rev 32 |
| Demography | `baseMortalityChild`…`Elder` | Per10k | 0.0126, 0.0025, 0.0028, 0.0125 | [P] (rev 32; [UNCERTAIN] per-bracket averages) |
| Demography | `birthRate` | Per10k | 0.0475 per woman-season | [P] (rev 32) |
| Demography | `hungerMortalityChild`…`Elder` | Per10k | 0.25, 0.10, 0.10, 0.35 | [P] (rev 33) |
| Demography | `effortFull` | Per10k | 0.5 | [P] (rev 27) |
| Start | `startingBands`, `startingBandSize` | people / count | 2, 25 | [P] (rev 38); 15-50 [R: report 3] |
| Migration | `migrateAfter`, `searchRadius` | seasons / cells | 2, 14 | [P] (rev 34) |
| Migration | `travelCost`, `migrateMargin` | Per10k | 0.05 per cell, 0.2 | [P] (rev 34) |
| Lifecycle | `fissionAt`, `dissolveAfter`, `hostRange`, `minViable` | people / seasons / cells | 50, 3, 15, 5 | [P] (revs 25, 35) |
| Lifecycle | `fissionMargin` | Per10k | 0.2 | [P] (rev 25) |
| Events | `stableSeasons`, `causeWindow` | seasons | 2, 8 | [P] (rev 36) |
| Drought | `droughtMild`, `droughtSevere` | Per10k (anomaly) | prototype severe 0.9-1.5 | [P] |
| Drought | `droughtDefaultSeasons` | seasons | 8 | [P] |
| Snapshot | `tripGoodPct`, `tripPoorPct` | % | 100, 50 | [P] |
| Snapshot | `trendBand` | Per10k | 0.10 | [P] (rev 40) |

Derived, not config: `n_f` (§8), `maxHuntFraction` (§8), `medianKveg` (§4.1). Test scenario (not config): plateau 1,200 yr, drought radius 20, severe preset, 8 seasons (§18).

## 18. Testing plan
- Unit: each formula (clamping, stability, conservation where it applies, no NaN). Named cases: `V = 0` and ocean fauna cells; `n_f > 1` gives the same one-season totals as `n_f = 1` within rounding for small `D`; binomial at `q = 0`, `0.5`, `1` and `n = 0`; drought fade profile (full at ≤ r/2, half at 0.75r, 0 at ≥ r); single-cell drought at three moisture levels against the §7 targets.
- Property (fast-check, rev 14): every event's causes appear earlier in the log; non-`dwindled` band outcomes reach a root in ≤ 3 hops, and those within a drought + `causeWindow` reach its `drought_began`; every hunger event cites a `forage_failed`; emission order identical across two runs; same seed + commands → same state hash; populations never negative; V ≥ 0, logistic growth never takes V above K and die-back never below it; a drought never raises moisture; no dry spell shorter than `dryMinSeasons`; the glance word is a pure function of the snapshot and a starving band always reads starving; binomial sampler: exact pmf, monotone in q, never n at u = 1 − 2^-32.
- Calibration (slow, rev 41): rerun the anchor calibration on the reference seeds; fail if fresh effort on median land is outside 0.45-0.55 at the config's return constants.
- Determinism: state hash every 100 seasons, Node (Linux) vs Chrome (Windows) [R: timescale report].
- Acceptance (success test; decided rev 38): a procedural slice world, seed fixed by the rev 16 refuge check before any drought run (never chosen by outcome); 2-band start run to the density plateau (1,200 yr [P]); one severe local drought (8 seasons, radius 20 [P]) centred on the land cell nearest the centroid of living bands at that season [P]. Pass when, in [drought start, drought end + `causeWindow`], at least one `band_migrated` and one non-`dwindled` `band_died_out` each reach `drought_began` in ≤ 3 hops and both §15 sentences render; and the same seed with no drought command has neither outcome in that window. A 20-seed pass rate is reported, not a gate. Tag the test slow until keyframes exist.
- Batch checks (tuning reports, not CI gates; from the log): dry share 12-18% (rev 19); biome shares 3-50%, ≥ 5 of 20 seeds pass the refuge check (revs 16, 18); herd crash 25-75%, onset 1-3 seasons, no cell extinction (rev 30); 1-4 camp moves per band-year (rev 24); 0 dissolutions in 600 calm years on a filled map (rev 26); density 0.45-1.35/cell rising with richness, bands 25-50, hunger ≤ 3%, meat share 30-50% (revs 27-29); ≥ 18 of 20 seeds with fresh effort 0.4-0.6 on their own median land (rev 41); causeless `forage_failed` among exposed bands = 0 (rev 36); glance word share and flicker (rev 37); 20-seed acceptance pass rate and control cleanliness (rev 38).

## 19. Alternatives considered
| Topic | Options | Pick | Why |
|---|---|---|---|
| Number representation | doubles / fixed-point | doubles (rev 15) | §3 |
| Demography draws | per-member + new key field / binomial per bracket / expected value + remainder | binomial per bracket, 1 − u flip (rev 31) | same distribution, no key change; expected values erased seed variety |
| Event emission | in systems / state-diff detector / transition records + emitter | transition records + emitter (rev 17) | no actions inferred from diffs |
| Migration randomness | none / `Migration` draw | none (rev 34) | "why" stays a pure function of state |
| Migration targets | free sites only / overlap on standing stock / overlap with competitor share | competitor share (rev 34) | spacing suppressed migration; share discounts occupied land |
| Glance words | draft (restless first, trend-based) / severity-first trend-based / severity-first effort-based | effort-based (rev 37) | draft hid starving and left 99% of calm seasons wordless |
| Event causes | active climate only / lookback window + payload facts / new cause events | lookback + payload facts (rev 36) | active-only orphaned post-drought failures |
| Test scenario | hand-built fixture / filled procedural map + control / same + pass-rate gate | filled map + control (rev 38) | fixtures 0/9 without geometry tuned to the outcome; a rate gate invites tuning |

## 20. Errors, build order, rollback
**Caller-triggerable errors** (the viewer or a test harness is the caller):
- Drought command with `radius < 0`, `durationSeasons < 1`, `magnitude ≤ 0`, `sign` not ±1, or `centerCell` off-map: MUST be rejected when appended to the command log, with the field name in the error; nothing is logged or applied. A centre on a sea cell is valid (the disc reaches land).
- Config with a missing field, a non-integer, or a value outside its stated range: config load MUST fail with the field name; no world is created.
- Commands for a past tick: rejected (the command log is append-only in tick order).
- Impossible by construction (asserted, not handled): NaN or ±Infinity in state (state hash rejects them), negative bracket counts, duplicate `EntityId` on registration.

**Build order** (laptop): command log (rule 6) → entity registry → systems in §5 order, each with its unit and property tests first → anchor calibration tool and its slow test (after worldgen, vegetation, plant food and fauna exist; rev 41) → Legends templates → acceptance test (slow-tagged).

**Rollback:** no saves exist, so changing `SimConfig` changes the config-hash golden value once, with no migration. Appending `Purpose` codes 6-12 leaves the RNG golden values unchanged. After v1.0, the spec changes only through a decision-log revision and a minor version bump; the first save format freezes the config hash and content keys (no rollback after that without a save migration).

## 21. Decision trace
| Q | Topic | Settled |
|---|---|---|
| 0-7 | numbers, map, emission, worldgen, climate, drought, vegetation, fauna | revs 15-22 |
| R1-R4e | whole-system review: guilds, home range, lifecycle, host guard, regulation, anchor, hunt cap, herd target | revs 23-30 |
| 9a-9c | demography draws, brackets, hunger mortality | revs 31-33 |
| 10-14 | migration, die-out floor, events, glance words, test scenario | revs 34-38 |
| Finalize | band-card food trend | rev 40 |
| Finalize | return-anchor calibration | rev 41 |

## 22. Future consideration
| Item | Waits for |
|---|---|
| Band fusion and seasonal aggregation | prompt 12 flags fusion as the realistic end of small bands; `dwindled` is its stand-in |
| New cause events (`range_depleted`, `band_dwindling`, arrival crowding) | batch runs showing failures they would explain (rev 36) |
| Prey depression | an effect in prototypes (deferred rev 24) |
| Protein/fat budget | farming (rev 23) |
| Hidden aging stages | a system that reads true age (rev 32) |
| Glance hysteresis, a `lean` word | flicker or gap complaints in play (rev 37) |
| Seasonal guild factor ≠ 1 | a seasonality or temperature field |

## Changelog
### v0.27 - 2026-11-02
- Decided: return-anchor calibration (§9, rev 41): offline tool on reference seeds writes the return constants; slow test (§18); build order (§20). All finalize questions settled; v1.0 proposed.
### v0.26 - 2026-11-02
- Decided: band-card food trend (§16, rev 40): 4-season change in food pressure, `trendBand` 0.10 (§17).
### v0.25 - 2026-11-01
- Finalize consistency pass; no decision changed. Added: lifecycle system slot after migration (§5), state table (§5.1), plant-food regrowth rule from the prototype (§7), Purpose code table 6-12 (§2), config scale rule and full tunable table (§17), errors/build order/rollback (§20), future consideration (§22), batch-check list (§18). Fixed: §7 subtracted people's harvest from V (stale since rev 23); §7 "shortage must come from game" (stale, correction #15); fauna `need` renamed `herdNeed`; Type II return written as `maxReturn·S/(S + halfStock)` (removes the clash with substep `h`); stale `huntEff`/`huntHalf`; `stockPct` defined as plant stock vs `pFrac·Kveg` (prototype basis); property "V in [0, K]" (die-back keeps V above K); dissolution distance home-to-home. Removed: rough-draft notes and §20 rough-draft column; v0.24 food trend withdrawn pending decision.
### v0.24 - 2026-11-01
- Decided: Q14 test scenario and pass sentence (§15 templates, §18 acceptance with a no-drought control). Fixed: `stockPct` denominator is base capacity (§14).
### v0.23 - 2026-11-01
- Decided: Q13 glance words (§16). Noted: §9 food trend defect (stash upkeep).
### v0.22 - 2026-11-01
- Decided: Q12 event set and causes (§14).
### v0.21 - 2026-11-01
- Decided: Q11 die-out floor (§12): `minViable` 5; zero-labour guard on the migration share (§11).
### v0.20 - 2026-11-01
- Decided: Q10 migration (§11).
### v0.17-v0.19 - 2026-11-01
- Decided: Q9a draws (1 − u flip), Q9b brackets and base rates, Q9c hunger mortality and fertility (§10).
### v0.10-v0.16 - 2026-10-31 to 2026-11-01
- Decided: R1 guilds, R2 home range and camp, R3 lifecycle, R4a-R4e host guard, regulation, anchor, hunt cap, herd target. Fixed: v0.8 fed people V directly.
### v0.3-v0.8 - 2026-10-30
- Decided: Q2 emission, Q3 worldgen, Q4 climate, Q5 drought, Q6 vegetation, Q7 fauna. Fixed: gradient noise needs no trig.
### v0.1-v0.2 - 2026-10-30
- First draft; divide-by-zero, substep-scaling and cause-chain fixes found by the rough Gemini draft's review (`archive/design/spec-rough-draft-gemini-2026-10-30.md`).
