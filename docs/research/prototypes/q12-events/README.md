# Q12 event-cause prototypes (throwaway; never port)

Evidence for decision log rev 36 (spec Q12, option B: climate lookback `causeWindow`, shortfall episodes, outcome `dwindled`). Base: `q11-minviable/` (rev 26-35 rules, `variants.apply('share', S, R)`, `MIN_VIABLE` 5).

| File | What |
|---|---|
| `q12run.py` | `python3 q12run.py <map|island> <seed> <magnitude> <out.pkl>`: runs the base and dumps per-band, per-season facts (balance, hunger streak, camp, drought exposure, catchment stock ratio, labour share, lifecycle action with host or daughter). Map: 1,200 yr to the plateau, 8-season drought; island: 12-season drought. Prints density per century |
| `q12emit.py` | `python3 q12emit.py spec <pkl...>`: §14 as written (climate cited only while active, most recent `forage_failed`); per-outcome hop counts to `drought_began` |
| `q12lean.py` | `python3 q12lean.py <window> <pkl...>`: option B (lookback on the band's own drought exposure, episode-scoped citations, `dwindled`); totals |
| `q12inspect.py`, `q12inspect2.py` | Histories of causeless perishings; classification of causeless `forage_failed` (timing, migrant or resident, nearby arrivals, stock, share) |
| `sysproto_q10.py`, `run5_q10.py`, `variants.py`, `q9b_modes.py` | Copies from `q11-minviable/` |
| `results_*.txt` | Outputs. Note: map runs with the same seed share their pre-drought history, so calm-window counts in `results_lookback_map.txt` double-count across magnitudes |

Findings (shape only):
- Plateau 0.66-0.72 people per rich cell from century 8-10, 3 seeds.
- Drought window: 39/39 outcomes (31 migrations, 8 dissolutions) reached `drought_began` in 2 hops under both rules.
- §14 as written left 15/83 drought-window `forage_failed` causeless, mostly 1-5 seasons after the drought ended (herd lag; stock 10-24% of capacity). Lookback 4 left 4, 8 and 16 left 2 (14+ seasons after; unrelated).
- 0 `forage_failed` in the calm 200 years at the plateau; 4 during the fill (one oversized band, stock ~30%, then split).
- 3 distinct calm perishings in 3,600 band-years: zero hunger, effort 0.35-0.43, drift from ~10 to 5 over 15 years (demographic chance). Emitted as `dwindled`, no causes.
- 0 hunger events without a `forage_failed`; island 0 endings, 0 causeless failures.
- Prototype choices, not from the spec: `stableSeasons` 2; the episode closes after 2 non-negative, non-hungry seasons; exposure = drought strength > 0 at the camp cell.
