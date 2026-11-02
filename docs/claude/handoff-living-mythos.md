# active-memory handoff: Living mythos (civilization simulation)

**Handoff #14** · 2026-11-02 · Lineage: #1 (2026-10-23): engine/stack research, scoping, grilling Q1-Q4, timescale research, Gemini novelty review · #2 (2026-10-23): Project set up, repo skeleton pushed · #3 (2026-10-24): reframe to "terrarium you poke", research batch reviewed, depth/visuals brainstorm, pixel-art look tests v1-v5, decision log rev 8 · #4 (2026-10-24 to 10-28): slice focus; forks = stretch; cloud sessions = tests/tooling; all brainstorm questions closed; decision log rev 11; Project docs consolidated · #5 (2026-10-30): laptop back and linked; Windows `pnpm check` passed; config, lineage IDs, event log built; Project docs mirrored into repo `docs/`; decision log rev 12 · #6 (2026-10-30): 64-bit rng key, tick loop, testing tooling; spec v0.1 drafted, Gemini agent's rewrite archived, spec v0.2; grilling Q0-Q1; decision log rev 16 · #7 (2026-10-30): spec grilling Q2-Q7 settled (revs 17-22); Gemini prompt 7 run and reviewed; fauna model validated in a throwaway prototype; spec v0.8 · #8 (2026-10-30 to 11-01): Q8 replaced by a whole-system review; Gemini prompts 8-11 run and reviewed; R1-R3 settled with prototypes (revs 23-25); spec v0.11; laptop screen broke · #9 (2026-11-01): R4 split into R4a-R4e and settled with prototypes (revs 26-30); 600-yr runs exposed that rev 25's baseline was a growth snapshot; whole-system review closed; spec v0.16 · #10 (2026-11-01): Q9 split into Q9a-Q9c and settled with prototypes (revs 31-33); calibrated demography fills maps in ~700 yr; cut-off bands never perished; spec v0.19 · #11 (2026-11-01): Q10 migration (rev 34) and Q11 die-out floor (rev 35); spec v0.21 · #12 (2026-11-01): Q12 event causes (rev 36: climate lookback `causeWindow`, shortfall episodes, outcome `dwindled`) and Q13 glance words (rev 37: severity first, well-fed from effort); prompt 12 report uploaded, review deferred to Q14; spec v0.23 · #13 (2026-11-01): prompt 12 reviewed (no decision changed); Q14 test scenario (rev 38: procedural filled map + local drought, no-drought control, templates, `stockPct` vs base capacity); all spec questions settled; spec v0.24 · #14 (2026-11-01 to 11-02): spec finalize (spec-developer Phase 3): consistency pass (rev 39), band-card food trend (rev 40), return-anchor calibration (rev 41); spec v0.27, v1.0 proposed; cloud gate lifted with a Windows check (rev 42); CI workflow added (startup_failure, account-level); PR #1 Purpose codes 6-12; interim Linux-verified merge rule (rev 43), PR #1 merged; independent audit of v0.27 (23 findings) fixed in spec v0.28 (revs 44-48)

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
- **Current focus:** scoped re-audit of spec v0.28, then v1.0 approval; cloud sim work under the rev 43 interim merge rule.

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
11. Spec finalize: "Propose v1.0 when the pass is done." (2026-11-01). Proposing is not approving: v1.0 waits for Jordan's explicit approval.

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
| 21 | Spec v0.8-v0.24 §7 still subtracted people's harvest from V and kept "shortage must come from game"; lifecycle had no system slot | Fixed in the v0.25 consistency pass (rev 39). Re-read whole sections after each decision, not just the changed lines |
| 22 | Rev 28 recorded fresh effort 0.55 at K2 (×1.5) | That was measured while bands settled new land; at the no-band herd equilibrium it is 0.38. Say which state a measurement comes from (rev 41) |
| 23 | The v0.25 consistency pass kept and worsened a double grazing subtraction, left "expected catchment return" undefined, and missed K = 0, negative counts and 64-bit payload IDs | An independent audit in a fresh session caught 23 issues the same-chat pass missed (revs 44-48). Self-review is not verification: run an independent audit before approving consequential docs |
| 24 | Spec §7 and §18 rules were written from memory of the prototype | Re-read the prototype code (`sysproto_q10.py`, `run5_q10.py`, `variants.py`) when writing a rule it is cited for |

## 6. Decisions this handoff (details in decision log revs 39-48 and spec v0.28)
| Decision | Why |
|---|---|
| Rev 39: finalize consistency pass. No decision reversed. `lifecycle` system after `migration` (dissolution → perishing → fission); `Purpose` 6-9 deaths, 10 `WorldgenHeight`, 11 `WorldgenMoisture`, 12 `ClimateSpaceTime`; config scale rule (counts as-is, rest `Per10k`); full §17 tunable table; plant stock P rule (cap `pFrac`·V); `stockPct` = plant stock ÷ `pFrac`·`Kveg` (game excluded); command and config errors; state table; future-consideration list | Spec had gaps and stale text from before rev 23 |
| Rev 40: band-card food trend = pressure now − 4 seasons ago (pressure = effort while fed, 1 + shortfall otherwise); `trendBand` 0.10; snapshot only | Option B. Calm 99.8% steady, flicker 0.01/band-yr, 36/36 hunger onsets warned (median 4 seasons ahead); v0.24 read rising 100% of calm seasons |
| Rev 41: return constants written by an offline calibration tool (fields-only burn-in ≥ 200 seasons on reference seeds; reference band at `effortFull` on median-`Kveg` land); slow test fails outside 0.45-0.55. Revises rev 28 from per world to reference worlds | Option C. Herd stock not proportional to K and settles in 37-173 seasons; per-world scaling swung 2× and would erase seed richness |
| Revs 44-48: audit fixes. 44 text fixes (grazing once via new `plant_food` system, K = 0 guard, survivors-only aging, proportional removal, sequential band order, executable acceptance, rev 31 check corrected); 45 dry spells read the natural anomaly + two-slot lookback; 46 expected return E (uncapped, labour per use, share only in migration); 47 payload IDs as Hi/Lo uint32; 48 initial world, starting bands, daughter state (stash split, `nonNegSeasons = stableSeasons`) | Independent audit 2026-11-02 (`design/spec-v1-audit-2026-11-02.md`): verdict do not approve v0.27; Claude re-checked all 6 blockers; leans taken under "proceed with suggested" |
| Rev 43: interim merge rule: Linux-verified merges while no Windows check exists; laptop runs the Windows check first on return | Option D. Billing blocks CI and Jordan can't update payment now; waiting (C) would stack 4-6 PRs |
| Rev 42: cloud gate lifted. Cloud and laptop may write sim logic; sim-core changes go on a branch and merge only after `pnpm check` passes on Windows (CI `windows-latest` or the laptop) plus a determinism-reviewer pass; docs and tooling may go straight to `Main-REPO` | Jordan's "cloud approval" = the lean. CI as the Windows check is Claude's fill-in (laptop screen broken). Linux `pnpm check` in the cloud matched Windows (67 + 1 todo) |

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
- ❌ Balance-based band-card trend; Δ-effort trend at band 0.05 (rev 40). ❌ Per-world return scaling at worldgen (rev 41). Not rejected: dropping the trend from the card (rev 40 D); hand-tuned return constants (rev 41 A, the fallback if the tool is late).
- Earlier rejections still stand: per-biome carrying capacities (rev 18); global temporal climate noise (rev 19); hard-edged drought disc (rev 20); instant clamp of vegetation to K (rev 21); logistic fauna on `cF·V` and fauna without density mortality (rev 22); pure state-diff event detector (rev 17).

## 8. Data & facts (exact)
| Item | Value |
|---|---|
| Decision log | rev 48 |
| Spec | v0.28 (file `design/spec_v0.1.md`); audit fixes applied (revs 44-48); re-audit pending, then v1.0 approval |
| Audit | `design/spec-v1-audit-2026-11-02.md`: 6 blockers, 11 majors, 6 minors, all addressed; re-audit variant in `claude/audit-prompt-spec-v1.md` |
| Integration review | `design/integration-review-2026-10-30.md`: closed rev 30; issues I1-I11 |
| Tests | 67 pass, 1 todo, on Windows (no sim code changed in handoffs #7-#12) |
| RNG golden values | 1759517345 and 3421405739 (`rng.test.ts`). Never update casually |
| Map | slice default 128×128; catchment Euclidean disc r = 3 (29 cells); ~3 km per cell |
| Home range | radius 5 cells [P] (81 cells); home cells ≥ `homeRange` apart (rev 27) |
| Band lifecycle [P] | `fissionAt` 50, `fissionMargin` 0.2 (fission and host guard), `dissolveAfter` 3 hungry seasons, `hostRange` 15 cells, `minViable` 5 (rev 35) |
| Migration [P] (rev 34) | `migrateAfter` 2, `searchRadius` 14, `travelCost` 0.05 per cell, `migrateMargin` 0.2; share weight linear 1 → 0 at 2·`catchment` (6 cells) |
| Events [P] (rev 36) | `stableSeasons` 2, `causeWindow` 8 seasons; outcomes perished / dissolved / dwindled |
| Food trend (rev 40) | pressure = effort while fed, 1 + shortfall otherwise; trend = now − 4 seasons ago; `trendBand` 0.10 [P] |
| Purpose codes (rev 39) | 1 ForageYield, 2 Migration (reserved), 3 Birth, 4 Death (retired), 5 Invention (reserved), 6-9 DeathChild/YoungAdult/Adult/Elder, 10 WorldgenHeight, 11 WorldgenMoisture, 12 ClimateSpaceTime. Only 1-5 exist in `rng.ts` |
| Config scale (rev 39) | integer counts as-is; everything else ×10,000 (`Per10k`); prototype values are in prototype units (rich K = 2) |
| Glance (rev 37) | starving > hungry > well-fed (effort ≤ `effortFull`) > settled; restless = band-card line |
| Regulation and anchor [P] | `effortFull` 0.5; fresh effort on median land = `effortFull`; prototype return ×1.5 over rev 23 values |
| Demography (rev 32-33) [P] | brackets 0-14 / 15-19 / 20-44 / 45+ (60 / 20 / 100 seasons / death only); base mortality per season 0.0126 / 0.0025 / 0.0028 / 0.0125; births 0.0475 per woman-season, fertile = young adults + adults; hunger mortality at total shortfall 0.25 / 0.10 / 0.10 / 0.35; intrinsic growth +0.86%/yr (prototype, no food limit) |
| Acceptance targets | density 0.45-1.35 per land cell; bands 25-50; background hunger ≤ 3%; meat share 30-50% |
| Hunt cap | `huntShare` 0.2 × `rMax` (≈ 0.01/season) |
| Guild starting values [P] | stash ≤ 0.5 seasons of consumption; spoilage 0.15-0.25/season; labour weights 0.25 / 0.75 / 1 / 0.5; need 0.6 / 1 / 1 / 0.8 (children / young adults / adults / elders) |
| Dry-spell share target | ~15% of seasons per region, tune 12-18% (rev 19) |
| Vegetation targets (severe drought, [P]) | dry: −45-70% in 1-2 seasons, 90% recovery in 0.5-1.2× drought length; wet: −25-45% over 2-5 seasons, 1.5-2.5× |
| Fauna | `rMax` 0.04-0.06/season; targets: crash 25-75%, onset 1-3 seasons, no extinction, above 50% within 200 seasons; recovery time diagnostic (prototype 21-194) |
| Finalize prototype results (shape only) | Trend (3 map seeds × 1.5, 1 × 0.9, 3 islands; plateau 0.66-0.73): B calm 99.8% steady, flicker 0.01, warned 36/36 map + 10/10 mag 0.9 + 5/5 island. Anchor (uniform K, no bands): F_eq 0.010 / 0.105 / 0.180 / 0.227 / 0.281 / 0.310 at K 0.6 / 1 / 1.5 / 2 / 3 / 4; settle 37-173 seasons; fresh effort at ×1.5 1.00 / 0.75 / 0.50 / 0.38 / 0.34 / 0.33; per-world scale 1.49 / 0.76 / 0.68 at median K 1 / 2 / 3 |
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
| Repo head | `Main-REPO` at `8c04472` (PR #1) + CONTEXT/handoff docs commit (see `git log`) |
| GitHub Actions (verified 2026-11-02, GitHub docs) | Free private repos: $12/month included compute; Linux $0.006/min, Windows $0.010/min (≈ 1,200 Windows min/month) |
| Look test artifact | https://claude.ai/artifact/8TGrzjEVAJF1L2R669HcN5 (Version 5) |

## 9. People, terms & names
- **People:** Jordan. Gemini = external deep-research tool Jordan runs.
- **Terms:** "nudge", "Legends", "rule of cool", "crucibles", "ant-farm feel", "lab coat", "glance word", "camp snapshot", "the slice", "bloom", "the mirror" (repo `docs/`), "transition records" and "emitter" (rev 17), "condition index" (rev 22), "die-back" (rev 21), "guild" (rev 23), "home range" and "camp" (rev 24), "fission", "dissolution", "perished" (rev 25), "host guard" (rev 26), "effort" and "fresh effort" (revs 27-28), "filled map" (= density plateau), "shortfall" (rev 33), "cut-off band" / island scenario (Q9c), "shortfall episode", "causeWindow", "dwindled" (rev 36), "well-fed" (rev 37), "pressure" (rev 40), "calibration tool" / "reference band" (rev 41).
- **Names in use:** repo `shadepants/the-living-mythos` (private), branch `Main-REPO`; prototype folders under `research/prototypes/`: `q7-fauna/`, `q8-system/` (R4 in `r4/`), `q9-demography/`, `q10-migration/`, `q11-minviable/`, `q12-events/`, `q13-glance/`, `q14-scenario/`, `finalize-trend/`, `finalize-anchor/`.

## 10. Work state
| Item | Status | Location | Notes |
|---|---|---|---|
| Decision log | rev 48 | Project `design/decision-log.md`; mirrored | — |
| Spec | v0.28 draft, v1.0 candidate | Project `design/spec_v0.1.md`; mirrored | Re-audit (scoped variant), fix anything it finds, then Version 1.0 / Approved |
| Gemini prompts | 1-12 run and reviewed; 13-15 suggested | `research/gemini-prompts.md` | Prompt 12 review: `research/famine-outcomes-review-2026-11-01.md` |
| Prototypes | throwaway Python; never port | `research/prototypes/` (READMEs list each script) | Latest: `finalize-anchor/`, `finalize-trend/` (streams from `q13-glance/q13run.py`), `q14-scenario/` (`q14run.py` adds fixtures, mag-0 controls, `pbase`; `q14chain.py` = pass check + sentence rendering). A full map run (1,200 yr + 60) is ~2-4 min; 2 in parallel on 2 cores |
| sim-core | unchanged: rng, lint bans, config, lineage IDs, event log, tick loop; 67 tests + 1 todo | repo `packages/sim-core` | Entity registry needed early (fission creates bands). Pending from rev 31: append the 4 death purposes; fast-check tests for the binomial sampler — tests only, so cloud-eligible under rev 10 |
| Doc workflow | cloud session: `add_repo` (push) then `git clone --depth 1 -b Main-REPO`; edit `docs/`; `project_write` from local paths; one `docs:` commit per decision; fetch + rebase; push | — | `gh repo clone` fails (GraphQL blocked) |
| Laptop | screen broken; behind GitHub (docs only, fast-forward) | laptop clone | Needs repair or an external monitor before pulling or sim code |
| Repo `CLAUDE.md` | updated 2026-11-02: rev 42 gate text, rule 4 built | repo root | — |
| CI `check` workflow | `.github/workflows/check.yml`: `pnpm check` on windows-latest + ubuntu-latest, every push and PR, GitHub-made actions + corepack | repo | Every run so far: `startup_failure`, 0 jobs, also after removing the third-party action. Cause confirmed by Jordan 2026-11-02: GitHub billing issue on the account Jordan can't update payment for now (2026-11-02), so the workflow is manual-only (`workflow_dispatch`) to stop red runs on every push; restore the push/PR triggers noted in the file once billing is fixed. Until then the laptop is the only Windows check (rev 42) |
| PR #1 `Purpose` 6-12 | merged 2026-11-02 as `8c04472` (squash), Linux-verified only (rev 43) | `Main-REPO` | Covered by the laptop's first Windows check |
| Dependabot | 1 moderate alert on `Main-REPO` | repo Security tab | Not reviewed |
| Project instructions | Settings text still has the old success-test wording | `claude/project-instructions.md` | [NEED: Jordan] paste |

## 11. Next steps
1. **Next action:** run the re-audit variant of `claude/audit-prompt-spec-v1.md` in a fresh session; fix its findings; then Jordan approves spec v1.0 (Version 1.0, Status Approved, changelog v1.0, decision-log header note; sync and push).
2. Interim merge rule (rev 43): sim-core PRs merge on green Linux `pnpm check` + clean determinism review, commit notes "Linux-verified only". When the laptop returns: Windows `pnpm check` on `Main-REPO` first. When billing is fixed: restore the `check` workflow's push/PR triggers (noted in the file); that also ends rev 43.
3. Cloud sim work (rev 42), each on its own branch and PR, tests first: binomial sampler + fast-check tests (exact pmf, monotone in q, never n at u = 1 − 2^-32); command log (hard rule 6) with §20 validation; entity registry. Then systems in spec §5 order, calibration tool + slow test, Legends templates, acceptance test (slow-tagged). The `determinism-rules` skill and `determinism-reviewer` run on every sim-core diff.
4. Open tuning gaps (batch tuning, not decisions): herd crash 12-25% vs 25-75% target; K2 density near the floor; slow 2-band fill; post-drought refuge crowding; causeless and window-edge `forage_failed`; glance word share vs `effortFull`; die-out rate vs the `searchRadius`/`hostRange` gap (never retune radii to pass the test); trend with a seasonal cycle (rev 40); seed spread of median `Kveg` (rev 41).
5. Candidate Gemini prompts 13-15 (`research/gemini-prompts.md`); possible new one on band fusion and minimum residential group size. Parked: v5 Close-up rewatch; property norm; benchmarks once fields run; Dependabot alert.

## 12. Open questions
- Re-audit of spec v0.28, then v1.0 approval [NEED: Jordan].
- CI blocked by a GitHub billing issue; Jordan can't update payment for now (rev 43 covers it). Independent audit of the v1.0 candidate: `claude/audit-prompt-spec-v1.md`, run in a fresh session before approving.
- Stray Project doc `next-steps-prompts.md` at the Project root (duplicate of `claude/next-steps-prompts.md`): delete? Ask Jordan.
- Gemini stash on the laptop (`stash@{0}`): drop once Jordan agrees the archive copies are enough.
- [NEED: Jordan] paste `claude/project-instructions.md` into Project settings.

## 13. Re-attach checklist
Nothing to attach inside the Project (the prompt 12 PDF is a Project file).

---
<sub>Audit: 13/13 sections · 11 rules · 22 corrections · 48 data points · secrets removed: none found · generated by active-memory (handoff #14)</sub>
