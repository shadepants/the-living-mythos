# The Living Mythos

An observational god-view civilization sandbox: watch hunter-gatherer bands grow toward the first farming villages, read their history, and nudge the world to see what ripples and what fades.

## Status
Pre-alpha. Only `packages/sim-core` exists: the deterministic foundations — hash-based RNG, determinism lint rules, versioned config hash, lineage-derived entity IDs and the entity registry, causal event log, fixed-substep tick loop, exact binomial sampler, and the command log. No worldgen, real systems, or viewer yet. Spec v1.0 was approved on 2026-11-03 (decision log rev 50); design docs are mirrored in `docs/`. Current code state is in `CONTEXT.md` (126 tests + 1 todo, Linux, after PR #4).

## Getting started
Requires Node 22+ and pnpm 10.

```powershell
pnpm install
pnpm check
```

`pnpm check` runs typecheck, lint and tests. See `CLAUDE.md` for the determinism rules every change must follow.
