# Q13 glance-word prototype (throwaway; never port)

Evidence for decision log rev 37 (spec Q13, option C: severity first, starving > hungry > well-fed > settled). Base: `q12-events/` (needs its `sysproto_q10.py`, `run5_q10.py`, `variants.py`, `q9b_modes.py` alongside).

| File | What |
|---|---|
| `q13run.py` | `q12run.py` plus per-band consumption (stash ratio). Same args |
| `q13glance.py` | `python3 q13glance.py <pkl...>`: variants `draft` (restless first, trend rules), `severity`, `ladder` (trend-based with lean and default), `effort` (picked), `effort_hyst` (enter 0.5, leave 0.55). Word shares calm 200 yr / drought 60 yr, flicker, word shown the season before migrating or ending, restless vs starving overlap |
| `results_*.txt` | Outputs (3 map seeds × magnitude 1.5; 5 islands × 1.5). The `effort` rows label the word `thriving`; the decision renames it `well-fed` |

Findings (shape only):
- restless ⊂ starving in 120/120 band-seasons (`migrateAfter` = `starvingSeasons` = 2); restless-first hid starving on 5/5 dissolving bands.
- Plateau: balance +0.11-0.14 × consumption every season (stash upkeep), stash 0.36-0.39 × consumption, effort median 0.60 (p5-p95 0.47-0.67). Draft trend rules: 99% of calm band-seasons get no word.
- Effort rule: calm 8% at or below `effortFull`, flicker 0.06 changes per band-year (0.02 with hysteresis). Perishing (dwindled) bands read low-effort to the end (4/4).
- `lean` (negative balance, not hungry): 0-0.1% of seasons, at most 1 season long.
