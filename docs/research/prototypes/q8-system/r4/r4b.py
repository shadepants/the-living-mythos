# R4 probe 4: anchor per-worker return so a band on fresh land needs ~half its labour, then
# effort-scaled fertility. args: K e0|off fMin seed gScale
import sys, numpy as np, sysproto_r3 as S, run5 as R
R.EXCL = int(sys.argv[7]) if len(sys.argv) > 7 else 10; S.MDP = float(sys.argv[8]) if len(sys.argv) > 8 else 0.0; R.HOST_GUARD = len(sys.argv) > 6; K = float(sys.argv[1]); S.EFF = None if sys.argv[2] == 'off' else (float(sys.argv[2]), float(sys.argv[3]))
seed = int(sys.argv[4]); g = float(sys.argv[5]); S.gMaxW *= g; S.hMaxW *= g
w = S.World(np.full((S.H, S.W), K), seed)
w.bands = [S.Band('A', (12, 12), 25), S.Band('B', (44, 12), 25)]; ev = []; hung = obs = 0; effs = []; hbig = 0
for t in range(2400):
    R.step(w, t, 0.0, 2, ev)
    al = [b for b in w.bands if b.alive and b.log]
    hung += sum(b.log[-1][3] > 0 for b in al); hbig += sum(b.log[-1][3] > 0 and b.br.sum() > 50 for b in al); obs += len(al); effs += [getattr(b, 'eff', 0) for b in al]
    if (t+1) % 400 == 0:
        late = [e for e in ev if e[0] > t-400]; pops = [b.br.sum() for b in al] or [0]
        print(f"EX{R.EXCL} MDP{S.MDP} K{K} g{g} EFF{S.EFF} s{seed} t{t+1}: bands {len(al)} dens {sum(pops)/(S.W*S.H):.2f} size {min(pops):.0f}-{np.mean(pops):.0f}-{max(pops):.0f} "
              f"hungry {hung/max(obs,1):.3f} effort {np.mean(effs or [0]):.2f} meat {np.mean([b.log[-1][4] for b in al] or [0]):.2f} "
              f"fis {sum(e[1]=='fission' for e in late)} diss {sum(e[1]=='dissolved' for e in late)} hungerInBig {hbig/max(hung,1):.2f}", flush=True)
        hung = obs = 0; effs = []; hbig = 0
