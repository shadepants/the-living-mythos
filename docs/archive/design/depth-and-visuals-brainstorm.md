# Living mythos: simulation depth, visuals and information (brainstorm)

**Archived 2026-10-28** (moved from `design/`). All questions closed; outcomes live in `design/decision-log.md` (rev 8-11). Kept for the ideas not yet scheduled (lore, dig tool, kinship drift, named herds, foreshadowing, event flares, time ribbon), which later spec versions may draw on.

2026-10-23. Brainstorm, not decisions. Items marked **[pick]** are Claude's leans, to be grilled one at a time. Framing from rev 4: a terrarium you poke; plausible mechanisms, not Earth; live nudge and watch.

**Status 2026-10-28: all questions in section 8 are closed.** Where this document differs from `design/decision-log.md` (rev 11), the decision log wins. Notably superseded: the "living atlas" look (now pixel art), lore in v1 (deferred), the separate camp diorama (folded into Close-up).

## 1. Two rules for spending depth
1. **Deep where causes flow through.** If a system sits on the path from "drought" to "band migrated / died out", it has to be real: the success test and every good story run through it.
2. **Cheap where the eye lands.** Things that are seen constantly but don't cause much can be shallow or purely visual, as long as they're driven by real state and never lie about it.

Anything that's neither on a causal path nor seen often doesn't get built.

## 2. Depth map
| System | Depth | Why | Notes |
|---|---|---|---|
| Food web (vegetation, large/small fauna, catchment harvest, diet breadth) | **Deep** | Engine of everything: hunger, migration, splitting, the turn to grain | Per-cell fields, per-band harvest. The most important code in v1 |
| Band demography (4 brackets, births/deaths, fission/fusion) | **Deep** | Population is how consequences land | Per-member hash draws; bands ≤ ~50 |
| Knowledge (techniques, elders, forgetting) | **Medium-deep** | Source of the best stories: the last fire-keeper dies | Level + progress + forgetting time |
| Relations between bands (kin, marriage exchange, grudges, raids) | **Medium** | Where drama between groups comes from | One scalar per pair + a short list of remembered events (grudges point at real events) |
| Movement and migration | **Medium** | Visible and causal | Band evaluates neighbouring catchments and moves; no per-person pathfinding |
| Climate | **Shallow, generated** | Drives everything, needs no internals | Seeded anomaly curve with dials |
| Fire on the landscape | **Medium, very visible** | Humans repaint the map over centuries | Fire age field + mosaic burning |
| Lore (beliefs born from history; see 3) | **Shallow mechanics, huge payoff** | The "mythos" in the name; the funny/strange generator | Small set of traits, each with one mechanical effect |
| Names and language | **Painted, but state-driven** | Cheap, readable kinship | Phonology per lineage, drifts on fission |
| People on screen, weather, seasons | **Painted** | Pure visuals derived from state | Never feeds back into the sim |
| Individual minds, genetics, trade economy, battle tactics, religion as a system | **Not built** | Not on a causal path in v1 | Lore covers belief; raids resolve as one event |

## 3. Where it's coolest
**a) Lore with teeth [pick].** Bands form beliefs from their own salient history, and each belief changes one behaviour:
- A band that survived a famine on eels adopts an eel totem → eats eels first, never leaves the river.
- A band whose elder died hunting the great herd makes the herd taboo → narrower diet → may starve next to food. (Funny and tragic, and fully explained.)
- A band that lost fire to a bad winter fears lightning → avoids burned land.
- Beliefs pass down on fission, drift, and can be dropped when they stop paying.
This is the project's name made literal: myths that grow from the simulation and then steer it. Mechanically small (a handful of trait types, each a bias), narratively the biggest thing in the game. Respects variable discipline: every trait has a mechanical effect the Legends can report.

**b) You become a myth [pick].** Every nudge is logged with a cause. Bands that live through your drought can form lore about it ("the Sky Thief who took the rain"). Your interventions show up in their mythology, so poking the terrarium leaves fingerprints in its culture.

**c) The land is the history book.** Over centuries the map shows human fingerprints: burned mosaics, overhunted zones, trails worn between camps, middens and cairns at old campsites, grain patches by rivers. A "dig" tool on any cell shows its stratigraphy: who camped here, what happened, in which years.

**d) Kinship you can see.** Daughter bands inherit their parent's colour with a small hue drift, and names with phonetic drift. After a few millennia the map's colours and the names form a readable family tree without opening a single menu.

**e) Named great herds.** A few megafauna herds are tracked entities with names ("the Grey Drift") that migrate across the map. They're the sugar cube in the ant farm, and hunting one to extinction is a world event.

**f) Foreshadowing.** Incremental sifting tracks story patterns that have started but not finished. The UI can whisper "The Ash Band's stores are running low…" before the famine lands. Suspense from the same machinery as the Legends.

## 4. Visual design
*(Superseded: look decided as pixel art, decision log rev 8; diorama folded into Close-up, rev 11.)*

**Look [pick: living atlas].** A hand-drawn atlas with life on it: shaded relief, biome colours on parchment tones, rivers as ink. Bands are glowing campfires with tiny figures. Territories are soft watercolour washes in the band's lineage colour. Fits "mythos", cheap in PixiJS, readable at any zoom.

| Style option | Strength | Weakness |
|---|---|---|
| Living atlas (lean) | Mythic, readable, cheap, distinctive | Less "busy" than pixel sims |
| Pixel world (WorldBox-like) | Lively, familiar to the audience | Looks like WorldBox; per-pixel detail costs |
| Abstract data view | Clear, cheapest | Not an ant farm; no wonder |

**Semantic zoom (3 levels).**
1. **World:** territories, lineage colours, herd paths, event flares, the season.
2. **Region:** individual camps, trails, fire patches, herds, grain stands.
3. **Camp diorama:** the "glass of the ant farm". Figures by age bracket (children running, elders by the fire), and objects for known techniques (spears, baskets, a grindstone appears when grain is learned, the hearth goes dark if fire is lost). Purely visual, driven entirely by band state.

**Event flares.** When something notable happens, a glyph pops on the map with a ripple: spark (invention), cracked bowl (famine), forked line (split), skull (band lost), eye (lore formed). The eye is drawn to where history is happening.

**Time ribbon.** A strip along the bottom: the heartbeat of event density over time, auto-named eras from quiet-epoch compression ("The Long Thaw", "Age of Embers"), and a scrubber. Your nudges show as small hand marks on it.

```
+----------------------------------------------------------+
| [season/year]          WORLD MAP (atlas)       [god tools]|
|                                                          |
|   ~wash~  (*)camp   ...trail...   herd>>>    (!)flare    |
|                                                          |
|                         [band card pops on click]        |
+----------------------------------------------------------+
| whisper: "The Ash Band's stores are running low..."      |
| ribbon: ..|.||....|||||..|....  The Long Thaw | Age of.. |
+----------------------------------------------------------+
```

## 5. What you can see vs what's hidden
Principle [pick]: **the world doesn't explain itself; you investigate.** Wonder first, answers one click away, raw numbers only on request. *(Adopted, decision log rev 10.)*

| Layer | How you get it | Shows |
|---|---|---|
| Ambient | Always on, no UI | Map, fires, trails, washes, flares, season, era name, whispers |
| Glance | Hover | Band name, rough size, one status word ("hungry", "thriving", "restless"), lineage colour |
| Inspect | Click | Band card: population bars by bracket, food trend arrow, technique pips, lore traits, relations, notable figures, last few events |
| Investigate | Legends | Chronicle, "why?" cause chains, figure biographies, place history (dig), lineage tree |
| Lab coat | Toggle, off by default | Field heatmaps, exact numbers, tunables, RNG keys. For you as the developer and for curious players |

Hidden on purpose:
- **The future.** No predictions beyond whispers of arcs already underway.
- **Exact numbers outside lab coat mode.** Words and bars keep it a terrarium, not a spreadsheet.
- **Minds.** There are none to show; bands have status and beliefs, not thoughts.

Open option, later: a "chronicler" mode where only places people have lived have recorded history, so the map's history thins out at the edges.

## 6. God tools (environmental first, per the decision log)
*(v1 = rain/drought + bloom; slice = drought. A tool ships with its mechanism. Decision log rev 11.)*

Physical gestures, not menus:
- **Rain / drought:** drag a cloud on or off a region.
- **Spark:** start a fire.
- **Bloom:** make a patch of land fertile for a few years (the sugar cube).
- **Herd:** drag a great herd somewhere.
- **Later:** sickness (biological); a stranger band arrives, whisper a technique (cultural).

Each one is logged and can enter the bands' lore (3b).

## 7. Risks
- **Lore scope creep.** Cap v1 at ~6 trait types, each with exactly one mechanical effect.
- **Illegibility.** Too many flares and washes. Salience thresholds and zoom levels decide what's drawn.
- **Diorama cost.** Cap the figures drawn per camp; it's a view, not a crowd sim.
- **"Painted" drifting from state.** Visuals must read from sim state only, and never feed back.

## 8. Questions to grill, in order
1. ~~Lore with teeth in v1, or later?~~ **Resolved 2026-10-24: later** (after food web and demography are stable).
2. ~~Visual style~~ **Resolved 2026-10-24: pixel.** Look test artifact: https://claude.ai/artifact/8TGrzjEVAJF1L2R669HcN5
3. ~~Information default~~ **Resolved 2026-10-28: investigate-to-learn, lab coat toggle off by default** (decision log rev 10).
4. ~~Which god tools ship in v1~~ **Resolved 2026-10-28: rain/drought + bloom; slice ships drought** (rev 11).
5. ~~Camp diorama in v1 or later~~ **Resolved 2026-10-28: folded into Close-up, reading a read-only camp snapshot** (rev 11).
