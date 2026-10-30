# active-memory handoff: Living mythos (civilization simulation)

**Handoff #4** · 2026-10-28 · Lineage: #1 (2026-10-23): engine/stack research, scoping, grilling Q1-Q4, timescale research, Gemini novelty review · #2 (2026-10-23): Project set up, repo skeleton pushed · #3 (2026-10-24): reframe to "terrarium you poke", research batch reviewed, depth/visuals brainstorm, pixel-art look tests v1-v5, decision log rev 8 · #4 (2026-10-24 to 10-28): priorities reset toward the success-test slice; forks = stretch; spec scope = slice; cloud sessions = tests/tooling only; all brainstorm questions closed; decision log rev 11; Project docs verified, consolidated and archived

## 0. Instructions for Claude (read first)

You are continuing work from a previous chat. That chat is gone; this file plus `design/decision-log.md` is the complete context. Where they disagree, the decision log wins for decisions; this file wins for work state and next steps.

1. Read this whole file before replying.
2. Follow sections 3 (Style), 4 (Hard rules) and 5 (Corrections) in every reply. They override your defaults.
3. Use the values in section 8 exactly. Never round, re-estimate, or "correct" them.
4. Do not suggest anything in section 7 (Changed / rejected) again unless the user brings it up.
5. Code word: none active.
6. First reply: at most 5 lines covering goal, current state, next step (section 11). Ask the questions in section 12. End with "Ready to continue with <next step>?" and wait.

## 1. Mission
- **Goal:** Plan, then build, "Living mythos": an observational god-view sandbox, "a terrarium you poke", "like a kid with an ant colony". Bands develop, change the land and each other, make history in unexpected ways; you watch, read the Legends, and nudge. Inspired by Dwarf Fortress worldgen + Legends. Not a game to win; not a copy of Earth's timeline.
- **v1 scope:** simple hunter-gatherer bands to the first farming villages, one procedural landmass, time from year 0. Long-term: a Roman-Empire-like civilization.
- **Success test:** "I trigger a drought and can read in the Legends why one band migrated and another died out." Stretch: fork the world before the drought. v1 passes without the fork.
- **Core loop:** live nudge and watch. Forks are a v1 stretch goal (Jordan chose option C, 2026-10-24).
- **Current focus:** the success-test slice. Build food, movement and death into a caused story before anything else.

## 2. About the user
- Jordan; hobbyist developer, Calgary; phone-only until his laptop returns (Windows 11, i7-8665U, 16GB, integrated GPU). Also develops from a Pixel 10 Pro XL.
- Claude Code CLI for editing; Claude app for planning, debugging by paste, learning. pnpm only (npm blocked). PowerShell chains with `;`; package.json scripts chain with `&&`.
- This chat lives in the claude.ai Project "Living mythos".
- Claude Code mobile Code tab can see the repo (confirmed by Jordan 2026-10-28).
- 2026-10-28: a desktop-app computer link appeared in the chat session. Unverified whether it is the laptop or whether the laptop is back; ask before assuming.

## 3. Style & communication
- English; senior peer; lead with assessment, not agreement; no filler, no emoji, no time estimates.
- Mobile-length replies; tables for options and comparisons.
- Grill-style: one question at a time, options as a table, lean stated; recommend, don't survey.
- Separate known from inferred in the sentence; flag `[NEED: ]`, `[BLOCKED: ]`, `[UNCERTAIN: ]`.
- When a decision is made, propose the exact decision-log edit. Jordan has approved writing revisions to the Project log directly as decisions land ("update with revisions"). Offer a handoff refresh before a chat gets long.
- Jordan's working order: finish the open questions before updating the repo.

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

## 6. Decisions this handoff (details in decision log rev 11)
- Forks: v1 stretch goal, not a pass condition (rev 9).
- First spec: success-test slice only. Worldgen (heightmap + biomes), climate regime, vegetation + large fauna, bands with food balance and 4 brackets, migration and die-out, drought nudge, caused events, templated Legends (rev 9).
- Cloud sessions: tests and tooling only (hard-rule tests 3/5/6/7, hooks, determinism-reviewer subagent, determinism skill). No sim logic in the cloud until Windows `pnpm check` passes (rev 10).
- Information default: investigate-to-learn with lab coat toggle off by default; glance words from named config thresholds (rev 10).
- God tools: v1 = rain/drought + bloom; slice = drought; a tool ships with its mechanism, never before (rev 11).
- Diorama folded into Close-up; all views read a read-only camp snapshot, never sim internals (rev 11).
- Docs housekeeping (2026-10-28, approved by Jordan): Project docs verified, consolidated and archived; `archive/` folder convention added (see README).

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
| Toolchain | TS ~6.0.3, vitest 5.0.5, eslint 10.13.0, typescript-eslint 8.72.0; pnpm 10.28.0 |
| RNG golden values | 3476084382 and 892054880 (`rng.test.ts`); never update casually |
| Catchment | 3-5 cells; events max 3 enabling causes |
| Camp snapshot fields (slice) | food balance and trend, stash level, hunger state, 4 bracket counts, season, last foraging trip outcome |
| Benchmark order (laptop) | field cost/season; group cost at 1,000/5,000/20,000; run-ahead ratio; snapshot cost; cross-browser hash; then WASM/multi-worker |

## 9. People, terms & names
- Jordan. Gemini = external deep-research tool Jordan runs.
- "nudge", "Legends", "rule of cool", "crucibles", "ant-farm feel", "lever table" (purpose/density/traces), "lab coat" (raw-number toggle), "glance word", "camp snapshot", "the slice" (success-test vertical slice), "bloom" (fertility nudge).
- Repo `shadepants/the-living-mythos`, branch `Main-REPO`, commit 3aac7a2. Packages `sim-core` (exists), `sim-worker`, `viewer` (not yet).

## 10. Work state
| Item | Status | Location |
|---|---|---|
| Decision log | rev 11 (paths updated after archive pass) | Project `design/decision-log.md` |
| Brainstorm | All questions closed; archived | `archive/design/depth-and-visuals-brainstorm.md` |
| Research | All Gemini prompts (1-6) run and reviewed; prompts consolidated into one file; batch review archived; tooling report partly decided (cloud sessions) | `research/`, `archive/research/` + PDFs |
| Look test | v5 published; rewatch parked (not blocking the spec). Artifact code is a visual reference only; rewrite, don't port | artifact above |
| Project instructions | Settings text has the old success-test wording; Project copy updated with "(stretch)" | `claude/project-instructions.md` |
| Project docs pass | Done 2026-10-28 (see below) | README "Archive" section |
| Repo | sim-core RNG + lint bans; 7 tests pass; not yet run on Windows. Untouched this handoff. Docs pass pending | GitHub |
| Spec | Not started; scope = slice | will be `design/spec_v0.1.md` |

**Project docs pass, 2026-10-28 (what was done):**
- Verified statuses against decision log rev 11 and fixed stale ones: `research/gemini-prompts.md` said prompt 6 "ready" (it was run); the novelty prompt said "not yet run" (it was run); the batch review and pixel-art review said "pending approval" (both largely adopted; remaining pixel items listed in the review's status line and the log's open questions).
- Consolidated: novelty prompt merged into `research/gemini-prompts.md` as prompt 1; original deleted.
- Archived (moved, with dated status notes): batch review → `archive/research/`; brainstorm → `archive/design/`.
- References updated in the decision log and README. Project instructions copy reconciled with the Settings text.
- Not re-verified: the bodies of `research/stack-and-prior-projects-report.md`, `research/timescale-report.md`, `research/tooling-report.md`, `research/novelty-report-gemini.txt` (statuses in README are carried over, not re-checked line by line). PDFs can't be moved by the Project tool.

## 11. Next steps
1. Grill the last tooling question: which property-based-testing skill is primary (fast-check `javascript-testing-expert` vs Trail of Bits). This closes the open questions.
2. **Repo docs pass** (same treatment as the Project; docs only, no sim logic; allowed in a cloud session under rev 10). Do it in a Claude Code session on `shadepants/the-living-mythos`, branch `Main-REPO`:
   1. List every doc in the repo (`README.md`, `CLAUDE.md`, anything under `docs/` or package READMEs).
   2. Verify each against Project `design/decision-log.md` rev 11: the 7 hard rules (wording and which are implemented), stack and toolchain versions (section 8), branch name, success test with fork as stretch, slice scope.
   3. Update `CLAUDE.md` with the rules that bind code: rev 10 (no sim logic in cloud sessions until Windows `pnpm check` passes), rev 11 (views read the camp snapshot only; tools ship with their mechanism), slice scope.
   4. Move stale or superseded docs to `docs/archive/` with a dated status note at the top; don't delete.
   5. Consolidate duplicates; keep one source per topic.
   6. Open question for Jordan before writing: should the repo mirror the decision log? Claude Code can't read the Project, so code-writing agents need the binding rules in-repo. Lean: `CLAUDE.md` carries the code-binding rules; the slice spec moves into the repo once drafted; the full decision log stays in the Project.
   7. One conventional commit (e.g. `docs: verify, consolidate and archive repo docs`), then report back and update this handoff.
3. Draft the slice spec (spec-developer, then grill), `design/spec_v0.1.md`. Judge every item against the success test. Settle slice-relevant pixel-art review items during the spec.
4. Cloud session: write tests for hard rules 3, 5, 6, 7, plus hooks and the read-only determinism-reviewer subagent. No sim logic.
5. When the laptop returns: `pnpm install; pnpm check` on Windows (gate for sim logic), PixiJS skills, benchmark order.
6. Parked: v5 Close-up rewatch; property norm (deferred to batch runs).

## 12. Open questions
- PBT skill choice (next step 1).
- Repo mirrors the decision log or not (next step 2.6).
- [NEED: Jordan] paste updated `claude/project-instructions.md` into Project settings (success test now says "fork the world (stretch)").
- [BLOCKED] hardware benchmark and Windows `pnpm check` need the laptop.

## 13. Re-attach checklist
Nothing to attach inside the Project. The look-test source file lived only in an earlier cloud session; the published artifact is the durable copy.
