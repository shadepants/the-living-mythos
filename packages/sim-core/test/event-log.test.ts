import { describe, expect, it } from 'vitest';
import { fc, test } from '@fast-check/vitest';
import { MAX_CAUSES, createEventLog, founderId, type Cause, type EventInput, type EventLog } from '../src/index.ts';

const band = founderId(0);
const otherBand = founderId(1);

const eventCause = (id: number): Cause => ({ kind: 'event', id: id as never });

const seeded = (): EventLog => {
  const log = createEventLog();
  log.append({ type: 'drought_began', tick: 10, primary: band });
  return log;
};

describe('causal event log (hard rule 5)', () => {
  it('assigns sequential run-local ids starting at 0', () => {
    const log = createEventLog();
    const first = log.append({ type: 'drought_began', tick: 1, primary: band });
    const second = log.append({ type: 'band_migrated', tick: 2, primary: band });
    expect(first.id).toBe(0);
    expect(second.id).toBe(1);
    expect(log.size).toBe(2);
    expect(log.get(1)).toBe(second);
  });

  it('builds the content key from type, tick and primary lineage id', () => {
    const log = createEventLog();
    const event = log.append({ type: 'band_migrated', tick: 7, primary: band });
    expect(event.contentKey).toBe(`band_migrated:7:${band}:0`);
    expect(event.ordinal).toBe(0);
  });

  it('disambiguates events that share type, tick and primary with an ordinal', () => {
    const log = createEventLog();
    const a = log.append({ type: 'band_migrated', tick: 7, primary: band });
    const b = log.append({ type: 'band_migrated', tick: 7, primary: band });
    const other = log.append({ type: 'band_migrated', tick: 7, primary: otherBand });
    expect(b.ordinal).toBe(1);
    expect(other.ordinal).toBe(0);
    expect(new Set([a.contentKey, b.contentKey, other.contentKey]).size).toBe(3);
  });

  it('gives the same content keys when the same history is emitted again', () => {
    const emit = (): string[] => {
      const log = createEventLog();
      log.append({ type: 'drought_began', tick: 3, primary: band });
      log.append({ type: 'band_migrated', tick: 4, primary: band });
      log.append({ type: 'band_migrated', tick: 4, primary: band });
      return log.events().map((e) => e.contentKey);
    };
    expect(emit()).toEqual(emit());
  });

  it('records up to three distinct causes', () => {
    const log = createEventLog();
    const c0 = log.append({ type: 'drought_began', tick: 1, primary: band });
    const c1 = log.append({ type: 'forage_failed', tick: 2, primary: band });
    const c2 = log.append({ type: 'food_deficit', tick: 2, primary: band });
    const effect = log.append({
      type: 'band_migrated',
      tick: 3,
      primary: band,
      causes: [
        { kind: 'event', id: c0.id },
        { kind: 'event', id: c1.id },
        { kind: 'event', id: c2.id },
      ],
    });
    expect(MAX_CAUSES).toBe(3);
    expect(effect.causes).toHaveLength(3);
  });

  it('rejects more than three causes', () => {
    const log = createEventLog();
    for (let i = 0; i < 4; i++) log.append({ type: 'forage_failed', tick: 1, primary: band });
    const causes = [0, 1, 2, 3].map(eventCause);
    expect(() => log.append({ type: 'band_migrated', tick: 2, primary: band, causes })).toThrow(RangeError);
  });

  it('rejects duplicate causes', () => {
    const log = seeded();
    const causes = [eventCause(0), eventCause(0)];
    expect(() => log.append({ type: 'band_migrated', tick: 11, primary: band, causes })).toThrow(RangeError);
  });

  it('rejects a cause that points at an event that does not exist yet', () => {
    const log = seeded();
    expect(() =>
      log.append({ type: 'band_migrated', tick: 11, primary: band, causes: [eventCause(1)] }),
    ).toThrow(RangeError);
  });

  it('allows cause and effect inside the same tick', () => {
    // A later-tick cause cannot occur: ticks never go backwards and causes must already exist.
    const log = createEventLog();
    log.append({ type: 'drought_began', tick: 5, primary: band });
    expect(() =>
      log.append({ type: 'band_migrated', tick: 5, primary: band, causes: [eventCause(0)] }),
    ).not.toThrow();
  });

  it('accepts a nudge command as a cause', () => {
    const log = createEventLog();
    const event = log.append({
      type: 'drought_began',
      tick: 1,
      primary: band,
      causes: [{ kind: 'command', id: 0 }],
    });
    expect(event.causes).toEqual([{ kind: 'command', id: 0 }]);
  });

  it('rejects a malformed command cause', () => {
    const log = createEventLog();
    const causes: Cause[] = [{ kind: 'command', id: -1 }];
    expect(() => log.append({ type: 'drought_began', tick: 1, primary: band, causes })).toThrow(RangeError);
  });

  it('rejects ticks that go backwards', () => {
    const log = seeded();
    expect(() => log.append({ type: 'band_migrated', tick: 9, primary: band })).toThrow(RangeError);
  });

  it('rejects bad types, ticks, primaries and payloads', () => {
    const log = createEventLog();
    expect(() => log.append({ type: 'Bad:Type', tick: 1, primary: band })).toThrow(RangeError);
    expect(() => log.append({ type: '', tick: 1, primary: band })).toThrow(RangeError);
    expect(() => log.append({ type: 'ok', tick: -1, primary: band })).toThrow(RangeError);
    expect(() => log.append({ type: 'ok', tick: 1.5, primary: band })).toThrow(RangeError);
    expect(() => log.append({ type: 'ok', tick: 1, primary: 'nope' as never })).toThrow(RangeError);
    expect(() => log.append({ type: 'ok', tick: 1, primary: band, payload: { food: 0.5 } })).toThrow(RangeError);
  });

  it('leaves the log unchanged when an append is rejected', () => {
    const log = seeded();
    expect(() => log.append({ type: 'band_migrated', tick: 11, primary: band, causes: [eventCause(5)] })).toThrow();
    expect(() => log.append({ type: 'band_migrated', tick: 11, primary: band, payload: { x: 0.5 } })).toThrow();
    expect(log.size).toBe(1);
    // The failed attempts must not have consumed ordinal 0 or id 1.
    const next = log.append({ type: 'band_migrated', tick: 11, primary: band });
    expect(next.id).toBe(1);
    expect(next.ordinal).toBe(0);
  });

  it('keeps integer payloads and defaults to empty', () => {
    const log = createEventLog();
    const withPayload = log.append({ type: 'food_deficit', tick: 1, primary: band, payload: { deficit: 12 } });
    const bare = log.append({ type: 'food_deficit', tick: 2, primary: band });
    expect(withPayload.payload).toEqual({ deficit: 12 });
    expect(bare.payload).toEqual({});
  });

  it('is not changed by mutating the input after append', () => {
    const log = createEventLog();
    const causes: Cause[] = [];
    const payload: Record<string, number> = { deficit: 1 };
    const event = log.append({ type: 'food_deficit', tick: 1, primary: band, causes, payload });
    payload['deficit'] = 99;
    expect(event.payload).toEqual({ deficit: 1 });
    expect(Object.isFrozen(event)).toBe(true);
  });

  it('only lets a log reference earlier events, so causal chains cannot loop', () => {
    const log = createEventLog();
    let previous = log.append({ type: 'drought_began', tick: 1, primary: band });
    for (let i = 0; i < 50; i++) {
      previous = log.append({
        type: 'band_migrated',
        tick: 2 + i,
        primary: band,
        causes: [{ kind: 'event', id: previous.id }],
      });
    }
    for (const event of log.events()) {
      for (const cause of event.causes) {
        if (cause.kind === 'event') expect(cause.id).toBeLessThan(event.id);
      }
    }
  });
});

const uint32 = fc.nat({ max: 0xffffffff });
const validEvents = fc
  .array(fc.record({ type: fc.constantFrom('drought_began', 'band_migrated'), tick: uint32, bandIndex: fc.nat({ max: 3 }) }))
  .map((events) => [...events].sort((a, b) => a.tick - b.tick));
const REJECTIONS = ['too_many_causes', 'bad_type', 'future_cause', 'float_payload', 'earlier_tick'] as const;

describe('causal event log properties', () => {
  test.prop([validEvents, fc.constantFrom(...REJECTIONS)])(
    'never changes the log, ordinals included, when an append is rejected',
    (events, rejection) => {
      const log = createEventLog();
      for (const e of events) log.append({ type: e.type, tick: e.tick, primary: founderId(e.bandIndex) });
      const lastTick = events.at(-1)?.tick ?? 0;
      fc.pre(rejection !== 'earlier_tick' || lastTick > 0);
      const before = log.events();

      const base: EventInput = { type: 'drought_began', tick: lastTick, primary: founderId(0) };
      const rejected: Record<(typeof REJECTIONS)[number], EventInput> = {
        too_many_causes: { ...base, causes: [0, 1, 2, 3].map((id): Cause => ({ kind: 'command', id })) },
        bad_type: { ...base, type: 'Drought-Began' },
        future_cause: { ...base, causes: [{ kind: 'event', id: log.size as never }] },
        float_payload: { ...base, payload: { severity: 0.5 } },
        earlier_tick: { ...base, tick: lastTick - 1 },
      };
      expect(() => log.append(rejected[rejection])).toThrow(RangeError);
      expect(log.events()).toEqual(before);

      const sameGroup = before.filter((e) => e.type === base.type && e.tick === base.tick && e.primary === base.primary);
      expect(log.append(base).ordinal).toBe(sameGroup.length);
    },
  );

  test.prop([fc.array(fc.record({ tick: uint32, causeCount: fc.nat({ max: MAX_CAUSES + 2 }) }))])(
    'never stores a tick that goes backwards or more than MAX_CAUSES causes',
    (inputs) => {
      const log = createEventLog();
      for (const { tick, causeCount } of inputs) {
        const causes = Array.from({ length: causeCount }, (_, id): Cause => ({ kind: 'command', id }));
        try {
          log.append({ type: 'band_migrated', tick, primary: band, causes });
        } catch (error) {
          expect(error).toBeInstanceOf(RangeError);
        }
      }
      const stored = log.events();
      expect(stored.every((e, i) => i === 0 || e.tick >= (stored[i - 1]?.tick ?? 0))).toBe(true);
      expect(stored.every((e) => e.causes.length <= MAX_CAUSES)).toBe(true);
    },
  );
});
