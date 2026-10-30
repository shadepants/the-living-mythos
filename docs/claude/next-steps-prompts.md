# Next steps: skill setup and spec prompts

2026-10-30. From the skill review in the planning chat. Each step gives Claude's suggested option; Jordan confirms or overrides when running it. The decision log wins over this doc.

Where each prompt runs:
| Prompt | Runs in | Why there |
|---|---|---|
| A. Tooling setup | Laptop Claude Code session (repo clone) | Installs and repo commits happen on the laptop; tests and tooling only, no sim logic |
| B. Spec grilling | New claude.ai planning chat in the Project | The spec and decision log live in the Project |
| C. Later triggers | Whichever surface the trigger names | Not needed until the work reaches them |

---

## Prompt A: laptop Claude Code session

Paste everything in the code block.

```
Task: set up the testing and determinism tooling recommended in docs/claude/next-steps-prompts.md. Tests and tooling only; no sim logic. Read CLAUDE.md first.

Step 0. git pull --ff-only origin Main-REPO. Stop if the tree isn't clean.

Step 1. Property-based testing skill.
  Suggested option: fast-check `javascript-testing-expert` (maintained by fast-check's author), NOT Trail of Bits property-based-testing. Install only one; two PBT skills give conflicting advice.
  a. Vet before installing (tooling-report checklist): read every file in dubzzz/fast-check skills/javascript-testing-expert/ (SKILL.md, references, any scripts). Stop and report if it ships hooks, downloads, or network calls.
  b. Install: pnpx skills add dubzzz/fast-check --skill javascript-testing-expert
     If that fails on Windows, copy the folder into .claude/skills/javascript-testing-expert/ instead.
  c. Add dev dependencies to packages/sim-core with pnpm: fast-check and @fast-check/vitest, latest stable. Check the versions against the npm registry and note their maintenance status; don't trust remembered version numbers.
  d. Write property tests for code that already exists (no new sim logic):
     - rng: hashKey is pure (same key, same value); any single-field change changes the hash in all but a negligible fraction of cases; rand01 stays in [0, 1).
     - lineage: deriveEntityId is pure; distinct (parent, season, sibling) inputs never collide in a generated batch.
     - event-log: a rejected append leaves the log unchanged; ticks never go backwards; no event has more than 3 causes.
     - tick: systemsDue depends only on (schedule, season); the same schedule and season always give the same system list.
  e. Run pnpm check. Commit: test(sim-core): add property tests for rng, lineage, event log and schedule

Step 2. Project determinism skill.
  Suggested option: write our own skill with skill-creator, stored in the repo at .claude/skills/determinism-rules/SKILL.md, rather than any third-party determinism skill (none fits counter-based RNG or our event log).
  Contents: hard rules 1-7 as they stand in CLAUDE.md; rev 12 integer-only config and payloads; rev 13 RngKey with entityHi and entityRngFields; the golden-value rule; "tests before sim code". Description should trigger on any edit under packages/sim-core.
  Include 3 eval cases: a diff using Math.random, a diff adding a Purpose code in the middle, a diff that updates a golden value without a commit-message justification. Each must be flagged.
  Commit: chore: add determinism-rules project skill

Step 3. Read-only determinism reviewer subagent.
  Suggested option: .claude/agents/determinism-reviewer.md with tools: Read, Grep, Glob (no edit tools). Checklist from research/tooling-report.md "Subagent" section plus rev 12-13 (integer payloads, entityHi). Description: "Use after any change to packages/sim-core."
  Commit: chore: add read-only determinism-reviewer subagent

Step 4. Do NOT install yet: the PixiJS skill pack (wait for viewer work), the Trail of Bits PBT skill, adversarial-review or adversarial-plan (need Codex; on the tooling report's skip list).

Step 5. Run pnpm check on Windows, push, and report: the installed skill's version or commit, the fast-check versions, the new test count, and anything the vetting in step 1a found.
```

**Decision-log edit when Step 1 runs:** close the open question "which PBT skill is primary" with "fast-check `javascript-testing-expert`; Trail of Bits not installed (overlap)". Claude in the planning chat makes this edit once Jordan confirms.

---

## Prompt B: new planning chat (grill the spec)

Before starting: in this chat, run `/amhandoff` (or say "refresh the handoff") so the new chat starts from the current state. Then open a new chat in the Project and paste:

```
Continue from claude/handoff-living-mythos.md. Task: grill the open questions in design/spec_v0.1.md section 20, one at a time, in order. For each: options table, strongest counterargument first, at least two failure modes, your lean, then wait for my pick. After each pick, edit the spec and propose the exact decision-log edit. Use the grill skill. When all are settled, run spec-developer Phase 3 (finalize) on the spec.
```

Claude's suggested option for each question (from the spec draft; for orientation, not pre-decided):
| # | Question | Suggested option |
|---|---|---|
| 0 | Number representation | Doubles in state, basic arithmetic only; state hash fails on NaN and normalizes -0 |
| 1 | Map size, catchment metric | 128×128 for the slice (256×256 stays the v1 size); Chebyshev catchment, radius 3 |
| 2 | Drought command | One signed rain/drought command: magnitude in anomaly units, duration in seasons, centre cell + radius (0 = whole map) |
| 3 | Demography draws, bracket cuts | One binomial draw per bracket (inverse CDF); fixes the log's "per-member" wording. Cuts 0-14 / 15-24 / 25-49 / 50+ |
| 4 | Event emission, world-event primary | One regime-detector pass at the end of each season; `ROOT_ID` as primary for world events |
| 5 | Climate regime | Seasonal lookup table + 1D temporal value noise + coarse regional noise, scaled by the volatility and severity dials |
| 6 | Vegetation and fauna targets | A 4-8 season drought visibly drops vegetation, and recovery takes longer than the drought |
| 7 | Migration | Trigger after N hungry seasons; best target within a search radius by expected yield minus travel cost; tie-break lowest cell index; no random draw |
| 8 | Die-out | Population 0 (no floor) for the slice |
| 9 | Glance words | thriving / settled / hungry / starving / restless, each on a named config threshold |
| 10 | Test scenario | Fixed seed, 2 bands, one with a better refuge inside its search radius and one without; drought at a fixed season; pass when each chain reaches `drought_began` within 3 hops |
| 11 | Worldgen biome table | 4 height bands × 3 moisture bands, about 8 biomes |

Also in that chat, once the spec is settled:
- **instructions-audit:** "Audit the Project instructions, claude/project-instructions.md, handoff #5 and the repo CLAUDE.md for conflicts and duplication." Suggested option: keep code-binding rules only in CLAUDE.md and planning rules only in the Project instructions; the handoff points to both.
- [NEED: Jordan] Paste `claude/project-instructions.md` into Project Settings (still pending since 2026-10-28).

---

## C. Later triggers (don't set up now)

| When | Skill | Suggested option |
|---|---|---|
| Viewer work starts | PixiJS skill pack | In Claude Code: `/plugin marketplace add pixijs/pixijs-skills`; re-check the version against PixiJS v8.22.0 at install |
| First headless batch runs (tuning) | dataviz | Chart population and vegetation per seed from exported CSV; one chart per question, not a dashboard |
| Spec question 11 (biomes) | algorithmic-art | Phone-side previews of value noise and biome bands only; never port its code (not deterministic) |
| Close-up rewatch ("ant-farm feel") | iteration-tracker | Track each look-test version against the lever table (purpose, density, traces) |
| Benchmarks (after fields run) | Chrome DevTools MCP | Frame-time traces and heap snapshots, compared on the same laptop only |
