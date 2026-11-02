# Spec v0.28 scoped re-audit

**Status:** Fixes applied 2026-11-02 in spec v0.29 (decision log rev 49), leans taken under "proceed with suggested". Originally opened 2026-11-02. Scoped re-audit of `design/spec_v0.1.md` v0.28 against decision log rev 48 and repo `Main-REPO` at `ce50b6b`, run from the re-audit variant in `claude/audit-prompt-spec-v1.md`. Scope: the 23 findings of `design/spec-v1-audit-2026-11-02.md`; the sections v0.28 changed; revs 45-48 against the prototypes they cite. No spec, log or repo file was edited; nothing was committed.

Auditor independence: a fresh session that had not seen the chats that wrote v0.28. It did read the handoff, as the prompt's read list requires.

## Verdict: approve with fixes

No fix reopens a decision or touches the Rejected list. Findings N4 and N5 change rev 44's acceptance fill-ins, so they need a small new rev; the rest are spec text. These three decide it:

1. **N3: a §18 property test is false on valid runs (major).** "Outcomes within drought + `causeWindow` reach its `drought_began`" fails for crowded unexposed hosts (a known risk in the log), dry-spell-only failures anywhere on the map (rev 45 makes these normal), and episodes opened before the drought.
2. **N4: acceptance never says which climate it runs in (major).** With default `volatility` > 0, natural dry spells (~15% of region-seasons) can put migrations into the control window. Every prototype control ran nudge-only (`q14run.py:40`).
3. **N2: no system writes the event-ID state (major).** The episode's `forage_failed` ID and the two lookback slots' event IDs exist only after `emit_events`, whose §5 Writes column is "events". Which camp updates the slots is also unstated.

## Status of the 23 original findings

| # | Status | Note |
|---|---|---|
| 1 grazing twice | fixed | §5 `plant_food` #5, §7, §8 agree |
| 2 dry spell from drought | fixed | §6 natural anomaly, two slots; residuals N2, N6 |
| 3 expected return E | fixed | §9 E matches `yield_at(..., 9e9, n)` at every cited line |
| 4 K = 0 | fixed | both V and P branches |
| 5 negative counts | fixed | checked: `floor(x/span + rem) ≤ x` for integer x ≥ 0, span ≥ 1, rem < 1 |
| 6 64-bit payload IDs | fixed | §14 Hi/Lo |
| 7 sampler test wording | fixed in §18; §10's new u = 0 sentence is wrong (N1) | fix introduced a problem |
| 8 perishing clause | partly fixed | spec matches the prototype; the log's rev 35 row still says "no qualifying host" (N8) |
| 9 `medianKveg` | fixed | gone from §4.1, §5.1, §17 |
| 10 labour and effort | fixed | matches `sysproto_q10.py:126` |
| 11 removal and order | fixed | proportional, band ID order |
| 12 `maxGatherFraction` | fixed | 0.5 (`yield_at`, `sysproto_q10.py:69`) |
| 13 migration units, order | fixed | |
| 14 noise keys | fixed | max key (255·4096 + 4095)·4096 + 4095 = 2^32 − 1, fits uint32 (computed) |
| 15 daughter state | fixed | `nonNegSeasons = stableSeasons` matches the prototype emitter's default (`q12lean.py:15`) |
| 16 initial world | fixed; minor residual N9 | |
| 17 acceptance executable | partly fixed | now executable; the seed proxy measures the wrong point (N5) and climate is unstated (N4) |
| 18 sea flux | fixed (deviation recorded) | |
| 19 radius 0 | fixed | |
| 20 `rV` range | fixed | |
| 21 rounding, bounds | fixed except the u = 0 claim (N1) | |
| 22 fill-ins | fixed | Sinclair tag gone; trip thresholds recorded |
| 23 error tests | fixed | |

## New findings

Severity as in the first audit: blocker = wrong behaviour or blocks the build; major = two developers would resolve it differently, or a specified test is wrong; minor = wording or tags.

| # | Sev | § | Finding | Evidence | Proposed fix | Log impact |
|---|---|---|---|---|---|---|
| N1 | major | 10, 18 | "At u = 0 with q > 0.5 the walk ... takes this fallback, giving 0 events" is false. Rounding pushes the cumulative sum past 1 before k = n, so the flip returns 1 or more | Scratch run of the §10 sampler as written: u = 0, n ≤ 200, q in (0.5, 1): nonzero result in 6,672 of 19,899 cases; 145 monotonicity-in-q violations, all at u = 0; 0 at u = 2^-32, 3·2^-32, 0.5, 1 − 2^-32. `rand01` = hash / 2^32 (`rng.ts:79`), so u = 0 is reachable, and fast-check generators favour edge values, so the §18 "monotone in q" property should hit it | Return 0 events when u = 0, before the flip; add u = 0 as a named case in the sampler tests | none |
| N2 | major | 5, 5.1, 14 | Band fields holding event IDs (open episode, drought slot, dry-spell slot) can only be filled once events exist, but §5 says only `emit_events` creates events and lists its writes as "events". `nonNegSeasons` and the pressure ring have no writer in the table either. Whether a slot reads the camp before or after migration is unstated | §5 table; §5.1 rows. Prototype updates the slot from the end-of-season camp (`q14run.py:102`, after lifecycle) and counts the current season (`q12lean.py:23-25`, `t − last ≤ WIN`, inclusive) | State that `emit_events` writes the episode ID and slot IDs into band state; forage writes `nonNegSeasons` and the ring; slots read the end-of-season camp; window inclusive | none |
| N3 | major | 18 | Property "non-`dwindled` outcomes ... within a drought + `causeWindow` reach its `drought_began`" fails on correct runs: unexposed refuge hosts that fail from crowding (log, known risk rev 36), failures inside natural dry spells elsewhere on the map (rev 45), and episodes opened before the drought | §18 property list; log Known risks, cause attribution | Scope it: every `forage_failed` whose band's drought slot is within `causeWindow` cites `drought_began`, and every non-`dwindled` outcome cites its episode's `forage_failed`. Keep "every outcome reaches a root in ≤ 3 hops" | rev 36 check wording needs the same correction |
| N4 | major | 18, 6 | Acceptance does not state `volatility`. With natural climate on, the no-drought control can show migrations or dissolutions in the window from dry spells, and a failure would invite tuning. No prototype ran natural climate (rev 45's own risk) | `q14run.py:40` (drought anomaly only); §6 "volatility = 0 ... usable for the test scenario" | Run acceptance at `volatility = 0`; report a second, non-gating run at default volatility | new rev (fill-in) |
| N5 | major | 18 | The seed's refuge check looks at a ring around the land centroid, but the drought is centred on the mean of band homes at the drought season. The check can pass with no refuge near the real drought | §18 acceptance text | Run the no-drought burn-in first, then apply the ring check around the drought centre. Still before any drought run, so not chosen by outcome (rev 38) | new rev (amends the rev 44 fill-in) |
| N6 | major | 5.1, 14 | One drought slot, but overlapping drought commands are valid (§13). Which `drought_began` the slot keeps is undefined | §5.1 drought slot; §13 stacking | Keep the most recently begun; ties by lowest command ID | none |
| N7 | major | 12 | Fission site search: "within `searchRadius`" has no metric. Migration uses a Euclidean disc (§11); the prototype's fission search is a square (no disc test) | `q14run.py:84-87`, `run5_q10.py:38-41` | Pick Euclidean (consistent with §11) and note the deviation, or record the square | none |
| N8 | minor | 12; log | Rev 44 says no decision reversed, but §12.2 ends any band under `minViable` that did not migrate, including hungry bands at 1-2 seasons that never had a host check. Rev 35's row still says "no qualifying host and no migration target". The spec matches the prototype | `sysproto_q10.py:149` (prototype ends every band under 5) | Add a "[Rev 44 correction]" note to the rev 35 row | log note |
| N9 | minor | 4.1 | Starting bands get daughter state, but "lookback slots copied from the parent" has no parent (mean empty). Both bands land at least `homeRange` (5) apart on the best land, so their catchments overlap; the prototype placed them 24 cells apart. Fill time effect unmeasured [UNCERTAIN] | `q14run.py:17` | Say slots start empty; batch-check fill time | none |
| N10 | minor | 18 | Grazing test says "V's drop over a season equals the grazing removed"; vegetation growth runs in the same season | §5 order | Measure across `large_fauna` only | none |
| N11 | minor | header, 2 | "Code facts checked 2026-11-01 ... `Purpose` codes 1-5" is stale. Codes 1-12 exist. The handoff §8 says the same | `rng.ts:9-27`; `CONTEXT.md:11` | Update the date and code range | none |
| N12 | minor | 17, 18 | Rev 47's check "a raw 64-bit value rejected" is missing from §18. `refugeMinCells` is missing from §17's test-scenario list | rev 47 row; §17 last line | Add both | none |
| N13 | minor | 7, 9 | Implicit: game removal in F units (`take / foodPerHerd`); whether `vegSeed` is tested before or after the V update | §7, §9 | One clause each | none |
| N14 | minor | 5 | Same-tick causes rely on record order: forage must write `balance_turned_negative` before `hunger_changed` so `forage_failed` precedes `band_hunger_began` | §5 emitter text | State the record order | none |

## Changed-section checks with no finding

- Determinism: every new formula (E, allocation, removal, aging, fade) uses + − × ÷ only; ties stated for camp, migration, host, fission site and starting placement; payload IDs integer.
- Edge cases: K = 0, region with no land cells, two bands choosing one cell and radius 0 are now defined. Zero people at forage cannot happen, by construction: lifecycle ends bands under 5 before the next forage (inferred from the run order). Zero labour at migration is defined (share guard). Overlapping droughts in the lookback: undefined (N6).
- Revs 45-48 options and leans: no error of fact found against the cited prototype lines (table below).

## Evidence check

| Claim | Source | Result |
|---|---|---|
| Rev 46: host guard, fission, migration share and camp scoring use an uncapped return | `run5_q10.py:9-12`, `:36-44`; `variants.py:31`; `sysproto_q10.py:105-115` | verified |
| Rev 48: prototype V = 0.83K, F = 0.2 where K > 0.5, c = 0.85 | `sysproto_q10.py:44` | verified |
| Rev 48: mix 8 : 4 : 9 : 4 per 25 | `sysproto_q10.py:167` | verified |
| Rev 48: daughters started with stash 0; parent kept its stash | `q14run.py:91-92`; `Band` init | verified |
| Rev 48: `nonNegSeasons` must start at `stableSeasons` | `q12lean.py:15` (emitter defaults every band to `STABLE`) | verified (spec now matches the prototype) |
| Rev 47: payload fields must be safe integers | `event-log.ts:92-101` | verified |
| Rev 44: effort × C/target; take/n floored; start-of-season sums; clamp at 0; strict > camp margin | `sysproto_q10.py:126`, `:122`, `:97`, `:145`, `:115` | verified |
| Herds settle in 37-173 seasons (K 0.6 never) | `finalize-anchor/results.txt:2-7` | verified |
| Q14 5/6 pass, fail seed 1 at 0.9 | `q14-scenario/results_map.txt` | verified |
| Rev 45: no prototype ran natural dry spells | `q14run.py:40` | verified for Q14; other prototype folders not checked |
| `Purpose` 1-12 in code | `rng.ts:9-27` | verified |
| 67 tests + 1 todo | `CONTEXT.md:19` | unverified (`pnpm check` not run) |

## External checks for majors

- N1: a fast-check property over (n, q, u) with u drawn from the `rand01` grid including 0.
- N2, N6: a second developer implementing `emit_events` from §5 and §14 cold.
- N3: rerun `q14chain.py` with the narrowed property on the six Q14 streams; it must pass, and the old wording must be shown to fail on a stream with natural climate.
- N4: rerun `q14run.py` with volatility > 0 and count control-window outcomes.
- N5: on 20 procedural seeds, distance between the land centroid and the band-home centroid at year 1,200.
- N7: a fission-rate batch run, square vs disc search.

## Not checked, and why

- Prototype reruns: the session's permission check blocked running repo scripts, so no prototype was rerun (the first audit reran `finalize-anchor/`). The sampler checks above ran in a scratch script written from §10, not repo code.
- `pnpm check`: not run, same reason. Windows: no check available (rev 43).
- Sections v0.28 did not change (§1-§3, §16, §19, §21, §22), beyond the stale code claim in the header.
- Every §17 value against the log: sampled, not exhaustive.
- Gemini PDFs: out of scope.
