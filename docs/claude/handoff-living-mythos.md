# active-memory handoff: Living mythos (civilization simulation)

**Handoff #13** · 2026-11-01 · Lineage: #1 (2026-10-23): engine/stack research, scoping, grilling Q1-Q4, timescale research, Gemini novelty review · #2 (2026-10-23): Project set up, repo skeleton pushed · #3 (2026-10-24): reframe to "terrarium you poke", research batch reviewed, depth/visuals brainstorm, pixel-art look tests v1-v5, decision log rev 8 · #4 (2026-10-24 to 10-28): slice focus; forks = stretch; cloud sessions = tests/tooling; all brainstorm questions closed; decision log rev 11; Project docs consolidated · #5 (2026-10-30): laptop back and linked; Windows `pnpm check` passed; config, lineage IDs, event log built; Project docs mirrored into repo `docs/`; decision log rev 12 · #6 (2026-10-30): 64-bit rng key, tick loop, testing tooling; spec v0.1 drafted, Gemini agent's rewrite archived, spec v0.2; grilling Q0-Q1; decision log rev 16 · #7 (2026-10-30): spec grilling Q2-Q7 settled (revs 17-22); Gemini prompt 7 run and reviewed; fauna model validated in a throwaway prototype; spec v0.8 · #8 (2026-10-30 to 11-01): Q8 replaced by a whole-system review; Gemini prompts 8-11 run and reviewed; R1-R3 settled with prototypes (revs 23-25); spec v0.11; laptop screen broke · #9 (2026-11-01): R4 split into R4a-R4e and settled with prototypes (revs 26-30); 600-yr runs exposed that rev 25's baseline was a growth snapshot; whole-system review closed; spec v0.16 · #10 (2026-11-01): Q9 split into Q9a-Q9c and settled with prototypes (revs 31-33); calibrated demography fills maps in ~700 yr; cut-off bands never perished; spec v0.19 · #11 (2026-11-01): Q10 migration (rev 34) and Q11 die-out floor (rev 35); spec v0.21 · #12 (2026-11-01): Q12 event causes (rev 36: climate lookback `causeWindow`, shortfall episodes, outcome `dwindled`) and Q13 glance words (rev 37: severity first, well-fed from effort); prompt 12 report uploaded, review deferred to Q14; spec v0.23 · #13 (2026-11-01): prompt 12 reviewed (no decision changed); Q14 test scenario (rev 38: procedural filled map + local drought, no-drought control, templates, `stockPct` vs base capacity); all spec questions settled; spec v0.24

## 0. Instructions for Claude (read first)

You are continuing work from a previous chat. That chat is gone; this file plus `design/decision-log.md` and `design/spec_v0.1.md` is the complete context (`design/integration-review-2026-10-30.md` is closed and kept as evidence). Where they disagree, the decision log wins for decisions; this file wins for work state and next steps.

1. Read this whole file before replying.
2. Follow sections 3 (Style), 4 (Hard rules) and 5 (Corrections) in every reply. They override your defaults.
3. Use the values in section 8 exactly. Never round, re-estimate, or "correct" them.
4. Do not suggest anything in section 7 (Changed / rejected) again unless the user brings it up.
5. Code word: none active. If the user types /amcodeword, start every reply with the phrase they choose (default "Yes Boss!").
6. First reply: at most 5 lines covering goal, current state, next step (section 11). Ask the questions in section 12 only if they block the next step. If the user's opening message already says to continue, start the next step in that reply instead of waiting.

(Claude Code reading this from the repo mirror: these instructions are for claude.ai planning chats. Take your working rules from the root `CLAUDE.md`.)

## 1. Mission
- **Goal:** Plan, then build, "Living mythos": an observational god-view sandbox, "a terrarium you poke", "like a kid with an ant colony". Bands develop, change the land and each other, make history in unexpected ways; you watch, read the Legends, and nudge. Inspired by Dwarf Fortress worldgen + Legends. Not a game to win; not a copy of Earth's timeline.
- **v1 scope:** simple hunter-gatherer bands to the first farming villages, one procedural landmass, time from year 0. Long-term: a Roman-Empire-like civilization.
- **Success test:** "I trigger a drought and can read in the Legends why one band migrated and another died out." Stretch: fork the world before the drought. v1 passes without the fork.
- **Core loop:** live nudge and watch. Forks are a v1 stretch goal.
- **Current focus:** finalize the spec (spec-developer Phase 3, including the band-card food trend), so the laptop can build the systems.

## 2. About the user
- Jordan; hobbyist developer, Calgary. Laptop: Windows 11, i7-8665U, 16GB, integrated GPU; device `mobilebattlestation`, Node 25.3.0, pnpm 10.28.0. **Laptop screen broke on 2026-10-31**; not usable until repaired or connected to an external monitor. Also develops from a Pixel 10 Pro XL.
- Laptop repo clone: `C:\Users\User\Workspace\Repositories\the-living-mythos`. Claude Code CLI runs there.
- Claude app for planning, debugging by paste, learning. pnpm only. PowerShell chains with `;`; package.json scripts chain with `&&`.
- This chat lives in the claude.ai Project "Living mythos".

## 3. Style & communication
- **Language:** English.
- **Tone:** senior peer; lead with assessment, not agreement; no filler, no emoji, no time estimates.
- **Reply length:** mobile-length; tables for options and comparisons.
- **Grill format, per question:** options table, strongest counterargument, ≥2 failure modes, verdict/lean, external check, exact decision-log row. One question at a time.
- **Known vs inferred:** separate in the sentence; flag `[NEED: ]`, `[BLOCKED: ]`, `[UNCERTAIN: ]`.
- **Verify first:** for consequential models, spot-check the claims (a quick search to verify a cited figure is fine; deep research goes to Gemini), and where a model's behaviour is the claim, run a throwaway prototype (scratchpad, Python floats, never sim code) and report what it actually does before Jordan picks. Q7, R2, R3, every R4 part, Q12 and Q13 caught real problems this way.
- **Run long enough:** lifecycle and population checks run on a filled map, to a density plateau (1,200 years from a 2-band start; print density per century to confirm). Plateau ~0.66-0.72 per rich cell from century 8-10.
- **Check against streams:** for rules that read sim output (events, glance words), dump per-season facts once and apply rule variants offline (`q12run.py`/`q13run.py` pattern).
- **After each pick:** update the decision log (next rev), the spec (next minor version) and the Project index (`claude/README.md`); file prototype scripts under `research/prototypes/`; write the same files to the Project (`project_write` with `local_path`); re-sync the repo mirror in one `docs:` commit and push. Jordan pulls on the laptop. Jordan approved writing revisions directly as decisions land ("Proceed with suggested" = pick the lean).
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
8. "For consequential models, verify claims and run a throwaway prototype before I pick. ... Run on a filled map to a density plateau (1,200 years; print density per century to confirm) plus the island scenario. ... After each pick, update the spec, decision log and index, file prototype scripts, re-sync the repo mirror in one docs commit, and push. My laptop screen is still broken, so flag anything that needs the laptop. "Proceed with suggested" means take your lean. Offer a handoff refresh before the chat gets long." (2026-11-01)
9. "Never tune the sim for drama." Restated 2026-11-01: die-out may be dissolution-led; do not lower drought floors or raise `minViable` to manufacture perishing; Q14 must not tune the sim for drama.
10. Prompt 12 report: "Unless it bears context to anything before q14 wait til then" (2026-11-01). Done: reviewed at the start of Q14 (handoff #13).

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
| 13 | Grilled Q8 (food balance) in isolation as a formula choice | Jordan: research better solutions, revise earlier decisions if needed (rule 7). Led to the whole-system review |
| 14 | Spec v0.8 §9 fed people vegetation V directly | V is herbivore forage; people eat guild stocks (rev 23) |
| 15 | Rev 21 note: "a lasting post-drought shortage must come from game" | Prototypes: plants backfilled; outcomes hinge on band size, migration scoring, hunger mortality and refuge occupancy |
| 16 | Rev 25's "quiet baseline" from seasons 400-600 of run5 | That was the growth phase; once full, the rules cycled every ~150 yr. Run lifecycle checks on a filled map (rev 26) |
| 17 | Spec v0.16 binomial flip (q > 0.5) reused the same u | Not monotone in q (2,838 violations in 1.19M checks); flip with 1 − u (rev 31) |
| 18 | "Filled map = ≥ 600 years" | Calibrated demography (rev 32) fills a 2-band start by ~century 7-10. Run to a density plateau |
| 19 | Q9 prototypes reverted any migration whose new home was within `homeRange` of another home (a rule the spec never had) | It was the suppressor. Check a prototype's own extra rules before blaming the model (rev 34) |
| 20 | Q12-Q13 prototypes measured `stockPct` against the drought-lowered capacity | Read 30-66% for bands at 10-11% of normal; Legends need base capacity (rev 38) |

## 6. Decisions this handoff (details in decision log revs 36-37 and spec v0.23)
| Decision | Why |
|---|---|
| Prompt 12 reviewed (`research/famine-outcomes-review-2026-11-01.md`) | No decision changed. Supports revs 26, 33, 35. Flags: `dwindled` is an artifact of deferred fusion (word it as breaking up); real dispersal splits families among several hosts (revisit with relations) |
| Rev 38 (Q14): procedural slice world, seed from the rev 16 refuge check (never by outcome), 2-band start to the plateau (1,200 yr [P]), severe local drought (8 seasons, radius 20 [P], centred near the bands' centroid [P]). Pass: ≥ 1 `band_migrated` and ≥ 1 non-`dwindled` `band_died_out` in [start, end + `causeWindow`], each ≤ 3 hops, both sentences render; same seed with no drought shows neither. 20-seed pass rate reported, not a gate. `stockPct` vs base capacity. Templates in spec §15 | Option B. Filled map 5/6 pass, controls 3/3 clean, island 0/5, hand-built fixtures 0/9 (needs geometry tuned to the outcome). 3/8 dissolution hosts in the 14-15 radius gap (risk, do not retune for the test) |

## 7. Changed / rejected
See decision log "Rejected". Plus:
- Spec Q8 as a standalone food formula → whole-system review R1-R4 (closed rev 30).
- ❌ Hard-coded food channels; people eating V directly (rev 23).
- ❌ Dual (protein/fat) currency in the slice: deferred to farming, not rejected.
- ❌ Fixed camp and whole-home-range footprint (R2 options A and C).
- ❌ Fission without dissolution; fission without a viability guard (rev 25).
- ❌ Hosts accepting refugees they cannot feed (R4a option A); refugees split among hosts (R4a C, not needed).
- ❌ Hunger as the only population regulator (R4b A); density-dependent human mortality as the regulator (R4b C; kept only as an untested B + weak C tuning fallback).
- ❌ Calibrating to Kaplan production at full labour (R4c B); fitting constants to targets (R4c C, R4d C).
- ❌ Fixed hunt cap without a basis (R4d A).
- ❌ Herd recovery-time target, both 30-50 and 40-100 seasons (rev 30).
- Prey depression: tested, no clear effect; deferred (not rejected).
- ❌ Home-spacing rule on migration targets (rev 34). ❌ Die-out floor ≥ 10; lowering the drought capacity floor to force perishing (rev 35). Not rejected: standing-stock overlap scoring (Q10 B).
- ❌ Deterministic expected-value demography; per-member draws (rev 31). ❌ Hunger mortality by hunger state alone (rev 33). Not rejected: draft cuts (Q9b A), hidden stages (Q9b B, upgrade path), adults-only fertility (Q9b D); priority feeding (Q9c C, not prototyped).
- ❌ Climate causes only while active; reason thresholds inside the sim (rev 36). Not rejected: new cause events `range_depleted`, `band_dwindling`, arrival-crowding causes (Q12 C; wait for batch runs).
- ❌ restless above starving; glance words from the balance-based trend (rev 37). Not rejected: glance hysteresis (Q13; 0.02 vs 0.06 flicker, not worth a tunable now); a `lean` word (0-0.1% of seasons).
- ❌ Hand-built fixture as the acceptance scenario; pass-rate gate; `stockPct` vs drought-lowered capacity (rev 38).
- Earlier rejections still stand: per-biome carrying capacities (rev 18); global temporal climate noise (rev 19); hard-edged drought disc (rev 20); instant clamp of vegetation to K (rev 21); logistic fauna on `cF·V` and fauna without density mortality (rev 22); pure state-diff event detector (rev 17).

## 8. Data & facts (exact)
| Item | Value |
|---|---|
| Decision log | rev 38 |
| Spec | v0.24 (file `design/spec_v0.1.md`); all questions settled (Q14 rev 38); finalize next |
| Integration review | `design/integration-review-2026-10-30.md`: closed rev 30; issues I1-I11 |
| Tests | 67 pass, 1 todo, on Windows (no sim code changed in handoffs #7-#12) |
| RNG golden values | 1759517345 and 3421405739 (`rng.test.ts`). Never update casually |
| Map | slice default 128×128; catchment Euclidean disc r = 3 (29 cells); ~3 km per cell |
| Home range | radius 5 cells [P] (81 cells); home cells ≥ `homeRange` apart (rev 27) |
| Band lifecycle [P] | `fissionAt` 50, `fissionMargin` 0.2 (fission and host guard), `dissolveAfter` 3 hungry seasons, `hostRange` 15 cells, `minViable` 5 (rev 35) |
| Migration [P] (rev 34) | `migrateAfter` 2, `searchRadius` 14, `travelCost` 0.05 per cell, `migrateMargin` 0.2; share weight linear 1 → 0 at 2·`catchment` (6 cells) |
| Events [P] (rev 36) | `stableSeasons` 2, `causeWindow` 8 seasons; outcomes perished / dissolved / dwindled |
| Glance (rev 37) | starving > hungry > well-fed (effort ≤ `effortFull`) > settled; restless = band-card line |
| Regulation and anchor [P] | `effortFull` 0.5; fresh effort on median land = `effortFull`; prototype return ×1.5 over rev 23 values |
| Demography (rev 32-33) [P] | brackets 0-14 / 15-19 / 20-44 / 45+ (60 / 20 / 100 seasons / death only); base mortality per season 0.0126 / 0.0025 / 0.0028 / 0.0125; births 0.0475 per woman-season, fertile = young adults + adults; hunger mortality at total shortfall 0.25 / 0.10 / 0.10 / 0.35; intrinsic growth +0.86%/yr (prototype, no food limit) |
| Acceptance targets | density 0.45-1.35 per land cell; bands 25-50; background hunger ≤ 3%; meat share 30-50% |
| Hunt cap | `huntShare` 0.2 × `rMax` (≈ 0.01/season) |
| Guild starting values [P] | stash ≤ 0.5 seasons of consumption; spoilage 0.15-0.25/season; labour weights 0.25 / 0.75 / 1 / 0.5; need 0.6 / 1 / 1 / 0.8 (children / young adults / adults / elders) |
| Dry-spell share target | ~15% of seasons per region, tune 12-18% (rev 19) |
| Vegetation targets (severe drought, [P]) | dry: −45-70% in 1-2 seasons, 90% recovery in 0.5-1.2× drought length; wet: −25-45% over 2-5 seasons, 1.5-2.5× |
| Fauna | `rMax` 0.04-0.06/season; targets: crash 25-75%, onset 1-3 seasons, no extinction, above 50% within 200 seasons; recovery time diagnostic (prototype 21-194) |
| Q14 prototype results (shape only) | Plateau 0.66-0.73 per rich cell from century 8-10 (seeds 1-3). Filled map + local drought: 5/6 pass (fail seed 1 mag 0.9); 2-8 migrations, 0-2 dissolutions per run, all 2 hops. Controls (mag 0, same history) 0 outcomes 3/3. Island 0/5. Fixtures 0/9. Dissolution host distances: 3 at 14.1-14.3, 3 at 1.0-1.4, 1 at 12.6 (8 incl. one shared history). `stockPct` vs base 10-11% where drought-capacity basis read 48-57% |
| Q12-Q13 prototype results (shape only) | Plateau 0.66-0.72 per rich cell from century 8-10 (seeds 1-3, 1,200 yr; runs reproduce exactly). Drought window, 6 runs: 31 migrations, 8 dissolutions, all 2 hops to `drought_began`; causeless `forage_failed` 15/83 (active-only) → 4 (window 4) → 2 (window 8, 16). Calm plateau: 0 `forage_failed`; balance +0.11-0.14 × consumption, stash 0.36-0.39 × consumption, effort median 0.60 (p5-p95 0.47-0.67), 8-9% at ≤ `effortFull`. 3 calm perishings in 3,600 band-years (hunger 0, drift ~10 → 5). restless ⊂ starving 120/120. Island: 0 endings, 0 causeless failures |
| Q10-Q11 prototype results (shape only) | Migrations per 8-season drought: mag 0.9 C 2/6/4, mag 1.5 7/9/9; 0 in 200 calm years; island 0. Islands at capacity floor 0.2 bottom at 12-24 people; floor 5 perished 0/5 at 0.2, 1/5 at 0.1 and 0.05, 5/5 at 0. Bands below floor per 200 yr (calm / drought): 5 → 0-1 / 0-1, 10 → 2-3 / 0-5, 12 → 4-6 / 1-5 |
| Q9 prototype results (3 seeds, shape only) | rev 32 rates: K2 filled by century 7 at 0.50/cell; cut-off band (island, 12-season drought, magnitude 0.9-1.5) −3-59%, settles at 12-20 people, never perished |
| R4 prototype results (1-2 seeds, shape only) | rev 26 rules + ×1.5 return: K2 0.77/cell, K4 1.60/cell; filled-map drought crash 12-25% (below target); cap 0.02 gave 2 perished bands |
| Island scenario note | 2 of 5 island seeds hold 2 bands at the drought (fission before onset); both go hungry together, so neither can host the other |
| Verified handoff #13 | Garry Lake 1957-58: 58 died, 31 airlifted (Wikipedia, citing Bouchard 1987, Tester & Kulchyski 1994); Henik Lake: 59 moved 1957 (Wikipedia "Kikkik"); Tsimane incapacitated ~10% of days (Gurven et al. 2012 via PMC7744098); Cashdan 1983 exists (*CA* 24:47-66). Conflicting: Nueltin move 1949 vs 1950; St. Lawrence Island counts |
| Verified handoff #11 | Lee 1972 via Peaceful Societies summary: !Kung boundaries vague and undefended; frequent visits with food sharing (primary not read) |
| Verified handoff #10 | Gurven & Kaplan 2007 (l15 0.57, adult mortality ~1%/yr to 40 then Gompertz, modal adult death 72 (68-78), forager TFR mean 5.7); Walker et al. 2006 (age at first reproduction ~19.2, menarche ~14.7) |
| Verified handoff #9 | Kaplan et al. 2000 Table 2; ovarian function sensitive to energetic conditions (Harvard Reproductive Ecology Lab); Robinson & Redford approach (CITES guidance); Kruger buffalo ~32,000 → ~14-15,000 after the early-1990s drought |
| Unverified | Prompt 8 famine age shape; per-bracket mortality averages read from G&K's curve; prompt 8 claim that stressed hosts refuse refugees (Cashdan 1983 found, not read); workload → fertility link and shape; Robinson & Redford formula; ungulate recovery times; handoff #8's list (St. Lawrence Island, Binford storage threshold, 85-90% dissolution share, Binford packing threshold) |
| Repo head | rev 38 + handoff #13 docs commit follows `6efe1a2` (see `git log`) |
| Look test artifact | https://claude.ai/artifact/8TGrzjEVAJF1L2R669HcN5 (Version 5) |

## 9. People, terms & names
- **People:** Jordan. Gemini = external deep-research tool Jordan runs.
- **Terms:** "nudge", "Legends", "rule of cool", "crucibles", "ant-farm feel", "lab coat", "glance word", "camp snapshot", "the slice", "bloom", "the mirror" (repo `docs/`), "transition records" and "emitter" (rev 17), "condition index" (rev 22), "die-back" (rev 21), "guild" (rev 23), "home range" and "camp" (rev 24), "fission", "dissolution", "perished" (rev 25), "host guard" (rev 26), "effort" and "fresh effort" (revs 27-28), "filled map" (= density plateau), "shortfall" (rev 33), "cut-off band" / island scenario (Q9c), "shortfall episode", "causeWindow", "dwindled" (rev 36), "well-fed" (rev 37).
- **Names in use:** repo `shadepants/the-living-mythos` (private), branch `Main-REPO`; prototype folders under `research/prototypes/`: `q7-fauna/`, `q8-system/` (R4 in `r4/`), `q9-demography/`, `q10-migration/`, `q11-minviable/`, `q12-events/`, `q13-glance/`.

## 10. Work state
| Item | Status | Location | Notes |
|---|---|---|---|
| Decision log | rev 38 | Project `design/decision-log.md`; mirrored | — |
| Spec | v0.24 draft | Project `design/spec_v0.1.md`; mirrored | All questions settled; finalize next; §16 food trend defect still open |
| Gemini prompts | 1-12 run and reviewed; 13-15 suggested | `research/gemini-prompts.md` | Prompt 12 review: `research/famine-outcomes-review-2026-11-01.md` |
| Prototypes | throwaway Python; never port | `research/prototypes/` (READMEs list each script) | Latest: `q14-scenario/` (`q14run.py` adds fixtures, mag-0 controls, `pbase`; `q14chain.py` = pass check + sentence rendering). A full map run (1,200 yr + 60) is ~2-4 min; 2 in parallel on 2 cores |
| sim-core | unchanged: rng, lint bans, config, lineage IDs, event log, tick loop; 67 tests + 1 todo | repo `packages/sim-core` | Entity registry needed early (fission creates bands). Pending from rev 31: append the 4 death purposes; fast-check tests for the binomial sampler — tests only, so cloud-eligible under rev 10 |
| Doc workflow | cloud session: `add_repo` (push) then `git clone --depth 1 -b Main-REPO`; edit `docs/`; `project_write` from local paths; one `docs:` commit per decision; fetch + rebase; push | — | `gh repo clone` fails (GraphQL blocked) |
| Laptop | screen broken; behind GitHub (docs only, fast-forward) | laptop clone | Needs repair or an external monitor before pulling or sim code |
| Project instructions | Settings text still has the old success-test wording | `claude/project-instructions.md` | [NEED: Jordan] paste |

## 11. Next steps
1. **Next action:** spec finalize (spec-developer Phase 3) on `design/spec_v0.1.md` v0.24: consistency pass across sections, every tunable listed in §17 with scale and tag, resolve the §16 band-card food trend (candidate: 4-season change in effort) [NEED: Jordan], drop stale rough-draft notes, bump to v1.0 when Jordan approves.
2. Then the laptop builds, in order: command log (rule 6), entity registry, then systems in spec §5 order; Q14 acceptance test last (slow-tagged until keyframes).
3. Open tuning gaps (batch tuning, not decisions): herd crash 12-25% vs 25-75% target; K2 density near the floor; slow 2-band fill; post-drought refuge crowding; causeless and window-edge `forage_failed`; glance word share vs `effortFull`; die-out rate vs the `searchRadius`/`hostRange` gap (rev 38; never retune radii to pass the test).
4. Candidate Gemini prompts 13-15 (`research/gemini-prompts.md`): access to neighbours' ranges in drought; fertility vs workload; time allocation. Possible new one: band fusion and minimum residential group size (prompt 12 flagged fusion as the realistic end for small bands).
5. Decide the rev 10 cloud gate (lean: lift with a Windows check before each sim merge). Benchmarks once fields run. Parked: v5 Close-up rewatch; property norm.

## 12. Open questions
- §16 band-card food trend definition (at finalize).
- Rev 10 cloud gate: lift as written / keep / lift with a Windows check before each sim merge (lean). The broken laptop screen blocks sim work until decided or repaired.
- Stray Project doc `next-steps-prompts.md` at the Project root (duplicate of `claude/next-steps-prompts.md`): delete? Ask Jordan.
- Gemini stash on the laptop (`stash@{0}`): drop once Jordan agrees the archive copies are enough.
- [NEED: Jordan] paste `claude/project-instructions.md` into Project settings.

## 13. Re-attach checklist
Nothing to attach inside the Project (the prompt 12 PDF is a Project file).

---
<sub>Audit: 13/13 sections · 10 rules · 20 corrections · 44 data points · secrets removed: none found · generated by active-memory (handoff #13)</sub>
