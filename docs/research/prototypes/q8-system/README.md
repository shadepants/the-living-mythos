# Whole-system prototypes (throwaway)

Status 2026-10-30: evidence for `design/integration-review-2026-10-30.md` (spec Q8 rethink). Not sim code: Python floats, numpy RNG, untuned parameters, no determinism rules. Never port.

Run from this folder with Python 3 and numpy.

| Script | What it shows |
|---|---|
| `eco.py` | Rev 22 fauna + rev 21 vegetation for one lumped cell (from the Q7 prototype, `mDens` 0.1) |
| `band.py` | One band on a lumped 29-cell catchment; yield options A (spec v0.8 linear), B (fixed split, Type II), C (rank-and-cap, satisficing). First calibration: game hunted out in all three |
| `band2.py` - `band4.py` | Sweeps of hunt cap, gathering return and food per herd unit. Hunting holds game at 38-64%; cap 1.5%/season collapses it; severe drought hunger ends 2-6 seasons after the drought |
| `sysproto.py` | Integrated model: guilds (game, plant foods), rank-and-cap, home range with seasonal camp choice, migration, binomial demography, die-out at 5 |
| `run1.py` | Two bands, no fission, drought 8 and 16 seasons: bands grow to 32-78, background hunger, both migrate, no die-out |
| `run2.py` | Adds fission above 50 and kept-apart homes: 10-13 bands, almost no background hunger, no migrations and no die-outs under drought. Its "bands at drought" figure counts all bands ever founded (reporting bug, harmless) |
| `sysproto_dep.py`, `run3.py` - `run3d.py` | Behavioural prey depression (hunters see F/(1+ψ·recent hunting labour)) and return-ordered vs fixed-rank allocation, 2 bands, no drought. No clear protective effect at these settings; results noisy (2 seeds). `campmoves/yr` = 4.0 everywhere is an artifact: the camp is re-chosen every season |
| `sysproto_r2.py`, `run4.py` | R2: fixed camp (A, 29-cell catchment) vs seasonal camp choice inside a radius-5 home range (B) vs whole home range as the footprint (C, 81 cells). 2 bands, no fission, severe 8-season drought, 3 seeds. Band size tracks footprint (A 34-42, B 57-77, C 57-120); background hunger per 200 seasons A 9-19, B 0-14, C 0-4; in all three both bands migrated and none died. Run: `python3 run4.py A B C` |
