# R4 probe: what do the rev 23-25 [P] values produce against prompt 10 targets?
# Uniform-richness maps, no drought, lifecycle L2 + fission guard. Measures after burn-in:
# people per land cell, band sizes, meat share of yield, game stock vs unhunted, hunger.
import sys, numpy as np
import sysproto_r3 as S, run5 as R

def measure(Kval, seed, seasons=800, tail=200, meatConv=None):
    if meatConv: S.meatConv = meatConv
    K = np.full((S.H, S.W), Kval)
    w0 = S.World(K, seed)                       # unhunted reference
    for t in range(seasons): w0.step_fields(0.0)
    w = S.World(K, seed); w.bands = [S.Band('A', (12, 12), 25), S.Band('B', (44, 12), 25)]; ev = []
    meat = []; hung = 0; bs = []
    for t in range(seasons):
        R.step(w, t, 0.0, 2, ev)
        if t >= seasons - tail:
            alive = [b for b in w.bands if b.alive]
            for b in alive:
                if not b.log: continue
                meat.append(b.log[-1][4]); hung += b.log[-1][3] > 0
            bs.append([b.br.sum() for b in alive])
    alive = [b for b in w.bands if b.alive]
    pops = [b.br.sum() for b in alive] or [0]
    meat = meat or [0]
    late = [e for e in ev if e[0] >= seasons - tail]
    return dict(K=Kval, seed=seed, bands=len(alive), dens=sum(pops)/(S.W*S.H),
                bmin=min(pops), bmean=np.mean(pops), bmax=max(pops), meat=np.mean(meat),
                game=w.F.mean()/max(w0.F.mean(), 1e-9), hungry=hung/max(1, len(meat)),
                ev={k: sum(1 for e in late if e[1] == k) for k in ('fission', 'dissolved', 'migrated', 'died')})

if __name__ == '__main__':
    mc = float(sys.argv[1]) if len(sys.argv) > 1 else None
    for Kval in (0.5, 1.0, 2.0, 4.0):
        for seed in (1, 2):
            r = measure(Kval, seed, meatConv=mc)
            print(f"K{r['K']} s{r['seed']}: bands {r['bands']} dens {r['dens']:.2f}/cell size {r['bmin']:.0f}-{r['bmean']:.0f}-{r['bmax']:.0f} "
                  f"meat {r['meat']:.2f} game {r['game']:.2f} hungry {r['hungry']:.3f} last50yr {r['ev']}", flush=True)
