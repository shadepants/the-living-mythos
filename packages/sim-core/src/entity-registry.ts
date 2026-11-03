// Hard rule 3 (completion): the lineage id does not encode its parent, so the registry
// stores it and asserts uniqueness on registration (spec §5.1, §12, §20; decision log rev 12).
// The registry derives each id itself from (parent, birth tick, sibling index), so a stored
// parent can never disagree with its id. Records are never removed: ended bands stay as
// history records (§12).

import { ROOT_ID, deriveEntityId, isEntityId, type EntityId } from './lineage.ts';

export interface EntityRecord {
  readonly id: EntityId;
  /** `ROOT_ID` for founders. */
  readonly parent: EntityId;
  /** Absolute season of founding (for a band: the fission season). */
  readonly birthTick: number;
  /** Index among the parent's children born that season. */
  readonly siblingIndex: number;
}

export interface EntityRegistry {
  /**
   * Derives the id for (parent, birthTick, siblingIndex), records it and returns the frozen record.
   * @throws RangeError if the id is already registered, the parent is neither `ROOT_ID` nor
   *   registered, the birth tick precedes the parent's, or an input is malformed. The registry
   *   is left unchanged. All of these are impossible by construction in a correct sim (§20).
   */
  readonly register: (parent: EntityId, birthTick: number, siblingIndex: number) => EntityRecord;
  readonly get: (id: EntityId) => EntityRecord | undefined;
  readonly has: (id: EntityId) => boolean;
  /** All records in registration order (a copy). */
  readonly records: () => readonly EntityRecord[];
  readonly size: number;
}

/** Creates an empty entity registry. */
export const createEntityRegistry = (): EntityRegistry => {
  // Map keeps insertion order, which follows the deterministic registration sequence.
  const byId = new Map<EntityId, EntityRecord>();

  const register = (parent: EntityId, birthTick: number, siblingIndex: number): EntityRecord => {
    if (!isEntityId(parent)) throw new RangeError(`parent must be a well-formed entity id, got "${parent}"`);
    const parentRecord = byId.get(parent);
    if (parent !== ROOT_ID && parentRecord === undefined) {
      throw new RangeError(`parent ${parent} is not registered`);
    }
    if (parentRecord !== undefined && birthTick < parentRecord.birthTick) {
      throw new RangeError(`birth tick ${birthTick} precedes parent ${parent} birth tick ${parentRecord.birthTick}`);
    }
    // deriveEntityId validates birthTick and siblingIndex as uint32.
    const id = deriveEntityId(parent, birthTick, siblingIndex);
    if (id === ROOT_ID) throw new RangeError('derived id collides with ROOT_ID');
    if (byId.has(id)) {
      throw new RangeError(`entity ${id} is already registered (parent ${parent}, tick ${birthTick}, sibling ${siblingIndex})`);
    }
    // `+ 0` stores -0 as 0, as in the command log, so reloaded records compare equal.
    const record: EntityRecord = Object.freeze({ id, parent, birthTick: birthTick + 0, siblingIndex: siblingIndex + 0 });
    byId.set(id, record);
    return record;
  };

  return {
    register,
    get: (id) => byId.get(id),
    has: (id) => byId.has(id),
    records: () => [...byId.values()],
    get size() {
      return byId.size;
    },
  };
};
