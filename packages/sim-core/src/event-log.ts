// Hard rule 5: a causal event log from day one. Every event records at most
// three enabling causes (an event or a nudge command), so history stays a graph
// you can walk backwards instead of a diffuse pile of contributing factors.
//
// Ids are sequential and local to one run. Across runs and forks an event is
// matched by its content key (type, tick, primary lineage id, plus an ordinal
// when those three collide). Salience is not decided here: this log records
// what happened, and the narration layer later decides what matters.

import { isEntityId, type EntityId } from './lineage.ts';

const UINT32_MAX = 0xffffffff;
const TYPE_PATTERN = /^[a-z][a-z0-9_]*$/;

/** Most enabling causes one event may record. */
export const MAX_CAUSES = 3;

/** Sequential id, valid only inside the run that produced it. */
export type EventId = number;

/**
 * What enabled an event. Event causes are checked against this log. Command causes
 * (nudges) are only checked as non-negative integers until a command log exists.
 */
export type Cause =
  | { readonly kind: 'event'; readonly id: EventId }
  | { readonly kind: 'command'; readonly id: number };

export interface EventInput {
  /** Lowercase snake_case, e.g. `band_migrated`. Never contains ':'. */
  readonly type: string;
  /** Absolute simulation tick. Must not go backwards between appends. */
  readonly tick: number;
  /** The entity this event is mainly about. */
  readonly primary: EntityId;
  readonly causes?: readonly Cause[];
  /** Flat integers for narration templates (floats are rejected, as in the config). */
  readonly payload?: Readonly<Record<string, number>>;
}

export interface LogEvent {
  readonly id: EventId;
  readonly type: string;
  readonly tick: number;
  readonly primary: EntityId;
  /** Count of earlier events with the same type, tick and primary. Almost always 0. */
  readonly ordinal: number;
  /** `type:tick:primary:ordinal`, stable across runs and used to match events in forks. */
  readonly contentKey: string;
  readonly causes: readonly Cause[];
  readonly payload: Readonly<Record<string, number>>;
}

export interface EventLog {
  /**
   * Validates and records an event, returning the frozen stored copy.
   * @throws RangeError on any invariant violation; the log is left unchanged.
   */
  readonly append: (input: EventInput) => LogEvent;
  readonly get: (id: EventId) => LogEvent | undefined;
  /** All events in append order (a copy; the log itself cannot be mutated through it). */
  readonly events: () => readonly LogEvent[];
  readonly size: number;
}

const assertUint32 = (name: string, value: number): void => {
  if (!Number.isInteger(value) || value < 0 || value > UINT32_MAX) {
    throw new RangeError(`event field "${name}" must be an integer in [0, 2^32-1], got ${value}`);
  }
};

const freezeCauses = (causes: readonly Cause[], existingEvents: number): readonly Cause[] => {
  if (causes.length > MAX_CAUSES) {
    throw new RangeError(`an event records at most ${MAX_CAUSES} causes, got ${causes.length}`);
  }
  const seen = new Set<string>();
  const frozen = causes.map((cause): Cause => {
    if (!Number.isSafeInteger(cause.id) || cause.id < 0) {
      throw new RangeError(`${cause.kind} cause id must be a non-negative integer, got ${cause.id}`);
    }
    if (cause.kind === 'event' && cause.id >= existingEvents) {
      throw new RangeError(`event cause ${cause.id} does not exist yet (log has ${existingEvents} events)`);
    }
    const key = `${cause.kind}:${cause.id}`;
    if (seen.has(key)) throw new RangeError(`duplicate cause ${key}`);
    seen.add(key);
    return Object.freeze({ kind: cause.kind, id: cause.id });
  });
  return Object.freeze(frozen);
};

const freezePayload = (payload: Readonly<Record<string, number>>): Readonly<Record<string, number>> => {
  const copy: Record<string, number> = {};
  for (const [name, value] of Object.entries(payload)) {
    if (!Number.isSafeInteger(value)) {
      throw new RangeError(`payload field "${name}" must be a safe integer, got ${value}`);
    }
    copy[name] = value;
  }
  return Object.freeze(copy);
};

/** Creates an empty event log. */
export const createEventLog = (): EventLog => {
  const stored: LogEvent[] = [];
  const ordinals = new Map<string, number>();

  const append = (input: EventInput): LogEvent => {
    if (!TYPE_PATTERN.test(input.type)) {
      throw new RangeError(`event type must match ${TYPE_PATTERN}, got "${input.type}"`);
    }
    assertUint32('tick', input.tick);
    if (!isEntityId(input.primary)) {
      throw new RangeError(`event primary must be a well-formed entity id, got "${input.primary}"`);
    }
    const last = stored[stored.length - 1];
    if (last !== undefined && input.tick < last.tick) {
      throw new RangeError(`event tick ${input.tick} is earlier than the previous event tick ${last.tick}`);
    }

    // Validate everything before touching state, so a rejected append changes nothing.
    const causes = freezeCauses(input.causes ?? [], stored.length);
    const payload = freezePayload(input.payload ?? {});

    const groupKey = `${input.type}:${input.tick}:${input.primary}`;
    const ordinal = ordinals.get(groupKey) ?? 0;
    ordinals.set(groupKey, ordinal + 1);

    const event: LogEvent = Object.freeze({
      id: stored.length,
      type: input.type,
      tick: input.tick,
      primary: input.primary,
      ordinal,
      contentKey: `${groupKey}:${ordinal}`,
      causes,
      payload,
    });
    stored.push(event);
    return event;
  };

  return {
    append,
    get: (id) => stored[id],
    events: () => stored.slice(),
    get size() {
      return stored.length;
    },
  };
};
