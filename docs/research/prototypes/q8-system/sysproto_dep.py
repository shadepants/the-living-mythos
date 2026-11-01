# Throwaway integrated prototype for the whole-system review (spec Q8 rethink).
# Floats + numpy RNG; never port to sim-core. Models: rev 21 vegetation, rev 22 fauna
# with diffusion, an edible-plant guild, rank-and-cap foraging, a home range with a
# per-season camp choice (marginal-value style), migration, simple demography, die-out.
import numpy as np

W, H = 48, 24
R_CATCH, R_HOME = 3, 5
SEARCH, MARGIN, MIGRATE_AFTER, MIN_VIABLE = 14, 0.2, 2, 5
# vegetation / fauna (rev 21, rev 22 prototype units)
rV, dieBack = 0.7, 0.5
FP = dict(gMax=1.0, halfSat=0.3, need=1.0, maxGraze=0.5, condRate=0.6, rMax=0.06, cBreed=0.5,
          mBase=0.02, mDens=0.1, mStarve=0.25, cStarve=0.4, D=0.1, roam=2.0, n=4)
# plant-food guild (food units = adult person-seasons)
pFrac, rP = 1.8, 0.8
# foraging
hMaxW, hF, maxHunt, meatConv = 3.5, 0.10, 0.01, 300.0
gMaxW, hP = 1.8, 1.5
LAB = np.array([0.25, 0.75, 1.0, 0.5]); NEED = np.array([0.6, 1.0, 1.0, 0.8])
STASH_SEASONS, SPOIL, STARVING_AFTER = 0.5, 0.25, 2
# demography (per season)
BASE_M = np.array([0.0093, 0.003, 0.004, 0.02])
HUNG_M = np.array([0.02, 0.01, 0.01, 0.02]); STARVE_M = np.array([0.10, 0.05, 0.05, 0.10])
B_RATE = 0.045; FERT = {0: 1.0, 1: 0.5, 2: 0.1}
AGE_UP = np.array([1/60, 1/40, 1/100, 0.0])

def disc(r):
    return [(dx, dy) for dy in range(-r, r+1) for dx in range(-r, r+1) if dx*dx+dy*dy <= r*r]
DISC, HOME = disc(R_CATCH), disc(R_HOME)

def disc_sum(A, offs):
    out = np.zeros_like(A); cnt = np.zeros_like(A)
    for dx, dy in offs:
        sh = np.zeros_like(A); m = np.zeros_like(A)
        ys0, ys1 = max(0, -dy), min(H, H-dy); xs0, xs1 = max(0, -dx), min(W, W-dx)
        sh[ys0:ys1, xs0:xs1] = A[ys0+dy:ys1+dy, xs0+dx:xs1+dx]; m[ys0:ys1, xs0:xs1] = 1
        out += sh; cnt += m
    return out, cnt

def mf(a): return np.clip(1 + 0.8*a, 0.2, 1.2)

class World:
    def __init__(s, Kveg, seed=1):
        s.Kveg = Kveg; s.V = Kveg*0.83; s.F = np.full((H, W), 0.2)*(Kveg > 0.5); s.c = np.full((H, W), 0.85)
        s.P = pFrac*s.V; s.rng = np.random.default_rng(seed); s.bands = []
    def step_fields(s, anom):
        K = s.Kveg*mf(anom); V = s.V
        s.V = np.where(V <= K, V + rV*V*(1-V/np.maximum(K, 1e-9)), K + (V-K)*(1-dieBack))
        p = FP; h = 1/p['n']
        for _ in range(p['n']):
            F, V, c = s.F, s.V, s.c
            dem = F*p['gMax']*V/(V+p['halfSat'])*h; rem = np.minimum(dem, p['maxGraze']*h*V)
            sat = np.where(F > 1e-12, np.minimum(1, rem/np.maximum(F*p['need']*h, 1e-12)), 1.0)
            c = c + p['condRate']*h*(sat-c)
            b = p['rMax']*np.maximum(0, (c-p['cBreed'])/(1-p['cBreed']))*F*h
            d = (p['mBase'] + p['mDens']*F + p['mStarve']*np.maximum(0, (p['cStarve']-c)/p['cStarve']))*F*h
            F = np.maximum(0, F+b-d); V = np.maximum(0, V-rem)
            Dc = p['D']*(1 + p['roam']*(1-c))
            Fp = np.pad(F, 1, mode='edge'); lap = Fp[:-2, 1:-1]+Fp[2:, 1:-1]+Fp[1:-1, :-2]+Fp[1:-1, 2:]-4*F
            s.F, s.V, s.c = np.maximum(0, F + h*Dc*lap), V, c
        cap = pFrac*s.V; P = s.P
        s.P = np.where(P <= cap, P + rP*P*(1-P/np.maximum(cap, 1e-9)), cap + (P-cap)*(1-dieBack)) + 0.01

def yield_at(Pm, Fm, L, target, ncell):
    """Rank-and-cap: hunt first (Type II, capped), leftover labour gathers; satisfice at target."""
    rH = hMaxW*Fm/(Fm+hF); rG = gMaxW*Pm/(Pm+hP)
    meat = min(L*rH, maxHunt*Fm*ncell*meatConv, target)
    used = meat/rH if rH > 0 else 0.0
    plant = min(max(0, L-used)*rG, target-meat, Pm*ncell*0.5)
    return meat, plant

class Band:
    def __init__(s, name, home, n):
        s.name, s.home, s.camp = name, home, home
        s.br = np.array([8, 4, 9, 4], float)*n/25; s.br = np.round(s.br); s.carry = np.zeros(4)
        s.stash = 0.0; s.hungry = 0; s.alive = True; s.log = []; s.moves = 0; s.migr = []
    def cons(s): return float(s.br @ NEED)
    def lab(s): return float(s.br @ LAB)

PSI, DIST_DECAY = 0.0, 0.5
def season(w, t, anom, recs):
    w.step_fields(anom)
    if not hasattr(w, 'Dist'): w.Dist = np.zeros_like(w.F)
    w.Dist *= DIST_DECAY
    Fe = w.F/(1+PSI*w.Dist)
    sP, cnt = disc_sum(w.P, DISC); sF, _ = disc_sum(Fe, DISC)
    land = w.Kveg > 0.05
    for b in w.bands:
        if not b.alive: continue
        L, C = b.lab(), b.cons(); target = C + max(0, STASH_SEASONS*C - b.stash)
        def score(x, y):
            n = cnt[y, x]; m, p = yield_at(sP[y, x]/n, sF[y, x]/n, L, 9e9, n); return m+p
        # camp choice inside home range: best expected return (marginal-value style)
        hx, hy = b.home; best = None
        for dx, dy in HOME:
            x, y = hx+dx, hy+dy
            if 0 <= x < W and 0 <= y < H and land[y, x]:
                sc = score(x, y)
                if best is None or sc > best[0] + 1e-12: best = (sc, x, y)
        if (best[1], best[2]) != b.camp: b.moves += 1
        b.camp = (best[1], best[2]); cx, cy = b.camp; n = cnt[cy, cx]
        meat, plant = yield_at(sP[cy, cx]/n, sF[cy, cx]/n, L, target, n)
        for dx, dy in DISC:
            x, y = cx+dx, cy+dy
            if 0 <= x < W and 0 <= y < H:
                w.P[y, x] = max(0, w.P[y, x] - plant/n); w.F[y, x] = max(0, w.F[y, x] - meat/meatConv/n)
                rH_ = hMaxW*(sF[cy,cx]/n)/((sF[cy,cx]/n)+hF); w.Dist[y, x] += (meat/rH_ if rH_>0 else 0)/n
        y_ = meat+plant; bal = y_ - C
        b.stash = max(0, min(STASH_SEASONS*C, (b.stash+bal)*(1-SPOIL)))
        b.hungry = b.hungry+1 if (b.stash == 0 and bal < 0) else 0
        hs = 0 if b.hungry == 0 else (1 if b.hungry < STARVING_AFTER else 2)
        # demography: binomial per bracket (start-of-season counts)
        q = np.clip(BASE_M + (HUNG_M if hs == 1 else STARVE_M if hs == 2 else 0), 0, 1)
        deaths = w.rng.binomial(b.br.astype(int), q)
        births = w.rng.binomial(int(round((b.br[1]+b.br[2])/2)), B_RATE*FERT[hs])
        up = b.br*AGE_UP + b.carry; moved = np.floor(up); b.carry = up-moved
        b.br = b.br - deaths - moved + np.roll(moved, 1)*np.array([0, 1, 1, 1]); b.br[0] += births
        b.br = np.maximum(b.br, 0)
        # migration: shift the home range when hunger persists and a better range exists
        if b.hungry >= MIGRATE_AFTER:
            cur = best[0]; cand = None
            for dy in range(-SEARCH, SEARCH+1):
                for dx in range(-SEARCH, SEARCH+1):
                    x, y = hx+dx, hy+dy
                    if dx*dx+dy*dy <= SEARCH*SEARCH and 0 <= x < W and 0 <= y < H and land[y, x]:
                        sc = score(x, y) - 0.05*np.sqrt(dx*dx+dy*dy)
                        if cand is None or sc > cand[0] + 1e-12: cand = (sc, x, y)
            if cand and cand[0] > cur*(1+MARGIN):
                b.migr.append((t, b.home, (cand[1], cand[2]))); b.home = (cand[1], cand[2]); b.camp = b.home
        pop = b.br.sum()
        b.log.append((t, pop, bal/C, hs, meat/(y_ or 1)))
        if pop < MIN_VIABLE: b.alive = False; b.died = t
