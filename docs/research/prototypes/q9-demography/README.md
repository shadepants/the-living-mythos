# Q9 demography probes (throwaway, 2026-11-01)

Evidence for spec Q9 (decision log rev 31 onward). Python floats, numpy RNG, untuned, 3 seeds: shape evidence only. Never port.

`sysproto_r3.py` and `run5.py` are copies of `../q8-system/r4/` with a `DEMO` switch: `'bin'` = binomial draws (Q9a options A and B, same distribution), `'det'` = expected value with a carried remainder per band (option C). Run from this folder with Python 3 and numpy.

| Script | What it shows |
|---|---|
| `q9a.py` (args: `bin`/`det`, seed) | Filled map (r4e geometry, rev 26-29 settings), 600 yr, then a severe 8-season local drought. bin: 32-35 bands, density 0.60-0.62, size mean 30-31 (sd 7.6-7.8), 24-29 fissions in yr 200-600. det: 18 bands, density 0.48, size mean 40 (sd 5.7), 10 fissions, identical across seeds 1-3. Drought +40 yr: 0-1 migrations and 0-1 dissolutions in both (the known Q11/tuning gap) |
| `q9a_sampler.py` | Spec §10 inverse-CDF binomial vs exact pmf: worst total-variation distance 8.2e-5 over 49 (n, q) cases (1/65,536 grid); edge cases q = 0, 1, n = 0 |
| `q9a_mono.py` | Monotonicity in q for a fixed u: v0.16 same-u flip 2,838 violations of 1,194,000; 1 − u flip 0 |
