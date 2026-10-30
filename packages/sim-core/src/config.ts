// Hard rule 7: every tunable lives in one versioned config, and saves and forks
// record its hash. Values are integers only: float-to-text formatting is not
// guaranteed identical across engines, so floats never enter the hash input.

import { mix32 } from './rng.ts';

const TWO_POW_32 = 0x100000000;

/**
 * The versioned set of tunables. Placeholder fields until the design log fixes the real ones.
 * A type alias, not an interface: only aliases are assignable to the string-indexed record
 * that `hashConfig` accepts.
 */
export type SimConfig = {
  /** Bump when the meaning of any field changes. */
  readonly version: number;
  readonly seasonsPerYear: number;
  readonly startingBandSize: number;
};

export const DEFAULT_CONFIG: SimConfig = {
  version: 1,
  seasonsPerYear: 4,
  startingBandSize: 25,
};

const foldWord = (state: number, word: number): number => mix32(state ^ word);

const foldString = (state: number, text: string): number => {
  let h = foldWord(state, text.length);
  for (let i = 0; i < text.length; i++) h = foldWord(h, text.charCodeAt(i));
  return h;
};

const foldInteger = (state: number, name: string, value: number): number => {
  if (!Number.isSafeInteger(value)) {
    throw new RangeError(`config field "${name}" must be a safe integer, got ${value}`);
  }
  // `>>> 0` is ToUint32 (value mod 2^32, correct for negatives); division by 2^32 is exact.
  const low = value >>> 0;
  const high = Math.floor(value / TWO_POW_32) >>> 0;
  return foldWord(foldWord(state, low), high);
};

/**
 * Deterministic 32-bit hash of a flat integer config. Keys are sorted by UTF-16
 * code unit, so object key order never affects the result.
 * @throws RangeError if any value is not a safe integer.
 */
export const hashConfig = (config: Readonly<Record<string, number>>): number => {
  let h = mix32(0x6a09e667);
  for (const name of Object.keys(config).sort()) {
    h = foldString(h, name);
    h = foldInteger(h, name, config[name] as number);
  }
  return h;
};
