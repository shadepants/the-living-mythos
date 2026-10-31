# Throwaway prototype of spec Q7 option C (+ rev 21 vegetation). Not sim code.
import math
P = dict(rV=0.7, dieBack=0.5, gMax=1.0, halfSat=0.3, need=1.0, maxGraze=0.5,
         condRate=0.6, rMax=0.06, cBreed=0.5, mBase=0.02, mStarve=0.25, cStarve=0.4, n=4)
def mf(anom):  # moisture factor: 1 at 0, linear down to floor 0.2 at anom -1
    return max(0.2, min(1.2, 1 + 0.8*anom))
def season(V, F, c, Kveg, anom, p=P):
    K = Kveg*mf(anom)
    V = V + p['rV']*V*(1-V/K) if V <= K else K + (V-K)*(1-p['dieBack'])
    h = 1/p['n']
    for _ in range(p['n']):
        if F <= 0: break
        demand = F*p['gMax']*V/(V+p['halfSat'])*h
        rem = min(demand, p['maxGraze']*h*V)
        sat = min(1.0, rem/(F*p['need']*h))
        c += p['condRate']*h*(sat-c)
        births = p['rMax']*max(0,(c-p['cBreed'])/(1-p['cBreed']))*F*h
        deaths = (p['mBase'] + p['mStarve']*max(0,(p['cStarve']-c)/p['cStarve']))*F*h
        F += births - deaths; V -= rem
    return max(V,0), max(F,0), c
def run(Kveg=1.0, drought=None, seasons=400, F0=0.1, p=P):
    V, F, c = Kveg, F0, 0.8; out=[]
    for t in range(seasons):
        a = -0.9 if drought and drought[0] <= t < drought[0]+drought[1] else 0.0
        V, F, c = season(V, F, c, Kveg, a, p); out.append((t, V, F, c))
    return out
# 1) Equilibrium and self-oscillation at several enrichment levels (no drought)
print("Kveg  V_end  F_end  c_end  F range over last 200 seasons (osc check)")
for K in (0.5, 1.0, 2.0, 4.0):
    o = run(Kveg=K, seasons=1200)
    tail = [r[2] for r in o[-200:]]
    print(f"{K:4} {o[-1][1]:.3f} {o[-1][2]:.3f} {o[-1][3]:.3f}  {min(tail):.3f}-{max(tail):.3f}")
