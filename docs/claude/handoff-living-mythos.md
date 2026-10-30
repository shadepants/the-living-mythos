# active-memory handoff: Living mythos (civilization simulation)

**Handoff #6** · 2026-10-30 · Lineage: #1 (2026-10-23): engine/stack research, scoping, grilling Q1-Q4, timescale research, Gemini novelty review · #2 (2026-10-23): Project set up, repo skeleton pushed · #3 (2026-10-24): reframe to "terrarium you poke", research batch reviewed, depth/visuals brainstorm, pixel-art look tests v1-v5, decision log rev 8 · #4 (2026-10-24 to 10-28): slice focus; forks = stretch; cloud sessions = tests/tooling; all brainstorm questions closed; decision log rev 11; Project docs consolidated · #5 (2026-10-30): laptop back and linked; Windows `pnpm check` passed; laptop session built config, lineage IDs and event log; Project docs mirrored into repo `docs/`; repo `CLAUDE.md`/`README.md` brought up to date; TS range fixed; decision log rev 12 · #6 (2026-10-30): 64-bit rng key, tick loop and testing tooling built; spec v0.1 drafted, a Gemini agent's unapproved "finalized" rewrite archived as a rough draft, 4 real bugs fixed (spec v0.2); grilling started in dependency order: Q0 and Q1 settled; decision log rev 16

## 0. Instructions for Claude (read first)

You are continuing work from a previous chat. That chat is gone; this file plus `design/decision-log.md` is the complete context. Where they disagree, the decision log wins for decisions; this file wins for work state and next steps.

1. Read this whole file before replying.
2. Follow sections 3 (Style), 4 (Hard rules) and 5 (Corrections) in every reply. They override your defaults.
3. Use the values in section 8 exactly. Never round, re-estimate, or "correct" them.
4. Do not suggest anything in section 7 (Changed / rejected) again unless the user brings it up.
5. Code word: none active.
6. First reply: at most 5 lines covering goal, current state, next step (section 11). Ask the questions in section 12. End with "Ready to continue with <next step>?" and wait.

(Claude Code reading this from the repo mirror: these instructions are for claude.ai planning chats. Take your working rules from the root `CLAUDE.md`.)

## 1. Mission
- **Goal:** Plan, then build, "Living mythos": an observational god-view sandbox, "a terrarium you poke", "like a kid with an ant colony". Bands develop, change the land and each other, make history in unexpected ways; you watch, read the Legends, and nudge. Inspired by Dwarf Fortress worldgen + Legends. Not a game to win; not a copy of Earth's timeline.
- **v1 scope:** simple hunter-gatherer bands to the first farming villages, one procedural landmass, time from year 0. Long-term: a Roman-Empire-like civilization.
- **Success test:** "I trigger a drought and can read in the Legends why one band migrated and another died out." Stretch: fork the world before the drought. v1 passes without the fork.
- **Core loop:** live nudge and watch. Forks are a v1 stretch goal (option C, 2026-10-24).
- **Current focus:** the success-test slice. The deterministic foundations are built; the tick loop and the slice spec are next.

## 2. About the user
- Jordan; hobbyist developer, Calgary. Laptop is back (Windows 11, i7-8665U, 16GB, integrated GPU; device name `mobilebattlestation`, Node 25.3.0, pnpm 10.28.0). Also develops from a Pixel 10 Pro XL.
- Laptop repo clone: `C:\Users\User\Workspace\Repositories\the-living-mythos`. Claude Code CLI runs there.
- Claude app for planning, debugging by paste, learning. pnpm only (npm blocked). PowerShell chains with `;`; package.json scripts chain with `&&`.
- This chat lives in the claude.ai Project "Living mythos". Planning chats can reach the laptop through the desktop-app link when it's on.

## 3. Style & communication
- English; senior peer; lead with assessment, not agreement; no filler, no emoji, no time estimates.
- Mobile-length replies; tables for options and comparisons.
- Grill-style: one question at a time, options as a table, lean stated; recommend, don't survey.
- Separate known from inferred in the sentence; flag `[NEED: ]`, `[BLOCKED: ]`, `[UNCERTAIN: ]`.
- When a decision is made, propose the exact decision-log edit. Jordan has approved writing revisions to the Project log directly as decisions land ("update with revisions"). Offer a handoff refresh before a chat gets long.
- After any decision-log revision, re-sync the repo mirror (`docs/`) in one docs commit.

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
| 2 | Said backward scrubbing "comes free" | Needs keyframes + command log + replay (self-corrected) |
| 3 | Proposed variable tick length | Fixed seasonal ticks (self-corrected) |
| 4 | Implied PixiJS in an OffscreenCanvas Worker | Main thread for PixiJS (research correction) |
| 5 | Framed v1 around two timelines / forks | Jordan: "I don't need to see the two timelines"; live nudge is the core loop. Forks later settled as a v1 stretch goal (option C) |
| 6 | Treated Earth's timeline as the model | Jordan: "We don't have to be a copycat/clone of Earth's timeline" |
| 7 | Round-one winter used noisy dither speckle; Earth palette muted | Snowline winter; Endesga 32 |
| 8 | Colour-blind tooling as a v1 concern | Jordan: not needed now |
| 9 | Asked which success test was current, offering forks as A/B/C | Jordan: "Option C was already decided." The log had not recorded it; check past decisions before re-asking |

## 6. Decisions and changes this handoff (details in decision log rev 13-16)
- Rev 13: `RngKey` gains `entityHi`; built (`b7d17b8`); RNG golden values recaptured once.
- Rev 14: primary PBT skill = fast-check `javascript-testing-expert` (Jordan ran Prompt A). Spec at v0.2.
- Rev 15 (spec Q0): doubles in sim state, basic arithmetic only; state hash rejects NaN/Infinity and normalizes -0; fixed summation order.
- Rev 16 (spec Q1): world size is a setting, slice default 128×128; catchment Euclidean disc r = 3 (29 cells).
- Gemini (Antigravity) agent episode: it answered all 12 spec questions with Claude's leans, marked the spec "finalized", and edited the repo mirror directly. Jordan's call: treat it as a very rough early draft and grill properly. Its edits are stashed on the laptop (`stash@{0}`, "gemini-staged-edits-2026-10-30"); copies archived at `archive/design/spec-rough-draft-gemini-2026-10-30.md` (+ its proposed log diff in the repo). Rule going forward: no agent edits `docs/` or the decision log except to mirror the Project.
- Still unconfirmed from rev 12: ordinal and command-cause rules ("Jordan did not veto").

## 7. Changed / rejected
See decision log "Rejected". Plus: Bayer-dithered 75% snow (the speckle); Tol-to-Endesga colour-blind guarantee (lost in mapping; moot); Earth palette as default; "living atlas" look from the brainstorm (superseded by pixel art); presentation work ahead of the slice (rewatch and polish are parked until the slice runs).

## 8. Data & facts (exact)
| Item | Value |
|---|---|
| Look test artifact | https://claude.ai/artifact/8TGrzjEVAJF1L2R669HcN5 (Version 5) |
| Look test scale | 192 cells, 384 terrain pixels; cell = 2 px = ~3 km; World 576 km across, Region 288 km, Close-up 144 km |
| Endesga 32 | hex codes verified against Lospec |
| PixiJS | v8.22.0; `ParticleContainer.addParticle(new Particle())`, `boundsArea`, `dynamicProperties`; `TextureStyle.defaultOptions.scaleMode = 'nearest'` + `roundPixels` (verified) |
| Unverified | Report claim: v8.19 particle blend modes, v8.20 ParticleContainer tint/alpha inheritance (check changelog on install) |
| Toolchain | TS ~6.0.3 (locked 6.0.3), vitest 5.0.5, eslint 10.13.0, typescript-eslint 8.72.0; pnpm 10.28.0 |
| RNG golden values | 1759517345 and 3421405739 (`rng.test.ts`), recaptured once for the 64-bit key (rev 13, commit `b7d17b8`; old values 3476084382 and 892054880). Config hash and lineage golden values unchanged. Never update casually |
| Tests | 67 pass, 1 todo, on Windows (2026-10-30: tick loop + property tests) |
| Entity IDs | 64-bit, 16 lowercase hex chars; `entityRngFields()` returns `{ entity: low 32, entityHi: high 32 }` |
| Entity-key collision risk | Fixed rev 13 (was ~4.5% at 20,000 entities with a 32-bit key) |
| Catchment | Euclidean disc r = 3, 29 cells, ≤ 9 km (rev 16); events max 3 enabling causes |
| Camp snapshot fields (slice) | food balance and trend, stash level, hunger state, 4 bracket counts, season, last foraging trip outcome |
| Benchmark order (laptop) | field cost/season; group cost at 1,000/5,000/20,000; run-ahead ratio; snapshot cost; cross-browser hash; then WASM/multi-worker |

## 9. People, terms & names
- Jordan. Gemini = external deep-research tool Jordan runs.
- "nudge", "Legends", "rule of cool", "crucibles", "ant-farm feel", "lever table" (purpose/density/traces), "lab coat" (raw-number toggle), "glance word", "camp snapshot", "the slice" (success-test vertical slice), "bloom" (fertility nudge), "the mirror" (repo `docs/`).
- Repo `shadepants/the-living-mythos` (private), branch `Main-REPO`. Packages `sim-core` (exists), `sim-worker`, `viewer` (not yet).

## 10. Work state
| Item | Status | Location |
|---|---|---|
| Decision log | rev 16 | Project `design/decision-log.md`; mirrored to repo `docs/design/` |
| Spec | v0.2 draft (file name `spec_v0.1.md`); Q0, Q1 settled; Q2-Q14 open, ordered in §20 | Project `design/spec_v0.1.md` |
| sim-core | rng (64-bit key), lint bans, config + hash, lineage IDs, event log, tick loop; property tests; 67 pass + 1 todo. No command log, entity registry, fields or systems yet | repo `packages/sim-core`; `CONTEXT.md` |
| Tooling | fast-check skill (pinned `fd17f486fc`), `determinism-rules` project skill, read-only `determinism-reviewer` subagent | repo `.claude/` |
| Config fields | Placeholders (`seasonsPerYear`, `startingBandSize`); real tunables come from the settled spec | `config.ts` |
| GitHub / laptop / cloud | Synced at end of handoff #6 | `Main-REPO` |
| Research | All Gemini prompts (1-6) run and reviewed | `research/`, `archive/research/` + PDFs |
| Look test | v5 published; rewatch parked. Artifact code is a visual reference only | artifact in section 8 |
| Project instructions | Settings text still has the old success-test wording | `claude/project-instructions.md` |

## 11. Next steps
1. **Grill spec question 2: event emission model and world-event primary** (§5, §14). Then Q3-Q14 in the §20 order, one at a time: options table, strongest counterargument, ≥2 failure modes, lean, external check, exact decision-log row. After each pick: update the spec and log (next rev), re-sync the mirror (one `docs:` commit), pull on the laptop.
2. Use the archived Gemini draft only as input; its numbers are unsourced guesses, its test scenario assumes worldgen geometry that doesn't exist yet, and it mentions a river delta (rivers are deferred).
3. When all questions settle: spec-developer Phase 3 (finalize), then the laptop builds command log (rule 6), entity registry, then systems in spec §5 order.
4. Decide the rev 10 cloud gate (lift / keep / lift with a Windows check before each sim merge). Lean: the last.
5. Benchmarks once fields run. Parked: v5 Close-up rewatch; property norm.

## 12. Open questions
- Spec Q2-Q14 (next step 1).
- Ordinal and command-cause confirmation (rev 12).
- Rev 10 gate.
- Stray Project doc `next-steps-prompts.md` at the Project root (duplicate of `claude/next-steps-prompts.md`, origin unknown): delete? Ask Jordan; don't delete unasked.
- Gemini stash on the laptop: drop once Jordan agrees the archive copies are enough.
- [NEED: Jordan] paste `claude/project-instructions.md` into Project settings.

## 13. Re-attach checklist
Nothing to attach inside the Project. The look-test source file lived only in an earlier cloud session; the published artifact is the durable copy.
