# Living mythos

Observational god-view civilization sandbox. v1: Paleolithic bands to first farming villages. Design source of truth is the claude.ai Project "Living mythos" (`design/decision-log.md`). A read-only mirror of the Project docs lives in `docs/` (start with `docs/design/decision-log.md`); if the mirror and the Project disagree, the Project wins. Never edit `docs/` to change a decision. This file carries only what code work needs.

## Layout
- `packages/sim-core`: pure TypeScript simulation. No DOM, no I/O, no wall clock.
- `sim-worker` and `viewer` (PixiJS v8, main thread) are added when first needed, not before.
- `docs/`: Project mirror (decision log, research, handoff). `CONTEXT.md`: current code state.

## Commands (PowerShell)
- `pnpm install`
- `pnpm check` runs typecheck, lint and tests.
- `pnpm -C packages/sim-core exec vitest` for watch mode.

pnpm only; never npm. Default branch is `Main-REPO`. package.json scripts chain with `&&` (pnpm runs scripts through cmd.exe on Windows, where `;` is not a separator); commands typed in PowerShell chain with `;`. TypeScript is pinned to 6.0.x (`~6.0.3`) because typescript-eslint 8.x supports only <6.1.

## Scope (decision log rev 9)
Build the success-test slice only: worldgen (heightmap + biomes), climate regime, 2 fields (vegetation, large fauna), bands with food balance and 4 age brackets, migration and die-out, the drought nudge, events with causes, templated Legends. Techniques, farming and other fields come in later spec versions. If a change isn't on the path "drought → band migrated or died out → readable why", don't build it yet.

## Where code may be written (rev 10)
Cloud sessions (Linux VM) may write tests and tooling only: hard-rule tests, hooks, the determinism-reviewer subagent, the determinism skill. Sim logic is written on the Windows laptop. Windows `pnpm check` passed on 2026-10-30; whether this gate lifts is an open question in the decision log, so treat it as still in force.

## Determinism hard rules (tests before sim code)
1. Randomness only via `rand01`/`hashKey` keyed on (seed, absolute season, full 64-bit entity as `entity` + `entityHi`, purpose). Spread `entityRngFields(id)` into the key; non-lineage keys set `entityHi: 0` and use their own `Purpose` codes (rev 13). Never a shared sequential stream. Add new `Purpose` codes at the end; never renumber. Built: `rng.ts`.
2. No platform-dependent math in `sim-core/src`: ESLint bans Math.random, trig/exp/log/pow/cbrt/hypot, the `**` operator, `Date`, `Date.now`, `performance.now`. Math.sqrt and basic arithmetic are fine. Built: `eslint.config.js`.
3. Stable lineage-derived IDs (parent, birth tick, sibling index). Built: `lineage.ts`. The ID does not encode the parent; the entity registry (not built) must store it and assert uniqueness.
4. Fixed internal substeps for environment fields; schedules never depend on state. Not built (tick loop).
5. Causal event log from day one; every event records at most 3 causes, each an earlier event or a nudge command. Content key `type:tick:primary:ordinal`. Built: `event-log.ts`.
6. Snapshots = keyframes + command log + replay. Not built.
7. All tunables in a versioned config; saves and forks record the config hash. Built: `config.ts` (placeholder fields until the slice spec).

Config values and event payloads are integers only (rev 12). Store fractional tunables as scaled integers.

The golden-value tests (rng, config hash, lineage IDs) must never be updated casually: a change means existing saves and forks no longer replay.

## Views (rev 11)
Views read a read-only camp snapshot built from sim state, never sim internals. One snapshot field per thing a view draws. A god tool ships only with its mechanism (the slice ships drought).

## Conventions
Strict TS, const-first, explicit return types on exports, early returns. Conventional commits, one logical change each.
