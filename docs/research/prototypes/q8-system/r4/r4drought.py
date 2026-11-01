# R4a: drought on a FILLED map (burn 1600 seasons), run5 geometry (west K=2, east strip K=0.3), host guard on/off.
import sys, numpy as np, sysproto_r3 as S, run5 as R
R.HOST_GUARD = sys.argv[1] == 'hg'; seed = int(sys.argv[2]); burn = 1600; dur = 8
K = np.full((S.H, S.W), 2.0); K[:, 50:] = 0.3
w = S.World(K, seed); w.bands = [S.Band('A', (12, 12), 25), S.Band('B', (36, 12), 25)]; ev = []
for t in range(burn + 80): R.step(w, t, R.drought(t, burn, dur), 2, ev)
c = lambda a, b, k: sum(1 for e in ev if a <= e[0] < b and e[1] == k)
al = [b for b in w.bands if b.alive]
for lab, a, b in (('pre 200y', burn-800, burn), ('drought+18y', burn, burn+80)):
    print(f"HG{R.HOST_GUARD} s{seed} {lab}: mig {c(a,b,'migrated')} diss {c(a,b,'dissolved')} perished {c(a,b,'died')} fission {c(a,b,'fission')}")
print(f"  end: bands {len(al)} pop {sum(b.br.sum() for b in al):.0f}", flush=True)
