import { describe, expect, it } from 'vitest';
import { MAX_CAUSES, createEventLog, founderId, type Cause, type EventLog } from '../src/index.ts';

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
