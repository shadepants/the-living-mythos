# R4 probe 3: effort-scaled fertility vs boom-bust. Long runs, no drought.
import sys, numpy as np, sysproto_r3 as S, run5 as R
R.EXCL = 10; K = float(sys.argv[1]); S.EFF = None if sys.argv[2] == 'off' else (float(sys.argv[2]), float(sys.argv[3]))
w = S.World(np.full((S.H, S.W), K), int(sys.argv[4]) if len(sys.argv) > 4 else 1)
w.bands = [S.Band('A', (12, 12), 25), S.Band('B', (44, 12), 25)]; ev = []; hung = obs = 0; effs = []
for t in range(2400):
    R.step(w, t, 0.0, 2, ev)
    al = [b for b in w.bands if b.alive and b.log]
    hung += sum(b.log[-1][3] > 0 for b in al); obs += len(al); effs += [getattr(b, 'eff', 0) for b in al]
    if (t+1) % 400 == 0:
        late = [e for e in ev if e[0] > t-400]; pops = [b.br.sum() for b in al]
        print(f"K{K} EFF{S.EFF} t{t+1}: bands {len(al)} dens {sum(pops)/(S.W*S.H):.2f} size {min(pops):.0f}-{np.mean(pops):.0f}-{max(pops):.0f} "
              f"hungry {hung/max(obs,1):.3f} effort {np.mean(effs):.2f} meat {np.mean([b.log[-1][4] for b in al]):.2f} "
              f"fis {sum(e[1]=='fission' for e in late)} diss {sum(e[1]=='dissolved' for e in late)}", flush=True)
        hung = obs = 0; effs = []
