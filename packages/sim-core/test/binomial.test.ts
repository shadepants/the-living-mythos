import { describe, expect, it } from 'vitest';
import { fc, test } from '@fast-check/vitest';
import { binomialWalk, intPow, sampleBinomial } from '../src/binomial.ts';

// Reference pmf, computed independently of the sampler (no flip, no walk).
// Math.pow is allowed here: the ban covers sim-core/src only, and this is the oracle.
const refPmf = (n: number, q: number): number[] => {
  const out: number[] = [];
  let coef = 1; // C(n, k), built incrementally
  for (let k = 0; k <= n; k++) {
    if (k > 0) coef = (coef * (n - k + 1)) / k;
    out.push(coef * Math.pow(q, k) * Math.pow(1 - q, n - k));
  }
  return out;
};

// rand01 yields multiples of 2^-32 in [0, 1); generate the same lattice.
const TWO_POW_32 = 0x100000000;
const uArb = fc.integer({ min: 0, max: TWO_POW_32 - 1 }).map((i) => i / TWO_POW_32);
const nArb = fc.integer({ min: 0, max: 200 });
const qArb = fc.double({ min: 0, max: 1, noNaN: true });

describe('intPow', () => {
  it('matches repeated multiplication, including exponent 0', () => {
    expect(intPow(0.5, 0)).toBe(1);
    expect(intPow(0.5, 3)).toBe(0.125);
    expect(intPow(0, 0)).toBe(1);
    expect(intPow(0, 5)).toBe(0);
  });
});

describe('sampleBinomial edge cases (spec §10, §18)', () => {
  it('n = 0 always gives 0', () => {
    for (const q of [0, 0.3, 0.5, 0.9, 1]) expect(sampleBinomial(0, q, 0.7)).toBe(0);
  });

  it('q = 0 gives 0 and q = 1 gives n', () => {
    expect(sampleBinomial(10, 0, 0.999)).toBe(0);
    expect(sampleBinomial(10, -0.1, 0.5)).toBe(0);
    expect(sampleBinomial(10, 1, 0)).toBe(10);
    expect(sampleBinomial(10, 1.2, 0.5)).toBe(10);
  });

  it('q = 0.5 splits the unit interval symmetrically for n = 1', () => {
    expect(sampleBinomial(1, 0.5, 0.49)).toBe(0);
    expect(sampleBinomial(1, 0.5, 0.5)).toBe(1);
  });

  // Rev 49: at u = 0 the flip ran the walk at 1 - u = 1, where rounding could pass n.
  test.prop([nArb, qArb.filter((q) => q < 1)])('u = 0 gives 0 events for every q < 1', (n, q) => {
    expect(sampleBinomial(n, q, 0)).toBe(0);
  });

  it('n is reachable through the walk (no fallback) when P(n) is large', () => {
    expect(binomialWalk(1, 0.5, 0.9)).toEqual({ k: 1, usedFallback: false });
  });

  it('rejects inputs no caller should produce', () => {
    expect(() => sampleBinomial(-1, 0.5, 0.5)).toThrow(RangeError);
    expect(() => sampleBinomial(2.5, 0.5, 0.5)).toThrow(RangeError);
    expect(() => sampleBinomial(5, Number.NaN, 0.5)).toThrow(RangeError);
    expect(() => sampleBinomial(5, 0.5, 1)).toThrow(RangeError);
    expect(() => sampleBinomial(5, 0.5, -0.1)).toThrow(RangeError);
    expect(() => sampleBinomial(1001, 0.5, 0.5)).toThrow(RangeError);
    expect(() => sampleBinomial(5, 0.5, 1e-12)).toThrow(RangeError);
  });
});

describe('sampleBinomial properties (spec §18, rev 31, rev 44, rev 49)', () => {
  test.prop([nArb, qArb, uArb])('result is an integer in [0, n]', (n, q, u) => {
    const k = sampleBinomial(n, q, u);
    expect(Number.isInteger(k)).toBe(true);
    expect(k).toBeGreaterThanOrEqual(0);
    expect(k).toBeLessThanOrEqual(n);
  });

  test.prop([nArb, qArb, qArb, uArb])('monotone in q for a fixed key (the 1 - u flip)', (n, q1, q2, u) => {
    const lo = Math.min(q1, q2);
    const hi = Math.max(q1, q2);
    expect(sampleBinomial(n, lo, u)).toBeLessThanOrEqual(sampleBinomial(n, hi, u));
  });

  // Targets the flip boundary, where the v0.16 same-u flip broke monotonicity.
  test.prop([nArb, fc.double({ min: 0.45, max: 0.55, noNaN: true }), fc.double({ min: 0.45, max: 0.55, noNaN: true }), uArb])(
    'monotone in q across the q = 0.5 flip',
    (n, q1, q2, u) => {
      const lo = Math.min(q1, q2);
      const hi = Math.max(q1, q2);
      expect(sampleBinomial(n, lo, u)).toBeLessThanOrEqual(sampleBinomial(n, hi, u));
    },
  );

  test.prop([nArb, qArb, uArb, uArb])('nondecreasing in u (inverse CDF)', (n, q, u1, u2) => {
    const lo = Math.min(u1, u2);
    const hi = Math.max(u1, u2);
    expect(sampleBinomial(n, q, lo)).toBeLessThanOrEqual(sampleBinomial(n, q, hi));
  });

  test.prop([nArb, fc.double({ min: 0, max: 0.5, noNaN: true }), uArb])(
    'fallback is taken only when the cumulative sum up to n - 1 is <= u',
    (n, q, u) => {
      const { k, usedFallback } = binomialWalk(n, q, u);
      if (!usedFallback) return;
      expect(k).toBe(n);
      const pmf = refPmf(n, q);
      let cdfBelowN = 0;
      for (let i = 0; i < n; i++) cdfBelowN += pmf[i] ?? 0;
      // Reference and walk round differently; allow far less than one rand01 step.
      expect(cdfBelowN).toBeLessThanOrEqual(u + 1e-12);
    },
  );
});

describe('sampleBinomial matches the exact pmf (spec §18)', () => {
  // Inverse CDF is monotone in u, so a uniform grid of u assigns each k a run of grid
  // points of length P(k) * G, give or take one point at each boundary.
  const G = 1 << 14;
  const cases: [number, number][] = [
    [1, 0.3], [5, 0.0126], [12, 0.5], [20, 0.0475], [25, 0.9], [40, 0.25], [60, 0.75], [200, 0.0028], [100, 0.6],
  ];
  for (const [n, q] of cases) {
    it(`n = ${n}, q = ${q}`, () => {
      const counts = new Array<number>(n + 1).fill(0);
      for (let i = 0; i < G; i++) {
        const k = sampleBinomial(n, q, i / G); // i / 2^14 lies on the 2^-32 lattice
        counts[k] = (counts[k] ?? 0) + 1;
      }
      const pmf = refPmf(n, q);
      for (let k = 0; k <= n; k++) {
        expect(Math.abs((counts[k] ?? 0) / G - (pmf[k] ?? 0))).toBeLessThanOrEqual(2 / G);
      }
    });
  }
});
