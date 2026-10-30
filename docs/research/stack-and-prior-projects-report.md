# Civilization "God-View" Simulation: Prior Projects, Verified Stack Options, and a Recommendation (October 2026)

Research report, 2026-10-22 (Claude research task). Note: a later timescale report refines the threading and tick advice; see research/timescale-report.md.

---

The web stack from the earlier discussion holds up against the evidence: a pure TypeScript simulation core with no renderer dependency, PixiJS v8 for rendering, Vitest for headless tests, and a hybrid granularity model. One correction: the simulation should start on the main thread or in a plain Worker, and moving PixiJS itself into an OffscreenCanvas Worker should be an optional later step, not a starting requirement. The best evidence for this design comes from the projects that resemble the goal most closely. Azgaar's Fantasy Map Generator is a browser-based world simulation written in JavaScript and moving to TypeScript, with a strict data/generator/renderer split. Victoria 3 and Ultima Online show that performance walls are reached through simulation cost (pop counts, pathfinding, radial searches), not rendering.

## TL;DR
- **Recommendation stands, with adjustments.** Use TypeScript (strict) + pnpm + Vitest for a renderer-free simulation core, and PixiJS v8 (currently 8.22.0, released 1 Oct 2026) for 2D rendering. PixiJS now auto-detects Web Workers and renders to OffscreenCanvas, so the earlier memory-based claim is verified. Godot 4.7 is the strongest alternative but only with GDScript, because Godot 4 still cannot export C# projects to the web. Unity and Bevy are viable but a poorer fit for this hardware, language preference, and goal.
- **Use a hybrid granularity model.** Represent the population as aggregate "pops" (cohorts per region, as in Victoria) and promote a small number of notable individuals to full agents (as in Dwarf Fortress historical figures and Caves of Qud sultans). Full per-person agents scale only to the tens of thousands even in heavily optimized native games (Songs of Syx is advertised at up to 30k individuals). LLM-driven agents are far more expensive: Park et al.'s Generative Agents paper (Stanford/Google) reports that simulating "25 agents for two days" required "costing thousands of dollars in token credits and taking multiple days to complete."
- **The main risks are sim-cost growth and opacity, not graphics.** Victoria 3's pop count roughly quadruples over a game (about 20k–25k to about 100k). Its Tech Lead wrote in Dev Diary #76 that employment-update cost is "very strongly correlated with the number of pops" and that "design has tweaked how aggressively the game merges small pops"; the team also built a performance dashboard. Ultima Online's lead designer Raph Koster wrote that in its ecology "the constant radial searches were incredibly expensive, and so was all the pathfinding." Build deterministic ticks, per-system timing, entity caps or merging, and a "why did this happen" event log from the beginning.

## Key Findings

### 1. Prior projects comparison

Status key: **V** = verified in this research with a source; **M** = from general knowledge, not re-verified here (treat as likely but unconfirmed).

| Project | Stack | Granularity | Scale | Visualization | Intervention | Lesson |
|---|---|---|---|---|---|---|
| Dwarf Fortress (Bay 12) | C/C++ (M); started 2002, public 2006 (V) | Hybrid: world-gen simulates civilizations and historical figures abstractly; fortress mode simulates individuals in detail (V) | Thousands of years of history, hundreds of sites (V, descriptive) | ASCII/tiles; Legends mode browses the history of every civilization and figure (V) | World-gen parameters, seed; play in the world (V) | Worldgen "establishes the cast and their relationships" so it can stop at any point. Tarn Adams describes pushing world-gen processes into live play as a deliberate later step (V) |
| Caves of Qud (Freehold) | Unity/C# (M) | Generated history with ex post facto rationalization (V) | Sultan-era histories, villages, quests (V) | Tile roguelike; history exposed through in-game "gospels" (V) | None (player-avatar view) | Events are generated first and rationalized afterwards, using a state machine and replacement grammar. A two-phase world creation delays full fabrication (V). This is a cheap substitute for full causal simulation |
| Songs of Syx (Gamatron) | Java (written for 1.8, runs on 21), custom engine "Snake2D" on LWJGL 3 (V) | Individual citizens + world map | "Cities with up to 30k individuals" (V, official wiki); fan sources cite 40k+ (unverified) | 2D sprites | City-builder controls | One solo developer reached tens of thousands of agents by writing custom data structures for nearly every Java type (V). This shows how much engineering per-agent scale demands |
| WorldBox (Maxim Karpenko) | Unity (V); Flash prototype 2011–2012 (V) | Individual units + kingdoms | Not published | Pixel-art map | God powers: terrain brushes, disasters, plague, spawning (V) | This is the closest commercial match to "watch and nudge." Its design goal is "the ULTIMATE god simulator… without the game limiting you with resources and missions" (V) |
| Victoria 3 (Paradox) | Clausewitz/Jomini, C++ (M) | Aggregate "pops" (V) | About 20k–25k pops at start, about 100k at end in automated tests; Dev Diary #76: "For Victoria 3 a tick is six hours, or a quarter of a day" (V) | Map modes, economic panels | Policy/laws, player actions | Dev Diary #76 names "the employment update, followed by the pop need cache update and the modifier update" as the costliest tick work. Employment-update cost is "very strongly correlated with the number of pops… the number of objects, not the total population," so "design has tweaked how aggressively the game merges small pops." In 2024, AI and migration changes cancelled out performance gains, which led to a "Performance Dashboard" with per-system heatmaps (V) |
| Ultima Online ecology (Origin, 1997) | Server-side sim (M) | Individual creatures with resource needs | MMO world | 2D isometric | Players | Raph Koster ("UO's resource system, part 2," 2006): "The problem was that the constant radial searches were incredibly expensive, and so was all the pathfinding." On Hacker News (2018) he added that it "was removed during the beta after being rewritten by an engineer who didn't really like or understand it." The closed economy failed separately, because of player hoarding (V) |
| Azgaar's Fantasy Map Generator | JavaScript moving to TypeScript; d3/SVG rendering; runs fully client-side (V) | Aggregate: cells, states, cultures, religions, burgs (V) | Configurable, e.g. 10K points, 500 burgs (V) | Layered SVG map (WebGL also mentioned in README) | Editors perform "controlled mutations" of world state (V) | The README requires that the data layer hold no logic, that generators implement the simulation, and that the renderer be "pure visualization" that never modifies world data (V). This is the same separation proposed for this project |
| Sugarscape (Epstein & Axtell 1996) | Original: Ascape-era; now reimplemented in Mesa/NetLogo (V) | Individual agents on a grid | 50×50 toroidal grid (V) | Grid + charts | Parameter changes | Trade, group formation, and skewed wealth distributions emerged from simple rules (V) |
| Artificial Anasazi (Dean, Axtell et al.) | Ascape originally; NetLogo replication (V) | Households as agents (5 persons each) (V) | Starts with 14 households in AD 800; 80×120 cells of 100 m (V). Sources differ on the peak: Janssen (JASSS 2009) describes growth to "about 250 households" in one passage, and in §4.3 says the archaeological data show "numbers just above 200," against a default-setting model potential of "around 1050 in 1260" | Map + household-count time series | Environmental drivers (PDSI, water) | Reproduced the population curve AD 800–1300, but environment alone could not explain abandonment. Janssen's "Understanding Artificial Anasazi" (JASSS 12(4)13, 2009) found the fit "is based on two parameters that adjust the carrying capacity of the Long House Valley… the specific agent behavior contributes only a modest improvement," and that the agent model "acted as a smoothing function for the irregular carrying capacity levels" (V). Aggregate parameters often dominate |
| Mesa (Python ABM) | Python; SolaraViz browser visualization; Mesa 3 stable, 4.0 in alpha (V) | Individual agents | Research-scale | Browser grid/network + live charts; Mesa 3.2 added an in-viz command console (V) | Sliders, console | A good fit for prototyping rules and charting, not for a polished god-view |
| NetLogo | Scala/Java on JVM; 7.0.4 (May 2026); NetLogo Web in browser (V) | Individual "turtles" on patches | Research-scale | Built-in 2D view + plots | Sliders/buttons, live code | A proven teaching and research tool, but its language and UI ceiling limit a custom sandbox |
| Generative Agents "Smallville" (Stanford) | LLM agents (GPT-3.5-turbo) + Phaser-style sandbox (M) | Individual LLM agents | 25 agents, 2 game days (V) | 2D tile town | Natural-language injection | Park et al. (arXiv 2304.03442): the study "required substantial time and resources to simulate 25 agents for two days, costing thousands of dollars in token credits and taking multiple days to complete" (V). LLM agents fit a few narrated notables, not a population |
| Concordia (DeepMind) | Python library; LLM + associative memory; "Game Master" mediates the environment (V) | Individual LLM agents | Small | Text logs | GM / natural-language actions | The Game Master pattern can serve as an intervention and narration layer |
| RimWorld, Crusader Kings, Ages of Conflict, UEBS, Nicky Case explorables | Not verified in this research | — | — | — | — | Mentioned only as genre references; no claims are made here |

### 2. Engine/stack comparison (verified current facts)

| Option | Current status (verified) | Fit for large sims | Fit for this user/laptop | Key trade-off |
|---|---|---|---|---|
| **TypeScript + PixiJS v8** | v8.22.0 released 1 Oct 2026. v8.16.0 (Feb 2026) added an experimental Canvas renderer for environments without WebGL/WebGPU. In Workers, PixiJS selects WebWorkerAdapter automatically and renders to OffscreenCanvas. Accessibility and DOM interaction are unavailable in Workers | Rendering many sprites is mature. Sim speed depends on your data layout (typed arrays) | Excellent: matches TS-strict + pnpm; small install footprint (inference); runs on the integrated GPU via WebGL/WebGPU | You build the UI, inspector, and save system yourself. JS performance needs a data-oriented design |
| **bitECS (JS ECS)** | 0.4.0 is "a complete rewrite in TypeScript." Storage-agnostic (SoA TypedArrays recommended; TypedArrays required for SharedArrayBuffer threading); serialization module included; one maintainer | Data-oriented iteration; Phaser 4 uses it internally | Good, but pre-1.0 with a single maintainer | Optional. Plain SoA typed arrays may be enough |
| **Three.js / WebGPU** | WebGPU ships in Chrome/Edge 113+ (Windows D3D12), Firefox 141 on Windows, Safari 26. Firefox Linux support is still in progress | WebGPU compute could later handle field simulations (climate, diffusion) | Works on Windows Intel iGPUs through D3D12 (inference from platform list) | 3D is extra scope for an observational 2D map |
| **Rust→WASM hot loops** | Not separately verified here | Useful for pathfinding and diffusion kernels | Adds a second toolchain | Defer until a profiler shows a specific hotspot |
| **Godot 4 (GDScript)** | 4.7 stable 18 Jun 2026; 4.7.2 maintenance 18 Aug 2026; 4.8 in development | Good 2D renderer, editor, built-in UI | Light enough for this laptop; open source (MIT) | GDScript is slower than C# for hot loops. Not TypeScript |
| **Godot 4 (C#)** | Docs: "Projects written in C# using Godot 4 currently cannot be exported to the web." Users still hit this error on 4.7 stable mono; only unofficial workarounds exist | C# is fast enough for tens of thousands of agents (inference) | Desktop-only distribution | No web build. A static-typed language, but not TS |
| **Unity 6 + Entities** | Runtime Fee cancelled 12 Sep 2024. Personal plan is free up to $200k revenue/funding. Entities 1.5.0 (Sep 2026) for Unity 6.0; from Unity 6.4 Entities is a core package versioned with the editor; Entities.ForEach is obsolete | DOTS/Burst is the strongest option here for huge agent counts | Heavy editor on 16 GB RAM and an integrated GPU (inference); C# | High learning curve; the version split (1.x vs core) adds churn |
| **Bevy (Rust ECS)** | 0.19 (19 Jun 2026) and 0.20 (Oct 2026) released; still pre-1.0 with breaking changes each release | ECS-native, parallel systems | Rust compile times on a 4-core laptop are a drag (inference) | No editor; ongoing API churn |
| **Mesa / NetLogo** | Mesa 3 stable, 4.0.0a0 dev; NetLogo 7.0.4 | Research-grade | Very light | Best used as a throwaway prototyping notebook for rules, not as the product |
| **Custom Java/C++ (Songs of Syx, DF path)** | Proven by shipped games | Highest ceiling | High effort | Only justified if the agent count must exceed what JS can handle |

## Details

### Architecture lessons drawn from the evidence
1. **Keep the simulation and the renderer strictly separate.** Azgaar's README codifies this: data with no logic, generators as the simulation, editors as controlled mutations, and a renderer that never modifies world data. Model this project's "nudges" as editor-style mutations: typed commands applied at tick boundaries.
2. **Use a deterministic fixed tick and seeded RNG.** Dwarf Fortress worlds are reproducible from a seed, and Adams notes you can run the same seed to different end years. Victoria 3's Dev Diary #76 states "a tick is six hours, or a quarter of a day," compared with one day in CK3/EU4 and one hour in HOI4. Use a fixed timestep with a render interpolation loop (bitECS documents this pattern). Determinism makes save/replay and A/B "what if I trigger a drought" comparisons possible: fork a seed, apply the nudge, and diff the outcomes.
3. **Use hybrid granularity and level of detail.** Aggregate cohorts drive demographics and economics, and full agents are reserved for notables. Janssen's 2009 JASSS replication of Artificial Anasazi found the fit "is based on two parameters that adjust the carrying capacity," with agent behavior contributing "only a modest improvement." Caves of Qud shows that narrative "why" can be generated cheaply after the fact.
4. **Build observability in from the start.** Victoria 3's team found that its "internal tools for monitoring performance were simply inadequate" and built per-system heatmaps. Mesa ships live plots and a console. Plan for per-system tick timing, time-series charts, and a causal event log (each event records its parent cause IDs) so the inspector can answer "why did this happen."
5. **Watch for search and pathfinding costs.** In Ultima Online's ecology, according to Raph Koster, "the constant radial searches were incredibly expensive, and so was all the pathfinding." The ecology was not destroyed by players. Use spatial hashing, flow fields per region, and budgeted per-tick work.

### Threading note (verified and inferred)
PixiJS in a Worker is supported, but DOM interaction and accessibility are unavailable there. For a god-view tool with heavy UI (inspectors, charts, sliders), the simpler arrangement (inference) is: simulation in a Worker, posting compact snapshots or transferable typed arrays; and PixiJS plus the UI on the main thread. Moving rendering to OffscreenCanvas is an optimization to make later, only if needed.

## Recommendations
1. **Stack:** pnpm monorepo with `sim-core` (pure TS, no DOM imports, Vitest), `sim-worker` (thin wrapper), and `viewer` (PixiJS 8.22 + UI + charts). Store state as SoA typed arrays. Add bitECS only if component churn justifies it.
2. **Granularity:** a region/cell grid (Azgaar-like) holding cohort pops (age, culture, occupation, wealth bands), plus a capped set of notable agents (rulers, prophets, generals) whose biographies come from logged events.
3. **Interventions:** typed command objects (`TriggerDrought{region, severity, duration}`, `SetPolicy{state, policy}`) are queued and applied at tick start, logged with cause IDs, and replayable.
4. **Prototyping:** Mesa or NetLogo is acceptable for testing a rule in an afternoon notebook, but port the rule to TS before building on it.
5. **Defer** Rust/WASM, WebGPU compute, and LLM narrators until profiling or design shows a concrete need. If added, an LLM narrator should only describe logged events, as a Concordia-style Game Master, and never drive the population.

### Strongest counterargument
Godot 4.7 with GDScript (or C# for desktop-only) provides an editor, scene tree, UI controls, tilemaps, and inspector-style debugging out of the box. That removes the large hidden cost of the web route, which is building every panel, chart, and save/load path yourself. Unity DOTS has the highest agent-count ceiling. If the user decides the goal requires hundreds of thousands of individually simulated people, a C# or native ECS stack is the defensible choice. The rebuttal is that the evidence (Victoria 3 pops, Anasazi replication) suggests aggregate-plus-notables gets most of the emergent value without that scale, and TS keeps the user in their strongest language with headless tests.

### Failure modes to plan for
1. **Entity explosion and late-game slowdown.** Counts grow over simulated time (Victoria 3 roughly quadruples its pops). Mitigate with merge thresholds, hard caps, and per-system timing budgets checked in CI against a seeded long run.
2. **Opaque emergence.** Without causal logs, the user sees collapse but not its cause, which defeats an observational sandbox. Mitigate with an event log that records parent causes, plus time-series charts.
3. **Scope creep in the rules.** Dwarf Fortress is a decades-long "life's work," and Koster calls parts of UO's closed economy a "mistake" that was gutted. Mitigate by adding one system at a time, each with a headless test asserting a plausible macro-behavior.
4. **Worker/UI coupling.** Putting PixiJS in a Worker loses DOM interaction, which complicates inspectors. Keep the renderer on the main thread unless profiling forces the move.

## Caveats
- Entries marked M (DF/Victoria engine language, Caves of Qud and Smallville stacks) and the projects listed as unverified were not re-confirmed in this research.
- Songs of Syx population figures vary by source and version (30k official wiki vs 40k+ fan sources).
- Install footprint and integrated-GPU performance statements are inference. Benchmark on the actual i7-8665U before committing.
- Some 2026 secondary sources (blogs and aggregators about WebGPU "Baseline") carry marketing tone. The browser-version facts above rely on Chrome and web.dev documentation.

## Sources
- https://github.com/Azgaar/Fantasy-Map-Generator/blob/master/README.md
- https://hysenlabs.com/projects/azgaar-fantasy-map-generator
- https://massivelyop.com/2022/09/03/the-game-archaeologist-how-ultima-online-got-made/
- https://forum.paradoxplaza.com/forum/developer-diary/victoria-3-dev-diary-76-performance.1570277/page-3
- https://scalar.usc.edu/works/game-changers-2016-exhibit/dwarf-fortress
- https://en.wikipedia.org/wiki/Dwarf_Fortress
- https://en.wikipedia.org/wiki/Tarn_Adams
- https://ceur-ws.org/Vol-2862/paper5.pdf
- https://www.freeholdgames.com/papers/Generation_of_mythic_biographies_in_Cavesofqud.pdf
- https://dl.acm.org/doi/abs/10.1145/3102071.3110574
- https://github.com/4rg0n/songs-of-syx-mod-example/blob/master/doc/howto/game_code.md
- https://shapes.inc/fandom/songs-of-syx
- https://songsofsyx.com/wiki/index.php/Songs_of_Syx
- https://steamcommunity.com/app/1162750/discussions/0/3820784854040045190/
- https://en.wikipedia.org/wiki/WorldBox
- https://store.steampowered.com/app/1206560/WorldBox__God_Simulator/
- https://gamerant.com/db/video-game/worldbox-god-simulator/
- https://azgaar.github.io/Fantasy-Map-Generator-old/
- https://news.ycombinator.com/item?id=21099344
- https://azgaar.joshenbaum.org/
- https://jasss.soc.surrey.ac.uk/12/1/6/appendixB/EpsteinAxtell1996.html
- https://mitpress.mit.edu/9780262550253/growing-artificial-societies/
- https://mesa.readthedocs.io/stable/examples/advanced/sugarscape_g1mt.html
- https://www.theoj.org/joss-papers/joss.07668/10.21105.joss.07668.pdf
- https://zenodo.org/records/15279748
- https://deepwiki.com/projectmesa/mesa
- http://ccl.northwestern.edu/netlogo/docs/faq.html
- https://www.netlogo.org/announcements/
- https://opensource.com/article/19/2/get-started-netlogo
- https://deepmind.google/research/publications/64717/
- https://pixijs.download/release/docs/environment.html
- https://pixijs.download/dev/docs/environment.html
- https://pixijs.com/blog/8.16.0
- https://github.com/pixijs/pixijs/releases
- https://github.com/NateTheGreatt/bitECS/blob/main/docs/RELEASE_NOTES_0.4.0.md
- https://socket.dev/npm/package/bitecs
- https://phaser.io/devlogs/260
- https://bitecs.dev/docs/introduction
- https://developer.chrome.com/docs/web-platform/webgpu/overview
- https://web.dev/blog/webgpu-supported-major-browsers
- https://godotengine.org/article/maintenance-release-godot-4-7-2/
- https://godotengine.org/article/maintenance-release-godot-4-7-1/
- https://godotengine.org/download/archive/4.7-stable/
- https://sourceforge.net/projects/godot-engine.mirror/files/4.7.2-stable/godot-4.7.2-stable.tar.xz/download
- https://docs.godotengine.org/en/4.5/tutorials/export/exporting_for_web.html
- https://forum.godotengine.org/t/cant-export-to-web/141491
- https://note.com/kagashi/n/nb7aa24a25755?hl=en
- https://docs.unity3d.com/Packages/com.unity.entities@1.5/changelog/CHANGELOG.html
- https://docs.unity.com/en-us/engine/6000.0/manual/packages-list/packages-all/pack-safe/com-unity-entities
- https://docs.unity3d.com/Packages/com.unity.entities@6.6/changelog/CHANGELOG.html
- https://aplusgamesstudio.com/blog/unity-pricing-2026
- https://bevy.org/news/bevy-0-19/
- https://medium.com/@ezraclintoc/bevy-0-19-just-dropped-here-is-what-actually-changed-4bb35e79bf82
- https://github.com/bevyengine/bevy/releases
- https://www.gamedeveloper.com/programming/how-tarn-adams-upgraded-and-optimized-dwarf-fortress-for-its-official-steam-release
- https://bitecs.dev/docs/system
- https://forum.paradoxplaza.com/forum/threads/victoria-3-dev-diary-142-2024-in-retrospect.1726056/
- https://forum.paradoxplaza.com/forum/developer-diary/victoria-3-dev-diary-76-performance.1570277/
- https://dwarffortresswiki.org/index.php/Dwarf_Fortress
- https://massivelyop.com/2018/06/14/magic-through-serendipity-raph-koster-on-the-glorious-mess-that-was-ultima-online/
- https://vr.org/articles/webgpu-baseline-2026-three-js-webxr-default
