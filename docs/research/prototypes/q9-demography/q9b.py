# Q9b probe: bracket options on a filled map (rev 26-31 settings), 600 yr, then a severe 8-season local drought.
# args: mode (R/A/B/C) seed
import sys, numpy as np, sysproto_q9b as S, run5_q9b as R
from q9b_modes import MODES
mode, seed = sys.argv[1], int(sys.argv[2]); S.configure(*MODES[mode])
R.EXCL, R.HOST_GUARD, S.EFF = 5, True, (0.5, 0.0); S.gMaxW *= 1.5; S.hMaxW *= 1.5; S.maxHunt = 0.01
K = np.full((S.H, S.W), 2.0); K[:, 50:] = 0.3
w = S.World(K, seed); w.bands = [S.Band('A', (12, 12), 25), S.Band('B', (36, 12), 25)]; ev = []
burn, dur = 2400, 8
sizes, hung, obs, effs, pops = [], 0, 0, [], []
yy, xx = np.mgrid[0:S.H, 0:S.W]
for t in range(burn + 240):
    R.step(w, t, R.drought(t, burn, dur), 2, ev)
    al = [b for b in w.bands if b.alive and b.log]
    if 800 <= t < burn:
        sizes += [b.br.sum() for b in al]; hung += sum(b.log[-1][3] > 0 for b in al); obs += len(al)
        effs += [getattr(b, 'eff', 0) for b in al]
    # population of bands whose home is inside the drought radius (r = 20 around (18, 12))
    pops.append(sum(b.br.sum() for b in al if (b.home[0]-18)**2+(b.home[1]-12)**2 <= 400))
c = lambda k, a, z: sum(1 for e in ev if a <= e[0] < z and e[1] == k)
p = np.array(pops); pre = p[burn-40:burn].mean(); post = p[burn:]; tl = int(post.argmin())
rec = next((i for i in range(tl, len(post)) if post[i] >= 0.95*pre), None)
sz = np.array(sizes)
print(f"{mode} s{seed} | yr200-600: dens {sum(b.br.sum() for b in w.bands if b.alive and b.log)/(S.W*S.H):.2f} "
      f"size {sz.mean():.1f}±{sz.std():.1f} hungry {hung/obs:.3f} effort {np.mean(effs):.2f} fis {c('fission',800,burn)} "
      f"diss {c('dissolved',800,burn)} died {c('died',800,burn)} | drought: core pop -{1-post.min()/pre:.0%} lowest +{tl} "
      f"95% back +{rec} | mig {c('migrated',burn,burn+240)} diss {c('dissolved',burn,burn+240)} died {c('died',burn,burn+240)}", flush=True)
