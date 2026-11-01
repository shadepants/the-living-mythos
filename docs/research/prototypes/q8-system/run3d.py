# Fixed-rank (hunt first) with the same strong depression, for comparison with run3c.
import run3, sysproto_dep as S, sys
S.meatConv = 40.0
for psi in map(float, sys.argv[1:]):
    print(f"rank cap 0.2 psi {psi}: " + " || ".join(run3.run(s,0.2,psi) for s in (1,2)))
