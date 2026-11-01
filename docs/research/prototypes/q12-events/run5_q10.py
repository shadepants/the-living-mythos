# Copy of research/prototypes/q8-system/run5.py (R3 lifecycle), used as a library by r4probe.py.
import numpy as np, sys
import sysproto_q10 as S
S.W = 64
FISSION_AT, EXCL, HOST_RANGE, DISSOLVE_AFTER = 50, 2*S.R_HOME, 15, 3
FISSION_GUARD, FISSION_MARGIN = True, 0.2
HOST_GUARD = False
NO_REVERT = False  # R4 probe: host accepts only if its camp can feed host + refugees x 1.2
def can_host(w, o, b):
    sP, cnt = S.disc_sum(w.P, S.DISC); sF, _ = S.disc_sum(w.F, S.DISC); x, y = o.camp; n = cnt[y, x]
    L = o.lab() + b.lab(); C = o.cons() + b.cons(); m, p = S.yield_at(sP[y, x]/n, sF[y, x]/n, L, 9e9, n)
    return m + p >= C*(1+FISSION_MARGIN)
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
            if life >= 1 and not NO_REVERT and not far(w, b, *b.home):
                b.home = b.camp = homes[id(b)]; b.migr.pop(); S.DIAG.append((t, b.name, 'reverted', 0, 0))
            else: ev.append((t, 'migrated', b.name))
        if life >= 2 and b.hungry >= DISSOLVE_AFTER:
            hosts = [o for o in w.bands if o is not b and o.alive and o.hungry == 0 and
                     (o.home[0]-b.home[0])**2+(o.home[1]-b.home[1])**2 <= HOST_RANGE**2 and (not HOST_GUARD or can_host(w, o, b))]
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
