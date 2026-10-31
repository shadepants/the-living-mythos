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
