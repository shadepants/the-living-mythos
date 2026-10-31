# Iteration 2: add band fission (> FISSION_AT) and territorial exclusion for new homes/migration targets.
import numpy as np
import sysproto as S
from run1 import anom_field
S.W = 64
FISSION_AT, EXCL = 50, 2*S.R_HOME

_orig_season = S.season
def far_from_others(w, b, x, y):
    return all((o is b) or (not o.alive) or (x-o.home[0])**2 + (y-o.home[1])**2 >= EXCL*EXCL for o in w.bands)

def season(w, t, anom):
    # restrict migration by patching Band.home search: run original, then undo moves into others' territory
    homes = {id(b): b.home for b in w.bands}
    _orig_season(w, t, anom, None)
    for b in list(w.bands):
        if not b.alive: continue
        if b.home != homes[id(b)] and not far_from_others(w, b, *b.home):
            b.home = b.camp = homes[id(b)]; b.migr.pop()   # target occupied: cancel
        if b.br.sum() > FISSION_AT and b.hungry == 0:
            sP, cnt = S.disc_sum(w.P, S.DISC); sF, _ = S.disc_sum(w.F, S.DISC)
            best = None; hx, hy = b.home
            for dy in range(-S.SEARCH, S.SEARCH+1):
                for dx in range(-S.SEARCH, S.SEARCH+1):
                    x, y = hx+dx, hy+dy
                    if 0 <= x < S.W and 0 <= y < S.H and w.Kveg[y, x] > 0.05 and far_from_others(w, None, x, y):
                        n = cnt[y, x]; m, p = S.yield_at(sP[y, x]/n, sF[y, x]/n, 10, 9e9, n)
                        if best is None or m+p > best[0] + 1e-12: best = (m+p, x, y)
            if best:
                nb = S.Band(b.name + str(len(w.bands)), (best[1], best[2]), 0)
                half = np.floor(b.br/2); nb.br = half; b.br = b.br - half
                w.bands.append(nb)

def run(seed, dur=8, mag=0.9, burn=600, after=200):
    K = np.full((S.H, S.W), 2.0); K[:, 50:] = 0.3
    w = S.World(K, seed); w.bands = [S.Band('A', (20, 12), 25), S.Band('B', (44, 12), 25)]
    for t in range(burn+after): season(w, t, anom_field(t, burn, dur, mag))
    return w

if __name__ == '__main__':
    for dur in (8, 16):
        print(f"severe drought {dur} seasons")
        for seed in range(1, 5):
            w = run(seed, dur); burn = 600
            alive_pre = [b for b in w.bands if (not hasattr(b, 'died')) or b.died >= burn]
            sizes = [int(b.log[-1][1]) if b.alive else 0 for b in w.bands]
            hpre = np.mean([sum(1 for r in b.log if 400 <= r[0] < burn and r[3] > 0) for b in alive_pre])
            mig = sum(1 for b in w.bands for m in b.migr if m[0] >= burn)
            died = [(b.name, b.died-burn) for b in w.bands if hasattr(b, 'died') and b.died >= burn]
            diedpre = sum(1 for b in w.bands if hasattr(b, 'died') and b.died < burn)
            print(f" seed {seed}: bands at drought {len(alive_pre)} (died pre {diedpre}), mean hungry seasons/band in prior 200 {hpre:.1f} | migrations {mig} | died out {died} | final sizes {sorted(sizes)}")
