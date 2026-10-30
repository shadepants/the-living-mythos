# Batch review: Gemini reports 2-5 + open-source repos

**Archived 2026-10-28** (moved from `research/`). Kept as the spot-check evidence behind several decisions. Status of its proposals:
- Section 5 edits were adopted into the decision log (rev 4-8), with changes: the climate row became a world-seeded regime, not an Earth-style curve with CO2 (rev 4); the fork-vocabulary row was not adopted (forks are now a v1 stretch goal, rev 9). Prompt 5's ideas wait until forks are worked on.
- Outdated statements below: "Our v1 has no climate system" (it now has a seeded climate regime); section 4's watchability question (superseded by the procedural world with time from year 0, rev 4).
- Still open: property norm (deferred, see decision log).

Reviewed 2026-10-23. Covers the five PDFs uploaded to the Project.

## 1. What each file is

| File | Prompt | Verdict |
|---|---|---|
| `World and History Simulation Architecture.pdf` | 2 (internals of closest matches) | Useful; mostly confirms existing decisions. One recommendation conflicts with decision (a) |
| `Prehistoric Observational Simulation Design.pdf` | 3 (grounding in prehistory) | Most valuable, also most flawed. Use its ranges and sources; do not use its update equations as written |
| `Procedural History Narration Pipeline.pdf` | 4 (narration) | Strong; adopt the pipeline shape with two fixes |
| `Comparative Simulation Visualization Framework.pdf` | 5 (fork comparison) | Good vocabulary for Q5; misses that a deterministic chaotic sim needs a noise envelope |
| `Open Source Repositories for Civilization Simulati....pdf` | Extra (not in gemini-prompts.md) | Mixed; several picks are wrong for this project |

**Independence caveat (inference):** all five reports were written by the same tool from the same context block I wrote. Their agreement with our decisions is partly an echo of that context, not independent confirmation. Treat convergence as weak evidence.

## 2. Spot-checks

| Claim | Result | How |
|---|---|---|
| EMBERS model (2025) exists and drives skill-loss numbers | **Partly false.** EMBERS is real (Arinyo i Prats, Sandgathe, Riede, Collard; Open Research Europe 5:205, 2025). But the report's "EMBERS" decay 0.01-0.08/yr and practice gain 0.05-0.20/bout are not in the paper. EMBERS uses exponential decay with forgetting time τ = 1-16 years (rate 1/τ = 0.06-1.0/yr) and finds use-interval variability is the strongest driver of loss and expert numbers the weakest | Read the paper (PMC12775662) |
| Report 3's mortality defaults reproduce its own life table | **False.** μ_child = 0.08/yr gives l15 = 0.29, not the 0.57 it cites. l15 = 0.57 needs μ ≈ 0.0375/yr | Computed |
| Report 3's birth rule matches TFR 4.5-6 | **False.** One birth per 3.5 yr for every woman 15-49 gives ~8 lifetime births. With its own mortality: r ≈ +0.5%/yr, not ≈ 0 | Computed |
| Report 3's domestication rule takes ~2,500 years | **False.** Its formula dx = s(1-x) reaches 0.75 in ~534 years at s = 0.0025. A logistic selection form takes ~1,600 | Computed |
| Henrich 2004 Tasmania equation and Vaesen et al. critique | Consistent with what I know; not re-fetched | Knowledge |
| Gurven & Kaplan 2007: modal adult age at death ~72 (68-78) | Consistent with the paper's known abstract | Search |
| siftystudio/viv exists, TS runtime `@siftystudio/viv-runtime` | **True**, but **source-available, non-commercial only**; open beta 0.x; solo project | GitHub page |
| mkremins/winnow reusable | JS with bundled DataScript 0.18.4; **no license shown**, so code can't be reused. Ideas can | GitHub page |
| ShiJbey/neighborly by "Kolby Webre" | **Wrong author.** It's Shi Johnson-Bey (CoG 2022), Python | Search |
| gitgraph.js recommended | Report's own citation marks it **[ARCHIVED]** | Report citation |
| Victoria 3 Dev Diary #76 modifier DAG; Songs of Syx 1M-ancestor family tree in 6 MB; WorldBox lineage pruning | Unverified. Low stakes | - |
| bioRxiv DOI `10.64898/...` in report 5 | Suspicious: bioRxiv DOIs use `10.1101`. Irrelevant to any decision | Pattern check |

## 3. Findings by report

### Report 3: prehistory (prompt 3)
Useful:
- Parameter ranges with sources: band 15-50 (25), mating network 175-500, fertility, mortality, biome densities, return rates, fire mosaic effects, domestication duration 1,500-4,000 years, reversibility (Late Natufian, Fremont).
- Diet-breadth model is the right mechanism for the farming shift: grain enters the diet when large-game encounter rates fall. This argues for **splitting fauna into large and small** fields.
- Catchment 5-12 km (8 km) supports our 3-5 cell catchment if a cell is ~3 km. That pins the **working cell size at ~3 km**.
- Watchability: deep Upper Paleolithic is mostly static for 5,000-11,000-year stretches, punctuated by Dansgaard-Oeschger shifts every 1,000-2,000 years. The 16,000-8,000 BP window holds most of the drama.
- Agriculture needs Holocene stability and CO2 (Richerson, Boyd, Bettinger). **Our v1 has no climate system, so the crucible bias has no trigger.**

Wrong or risky:
- Update equations don't reproduce its own tables (section 2). Use ranges; calibrate by batch runs.
- Technique emergence is hard threshold gates (cultivation needs sedentism + grain > 0.6 + storage > 0.5 + property > 0.5). That's 3-4 prerequisites and a hard gate: **conflicts with "max 1-2 prerequisites" and "crucibles are a bias, not a gate"**.
- Uses ln, exp and Gumbel draws: banned in sim-core by hard rule 2. Henrich's N* can be a precomputed config constant.
- Inbreeding rule (network < 175 → child mortality +100%) has no cited magnitude. Tunable at most. [UNCERTAIN]
- Adaptive "epoch mode" pacing at 100-500 ticks/s: fine as playback speed (already decided), not as simulation compression (rejected).

### Report 2: architecture (prompt 2)
- Confirms group-level aggregation, SoA typed arrays, zero allocation in hot loops, DF-style event collections, lineage IDs, and a worker/main split with WebGL rendering.
- Victoria 3 pop fragmentation: our 4-bracket bands avoid it as long as culture/technique stay band attributes, not population splits.
- **Conflict:** it recommends promoting events to the permanent log only if salience passes a threshold. Our decision (a) is "emit only at regime thresholds". Salience depends on run-wide base rates, so it differs between forks and would make fork logs non-comparable. Salience must stay in the narration layer.
- RimWorld storyteller (inject incidents to keep drama) **conflicts with "never tune the sim for drama"**. Reject it inside the sim. Fine as a presentation-side "suggest a nudge" prompt for the viewer.
- Its sample `Band` interface (string name, Map, number[]) contradicts its own zero-allocation advice. Ignore the sample.

### Report 4: narration (prompt 4)
Adopt the pipeline: regime events with ≤3 causes → DF-style collections → incremental sifting patterns → salience + quiet-epoch compression → first_valid conditional templates with a seeded lexical grammar → optional closed-world LLM realizer later.

Fixes:
- **Seed narration by a content key, not `event.id`.** Sequential IDs diverge after a fork, so the same event would read differently in two branches. Use (type, tick, primary lineage ID).
- "Halpern-Pearl" is overclaimed: it implements transitive reduction, which can delete a genuine second cause. With ≤3 causes recorded at source, show recorded causes; use reduction only for long ancestor chains.
- Its event schema uses `Record<string, number>` metadata and unbounded `causeIds`. Use fixed fields and ≤3 causes (SoA store).
- Salience uses log2: fine, it lives outside sim-core.

### Report 5: fork comparison (prompt 5)
Useful:
- Four regimes instead of two: **absorbed, fading, offset (new stable state), ripple**. Good seed for Q5.
- Lead with an explicit divergence curve and badge, then drill down to maps. Split-slider wipe and difference heatmap for maps.
- Distinguish migration from loss: band moved 5 cells ≠ band died. Sliced Wasserstein is one way; matching bands by lineage ID is cheaper for us (hard rule 3).
- Event-log divergence needs events matched across forks: again a content key.

Missing (inference, consequential):
- In a deterministic system, divergence from a real nudge rarely returns to exactly zero once integer populations differ, and chaotic amplification can make almost every nudge eventually "ripple". Fixed thresholds (0.05, 0.50) would then always say ripple. **Ripple must be judged against a null envelope**, e.g. K micro-nudges or seed-jittered runs (the report's own functional-boxplot idea). Cost: K extra runs per comparison. External check: once the sim exists, run 20 micro-nudges and look at the spread.

### Extra: open-source repos
| Repo | Use? | Why |
|---|---|---|
| Viv | Reference only | Non-commercial license; beta. Read its sifting design |
| Winnow | Reimplement ideas | No license; `unless between` + staged patterns are the useful part |
| Tracery | Maybe, or write our own ~200-line grammar | Tiny; old but stable [UNCERTAIN: maintenance] |
| compromise | No | Templates handle tense; NLP post-processing is overkill |
| dual-mesh / Voronoi | No | Square grid is decided; not reopening |
| tectonics.js / GLSL fields | **No** | GPU float results vary by driver: breaks determinism. Fields stay on CPU in sim-core |
| bitECS + SharedArrayBuffer | Still "only if needed" | SAB needs cross-origin isolation headers; run-ahead playback reads history, not live state |
| Trrack | No | Tracks UI state as JSON; our forks are keyframes + command log |
| elkjs | Later, maybe | Causal graph layout in a worker; only if chains get long |
| gitgraph.js | No | Archived |
| DFHack df-structures | Reference | Event and collection model |

## 4. Watchability: the open question this batch was meant to settle
Report 3 recommends simulating 16,000-8,000 BP (32,000 ticks) instead of 30,000 years (120,000 ticks). Grilled separately; see the handoff.

## 5. Proposed decision-log edits (adopted with changes; see archive note at top)

Add to Decisions table:
| Area | Decision | Basis |
|---|---|---|
| Environment fields (revised) | Fields: vegetation, soil, **large fauna, small fauna**, water, **fire age** (fire risk derived from fire age + vegetation), **crop domestication**. Elevation static | Report 3: diet-breadth shift needs separate large/small game; fire mosaic needs time since burn |
| Climate forcing | Exogenous, deterministic climate curve (temperature/moisture anomaly + CO2 scalar per season) stored as versioned config data. Not a climate simulation. Drought nudges layer on top | Report 3: farming needs Holocene stability; crucible bias needs a trigger |
| Cell size | Working assumption ~3 km per cell (catchment 3 cells ≈ 9 km). 256×256 ≈ 770 km square ≈ 350-2,800 bands at forager densities | Report 3 catchment 5-12 km; computed |
| Technique model (refined) | Integer level (0-3) plus a progress accumulator. Decay as forgetting time τ in years, driven by use intervals; elders lengthen τ. Report 3's 0.03/0.08 decay defaults rejected as unsupported | EMBERS (verified): τ 1-16 yr; use variability dominates |
| Demography calibration | Use report 3 ranges as calibration targets (l15 ≈ 0.57, TFR 4.5-6, long-run r ≈ 0 through crashes), not its equations. Births/deaths via per-member hash draws (bands ≤ ~50, so cheap; no exp/log) | Section 2 arithmetic; hard rules 1-2 |
| Event identity | Each event has a content key (type, tick, primary lineage ID). Sequential IDs are local to a run. Fork matching and narration seeding use the content key | Reports 4-5; hard rule 3 |
| Salience | Salience is computed in the narration layer and never decides what the sim logs | Resolves report 2 vs decision (a) |
| Narration pipeline | Collections → incremental sifting patterns → salience + quiet-epoch compression → first_valid conditional templates + seeded lexical grammar. LLM later, closed-world packets only | Report 4 |
| Fork vocabulary (Q5 seed, extends existing row) | Regimes: absorbed / fading / offset / ripple, judged against a null envelope from micro-nudges | Report 5 + review |

Add to Rejected:
- Drama director inside the sim (RimWorld storyteller). Presentation-side nudge suggestions are fine
- Salience-gated logging
- Hard-gated technique emergence thresholds (report 3); use bias weights with ≤2 prerequisites
- GPU-computed simulation fields
- Voronoi mesh (dual-mesh), compromise, Trrack, gitgraph.js
- Reusing Winnow code (no license); Viv as a dependency (non-commercial license)

Open, not proposed yet:
- Property norm (Bowles & Choi) as a band attribute: needed for farming, or does the crucible bias suffice? Lean: defer until a batch run shows farming needs it.
