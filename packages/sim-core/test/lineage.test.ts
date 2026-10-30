import { describe, expect, it } from 'vitest';
import { ROOT_ID, Purpose, deriveEntityId, entityKey, founderId, rand01 } from '../src/index.ts';

describe('lineage-derived entity ids (hard rule 3)', () => {
  it('derives the same id from the same (parent, birth season, sibling index)', () => {
    const parent = founderId(0);
    expect(deriveEntityId(parent, 120, 1)).toBe(deriveEntityId(parent, 120, 1));
  });

  it('is a fixed-length 16 character lowercase hex string', () => {
    expect(founderId(0)).toMatch(/^[0-9a-f]{16}$/);
    let id = founderId(3);
    for (let generation = 0; generation < 200; generation++) id = deriveEntityId(id, generation, 0);
    expect(id).toMatch(/^[0-9a-f]{16}$/);
  });

  it('changes when any single input changes', () => {
    const parent = founderId(0);
    const base = deriveEntityId(parent, 120, 1);
    expect(deriveEntityId(founderId(1), 120, 1)).not.toBe(base);
    expect(deriveEntityId(parent, 121, 1)).not.toBe(base);
    expect(deriveEntityId(parent, 120, 2)).not.toBe(base);
  });

  it('distinguishes swapped season and sibling index', () => {
    const parent = founderId(0);
    expect(deriveEntityId(parent, 7, 1000)).not.toBe(deriveEntityId(parent, 1000, 7));
  });

  it('does not depend on whether other siblings exist', () => {
    const parent = founderId(0);
    const alone = deriveEntityId(parent, 50, 2);
    deriveEntityId(parent, 50, 0);
    deriveEntityId(parent, 50, 1);
    expect(deriveEntityId(parent, 50, 2)).toBe(alone);
  });

  it('gives founders distinct ids rooted at ROOT_ID', () => {
    expect(founderId(0)).toBe(deriveEntityId(ROOT_ID, 0, 0));
    expect(founderId(0)).not.toBe(founderId(1));
    expect(founderId(0)).not.toBe(ROOT_ID);
  });

  it('produces no duplicate ids across a large family tree', () => {
    const seen = new Set<string>();
    let count = 0;
    for (let f = 0; f < 10; f++) {
      const founder = founderId(f);
      for (let season = 0; season < 100; season++) {
        for (let sibling = 0; sibling < 100; sibling++) {
          seen.add(deriveEntityId(founder, season, sibling));
          count++;
        }
      }
    }
    expect(count).toBe(100_000);
    expect(seen.size).toBe(count);
  });

  it('rejects season and sibling index outside uint32', () => {
    const parent = founderId(0);
    expect(() => deriveEntityId(parent, -1, 0)).toThrow(RangeError);
    expect(() => deriveEntityId(parent, 0, 1.5)).toThrow(RangeError);
    expect(() => deriveEntityId(parent, 2 ** 32, 0)).toThrow(RangeError);
  });

  it('rejects a malformed parent id', () => {
    expect(() => deriveEntityId('not-an-id' as never, 0, 0)).toThrow(RangeError);
  });

  it('pins known outputs so any drift fails loudly', () => {
    // Golden values: a change means every saved lineage and fork gets new ids.
    expect(founderId(0)).toMatchInlineSnapshot(`"352bad6048ab73b3"`);
    expect(deriveEntityId(founderId(0), 120, 1)).toMatchInlineSnapshot(`"681d77bea5f3eabe"`);
  });
});

describe('entityKey (bridge to the rng)', () => {
  it('returns a stable uint32 for an id', () => {
    const key = entityKey(founderId(0));
    expect(Number.isInteger(key)).toBe(true);
    expect(key).toBeGreaterThanOrEqual(0);
    expect(key).toBeLessThanOrEqual(0xffffffff);
    expect(entityKey(founderId(0))).toBe(key);
  });

  it('feeds rand01 without throwing and keeps entities independent', () => {
    const a = founderId(0);
    const b = founderId(1);
    const draw = (id: typeof a): number =>
      rand01({ seed: 42, season: 10, entity: entityKey(id), purpose: Purpose.Birth });
    const before = draw(a);
    draw(b);
    expect(draw(a)).toBe(before);
    expect(draw(a)).not.toBe(draw(b));
  });
});
