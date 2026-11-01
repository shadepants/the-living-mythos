# Event trace for one L2 run, to see whether dissolutions churn with fissions.
import run5, numpy as np, sysproto_r3 as S
K = np.full((S.H, S.W), 2.0); K[:, 50:] = 0.3
w = S.World(K, 2); w.bands = [S.Band('A', (12, 12), 25), S.Band('B', (36, 12), 25)]; ev = []
for t in range(680): run5.step(w, t, run5.drought(t, 600, 8), 2, ev)
post = [e for e in ev if e[0] >= 600]
print(len(post), "events after onset; by type:", {k: sum(1 for e in post if e[1]==k) for k in ('fission','dissolved','migrated','died')})
for e in post[:24]: print(e[0]-600, e[1], e[2])
alive = [b for b in w.bands if b.alive]; print("homes x of alive:", sorted(b.home[0] for b in alive))
