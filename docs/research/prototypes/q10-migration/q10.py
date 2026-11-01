# Q10 probe: migration on a filled map (to a density plateau) and the island (no exit) case.
# args: variant scenario seed [mag] ; rev 26-33 settings as q9c.py option B (shortfall mortality).
import sys, numpy as np, sysproto_q10 as S, run5_q10 as R
from q9b_modes import MODES
from collections import Counter
var, scen, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]); mag = float(sys.argv[4]) if len(sys.argv) > 4 else 0.9
S.configure(*MODES['C']); S.HMODE = 'short'
R.EXCL, R.HOST_GUARD, S.EFF = 5, True, (0.5, 0.0); S.gMaxW *= 1.5; S.hMaxW *= 1.5; S.maxHunt = 0.01
import variants; variants.apply(var, S, R)
yy, xx = np.mgrid[0:S.H, 0:S.W]
if scen == 'map':
    K = np.full((S.H, S.W), 2.0); K[:, 50:] = 0.3; burn = 4800
    w = S.World(K, seed); w.bands = [S.Band('A', (12, 12), 25), S.Band('B', (36, 12), 25)]
    dr = lambda t: R.drought(t, burn, 8, mag=mag); ctr = (18, 12)
else:
    K = np.full((S.H, S.W), 0.06); K[np.sqrt((xx-16)**2+(yy-12)**2) <= 10] = 2.0; burn = 800
    w = S.World(K, seed); w.bands = [S.Band('A', (16, 12), 25)]
    dr = lambda t: R.drought(t, burn, 12, cx=16, cy=12, r=24, mag=mag); ctr = (16, 12)
rich = (K >= 2).sum(); ev = []; dens = []; hung = obs = 0; maxstreak = Counter(); trig = Counter()
for t in range(burn + 240):
    R.step(w, t, dr(t), 2, ev)
    al = [b for b in w.bands if b.alive]
    if t % 400 == 399: dens.append(sum(b.br.sum() for b in al)/rich)
    if burn - 800 <= t < burn:
        hung += sum(1 for b in al if b.log and b.log[-1][3] > 0); obs += len(al)
    if t >= burn:
        for b in al: maxstreak[b.name] = max(maxstreak[b.name], b.hungry)
pre = [b for b in w.bands if b.log and b.log[0][0] < burn]
inzone = [b for b in pre if np.hypot(b.home[0]-ctr[0], b.home[1]-ctr[1]) <= 20 or b.name in maxstreak]
d = [x for x in S.DIAG if x[0] >= burn]
c = lambda k: sum(1 for e in ev if e[0] >= burn and e[1] == k)
mv = [(b.name, m) for b in w.bands for m in b.migr if m[0] >= burn]
poor = sum(1 for _, m in mv if m[2][0] >= 50); dist = [np.hypot(m[2][0]-m[1][0], m[2][1]-m[1][1]) for _, m in mv]
ms = Counter(min(v, 6) for v in maxstreak.values())
pm = sum(1 for e in ev if burn-800 <= e[0] < burn and e[1] == "migrated"); pdis = sum(1 for e in ev if burn-800 <= e[0] < burn and e[1] in ("dissolved","died"))
print(f"pre-drought 200yr: mig {pm} endings {pdis} | " + f"{var} {scen} s{seed} m{mag} | dens/century(rich) " + " ".join(f"{x:.2f}" for x in dens) +
      f" | pre hungry {hung/max(obs,1):.3f} bands {len([b for b in w.bands if b.alive])} | drought: mig {c('migrated')} diss {c('dissolved')} "
      f"died {c('died')} fis {c('fission')} | max hungry streak hist {dict(sorted(ms.items()))} | dest poor {poor} dist {np.mean(dist) if dist else 0:.1f} | trig reasons {dict(Counter(x[2] for x in d))}", flush=True)
