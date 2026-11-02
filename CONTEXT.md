# The Living Mythos: project state

## Goal
Observational god-view civilization sandbox: watch Paleolithic bands grow into first farming villages, read their history, and nudge the world to see what ripples.

## Tech Stack
TypeScript (strict, pinned 6.0.x), pnpm workspace, Vitest, ESLint (determinism bans). Viewer will be PixiJS v8 later.

## Current State
- [x] Workspace scaffold, `packages/sim-core`
- [x] Hash-based RNG (`rng.ts`) with golden-value test. `Purpose` codes 1-12 (6-12 appended 2026-11-02, PR #1, Linux-verified only under rev 43; Death 4 retired, Migration 2 and Invention 5 reserved). Keyed on the full 64-bit entity id (`entity` + `entityHi`, rev 13); golden values were recaptured once on 2026-10-30, before any saves existed.
- [x] Versioned config + `hashConfig` (`config.ts`), golden-value test; fields are placeholders
- [x] Lineage-derived entity IDs (rule 3): 64-bit hex `EntityId` (`lineage.ts`), `entityRngFields` bridges to the rng. The id does not encode the parent; the event log must store it and assert id uniqueness on registration.
- [x] Causal event log (rule 5, `event-log.ts`): sequential run-local ids, content key `type:tick:primary:ordinal`, max 3 causes (event or command), flat-integer payload, append-only with ticks non-decreasing. No event taxonomy yet.
  - Open: command causes are only shape-checked until the command log exists (rule 6).
  - Open: lineage parent is not recorded by the log; the future entity registry must store it and assert id uniqueness.
- [x] Tick loop with fixed substeps (rule 4, `tick.ts`): one tick = one season; `createSchedule` freezes an ordered list of systems (name, period, offset, substeps); `systemsDue` is a pure function of the season; `runTick` runs due systems in order for their fixed substeps. No real systems yet.
  - Open: periods and substep counts are passed by the caller; they move into `SimConfig` with the slice spec (changing the config hash once, before saves exist).
- [x] Tooling: property tests (fast-check 4.10.2, @fast-check/vitest 0.5.0, pinned); `Purpose` list pinned by a test; project skills `javascript-testing-expert` (fast-check, commit fd17f486fc) and `determinism-rules`; read-only `determinism-reviewer` subagent. 67 tests + 1 todo.
- [ ] Windows `pnpm check` on `Main-REPO` when the laptop returns (rev 43): first task, before new sim work
- [ ] Binomial sampler (spec §10) with fast-check property tests
- [ ] Command log (rule 6) and entity registry (stores lineage parent, asserts id uniqueness); the command log unblocks the `it.todo` fork test in `rng.test.ts`

## Don't Forget
Determinism hard rules are in `CLAUDE.md`. Golden values (rng, config hash) are never updated casually: a change breaks replay of saves and forks.
