# Finalize probe: return-anchor scale. Fields only (no bands) on uniform-K grids: how long until
# unforaged stocks settle, and how fresh effort of a reference band varies with K under a fixed
# return scale (prototype x1.5) vs a scale computed so median land gives effortFull. Throwaway; never port.
import numpy as np, sysproto_q10 as S
from q9b_modes import MODES
S.configure(*MODES['C']); S.gMaxW *= 1.5; S.hMaxW *= 1.5; S.maxHunt = 0.01
br = S.expand_start(25); L = float(br @ S.LAB); C = float(br @ S.NEED); n = len(S.DISC)
def effort(Pm, Fm, k=1.0):
    g0, h0 = S.gMaxW, S.hMaxW; S.gMaxW, S.hMaxW = g0*k, h0*k
    m, p = S.yield_at(Pm, Fm, L, C, n); rH = S.hMaxW*Fm/(Fm+S.hF); rG = S.gMaxW*Pm/(Pm+S.hP)
    used = (m/rH if rH > 0 else 0) + (p/rG if rG > 0 else 0)
    S.gMaxW, S.hMaxW = g0, h0
    return min(1.0, used/L) if m+p >= C-1e-9 else 1.0
print(f'reference band 25: L={L:.2f} C={C:.2f}')
res = {}
for K in (0.6, 1.0, 1.5, 2.0, 3.0, 4.0):
    w = S.World(np.full((S.H, S.W), K)); Fs, Ps = [], []
    for t in range(800):
        w.step_fields(0.0); Fs.append(w.F.mean()); Ps.append(w.P.mean())
    Fe, Pe = np.mean(Fs[-100:]), np.mean(Ps[-100:])
    settle = next((t for t in range(800) if all(abs(f-Fe) <= 0.05*Fe for f in Fs[t:])), None)
    amp = (max(Fs[-100:])-min(Fs[-100:]))/max(Fe,1e-9)
    res[K] = (Fe, Pe)
    print(f'K={K}: F_eq={Fe:.3f} (F/K {Fe/K:.3f}) P/K {Pe/K:.2f} P_eq={Pe:.2f} settle(F within 5%)={settle} seasons, '
          f'late swing {100*amp:.1f}%, F at t=0 0.200, t=40 {Fs[40]:.3f}, fresh effort x1.5 = {effort(Pe, Fe):.2f}')
# computed scale: k such that fresh effort on 'median' land = 0.5, for each candidate median K
for Km in (1.0, 2.0, 3.0):
    lo, hi = 0.1, 10.0
    for _ in range(60):
        mid = (lo+hi)/2
        (lo, hi) = (mid, hi) if effort(*res[Km][::-1], k=mid) > 0.5 else (lo, mid)
    k = (lo+hi)/2
    print(f'median K={Km}: computed scale k={k:.2f} (x1.5 base) -> fresh effort ' +
          ' '.join(f'K{K}:{effort(res[K][1], res[K][0], k):.2f}' for K in res))
