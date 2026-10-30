// Hard rule 4: fixed internal substeps for environment fields, and schedules
// never depend on state. Which systems run in a season, in what order and how
// many substeps each takes is a pure function of the season index. State flows
// through the steps but can never change the schedule, so a replay or fork
// always visits the same steps in the same order.
//
// One tick is one season (decision log: seasonal ticks always). Slow systems use
// a fixed period instead of a variable tick length.

const UINT32_MAX = 0xffffffff;

export interface StepContext {
  readonly seed: number;
  /** Absolute season index; also the tick number used by the event log. */
  readonly season: number;
  /** 0-based index of this substep within the season. */
  readonly substep: number;
  readonly substeps: number;
}

export interface ScheduledSystem<S> {
  /** Unique within a schedule; used in error messages and traces. */
  readonly name: string;
  /** Runs on seasons where `(season - offset) % period === 0`. 1 means every season. */
  readonly period: number;
  /** In [0, period). Spreads slow systems across seasons. */
  readonly offset: number;
  /** Fixed number of `step` calls per run; never derived from state. */
  readonly substeps: number;
  readonly step: (state: S, ctx: StepContext) => void;
}

export interface Schedule<S> {
  /** Run order within a season is the array order. */
  readonly systems: readonly ScheduledSystem<S>[];
}

const assertInt = (name: string, field: string, value: number, min: number, max: number): void => {
  if (!Number.isInteger(value) || value < min || value > max) {
    throw new RangeError(`system "${name}" ${field} must be an integer in [${min}, ${max}], got ${value}`);
  }
};

const assertSeason = (name: string, value: number): void => {
  if (!Number.isInteger(value) || value < 0 || value > UINT32_MAX) {
    throw new RangeError(`${name} must be an integer in [0, 2^32-1], got ${value}`);
  }
};

/**
 * Validates and freezes a schedule.
 * @throws RangeError on a bad period, offset or substep count, or a duplicate name.
 */
export const createSchedule = <S>(systems: readonly ScheduledSystem<S>[]): Schedule<S> => {
  const names = new Set<string>();
  for (const system of systems) {
    if (names.has(system.name)) throw new RangeError(`duplicate system name "${system.name}"`);
    names.add(system.name);
    assertInt(system.name, 'period', system.period, 1, UINT32_MAX);
    assertInt(system.name, 'offset', system.offset, 0, system.period - 1);
    assertInt(system.name, 'substeps', system.substeps, 1, 1024);
  }
  return Object.freeze({ systems: Object.freeze(systems.map((s) => Object.freeze({ ...s }))) });
};

/** The systems that run in `season`, in run order. Depends only on the schedule and the season. */
export const systemsDue = <S>(schedule: Schedule<S>, season: number): readonly ScheduledSystem<S>[] => {
  assertSeason('season', season);
  return schedule.systems.filter((s) => season >= s.offset && (season - s.offset) % s.period === 0);
};

/**
 * Runs one season: every due system, in order, for its fixed number of substeps.
 * @throws RangeError if `seed` or `season` is not a uint32.
 */
export const runTick = <S>(schedule: Schedule<S>, state: S, seed: number, season: number): void => {
  assertSeason('seed', seed);
  for (const system of systemsDue(schedule, season)) {
    for (let substep = 0; substep < system.substeps; substep++) {
      system.step(state, { seed, season, substep, substeps: system.substeps });
    }
  }
};
