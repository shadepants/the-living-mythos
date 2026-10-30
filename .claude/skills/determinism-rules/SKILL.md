---
name: determinism-rules
description: Use before writing or reviewing any change under packages/sim-core, and whenever a change touches rng keys, Purpose codes, golden-value tests, lineage ids, the event log, config fields or the tick schedule. Covers the procedure lint and tests cannot enforce.
---

# Determinism rules: working procedure

The rules themselves live in the repo `CLAUDE.md` (hard rules 1-7, rev 12-13) and `docs/design/decision-log.md`; they win over this file. Lint and tests already enforce much of it:

| Enforced by | What |
|---|---|
| ESLint (`eslint.config.js`) | No Math.random, trig, exp/log/pow/cbrt/hypot, `**`, Date, performance.now in `sim-core/src` |
| Golden tests (`rng.test.ts`, `config.test.ts`, lineage tests) | Hash outputs, config hash, ids, and the pinned `Purpose` list |
| Property tests (fast-check) | Purity, key sensitivity, log invariants, schedule order |

This skill covers what they cannot.

## Before writing sim code
1. Write or extend the test first (hard rule: tests before sim code). For an invariant ("always", "never"), use a property test with `@fast-check/vitest`; see the `javascript-testing-expert` skill.
2. Every random draw: `rand01({ seed, season, ...entityRngFields(id), purpose })`. Cells: own Purpose code, cell index in `entity`, `entityHi: 0`. Need a new Purpose? Append it at the end of `Purpose` and extend the pinned list in `rng.test.ts`.
3. New tunable: add it to `SimConfig` as a safe integer (scaled if fractional), bump `version` if a meaning changes. Adding a field changes the config hash on purpose: say so in the commit message.
4. New system: give it a fixed period, offset and substep count in the schedule. Never compute them from state.

## Golden values
Never update a golden value to make a test pass. If a change must alter one:
1. Stop and tell Jordan which value changes and why.
2. Only with Jordan's yes: update it, keep the previous value in a comment, and say "changes golden value" with the reason in the commit message.
3. Propose the decision-log edit (the Project is the source of truth; never edit `docs/` to record a decision).

## Before committing
1. `pnpm check` (typecheck, lint, tests).
2. Run the `determinism-reviewer` subagent on the diff; fix or explain every finding.
3. Conventional commit, one logical change.
