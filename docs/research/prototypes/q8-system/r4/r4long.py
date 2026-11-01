# Is density an equilibrium or a growth snapshot? Total population every 200 seasons.
import sys, numpy as np, sysproto_r3 as S, run5 as R
R.EXCL = int(sys.argv[1]); K = float(sys.argv[2]); N = int(sys.argv[3])
w = S.World(np.full((S.H, S.W), K), 1); w.bands = [S.Band('A', (12, 12), 25), S.Band('B', (44, 12), 25)]; ev = []
hung = 0; obs = 0
for t in range(N):
    R.step(w, t, 0.0, 2, ev)
    al = [b for b in w.bands if b.alive and b.log]
    hung += sum(b.log[-1][3] > 0 for b in al); obs += len(al)
    if (t+1) % 200 == 0:
        late = [e for e in ev if e[0] > t-200]
        print(f"EXCL{R.EXCL} K{K} t{t+1}: bands {len(al)} pop {sum(b.br.sum() for b in al):.0f} dens {sum(b.br.sum() for b in al)/(S.W*S.H):.2f} "
              f"hungry {hung/max(obs,1):.3f} meat {np.mean([b.log[-1][4] for b in al]):.2f} game {w.F.mean():.3f} "
              f"fis {sum(e[1]=='fission' for e in late)} diss {sum(e[1]=='dissolved' for e in late)}", flush=True)
        hung = obs = 0
