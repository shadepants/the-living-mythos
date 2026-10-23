# Living mythos

Observational god-view civilization sandbox. v1: Paleolithic bands to first farming villages. Design source of truth is the claude.ai Project "Living mythos" (`design/decision-log.md`); this file carries only what code work needs.

## Layout
- `packages/sim-core`: pure TypeScript simulation. No DOM, no I/O, no wall clock.
- `sim-worker` and `viewer` (PixiJS v8, main thread) are added when first needed, not before.

## Commands (PowerShell)
- `pnpm install`
- `pnpm check` runs typecheck, lint and tests.
- `pnpm -C packages/sim-core exec vitest` for watch mode.

pnpm only; never npm. Default branch is `Main-REPO`. package.json scripts chain with `&&` (pnpm runs scripts through cmd.exe on Windows, where `;` is not a separator); commands typed in PowerShell chain with `;`. TypeScript is pinned to 6.0.x because typescript-eslint 8.x does not support TS 7 yet.

## Determinism hard rules (tests before sim code)
1. Randomness only via `rand01`/`hashKey` keyed on (seed, absolute season, entity, purpose). Never a shared sequential stream. Add new `Purpose` codes at the end; never renumber.
2. No platform-dependent math in `sim-core/src`: ESLint bans Math.random, trig/exp/log/pow/cbrt/hypot, the `**` operator, `Date`, `Date.now`, `performance.now`. Math.sqrt and basic arithmetic are fine.
3. Stable lineage-derived IDs (parent, birth tick, sibling index).
4. Fixed internal substeps for environment fields; schedules never depend on state.
5. Causal event log from day one; every event records parent-cause IDs (max 3 enabling causes).
6. Snapshots = keyframes + command log + replay.
7. All tunables in a versioned config; saves and forks record the config hash.

The golden-value test in `test/rng.test.ts` must never be updated casually: a change means existing saves and forks no longer replay.

## Conventions
Strict TS, const-first, explicit return types on exports, early returns. Conventional commits, one logical change each.
