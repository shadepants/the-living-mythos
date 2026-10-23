import { describe, expect, it } from 'vitest';
import { Purpose, hashKey, rand01, type RngKey } from '../src/index.ts';

const key = (overrides: Partial<RngKey> = {}): RngKey => ({
  seed: 42,
  season: 1000,
  entity: 7,
  purpose: Purpose.Migration,
  ...overrides,
});

describe('hash-based rng (hard rule 1)', () => {
  it('returns the same value for the same key', () => {
    expect(rand01(key())).toBe(rand01(key()));
  });

  it('is unaffected by unrelated draws (no shared stream)', () => {
    const before = rand01(key());
    for (let e = 0; e < 1000; e++) rand01(key({ entity: e }));
    expect(rand01(key())).toBe(before);
  });

  it('changes when any single key field changes', () => {
    const base = hashKey(key());
    expect(hashKey(key({ seed: 43 }))).not.toBe(base);
    expect(hashKey(key({ season: 1001 }))).not.toBe(base);
    expect(hashKey(key({ entity: 8 }))).not.toBe(base);
    expect(hashKey(key({ purpose: Purpose.Birth }))).not.toBe(base);
  });

  it('distinguishes swapped field values', () => {
    expect(hashKey(key({ season: 7, entity: 1000 }))).not.toBe(hashKey(key({ season: 1000, entity: 7 })));
  });

  it('pins known outputs so any cross-engine or refactor drift fails loudly', () => {
    // Golden values captured on Node 22. A change here means old saves and forks no longer replay.
    expect(hashKey(key())).toMatchInlineSnapshot(`3476084382`);
    expect(hashKey({ seed: 0, season: 0, entity: 0, purpose: 0 })).toMatchInlineSnapshot(`892054880`);
  });

  it('stays in [0, 1) and is roughly uniform', () => {
    const n = 100_000;
    const buckets = new Array<number>(10).fill(0);
    for (let i = 0; i < n; i++) {
      const r = rand01(key({ entity: i }));
      expect(r).toBeGreaterThanOrEqual(0);
      expect(r).toBeLessThan(1);
      const b = Math.floor(r * 10);
      buckets[b] = (buckets[b] ?? 0) + 1;
    }
    for (const count of buckets) {
      expect(Math.abs(count - n / 10)).toBeLessThan(n / 10 * 0.05);
    }
  });

  it('rejects keys that are not uint32 integers', () => {
    expect(() => hashKey(key({ seed: -1 }))).toThrow(RangeError);
    expect(() => hashKey(key({ season: 1.5 }))).toThrow(RangeError);
    expect(() => hashKey(key({ entity: 2 ** 32 }))).toThrow(RangeError);
    expect(() => hashKey(key({ purpose: Number.NaN }))).toThrow(RangeError);
  });

  it.todo('a no-op nudge produces an identical fork (needs the tick loop)');
});
