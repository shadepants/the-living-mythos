# Q9a probe: stochastic (binomial) vs deterministic (expected value + carried remainder) demography
# on a filled map, rev 26-29 settings, then a severe 8-season local drought. args: bin|det seed
import sys, numpy as np, sysproto_r3 as S, run5 as R
S.DEMO = sys.argv[1]; seed = int(sys.argv[2])
R.EXCL, R.HOST_GUARD, S.EFF = 5, True, (0.5, 0.0); S.gMaxW *= 1.5; S.hMaxW *= 1.5; S.maxHunt = 0.01
K = np.full((S.H, S.W), 2.0); K[:, 50:] = 0.3          # r4e geometry: rich west, poor east strip
w = S.World(K, seed); w.bands = [S.Band('A', (12, 12), 25), S.Band('B', (36, 12), 25)]; ev = []
burn, dur = 2400, 8
sizes, hung, obs = [], 0, 0
for t in range(burn + 160):
    R.step(w, t, R.drought(t, burn, dur), 2, ev)
    al = [b for b in w.bands if b.alive and b.log]
    if 800 <= t < burn:                                  # years 200-600: filled map
        sizes += [b.br.sum() for b in al]; hung += sum(b.log[-1][3] > 0 for b in al); obs += len(al)
    if t == burn - 1:
        pre_bands = len(al); pre_dens = sum(b.br.sum() for b in al)/(S.W*S.H)
c = lambda k, a, z: sum(1 for e in ev if a <= e[0] < z and e[1] == k)
sz = np.array(sizes)
al = [b for b in w.bands if b.alive]
print(f"{S.DEMO} s{seed} | yr200-600: bands {pre_bands} dens {pre_dens:.2f} size mean {sz.mean():.1f} sd {sz.std():.1f} "
      f"min {sz.min():.0f} max {sz.max():.0f} hungry {hung/obs:.3f} fis {c('fission',800,burn)} diss {c('dissolved',800,burn)} "
      f"died {c('died',800,burn)} | drought+40yr: mig {c('migrated',burn,burn+160)} diss {c('dissolved',burn,burn+160)} "
      f"died {c('died',burn,burn+160)} fis {c('fission',burn,burn+160)} bands after {len(al)}", flush=True)
