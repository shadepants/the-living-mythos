# Q9c probe: hunger mortality form, rev 26-32 settings (demography = Q9b option C).
# args: mode (R/A/B) scenario (map/island) seed [drought magnitude]
#   map    = filled map (750 yr) then a severe 8-season local drought, as in q9b.py
#   island = one band on a rich patch ringed by barren land (no migration target, no host), drought over the patch
import sys, numpy as np, sysproto_q9c as S, run5_q9c as R
from q9b_modes import MODES
mode, scen, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]); mag = float(sys.argv[4]) if len(sys.argv) > 4 else 0.9
S.configure(*MODES['C'])
if mode == 'R':   # rev 30 prototype rates and the old hunger fertility factor (redundancy check)
    S.set_state_rates(0.01, 0.05, [2, 1, 1, 2]); S.FERT = {0: 1.0, 1: 0.5, 2: 0.1}
elif mode == 'A': # hunger states, prompt 8 age shape (children 2.5x, elders 3.5x adults), effort-only fertility
    S.set_state_rates(0.01, 0.05, [2.5, 1, 1, 3.5])
else:             # shortfall-scaled
    S.HMODE = 'short'
R.EXCL, R.HOST_GUARD, S.EFF = 5, True, (0.5, 0.0); S.gMaxW *= 1.5; S.hMaxW *= 1.5; S.maxHunt = 0.01
yy, xx = np.mgrid[0:S.H, 0:S.W]
if scen == 'map':
    K = np.full((S.H, S.W), 2.0); K[:, 50:] = 0.3; burn = 3000
    w = S.World(K, seed); w.bands = [S.Band('A', (12, 12), 25), S.Band('B', (36, 12), 25)]
    dr = lambda t: R.drought(t, burn, 8, mag=mag)
else:
    K = np.full((S.H, S.W), 0.06); K[np.sqrt((xx-16)**2+(yy-12)**2) <= 10] = 2.0; burn = 800
    w = S.World(K, seed); w.bands = [S.Band('A', (16, 12), 25)]
    dr = lambda t: R.drought(t, burn, 12, cx=16, cy=12, r=24, mag=mag)
ev = []; hung = obs = 0; sizes = []; traj = []; kids = []
for t in range(burn + 240):
    R.step(w, t, dr(t), 2, ev)
    al = [b for b in w.bands if b.alive and b.log]
    if burn - 1200 <= t < burn:
        hung += sum(b.log[-1][3] > 0 for b in al); obs += len(al); sizes += [b.br.sum() for b in al]
    if t >= burn - 4:
        traj.append(sum(b.br.sum() for b in al if np.hypot(b.home[0]-(18 if scen == 'map' else 16), b.home[1]-12) <= 20))
        kids.append(sum(b.br[S.GROUP == 0].sum() for b in al)/max(1, sum(b.br.sum() for b in al)))
c = lambda k: sum(1 for e in ev if e[0] >= burn and e[1] == k)
tr = np.array(traj); pre = tr[:4].mean(); low = tr[4:].min(); tl = int(tr[4:].argmin())
print(f"{mode} {scen} s{seed} mag{mag} | pre-drought: hungry {hung/max(obs,1):.3f} size {np.mean(sizes):.1f} | drought: pop {pre:.0f} -> {low:.0f} "
      f"(-{1-low/max(pre,1):.0%}) lowest +{tl} | child share {kids[3]:.2f} -> {min(kids[4:]):.2f} | mig {c('migrated')} diss {c('dissolved')} "
      f"perished {c('died')} | hungry-season births possible {S.REDUNDANT_CHECK}", flush=True)
