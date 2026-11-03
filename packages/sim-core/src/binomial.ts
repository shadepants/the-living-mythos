// Spec §10 (decision log rev 31, corrected revs 44 and 49): exact Bin(n, q) by inverse CDF
// from one uniform u. Basic arithmetic only (hard rule 2), so the draw is identical on
// every engine. The caller supplies u = rand01(key); this module never draws.

/** x^e for a non-negative integer e by repeated multiplication (Math.pow and ** are banned). */
export const intPow = (x: number, e: number): number => {
  let out = 1;
  for (let i = 0; i < e; i++) out *= x;
  return out;
};

export interface WalkResult {
  readonly k: number;
  /** True when the cumulative sum never exceeded u and n was returned by fallback. */
  readonly usedFallback: boolean;
}

/**
 * Inverse-CDF walk for q in [0, 0.5]. With 1 − q ≥ 0.5 the ratio q/(1 − q) never divides by 0,
 * and p(0) = (1 − q)^n underflows only past n ≈ 1,074 (bracket counts stay far below).
 * Exported for the fallback property test; callers use `sampleBinomial`.
 */
export const binomialWalk = (n: number, q: number, u: number): WalkResult => {
  const ratio = q / (1 - q);
  let p = intPow(1 - q, n);
  let cumulative = p;
  let k = 0;
  while (cumulative <= u) {
    // Rounding (~1e-14) can leave the sum ≤ u at k = n; n is then the only valid answer.
    if (k === n) return { k: n, usedFallback: true };
    p = (p * (n - k)) / (k + 1) * ratio;
    k++;
    cumulative += p;
  }
  return { k, usedFallback: false };
};

/**
 * Number of events among n trials with probability q each, for uniform u in [0, 1).
 * Monotone in q for a fixed u: for q > 0.5 it returns n − Bin(n, 1 − q) drawn with 1 − u
 * (the same-u flip broke monotonicity, rev 31).
 */
export const sampleBinomial = (n: number, q: number, u: number): number => {
  if (!Number.isInteger(n) || n < 0) throw new RangeError(`binomial n must be a non-negative integer, got ${n}`);
  if (Number.isNaN(q)) throw new RangeError('binomial q must not be NaN');
  if (!(u >= 0 && u < 1)) throw new RangeError(`binomial u must be in [0, 1), got ${u}`);

  if (q <= 0) return 0;
  if (q >= 1) return n;
  // Rev 49: the flip would run the walk at 1 − u = 1, where rounding can pass 1 before k = n.
  if (u === 0) return 0;
  if (q > 0.5) return n - binomialWalk(n, 1 - q, 1 - u).k;
  return binomialWalk(n, q, u).k;
};
