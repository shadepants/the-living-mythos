# The Living Mythos

An observational god-view civilization sandbox: watch hunter-gatherer bands grow toward the first farming villages, read their history, and nudge the world to see what ripples and what fades.

## Status
Pre-alpha. Only `packages/sim-core` exists: a deterministic hash-based RNG plus the lint rules that keep the simulation deterministic. The viewer comes later.

## Getting started
Requires Node 22+ and pnpm 10.

```powershell
pnpm install
pnpm check
```

`pnpm check` runs typecheck, lint and tests. See `CLAUDE.md` for the determinism rules every change must follow.
