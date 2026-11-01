# Q11 probe: band minimum sizes with no die-out floor (MIN_VIABLE=1), rev 34 migration (share).
# For each band: lowest population in the no-drought window (200 yr before) and in the drought window (60 yr after onset).
# args: scenario seed mag
import sys, numpy as np, sysproto_q10 as S, run5_q10 as R, variants
from q9b_modes import MODES
scen, seed, mag = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]); mmf = float(sys.argv[4]) if len(sys.argv) > 4 else 0.2
S.configure(*MODES['C']); S.HMODE = 'short'
R.EXCL, R.HOST_GUARD, S.EFF = 5, True, (0.5, 0.0); S.gMaxW *= 1.5; S.hMaxW *= 1.5; S.maxHunt = 0.01
variants.apply('share', S, R); S.MIN_VIABLE = int(sys.argv[5]) if len(sys.argv) > 5 else 1
S.mf = lambda a: np.clip(1 + 0.8*a, mmf, 1.2)   # minMoistureFactor floor (prototype default 0.2)
yy, xx = np.mgrid[0:S.H, 0:S.W]
if scen == 'map':
    K = np.full((S.H, S.W), 2.0); K[:, 50:] = 0.3; burn = 4800
    w = S.World(K, seed); w.bands = [S.Band('A', (12, 12), 25), S.Band('B', (36, 12), 25)]
    dr = lambda t: R.drought(t, burn, 8, mag=mag)
else:
    K = np.full((S.H, S.W), 0.06); K[np.sqrt((xx-16)**2+(yy-12)**2) <= 10] = 2.0; burn = 800
    w = S.World(K, seed); w.bands = [S.Band('A', (16, 12), 25)]
    dr = lambda t: R.drought(t, burn, 12, cx=16, cy=12, r=24, mag=mag)
pre, dro, ev = {}, {}, []
for t in range(burn + 240):
    R.step(w, t, dr(t), 2, ev)
    for b in w.bands:
        if not b.alive or not b.log or t - b.log[0][0] < 8: continue   # skip founding seasons
        p = b.br.sum(); hs = b.log[-1][3]
        if burn - 800 <= t < burn: pre[b.name] = min(pre.get(b.name, 99), p)
        elif t >= burn: dro[b.name] = (min(dro.get(b.name, (99, 0))[0], p), max(dro.get(b.name, (99, 0))[1], b.hungry))
fl = [5, 8, 10, 12, 15]
cnt = lambda d, f: sum(1 for v in d.values() if (v[0] if isinstance(v, tuple) else v) < f)
print(f"{scen} s{seed} m{mag} mmf{mmf} | bands pre {len(pre)} drought {len(dro)} | below floor (pre / drought) " +
      " ".join(f"{f}:{cnt(pre,f)}/{cnt(dro,f)}" for f in fl) +
      f" | drought mins {sorted(v[0] for v in dro.values())[:6]} | perished {sum(e[1]=='died' for e in ev if e[0]>=burn)} diss {sum(e[1]=='dissolved' for e in ev if e[0]>=burn)}", flush=True)
