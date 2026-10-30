import { describe, expect, it } from 'vitest';
import { createSchedule, runTick, systemsDue, type ScheduledSystem } from '../src/index.ts';

interface ToyState {
  readonly trace: string[];
  value: number;
}

const tracing = (name: string, period: number, offset: number, substeps: number): ScheduledSystem<ToyState> => ({
  name,
  period,
  offset,
  substeps,
  step: (state, ctx) => {
    state.trace.push(`${ctx.season}:${name}:${ctx.substep}/${ctx.substeps}`);
    // Integer-only update that depends on state, so replays can be compared by value.
    state.value = (state.value * 31 + ctx.season + ctx.substep) % 1000003;
  },
});

const toySchedule = createSchedule<ToyState>([
  tracing('vegetation', 1, 0, 3),
  tracing('fauna', 1, 0, 2),
  tracing('soil', 4, 1, 1),
]);

const run = (initial: number, seasons: number): ToyState => {
  const state: ToyState = { trace: [], value: initial };
  for (let season = 0; season < seasons; season++) runTick(toySchedule, state, 42, season);
  return state;
};

describe('tick loop with fixed substeps (hard rule 4)', () => {
  it('runs due systems in declared order, each for its fixed substep count', () => {
    const state: ToyState = { trace: [], value: 0 };
    runTick(toySchedule, state, 42, 1);
    expect(state.trace).toEqual([
      '1:vegetation:0/3',
      '1:vegetation:1/3',
      '1:vegetation:2/3',
      '1:fauna:0/2',
      '1:fauna:1/2',
      '1:soil:0/1',
    ]);
  });

  it('runs slow systems on a fixed period and offset', () => {
    const due = (season: number): string[] => systemsDue(toySchedule, season).map((s) => s.name);
    expect(due(0)).toEqual(['vegetation', 'fauna']);
    expect(due(1)).toEqual(['vegetation', 'fauna', 'soil']);
    expect(due(4)).toEqual(['vegetation', 'fauna']);
    expect(due(5)).toEqual(['vegetation', 'fauna', 'soil']);
    expect(due(9)).toEqual(['vegetation', 'fauna', 'soil']);
  });

  it('visits the same steps whatever the state is', () => {
    const a = run(0, 40);
    const b = run(999, 40);
    expect(b.trace).toEqual(a.trace);
    expect(b.value).not.toBe(a.value);
  });

  it('replays to an identical state', () => {
    const a = run(7, 200);
    const b = run(7, 200);
    expect(b.value).toBe(a.value);
    expect(b.trace).toEqual(a.trace);
  });

  it('passes the seed and season through to every step', () => {
    const seen: [number, number][] = [];
    const schedule = createSchedule<null>([
      { name: 'probe', period: 1, offset: 0, substeps: 1, step: (_s, ctx) => seen.push([ctx.seed, ctx.season]) },
    ]);
    runTick(schedule, null, 7, 12);
    expect(seen).toEqual([[7, 12]]);
  });

  it('cannot be changed after creation', () => {
    const systems = [tracing('vegetation', 1, 0, 3)];
    const schedule = createSchedule(systems);
    systems.push(tracing('late', 1, 0, 1));
    expect(schedule.systems.map((s) => s.name)).toEqual(['vegetation']);
    expect(Object.isFrozen(schedule.systems)).toBe(true);
    expect(Object.isFrozen(schedule.systems[0])).toBe(true);
  });

  it('rejects invalid schedules', () => {
    expect(() => createSchedule([tracing('a', 0, 0, 1)])).toThrow(RangeError);
    expect(() => createSchedule([tracing('a', 1.5, 0, 1)])).toThrow(RangeError);
    expect(() => createSchedule([tracing('a', 4, 4, 1)])).toThrow(RangeError);
    expect(() => createSchedule([tracing('a', 4, -1, 1)])).toThrow(RangeError);
    expect(() => createSchedule([tracing('a', 1, 0, 0)])).toThrow(RangeError);
    expect(() => createSchedule([tracing('a', 1, 0, 2.5)])).toThrow(RangeError);
    expect(() => createSchedule([tracing('a', 1, 0, 1), tracing('a', 2, 0, 1)])).toThrow(RangeError);
  });

  it('rejects seeds and seasons that are not uint32', () => {
    const state: ToyState = { trace: [], value: 0 };
    expect(() => runTick(toySchedule, state, -1, 0)).toThrow(RangeError);
    expect(() => runTick(toySchedule, state, 42, 1.5)).toThrow(RangeError);
    expect(() => runTick(toySchedule, state, 42, 2 ** 32)).toThrow(RangeError);
    expect(state.trace).toEqual([]);
  });
});
