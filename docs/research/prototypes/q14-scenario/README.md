# Q14 test-scenario prototypes (throwaway; never port)

Evidence for spec Q14 (test scenario and pass sentence). Base: `q12-events/` rules (rev 26-35) with the rev 36 emitter (`q12lean.emit`, `causeWindow` 8).

| File | What |
|---|---|
| `q14run.py` | `python3 q14run.py <map|island|fixture|fixture2> <seed> <magnitude> <out.pkl>`: `q13run.py` plus two hand-built fixtures and `pbase` (catchment plant stock vs base, no-drought capacity). Magnitude 0 = no-drought control with the same history up to the drought season. Map: 1,200 yr to the plateau, prints density per century |
| `q14chain.py` | `python3 q14chain.py <pkl...>`: pass check (≥ 1 `band_migrated` and ≥ 1 non-`dwindled` `band_died_out` in [drought start, drought end + `causeWindow`], each ≤ 3 hops to `drought_began`), same counts in an equal calm window, and Legends sentences rendered from the real chain (presentation names) |
| `sysproto_q10.py`, `run5_q10.py`, `variants.py`, `q9b_modes.py`, `q12lean.py` | Copies from `q12-events/` |
| `results_*.txt` | Outputs: filled map (3 seeds × magnitude 0.9 / 1.5), no-drought controls (3 seeds) + seed 1 rerun with base-capacity stock, island (5 seeds), fixtures (9 runs) |

Findings (shape only):
- Plateau 0.66-0.73 per rich cell from century 8-10 (3 seeds, reproduced exactly).
- Filled map + local drought: 5/6 runs pass (fail: seed 1 at magnitude 0.9, 2 migrations, no die-out). Per run 2-8 migrations, 0-2 dissolutions, all chained in 2 hops (outcome → `forage_failed` → `drought_began`).
- No-drought controls (same seed, same history): 0 migrations and 0 endings in the test window, 3/3. Calm window before the drought: one `dwindled` (seed 1), nothing else.
- Island: 0/5 (no outcomes; bands go hungry together or not at all).
- Hand-built fixtures, 0/9: patches of radius 4-5 could not sustain bands (all ended before the drought); radius-7 patches kept the bands, but the "cut-off" band migrated onto the host's patch (share-discounted host land still beat its droughted range) or nobody went hungry. Producing "D dissolves into H" would mean tuning geometry toward an outcome.
- Dissolution hosts: 3 of 8 lay 14.1-14.3 cells away, inside `hostRange` 15 but outside `searchRadius` 14 (a host there can't also be a migration target); 3 were adjacent (1.0-1.4 cells), 1 at 12.6.
- `stockPct` against the drought-lowered capacity read 30-66% for bands whose plant stock was 10-11% of normal; the Legends need the base (worldgen) capacity as the denominator.
