# Throwaway Q8 prototype: three yield models on a lumped 29-cell catchment. Floats; never port.
import sys; sys.path.insert(0,'.')
from eco import eco, P as EP
N=29; KV=2.0
CONS = 8*0.6 + 4*1 + 9*1 + 4*0.8     # 21 food/season (children 0.6, YA 1, adult 1, elder 0.8)
L = 9 + 0.5*4                         # 11 workers
hE, hH = 4.0, 0.15   # per-hunter return hE*F/(F+hH): ~2.4 at unhunted F=0.227
gE, hV = 2.6, 0.8    # per-gatherer return gE*V/(V+hV): ~1.76 at V=1.67
meatConv, plantConv = 50.0, 10.0
maxHunt = 0.05       # max fraction of herd taken per season
stashCap, spoil = 0.5*CONS, 0.25

def forage(model, V, F, stash):
    rH = hE*F/(F+hH); rG = gE*V/(V+hV)
    if model=='A':   # spec v0.8 text: every worker does both, linear in V and F
        meat = L*0.6*F*meatConv*0.3; plant = L*0.6*V*plantConv*0.1   # scaled to match baseline
    elif model=='B': # fixed half split, Type II, use all labour
        meat = min(0.5*L*rH, maxHunt*F*N*meatConv); plant = 0.5*L*rG
    else:            # C: rank-and-cap + satisfice
        target = CONS + max(0, stashCap - stash)
        meat = min(L*rH, maxHunt*F*N*meatConv, target)
        used = meat/rH if rH>0 else 0
        plant = min((L-used)*rG, target-meat)
    return meat, plant

def run(model, drought=(-0.9,8), t0=600, T=760, quiet=False):
    V=[1.666]; F=[0.227]; c=0.856; stash=stashCap
    V,F=1.666,0.227; rec=[]
    for t in range(T):
        a = drought[0] if t0<=t<t0+drought[1] else 0.0
        V,F,c = eco(V,F,c,KV,a)
        meat,plant = forage(model,V,F,stash)
        V = max(0, V - plant/plantConv/N); F = max(0, F - meat/meatConv/N)
        y = meat+plant; bal = y-CONS
        stash = max(0, min(stashCap, (stash+bal)*(1-spoil)))
        hungry = stash==0 and bal<0
        rec.append((t,V,F,y,bal,hungry,meat/(y or 1)))
    return rec

def report(model, drought=(-0.9,8)):
    r=run(model,drought); t0=600; d=drought[1]
    pre=r[400:600]
    Fpre=sum(x[2] for x in pre)/200
    osc = max(x[2] for x in pre)-min(x[2] for x in pre)
    hpre=sum(x[5] for x in pre)
    neg = next((x[0]-t0 for x in r[t0:] if x[4]<0), None)
    hung=[x for x in r[t0:] if x[5]]
    run_=best=0
    for x in r[t0:]:
        run_ = run_+1 if x[5] else 0; best=max(best,run_)
    lasth = max((x[0] for x in hung), default=None)
    tail = (lasth - (t0+d) + 1) if lasth is not None else None
    ms = lambda s: sum(x[6] for x in s)/len(s)
    print(f"{model}: F/0.227={Fpre/0.227:.2f} osc={osc:.3f} hungry_pre={hpre} | firstNeg+{neg} hungry={len(hung)} longest={best} tailAfterEnd={tail} | meat share pre {ms(pre):.2f} during {ms(r[t0:t0+d]):.2f} after {ms(r[t0+d:t0+d+20]):.2f}")
for dr in ((-0.9,8),(-0.45,8)):
    print("drought",dr)
    for m in "ABC": report(m,dr)
