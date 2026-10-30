# Handoff (Claude Code, laptop)

Last updated: 2026-10-30, Claude Code (Opus 5.5), laptop session. Planning-chat state lives in `docs/claude/handoff-living-mythos.md` (Project mirror; don't edit it here).

## What changed
- `packages/sim-core/src/tick.ts`: tick loop with fixed substeps (hard rule 4). `createSchedule`, `systemsDue` (pure function of the season), `runTick`. No real systems yet; periods and substeps will move into `SimConfig` with the spec.
- Property tests (fast-check 4.10.2, @fast-check/vitest 0.5.0, pinned) added to the existing rng, lineage, event-log and tick test files.
- `rng.test.ts` pins the `Purpose` code list.
- `.claude/skills/javascript-testing-expert/` (verbatim, fast-check commit fd17f486fc), `.claude/skills/determinism-rules/` (+ 3 evals), `.claude/agents/determinism-reviewer.md` (Read/Grep/Glob only).
- Outside the repo: `~/.agents/scripts/agy_bridge.py` fixed (commit 2357ce7). It now reports empty agy output and tells agy not to use tools.
- All pushed: `Main-REPO` at `0823699`, in sync with origin.

## Verified (this session)
- `pnpm check`: 67 passed, 1 todo.
- Mutation check: dropping `entityHi` from `hashKey` and loosening the cause limit each fail 3 tests.
- determinism-reviewer instructions, run through a general-purpose agent: all 3 eval cases flagged BLOCKING.
- Secret scan of the pushed diff: clean. The repo is private.

## Not verified
- `determinism-reviewer` invoked by its own agent type. It only loads at session start.
- Whether the `determinism-rules` skill auto-triggers on sim-core edits.
- Tick loop with real systems or at benchmark scale.

## Notes
- A planning chat rebased this branch mid-session (07:14 and 07:19) to add the docs mirror commits. Pull with `--ff-only` before working.
- The slice spec draft is `docs/design/spec_v0.1.md`, with open questions in its section 20. The brief I wrote earlier in the scratchpad is superseded; don't use it.

## Next steps
1. Planning chat: close the decision-log PBT question ("fast-check `javascript-testing-expert`; Trail of Bits not installed"). Refresh the handoff: 67 tests + 1 todo, tick loop and tooling built.
2. Planning chat: run Prompt B (`docs/claude/next-steps-prompts.md`) to grill spec section 20.
3. Laptop, after the spec settles: build the command log (hard rule 6), test first. This unblocks the `it.todo` fork test in `rng.test.ts`.
4. Then the entity registry (stores the lineage parent, asserts id uniqueness).
5. Run `determinism-reviewer` on each sim-core change.
