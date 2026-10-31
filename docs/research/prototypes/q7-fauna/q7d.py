exec(open("q7c.py").read().split("hits = []")[0])
import collections
rows=[]
for rMax, cBreed, cStarve, mStarve, mDens, condRate in itertools.product(
        (0.05, 0.06), (0.2, 0.35), (0.6, 0.7), (0.3, 0.5), (0.03, 0.05), (0.5, 0.8)):
    p = dict(q.P, rMax=rMax, cBreed=cBreed, cStarve=cStarve, mStarve=mStarve, mDens=mDens, condRate=condRate, mBase=0.01)
    m = metrics(p)
    if m: rows.append(m)
print(len(rows), "viable settings")
import statistics as s
for i,name in enumerate(["min F/base","season of min","lag","recovery","osc"]):
    v=[r[i] for r in rows if r[i] is not None]
    print(f"{name}: min {min(v):.2f} median {s.median(v):.2f} max {max(v):.2f}")
