# Deterministic Deep-Time Simulation in the Browser: Seasonal Ticks, Run-Ahead Playback, and Fork-Safe Time Compression

Research report, 2026-10-23 (Claude research task). Question: how to simulate tens of thousands of years at seasonal resolution, deterministically, in a browser, at a watchable pace.

---

Keep the seasonal tick as the only clock inside the simulation, and do all time compression on the viewing side. The best way to do that is a run-ahead history buffer: the worker simulates every season at full speed, ahead of what the viewer is watching. The viewer then plays the recorded history back at a speed chosen from the causal event log. Two things help make this affordable: a fixed (not state-dependent) multi-rate update schedule for the expensive parts, and coarse grids during the Paleolithic. State-adaptive tricks such as quiescence skipping, switching between agent-based and equation-based models, and coarse projective integration all break fork comparability unless you add extra machinery, so keep them out of the v1 core.

## TL;DR

- **Your current candidate is right, with one upgrade.** Make era-dependent speed a playback feature, not a simulation feature. Also decouple how far the simulation has run from what the viewer is watching: the worker runs ahead and records, and the renderer plays back. Skipping quiet periods then becomes a decision made over the recorded log, which cannot fake divergence between forks.
- **Throughput looks achievable, but measure it.** Published figures put plain JavaScript on a Float32Array at roughly 0.6 ms for one 512×512 diffusion step on a recent laptop-class chip. A 120,000-tick Paleolithic run with five fields and a few substeps is therefore within reach on a 4-core laptop, provided the grids stay coarse and slow fields run on a fixed, slower schedule. This is an inference, and the first benchmark should be on the i7-8665U itself.
- **Avoid anything whose timestep or fidelity depends on simulation state.** That covers quiescence detection, event-queue time advance, hybrid switching between agent-based and equation-based models, and projective integration. If one is needed later, the fork pair must share a single fidelity schedule (the union of both branches' detailed periods). Hash-based random draws must be keyed on absolute season index, not on tick count.

## Key Findings

### Verified facts (with sources and dates)

**Games**

- **Dwarf Fortress** separates a fast, coarse history phase from a detailed play phase, and both use the same event data structures. In a March 14, 2023 interview with Game Developer, Tarn Adams said: "All the data structures for historical events are the same between all the modes, though some modes have more details than others." He also said world generation "is based on a seed, so you could run one world out to 110 years, say, and the same world out to 100 and play the last ten years yourself… You'd end up with two 110-year worlds with near identical histories, but the last ten would diverge." In a Game Rant interview at the Steam release, he said world generation "has to crank a year every two seconds if it can, even when 20,000 people are running around." His general optimization advice in the same Game Developer piece: "all sorts of things can be skipped, delayed, or otherwise scheduled… Think about how often you actually need to do something and try to do it only that much."
- **Dwarf Fortress fortress mode uses fixed multi-rate scheduling.** In a separate Game Developer Q&A, Adams described it: every ten ticks the seasons and weather advance; every fifty ticks, staggered, taverns, temples and libraries update; every hundred ticks items rot; every thousand ticks deleted objects are freed; vegetation advances every tick with "staggers and flags."
- **Victoria 3 (Paradox)** uses tick categories. Dev Diary #76 states: "On Victoria 3 we have yearly, monthly, weekly, daily, and (regular) ticks." It also states that "In CK3 and EU4 a tick is a single day, while on HOI4 it's just one hour. For Victoria 3 a tick is six hours." The same diary says "many of our most expensive tick tasks are run on a weekly basis" and that a weekly tick "also includes all daily and tickly tick tasks." It names the employment update as the single most expensive item, followed by the pop need cache update and the modifier update. A Paradox forum thread notes that a 100-year Victoria 3 campaign at four ticks per day is about 146,000 ticks. That is the same order of magnitude as your Paleolithic run.
- **Civilization changes years per turn by era, on a fixed calendar.** Civilization VI at Standard speed runs 40 years per turn from 4000 BC, then 25, 20, 10, 5, 2, 1, and finally half a year per turn from 2020 AD (Civilization Wiki). Civilization III uses 540 turns: 50 years per turn from 4000 BC down to 1 year per turn from 1950 to 2050 (CivFanatics, Apolyton).
- **RimWorld 1.6 added distance-based variable tick rates.** Pawns out of camera view update needs, health and similar systems less often. The author of the Steam Workshop mod "Performance - Slower Pawn Tick Rate" reports that some vanilla jobs "happen slower to pawns offscreen," naming "the snow and sand clearing, repairing mechs, and beating out fires." The author also says the "vanilla game uses variable tick rate up to 15x." In other words, variable-rate updates created behavioral differences even in a shipped commercial game.
- **Caves of Qud skips simulation altogether for deep history.** Jason Grinblat's GDC 2018 talk describes how he "avoided building a full historical simulation by generating historical events and rationalizing them after the fact." The FDG 2017 paper by Grinblat and Bucklew describes a state machine plus replacement grammar for sultan biographies.

**Academic models**

- **Artificial Anasazi / Long House Valley** runs "from 800 to 1350 in annual time steps." Janssen (JASSS, 2009) found that the code uses an annual step while the paper describes a monthly storage-consumption clock: "A second clock runs from April to April and reduces the amount of maize in storage by 13.33 kg of maize per month." Sub-annual processes were folded into an annual step.
- **Village Ecodynamics Project** households interact "with annually changing virtual natural and social environments in Southwest Colorado between A.D. 600… and A.D. 1300" (AAAS 2011 abstract). That is about 700 annual steps.
- **HANDY** (Motesharrei et al., Ecological Economics 101, 2014) is a four-equation ODE model (Elites, Commoners, Nature, Wealth). "All the simulations below use the Euler integration method with a time-step of 1 year and single precision."
- **Multi-millennial dispersal models use much coarser steps.**
  - In the SteppingOut model (Mithen and Reed 2002), "each step represents 250 years" (Romanowska review, 2015).
  - Fort's Neolithic spread models step by generation. Isern, Fort et al. (PNAS 2017) use "one generation, for which we use the realistic value of 32 y" per iteration. Fort et al. (Nature Communications 2024) run "T=32 yr… for t = 200 iterations."
  - A Science Advances study simulated "1600 generations" of 25 years from roughly 40,000 BP.
  - The GLUES Neolithic simulator (Lemmen 2009, PANGAEA) covers 685 land regions from 9500 to 2000 BC. Its "data are presented as 50-year averages," which describes output averaging and not necessarily the integration step.
  - LaPolice, Williams and Huber (Nature Communications, Aug 25, 2025) solve a 1D reaction-diffusion model over 100 generations of 25 years. Their 2D agent-based model, though, uses "annual timesteps and… overlapping generations." That is a recent precedent for annual steps in a multi-millennial agent-based model.
- **Switching between agent-based and equation-based models has precedent in epidemiology.** Bobashev, Goedecke, Yu and Epstein (2007) "introduce a hybrid model that starts as agent-based and switches to equation-based after the number of infected individuals is large enough." Hunter and Mac Namee (JASSS 23(4), 2020) switch at 10% or 20% infected and found that results "move farther from the equation-based disease component model as the switch increases." The switch threshold measurably changes the outcomes.
- **Equation-free coarse projective integration** (Kevrekidis, Gear, Samaey; Scholarpedia) runs short bursts of the fine model, estimates coarse time derivatives, and projects forward. It "is especially suited for problems with a large gap in their eigenvalue spectrum."
- **Discrete-event versus time-stepped.** Buss and Al Rowaei (Winter Simulation Conference 2010) found that large fixed time steps run fast but can be "seriously flawed," and that next-event time advance is more accurate. Their point is that time-step size is itself a modeling decision.

**Engineering facts**

- **ECMAScript leaves Math.sin, cos, exp, pow, log, atan2 and similar functions "implementation-approximated"** (MDN: "different browsers can give a different result. Even the same JavaScript engine on a different OS or architecture can give different results"). Projects that need lockstep determinism, such as the OpenFrontIO PR #5817, ban these functions from simulation code. Basic arithmetic and Math.sqrt are exactly specified by IEEE 754.
- **SharedArrayBuffer requires cross-origin isolation** via the headers `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp` (web.dev guide).
- **Counter-based RNGs** (Salmon et al., SC'11, "Parallel Random Numbers: As Easy as 1, 2, 3") compute the nth random number "directly by some function, b, applied to n." This is the formal version of your (seed, tick, entity, purpose) hashing, and it parallelizes without synchronization.
- **WebAssembly is not automatically faster.** Jangda et al. (USENIX ATC 2019) measured WebAssembly at a median 1.53× (Chrome) and 1.54× (Firefox) slower than native on SPEC CPU, with auto-vectorization disabled. Surma (surma.dev) found an idiomatic WebAssembly port that was still not faster than optimized JavaScript.

### Throughput datapoints (from the targeted subagent search; mostly informal sources)

- **Heat diffusion on a 512×512 F32 grid.** A GitHub issue on the Bend language repository (bendlang/bend #1352, Oct 5, 2026; Apple M2 Pro, Node 26.5) reports that "the same kernel written as a plain loop takes 22 ms in C (clang -O3) and 60 ms in JS over a Float32Array" for 100 steps. That is about 0.6 ms per step, or roughly 4.4×10⁸ cell-updates per second in JavaScript, about 2.7× slower than C. This is an anecdotal source, Node rather than Chrome (both run V8), and Apple silicon rather than your Intel chip.
- **Game of Life, 2560×1440.** A GitHub README (Jumbub/game-of-life-js; i5-7600K desktop) reports 0.34 ns per cell average in JavaScript, about 1.3 ms per generation. This number is flattered by skip optimizations and workers.
- **WebAssembly SIMD gains are mixed.** The V8 team blog (2020, updated 2022) reports a demo going from 14–15 FPS to 38–40 FPS with SIMD "on a modern laptop." The TensorFlow.js blog (Sept 2, 2020) reports "SIMD brings a 1.7-4.5X performance improvement to plain Wasm, and multithreading brings another 1.8-2.9X." A 2025 ASRJETS paper (low-tier journal, hardware unspecified) found plain JavaScript beating WebAssembly on 3×3 to 9×9 blur kernels (8.14 ms vs 12.02 ms for 3×3). Blocked SIMD WebAssembly beat JavaScript by only 1.64× on 1024² matrix multiply. No stencil-specific SIMD benchmark was found.
- **Worker transfer cost.** Transferring an ArrayBuffer is "extremely fast and independent of the size of the ArrayBuffer" (Surma, 2019). Copying is proportional to size: a 2011 Chrome blog measured 302 ms to clone a 32 MB buffer round trip, versus 6.6 ms when transferred.

### Inference: the arithmetic for your laptop

The i7-8665U is a 15 W-class mobile chip and will throttle under sustained load. Assume it is about 1.5–2.5× slower per core than an M2 Pro on this kind of kernel. That puts a 512×512 diffusion pass at roughly 1–1.5 ms, and a 256×256 pass at roughly 0.25–0.4 ms. With five fields and four substeps per season (20 passes):

- **At 256×256:** roughly 5–8 ms per season for fields. That is about 125–200 seasons per second before group logic.
- **At 512×512:** roughly 20–30 ms per season, or about 33–50 seasons per second.

A 30,000-year Paleolithic run is 120,000 ticks. The 256×256 case is comfortably faster than any plausible playback rate. The 512×512 case is borderline unless slow fields move to a slower fixed schedule. Thousands of groups with four age brackets are cheap next to the grid work if they are stored in structure-of-arrays typed arrays. These are estimates to verify, not measurements.

## Comparison of Candidate Approaches

| # | Approach | How it works | Determinism / fork safety | Effect on seasonal fidelity | Implementation complexity | Performance gain | Precedent |
|---|---|---|---|---|---|---|---|
| 1 | Fixed seasonal tick + playback speed (your candidate) | Sim always steps one season; renderer fast-forwards quiet stretches | Fully safe; skipping is a viewing choice | Full | Low | None in sim; viewing compresses | DF worldgen vs. play; RimWorld/ONI speed controls |
| 2 | Run-ahead history buffer (recommended extension of 1) | Worker simulates ahead and records state deltas and events; viewer plays back with log-driven pacing | Fully safe; pacing is computed from the recorded log after the fact | Full | Low–medium (ring buffer, keyframes) | Decouples sim cost from watch speed; quiet eras can be shown at 1000× | DF: worldgen runs, then Legends browses the recorded history |
| 3 | Static multi-rate scheduling | Each subsystem has a fixed period (e.g., fire per season, soil per year, relations per year), staggered by entity hash | Safe if periods depend only on tick index and config, never on state | Season-sensitive systems keep full rate; slow systems coarsen | Low–medium | Large on slow fields (soil, slow vegetation) | DF (10/50/100/1000-tick cadences); Victoria 3 (yearly/monthly/weekly/daily ticks) |
| 4 | Calendar-scheduled era timestep | Tick length set by calendar (e.g., annual ticks before 15,000 BP, seasonal after) with seasons folded in analytically | Safe if the schedule is config, not state; both forks share it | Lost as discrete events in coarse eras; kept as averages | Medium (two code paths per process) | ~4× in coarse eras | Civilization years-per-turn tables; Artificial Anasazi's annual step with a monthly consumption clock inside |
| 5 | Level of detail by observer attention | Detail only where the camera is; coarse elsewhere | Breaks determinism unless camera-independent; RimWorld's variant changed behavior | Varies by place | Medium | Large | RimWorld 1.6 distance-based tick rates |
| 6 | State-adaptive quiescence skipping / event-queue time advance | Detect steady state or schedule next events; jump time | Unsafe by default: a nudge changes what is "quiet," so the forks skip differently and fake divergence | Breaks on skipped seasons unless replayed analytically | High | Potentially very large | Discrete-event simulation literature (Buss and Al Rowaei 2010) |
| 7 | Hybrid agent-based ↔ equation-based switching | Run groups as ODE aggregates in quiet periods, switch to groups when thresholds trip | Unsafe by default; switch timing changes outcomes (Hunter and Mac Namee 2020) | ODE phase loses discrete winter famines and notable records | High (bidirectional lift/restrict) | Large | Bobashev et al. 2007; HANDY as the ODE template |
| 8 | Equation-free coarse projective integration | Short fine bursts, estimate coarse derivative, project ahead | Deterministic but fragile; projection uses floats and fitted rates; forks must share burst schedule | Discards seasonal detail in projected spans | Very high | Large only with clear timescale separation | Kevrekidis/Gear/Samaey; patch dynamics for spatial agent-based models (arXiv 1404.7199) |
| 9 | Generate-then-rationalize prehistory | Don't simulate deep time; generate a plausible backstory and start the sim later | Safe (seeded), but forks cannot reach into the generated prehistory | None before the sim start | Low–medium | Total for the skipped span | Caves of Qud sultans; your fallback of a later start |

## Details: Deep Dives on the Three Most Promising Approaches

### 1. Run-ahead history buffer (sim time decoupled from watch time)

**How it works.** The Web Worker advances the authoritative seasonal simulation as fast as it can. Each tick it emits two things to a history store: compact state deltas, with periodic full keyframes of the field grids and group arrays, and the causal events produced that tick. The renderer holds its own playhead into that store. A pacing function reads the event log ahead of the playhead and sets playback speed. For example, it might slow to one season per second when an event of narrative weight at or above some threshold is within N seasons, and otherwise cruise at hundreds of seasons per second. The viewer can never overtake the sim frontier. When the frontier is close, the pacer degrades gracefully toward real-time.

**Why it fits your constraints.**
- **Determinism.** The sim never knows how fast anyone is watching. This is the same separation Dwarf Fortress has between world generation and Legends: history is computed, then browsed.
- **Forks.** Snapshot at season S, run branch A (no nudge) and branch B (drought) as independent seasonal sims, and diff the logs and states season by season. Because neither branch skips anything, every difference is real. Pacing for a fork comparison can use the union of both logs' salient events, so the viewer slows wherever either history does something notable.
- **Causal event log.** The pacer is the log's first consumer, so log quality directly drives the viewing experience. That is a useful design pressure.
- **Field substeps.** These are unchanged. The fixed internal substeps run every season.

**Integration specifics (inference).**
- Store field keyframes every K seasons as quantized Uint16 snapshots. Store groups as structure-of-arrays snapshots.
- Rendering at a playhead between keyframes either replays deltas or, more cheaply, shows the nearest keyframe for fields (fields change slowly at fast-forward speeds) and exact group state from the deltas.
- Transfer finished buffers to the main thread as transferables rather than copying them.
- Memory is the constraint to watch. 120,000 seasons of full grids is infeasible, so grids must be keyframed sparsely, while the event log is kept in full.

### 2. Static multi-rate scheduling (operator splitting by timescale, fixed by config)

**How it works.** Split the per-tick update into operators, each with a declared period and phase:
- Fire and fauna movement: every season.
- Vegetation growth: every season, but at a coarser grid.
- Soil formation and water table: once a year, at a fixed season.
- Inter-band relations decay: once a year.
- Technique drift: once a year, staggered so that hash(entity) mod 4 picks the season, which spreads load.

An operator that runs every n seasons integrates n seasons' worth of change. It does so either by running its own stable substeps (diffusion substeps must still respect the explicit stability limit for the larger interval) or by using a closed form where one exists, such as exponential relaxation.

**Why it is fork-safe.** The schedule depends only on (tick index, entity id, config), never on state, so both branches of a fork execute exactly the same operator calls. This is the Dwarf Fortress and Paradox pattern: DF's 10/50/100/1000-tick cadences and Victoria 3's yearly, monthly, weekly and daily categories.

**Seasonal fidelity.** Keep every process that carries a seasonal meaning at the full rate: winter food stress, migration timing, harvest. Only slow state is coarsened. Your premise holds: seasons stay "real" where they matter.

**Caveats.**
- Running a diffusion operator yearly instead of seasonally does not remove the stability limit. The operator needs 4× the substeps, or an implicit or analytic solve, so the gain comes from fields that barely diffuse, not from the diffusive ones.
- Closed-form decay needs exp(). Because Math.exp is implementation-approximated, use your own deterministic exp (a polynomial or table built from basic arithmetic), or precompute per-period decay factors once from config.

### 3. Calendar-scheduled era timestep (the fallback if benchmarks fail)

**How it works.** Before some configured date, for example the start of the Late Glacial, the sim steps annually. Inside each annual step, the four seasons run as a cheap, deterministic sub-model on group-level aggregates: lean-season food balance, a migration decision, and an annual mortality draw per age bracket. The full field grid updates once a year with appropriate substeps. After the configured date, seasonal ticking resumes. The Artificial Anasazi precedent is exact: an annual step that folds in a monthly maize-consumption clock.

**Fork safety.** Safe if the switch date is configuration and identical in both branches. Never make the switch state-triggered, for example "switch to seasonal when the first farming village appears." A drought nudge could delay farming and so change which stretch got coarse treatment, which is exactly the fake divergence you want to avoid.

**RNG keying.** Key draws on absolute season index, not tick number. Keep annual-mode draws under a distinct purpose tag, such as `purpose = "annual-winter-mortality"`. That way, changing the switch date in config changes only the draws in the affected span, rather than shifting every later key.

**Cost.** You lose discrete within-year events in the deep Paleolithic, such as "the band split in autumn after a failed migration." The event log has to tolerate events dated to a year rather than a season. Civilization's lesson is that viewers accept coarse early time steps if the calendar makes the change visible.

### Why not the state-adaptive methods (approaches 6–8) for v1

All three share one structural problem: the decision to go coarse is a function of state, and a nudge changes state. Hunter and Mac Namee showed that outcomes shift with the switching threshold alone. RimWorld's distance-based tick rate produced jobs that progress differently when off-screen. For a tool whose core value is a credible counterfactual diff, these methods make every difference ambiguous: is it the drought, or the switch?

If you adopt one later, there is one workable pattern (inference). Run both branches once to collect each branch's fidelity mask (which seasons and regions wanted detail). Then re-run both under the union mask, so the pair is compared under identical fidelity. Forks cost roughly double, but divergence becomes attributable. Equation-free projection adds a further risk: float-heavy derivative estimation is sensitive to operation order, and that matters across browsers.

## Recommendation

1. **Adopt approach 1 plus approach 2 as the architecture.** Keep the seasonal tick, with a run-ahead history buffer and log-driven playback pacing.
2. **Add approach 3, static multi-rate scheduling, from the start.** It is cheap, fork-safe, and is what both Dwarf Fortress and Paradox actually ship.
3. **Hold approach 4, calendar-scheduled annual ticks for the deep Paleolithic, as a config-level fallback.** Use it only if the laptop benchmark cannot sustain a comfortable lead over playback.
4. **Keep "start later" (approach 9) as a scenario option, not as the architecture.** A Qud-style generated backstory can cover the skipped span narratively.
5. **Do not build state-adaptive time compression into the v1 core.**

**Strongest counterargument.** The bottleneck may not be ticks at all. It may be that 30,000 years of Paleolithic band life produces very little the event log would call salient. Even at infinite simulation speed, the viewer would mostly watch fast-forward. On that view, the project should simulate less, not faster: start nearer the farming transition, generate the deep past, and spend the compute on the dense later eras. Those eras, running toward Roman scale with thousands of settlements ticking seasonally, are where the real cost will appear and where level-of-detail will eventually be unavoidable. This is a serious argument. The recommendation answers it only partly: the run-ahead architecture keeps the option open, and the playback pacer will reveal empirically how much of the Paleolithic is watchable.

**Failure modes to plan for.**
- **The frontier stall.** In dense eras, simulation throughput can drop below the playback rate the pacer wants. The viewer catches up to the frontier and the experience degrades to real-time stepping. Mitigations: pre-run before showing, keep a minimum lead, and expose the frontier in the UI.
- **Silent cross-browser divergence.** Using any implementation-approximated Math function, unordered iteration over a Map built in data-dependent order, or a parallel float reduction whose order depends on worker timing will make "same seed, same world" false across machines or browsers. Ban these functions in sim code with a lint rule (as OpenFrontIO and others do). Fix partitioning and reduction order for any multi-worker split. Hash full state every N seasons in CI on two engines.
- **Log and history memory blow-up.** 120,000 seasons of events, plus keyframes, plus fork pairs, can exhaust browser memory long before 16 GB of system RAM matters. Tier the log by salience, keyframe sparsely, and compress older history.
- **RNG key drift.** If tick length ever changes, as in approach 4, and draws are keyed on tick count rather than absolute season, every later draw shifts. A config change would then masquerade as a different history.

## What to Benchmark First on the i7-8665U (Chrome, Web Worker, plugged in and on battery)

1. **Field-update cost per season.** Five fields at 256×256 and at 512×512, each with your actual substep count, in plain TypeScript on Float32Array. Report ms per season at steady state after JIT warm-up, and after five minutes of sustained load to capture thermal throttling. This single number decides between approaches 3 and 4.
2. **Group-update cost.** 1,000, 5,000 and 20,000 groups in structure-of-arrays layout, with four age brackets, relations and techniques, including event-log writes per tick.
3. **Run-ahead ratio by era.** Simulated seasons per wall-clock second, divided by your target playback rate during "quiet" stretches. You want a comfortable multiple above 1.
4. **Snapshot and fork cost.** Time and bytes to serialize a full snapshot, transfer it, and start a fork. Also the cost of the paired re-run for a fork comparison.
5. **Determinism check.** The same seed run in Chrome and Firefox (and Edge), comparing state hashes every 100 seasons. This catches Math-function and iteration-order leaks early.
6. **Only then, a WebAssembly or multi-worker trial on the hottest kernel.** The published evidence shows plain WebAssembly roughly ties optimized JavaScript on stencils, and SIMD gains are uncertain. Multi-worker parallelism needs COOP/COEP headers for SharedArrayBuffer and a fixed-order reduction.

## Caveats

- The throughput figures come mainly from a GitHub issue and a README on Apple silicon and desktop Intel hardware, not from controlled studies on your chip. The laptop arithmetic above is extrapolation.
- Several game-design facts come from interviews, dev diaries and community wikis rather than technical post-mortems. The Civilization years-per-turn tables are community-documented.
- I did not find primary technical sources for Songs of Syx, WorldBox, Spore or SimEarth time handling, so they are not used as evidence here.
- The epidemiology results on agent-based ↔ equation-based switching are the closest published analogue to your problem. Transferring their threshold-sensitivity findings to band demography is an inference.

## Sources
- https://www.gamedeveloper.com/programming/how-tarn-adams-upgraded-and-optimized-dwarf-fortress-for-its-official-steam-release
- https://gamerant.com/dwarf-fortress-interview-evolution-after-release/
- https://www.gamedeveloper.com/design/q-a-dissecting-the-development-of-i-dwarf-fortress-i-with-creator-tarn-adams
- https://admin-forum.paradoxplaza.com/forum/threads/four-ticks-per-day.1505480/page-2
- https://civilization.fandom.com/wiki/Speed_(Civ6)
- https://forums.civfanatics.com/threads/how-many-turns-from-4000-bc-until-2050-ad.24887/
- https://codehappy.net/apolyton/threads/36981-1.htm
- https://gdcvault.com/play/1024990/Procedurally-Generating-History-in-Caves
- https://www.freeholdgames.com/papers/Generation_of_mythic_biographies_in_Cavesofqud.pdf
- https://jasss.soc.surrey.ac.uk/12/4/13.html
- https://aaas.confex.com/aaas/2011/webprogram/Paper3471.html
- https://archive.connect.h1.co/article/718445349/
- https://climateandcapitalism.com/wp-content/uploads/2014/03/Motesharrei-Human-and-Nature-Dynamics.pdf
- https://cyberleninka.org/article/n/966377
- https://www.science.org/doi/10.1126/sciadv.adq9976
- https://www.brookings.edu/articles/a-hybrid-epidemic-model-combining-the-advantages-of-agent-based-and-equation-based-approaches/
- https://www.jasss.org/23/4/14.html
- http://www.scholarpedia.org/article/Equation-free_modeling
- https://www.informs-sim.org/wsc10papers/135.pdf
- https://softwaresim.com/blog/introduction-to-discrete-time-simulation/
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math
- https://github.com/openfrontio/OpenFrontIO/pull/5817
- https://simplified.media/guides/deterministic-lockstep
- https://www.dev-toolbox.tech/tools/browser-feature-detector/examples/shared-array-buffer-support
- https://andrewlock.net/understanding-security-headers-part-3-cross-origin-embedder-policy/
- https://www.thesalmons.org/john/random123/papers/random123sc11.pdf
- https://en.wikipedia.org/wiki/Pseudorandom_number_generator
- https://ar5iv.labs.arxiv.org/html/1901.09056
- https://www.usenix.org/system/files/atc19-jangda.pdf
- https://www.usenix.org/system/files/login/articles/login_fall19_03_jangda.pdf
- https://surma.dev/things/js-to-asc/
- https://github.com/bendlang/bend/issues/1352
- https://github.com/Jumbub/game-of-life-js
- https://v8.dev/features/simd
- https://blog.tensorflow.org/2020/09/supercharging-tensorflowjs-webassembly.html
- https://asrjetsjournal.org/American_Scientific_Journal/article/download/11676/2837/27853
- https://surma.dev/things/is-postmessage-slow/
- https://developer.chrome.com/blog/transferable-objects-lightning-fast
- https://zenn.dev/uhyo/articles/javascript-math-accuracy?locale=en
- https://top-mods.com/mods/rimworld/other/14186-performance-slower-pawn-tick-rate.html
- https://github.com/jjgroenendijk/sunset-driver/issues/471
- https://github.com/jjgroenendijk/sunset-driver/pull/472
