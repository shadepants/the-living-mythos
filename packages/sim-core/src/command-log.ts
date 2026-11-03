// Hard rule 6 (part one): the command log. Every nudge is a typed command stored in
// append order with a stable id, so a run can be replayed from keyframes plus this log.
// Spec §5.1, §13, §20 (decision log revs 11, 20, 39). The slice has one command type:
// the signed drought/rain command (sign −1 drought, +1 rain).

const UINT32_MAX = 0xffffffff;

export interface DroughtCommandInput {
  /** Absolute season the command takes effect (the next tick boundary or later). */
  readonly tick: number;
  /** −1 drought, +1 rain. */
  readonly sign: number;
  /** Anomaly units, scaled integer (×10,000, spec §17). */
  readonly magnitude: number;
  readonly durationSeasons: number;
  /** Row-major cell index; sea cells are valid (the disc reaches land). */
  readonly centerCell: number;
  /** Cells; 0 means the whole map. */
  readonly radius: number;
}

export interface DroughtCommand extends DroughtCommandInput {
  /** 1, 2, … in append order; event causes cite it. */
  readonly id: number;
}

/** A caller-triggerable rejection (spec §20); `field` names the offending input. */
export class CommandError extends RangeError {
  readonly field: string;

  constructor(field: string, message: string) {
    super(`command field "${field}": ${message}`);
    this.name = 'CommandError';
    this.field = field;
  }
}

export interface WorldSize {
  readonly worldWidth: number;
  readonly worldHeight: number;
}

export interface CommandLog {
  /**
   * Validates and records a command, returning the frozen stored copy.
   * `nextTick` is the first season not yet simulated; commands for earlier ticks are rejected.
   * @throws CommandError on any invalid field; the log is left unchanged.
   */
  readonly append: (input: DroughtCommandInput, nextTick: number) => DroughtCommand;
  readonly get: (id: number) => DroughtCommand | undefined;
  /** All commands in id order (a copy). */
  readonly commands: () => readonly DroughtCommand[];
  readonly size: number;
}

const requireInteger = (field: string, value: number): void => {
  if (!Number.isSafeInteger(value)) throw new CommandError(field, `must be an integer, got ${value}`);
};

const validate = (input: DroughtCommandInput, cellCount: number, minTick: number): void => {
  requireInteger('tick', input.tick);
  if (input.tick < 0 || input.tick > UINT32_MAX) throw new CommandError('tick', `must be in [0, 2^32-1], got ${input.tick}`);
  if (input.tick < minTick) {
    throw new CommandError('tick', `${input.tick} is in the past; the log is append-only in tick order (earliest allowed ${minTick})`);
  }
  requireInteger('sign', input.sign);
  if (input.sign !== -1 && input.sign !== 1) throw new CommandError('sign', `must be -1 or 1, got ${input.sign}`);
  requireInteger('magnitude', input.magnitude);
  if (input.magnitude <= 0) throw new CommandError('magnitude', `must be > 0, got ${input.magnitude}`);
  requireInteger('durationSeasons', input.durationSeasons);
  if (input.durationSeasons < 1) throw new CommandError('durationSeasons', `must be >= 1, got ${input.durationSeasons}`);
  // Seasons are uint32 in rng keys (§2), so the last active season must fit too.
  if (input.tick + input.durationSeasons - 1 > UINT32_MAX) {
    throw new CommandError('durationSeasons', `last active season ${input.tick + input.durationSeasons - 1} exceeds 2^32-1`);
  }
  requireInteger('centerCell', input.centerCell);
  if (input.centerCell < 0 || input.centerCell >= cellCount) {
    throw new CommandError('centerCell', `must be on the map [0, ${cellCount - 1}], got ${input.centerCell}`);
  }
  requireInteger('radius', input.radius);
  if (input.radius < 0) throw new CommandError('radius', `must be >= 0, got ${input.radius}`);
};

/** Creates an empty command log for a world of the given size. */
export const createCommandLog = (world: WorldSize): CommandLog => {
  const { worldWidth, worldHeight } = world;
  if (!Number.isSafeInteger(worldWidth) || worldWidth < 1 || !Number.isSafeInteger(worldHeight) || worldHeight < 1) {
    throw new RangeError(`world size must be positive integers, got ${worldWidth}×${worldHeight}`);
  }
  const cellCount = worldWidth * worldHeight;
  const stored: DroughtCommand[] = [];

  const append = (input: DroughtCommandInput, nextTick: number): DroughtCommand => {
    // A bad nextTick (NaN) would make every tick comparison false and let past commands in.
    if (!Number.isSafeInteger(nextTick) || nextTick < 0) throw new RangeError(`nextTick must be a non-negative integer, got ${nextTick}`);
    const last = stored[stored.length - 1];
    // Both readings of "past tick" (§20): before the next simulated season, or before the last command.
    const minTick = last === undefined ? nextTick : Math.max(nextTick, last.tick);
    validate(input, cellCount, minTick);
    // `+ 0` turns -0 into 0, so a live log and one reloaded from JSON compare equal.
    const command: DroughtCommand = Object.freeze({
      id: stored.length + 1,
      tick: input.tick + 0,
      sign: input.sign,
      magnitude: input.magnitude,
      durationSeasons: input.durationSeasons,
      centerCell: input.centerCell + 0,
      radius: input.radius + 0,
    });
    stored.push(command);
    return command;
  };

  return {
    append,
    get: (id) => (Number.isSafeInteger(id) && id >= 1 ? stored[id - 1] : undefined),
    commands: () => stored.slice(),
    get size() {
      return stored.length;
    },
  };
};
