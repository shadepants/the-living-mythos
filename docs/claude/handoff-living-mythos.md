# active-memory handoff: Living mythos (civilization simulation)

**Handoff #5** · 2026-10-30 · Lineage: #1 (2026-10-23): engine/stack research, scoping, grilling Q1-Q4, timescale research, Gemini novelty review · #2 (2026-10-23): Project set up, repo skeleton pushed · #3 (2026-10-24): reframe to "terrarium you poke", research batch reviewed, depth/visuals brainstorm, pixel-art look tests v1-v5, decision log rev 8 · #4 (2026-10-24 to 10-28): slice focus; forks = stretch; cloud sessions = tests/tooling; all brainstorm questions closed; decision log rev 11; Project docs consolidated · #5 (2026-10-30): laptop back and linked; Windows `pnpm check` passed; laptop session built config, lineage IDs and event log; Project docs mirrored into repo `docs/`; repo `CLAUDE.md`/`README.md` brought up to date; TS range fixed; decision log rev 12

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

## 6. Decisions and changes this handoff (details in decision log rev 12)
- Repo mirrors the Project docs in `docs/` (Jordan asked to upload all Project docs, 2026-10-30). Project stays the source of truth. Settles handoff #4 question 2.6.
- Event content key `type:tick:primary:ordinal`; a cause is an event or a nudge command. Both proposed by the laptop Claude Code session; recorded as "Jordan did not veto". [NEED: Jordan] confirm.
- Config values and event payloads are integer-only (built into code by the laptop session; recorded in rev 12).
- Implementation status recorded for hard rules 3, 5, 7.
- Repo housekeeping (2026-10-30): `typescript` range `^6.0.3` → `~6.0.3` (caret allowed 6.1+, which typescript-eslint 8.72 rejects); `CLAUDE.md` now carries slice scope, the rev 10 gate, rev 11 view rules, rule implementation status, integer-only rule, and the entity-key issue; `README.md` status updated.

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
| Tests | 57 pass, 1 todo, on Windows (2026-10-30, with the tick loop) |
| Entity IDs | 64-bit, 16 lowercase hex chars; `entityRngFields()` returns `{ entity: low 32, entityHi: high 32 }` |
| Entity-key collision risk | Fixed rev 13 (was ~4.5% at 20,000 entities with a 32-bit key) |
| Catchment | 3-5 cells; events max 3 enabling causes |
| Camp snapshot fields (slice) | food balance and trend, stash level, hunger state, 4 bracket counts, season, last foraging trip outcome |
| Benchmark order (laptop) | field cost/season; group cost at 1,000/5,000/20,000; run-ahead ratio; snapshot cost; cross-browser hash; then WASM/multi-worker |

## 9. People, terms & names
- Jordan. Gemini = external deep-research tool Jordan runs.
- "nudge", "Legends", "rule of cool", "crucibles", "ant-farm feel", "lever table" (purpose/density/traces), "lab coat" (raw-number toggle), "glance word", "camp snapshot", "the slice" (success-test vertical slice), "bloom" (fertility nudge), "the mirror" (repo `docs/`).
- Repo `shadepants/the-living-mythos` (private), branch `Main-REPO`. Packages `sim-core` (exists), `sim-worker`, `viewer` (not yet).

## 10. Work state
| Item | Status | Location |
|---|---|---|
| Decision log | rev 13 | Project `design/decision-log.md`; mirrored to repo `docs/design/` |
| sim-core | rng, lint bans, config + hash, lineage IDs, event log; 43 tests pass on Windows and Linux. No tick loop, command log, entity registry or fields yet | repo `packages/sim-core`; state in `CONTEXT.md` |
| Repo docs | `CLAUDE.md`, `README.md` updated; Project mirrored in `docs/` | GitHub, `Main-REPO` |
| GitHub / laptop / cloud | In sync as of handoff #5 | — |
| Config fields | Placeholders (`seasonsPerYear`, `startingBandSize`); real tunables come from the slice spec | `config.ts` |
| Spec | Not started; scope = slice | will be `design/spec_v0.1.md` |
| Research | All Gemini prompts (1-6) run and reviewed | `research/`, `archive/research/` + PDFs |
| Look test | v5 published; rewatch parked. Artifact code is a visual reference only; rewrite, don't port | artifact above |
| Project instructions | Settings text still has the old success-test wording | `claude/project-instructions.md` |

## 11. Next steps
1. Entity-key fix: done (`b7d17b8`, pushed). Tick loop (hard rule 4) built in `09dee57` on the laptop, not yet pushed.
2. Decide the rev 10 cloud gate (lift / keep / lift with a Windows check before each sim merge). Lean: the last.
3. Confirm or reverse the ordinal and command-cause rules (rev 12).
4. Grill the last tooling question: which property-based-testing skill is primary (fast-check `javascript-testing-expert` vs Trail of Bits).
5. Slice spec: v0.1 draft written 2026-10-30 (Project `design/spec_v0.1.md`); grill its open questions in order, starting with number representation. Judge every item against the success test. It names the real config tunables (as scaled integers), the event types the slice needs, and the slice-relevant pixel-art items. Move the spec into the repo mirror once drafted.
6. Laptop: tick loop with fixed substeps (rule 4), then command log (rule 6) and entity registry (stores lineage parent, asserts ID uniqueness). Unblocks the `it.todo` fork test.
7. Cloud/laptop tooling: hooks and the read-only determinism-reviewer subagent; PixiJS skills when the viewer starts.
8. Benchmarks once the tick loop and fields exist.
9. Parked: v5 Close-up rewatch; property norm (deferred to batch runs).

## 12. Open questions
- Rev 10 gate (next step 2).
- Ordinal and command-cause confirmation (next step 3).
- PBT skill choice (next step 4).
- [NEED: Jordan] paste `claude/project-instructions.md` into Project settings (success test now says "fork the world (stretch)").

## 13. Re-attach checklist
Nothing to attach inside the Project. The look-test source file lived only in an earlier cloud session; the published artifact is the durable copy.
