# R4e: herd crash and recovery under drought on a filled map, rev 26-29 settings. args: cap seed [nobands]
import sys, numpy as np, sysproto_r3 as S, run5 as R
S.maxHunt = float(sys.argv[1]); seed = int(sys.argv[2]); nob = len(sys.argv) > 3
R.EXCL, R.HOST_GUARD, S.EFF = 5, True, (0.5, 0.0); S.gMaxW *= 1.5; S.hMaxW *= 1.5
K = np.full((S.H, S.W), 2.0); K[:, 50:] = 0.3
w = S.World(K, seed); w.bands = [] if nob else [S.Band('A', (12, 12), 25), S.Band('B', (36, 12), 25)]; ev = []
yy, xx = np.mgrid[0:S.H, 0:S.W]; core = np.sqrt((xx-18)**2+(yy-12)**2) <= 10
burn, dur = 1600, 8; Fs = []
for t in range(burn + 240):
    R.step(w, t, R.drought(t, burn, dur), 2, ev); Fs.append(w.F[core].mean())
pre = np.mean(Fs[burn-40:burn]); post = np.array(Fs[burn:]); low = post.min(); tl = int(post.argmin())
rec = next((i for i in range(tl, len(post)) if post[i] >= 0.9*pre), None)
first = next((i for i in range(len(post)) if post[i] < 0.97*pre), None)
c = lambda k: sum(1 for e in ev if e[0] >= burn and e[1] == k)
print(f"{'unhunted' if nob else 'cap'+str(S.maxHunt)} s{seed}: crash {1-low/pre:.0%} decline starts +{first} lowest +{tl} "
      f"90% recovery +{rec} seasons from onset | mig {c('migrated')} diss {c('dissolved')} perished {c('died')}", flush=True)
