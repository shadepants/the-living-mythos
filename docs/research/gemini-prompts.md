# Gemini deep-research prompts (Living mythos)

Status (2026-10-31): prompts 1-11 run and reviewed; none pending. Reviews: prompt 1 → `research/novelty-report-gemini.txt` (caveats in decision log); prompts 2-5 + repos report → `archive/research/batch-review-2026-10-23.md`; prompt 6 → `research/pixel-art-review-2026-10-24.md`; prompt 7 → `research/vegetation-drought-review-2026-10-30.md`; prompts 8-11 → `research/forager-reports-review-2026-10-31.md`.
Usage for new prompts: paste the CONTEXT BLOCK first, then the prompt. Upload each report to the Project.
Consolidated 2026-10-28: prompt 1 moved here from the former `research/novelty-research-prompt.md` (deleted).

## Context block (updated 2026-10-24; paste before any prompt)
Check against the decision log before reuse; as of rev 11 it is still accurate, but the slice scope (rev 9) means new prompts should usually target the success-test slice only.

```
PROJECT CONTEXT
I'm building "Living mythos," an observational god-view sandbox: a terrarium you poke, like a kid with an ant colony. You watch bands of people develop, change the land and each other, and make history in unexpected ways, and you nudge things (drought, rain, fire) to alter the course. It's inspired by Dwarf Fortress world generation and Legends mode. It is not a copy of Earth's timeline: plausible mechanisms, procedural world, time counts from year 0. Version 1: simple hunter-gatherer bands through the first farming villages, on one procedurally generated landmass. Long-term: toward a Roman-Empire-like civilization.
- Stack: browser-based. Strict TypeScript, pnpm monorepo, simulation core in a Web Worker, PixiJS v8 renderer. Target hardware: a modest Windows laptop (i7-8665U, 16GB RAM, integrated GPU). Solo hobbyist developer who cannot draw.
- Simulation: deterministic seasonal ticks with hash-based randomness. Bands are groups with 4 age brackets. Techniques have skill levels that grow with use and are forgotten without practice; elders slow the forgetting. Grid fields for vegetation, soil, large and small fauna, water, fire age and crop domestication, coupled two ways with people. World-seeded climate.
- History: a causal event log where each event links to at most 3 causes, shown in a Legends-style browser with templated narration. Notable individuals exist as records, not simulated minds.
- Visuals: pixel art. Dithered procedural terrain, sprite markers for bands and herds, seasons, fire.
- Design principle: the simulation stays plausible; the drama lives in the presentation.
Report requirements: distinguish verified facts (with sources and dates) from inference; flag anything uncertain or contested; use tables for comparisons; no emoji; no time estimates; export as markdown.
```

## Done (kept for reference)

### Prompt 1: Novelty and prior art (done; report `research/novelty-report-gemini.txt`)
Written before the rev 4 reframe: it still describes forks as the signature feature and a Paleolithic arc. Kept as the record of what was asked.

```
Research and assess the novelty of a planned project by finding every existing project that resembles it: commercial games, indie and open-source projects, academic simulations, LLM-agent experiments, art pieces, and tools. The goal is to confirm the project is worth building and is not already done in substantially the same way. Answer honestly: if something already does this, say so plainly.

THE PROJECT
An observational "god-view" civilization simulation, closer to a sandbox to watch than a game to win. Planned v1:
- A procedurally generated landmass where Paleolithic hunter-gatherer bands live, migrate, and (sometimes) develop into the first farming villages, with no scripted tech tree. Techniques become possible when conditions hold (population density, surplus, local resources) and spread through contact. Stagnation and collapse are allowed outcomes.
- Two-way human-environment coupling: grid fields for vegetation, soil, fauna, water, and fire. People reshape the land (overhunting, burning, clearing), and the land reshapes them.
- Group-level simulation of bands and villages. Notable individuals exist as history records (name, lineage, deeds), not simulated minds.
- A Dwarf Fortress "Legends mode"-style history browser built on a causal event log: every event links to the events that caused it, with readable narration.
- Light-touch interventions ("nudges"): environmental first (drought, an ice age ending), later biological (introducing a domesticable plant, removing megafauna), and later cultural.
- The intended signature feature: deterministic counterfactual forks. Snapshot the world, run it with and without a nudge, and diff the two histories, with a "did this ripple or fade?" readout showing whether a nudge amplified or was absorbed.
- Browser-based (TypeScript, PixiJS).

WHAT TO FIND
1. The closest existing matches, judged against each element above, not just the genre label. Check at minimum (verify each exists and is described accurately; do not assume): Dwarf Fortress (worldgen and Legends), WorldBox, Ages of Conflict, Ultima Ratio Regum, Caves of Qud, Songs of Syx, RimWorld, Dawn of Man, Ancestors: The Humankind Odyssey, Humankind, the Civilization series, SimEarth, Spore's tribal and civilization stages, From Dust, Populous, Black & White, Thrive, Species: ALRE, Equilinox, Banished, Farthest Frontier, Crusader Kings, Victoria 3, Azgaar's Fantasy Map Generator, Legends Viewer and other Dwarf Fortress history tools, Altera's Project Sid, Stanford's Generative Agents, AI Town, Sugarscape, Artificial Anasazi, the HANDY model, Seshat and cliodynamics work, and NetLogo or Mesa civilization models. Go beyond this list: search itch.io, Steam (including upcoming and early-access titles), GitHub, Reddit (r/simulationgames, r/dwarffortress, r/proceduralgeneration, r/gamedev), Hacker News, academic agent-based modeling and archaeology journals, and Kickstarter.
2. Prior art for the counterfactual fork-and-diff feature specifically. Does any game or simulation let a user branch a world, compare two histories, and measure a nudge's effect? Look at replay and branching systems, time-travel or "what-if" history games, scientific ensemble and sensitivity-analysis tools, and debugging tools such as deterministic replay. This is the claimed differentiator, so test it hardest.
3. Prior art for causal, explainable history logs: games or systems that answer "why did this happen" with linked cause chains rather than flat event lists.
4. Abandoned or failed attempts at similar projects, and what killed them (scope, performance, "not fun to watch", tuning instability). Look for post-mortems, devlogs, and forum threads.
5. Audience evidence: is there demonstrated demand for watching rather than playing (Dwarf Fortress Legends readers, WorldBox's audience, "zero-player game" communities, simulation YouTube channels)?

OUTPUT
- A novelty matrix table: rows are the closest 10 to 15 projects; columns are the project's elements above (open-ended tech progression, Paleolithic-to-farming arc, two-way environment coupling, causal Legends history, nudge interventions, counterfactual fork-and-diff, browser-based). Mark each cell as has / partial / no, citing evidence for each.
- Deep dives on the 3 to 5 closest matches: what they do, what they don't, and how this project would differ.
- A plain verdict: which elements are genuinely new, which are well-trodden, and whether the combination exists anywhere.
- Positioning: the strongest angle for this project given what exists, plus any adjacent ideas worth borrowing.
- Risks: if nobody has built a given feature, assess whether that's an untapped opportunity or a sign it doesn't work (not fun, too costly, unreadable).
- For each of the closest matches, list any public technical material (GDC talks, devlogs, developer interviews, papers, open-source code) that explains how it works internally. This list will seed a follow-up deep-dive.
- Distinguish verified facts (with sources and dates) from inference. Flag any project you could not confirm exists. No emoji, no time estimates.
```

### Prompt 2: How the closest matches work internally (done)

```
Research in technical depth how existing world and history simulations work internally, so I can learn from their designs and avoid their mistakes. Focus on: Dwarf Fortress (world generation, historical figures, the Legends event data model, entity and site simulation), Caves of Qud (history generation by "generate then rationalize"), WorldBox (civilization and kingdom simulation, god powers), Azgaar's Fantasy Map Generator (open source: data model, generators, how cultures, states and religions are produced), Songs of Syx, and Victoria 3 (pop simulation and tick scheduling). Add others you find whose internals are publicly documented.

For each: the core data model for groups and history events; how events are generated and linked; how time advances; what's simulated versus generated; known performance limits; and what the developers said went wrong. Prioritize primary sources: GDC talks, developer interviews, devlogs, papers, and source code where it's open.

Output: a per-project technical summary, a table of design patterns that recur across projects, a section on approaches that failed and why, and specific recommendations for my causal event log, group data model and narration layer.
```

### Prompt 3: Grounding the rules in real prehistory (done)

```
Research the real mechanisms and plausible parameter ranges I need to make my simulation's rules realistic, for the span from the Upper Paleolithic to the first farming villages. Cover:
1. Forager demography: typical band sizes, population densities by biome, fertility and mortality by age, carrying capacity, and how bands split, merge and exchange marriage partners.
2. Foraging ecology: how hunting and gathering depletes and regenerates resources, seasonal mobility, the effects of human fire use on landscapes, and evidence on megafauna overhunting (the overkill hypothesis and its critics).
3. Knowledge transmission: how technologies spread and are lost in small populations (e.g., the Tasmanian case and the debate around it; cultural evolution models such as Henrich's).
4. The farming transition: which conditions preceded domestication in independent centers, theories of why it happened (Boserup's population-pressure theory, climate change at the end of the Pleistocene, others), how long the transition took, and whether it was reversible.
5. Watchability: what actually happened over Paleolithic timescales. Was change mostly slow and gradual, or punctuated by notable events (migrations, climate shocks, population crashes, technology shifts) at what frequency? I need to judge whether simulating 30,000 years is worth watching, or whether to start nearer the farming transition.

Output: per topic, the mechanisms, with parameter ranges in a table and sources; contested points flagged clearly; and a final section translating findings into concrete simulation rules and tunable parameters with suggested defaults.
```

### Prompt 4: Turning event logs into readable history (done)

```
Research how to turn a large simulation event log (thousands of years, many thousands of events) into readable, compelling history narration. This is my project's main readability risk. Cover:
1. Story sifting: academic work on finding interesting stories in simulation logs (e.g., Max Kreminski's work including Felt and Winnow, James Ryan's work on emergent narrative and Talk of the Town), and how sifting patterns are written.
2. Procedural narration techniques: templated grammars (e.g., Tracery), Caves of Qud's replacement grammars, Dwarf Fortress Legends text, and Crusader Kings event descriptions.
3. Salience: how systems decide which events matter (rarity, consequences, involvement of notable figures, causal depth), and how to summarize long quiet stretches.
4. Explaining causality: how to present "why did this happen" chains to a reader without overwhelming them.
5. LLM narration on top of a structured log: risks (hallucination, cost, inconsistency) and safe patterns, such as the LLM only describing logged events.

Output: a comparison table of approaches (quality, effort, determinism, runtime cost), a recommended pipeline from raw events to narrated history for my project, and example sifting patterns and narration templates for events like a band splitting, a famine, and a technique being lost.
```

### Prompt 5: Showing a fork comparison (done; shelved until forks are worked on as the v1 stretch goal)

```
Research how to visually present the difference between two runs of the same simulation (a baseline and one with an intervention), so a viewer can see at a glance whether an intervention's effect grew, faded or was absorbed. Cover: ensemble and sensitivity-analysis visualization in science; timeline and branching-history UIs (version control graphs, "what-if" tools, games with branching or rewind features); map diff techniques (side by side, overlay, difference heatmaps); and metrics for divergence over time between two complex system states.

Output: a table of visualization techniques with strengths and weaknesses, recommended designs for a "ripple or fade" readout, including how to compute a divergence score from two event logs and two grid states, and examples from real tools with sources.
```

### Prompt 6: Pixel-art look for a world simulation (done; review `research/pixel-art-review-2026-10-24.md`)

```
Research how to make a pixel-art world simulation look good, stay readable, and stay consistent when almost everything on screen is generated by code. Cover:
1. Prior art: how WorldBox, Dwarf Fortress (Steam/premium tileset), Songs of Syx, RimWorld, Caves of Qud, Kingdoms and Castles, Ultima Ratio Regum, and other pixel or low-res simulation and strategy games draw terrain, groups of people, herds, settlements, territory and events. Include what reviewers and players praised or criticised about readability.
2. Showing groups at scale: icons/banners vs crowds of tiny figures vs camp/settlement sprites vs abstract markers; how games show population size, movement and state (hungry, thriving) without numbers; how they avoid clutter with hundreds to thousands of groups across zoom levels.
3. Seasons and weather in pixel art: palette swaps vs overlays vs per-pixel effects; how snow, autumn, drought and fire are shown without visual noise; dithering patterns that read as clean vs noisy.
4. Procedural pixel terrain techniques: palette ramps and hue shifting, ordered vs error-diffusion dithering, autotiling and transition tiles, hillshade at low resolution, coastlines, rivers, outlines; how to keep generated terrain looking hand-made.
5. Palettes: restricted palettes suited to earthy, natural, prehistoric worlds (e.g. from Lospec), how many colours, and how to keep 10-30 distinct lineage colours legible and colour-blind safe on top of terrain.
6. Implementation in a browser with PixiJS v8: nearest-neighbour scaling, integer vs non-integer zoom, palette-swap shaders, rendering thousands of small sprites, text and labels alongside pixel art.
7. Animation economy: how few frames games get away with for walking, fire, smoke and water while still feeling alive.

Output: a comparison table of approaches for each topic (readability, effort for a solo developer who cannot draw, consistency, performance), links to concrete examples, recommended defaults for my project, and a list of pitfalls.
```

### Prompt 7: Vegetation drought decline and recovery (done 2026-10-30; review `research/vegetation-drought-review-2026-10-30.md`)
Asked for decline magnitude and seasons to nadir by vegetation type, recovery time (absolute and as a multiple of drought length), asymmetry and tipping points, grazing effects, and large-herbivore lags, with primary sources, observed vs modelled, ranges and a summary table. Feeds spec Q6 and Q7. Full prompt text was given in the planning chat of 2026-10-30.

## Whole-system review prompts (written 2026-10-30; all done 2026-10-31)
Purpose: ground the candidate architecture in `design/integration-review-2026-10-30.md`. Run 8 and 10 first; they decide R2-R4. Paste the context block first. Add this line after it for all four: "Current focus: a slice where bands forage, go hungry, migrate or die out after a drought. Seasonal ticks; grid cells ~3 km; bands of 15-50 people in 4 age brackets."

### Prompt 8: Forager responses to drought and famine (done; report `research/forager-famine-report-gemini.txt`)
```
Research how hunter-gatherer and other mobile foraging groups respond to drought and famine, in quantitative terms I can turn into simulation rules. Cover:
1. The sequence of responses: diet broadening, storage use, increased residential mobility, logistical trips, long-distance relocation, dispersal of members to kin or allied groups, group merging, and starvation in place. Which come first, and after how long (in seasons) of shortfall?
2. Mortality during forager famines and severe droughts: excess mortality by age (children, adults, elders), fertility suppression, and how long effects last. Include ethnographic and historical cases (e.g. Kalahari, Australian desert, Arctic, Great Basin, Plains) and archaeological evidence of group abandonment or extinction.
3. Whether whole bands actually die out, versus dissolving into neighbouring groups. How often does each happen, and what decides it (refuge availability, kin networks, territoriality)?
4. Relocation: distances moved, whether destinations were known refuges, occupied land, or empty land, and how territorial neighbours responded.
5. Recovery: how long until groups re-form or return.
Output: a response-sequence table with typical timing; a mortality table by age and severity with sources; a section on die-out vs dissolution with cases; flags for contested or thin evidence. Distinguish verified facts (with sources and dates) from inference.
```

### Prompt 9: Food storage by environment (done; report `research/food-storage-report-gemini.txt`)
```
Research hunter-gatherer food storage as a buffer against shortfall. Cover: which foragers stored food and which did not, related to effective temperature, latitude and seasonality (Binford, Kelly, Testart); typical storage amounts as days or seasons of consumption; spoilage and loss rates by food type (dried meat, nuts, seeds, roots, fish) and season; the "delayed-return" vs "immediate-return" distinction; and how storage changed mobility and sedentism on the path to farming.
Output: a table of storage duration and loss rates by environment and food type with sources; a short section on storage and sedentism; suggested defaults for a seasonal simulation (stash size in seasons of consumption, spoilage per season) with the evidence for each. Distinguish verified facts from inference.
```

### Prompt 10: Forager population ecology and band dynamics (done; report `research/population-ecology-report-gemini.txt`)
```
Research the population ecology of hunter-gatherer bands, for setting simulation targets. Cover:
1. Population density by environment: persons per km² versus net primary productivity, effective temperature, and reliance on hunting vs gathering vs fishing (Binford 2001, Kelly, Marlowe, D-PLACE).
2. Diet composition: share of energy from hunting, gathering and fishing by latitude or effective temperature, with numbers.
3. Home range and mobility: home range size, residential moves per year, distance per move, and how these relate to density and diet.
4. Band size and fission: typical residential group sizes, size at which groups split, how fission and fusion work seasonally and over years.
5. Growth: long-run forager population growth rates, and what held them low (mortality, fertility, infanticide, emigration).
6. Game depletion: offtake as a share of standing animal biomass, depletion halos around camps, sustainable harvest rates for large ungulates, and evidence that depletion drives camp moves.
Output: one table per topic with ranges and sources; correlations stated with sample sizes where available; suggested simulation targets with the evidence for each; flags for contested points. Distinguish verified facts from inference.
```

### Prompt 11: Architecture of forager and food-web simulations (done; report `research/food-system-architecture-report-gemini.txt`)
```
Research how existing agent-based and system-dynamics simulations of foragers and early farmers structure their food systems, so a simulation can add resources (small game, fish, nuts, wild grain, crops) without rewriting its core. Look at: Artificial Anasazi / Village Ecodynamics Project, HUMLAND, the MASON and NetLogo forager models, Gallagher et al. (Scientific Reports 2019) on hunter-gatherer agents, optimal foraging ABMs (prey choice, patch choice, central place foraging), Ache and Hadza foraging models, Pleistocene overkill models, and any game that models a food web for people (Dwarf Fortress, Songs of Syx, Banished, Dawn of Man) where internals are documented.
For each: how resources are represented (stocks, regrowth, return curves), how agents allocate labour across resources, how depletion and mobility interact, how farming was added, what made the model unstable or hard to tune, and what the authors would change.
Output: a comparison table; recurring patterns; a recommended resource interface for a seasonal grid simulation with two resources now and more later; pitfalls. Distinguish verified facts from inference.
```

## Suggested (not run)
The former suggestions (food storage, forager drought response) are now prompts 9 and 8.
