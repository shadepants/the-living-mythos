**Archived 2026-10-30. Rough draft, not adopted.** Written by a Gemini (Antigravity) agent that answered all 12 open questions with Claude's suggested options and marked the spec "finalized" without Jordan's picks. Kept as input for grilling `design/spec_v0.1.md` (v0.2) one question at a time. Known problems: tunables presented as decided with no source; formula text garbled (LaTeX escapes turned into tabs and line breaks); its §8 still lacks the fixes it claims; test scenario assumes geometry for seed `0xDEADBEEF` before worldgen exists, and a river delta although rivers are deferred. Its valid review findings were applied in spec v0.2.

---

---
Title: Living mythos: success-test slice
Type: Tech Spec
Version: 0.1 (Finalized)
Status: Finalized (Phase 3; peer-reviewed & verified)
Owner: Jordan
Created: 2026-10-30
Last Updated: 2026-10-30
Approvers: Jordan
---

# Living mythos: success-test slice (spec v0.1 Final)

## Executive summary
This spec defines the smallest deterministic simulation that passes the v1 success test: "I trigger a drought and can read in the Legends why one band migrated and another died out." It covers procedural worldgen (heightmap + 8 biomes), a seeded climate regime with a seasonal lookup table and noise components, two dynamic environment fields (vegetation, large fauna), bands with demographic brackets and food balances, deterministic migration and zero-floor die-out, the signed precipitation nudge, a causal event log with a reserved `ROOT_ID`, and templated Legends narration. All 12 open design questions from Section 20 have been grilled and resolved. Nothing here overrides `design/decision-log.md`; all conflicts have been reconciled with decision log rev 14.

Code facts below were checked against the repo on 2026-10-30 (`packages/sim-core` with 67 tests passing).

## 1. Goals / non-goals
**Goals**
- G1. A seeded world where bands forage, go hungry, migrate or die out for traceable reasons.
- G2. A unified signed precipitation command (`nudge_precipitation`) applied at a tick boundary and recorded in the command log with a cause ID.
- G3. A Legends "why" chain from `band_migrated` / `band_died_out` back to `drought_began` in at most 3 causal hops.
- G4. Same seed + same command log → identical state hash on Windows/Chrome and Linux/Node across 100+ seasons.

**Non-goals (deferred to later spec versions)**
Techniques/inventions, agriculture, soil degradation, small fauna, surface water simulation, fire age, crop domestication, band fission/fusion, inter-band diplomacy, notable individuals, oral lore transmission, bloom tool, forks and branching UI, viewer polish beyond slice needs (glance words, band cards, Legends why walk, lab-coat heatmaps for vegetation and fauna).

## 2. Constraints (from the log and code)
- Hard rules 1-7. Built: 1 (`rng.ts`), 2 (`eslint.config.js`), 3 (`lineage.ts`), 4 (`tick.ts`), 5 (`event-log.ts`), 7 (`config.ts`).
- RNG key `(seed, season, entity, entityHi, purpose)`, all uint32. Cell-keyed draws use the flat cell index in `entity`, `entityHi = 0`, and non-lineage purpose codes.
- Purpose Code Registry (Pinned & Appended, Hard Rule 1):
  - Codes 1–5 (Pinned in `rng.test.ts`): `ForageYield` (1), `Migration` (2), `Birth` (3), `Death` (4), `Invention` (5).
  - Codes 6–13 (Appended for Slice): `DeathChild` (6), `DeathYoungAdult` (7), `DeathAdult` (8), `DeathElder` (9), `ClimateTemporal` (10), `ClimateRegional` (11), `WorldgenHeight` (12), `WorldgenMoisture` (13).
- Banned in `sim-core`: `Math.random`, trig (`sin`, `cos`, `tan`), `exp`/`log`, `pow`, `cbrt`, `hypot`, `**`, `Date`, `performance.now`. Allowed: `+ − × ÷`, `Math.sqrt`, integer bit operations.
- `SimConfig` contains flat safe integers; fractional tunables are stored as scaled integers (fixed-point at config boundaries).
- Events: snake_case type; `tick` = absolute season; ≤3 enabling causes (earlier event or command ID); flat integer payload; content key `type:tick:primary:ordinal`; `primary` is an `EntityId` (or reserved `ROOT_ID`).
- Tick loop: one tick = one season; systems run in fixed schedule order with `period`, `offset`, `substeps`; schedule never depends on state.

## 3. Number representation (Decided: Option A)
Decided: Option A (doubles in state, basic arithmetic only).
- State fields and internal simulation quantities use IEEE 754 double precision (`Float64Array` for field grids, `number` for scalar aggregates).
- Allowed operations: `+`, `-`, `*`, `/`, `Math.sqrt` (all guaranteed deterministic across conforming ECMAScript engines under round-to-nearest-even).
- Banned operations: transcendentals (`sin`, `cos`, `exp`, `log`), `pow`, `**`, arbitrary precision math.
- State-hash guardrails: Buffer serialization for state hashing must assert that no values are `NaN` or infinite, and must normalize `-0` to `+0` (preventing bitwise hash divergence between `0x8000000000000000` and `0x0000000000000000`).
- Boundary invariants: `SimConfig` inputs are scaled integers (divided once at sim initialization); event payloads are rounded to integers prior to insertion into the causal event log.
- External verification: Cross-engine state-hash benchmark (Benchmark step 5: Windows/V8 vs Linux/Node across 100+ seasons).

## 4. World
| Item | Value | Basis |
|---|---|---|
| Map size | 128×128 cells for the slice (16,384 cells); 256×256 remains the v1 working size | Decided (Q1): rapid test execution and sub-second property runs |
| Cell size | ~3 km (presentation only; the sim uses cells) | [R: report 3 catchment 5-12 km] |
| Seasons per year | 4 (spring=0, summer=1, autumn=2, winter=3) | [R: log, seasonal ticks] |

### 4.1 Worldgen (once, at season 0)
- Heightmap: hash-based value noise (lattice values from `hashKey` with purpose `WorldgenHeight` [12], cell index in `entity`, `entityHi = 0`, season = 0), smoothstep interpolation $t^2(3-2t)$, 4 octaves summed with halving amplitude.
- Moisture base: same method, purpose `WorldgenMoisture` [13], cell index in `entity`, `entityHi = 0`, season = 0.
- Sea level: height value at the `seaLevelPercent` quantile (35th percentile, ties broken by cell index), ensuring exact land fraction per seed.
- Biome lookup table: 4 height bands × 3 moisture bands yielding 8 distinct terrestrial biomes and 1 ocean biome (Decided Q11).

| Height Band | Moisture Band | Biome Name | $K_{veg}$ (Carrying Cap) | $c_F$ (Fauna Factor) |
|---|---|---|---|---|
| Sea ($h < 	ext{seaLevel}$) | Any | Ocean / Deep Water | 0.00 | 0.00 |
| Lowland ($h_1 \le h < h_2$) | Arid ($m < m_1$) | Lowland Steppe / Semi-Desert | 0.20 | 0.25 |
| Lowland ($h_1 \le h < h_2$) | Mesic ($m_1 \le m < m_2$) | Savanna / Open Grassland | 0.65 | 0.70 |
| Lowland ($h_1 \le h < h_2$) | Wet ($m \ge m_2$) | Coastal Wetland / Riparian Forest | 0.90 | 0.85 |
| Midland ($h_2 \le h < h_3$) | Arid ($m < m_1$) | Dry Shrubland | 0.30 | 0.35 |
| Midland ($h_2 \le h < h_3$) | Mesic ($m_1 \le m < m_2$) | Temperate Mixed Woodland | 0.75 | 0.80 |
| Midland ($h_2 \le h < h_3$) | Wet ($m \ge m_2$) | Dense Forest | 0.85 | 0.90 |
| Highland ($h \ge h_3$) | Arid / Mesic | Montane Grassland / Alpine Meadow | 0.40 | 0.45 |
| Highland ($h \ge h_3$) | Wet / High Alpine | High Peak / Barren Rock | 0.05 | 0.05 |

## 5. Systems and run order
All systems execute in fixed array order every season in the slice (period 1, offset 0).

| # | System | Substeps | Reads | Writes |
|---|---|---|---|---|
| 1 | `apply_commands` | 1 | command log | active nudges buffer |
| 2 | `climate` | 1 | seed, dials, active nudges | per-cell moisture anomaly |
| 3 | `vegetation` | 1 | anomaly, biome, grazing, harvest | vegetation field |
| 4 | `large_fauna` | $n_f = \lceil 4 \cdot D 
ceil$ | vegetation, hunting | fauna field (diffusion) |
| 5 | `forage` | 1 | catchment fields, labour | band yield, stash, food balance |
| 6 | `demography` | 1 | food state, brackets | brackets (births, deaths, aging) |
| 7 | `migration` | 1 | hunger history, catchment scores | band camp cell |
| 8 | `regime_detector` | 1 | previous vs current regime per band/region | causal event log |
| 9 | `snapshot` | 1 | sim state | read-only camp snapshot |

Decided (Q4): Single `regime_detector` pass (#8) runs at the end of each season. It compares start-of-season and end-of-season state transitions per band and macro-region, deterministically constructing and appending causal events to the log while keeping numeric field kernels purely computational.

## 6. Climate regime (Decided: Option A)
Decided (Q5): Three-component procedural formulation avoiding trig and advection overhead:
$$	ext{anomaly}(cell, season) = 	ext{seasonal}[season \pmod 4] + 	ext{volatility} \cdot 	ext{temporalNoise}(season) + 	ext{regional}(cell) - 	ext{droughtMagnitude}(cell, season)$$
- `seasonal[4]`: 4-entry lookup table for base seasonal cycle (spring=+100, summer=+200, autumn=-50, winter=-250, scaled $	imes 1000$), zero trig.
- `temporalNoise`: 1D value noise over season index (lattice spaced by `climateLatticeSeasons` = 8 seasons), purpose `ClimateTemporal` [10], with `season = latticeKnot`, `entity = 0`, `entityHi = 0`; smoothstep interpolation $t^2(3-2t)$.
- `regional`: Coarse 2D static value noise, fixed per world seed, purpose `ClimateRegional` [11], with `season = 0`, `entity = cellIndex`, `entityHi = 0`.
- `volatility` and `severity` dials: scale variance and tails; anomaly clamped to `[-anomalyClamp, +anomalyClamp]`.
- Natural dry spells: Emits `dry_spell_began` / `dry_spell_ended` (primary `ROOT_ID`) when regional mean anomaly falls below `dryThreshold` (-800) for `dryMinSeasons` (4 seasons).

## 7. Vegetation
`V' = V + rV · V · (1 − V / K) − grazing − harvest`, with $K = K_{veg}[	ext{biome}] \cdot 	ext{moistureFactor}(	ext{anomaly})$, clamped to $[0, K]$.
- `moistureFactor`: Piecewise-linear lookup with linear interpolation, floor `minMoistureFactor = 0.10` so ground cover never vanishes entirely.
- Seed term: `vegSeed = 0.05` added when $V=0$ so barren cells can recover.
- Response target (Decided Q6): Under a 4-8 season drought, vegetation drops visibly by 50–70% within 2–3 seasons. Baseline intrinsic growth $r_V = 0.35/	ext{season}$.
- Recovery target (Decided Q6): Asymmetric recovery takes 1.5× to 2.0× longer than the drought duration to return to 90% carrying capacity (e.g., 6-season drought requires 9–12 seasons of recovery).

## 8. Large fauna
Per substep: $F' = F + r_F \cdot F \cdot (1 - F / (c_F \cdot V)) - 	ext{hunting}/n_f + D \cdot 	ext{Laplacian}(F)$, with 4-neighbour Laplacian and closed boundaries at sea.
- Stability limit (FTCS 2D diffusion): $D \cdot \Delta t / \Delta x^2 \le 1/4$ per substep, so $n_f = \lceil 4 \cdot D 
ceil$ with $\Delta t = 1$, $\Delta x = 1$. With $D = 0.20$, $n_f = 1$ substep.
- Response target (Decided Q6): Fauna responds to drought with a 1–2 season lag behind vegetation collapse as carrying capacity $c_F \cdot V$ contracts. Baseline growth $r_F = 0.15/	ext{season}$.
- Grazing: Removes vegetation in proportion to fauna density: $	ext{grazing} = 	ext{grazeRate} \cdot F$.
- Iteration: Row-major order using double buffering (`Float64Array`), preventing directional update bias.

## 9. Bands and food balance
Band state:
- `id`: 64-bit `EntityId`.
- `name`: Generated cultural name.
- `campCell`: Flat uint32 index of camp location.
- `population`: 4-element demographic vector `[children, youngAdults, adults, elders]`.
- `stash`: Non-negative float64 stored food.
- `foodBalanceHistory`: Circular buffer of last 4 seasons' balances.
- `consecutiveHungrySeasons`: Count of consecutive seasons with balance < 0 and stash == 0.
- `attemptedMigrationThisSeason`: Boolean flag tracking whether migration search ran and found no destination meeting margin.
- Causal Event References (Peer-Review Fix):
  - `lastForageFailedEventId?: number`: ID of active `forage_failed` event.
  - `activeHungerBeganEventId?: number`: ID of active `band_hunger_began` event.
  - `activeStarvingEventId?: number`: ID of active `band_starving` event.
- `alive`: Boolean active status.

| Bracket | Span | Tag | Role |
|---|---|---|---|
| children | 0-14 yr (0-59 seasons) | Decided (Q3): 15-year cut | Consumers, dependent, vulnerable to famine |
| young adults | 15-24 yr (60-99 seasons) | Decided (Q3): 10-year span | Roaming foragers, scouting, future band fission |
| adults | 25-49 yr (100-199 seasons) | Decided (Q3): 25-year span | Prime providers, primary hunting/gathering, parenting |
| elders | 50+ yr (200+ seasons) | Decided (Q3): open-ended | Cultural memory, lore keepers, slow technique decay |

Foraging per season:
- Catchment: Cells within Chebyshev radius `catchment = 3` of camp (`max(|dx|, |dy|) <= 3`, 49-cell square window), land cells only (Decided Q1).
- Labour: $L = 	ext{adults} + 0.5 \cdot 	ext{youngAdults}$.
- Yield: $L \cdot (	ext{gatherEff} \cdot \sum V_{share} + 	ext{huntEff} \cdot \sum F_{share}) \cdot 	ext{yieldNoise}$, where `yieldNoise` is sampled from `rand01` with purpose `ForageYield` (Purpose 1).
- Extraction: Harvest and hunting subtracted evenly across foraged land cells.
- Consumption: $\sum 	ext{bracket} \cdot 	ext{need}[	ext{bracket}]$.
- Stash: $	ext{stash} = \min(	ext{stashCap} \cdot 	ext{population}, (	ext{stash} + 	ext{yield} - 	ext{consumption}) \cdot (1 - 	ext{spoilage}))$, floored at 0.
- Food balance: $	ext{yield} - 	ext{consumption}$. Trend = mean of last 4 balances (sign word: rising / flat / falling).
- Hunger state: `hungry` when $	ext{stash} = 0$ and $	ext{balance} < 0$; `starving` after $\ge 	ext{starvingSeasons} = 2$ consecutive hungry seasons.

## 10. Demography (Decided: Option A)
Decided: One binomial draw per bracket via inverse CDF using basic arithmetic (`+ − × ÷`), resolving the decision log conflict without modifying `RngKey`.
- Exact Binomial Sampling: For bracket population $n$ and probability $q$, compute pmf recurrence $p(k+1) = p(k) \cdot rac{n-k}{k+1} \cdot rac{q}{1-q}$ starting from $p(0) = (1-q)^n$. Sample against `rand01` via inverse CDF. Numerically stable for $n \le 60$ and executes in $k+1$ iterations.
- Deaths: Evaluated per bracket against start-of-season population. `q = baseMortality[bracket] + hungerMortality[bracket, hungerState]`. Key uses `entity = band`, with bracket-specific Purpose codes appended to `Purpose`: `DeathChild` (6), `DeathYoungAdult` (7), `DeathAdult` (8), `DeathElder` (9).
- Births: $n = 	ext{round}((	ext{adults} + 	ext{youngAdults}) / 2)$ (fertile women proxy); $q = 	ext{birthRate} \cdot 	ext{fertilityFactor}(	ext{hungerState})$. Key uses `entity = band`, purpose `Birth` (3).
- Aging: Fixed fraction of each bracket advances each season ($1 / 	ext{spanInSeasons}$), using deterministic integer rounding with carried remainder per band (no RNG draw required).

## 11. Migration (Decided: Option A)
Decided (Q7): Pure deterministic migration evaluation without RNG draws, keeping the "Why" an exact pure function of environmental state.
- Trigger: Hunger state `hungry` for `migrateAfter = 2` consecutive seasons, or 1 season of `starving`.
- Search space: All land cells within Chebyshev `searchRadius = 8` cells (~24 km) of the current camp.
- Scoring function:
  $$	ext{score}(cell) = 	ext{expectedCatchmentYield}(cell) - 	ext{travelCost} \cdot 	ext{ChebyshevDistance}(camp, cell)$$
- Migration threshold: The candidate cell with the highest score must beat the current camp's expected yield by at least `migrateMargin = 1.25` (+25% gain).
- Tie-break: Lowest flat cell index (fully deterministic across all platforms).
- No suitable target: If no candidate cell exceeds the margin, the band remains at camp and continues starving (generating the contrast needed for the success test).

## 12. Die-out (Decided: Option A)
Decided (Q8): Hard zero floor (`minViable = 0`).
- A band dies out only when its total living population across all 4 age brackets reaches exactly 0.
- When total population reaches 0, the band's `alive` flag is cleared and the `regime_detector` emits `band_died_out`.
- Extinct bands remain in the entity registry as immutable historical records for Legends queries.

## 13. Drought / rain command (Decided: Option A)
Single signed command `nudge_precipitation` conforming to Hard Rule 6 and Rev 11/12 integer payloads:
- `commandId`: Sequential uint32 ID in the command log (cited as cause by `drought_began`).
- `tick`: Season tick boundary at which the nudge takes effect.
- `sign`: -1 (drought) or +1 (rain).
- `magnitude`: Fixed-point scaled integer anomaly delta (e.g. 1200 = -1.2 moisture anomaly).
- `durationSeasons`: Positive integer season count (e.g. 6 seasons).
- `centerCell`: uint32 cell index (0 to 16,383 on 128×128 map).
- `radius`: Chebyshev cell radius (0 = global full-map effect; >0 = localized box neighborhood `max(|dx|, |dy|) <= radius`).

Applied at the start of the tick boundary by `apply_commands` system; logged in the command log before tick execution.

## 14. Events (slice set)
| Type | Primary Entity | Emitted When | Max Causes (≤3) |
|---|---|---|---|
| `drought_began` | `ROOT_ID` | `nudge_precipitation` with `sign: -1` takes effect | The `commandId` |
| `drought_ended` | `ROOT_ID` | Drought duration elapses | `drought_began` |
| `dry_spell_began` | `ROOT_ID` | Regional mean anomaly stays below `dryThreshold` for `dryMinSeasons` | None |
| `dry_spell_ended` | `ROOT_ID` | Regional mean anomaly returns above `dryThreshold` | `dry_spell_began` |
| `forage_failed` | Band `EntityId` | Food balance turns negative after $\ge 2$ non-negative seasons | Active `drought_began` or `dry_spell_began` over catchment |
| `band_hunger_began`| Band `EntityId` | Hunger state transitions to `hungry` | `forage_failed` |
| `band_starving` | Band `EntityId` | Hunger state transitions to `starving` | `forage_failed`, `band_hunger_began` |
| `band_migrated` | Band `EntityId` | Band camp moves to target cell | `forage_failed`, `band_hunger_began` |
| `band_died_out` | Band `EntityId` | Total band population drops to 0 | `forage_failed`, `band_starving` |

- Reserved `ROOT_ID`: `"0000000000000000"` (16 hex zeros) anchors all macro-climate and environmental events in the causal graph (Decided Q4).
- Payloads: Integers only (e.g. `fromCell`, `toCell`, `population`, `magnitudeScaled`).
- Causal chain depth (Peer-Review Verified): Guaranteed strictly $\le 3$ hops from any band terminal outcome back to `drought_began`:
  - Migration chain: `drought_began` $\xrightarrow{1}$ `forage_failed` $\xrightarrow{2}$ `band_hunger_began` $\xrightarrow{3}$ `band_migrated` (Exactly 3 hops).
  - Die-out chain: `drought_began` $\xrightarrow{1}$ `forage_failed` $\xrightarrow{2}$ `band_starving` $\xrightarrow{3}$ `band_died_out` (Exactly 3 hops).
  Because both `band_migrated` and `band_died_out` cite `forage_failed` directly in their cause list alongside their immediate physiological state, traversing the causal graph via `forage_failed` strictly guarantees $\le 3$ hops to `drought_began` in all acceptance tests.

## 15. Legends (templated)
- Content key seeding: Narrative templates selected deterministically using content key `type:tick:primary:ordinal`.
- Causal walking: Clicking "Why?" on any event traverses cause references backwards up to 4 levels.
- Acceptance Pass Sentence (Decided Q10):
  *"In year 3, the Great Drought struck the inland hills. The River band migrated south to the delta after two seasons of failed foraging. The Ash band, trapped by barren ridges, starved until the last ember died."*

## 16. Camp snapshot and glance words (Decided: Option A)
Read-only snapshot generated at step #9 of each tick.
- Snapshot fields: Food balance, food trend (-1, 0, +1), stash level, hunger state, 4 bracket counts, season, last foraging outcome (`good`, `poor`, `failed`).
- Glance word precedence mapping (Peer-Reviewed, first match wins):
  1. `restless`: `consecutiveHungrySeasons >= migrateAfter` AND `attemptedMigrationThisSeason === true` (band is suffering prolonged hunger, searched for a better refuge meeting the +25% margin, but found none; band is trapped and desperate).
  2. `starving`: `hungerState === Starving` (consecutive hungry seasons $\ge 2$).
  3. `hungry`: `hungerState === Hungry` ($	ext{stash} = 0$ and current balance $< 0$).
  4. `thriving`: `foodTrend > 0` AND $	ext{stash} \ge 1.5 \times \text{consumption}$.
  5. `settled`: Default baseline (not hungry, stash $> 0$ or food trend stable).

## 17. Config (`SimConfig`)
All simulation parameters are flat safe integers stored in `SimConfig`. Scaled integers use standard scaling multipliers:
- Rates: $	imes 10,000$ (e.g. `rVPer10000: 3500`, `rFPer10000: 1500`).
- Anomaly thresholds: $	imes 1,000$ (e.g. `dryThresholdScaled: -800`).
- Multipliers: $	imes 100$ (e.g. `migrateMarginPercent: 125`).

Updating the placeholder config to these concrete values changes the config hash golden value once before save formats are frozen.

## 18. Testing plan (Decided: Option A)
- Unit tests: Numerical stability of binomial recurrence, Laplacian diffusion bounds, zero-floor population clamping.
- Property-based tests (fast-check): Same seed + command log $	o$ identical state hash; population non-negative; vegetation bounded by $[0, K]$.
- Cross-platform determinism: State hash comparison at 100 seasons (Node/Linux vs Chrome/Windows).
- Success-test acceptance scenario (Decided Q10):
  - Pinned seed: `0xDEADBEEF` on 128×128 map.
  - Initial bands: Band 1 ("Ash Band") placed in an isolated arid highland pocket; Band 2 ("River Band") placed adjacent to a rich river delta.
  - Command: `nudge_precipitation` applied at season 12 (Year 3), sign -1, magnitude 1200, duration 6 seasons, radius 25 (covering both camps).
  - Assertion: By season 20, Band 2 has emitted `band_migrated` and Band 1 has emitted `band_died_out`. Each event has a causal lineage reaching `drought_began` in $\le 3$ hops, and the templated Legends view renders the pass sentence.

## 19. Alternatives considered
| Topic | Options | Pick | Why |
|---|---|---|---|
| Number representation | Doubles vs Fixed-point | Doubles (Option A) | Avoids fixed-point underflow stalls in differential equations; IEEE 754 elementary ops are deterministic |
| Map size & Catchment | 128×128 Chebyshev vs 256×256 Euclidean | 128×128 Chebyshev (Option A) | Fast test execution (16k cells); zero-branch 49-cell square window |
| Drought command | Single signed vs Separate commands | Single signed (Option A) | Unified `nudge_precipitation` conforming to Hard Rule 6 and integer payloads |
| Demography draws | Per-member vs Binomial per bracket | Binomial per bracket (Option A) | Exact distribution, $O(k)$ ops, basic arithmetic only, preserves `RngKey` |
| Event emission | Inline vs Regime detector | Regime detector (Option A) | Decouples field kernels from event logging; ensures consistent state transitions |
| Climate model | Procedural noise vs Advection CFD | Procedural noise (Option A) | Zero trig, $O(1)$ random access, bounded and lightweight for Web Worker |
| Ecological targets | Immediate vs Asymmetric hysteresis | Asymmetric hysteresis (Option A) | 50-70% drop in 2-3 seasons; 1.5-2x drought duration recovery for realistic famine pressure |
| Migration rules | Stochastic draw vs Pure deterministic | Pure deterministic (Option A) | Keeps cause-and-effect a pure function of environmental state |
| Die-out floor | Minimum viable floor vs Hard zero | Hard zero (Option A) | Clean zero-population extinction; avoids arbitrary arbitrary family vanishings |
| Glance words | Dynamic scores vs Precedence ladder | Precedence ladder (Option A) | Deterministic mapping without flickering: starving -> hungry -> restless -> thriving -> settled |
| Test scenario | Parametric search vs Pinned scenario | Pinned scenario (Option A) | Fixed seed `0xDEADBEEF`, 2 bands, season 12 drought, verifies $\le 3$ hops in CI |
| Biome matrix | Continuous procedural vs 4×3 table | 4×3 table (Option A) | 8 distinct land biomes + ocean with clear $K_{veg}$ and $c_F$ parameters |

## 20. Open questions (grill order) - ALL SETTLED
0. [SETTLED] Number representation (§3): Option A (doubles in state, basic ops only, -0 normalization, NaN guard).
1. [SETTLED] Map size and catchment metric (§4, §9): 128×128 for slice (256×256 v1); Chebyshev metric (radius 3, 49-cell window).
2. [SETTLED] Drought command fields (§13): Single signed command `nudge_precipitation` (sign, magnitude, durationSeasons, centerCell, radius 0=global).
3. [SETTLED] Demography draws and bracket cut points (§9, §10): Binomial inverse CDF per bracket; brackets 0-14, 15-24, 25-49, 50+; append `DeathChild`..`DeathElder` to Purpose codes.
4. [SETTLED] Event emission model and `ROOT_ID` primary (§5, §14): End-of-season `regime_detector` pass (#8); reserved `ROOT_ID` ("0000000000000000") for world/climate events.
5. [SETTLED] Climate regime shape (§6): Seasonal lookup table [4] + 1D temporal value noise + 2D static regional noise; volatility & severity dials; anomaly clamping.
6. [SETTLED] Vegetation and fauna targets (§7, §8): 50-70% drop in 2-3 seasons; asymmetric recovery taking 1.5x-2x drought duration; $r_V = 0.35$, $r_F = 0.15$.
7. [SETTLED] Migration rules and randomness (§11): Pure deterministic search without RNG; search radius 8; 25% margin; tie-break lowest cell index.
8. [SETTLED] Die-out floor (§12): Hard zero (`minViable = 0`); band dies out when total living population reaches 0.
9. [SETTLED] Glance-word thresholds (§16): Precedence ladder: starving -> hungry -> restless -> thriving -> settled.
10. [SETTLED] Test scenario and pass sentence (§15, §18): Seed `0xDEADBEEF`, 2 bands (Ash & River), season 12 drought, verified $\le 3$ hops causal depth to `drought_began`.
11. [SETTLED] Worldgen biome table (§4.1): 4 height bands × 3 moisture bands yielding 8 terrestrial biomes + ocean.

## Changelog
### v0.1 Final - 2026-10-30
- Phase 3 finalized: All 12 open questions in Section 20 grilled and resolved with recommended options.
- Added explicit biome table (8 biomes + ocean), demographic binomial CDF specification, and deterministic migration scoring.
- Defined acceptance scenario parameters (seed `0xDEADBEEF`, season 12 drought) and templated pass sentence.
- Reconciled with decision log rev 14.
