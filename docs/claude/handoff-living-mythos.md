# active-memory handoff: Living mythos (civilization simulation)

**Handoff #8** · 2026-11-01 · Lineage: #1 (2026-10-23): engine/stack research, scoping, grilling Q1-Q4, timescale research, Gemini novelty review · #2 (2026-10-23): Project set up, repo skeleton pushed · #3 (2026-10-24): reframe to "terrarium you poke", research batch reviewed, depth/visuals brainstorm, pixel-art look tests v1-v5, decision log rev 8 · #4 (2026-10-24 to 10-28): slice focus; forks = stretch; cloud sessions = tests/tooling; all brainstorm questions closed; decision log rev 11; Project docs consolidated · #5 (2026-10-30): laptop back and linked; Windows `pnpm check` passed; config, lineage IDs, event log built; Project docs mirrored into repo `docs/`; decision log rev 12 · #6 (2026-10-30): 64-bit rng key, tick loop, testing tooling; spec v0.1 drafted, Gemini agent's rewrite archived, spec v0.2; grilling Q0-Q1; decision log rev 16 · #7 (2026-10-30): spec grilling Q2-Q7 settled (revs 17-22); Gemini prompt 7 run and reviewed; fauna model validated in a throwaway prototype; spec v0.8 · #8 (2026-10-30 to 11-01): Q8 grilled, then replaced by a whole-system review at Jordan's request; Gemini prompts 8-11 written, run and reviewed; R1-R3 settled with prototypes (revs 23-25); spec v0.11; laptop screen broke

## 0. Instructions for Claude (read first)

You are continuing work from a previous chat. That chat is gone; this file plus `design/decision-log.md`, `design/spec_v0.1.md` and `design/integration-review-2026-10-30.md` is the complete context. Where they disagree, the decision log wins for decisions; this file wins for work state and next steps.

1. Read this whole file before replying.
2. Follow sections 3 (Style), 4 (Hard rules) and 5 (Corrections) in every reply. They override your defaults.
3. Use the values in section 8 exactly. Never round, re-estimate, or "correct" them.
4. Do not suggest anything in section 7 (Changed / rejected) again unless the user brings it up.
5. Code word: none active. If the user types /amcodeword, start every reply with the phrase they choose (default "Yes Boss!").
6. First reply: at most 5 lines covering goal, current state, next step (section 11). Ask the questions in section 12 only if they block the next step. End with "Ready to continue with <next step>?" and wait.

(Claude Code reading this from the repo mirror: these instructions are for claude.ai planning chats. Take your working rules from the root `CLAUDE.md`.)

## 1. Mission
- **Goal:** Plan, then build, "Living mythos": an observational god-view sandbox, "a terrarium you poke", "like a kid with an ant colony". Bands develop, change the land and each other, make history in unexpected ways; you watch, read the Legends, and nudge. Inspired by Dwarf Fortress worldgen + Legends. Not a game to win; not a copy of Earth's timeline.
- **v1 scope:** simple hunter-gatherer bands to the first farming villages, one procedural landmass, time from year 0. Long-term: a Roman-Empire-like civilization.
- **Success test:** "I trigger a drought and can read in the Legends why one band migrated and another died out." Stretch: fork the world before the drought. v1 passes without the fork.
- **Core loop:** live nudge and watch. Forks are a v1 stretch goal.
- **Current focus:** whole-system review (R4 left), then spec Q9-Q14, then finalize the spec so the laptop can build the systems.

## 2. About the user
- Jordan; hobbyist developer, Calgary. Laptop: Windows 11, i7-8665U, 16GB, integrated GPU; device `mobilebattlestation`, Node 25.3.0, pnpm 10.28.0. **Laptop screen broke on 2026-10-31**; it is not usable until repaired or connected to an external monitor. Also develops from a Pixel 10 Pro XL.
- Laptop repo clone: `C:\Users\User\Workspace\Repositories\the-living-mythos`. Claude Code CLI runs there.
- Claude app for planning, debugging by paste, learning. pnpm only. PowerShell chains with `;`; package.json scripts chain with `&&`.
- This chat lives in the claude.ai Project "Living mythos".

## 3. Style & communication
- **Language:** English.
- **Tone:** senior peer; lead with assessment, not agreement; no filler, no emoji, no time estimates.
- **Reply length:** mobile-length; tables for options and comparisons.
- **Grill format, per question:** options table, strongest counterargument, ≥2 failure modes, verdict/lean, external check, exact decision-log row. One question at a time.
- **Known vs inferred:** separate in the sentence; flag `[NEED: ]`, `[BLOCKED: ]`, `[UNCERTAIN: ]`.
- **Verify first:** for consequential models, search the claims, and where a model's behaviour is the claim, run a throwaway prototype (scratchpad, Python floats fine, never sim code) and report what it actually does before Jordan picks. Q7, R2 and R3 each caught real problems this way.
- **After each pick:** update the decision log (next rev), the spec (next minor version), the integration review and the Project index (`claude/README.md`); write the same files to the Project; re-sync the repo mirror in one `docs:` commit and push. Jordan pulls on the laptop. Jordan approved writing revisions directly as decisions land.
- **Reviews of Gemini reports:** spot-check key claims and say which were verified, corrected, conflicting or unverified.
- **Avoid:** re-asking decided questions; reopening the Rejected list.

## 4. Hard rules (word for word)
1. "Instead of using your usage for research give me the prompt to give to Gemini to do the deep research ... I can then upload the reports in the project for you to look over." When reviewing a report, spot-check key claims and say which were verified.
2. "Lead with assessment, not agreement. ... give the strongest counterargument first, name at least two genuine failure modes, then your verdict."
3. "Separate what you know from what you're inferring, in the sentence itself."
4. "When something is consequential, name the external check that would settle it."
5. "Rule of cool at the same time I want to balance realism." Simulation stays plausible; drama lives in presentation; never tune the sim for drama.
6. The 7 determinism hard rules in the decision log; tests before sim code.
7. "Research better solutions to this issue, even if it means revising previous decisions. This goes for any of them. The system needs to work as a whole. It's a simulation and will need to get deeper and more complex as systems are added" (2026-10-30, during Q8).
8. "For consequential models, verify claims and run a throwaway prototype before I pick. After each pick, update the spec and decision log, re-sync the repo mirror in one docs commit, and I'll pull on the laptop." (2026-10-30)

## 5. Corrections log
| # | Claude did | Correct version |
|---|---|---|
| 1 | Used its own Research tool | Gemini prompts instead (rule 1) |
| 2 | Said backward scrubbing "comes free" | Needs keyframes + command log + replay |
| 3 | Proposed variable tick length | Fixed seasonal ticks |
| 4 | Implied PixiJS in an OffscreenCanvas Worker | Main thread for PixiJS |
| 5 | Framed v1 around two timelines / forks | Live nudge is the core loop; forks a stretch goal |
| 6 | Treated Earth's timeline as the model | Not a copy of Earth's timeline |
| 7 | Noisy dither winter; muted Earth palette | Snowline winter; Endesga 32 |
| 8 | Colour-blind tooling as a v1 concern | Not needed now |
| 9 | Re-asked a decided question (success test option C) | Check past decisions before re-asking |
| 10 | Proposed vegetation recovery of 1.5-2× drought length everywhere | Prompt 7: dry/grass land recovers in ≤ ~1× drought length; only wet/forest land is slower |
| 11 | Spec said gradient noise needs trig | Fixed integer gradient table needs no trig (rev 18) |
| 12 | Proposed fauna model C without stability damping | Prototype showed boom-bust on rich land; density mortality `mDens` is required (rev 22) |
| 13 | Grilled Q8 (food balance) in isolation as a formula choice | Jordan: research better solutions, revise earlier decisions if needed, make the system work as a whole (rule 7). Led to the whole-system review |
| 14 | Spec v0.8 §9 fed people vegetation V directly (gathered ΣV) | V is herbivore forage; people eat guild stocks (rev 23) |
| 15 | Rev 21 note: "a lasting post-drought shortage must come from game" | Q8 prototypes: plants backfilled; outcomes hinge on band size, migration scoring, hunger mortality and refuge occupancy (note kept with a rev 23 correction) |

## 6. Decisions this handoff (details in decision log rev 23-25 and spec v0.11)
| Decision | Why |
|---|---|
| Rev 23 (R1): resource guilds behind one interface: per-cell stock in food units (1 = one adult's needs for a season), capacity from fields, per-guild regrowth rule (continuous, herd model, pulsed), per-worker Type II return a·S/(1 + a·h·S), per-season take cap as a fraction of stock, seasonal factor. Energy-only currency; protein/fat with farming. Slice guilds: large game and plant foods. Labour by rank, capped, until need + stash top-up. One pooled stash with proportional spoilage; stash size a world setting | Jordan, option B. Prototypes: fixed hunt/gather split starved on depleted game; hunt cap 1.5%/season collapsed game, 1% held. Prompt 11: game extinction when people are fed by other food (VEP, Alroy); storage expiry cliffs (Artificial Anasazi, verified) |
| Rev 24 (R2): home range (radius 5 [P]) with one camp per season, moved only if another camp beats it by `campMoveMargin`; forages that camp's 29-cell catchment; camp moves are snapshot state; migration shifts the home range and is the event; prey depression deferred | Jordan, option B + margin. Prototype `run4.py`: background hunger per 200 seasons fixed camp 9-19, seasonal camp 0-14, whole range 0-4 |
| Rev 25 (R3): fission above 50 with a viability guard (new site must feed the daughter band × 1.2); dissolution into the nearest non-hungry band within 15 cells after 3 hungry seasons; perishing below `minViable` when no host and no target; `band_died_out` carries `outcome` (perished / dissolved) and host ID; `band_split` proposed for Q12; fusion and aggregation deferred. Revises rev 9's non-goal | Jordan, option C. Prototype `run5.py`: fission alone → full maps absorb the drought with no events; without the guard dissolution churned (15 dissolutions + 15 splits in 16 years); with the guard: quiet baseline, 1-3 migrations and 4-8 dissolutions per drought |

## 7. Changed / rejected
See decision log "Rejected". Plus:
- Spec Q8 as a standalone food formula → whole-system review R1-R4 (rule 7).
- Q8 options A (linear yield, spec v0.8), B (fixed labour split), C (rank-and-cap alone) → folded into R1 guilds.
- ❌ Hard-coded food channels; people eating V directly (rev 23).
- ❌ Dual (protein/fat) currency in the slice: deferred to farming, not rejected.
- ❌ Fixed camp and whole-home-range footprint (R2 options A and C).
- ❌ Fission without dissolution; fission without a viability guard (rev 25).
- Prey depression: tested (`run3*.py`), no clear effect; deferred (not rejected).
- Earlier rejections still stand: per-biome carrying capacities (rev 18); global temporal climate noise (rev 19); hard-edged drought disc (rev 20); instant clamp of vegetation to K (rev 21); logistic fauna on `cF·V` and fauna without density mortality (rev 22); pure state-diff event detector (rev 17).

## 8. Data & facts (exact)
| Item | Value |
|---|---|
| Decision log | rev 25 |
| Spec | v0.11 (file `design/spec_v0.1.md`); Q0-Q7 and R1-R3 settled; R4 then Q9-Q14 open, order in §20 |
| Integration review | `design/integration-review-2026-10-30.md`: issues I1-I9, R1-R4 grill order |
| Tests | 67 pass, 1 todo, on Windows (no sim code changed in handoffs #7-#8) |
| RNG golden values | 1759517345 and 3421405739 (`rng.test.ts`). Never update casually |
| Map | slice default 128×128; catchment Euclidean disc r = 3 (29 cells); ~3 km per cell |
| Home range | radius 5 cells [P] (81 cells); prompt 10: 55-165 cells, 5-15 camp moves/yr, 10-15 km per move |
| Band lifecycle [P] | `fissionAt` 50, `fissionMargin` 0.2, `dissolveAfter` 3 hungry seasons, `hostRange` 15 cells, home cells ≥ 2·`homeRange` apart |
| Guild starting values [P] | hunt cap ≈ 0.01 of stock per season (≈ 4%/yr; reported sustainable band 2.5-5.5%/yr [UNCERTAIN]); stash ≤ 0.5 seasons of consumption; spoilage 0.15-0.25/season; labour weights 0.25 / 0.75 / 1 / 0.5; need 0.6 / 1 / 1 / 0.8 (children / young adults / adults / elders) |
| Dry-spell share target | ~15% of seasons per region, tune 12-18% (rev 19) |
| Vegetation targets (severe drought, [P]) | dry: −45-70% in 1-2 seasons, 90% recovery in 0.5-1.2× drought length; wet: −25-45% over 2-5 seasons, 1.5-2.5× |
| Fauna rMax | 0.04-0.06/season |
| Fauna targets ([P]) | crash 25-75%; deaths start 1-3 seasons after onset; recovery 30-50 seasons [UNCERTAIN]; prompt 8 suggests 40-100 seasons (unverified); Q8 prototypes saw 74-107 |
| Prompt 10 targets (input to R4) | density 0.05-0.15 persons/km² (≈ 0.45-1.35 per cell); band 25-35, fission 45-50; long-run growth ≈ 0, potential 1.5-3%/yr; warm-climate diet ≈ 53% plants, 26% hunting, 21% fishing; slice meat ≈ 30-50% |
| Verified this handoff | Batek camp moves fit the marginal value theorem; Binford moves/yr range 0-58 (D-PLACE B013); Caribou Inuit 1950 ~60 starved; Sadlermiut 53 of 58 died (epidemic); Artificial Anasazi 800 kg/household/yr, 2-yr storage, fission p 0.125; Gallagher 2019 model (two report formulas corrected); Hamilton 2007 home-range exponent 0.70 (0.756 controlled); Tallavaara 2018 direction |
| Conflicting / unverified | St. Lawrence Island deaths (report 75-86% vs ~1,000 of ~4,000); Binford 15.25 °C storage threshold and QTSTOR shares; 85-90% dissolution share; Robinson & Redford formula and offtake %; Binford packing threshold |
| Repo head | `docs:` commit after this handoff; see `git log` (rev 25 commit) |
| Look test artifact | https://claude.ai/artifact/8TGrzjEVAJF1L2R669HcN5 (Version 5) |

## 9. People, terms & names
- **People:** Jordan. Gemini = external deep-research tool Jordan runs.
- **Terms:** "nudge", "Legends", "rule of cool", "crucibles", "ant-farm feel", "lab coat", "glance word", "camp snapshot", "the slice", "bloom", "the mirror" (repo `docs/`), "transition records" and "emitter" (rev 17), "condition index" (rev 22), "die-back" (rev 21), "guild" (rev 23), "home range" and "camp" (rev 24), "fission", "dissolution", "perished" (rev 25), "whole-system review" / "R1-R4".
- **Names in use:** repo `shadepants/the-living-mythos` (private), branch `Main-REPO`; prototype folders `research/prototypes/q7-fauna/`, `research/prototypes/q8-system/`.

## 10. Work state
| Item | Status | Location | Notes |
|---|---|---|---|
| Decision log | rev 25 | Project `design/decision-log.md`; mirrored | — |
| Spec | v0.11 draft | Project `design/spec_v0.1.md`; mirrored | R4, Q9-Q14 open |
| Integration review | open; R1-R3 settled | `design/integration-review-2026-10-30.md` | R4 left |
| Gemini prompts | 1-11 run and reviewed; none pending | `research/gemini-prompts.md` | — |
| Prompt 8-11 review | done | `research/forager-reports-review-2026-10-31.md`; report text `research/forager-famine-report-gemini.txt`, `food-storage-report-gemini.txt`, `population-ecology-report-gemini.txt`, `food-system-architecture-report-gemini.txt`; PDFs in repo `docs/research/` | — |
| Q8/R prototypes | throwaway Python; evidence for revs 23-25; never port | `research/prototypes/q8-system/` (README lists each script) | Untuned parameters; numbers are shape evidence only |
| sim-core | unchanged: rng, lint bans, config, lineage IDs, event log, tick loop; 67 tests + 1 todo | repo `packages/sim-core` | Entity registry now needed earlier (fission creates bands) |
| Doc workflow | Claude (cloud session) cloned the repo, edited `docs/`, wrote the same files to the Project with `project_write` from the local path, one `docs:` commit per decision, pushed | — | — |
| Laptop | screen broken; behind GitHub (docs only, fast-forward) | laptop clone | Needs repair or an external monitor before pulling or sim code |
| Project instructions | Settings text still has the old success-test wording | `claude/project-instructions.md` | [NEED: Jordan] paste |

## 11. Next steps
1. **Next action:** grill review R4, calibration anchors and targets. Inputs: prompt 10 targets (section 8), rev 23-25 [P] values, prototype calibration issue I8 (food per stock unit vs need decides everything). Settle: food unit anchors, density and band-size targets, meat share, the hunt cap's basis, and whether rev 22's herd recovery target widens to 40-100 seasons. Prototype before Jordan picks.
2. Then spec Q9-Q14 in §20 order, same format. Carry-ins: Q9 needs homeostatic fertility (interbirth interval even when fed; prompt 10) and hunger mortality by age (prompt 8 shape); Q10 migration scoring must not prefer any unforaged land (review I7); Q11 `minViable` for perishing; Q12 adds `band_split` and the `outcome` payload, and a cause for self-inflicted depletion (I4); Q14 scenario needs one band with an exit and one cut off (to perish) or with a host (to dissolve).
3. When all questions settle: spec-developer Phase 3 (finalize), then the laptop builds command log (rule 6), entity registry, then systems in spec §5 order.
4. Decide the rev 10 cloud gate (more pressing with the laptop screen broken; lean: lift with a Windows check before each sim merge).
5. Benchmarks once fields run. Parked: v5 Close-up rewatch; property norm.

## 12. Open questions
- Review R4, spec Q9-Q14.
- Rev 10 cloud gate: lift as written / keep (sim logic only on the laptop) / lift with a Windows check before each sim merge (lean). The broken laptop screen blocks sim work until decided or repaired.
- Stray Project doc `next-steps-prompts.md` at the Project root (duplicate of `claude/next-steps-prompts.md`): delete? Ask Jordan.
- Gemini stash on the laptop (`stash@{0}`): drop once Jordan agrees the archive copies are enough.
- [NEED: Jordan] paste `claude/project-instructions.md` into Project settings.

## 13. Re-attach checklist
Nothing to attach inside the Project.

---
<sub>Audit: 13/13 sections · 8 rules · 15 corrections · 30 data points · secrets removed: none found · generated by active-memory</sub>
