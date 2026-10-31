import sys, numpy as np
import sysproto as S
S.W = 64
def build(seed):
    K = np.full((S.H, S.W), 2.0); K[:, 50:] = 0.3
    w = S.World(K, seed); w.bands = [S.Band('A', (20, 12), 25), S.Band('B', (44, 12), 25)]
    return w
def anom_field(t, t0, dur, mag, cx=32, cy=12, r=24):
    yy, xx = np.mgrid[0:S.H, 0:S.W]; d = np.sqrt((xx-cx)**2 + (yy-cy)**2)
    st = np.where(d <= r/2, 1.0, np.where(d < r, 2*(1-d/r), 0.0))
    return -mag*st if t0 <= t < t0+dur else 0.0*st
def run(seed, dur=8, mag=0.9, burn=400, after=200):
    w = build(seed)
    for t in range(burn+after): S.season(w, t, anom_field(t, burn, dur, mag), None)
    return w
def summary(w, burn=400, dur=8):
    out = []
    for b in w.bands:
        pre = [r for r in b.log if 200 <= r[0] < burn]
        hp = sum(1 for r in pre if r[3] > 0); pop0 = pre[-1][1] if pre else None
        post = [r for r in b.log if r[0] >= burn]
        hpost = sum(1 for r in post if r[3] > 0); mn = min((r[1] for r in post), default=None)
        meat = np.mean([r[4] for r in pre]) if pre else 0
        mig = [m[0]-burn for m in b.migr if m[0] >= burn]; migpre = sum(1 for m in b.migr if m[0] < burn)
        died = getattr(b, 'died', None)
        out.append(f"{b.name}: pop@burn {pop0:.0f} meat {meat:.2f} hungry_pre {hp} migr_pre {migpre} | hungry_post {hpost} minpop {mn:.0f} migrated {mig[:3]} died {None if died is None else died-burn}")
    return " || ".join(out)
if __name__ == '__main__':
    for dur in (8, 16):
        print(f"severe drought, {dur} seasons")
        for seed in range(1, 6): print(f" seed {seed}: " + summary(run(seed, dur), dur=dur))
