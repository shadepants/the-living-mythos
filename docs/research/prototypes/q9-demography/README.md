# Q9 demography probes (throwaway, 2026-11-01)

Evidence for spec Q9 (decision log rev 31 onward). Python floats, numpy RNG, untuned, 3 seeds: shape evidence only. Never port.

`sysproto_r3.py` and `run5.py` are copies of `../q8-system/r4/` with a `DEMO` switch: `'bin'` = binomial draws (Q9a options A and B, same distribution), `'det'` = expected value with a carried remainder per band (option C). Run from this folder with Python 3 and numpy.

| Script | What it shows |
|---|---|
| `q9a.py` (args: `bin`/`det`, seed) | Filled map (r4e geometry, rev 26-29 settings), 600 yr, then a severe 8-season local drought. bin: 32-35 bands, density 0.60-0.62, size mean 30-31 (sd 7.6-7.8), 24-29 fissions in yr 200-600. det: 18 bands, density 0.48, size mean 40 (sd 5.7), 10 fissions, identical across seeds 1-3. Drought +40 yr: 0-1 migrations and 0-1 dissolutions in both (the known Q11/tuning gap) |
| `q9a_sampler.py` | Spec §10 inverse-CDF binomial vs exact pmf: worst total-variation distance 8.2e-5 over 49 (n, q) cases (1/65,536 grid); edge cases q = 0, 1, n = 0 |
| `q9a_mono.py` | Monotonicity in q for a fixed u: v0.16 same-u flip 2,838 violations of 1,194,000; 1 − u flip 0 |

## Q9b (rev 32)
`sysproto_q9b.py` / `run5_q9b.py` add `configure()`: per-bracket spans, hidden stages (Erlang aging), mortality, birth rate, fertile brackets. Options in `q9b_modes.py` (R = rev 30 prototype rates; A draft cuts; B 3 hidden stages; C role cuts 0-14/15-19/20-44/45+ (picked); D role cuts, adults-only fertility).

| Script | What it shows |
|---|---|
| `q9b_theory.py` | No food limit, 200k-person microsim with true ages: median age at first fertility A/C 6 yr, B/D 11 (Walker et al. 2006: ~19); elder entry median A 32, B 43, C/D 28; intrinsic growth R +1.32, A +0.72, B +0.89, C +0.86, D +0.59 %/yr; need/labour 1.34-1.37 |
| `q9b.py` (args: mode, seed) | Filled-map run + severe drought, 3 seeds per option: drought outcomes 0-1 events in every option, core population drop 2-23% with seed noise dominating |
| `q9b_fill.py` | Density/bands per century to 800 yr (seed 1): R fills by century 4 (~0.6); B and C by century 7 (0.50-0.55); A 0.42 and D 0.31 still rising at century 8 |

## Q9c (rev 33)
`sysproto_q9c.py` / `run5_q9c.py` add `HMODE` ('state' = mortality by hunger state; 'short' = shortfall × rate per bracket, picked), effort-only fertility, and a counter of hungry seasons where effort fertility is above 0.

| Script | What it shows |
|---|---|
| `q9c.py` (args: R/A/B, map/island, seed, magnitude) | Redundancy counter 0 in every run (the hunger fertility factor never acts). Filled map (750 yr) + severe drought: A and B −11-13%, background hunger 0, B s2 2 perished. Island (one band, no exit, 12-season drought, magnitudes 0.9 and 1.5, 5 seeds × 3 modes): shortfall 0.15-0.5, 9-14 starving seasons, band −3-59%, settles at 12-20 people, never perished |
