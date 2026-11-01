# Q11 die-out floor prototypes (throwaway; never port)

Evidence for decision log rev 35 (spec Q11, option A: `minViable` 5). Base: `q10-migration/` (rev 34 share migration, rev 26-33 settings).

| File | What |
|---|---|
| `q11.py` | `python3 q11.py <map|island> <seed> <magnitude> [minMoistureFactor]`: floor off (`MIN_VIABLE` 1); per band, lowest population in the 200 no-drought years before the drought and in the 60 years after onset; counts bands below floors 5/8/10/12/15. Map runs 1,200 yr to the plateau first |
| `q11b.py` | Same with the floor as arg 5; counts perished bands |
| `sysproto_q10.py`, `run5_q10.py`, `variants.py`, `q9b_modes.py` | Copies from `q10-migration/` (variants gains a zero-labour guard) |
| `results_minsize.txt` | q11.py output (the mmf 0.0 island rows crashed on the divide by zero later guarded) |
| `results_island_floor5.txt` | q11b.py island runs, floor 5 |

Findings (shape only):
- Drought depth gates perishing, not the floor: with capacity kept at >= 20% (`minMoistureFactor` 0.2) islands bottom out at 12-24 people; floor 5 perished 0/5 islands at 0.2, 1/5 at 0.1 and 0.05, 5/5 at 0 (total failure).
- Filled map, bands below each floor in the 200 calm years / drought window (30-33 bands): 5: 0-1/0-1; 10: 2-3/0-5; 12: 4-6/1-5; 15: 7-10/5-7. Floors of 10+ end healthy small bands with no hunger cause.
- Found: the rev 34 share score divides by zero when a band reaches 0 labour before its end check (guard: share 0).
