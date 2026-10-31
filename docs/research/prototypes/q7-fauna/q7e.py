exec(open("q7c.py").read().split("hits = []")[0])
stable=[]
for rMax, cBreed, cStarve, mStarve, mDens, mBase, condRate in itertools.product(
        (0.04,0.06,0.08), (0.3,0.5), (0.5,0.65), (0.3,0.6), (0.05,0.1,0.2), (0.01,0.02), (0.5,0.8)):
    p = dict(q.P, rMax=rMax, cBreed=cBreed, cStarve=cStarve, mStarve=mStarve, mDens=mDens, mBase=mBase, condRate=condRate)
    m = metrics(p)
    if m and m[4] < 0.01: stable.append((m, (rMax,cBreed,cStarve,mStarve,mDens,mBase,condRate)))
print(len(stable), "stable of 576")
best = sorted(stable, key=lambda x: x[0][3])
for m,pp in best[:4]:
    print(f"crash {1-m[0]:.2f} lag {m[2]} rec {m[3]} | rMax,cBreed,cStarve,mStarve,mDens,mBase,cond={pp}")
strong=[x for x in stable if 1-x[0][0] >= 0.25]
print(len(strong), "stable with crash >= 25%; their recovery range:", min(x[0][3] for x in strong) if strong else None, "-", max(x[0][3] for x in strong) if strong else None)
ok=[x for x in strong if x[0][3]<=28 and x[0][2] and 1<=x[0][2]<=3]
print(len(ok), "also recover in <=28 seasons with lag 1-3")
for m,pp in ok[:3]: print(f"  crash {1-m[0]:.2f} lag {m[2]} rec {m[3]} | {pp}")
