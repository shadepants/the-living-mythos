# Finalize: band-card food-trend prototype (throwaway; never port)

Evidence for the spec finalize food-trend question (spec §16). Streams regenerated with `q13-glance/q13run.py` (needs the `q12-events/` base files alongside); trend variants applied offline by `q16trend.py <pkl...>`.

| File | What |
|---|---|
| `q16trend.py` | Variants: `bal4` (v0.24: mean of last 4 balances ÷ consumption), `effD4` (effort now − 4 seasons ago), `pressD4` (pressure = effort + shortfall, now − 4 seasons ago; band 0.05 or 0.10), `pressMM` (mean of last 4 pressures − mean of previous 4). Labels easing / steady / worsening. Reports calm shares (200 yr before the drought), flicker, drought-window shares, shares 8 seasons after, and lead from the first `worsening` to hunger onset |
| `results_*.txt` | Map seeds 1-3 × magnitude 1.5; map seed 2 × 0.9; island seeds 1-3 × 1.5; density per century |

Findings (shape only): `bal4` reads easing in 100% of calm band-seasons and warns of hunger 0 seasons ahead (23/36). `effD4` and `pressD4` at band 0.05 flicker 0.50 changes per band-year in calm. `pressD4` at band 0.10: calm 99.8% steady, flicker 0.01, 36/36 map hunger onsets preceded by `worsening` (median 4 seasons lead, 1-8). `pressMM` 0.05: calm 97.9% steady, flicker 0.10, lead median 3. The prototype has no seasonal cycle, so a 4-season lag is untested against seasonality.
