# Q7 fauna prototype (throwaway)

Status 2026-10-30: evidence for decision log rev 22 (spec Q7). Not sim code: Python floats, no determinism rules, never port.

Run from this folder (scripts load `q7.py` by relative path): `python3 q7.py`, then `q7b.py` … `q7e.py`.

| Script | What it shows |
|---|---|
| `q7.py` | Model C (herd condition, Type II intake) + rev 21 vegetation; no-drought runs at richness 0.5-4. Without density mortality, herds cycle at richness 2 and 4 |
| `q7b.py` | Adds `mDens`; cycling stops at ≥ 0.05; severe 8-season drought at richness 2: lag, vegetation and herd recovery |
| `q7c.py` | 128-setting sweep against the report's targets: none met all |
| `q7d.py` | Summary of that sweep (all viable settings oscillated) |
| `q7e.py` | 576-setting sweep: 131 stable with ≥ 25% crash; all took ≥ 30 seasons to recover |

Results are recorded in the decision log (rev 22) and handoff #7 §8.
