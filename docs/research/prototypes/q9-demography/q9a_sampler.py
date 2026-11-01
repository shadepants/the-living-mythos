# Q9a probe: spec §10 inverse-CDF binomial (basic arithmetic only) vs the exact pmf.
# Checks edge cases, total-variation distance on a 2^16-point uniform grid, and loop length.
from fractions import Fraction
from math import comb

def int_pow(x, n):
    r = 1.0
    for _ in range(n): r *= x
    return r

def binom_inv(n, q, u):
    if n <= 0 or q <= 0: return 0
    if q >= 1: return n
    if q > 0.5: return n - binom_inv(n, 1 - q, u)
    p = int_pow(1 - q, n); cum = p; k = 0; steps = 0
    while cum <= u and k < n:
        p = p * (n - k) / (k + 1) * q / (1 - q); k += 1; cum += p; steps += 1
    return k if cum > u else n

def exact(n, q):
    qf = Fraction(q)
    return [float(comb(n, k) * qf**k * (1 - qf)**(n - k)) for k in range(n + 1)]

assert binom_inv(0, 0.3, 0.9) == 0 and binom_inv(10, 0.0, 0.99) == 0 and binom_inv(10, 1.0, 0.0) == 10
worst = 0.0; G = 1 << 16
for n in (1, 2, 5, 12, 25, 40, 60):
    for q in (0.001, 0.0093, 0.05, 0.25, 0.5, 0.75, 0.99):
        h = [0] * (n + 1)
        for i in range(G): h[binom_inv(n, q, (i + 0.5) / G)] += 1
        ex = exact(n, q); tv = 0.5 * sum(abs(h[k] / G - ex[k]) for k in range(n + 1))
        worst = max(worst, tv)
print(f"max total-variation distance vs exact pmf over 49 (n,q) cases: {worst:.2e} (grid resolution 1/{G})")
# u just under 1 must not overrun n; q = 0.5 boundary uses the direct branch
print("u=1-2^-32:", binom_inv(60, 0.3, 1 - 2**-32), "| q=0.5,n=60,u=0.5:", binom_inv(60, 0.5, 0.5))
