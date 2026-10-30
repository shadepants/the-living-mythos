import { describe, expect, it } from 'vitest';
import { Purpose, hashKey, rand01, type RngKey } from '../src/index.ts';

const key = (overrides: Partial<RngKey> = {}): RngKey => ({
  seed: 42,
  season: 1000,
  entity: 7,
  entityHi: 0,
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
    expect(hashKey(key({ entityHi: 1 }))).not.toBe(base);
    expect(hashKey(key({ purpose: Purpose.Birth }))).not.toBe(base);
  });

  it('separates entities that share their low 32 bits and differ only in the high 32', () => {
    // Before rev 13 the key held only 32 bits of the id, so these two shared every draw.
    const a = key({ entity: 5, entityHi: 9 });
    const b = key({ entity: 5, entityHi: 10 });
    expect(hashKey(a)).not.toBe(hashKey(b));
    expect(rand01(a)).not.toBe(rand01(b));
  });

  it('separates entities that share their high 32 bits and differ only in the low 32', () => {
    expect(hashKey(key({ entity: 5, entityHi: 9 }))).not.toBe(hashKey(key({ entity: 6, entityHi: 9 })));
  });

  it('distinguishes swapped entity and entityHi values', () => {
    expect(hashKey(key({ entity: 7, entityHi: 1000 }))).not.toBe(hashKey(key({ entity: 1000, entityHi: 7 })));
  });

  it('distinguishes swapped field values', () => {
    expect(hashKey(key({ season: 7, entity: 1000 }))).not.toBe(hashKey(key({ season: 1000, entity: 7 })));
  });

  it('pins known outputs so any cross-engine or refactor drift fails loudly', () => {
    // Golden values captured on Node 22. A change here means old saves and forks no longer replay.
    // Recaptured once on 2026-10-30 (rev 13: entityHi joined the key); previous values were
    // 3476084382 and 892054880. No saves existed then.
    expect(hashKey(key())).toMatchInlineSnapshot(`1759517345`);
    expect(hashKey({ seed: 0, season: 0, entity: 0, entityHi: 0, purpose: 0 })).toMatchInlineSnapshot(`3421405739`);
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
    expect(() => hashKey(key({ entityHi: 2 ** 32 }))).toThrow(RangeError);
    expect(() => hashKey(key({ entityHi: -1 }))).toThrow(RangeError);
    expect(() => hashKey(key({ entityHi: 1.5 }))).toThrow(RangeError);
    expect(() => hashKey(key({ purpose: Number.NaN }))).toThrow(RangeError);
  });

  it.todo('a no-op nudge produces an identical fork (needs the tick loop)');
});
