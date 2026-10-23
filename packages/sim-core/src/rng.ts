// Hard rule 1: randomness is a pure function of (seed, season, entity, purpose).
// There is no shared stream, so drawing a number for one entity can never shift
// the numbers another entity gets. That is what keeps forks comparable.

const UINT32_MAX = 0xffffffff;
const TWO_POW_32 = 0x100000000;

/** Purpose codes keep draws for different decisions independent. Append only; never renumber. */
export const Purpose = {
  ForageYield: 1,
  Migration: 2,
  Birth: 3,
  Death: 4,
  Invention: 5,
} as const;
export type Purpose = (typeof Purpose)[keyof typeof Purpose];

export interface RngKey {
  readonly seed: number;
  /** Absolute season index since world start. */
  readonly season: number;
  readonly entity: number;
  readonly purpose: number;
}

// lowbias32 integer finalizer (Chris Wellons). Math.imul and bit ops are exact
// 32-bit integer operations in every engine, so this is platform-independent.
const mix32 = (input: number): number => {
  let h = input >>> 0;
  h = Math.imul(h ^ (h >>> 16), 0x7feb352d);
  h = Math.imul(h ^ (h >>> 15), 0x846ca68b);
  return (h ^ (h >>> 16)) >>> 0;
};

const assertUint32 = (name: string, value: number): void => {
  if (!Number.isInteger(value) || value < 0 || value > UINT32_MAX) {
    throw new RangeError(`rng key field "${name}" must be an integer in [0, 2^32-1], got ${value}`);
  }
};

/** Deterministic 32-bit hash of a key. */
export const hashKey = (key: RngKey): number => {
  assertUint32('seed', key.seed);
  assertUint32('season', key.season);
  assertUint32('entity', key.entity);
  assertUint32('purpose', key.purpose);

  // Distinct odd constants per field so swapping two field values changes the hash.
  let h = mix32(key.seed ^ 0x9e3779b9);
  h = mix32(h ^ key.season ^ 0x85ebca6b);
  h = mix32(h ^ key.entity ^ 0xc2b2ae35);
  h = mix32(h ^ key.purpose ^ 0x27d4eb2f);
  return h;
};

/** Uniform float in [0, 1). Division by a power of two is exact in IEEE 754. */
export const rand01 = (key: RngKey): number => hashKey(key) / TWO_POW_32;
