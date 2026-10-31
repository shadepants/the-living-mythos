import importlib.util, sys
spec = importlib.util.spec_from_file_location("q7", "q7.py"); q = importlib.util.module_from_spec(spec)
src = open("q7.py").read().split("# 1)")[0]; exec(src, q.__dict__)
# Mitigation: density-dependent mortality (stand-in for predators/disease/crowding), mDens * F per season
def season2(V, F, c, Kveg, anom, p):
    K = Kveg*q.mf(anom)
    V = V + p['rV']*V*(1-V/K) if V <= K else K + (V-K)*(1-p['dieBack'])
    h = 1/p['n']
    for _ in range(p['n']):
        if F <= 0: break
        demand = F*p['gMax']*V/(V+p['halfSat'])*h
        rem = min(demand, p['maxGraze']*h*V)
        sat = min(1.0, rem/(F*p['need']*h))
        c += p['condRate']*h*(sat-c)
        births = p['rMax']*max(0,(c-p['cBreed'])/(1-p['cBreed']))*F*h
        deaths = (p['mBase'] + p['mDens']*F + p['mStarve']*max(0,(p['cStarve']-c)/p['cStarve']))*F*h
        F += births - deaths; V -= rem
    return max(V,0), max(F,0), c
def run(Kveg, p, drought=None, seasons=1200, F0=0.1):
    V, F, c = Kveg, F0, 0.8; o=[]
    for t in range(seasons):
        a = -0.9 if drought and drought[0] <= t < drought[0]+drought[1] else 0.0
        V, F, c = season2(V, F, c, Kveg, a, p); o.append((t,V,F,c))
    return o
for md in (0.0, 0.05, 0.1, 0.2):
    p = dict(q.P, mDens=md)
    row = []
    for K in (1.0, 2.0, 4.0):
        tail = [r[2] for r in run(K, p)[-200:]]
        row.append(f"K{K}: {min(tail):.2f}-{max(tail):.2f}")
    print(f"mDens {md}: " + "  ".join(row))
# Drought response with the stabilised model: Kveg 2 (mid-rich), severe drought 8 seasons at t=400
p = dict(q.P, mDens=0.1)
o = run(2.0, p, drought=(400, 8), seasons=500)
base_V, base_F = o[399][1], o[399][2]
print("\nseason  V/base  F/base  cond")
for t in list(range(398, 412)) + [415, 420, 430, 440, 460, 480]:
    print(f"{t-400:+4d}  {o[t][1]/base_V:6.2f}  {o[t][2]/base_F:6.2f}  {o[t][3]:.2f}")
rec = next(t for t in range(408, 500) if o[t][2] >= 0.9*base_F)
vrec = next(t for t in range(408, 500) if o[t][1] >= 0.9*base_V)
print(f"veg back to 90% {vrec-408} seasons after drought ends; fauna back to 90% {rec-408} seasons")
