# Q14 probe: q13run.py plus a 'fixture' scenario (hand-built 3-band map: migrant M with a free refuge in reach,
# cut-off D whose only reachable land is host H's patch outside the drought). args as q13run; fixture takes
# an optional 5th arg 'hx,hy' for the host patch centre. mag 0 = no-drought control (same history to burn). Throwaway; never port.
# so emitter variants (q12emit.py) can be applied offline to the same stream.
# args: scenario(map|island) seed magnitude out.pkl
# Throwaway; never port. Lifecycle copied from run5_q10.step with host and daughter recorded.
import sys, pickle, numpy as np, sysproto_q10 as S, run5_q10 as R, variants
from q9b_modes import MODES
scen, seed, mag, out = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
S.configure(*MODES['C']); S.HMODE = 'short'
R.EXCL, R.HOST_GUARD, S.EFF = 5, True, (0.5, 0.0); S.gMaxW *= 1.5; S.hMaxW *= 1.5; S.maxHunt = 0.01
variants.apply('share', S, R); S.MIN_VIABLE = 5
if scen == 'fixture2': S.H = 48
yy, xx = np.mgrid[0:S.H, 0:S.W]
if scen == 'map':
    K = np.full((S.H, S.W), 2.0); K[:, 50:] = 0.3; burn = 4800; dur = 8
    w = S.World(K, seed); w.bands = [S.Band('A', (12, 12), 25), S.Band('B', (36, 12), 25)]
    cx, cy, r = 18, 12, 20
elif scen == 'fixture':
    hx, hy = map(int, (sys.argv[5] if len(sys.argv) > 5 else '24,20').split(','))
    K = np.full((S.H, S.W), 0.06)
    for (px, py, pr) in ((12, 6, 5), (25, 6, 5), (12, 18, 4), (hx, hy, 4)):
        K[np.sqrt((xx-px)**2+(yy-py)**2) <= pr] = 2.0
    burn = 800; dur = 8
    w = S.World(K, seed); w.bands = [S.Band('M', (12, 6), 25), S.Band('D', (12, 18), 25), S.Band('H', (hx, hy), 25)]
    cx, cy, r = 12, 12, 14
elif scen == 'fixture2':   # 64x48, patches r7: M and D in the drought core; refuge R reachable only by M, host H's patch only by D
    K = np.full((S.H, S.W), 0.06)
    for (px, py) in ((12, 14), (30, 10), (12, 34), (30, 40)):
        K[np.sqrt((xx-px)**2+(yy-py)**2) <= 7] = 2.0
    burn = 800; dur = 8
    w = S.World(K, seed); w.bands = [S.Band('M', (12, 14), 25), S.Band('D', (12, 34), 25), S.Band('H', (30, 40), 25)]
    cx, cy, r = 12, 24, 22
else:
    K = np.full((S.H, S.W), 0.06); K[np.sqrt((xx-16)**2+(yy-12)**2) <= 10] = 2.0; burn = 800; dur = 12
    w = S.World(K, seed); w.bands = [S.Band('A', (16, 12), 25)]
    cx, cy, r = 16, 12, 24
rich = (K > 1.0).sum()
dist = np.sqrt((xx-cx)**2+(yy-cy)**2); strength = np.where(dist <= r/2, 1.0, np.where(dist < r, 2*(1-dist/r), 0.0))
def anom(t): return -mag*strength if burn <= t < burn+dur else 0.0

def comp_share(b):
    Lb = b.lab(); tot = Lb; x, y = b.camp
    for o in w.bands:
        if o is b or not o.alive: continue
        d = np.hypot(o.camp[0]-x, o.camp[1]-y)
        if d < 2*S.R_CATCH: tot += o.lab()*(1 - d/(2*S.R_CATCH))
    return Lb/tot if tot > 0 else 0.0

def catch_ratio(b, a):
    # plant stock / plant capacity over the camp catchment; herd stock / start-of-run herd level (0.2/cell)
    x0, y0 = b.camp; ps = pc = fs = n = 0.0
    capP = S.pFrac*w.Kveg*S.mf(a if np.ndim(a) else np.zeros_like(w.Kveg))
    for dx, dy in S.DISC:
        x, y = x0+dx, y0+dy
        if 0 <= x < S.W and 0 <= y < S.H:
            ps += w.P[y, x]; pc += capP[y, x]; fs += w.F[y, x]; n += 1
    pb = sum(S.pFrac*w.Kveg[y0+dy, x0+dx] for dx, dy in S.DISC if 0 <= x0+dx < S.W and 0 <= y0+dy < S.H)
    return ps/max(pc, 1e-9), fs/n/0.2, ps/max(pb, 1e-9)   # third: stock vs base (no-drought) capacity

rows, world, dens = [], [], []
T = burn + 240
for t in range(T):
    a = anom(t)
    if t == burn: world.append((t, 'drought_began'))
    if t == burn+dur: world.append((t, 'drought_ended'))
    homes = {b.name: b.home for b in w.bands}; alive0 = {b.name: b.alive for b in w.bands}
    pops0 = {b.name: b.br.sum() for b in w.bands}
    S.season(w, t, a, None)
    act = {}
    for b in list(w.bands):
        if not alive0[b.name]: continue
        if not b.alive: act[b.name] = ('perished',); continue
        if b.home != homes[b.name]: act[b.name] = ('migrated', homes[b.name], b.home)
        if b.hungry >= R.DISSOLVE_AFTER:
            hosts = [o for o in w.bands if o is not b and o.alive and o.hungry == 0 and
                     (o.home[0]-b.home[0])**2+(o.home[1]-b.home[1])**2 <= R.HOST_RANGE**2 and R.can_host(w, o, b)]
            if hosts:
                h = min(hosts, key=lambda o: ((o.home[0]-b.home[0])**2+(o.home[1]-b.home[1])**2, o.name))
                h.br = h.br + b.br; b.br = b.br*0; b.alive = False; act[b.name] = ('dissolved', h.name); continue
        if b.br.sum() > R.FISSION_AT and b.hungry == 0:
            half0 = np.floor(b.br/2); dL = float(half0 @ S.LAB); dC = float(half0 @ S.NEED)
            sP, cnt = S.disc_sum(w.P, S.DISC); sF, _ = S.disc_sum(w.F, S.DISC); best = None
            for dy in range(-S.SEARCH, S.SEARCH+1):
                for dx in range(-S.SEARCH, S.SEARCH+1):
                    x, y = b.home[0]+dx, b.home[1]+dy
                    if 0 <= x < S.W and 0 <= y < S.H and w.Kveg[y, x] > 0.05 and R.far(w, None, x, y):
                        n = cnt[y, x]; m, p = S.yield_at(sP[y, x]/n, sF[y, x]/n, dL, 9e9, n)
                        if best is None or m+p > best[0]+1e-12: best = (m+p, x, y)
            if best and best[0] >= dC*(1+R.FISSION_MARGIN):
                nb = S.Band(b.name+'.'+str(len(w.bands)), (best[1], best[2]), 0)
                half = np.floor(b.br/2); nb.br = half; b.br = b.br-half; w.bands.append(nb)
                act[b.name] = act.get(b.name, ()) + ('split', nb.name)
    # per-band facts after lifecycle (only bands alive at season start, plus newborn daughters)
    for b in w.bands:
        if b.name not in alive0:   # daughter founded this season
            rows.append(dict(t=t, band=b.name, born=True, pop=float(b.br.sum())))
            continue
        if not alive0[b.name]: continue
        lg = b.log[-1] if b.log and b.log[-1][0] == t else None
        if lg is None: continue
        ins = float(strength[b.camp[1], b.camp[0]]) if burn <= t < burn+dur else 0.0
        pr, fr, pbase = catch_ratio(b, a)
        rows.append(dict(t=t, band=b.name, pop=float(lg[1]), pop0=float(pops0[b.name]), bal=float(lg[2]),
                         hs=int(lg[3]), hungry=int(b.hungry), stash=float(b.stash), short=float(getattr(b, 'short', 0)),
                         eff=float(getattr(b, "eff", 0)), cons=float(b.cons()) if b.alive else 0.0, camp=b.camp, home=b.home, indrought=ins,
                         share=comp_share(b) if b.alive else 0.0, pratio=pr, pbase=pbase, fratio=fr, act=act.get(b.name, ())))
    if t % 400 == 399:
        dens.append(sum(b.br.sum() for b in w.bands if b.alive)/rich)
pickle.dump(dict(scen=scen, seed=seed, mag=mag, burn=burn, dur=dur, rows=rows, world=world, dens=dens,
                 nbands=sum(b.alive for b in w.bands)), open(out, 'wb'))
print(scen, seed, mag, 'density/century', ' '.join(f'{d:.2f}' for d in dens), 'alive', sum(b.alive for b in w.bands), flush=True)
