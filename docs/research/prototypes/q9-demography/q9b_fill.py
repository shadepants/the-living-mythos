# Q9b probe: is the map filled? Density every 100 yr to 800 yr, no drought. args: mode seed
import sys, numpy as np, sysproto_q9b as S, run5_q9b as R
from q9b_modes import MODES
mode, seed = sys.argv[1], int(sys.argv[2]); S.configure(*MODES[mode])
R.EXCL, R.HOST_GUARD, S.EFF = 5, True, (0.5, 0.0); S.gMaxW *= 1.5; S.hMaxW *= 1.5; S.maxHunt = 0.01
K = np.full((S.H, S.W), 2.0); K[:, 50:] = 0.3
w = S.World(K, seed); w.bands = [S.Band('A', (12, 12), 25), S.Band('B', (36, 12), 25)]; ev = []; out = []
for t in range(3200):
    R.step(w, t, 0.0, 2, ev)
    if (t+1) % 400 == 0:
        al = [b for b in w.bands if b.alive]
        out.append(f"{sum(b.br.sum() for b in al)/(S.W*S.H):.2f}/{len(al)}")
print(f"{mode} s{seed} density/bands by century 1-8: {' '.join(out)}", flush=True)
