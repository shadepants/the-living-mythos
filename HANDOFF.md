# Handoff (Claude Code, laptop)

Last updated: 2026-11-16, Blanco (doc cleanup at Jordan's request). Supersedes the 2026-10-30 laptop handoff: everything it listed as next steps 3-4 has since merged. Planning-chat state lives in `docs/claude/handoff-living-mythos.md` (Project mirror; don't edit it here). Current code state is in `CONTEXT.md` — this file is the session handoff, CONTEXT.md wins on code facts.

## What changed since 2026-10-30
- Spec v1.0 approved: decision log rev 50 (2026-11-03, `63565d2`), after the rev 44-49 audit and re-audit fixes. The slice spec is `docs/design/spec_v0.1.md`.
- PR #1 (merged 2026-11-02, `8c04472`): `Purpose` codes 6-12 appended in `rng.ts`.
- PR #2 (merged 2026-11-02, `8f65a1d`): exact binomial sampler (spec §10, `binomial.ts`).
- PR #3 (merged 2026-11-02, `720f0d0`): command log (hard rule 6, first half; `command-log.ts`) with spec §20 error validation.
- PR #4 (merged 2026-11-02, `6672fdc`): entity registry (hard rule 3 completed; `entity-registry.ts`).
- `CONTEXT.md` was updated after each PR merge; `Main-REPO` is at `3132297`.
- CI: the `check` workflow has been manual-only since 2026-11-02 (GitHub billing issue; automatic runs ended in `startup_failure`). All four PRs merged "Linux-verified only" under the interim rev 43 rule.
- This cleanup (2026-11-16): README status corrected (it still said "No tick loop yet"; the tick loop shipped 2026-10-30), this handoff refreshed, and the four merged PR branches deleted (`sim/purpose-codes`, `feat/binomial-sampler`, `feat/command-log`, `feat/entity-registry`). PR content was verified present in the `Main-REPO` tree before deletion.

## Verified
- `CONTEXT.md` records 126 tests + 1 todo (Linux, after PR #4). The 2026-10-30 session recorded 67 passed + 1 todo, the mutation checks, and a clean secret scan.
- Blanco verified 2026-11-16, from a fresh clone at `3132297`: `binomial.ts`, `command-log.ts`, and `entity-registry.ts` are in `packages/sim-core/src/` and exported from `index.ts`; `Purpose` codes 1-12 are in `rng.ts`.
- Blanco ran `pnpm check` on that clone (Linux, pnpm 10.28.0, 2026-11-16): typecheck and lint clean, 126 passed + 1 todo — green, matching CONTEXT.md.

## Not verified
- Windows `pnpm check` on `Main-REPO` (rev 43): still owed when the laptop returns; first task before any new sim work.
- Keyframes and replay (rest of hard rule 6) are not built; the `it.todo` fork test in `rng.test.ts` still waits on them.
- `determinism-reviewer` invoked by its own agent type; whether the `determinism-rules` skill auto-triggers on sim-core edits.
- Tick loop with real systems or at benchmark scale.

## Notes
- [CHECK] Visibility: this repo was created private and the 2026-10-30 handoff recorded it as private; the GitHub API reported it **public** on 2026-11-16. Jordan to confirm that is intentional.
- Pull with `--ff-only` before working; a planning chat has rebased this branch mid-session before (2026-10-30).

## Next steps (from CONTEXT.md, spec §20)
1. When the laptop returns: run `pnpm check` on `Main-REPO` on Windows before any new sim work (rev 43), fix any failure, then the normal Windows-gate rule resumes.
2. Check event `command` causes against the command log.
3. Give `SimConfig` its real fields (this changes the config hash once, before saves exist).
4. Worldgen, then systems in spec §5 order.
5. Run `determinism-reviewer` on each sim-core change.
