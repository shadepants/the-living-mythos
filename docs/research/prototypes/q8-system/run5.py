# R3: band lifecycle. L0 die-out only (<5); L1 + fission above 50; L2 + dissolution into a non-hungry
# band within HOST_RANGE after DISSOLVE_AFTER hungry seasons. Seasonal camp with 10% move margin (rev 24).
# Local drought over the west half; east half is a refuge. Counts events after burn-in.
import numpy as np, sys
import sysproto_r3 as S
S.W = 64
FISSION_AT, EXCL, HOST_RANGE, DISSOLVE_AFTER = 50, 2*S.R_HOME, 15, 3
FISSION_GUARD, FISSION_MARGIN = False, 0.2
def drought(t, t0, dur, cx=18, cy=12, r=20, mag=0.9):
    if not (t0 <= t < t0+dur): return 0.0
    yy, xx = np.mgrid[0:S.H, 0:S.W]; d = np.sqrt((xx-cx)**2+(yy-cy)**2)
    return -mag*np.where(d <= r/2, 1.0, np.where(d < r, 2*(1-d/r), 0.0))
def far(w, b, x, y):
    return all(o is b or not o.alive or (x-o.home[0])**2+(y-o.home[1])**2 >= EXCL*EXCL for o in w.bands)
def step(w, t, anom, life, ev):
    homes = {id(b): b.home for b in w.bands}; alive0 = {id(b): b.alive for b in w.bands}
    S.season(w, t, anom, None)
    for b in list(w.bands):
        if not alive0[id(b)]: continue
        if not b.alive: ev.append((t, 'died', b.name)); continue
        if b.home != homes[id(b)]:
            if life >= 1 and not far(w, b, *b.home):
                b.home = b.camp = homes[id(b)]; b.migr.pop()
            else: ev.append((t, 'migrated', b.name))
        if life >= 2 and b.hungry >= DISSOLVE_AFTER:
            hosts = [o for o in w.bands if o is not b and o.alive and o.hungry == 0 and
                     (o.home[0]-b.home[0])**2+(o.home[1]-b.home[1])**2 <= HOST_RANGE**2]
            if hosts:
                h = min(hosts, key=lambda o: ((o.home[0]-b.home[0])**2+(o.home[1]-b.home[1])**2, o.name))
                h.br = h.br + b.br; b.br = b.br*0; b.alive = False; ev.append((t, 'dissolved', b.name)); continue
        if life >= 1 and b.br.sum() > FISSION_AT and b.hungry == 0:
            half0 = np.floor(b.br/2); dL = float(half0 @ S.LAB); dC = float(half0 @ S.NEED)
            sP, cnt = S.disc_sum(w.P, S.DISC); sF, _ = S.disc_sum(w.F, S.DISC); best = None
            for dy in range(-S.SEARCH, S.SEARCH+1):
                for dx in range(-S.SEARCH, S.SEARCH+1):
                    x, y = b.home[0]+dx, b.home[1]+dy
                    if 0 <= x < S.W and 0 <= y < S.H and w.Kveg[y, x] > 0.05 and far(w, None, x, y):
                        n = cnt[y, x]; m, p = S.yield_at(sP[y, x]/n, sF[y, x]/n, dL, 9e9, n)
                        if best is None or m+p > best[0]+1e-12: best = (m+p, x, y)
            if best and (not FISSION_GUARD or best[0] >= dC*(1+FISSION_MARGIN)):
                nb = S.Band(b.name+'.'+str(len(w.bands)), (best[1], best[2]), 0)
                half = np.floor(b.br/2); nb.br = half; b.br = b.br-half; w.bands.append(nb); ev.append((t, 'fission', b.name))
def run(life, seed, dur, burn=600, after=80):
    K = np.full((S.H, S.W), 2.0); K[:, 50:] = 0.3
    w = S.World(K, seed); w.bands = [S.Band('A', (12, 12), 25), S.Band('B', (36, 12), 25)]; ev = []
    for t in range(burn+after): step(w, t, drought(t, burn, dur), life, ev)
    pre = [e for e in ev if burn-200 <= e[0] < burn]; post = [e for e in ev if e[0] >= burn]
    c = lambda L, k: sum(1 for e in L if e[1] == k)
    alive = [b for b in w.bands if b.alive]
    return (f"bands {len(alive)} pop {sum(b.br.sum() for b in alive):.0f} | pre200: mig {c(pre,'migrated')} diss {c(pre,'dissolved')} died {c(pre,'died')} | "
            f"drought+20yr: mig {c(post,'migrated')} diss {c(post,'dissolved')} died {c(post,'died')} fission {c(post,'fission')}")
if __name__ == '__main__':
    life, dur = int(sys.argv[1]), int(sys.argv[2])
    FISSION_GUARD = len(sys.argv) > 3
    for seed in (1, 2, 3):
        print(f"L{life} dur{dur} seed{seed}: {run(life, seed, dur)}", flush=True)
