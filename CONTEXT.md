# The Living Mythos: project state

## Goal
Observational god-view civilization sandbox: watch Paleolithic bands grow into first farming villages, read their history, and nudge the world to see what ripples.

## Tech Stack
TypeScript (strict, pinned 6.0.x), pnpm workspace, Vitest, ESLint (determinism bans). Viewer will be PixiJS v8 later.

## Current State
- [x] Workspace scaffold, `packages/sim-core`
- [x] Hash-based RNG (`rng.ts`) with golden-value test
- [x] Versioned config + `hashConfig` (`config.ts`), golden-value test; fields are placeholders
- [x] Lineage-derived entity IDs (rule 3): 64-bit hex `EntityId` (`lineage.ts`), `entityKey` bridges to the rng. The id does not encode the parent; the event log must store it and assert id uniqueness on registration.
- [ ] Causal event log types (rule 5)
- [ ] Tick loop with fixed substeps (rule 4); unblocks the `it.todo` fork test in `rng.test.ts`
- Blocker: the design log (`design/decision-log.md`) lives in the claude.ai Project, not this repo. Config fields are unconfirmed against it.

## Don't Forget
Determinism hard rules are in `CLAUDE.md`. Golden values (rng, config hash) are never updated casually: a change breaks replay of saves and forks.
