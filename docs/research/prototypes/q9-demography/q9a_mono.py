# Q9a probe: is the inverse-CDF draw monotone in q for a fixed u (same seed, worse conditions -> never fewer deaths)?
# Compares the spec's flip (same u) with a flip that uses 1-u.
from q9a_sampler import binom_inv, int_pow
def flip1mu(n, q, u):
    if n <= 0 or q <= 0: return 0
    if q >= 1: return n
    if q > 0.5: return n - binom_inv(n, 1-q, 1-u)
    return binom_inv(n, q, u)
for name, f in (("spec same-u", binom_inv), ("flip 1-u", flip1mu)):
    bad = 0; tot = 0
    for n in (5, 25, 60):
        for i in range(2000):
            u = (i+0.5)/2000; prev = -1
            for j in range(1, 200):
                k = f(n, j/200, u); tot += 1
                if k < prev: bad += 1
                prev = k
    print(f"{name}: monotonicity violations {bad} of {tot}")
