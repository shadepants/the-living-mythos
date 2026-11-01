# R4d: hunt cap vs meat share and game depletion under rev 26-28 settings
# (host guard, effort fertility 0.5/0, homes 5 apart, return x1.5). args: K maxHunt seed
import sys, numpy as np, sysproto_r3 as S, run5 as R
K = float(sys.argv[1]); S.maxHunt = float(sys.argv[2]); seed = int(sys.argv[3])
R.EXCL, R.HOST_GUARD, S.EFF = 5, True, (0.5, 0.0); S.gMaxW *= 1.5; S.hMaxW *= 1.5
Km = np.full((S.H, S.W), K); w = S.World(Km, seed); w0 = S.World(Km, seed)
w.bands = [S.Band('A', (12, 12), 25), S.Band('B', (44, 12), 25)]; ev = []
acc = dict(h=0, o=0, m=[], g=[])
for t in range(2400):
    R.step(w, t, 0.0, 2, ev); w0.step_fields(0.0)
    if t >= 1600:
        al = [b for b in w.bands if b.alive and b.log]
        acc['h'] += sum(b.log[-1][3] > 0 for b in al); acc['o'] += len(al); acc['m'] += [b.log[-1][4] for b in al]
        acc['g'].append(w.F.mean()/w0.F.mean())
al = [b for b in w.bands if b.alive]; pops = [b.br.sum() for b in al]
print(f"K{K} cap{S.maxHunt} s{seed} yr400-600: bands {len(al)} dens {sum(pops)/(S.W*S.H):.2f} size {np.mean(pops):.0f} "
      f"meat {np.mean(acc['m']):.2f} game/unhunted {np.mean(acc['g']):.2f} (min {min(acc['g']):.2f}) hungry {acc['h']/acc['o']:.3f} "
      f"diss {sum(e[1]=='dissolved' for e in ev)}", flush=True)
