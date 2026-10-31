# active-memory handoff: Living mythos (civilization simulation)

**Handoff #7** · 2026-10-30 · Lineage: #1 (2026-10-23): engine/stack research, scoping, grilling Q1-Q4, timescale research, Gemini novelty review · #2 (2026-10-23): Project set up, repo skeleton pushed · #3 (2026-10-24): reframe to "terrarium you poke", research batch reviewed, depth/visuals brainstorm, pixel-art look tests v1-v5, decision log rev 8 · #4 (2026-10-24 to 10-28): slice focus; forks = stretch; cloud sessions = tests/tooling; all brainstorm questions closed; decision log rev 11; Project docs consolidated · #5 (2026-10-30): laptop back and linked; Windows `pnpm check` passed; config, lineage IDs, event log built; Project docs mirrored into repo `docs/`; decision log rev 12 · #6 (2026-10-30): 64-bit rng key, tick loop, testing tooling; spec v0.1 drafted, Gemini agent's rewrite archived, spec v0.2; grilling Q0-Q1; decision log rev 16 · #7 (2026-10-30): spec grilling Q2-Q7 settled (revs 17-22); rev 12 ordinal and command-cause rules confirmed; Gemini prompt 7 (vegetation drought) run and reviewed; fauna model validated in a throwaway prototype; spec v0.8

## 0. Instructions for Claude (read first)

You are continuing work from a previous chat. That chat is gone; this file plus `design/decision-log.md` and `design/spec_v0.1.md` is the complete context. Where they disagree, the decision log wins for decisions; this file wins for work state and next steps.

1. Read this whole file before replying.
2. Follow sections 3 (Style), 4 (Hard rules) and 5 (Corrections) in every reply. They override your defaults.
3. Use the values in section 8 exactly. Never round, re-estimate, or "correct" them.
4. Do not suggest anything in section 7 (Changed / rejected) again unless the user brings it up.
5. Code word: none active.
6. First reply: at most 5 lines covering goal, current state, next step (section 11). Ask the questions in section 12 only if they block the next step. End with "Ready to continue with <next step>?" and wait.

(Claude Code reading this from the repo mirror: these instructions are for claude.ai planning chats. Take your working rules from the root `CLAUDE.md`.)

## 1. Mission
- **Goal:** Plan, then build, "Living mythos": an observational god-view sandbox, "a terrarium you poke", "like a kid with an ant colony". Bands develop, change the land and each other, make history in unexpected ways; you watch, read the Legends, and nudge. Inspired by Dwarf Fortress worldgen + Legends. Not a game to win; not a copy of Earth's timeline.
- **v1 scope:** simple hunter-gatherer bands to the first farming villages, one procedural landmass, time from year 0. Long-term: a Roman-Empire-like civilization.
- **Success test:** "I trigger a drought and can read in the Legends why one band migrated and another died out." Stretch: fork the world before the drought. v1 passes without the fork.
- **Core loop:** live nudge and watch. Forks are a v1 stretch goal.
- **Current focus:** grilling the slice spec's open questions (Q8-Q14 left), then finalizing it so the laptop can build the systems.

## 2. About the user
- Jordan; hobbyist developer, Calgary. Laptop: Windows 11, i7-8665U, 16GB, integrated GPU; device `mobilebattlestation`, Node 25.3.0, pnpm 10.28.0. Also develops from a Pixel 10 Pro XL (often away from the laptop).
- Laptop repo clone: `C:\Users\User\Workspace\Repositories\the-living-mythos`. Claude Code CLI runs there.
- Claude app for planning, debugging by paste, learning. pnpm only. PowerShell chains with `;`; package.json scripts chain with `&&`.
- This chat lives in the claude.ai Project "Living mythos".

## 3. Style & communication
- English; senior peer; lead with assessment, not agreement; no filler, no emoji, no time estimates.
- Mobile-length replies; tables for options and comparisons.
- Grill format per question: options table, strongest counterargument, ≥2 failure modes, verdict/lean, external check, exact decision-log row. One question at a time.
- Separate known from inferred in the sentence; flag `[NEED: ]`, `[BLOCKED: ]`, `[UNCERTAIN: ]`.
- Jordan asks "verify claims and validity first" for consequential models: search the claims, and where a model's behaviour is the claim, run a throwaway prototype (scratchpad, floats fine, never sim code) and report what it actually does. Q7 showed this catches real problems.
- Jordan approved writing revisions to the Project log directly as decisions land.

## 4. Hard rules (word for word)
1. "Instead of using your usage for research give me the prompt to give to Gemini to do the deep research ... I can then upload the reports in the project for you to look over." When reviewing a report, spot-check key claims and say which were verified.
2. "Lead with assessment, not agreement. ... give the strongest counterargument first, name at least two genuine failure modes, then your verdict."
3. "Separate what you know from what you're inferring, in the sentence itself."
4. "When something is consequential, name the external check that would settle it."
5. "Rule of cool at the same time I want to balance realism." Simulation stays plausible; drama lives in presentation; never tune the sim for drama.
6. The 7 determinism hard rules in the decision log; tests before sim code.

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
| 10 | Proposed vegetation recovery of 1.5-2× drought length everywhere | Prompt 7: dry/grass land recovers in ≤ ~1× drought length; only wet/forest land is slower. The lasting shortage must come from game, not slowed plants |
| 11 | Spec said gradient noise needs trig | Fixed integer gradient table needs no trig (rev 18) |
| 12 | Proposed fauna model C without stability damping | Prototype showed boom-bust on rich land; density mortality `mDens` is required (rev 22) |

## 6. Decisions this handoff (details in decision log rev 17-22 and spec v0.8)
- Rev 17 (Q2): systems write per-season transition records; one emitter pass makes events in fixed order and attaches causes. World events use `ROOT_ID` primary with region/cell in the payload. Rev 12 ordinal confirmed.
- Rev 18 (Q3): gradient noise (integer gradient table, quintic fade, 4 octaves); radial edge falloff; sea at the 35% quantile; largest landmass only (slice; islands return as a world setting when sea travel exists, which Jordan wants later). Vegetation capacity continuous over base moisture × height penalty; 4×3 biome table is labels only.
- Rev 19 (Q4): climate anomaly = clamp(seasonal + volatility·space-time noise) − droughts; regions = climate-lattice blocks; dry spells with hysteresis; target ~15% of seasons dry per region, tune 12-18% (Jordan's numbers).
- Rev 20 (Q5): drought command: full strength to radius/2, linear fade to 0 at radius; commands stack after the natural clamp; presets mild/severe; default 8 seasons; instant onset. Rev 12 command causes confirmed.
- Rev 21 (Q6): vegetation: logistic below K; above K, V' = K + (V − K)(1 − dieBack); rV and dieBack piecewise-linear over base moisture (dry fast, wet slow); targets from the prompt 7 review.
- Rev 22 (Q7): large fauna: herd-condition model, Type II intake with a removal cap, births scaled by condition (rMax 0.04-0.06/season), deaths base + density (`mDens`, required) + starvation; condition-scaled diffusion with fixed substeps; capacity emerges from food; hunting Type II with a capped take.

## 7. Changed / rejected
See decision log "Rejected". Plus: per-biome carrying capacities (rev 18); global temporal climate noise (rev 19); hard-edged drought disc (rev 20); instant clamp of vegetation to K and a soil-moisture bucket in the slice (rev 21); logistic fauna on `cF·V` and fauna models without density mortality (rev 22); pure state-diff event detector (rev 17); the report's 12-28 season herd recovery (prototype: unreachable with stability; relaxed to 30-50 [UNCERTAIN]).

## 8. Data & facts (exact)
| Item | Value |
|---|---|
| Decision log | rev 22 |
| Spec | v0.8 (file `design/spec_v0.1.md`); Q0-Q7 settled; Q8-Q14 open, order in §20 |
| Repo head after this handoff's mirror commit | see `git log` (last decision commit `729e675`) |
| Tests | 67 pass, 1 todo, on Windows (no sim code changed this handoff) |
| RNG golden values | 1759517345 and 3421405739 (`rng.test.ts`). Never update casually |
| Map | slice default 128×128; catchment Euclidean disc r = 3 (29 cells) |
| Dry-spell share target | ~15% of seasons per region, tune 12-18% (rev 19) |
| Vegetation targets (severe drought, [P]) | dry: −45-70% in 1-2 seasons, 90% recovery in 0.5-1.2× drought length; wet: −25-45% over 2-5 seasons, 1.5-2.5× |
| Vegetation start endpoints | dry dieBack 0.40-0.60, rV 0.60-0.80; wet dieBack 0.10-0.20, rV 0.10-0.25 |
| Fauna rMax | 0.04-0.06/season (allometry: wildebeest 0.248/yr, buffalo 0.208, eland 0.150) |
| Fauna targets ([P]) | crash 25-75%; deaths start 1-3 seasons after onset; recovery 30-50 seasons [UNCERTAIN] |
| Prototype result (Q7) | without mDens: herds cycled 0.18-0.54 (richness 2), 0.20-1.07 (richness 4); mDens ≥ 0.05 stabilised all tested; 576-setting sweep: no stable setting with ≥25% crash recovered in < 30 seasons |
| Explicit diffusion | stable at h·D = 1/4, unstable at 0.26 (numerical check) |
| Prompt 7 review | `research/vegetation-drought-review-2026-10-30.md`; report text `research/vegetation-drought-report-gemini.txt`; PDF in repo `docs/research/` |
| Look test artifact | https://claude.ai/artifact/8TGrzjEVAJF1L2R669HcN5 (Version 5) |

## 9. People, terms & names
- Jordan. Gemini = external deep-research tool Jordan runs.
- "nudge", "Legends", "rule of cool", "crucibles", "ant-farm feel", "lab coat", "glance word", "camp snapshot", "the slice", "bloom", "the mirror" (repo `docs/`), "transition records" and "emitter" (rev 17), "condition index" (herd condition, rev 22), "die-back" (rev 21).
- Repo `shadepants/the-living-mythos` (private), branch `Main-REPO`.

## 10. Work state
| Item | Status | Location |
|---|---|---|
| Decision log | rev 22 | Project `design/decision-log.md`; mirrored |
| Spec | v0.8 draft; Q8-Q14 open | Project `design/spec_v0.1.md`; mirrored |
| sim-core | unchanged this handoff: rng, lint bans, config, lineage IDs, event log, tick loop; 67 tests + 1 todo | repo `packages/sim-core` |
| Doc workflow used this handoff | Claude (cloud session) cloned the repo, edited `docs/`, wrote the same files to the Project with `project_write` from the local path, made one `docs:` commit per decision and pushed. Jordan pulls on the laptop | — |
| Laptop | behind GitHub: needs `git pull` (fast-forward, docs only) | laptop clone |
| Q7 prototype scripts | throwaway, in the old session's scratchpad; likely gone. Findings recorded in the log and §8 | — |
| Project instructions | Settings text still has the old success-test wording | `claude/project-instructions.md` |

## 11. Next steps
1. **Grill spec Q8: food balance (yield, consumption, stash, hunger states)** (§9). Inputs: §8 hunting form (Type II, capped take); prompt 7 report's extra sections (unverified): low-latitude foragers hold 0-3 days of stored food, temperate/boreal collectors 1-2 seasons; bands broaden diet first, then move. Things to settle: labour weights, yield split across catchment cells (even vs nearest-first), stash cap and spoilage, hunger state thresholds, food trend band.
2. Then Q9-Q14 in §20 order, same format. After each pick: update spec and log (next rev), re-sync the mirror (one `docs:` commit), Jordan pulls.
3. Verify-first habit for models (section 3).
4. When all questions settle: spec-developer Phase 3 (finalize), then the laptop builds command log (rule 6), entity registry, then systems in spec §5 order.
5. Decide the rev 10 cloud gate (lean: lift with a Windows check before each sim merge).
6. Benchmarks once fields run. Parked: v5 Close-up rewatch; property norm.

## 12. Open questions
- Spec Q8-Q14.
- Rev 10 cloud gate.
- Stray Project doc `next-steps-prompts.md` at the Project root (duplicate of `claude/next-steps-prompts.md`): delete? Ask Jordan.
- Gemini stash on the laptop (`stash@{0}`): drop once Jordan agrees the archive copies are enough.
- [NEED: Jordan] paste `claude/project-instructions.md` into Project settings.
- Two suggested Gemini prompts not run (food storage, forager drought response); prompt 7's extra sections partly cover them.

## 13. Re-attach checklist
Nothing to attach inside the Project.
