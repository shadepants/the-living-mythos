exec(open("q7b.py").read().split("for md in")[0])
import itertools
def metrics(p, K=2.0):
    o = run(K, p, drought=(400, 8), seasons=520)
    bF, bV = o[399][2], o[399][1]
    if bF < 1e-3: return None
    Fs = [o[t][2]/bF for t in range(400, 470)]
    mn = min(Fs); tmin = Fs.index(mn)
    # lag: first season after onset where F falls >5% in one season
    lag = next((i for i in range(1, 30) if Fs[i] < Fs[i-1]*0.95), None)
    rec = next((t-408 for t in range(408, 520) if o[t][2] >= 0.9*bF), 999)
    tail = [r[2] for r in run(K, p, seasons=1200)[-200:]]
    return mn, tmin, lag, rec, max(tail)-min(tail)
hits = []
for rMax, cBreed, cStarve, mStarve, mDens, condRate in itertools.product(
        (0.05, 0.06), (0.2, 0.35), (0.6, 0.7), (0.3, 0.5), (0.03, 0.05), (0.5, 0.8)):
    p = dict(q.P, rMax=rMax, cBreed=cBreed, cStarve=cStarve, mStarve=mStarve, mDens=mDens, condRate=condRate, mBase=0.01)
    m = metrics(p)
    if not m: continue
    mn, tmin, lag, rec, osc = m
    if 0.25 <= 1-mn <= 0.75 and lag and 1 <= lag <= 3 and 12 <= rec <= 28 and osc < 0.01:
        hits.append((round(1-mn,2), lag, rec, rMax, cBreed, cStarve, mStarve, mDens, condRate))
print(len(hits), "of 128 settings meet all targets (crash 25-75%, mortality lag 1-3 seasons, recovery 12-28 seasons, no self-oscillation at K=2)")
for h in hits[:5]: print("crash", h[0], "lag", h[1], "rec", h[2], "| rMax cBreed cStarve mStarve mDens condRate =", h[3:])
# check osc robustness of first hit at richer cells
if hits:
    h = hits[0]; p = dict(q.P, rMax=h[3], cBreed=h[4], cStarve=h[5], mStarve=h[6], mDens=h[7], condRate=h[8], mBase=0.01)
    for K in (1.0, 4.0, 8.0):
        tail = [r[2] for r in run(K, p, seasons=1500)[-200:]]
        print(f"  K{K}: F range {min(tail):.3f}-{max(tail):.3f}")
