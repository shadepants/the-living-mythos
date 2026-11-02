# Finalize: return-anchor probe (throwaway; never port)

Evidence for decision log rev 41 (spec finalize, option C: offline calibration tool writes the return constants). Base: `q12-events/` files (`sysproto_q10.py`, `q9b_modes.py`) alongside.

| File | What |
|---|---|
| `q17anchor.py` | Fields only (no bands) on uniform-K grids K 0.6-4, 800 seasons: herd and plant equilibrium, time for herds to settle within 5%, fresh effort of a 25-person reference band at the prototype ×1.5 return scale; then the scale solved per "median K" (1, 2, 3) and the resulting fresh effort across K |
| `results.txt` | Output |

Findings (shape only): herd stock is not proportional to K (F/K 0.02-0.12); settles in 37-173 seasons (K 0.6 never, near zero); plant stock ≈ 1.5-1.8 × K. Fresh effort at ×1.5: 1.00 / 0.75 / 0.50 / 0.38 / 0.34 / 0.33 at K 0.6 / 1 / 1.5 / 2 / 3 / 4. Per-world scaling: scale 1.49 / 0.76 / 0.68 at median K 1 / 2 / 3 (2× swing). Rev 28's 0.55 at K2 was measured while bands settled new land, not at the herd equilibrium.
