# Same as run3 but game scarce relative to people (meatConv 40), so hunting pressure binds.
import run3, sysproto_dep as S
S.meatConv = 40.0
for cap,psi in ((0.01,0.0),(0.05,0.0),(0.2,0.0),(0.2,2.0),(0.2,6.0)):
    print(f"cap {cap} psi {psi}: " + " || ".join(run3.run(s,cap,psi) for s in (1,2)))
