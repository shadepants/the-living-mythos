import sys, run5 as R, r4probe as P
R.EXCL = int(sys.argv[1])
for K in [float(k) for k in sys.argv[2:]]:
    r = P.measure(K, 1)
    print(f"EXCL{R.EXCL} K{K}: bands {r['bands']} dens {r['dens']:.2f} size {r['bmin']:.0f}-{r['bmean']:.0f}-{r['bmax']:.0f} meat {r['meat']:.2f} game {r['game']:.2f} hungry {r['hungry']:.3f} {r['ev']}", flush=True)
