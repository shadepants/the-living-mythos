# R4 probe 2: home-range spacing (EXCL) vs density and band size. Uniform K, no drought.
import sys, run5 as R, r4probe as P
R.EXCL = int(sys.argv[1])
for K in (1.0, 2.0, 4.0):
    for s in (1, 2):
        r = P.measure(K, s)
        print(f"EXCL{R.EXCL} K{K} s{s}: bands {r['bands']} dens {r['dens']:.2f} size {r['bmin']:.0f}-{r['bmean']:.0f}-{r['bmax']:.0f} meat {r['meat']:.2f} game {r['game']:.2f} hungry {r['hungry']:.3f} {r['ev']}", flush=True)
