# Q10 migration variants. All share the trigger (hungry streak >= MIGRATE_AFTER) unless noted.
import numpy as np
def apply(var, S, R):
    parts = var.split('+')
    for p in parts:
        if p == 'base': pass
        elif p == 'free': S.MIGRATE = make(S, R, free=True)            # search only free sites (home >= EXCL from others)
        elif p == 'overlap': S.MIGRATE = make(S, R, free=False); R.NO_REVERT = True   # overlap allowed, standing-stock score
        elif p == 'share': S.MIGRATE = make(S, R, free=False, share=True); R.NO_REVERT = True  # overlap allowed, competitor-adjusted score
        elif p == 'sharefree': S.MIGRATE = make(S, R, free=True, share=True)
        elif p.startswith('after'): S.MIGRATE_AFTER = int(p[5:])
        elif p.startswith('rad'): S.SEARCH = int(p[3:])
        elif p.startswith('mar'): S.MARGIN = float(p[3:])
        else: raise SystemExit('unknown variant ' + p)

def make(S, R, free, share=False):
    def comp_share(w, b, x, y):
        # share of the target catchment's stock this band can expect: own labour over own + residents' labour,
        # residents weighted by catchment overlap (linear in camp distance, 0 at 2*R_CATCH). Inferred stand-in.
        Lb = b.lab(); tot = Lb
        for o in w.bands:
            if o is b or not o.alive: continue
            d = np.hypot(o.camp[0]-x, o.camp[1]-y)
            if d < 2*S.R_CATCH: tot += o.lab()*(1 - d/(2*S.R_CATCH))
        return Lb/tot
    def mig(w, b, t, best, score, land, hx, hy):
        if b.hungry < S.MIGRATE_AFTER: return
        sP, cnt = S.disc_sum(w.P, S.DISC); sF, _ = S.disc_sum(w.F, S.DISC); L = b.lab()
        def sc(x, y):
            n = cnt[y, x]; f = comp_share(w, b, x, y) if share else 1.0
            m, p = S.yield_at(sP[y, x]/n*f, sF[y, x]/n*f, L, 9e9, n); return m + p
        cur = max(sc(hx+dx, hy+dy) for dx, dy in S.HOME if 0 <= hx+dx < S.W and 0 <= hy+dy < S.H and land[hy+dy, hx+dx])
        cand = None
        for dy in range(-S.SEARCH, S.SEARCH+1):
            for dx in range(-S.SEARCH, S.SEARCH+1):
                x, y = hx+dx, hy+dy
                if dx*dx+dy*dy <= S.SEARCH**2 and 0 <= x < S.W and 0 <= y < S.H and land[y, x]:
                    if free and not R.far(w, b, x, y): continue
                    v = sc(x, y) - 0.05*np.sqrt(dx*dx+dy*dy)
                    if cand is None or v > cand[0] + 1e-12: cand = (v, x, y)
        ok = cand is not None and cand[0] > cur*(1+S.MARGIN)
        S.DIAG.append((t, b.name, 'move' if ok else ('nosite' if cand is None else 'nomargin'), cur, cand[0] if cand else 0))
        if ok:
            b.migr.append((t, b.home, (cand[1], cand[2]))); b.home = (cand[1], cand[2]); b.camp = b.home
    return mig
