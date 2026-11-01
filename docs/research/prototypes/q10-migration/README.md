# Q10 migration prototypes (throwaway; never port)

Evidence for decision log rev 34 (spec Q10, option C). Python floats + numpy RNG; base is `q9-demography/sysproto_q9c.py` with rev 26-33 settings (shortfall hunger mortality, effort fertility, host guard, homes >= 5 apart).

| File | What |
|---|---|
| `sysproto_q10.py` | Q9c prototype with the migration step made pluggable (`MIGRATE`) and a decision log (`DIAG`: move / nomargin / nosite / reverted) |
| `run5_q10.py` | Lifecycle wrapper; logs when a move is reverted by the home-spacing check; `NO_REVERT` switch |
| `variants.py` | `base` (Q9c: move then revert if within `homeRange` of another home), `free` (search free sites only, option A), `overlap` (no spacing, standing-stock score, option B), `share` (no spacing, score on stock x own labour / (own + overlapping residents' labour), option C); also `afterN`, `radN`, `marX` |
| `q10.py` | Driver: `python3 q10.py <variant> <map|island> <seed> [magnitude]`. Map = 64x24, rich K2 west of x 50, 2-band start, 1,200 yr burn (density per century printed), then 8-season local drought; island = rich disc ringed by barren land, 12-season drought |
| `batch.sh` | The runs behind `results_map.txt` and `results_island.txt` |

Findings (3 map seeds, 5 island seeds, shape only):
- Density plateau ~0.70 per rich cell from century 9-12.
- The Q9 prototypes' 0-1 migrations came from the spacing revert: `base` found a better target 13-21 times per drought and reverted every one.
- Migrations per drought, mag 0.9: base 0/0/0, free 1/0/3, overlap 5/10/3, share 2/6/4; mag 1.5: free 2/2/2, share 7/9/9.
- 0 migrations in the 200 no-drought years (share, overlap, seeds 1-2); 0 moves onto poor land; island bands never moved in any variant.
- Not measured: post-drought crowding in refuges (B vs C).
