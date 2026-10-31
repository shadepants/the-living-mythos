exec(open('band.py').read().split("for dr in")[0])
import itertools
def stats(m):
    r=run(m); pre=r[400:600]; t0=600
    Fr=sum(x[2] for x in pre)/200/0.227; hp=sum(x[5] for x in pre)
    hung=[x for x in r[t0:] if x[5]]
    b=cur=0
    for x in r[t0:]: cur=cur+1 if x[5] else 0; b=max(b,cur)
    lh=max((x[0] for x in hung),default=None); tail=(lh-607) if lh else None
    ms=sum(x[6] for x in pre)/200; md=sum(x[6] for x in r[600:608])/8; ma=sum(x[6] for x in r[608:628])/20
    # seasons after drought end until F back to 90% of pre
    Fb=sum(x[2] for x in pre)/200
    fr=next((x[0]-608 for x in r[608:] if x[2]>=0.9*Fb),None)
    return f"{m} F{Fr:.2f} meat{ms:.2f}/{md:.2f}/{ma:.2f} hp{hp} hung{len(hung)} longest{b} tail{tail} Frec{fr}"
print("meatConv, maxHunt, gE | meat share pre/during/after(20)")
for mc, mh, g in itertools.product((150,300),(0.01,0.02),(1.8,2.6)):
    globals().update(meatConv=mc, maxHunt=mh, gE=g)
    print(f"mc{mc} mh{mh} gE{g}: "+" || ".join(stats(m) for m in "BC"))
