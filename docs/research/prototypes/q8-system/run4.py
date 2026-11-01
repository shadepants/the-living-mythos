# R2 test: A fixed camp (29-cell catchment at home), B seasonal camp choice inside home range r=5,
# C whole home range (81 cells) as the seasonal footprint. Two bands, local severe drought over band B's side.
import numpy as np, sys
import sysproto_r2 as S
from run1 import anom_field
S.W = 64
def run(mode, seed, dur=8, burn=400, after=120):
    S.MODE = mode
    K = np.full((S.H, S.W), 2.0); K[:, 50:] = 0.3
    w = S.World(K, seed); w.bands = [S.Band('A', (20, 12), 25), S.Band('B', (44, 12), 25)]
    for t in range(burn+after): S.season(w, t, anom_field(t, burn, dur, 0.9), None)
    out = []
    for b in w.bands:
        pre = [r for r in b.log if 200 <= r[0] < burn]; post = [r for r in b.log if r[0] >= burn]
        hp = sum(1 for r in pre if r[3] > 0); hq = sum(1 for r in post if r[3] > 0)
        pop0 = pre[-1][1]; mn = min(r[1] for r in post)
        mig = [m[0]-burn for m in b.migr if m[0] >= burn][:2]; mp = sum(1 for m in b.migr if m[0] < burn)
        moves = b.moves/((burn+after)/4)
        d = getattr(b, 'died', None)
        out.append(f"{b.name} pop{pop0:.0f} hungryPre{hp} migPre{mp} | hungryPost{hq} min{mn:.0f} mig{mig} died{None if d is None else d-burn} camp/yr{moves:.1f}")
    return "  ".join(out)
if __name__ == '__main__':
    for mode in sys.argv[1:]:
        for seed in (1, 2, 3):
            print(mode, seed, run(mode, seed))
