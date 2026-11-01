# R4 probe (throwaway, 2026-11-01)

Evidence for review R4 (`design/integration-review-2026-10-30.md`) and decision log rev 26. Python floats, numpy RNG, untuned, 1-2 seeds: shape evidence only. Never port.

`sysproto_r3.py` and `run5.py` here are modified copies of the parent folder's files: `EFF` (effort-scaled fertility) and `HOST_GUARD` were added; defaults reproduce rev 25. Run from this folder with Python 3 and numpy.

| Script | What it shows |
|---|---|
| `r4probe.py` | Uniform-richness maps, 200 yr: K 0.5 bands die, K 1 shrinks to 9-12, K ≥ 2 looks fine. Density "0.4" was a growth snapshot |
| `r4excl.py`, `r4excl2.py` | Home-range spacing 3-10 cells: identical results across richness, because the population was still growing |
| `r4long.py` | 600 yr: ~150-yr boom-bust once the map fills (0.2 → 0.7 → 0.2 per cell), 13-65 dissolutions per crash, no drought |
| `r4fert.py`, `r4fert2.py` | Effort-scaled fertility. At rev 23 values a band on fresh land uses ~80% of its labour, so fertility collapses; with per-worker return × 1.8 effort is ~45%, but boom-bust remains |
| `r4fert3.py` | Adds the host guard (arg `hg`): 0 dissolutions in years 200-600; density 0.55 (K 2) to 1.3 (K 4) per cell; meat 32-41%; background hunger 3-10%; bands 60-140 where fission is blocked |
| `r4drought.py` | Drought on a filled map (run5 geometry): no guard, 13-18 dissolutions in the 200 yr before; guard, quiet baseline but 0-1 migrations and no endings |
