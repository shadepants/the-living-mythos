exec(open('band.py').read().split("for dr in")[0])
import itertools
def setp(**k): globals().update(k)
print("sweep: maxHunt, gE  -> per model: F ratio pre | hungry_pre | drought(-0.9,8): firstNeg, hungry, longest, tail")
for mh, g in itertools.product((0.01,0.02,0.03),(2.6,3.2,3.8)):
    setp(maxHunt=mh, gE=g)
    row=[]
    for m in "BC":
        r=run(m); pre=r[400:600]; t0=600
        Fr=sum(x[2] for x in pre)/200/0.227; hp=sum(x[5] for x in pre)
        hung=[x for x in r[t0:] if x[5]]; neg=next((x[0]-t0 for x in r[t0:] if x[4]<0),None)
        b=cur=0
        for x in r[t0:]: cur=cur+1 if x[5] else 0; b=max(b,cur)
        lh=max((x[0] for x in hung),default=None); tail=(lh-607) if lh else None
        ms=sum(x[6] for x in pre)/200
        row.append(f"{m} F{Fr:.2f} m{ms:.2f} hp{hp} neg{neg} h{len(hung)} L{b} t{tail}")
    print(f"mh={mh} gE={g}: "+" | ".join(row))
