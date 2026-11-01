# Q9b probe, no food limits: what each bracket option implies for real ages and growth.
# Individual microsim of the bracket rules (per-season hazards, aging by stage) with true ages tracked,
# plus the linear compartment model's growth rate and dependency ratio at its stable structure.
import numpy as np
from q9b_modes import MODES
LAB = np.array([0.25, 0.75, 1.0, 0.5]); NEED = np.array([0.6, 1.0, 1.0, 0.8])
rng = np.random.default_rng(7)
for name, (spans, ks, mort, b, fert) in MODES.items():
    ks4 = list(ks) + [1]; grp = np.repeat(np.arange(4), ks4)
    up = np.concatenate([[k/spans[i]]*k for i, k in enumerate(ks)] + [[0.0]]); m = np.asarray(mort)[grp]
    n = len(grp); fertile = np.isin(grp, fert)
    # linear model (expected values): x' = S x + births
    M = np.zeros((n, n))
    for j in range(n):
        surv = 1 - m[j]; M[j, j] += surv*(1-up[j])
        if j+1 < n: M[j+1, j] += surv*up[j]
        if fertile[j]: M[0, j] += b/2           # one birth per woman; women = half of fertile people
    ev, vec = np.linalg.eig(M); i = np.argmax(ev.real); lam = ev[i].real; v = np.abs(vec[:, i].real); v /= v.sum()
    g4 = np.array([v[grp == g].sum() for g in range(4)])
    dep = (g4 @ NEED)/(g4 @ LAB)
    # microsim: 200k newborns
    N = 200_000; stage = np.zeros(N, int); alive = np.ones(N, bool); age = np.zeros(N)
    ya_age = np.full(N, np.nan); fe_age = np.full(N, np.nan); el_age = np.full(N, np.nan); births = np.zeros(N); alive15 = None
    for t in range(480):
        if t == 60: alive15 = alive.mean()
        a = alive.copy(); g = grp[stage]
        births += np.where(a & fertile[stage], b, 0.0)
        die = a & (rng.random(N) < m[stage]); alive &= ~die
        mv = alive & (rng.random(N) < up[stage]); stage = np.minimum(stage + mv, n-1)
        g2 = grp[stage]; age += 1
        new_ya = alive & (g == 0) & (g2 == 1); ya_age[new_ya] = age[new_ya]/4
        new_fe = alive & ~fertile[np.where(mv, stage-1, stage)] & fertile[stage] & np.isnan(fe_age); fe_age[new_fe] = age[new_fe]/4
        new_el = alive & (g == 2) & (g2 == 3); el_age[new_el] = age[new_el]/4
    reached = ~np.isnan(ya_age); el = ~np.isnan(el_age)
    print(f"{name}: reach young-adult {reached.mean():.2f} | true l15 {alive15:.2f} | age entering young-adult "
          f"p10 {np.nanpercentile(ya_age,10):.1f} median {np.nanmedian(ya_age):.1f} p90 {np.nanpercentile(ya_age,90):.1f} yr | "
          f"first fertile p10 {np.nanpercentile(fe_age,10):.1f} median {np.nanmedian(fe_age):.1f} | entering elder p10 {np.nanpercentile(el_age,10):.0f} median {np.nanmedian(el_age):.0f} | births per woman reaching elder "
          f"{births[el].mean():.1f} | growth {100*(lam**4-1):+.2f}%/yr | stable mix C/YA/A/E {np.round(g4,2)} | need/labour {dep:.2f}", flush=True)
