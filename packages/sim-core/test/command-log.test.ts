import { describe, expect, it } from 'vitest';
import { fc, test } from '@fast-check/vitest';
import { CommandError, createCommandLog, type DroughtCommandInput } from '../src/command-log.ts';

const WORLD = { worldWidth: 32, worldHeight: 32 } as const;

const valid = (overrides: Partial<DroughtCommandInput> = {}): DroughtCommandInput => ({
  tick: 10,
  sign: -1,
  magnitude: 9000,
  durationSeasons: 8,
  centerCell: 500,
  radius: 20,
  ...overrides,
});

const fieldOf = (fn: () => unknown): string | undefined => {
  try {
    fn();
  } catch (error) {
    if (error instanceof CommandError) return error.field;
    throw error;
  }
  return undefined;
};

describe('command log (hard rule 6, spec §5.1, §13)', () => {
  it('assigns ids 1, 2, ... in append order and stores frozen copies', () => {
    const log = createCommandLog(WORLD);
    const a = log.append(valid(), 0);
    const b = log.append(valid({ sign: 1 }), 0);
    expect([a.id, b.id]).toEqual([1, 2]);
    expect(log.size).toBe(2);
    expect(log.get(1)).toBe(a);
    expect(log.get(0)).toBeUndefined();
    expect(Object.isFrozen(a)).toBe(true);
    expect(log.commands().map((c) => c.id)).toEqual([1, 2]);
  });

  it('cannot be mutated through commands()', () => {
    const log = createCommandLog(WORLD);
    log.append(valid(), 0);
    (log.commands() as unknown[]).pop();
    expect(log.size).toBe(1);
  });

  it('accepts radius 0 (whole map) and a centre on any cell, sea included', () => {
    const log = createCommandLog(WORLD);
    expect(log.append(valid({ radius: 0, centerCell: 0 }), 0).radius).toBe(0);
    expect(log.append(valid({ centerCell: 32 * 32 - 1 }), 0).centerCell).toBe(1023);
  });

  it('accepts commands for the next tick and later ticks in order', () => {
    const log = createCommandLog(WORLD);
    log.append(valid({ tick: 5 }), 5);
    log.append(valid({ tick: 5 }), 5);
    log.append(valid({ tick: 9 }), 6);
    expect(log.size).toBe(3);
  });
});

describe('command validation errors (spec §20)', () => {
  const cases: [string, Partial<DroughtCommandInput>, string][] = [
    ['radius < 0', { radius: -1 }, 'radius'],
    ['durationSeasons < 1', { durationSeasons: 0 }, 'durationSeasons'],
    ['magnitude = 0', { magnitude: 0 }, 'magnitude'],
    ['magnitude < 0', { magnitude: -5 }, 'magnitude'],
    ['sign 0', { sign: 0 }, 'sign'],
    ['sign 2', { sign: 2 }, 'sign'],
    ['centerCell below the map', { centerCell: -1 }, 'centerCell'],
    ['centerCell past the map', { centerCell: 32 * 32 }, 'centerCell'],
    ['non-integer magnitude', { magnitude: 0.5 }, 'magnitude'],
    ['non-integer radius', { radius: 2.5 }, 'radius'],
    ['negative tick', { tick: -1 }, 'tick'],
    ['NaN centerCell', { centerCell: Number.NaN }, 'centerCell'],
  ];
  for (const [name, bad, field] of cases) {
    it(`rejects ${name} with field "${field}" and logs nothing`, () => {
      const log = createCommandLog(WORLD);
      expect(fieldOf(() => log.append(valid(bad), 0))).toBe(field);
      expect(log.size).toBe(0);
    });
  }

  it('rejects a command for a tick already simulated', () => {
    const log = createCommandLog(WORLD);
    expect(fieldOf(() => log.append(valid({ tick: 4 }), 5))).toBe('tick');
    expect(log.size).toBe(0);
  });

  it('rejects a command earlier than the last logged command (append-only in tick order)', () => {
    const log = createCommandLog(WORLD);
    log.append(valid({ tick: 9 }), 0);
    expect(fieldOf(() => log.append(valid({ tick: 8 }), 0))).toBe('tick');
    expect(log.size).toBe(1);
  });

  it('a rejected append does not consume an id', () => {
    const log = createCommandLog(WORLD);
    expect(() => log.append(valid({ sign: 0 }), 0)).toThrow(CommandError);
    expect(log.append(valid(), 0).id).toBe(1);
  });

  it('CommandError is a RangeError naming the field', () => {
    const log = createCommandLog(WORLD);
    expect(() => log.append(valid({ radius: -3 }), 0)).toThrow(RangeError);
    expect(() => log.append(valid({ radius: -3 }), 0)).toThrow(/radius/);
  });

  it('rejects a duration whose last active season passes 2^32 - 1', () => {
    const log = createCommandLog(WORLD);
    const tick = 0xffffffff - 3;
    expect(fieldOf(() => log.append(valid({ tick, durationSeasons: 5 }), 0))).toBe('durationSeasons');
    expect(log.append(valid({ tick, durationSeasons: 4 }), 0).durationSeasons).toBe(4);
  });

  it('stores -0 inputs as 0 (replay equality after a JSON round-trip)', () => {
    const log = createCommandLog(WORLD);
    const c = log.append(valid({ tick: -0, centerCell: -0, radius: -0 }), 0);
    expect(Object.is(c.tick, 0)).toBe(true);
    expect(Object.is(c.centerCell, 0)).toBe(true);
    expect(Object.is(c.radius, 0)).toBe(true);
  });

  it('rejects a malformed nextTick from the sim loop', () => {
    const log = createCommandLog(WORLD);
    expect(() => log.append(valid(), Number.NaN)).toThrow(RangeError);
    expect(log.size).toBe(0);
  });

  it('rejects a world size that is not a positive integer', () => {
    expect(() => createCommandLog({ worldWidth: 0, worldHeight: 32 })).toThrow(RangeError);
    expect(() => createCommandLog({ worldWidth: 32, worldHeight: 1.5 })).toThrow(RangeError);
  });
});

describe('command log properties', () => {
  const commandArb = fc.record({
    tick: fc.integer({ min: 0, max: 50 }),
    sign: fc.constantFrom(-1, 1),
    magnitude: fc.integer({ min: 1, max: 20000 }),
    durationSeasons: fc.integer({ min: 1, max: 40 }),
    centerCell: fc.integer({ min: 0, max: 32 * 32 - 1 }),
    radius: fc.integer({ min: 0, max: 64 }),
  });

  test.prop([fc.array(commandArb, { maxLength: 30 })])(
    'stored ticks never decrease and ids stay dense whatever is attempted',
    (inputs) => {
      const log = createCommandLog(WORLD);
      for (const input of inputs) {
        try {
          log.append(input, 0);
        } catch (error) {
          expect(error).toBeInstanceOf(CommandError);
        }
      }
      const stored = log.commands();
      stored.forEach((c, i) => {
        expect(c.id).toBe(i + 1);
        if (i > 0) expect(c.tick).toBeGreaterThanOrEqual(stored[i - 1]?.tick ?? 0);
      });
    },
  );

  test.prop([fc.array(commandArb, { maxLength: 30 })])('same appends give the same log (replayable)', (inputs) => {
    const run = (): unknown[] => {
      const log = createCommandLog(WORLD);
      for (const input of inputs) {
        try {
          log.append(input, 0);
        } catch {
          // rejections are part of the same deterministic outcome
        }
      }
      return log.commands().map((c) => ({ ...c }));
    };
    expect(run()).toEqual(run());
  });
});
