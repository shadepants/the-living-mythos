import { describe, expect, it } from 'vitest';
import { DEFAULT_CONFIG, hashConfig, type SimConfig } from '../src/index.ts';

const config = (overrides: Partial<SimConfig> = {}): SimConfig => ({ ...DEFAULT_CONFIG, ...overrides });

describe('config hash (hard rule 7)', () => {
  it('returns the same hash for equal configs', () => {
    expect(hashConfig(config())).toBe(hashConfig(config()));
  });

  it('does not depend on key order', () => {
    const reordered: SimConfig = {
      startingBandSize: DEFAULT_CONFIG.startingBandSize,
      seasonsPerYear: DEFAULT_CONFIG.seasonsPerYear,
      version: DEFAULT_CONFIG.version,
    };
    expect(hashConfig(reordered)).toBe(hashConfig(DEFAULT_CONFIG));
  });

  it('changes when any single value changes', () => {
    const base = hashConfig(config());
    expect(hashConfig(config({ version: DEFAULT_CONFIG.version + 1 }))).not.toBe(base);
    expect(hashConfig(config({ seasonsPerYear: DEFAULT_CONFIG.seasonsPerYear + 1 }))).not.toBe(base);
    expect(hashConfig(config({ startingBandSize: DEFAULT_CONFIG.startingBandSize + 1 }))).not.toBe(base);
  });

  it('distinguishes swapped values between keys', () => {
    const a = config({ seasonsPerYear: 4, startingBandSize: 25 });
    const b = config({ seasonsPerYear: 25, startingBandSize: 4 });
    expect(hashConfig(a)).not.toBe(hashConfig(b));
  });

  it('handles negative and large safe integers', () => {
    const negative = hashConfig(config({ startingBandSize: -1 }));
    const big = hashConfig(config({ startingBandSize: Number.MAX_SAFE_INTEGER }));
    expect(negative).not.toBe(big);
    expect(negative).not.toBe(hashConfig(config()));
  });

  it('rejects non-integer values, since float formatting is not portable', () => {
    expect(() => hashConfig(config({ startingBandSize: 2.5 }))).toThrow(RangeError);
    expect(() => hashConfig(config({ startingBandSize: Number.NaN }))).toThrow(RangeError);
  });

  it('pins a known output so any drift fails loudly', () => {
    // Golden value: a change means saves and forks no longer match their recorded config hash.
    expect(hashConfig(DEFAULT_CONFIG)).toMatchInlineSnapshot(`2396677394`);
  });
});
