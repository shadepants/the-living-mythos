# Prey depression test: hunt cap vs no cap, with and without behavioural depression. 2 bands, no fission, no drought.
import numpy as np, sys
import sysproto_dep as S
S.W = 64
def run(seed, cap, psi, T=400):
    S.maxHunt = cap; S.PSI = psi
    K = np.full((S.H, S.W), 2.0); K[:, 50:] = 0.3
    w = S.World(K, seed); w.bands = [S.Band('A', (20, 12), 25), S.Band('B', (44, 12), 25)]
    for t in range(T): S.season(w, t, 0.0, None)
    out=[]
    for b in w.bands:
        hx,hy=b.home; ys,xs=np.mgrid[0:S.H,0:S.W]; m=(xs-hx)**2+(ys-hy)**2<=S.R_HOME**2
        Fr=w.F[m].mean()/0.227
        pre=[r for r in b.log if r[0]>=200]
        hung=sum(1 for r in pre if r[3]>0); meat=np.mean([r[4] for r in pre]); pop=b.log[-1][1]
        out.append(f"F{Fr:.2f} meat{meat:.2f} hungry{hung} pop{pop:.0f} campmoves/yr{b.moves/(T/4):.1f}")
    return " | ".join(out)
if __name__=="__main__":
  for cap,psi in ((0.01,0.0),(0.2,0.0),(0.2,0.5),(0.2,2.0)):
    print(f"cap {cap} psi {psi}: " + " || ".join(run(s,cap,psi) for s in (1,2)))
