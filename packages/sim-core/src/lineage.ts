// Hard rule 3: entity ids are derived from lineage (parent, birth season, sibling
// index), never from a global counter. The same history therefore yields the same
// ids in a replay or a fork, whatever order other entities were created in.
//
// An id is 64 bits (two independent 32-bit hash chains) written as 16 hex chars.
// 32 bits would collide after roughly 77k entities; 64 bits makes that negligible.
// The id does not encode the parent: the entity record and event log store it.

import { mix32 } from './rng.ts';

const UINT32_MAX = 0xffffffff;
const ID_PATTERN = /^[0-9a-f]{16}$/;

/** Branded string: a plain string will not typecheck where an EntityId is required. */
export type EntityId = string & { readonly __brand: 'EntityId' };

/** Parent of every founder. Not itself an entity. */
export const ROOT_ID = '0000000000000000' as EntityId;

const assertUint32 = (name: string, value: number): void => {
  if (!Number.isInteger(value) || value < 0 || value > UINT32_MAX) {
    throw new RangeError(`lineage field "${name}" must be an integer in [0, 2^32-1], got ${value}`);
  }
};

/** True when `value` is a well-formed entity id (shape only; says nothing about existence). */
export const isEntityId = (value: string): value is EntityId => ID_PATTERN.test(value);

const toHex32 = (value: number): string => value.toString(16).padStart(8, '0');

const splitId = (id: string): { high: number; low: number } => {
  if (!ID_PATTERN.test(id)) {
    throw new RangeError(`entity id must be 16 lowercase hex characters, got "${id}"`);
  }
  return { high: parseInt(id.slice(0, 8), 16), low: parseInt(id.slice(8), 16) };
};

/**
 * Id of the entity born to `parent` in `birthSeason`, as sibling number `siblingIndex`
 * among that parent's children born that season (twins get 0 and 1).
 * @throws RangeError if the parent id is malformed or a number is outside uint32.
 */
export const deriveEntityId = (parent: EntityId, birthSeason: number, siblingIndex: number): EntityId => {
  assertUint32('birthSeason', birthSeason);
  assertUint32('siblingIndex', siblingIndex);
  const { high, low } = splitId(parent);

  // Two chains with different salts and field orders, so the halves are independent.
  let a = mix32(high ^ 0x9e3779b9);
  a = mix32(a ^ low ^ 0x85ebca6b);
  a = mix32(a ^ birthSeason ^ 0xc2b2ae35);
  a = mix32(a ^ siblingIndex ^ 0x27d4eb2f);

  let b = mix32(siblingIndex ^ 0x165667b1);
  b = mix32(b ^ birthSeason ^ 0xd3a2646c);
  b = mix32(b ^ low ^ 0xfd7046c5);
  b = mix32(b ^ high ^ 0xb55a4f09);

  return (toHex32(a) + toHex32(b)) as EntityId;
};

/** The `index`-th founder of the world (born at season 0). */
export const founderId = (index: number): EntityId => deriveEntityId(ROOT_ID, 0, index);

/** First 32 bits of an id, for the `entity` field of an `RngKey`. */
export const entityKey = (id: EntityId): number => splitId(id).high;
