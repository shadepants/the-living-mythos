import { describe, expect, it } from 'vitest';
import { fc, test } from '@fast-check/vitest';
import { createEntityRegistry } from '../src/entity-registry.ts';
import { ROOT_ID, deriveEntityId, founderId, type EntityId } from '../src/lineage.ts';

describe('entity registry (hard rule 3, spec §5.1, §12, §20)', () => {
  it('registers founders under ROOT_ID with the lineage-derived id', () => {
    const reg = createEntityRegistry();
    const a = reg.register(ROOT_ID, 0, 0);
    const b = reg.register(ROOT_ID, 0, 1);
    expect(a.id).toBe(founderId(0));
    expect(b.id).toBe(founderId(1));
    expect(a).toEqual({ id: founderId(0), parent: ROOT_ID, birthTick: 0, siblingIndex: 0 });
    expect(Object.isFrozen(a)).toBe(true);
  });

  it('stores the parent, which the id itself does not encode', () => {
    const reg = createEntityRegistry();
    const parent = reg.register(ROOT_ID, 0, 0);
    const daughter = reg.register(parent.id, 4800, 0);
    expect(daughter.id).toBe(deriveEntityId(parent.id, 4800, 0));
    expect(reg.get(daughter.id)?.parent).toBe(parent.id);
    expect(reg.has(daughter.id)).toBe(true);
  });

  it('asserts uniqueness: the same (parent, tick, sibling) twice throws and changes nothing', () => {
    const reg = createEntityRegistry();
    const parent = reg.register(ROOT_ID, 0, 0);
    reg.register(parent.id, 10, 0);
    expect(() => reg.register(parent.id, 10, 0)).toThrow(/already registered/);
    expect(reg.size).toBe(2);
  });

  it('rejects an unregistered parent', () => {
    const reg = createEntityRegistry();
    expect(() => reg.register(founderId(7), 10, 0)).toThrow(/parent/);
    expect(reg.size).toBe(0);
  });

  it('rejects a birth tick earlier than the parent birth tick', () => {
    const reg = createEntityRegistry();
    const parent = reg.register(ROOT_ID, 0, 0);
    const child = reg.register(parent.id, 50, 0);
    expect(() => reg.register(child.id, 49, 0)).toThrow(/birth tick/);
    expect(reg.size).toBe(2);
  });

  it('rejects malformed ids and out-of-range numbers', () => {
    const reg = createEntityRegistry();
    expect(() => reg.register('nope' as EntityId, 0, 0)).toThrow(RangeError);
    expect(() => reg.register(ROOT_ID, -1, 0)).toThrow(RangeError);
    expect(() => reg.register(ROOT_ID, 0, 1.5)).toThrow(RangeError);
    expect(reg.size).toBe(0);
  });

  it('keeps ended entities: records are never removed (history records, §12)', () => {
    const reg = createEntityRegistry();
    reg.register(ROOT_ID, 0, 0);
    expect(reg.records().length).toBe(1);
    expect(reg).not.toHaveProperty('remove');
  });

  it('lists records in registration order and cannot be mutated through records()', () => {
    const reg = createEntityRegistry();
    const ids = [0, 1, 2].map((i) => reg.register(ROOT_ID, 0, i).id);
    (reg.records() as unknown[]).pop();
    expect(reg.records().map((r) => r.id)).toEqual(ids);
  });

  it('stores -0 inputs as 0', () => {
    const r = createEntityRegistry().register(ROOT_ID, -0, -0);
    expect(Object.is(r.birthTick, 0)).toBe(true);
    expect(Object.is(r.siblingIndex, 0)).toBe(true);
  });

  it('returns undefined for an unknown id and for ROOT_ID (not an entity)', () => {
    const reg = createEntityRegistry();
    expect(reg.get(founderId(0))).toBeUndefined();
    expect(reg.get(ROOT_ID)).toBeUndefined();
    expect(reg.has(ROOT_ID)).toBe(false);
  });
});

describe('entity registry properties', () => {
  // Build a random family tree: each step picks an existing entity (or ROOT) as parent.
  const step = fc.record({
    parentPick: fc.nat(),
    tickDelta: fc.integer({ min: 0, max: 40 }),
    sibling: fc.integer({ min: 0, max: 3 }),
  });

  test.prop([fc.array(step, { maxLength: 60 })])(
    'every stored record re-derives its id from its stored parent, and ids are unique',
    (steps) => {
      const reg = createEntityRegistry();
      for (const s of steps) {
        const all = reg.records();
        const pick = s.parentPick % (all.length + 1);
        const parent = pick === all.length ? undefined : all[pick];
        const parentId = parent?.id ?? ROOT_ID;
        const tick = (parent?.birthTick ?? 0) + s.tickDelta;
        try {
          reg.register(parentId, tick, s.sibling);
        } catch (error) {
          // Only a repeated (parent, tick, sibling) may be refused here.
          expect(String(error)).toMatch(/already registered/);
        }
      }
      const records = reg.records();
      expect(new Set(records.map((r) => r.id)).size).toBe(records.length);
      for (const r of records) {
        expect(deriveEntityId(r.parent, r.birthTick, r.siblingIndex)).toBe(r.id);
        expect(r.parent === ROOT_ID || reg.has(r.parent)).toBe(true);
      }
    },
  );

  test.prop([fc.array(step, { maxLength: 40 })])('the same registrations give the same registry (replayable)', (steps) => {
    const run = (): unknown[] => {
      const reg = createEntityRegistry();
      for (const s of steps) {
        const all = reg.records();
        const pick = s.parentPick % (all.length + 1);
        const parent = pick === all.length ? undefined : all[pick];
        try {
          reg.register(parent?.id ?? ROOT_ID, (parent?.birthTick ?? 0) + s.tickDelta, s.sibling);
        } catch {
          // duplicates refused identically in both runs
        }
      }
      return reg.records().map((r) => ({ ...r }));
    };
    expect(run()).toEqual(run());
  });
});
