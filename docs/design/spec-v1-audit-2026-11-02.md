# Spec v1.0 candidate audit (v0.27)

**Status:** Open, 2026-11-02. Independent audit of `design/spec_v0.1.md` v0.27, the v1.0 candidate, run from `claude/audit-prompt-spec-v1.md` against decision log rev 42 and repo `Main-REPO` at `c82dbf9`. No file was edited and nothing was committed during the audit. Findings feed spec v0.28 and any new decision-log revs listed below.

## Verdict: do not approve v0.27 as written

None of the fixes reopens a decision. Most are spec text; four need a small new rev (findings 2, 3, 6, 15-16). These three findings decide it:

1. **Grazing is subtracted twice (blocker).** §8 removes grazing from V inside each fauna substep. §7 and the §5 table then subtract "last season's grazing" again. The prototype does it once.
2. **A drought can be cited through a dry spell (blocker).** The region dry-spell mean uses the anomaly after droughts are subtracted, so a drought can start a dry spell. The lookback keeps only one event ID, so `forage_failed` may cite `dry_spell_began`, which has no cause, and the chain to `drought_began` breaks. Every prototype ran with drought only (`q14-scenario/q14run.py:40`), so this is untested.
3. **"Expected catchment return" is never defined (blocker).** Camp choice, migration, the host guard and fission all use it. §9's allocation stops at need, so a capped reading makes the ×(1 + margin) guards almost impossible to pass. The prototype uses an uncapped return (target 9e9), with no share discount for hosts and fission.

## Findings

Severity: blocker = wrong behaviour or blocks the build; major = ambiguity two developers would resolve differently; minor = wording or tags.

| # | Sev | § | Finding | Evidence | Proposed fix | Log impact |
|---|---|---|---|---|---|---|
| 1 | blocker | 5, 7, 8 | Grazing subtracted twice; P built before grazing | `sysproto_q10.py:50-62`: V −= removal per substep, then P from post-grazing V | Drop the §7 subtraction; compute P after fauna | none |
| 2 | blocker | 6, 14 | Drought can start a dry spell; single-ID lookback can lose the drought | §6 region mean uses anomaly; §5.1 stores one event ID | Dry spells read the natural anomaly only, or the lookback prefers droughts | new rev |
| 3 | blocker | 9, 11, 12 | Expected return undefined (capped or not; share or not; whose labour) | `variants.py:31`, `run5_q10.py:67` | Define it: uncapped, own labour, share only in migration | new rev |
| 4 | blocker | 7 | K = 0 or Pcap = 0 gives 0/0 = NaN | scratch run returned NaN; prototype guards with `max(K,1e-9)` | Guard: V' = min(V, K) when K = 0 (same for P) | none |
| 5 | blocker | 10, 20 | Aging and deaths both use start counts, so counts can go negative; §20 calls that impossible | scratch: child 1 − 1 death − 1 aged = −1; prototype clamps (`sysproto_q10.py:146`) | State the order and clamp, or cap deaths | none |
| 6 | blocker | 14 | Host ID and daughter ID are 64-bit; payload fields must be safe integers | `event-log.ts` freezePayload; `lineage.ts` 16-hex IDs | Split each ID into Hi/Lo uint32 fields | new rev (fill-in) |
| 7 | major | 18 | "Never n at u = 1 − 2^-32" is false: n is a valid draw whenever P(n) > 2^-32 | scratch: Bin(5, 0.0475) returns 5; any q > 0.5 returns n | Test "fallback taken only when cum ≤ u" | none (rev 31 check wording) |
| 8 | major | 12 | Perishing drops rev 35's "and no migration target"; unclear whether calm bands under 5 count as having "no qualifying host" | rev 35 row | Restore the clause; say that calm bands under 5 end | none |
| 9 | major | 4.1, 5.1, 17 | `medianKveg` "return anchor input" is left over from rev 28. Rev 41 rejected per-world scaling, and no sim system reads it | §4.1 last bullet | Move it to the calibration tool and batch test | none |
| 10 | major | 9 | "Using labour need_left/return" is wrong when the cap binds; effort is split across stash top-up without a rule | prototype: labour = taken/return; effort × C/target (`sysproto_q10.py:126`) | Copy the prototype rule | none |
| 11 | major | 9 | Even split of removal can push a cell below 0; forage order across overlapping catchments unstated | prototype floors at 0 per cell (leaks food) and runs bands in order | Proportional split; sequential in band ID order | none |
| 12 | major | 9, 17 | `maxGatherFraction` "prototype uncapped" is wrong | `yield_at`: `Pm*ncell*0.5` | 0.5 | none |
| 13 | major | 11 | Units of score and `travelCost` unstated (prototype: whole-band food, so 0.05/cell is small); whether bands see earlier migrations this season unstated | `variants.py:39` | State units; sequential update | none |
| 14 | major | 4.1, 6 | Noise keys: octaves share one Purpose and index scheme (correlated octaves); 3D climate lattice index encoding unstated | §4.1, §6 | Add octave to the index; define the encoding | none |
| 15 | major | 5.1, 12 | Daughter state undefined (stash, counters, remainders, ring, `nonNegSeasons`). Starting `nonNegSeasons` = 0 allows a hunger event with no `forage_failed` | §12.3 | Define initial values | new rev (fill-ins) |
| 16 | major | 4, 9 | Season-0 V, P, F, c and starting band placement and bracket mix undefined; calibration depends on them | prototype: V = 0.83K, F = 0.2 where K > 0.5, c = 0.85 | Specify | same rev as 15 |
| 17 | major | 18 | Acceptance not executable: "rev 16 refuge check" has no operational definition; centroid of what (homes or camps, weighted or not) | §18 | Define both | none |
| 18 | minor | 8 | Sea is zero-flux here; prototype lets herds diffuse into sea and edges are padded; prototype's "land" is Kveg > 0.05 | `sysproto_q10.py:58`, `:99` | Note the deviation or align | none |
| 19 | minor | 13 | Radius 0 = whole map, but the fade formula divides by radius | §13 | Explicit branch | none |
| 20 | minor | 7, 17 | "Logistic never above K" holds only for rV ≤ 1 (1.2 gives 1.008K) | scratch | Range check at config load | none |
| 21 | minor | 10 | Births `round` mode unstated; "n ≤ ~60" and "fallback unreachable" claims inaccurate (n can exceed 60; u = 0 at q > 0.5 hits the fallback, harmlessly) | scratch | Half away from zero; restate the bound (underflow ~n > 1,074) | none |
| 22 | minor | 9, 16, 17 | Unrecorded fill-ins: `vegSeed` (not in prototype), `tripGood/PoorPct`, "[R: Sinclair 2003]"; camp margin ">" vs log "at least" | — | Record or retag | rev 39-style note |
| 23 | minor | 18 | No tests for §20 command and config errors (rev 39 check) | §18 | Add | none |

## Edge cases

| Case | Status |
|---|---|
| Zero labour | Defined (rev 35 share guard) |
| Zero people | Defined only by inference (bands under 5 end in lifecycle before forage) |
| Zero stock | Defined |
| K = 0 | Wrong (finding 4) |
| Sea and map-edge cells | Partly defined; deviates from prototype (finding 18) |
| Empty catchment | Not reachable (camp is land) |
| Region with no land cells | Undefined (0/0 region mean) |
| Migrate and qualify for dissolution same season | Defined (rev 39) |
| Host ends or splits the season it receives refugees | Defined by run order (host can split; cannot dissolve) |
| Daughter founded on a migration target | Defined (spacing sees new homes) |
| Two bands picking the same cell | Undefined (finding 13) |
| Episode open when a band ends | Defined |
| Drought command on a sea centre | Defined (valid) |
| Radius 0 | Wrong (finding 19) |
| Overlapping commands | Defined (stack in command ID order) |

## Determinism

Ties are explicit everywhere checked (camp, migration target, host, fission site, sea level, landmass, emitter order). Formulas use only + − × ÷, sqrt, and ceil on config values. Payload rounding is stated (half away from zero). Gaps: findings 11, 13 and 14.

## Buildability: left implicit

Season names and which season is index 0; band names; `cellKm` location (presentation, not config); `seasonal[4]` values; reference seeds for the calibration tool; expected catchment return (finding 3); initial fields and band placement (finding 16); command ID assignment; median for an even count; noise output normalisation; Legends year = floor(season / 4) (inferred).

## Evidence check

| Claim | Source | Result |
|---|---|---|
| Q14 5/6 pass, fail s1 mag 0.9 | `q14-scenario/results_map.txt` | verified |
| Controls 0 outcomes 3/3 | `q14-scenario/results_controls.txt` | verified |
| Ash sentence, 10%, 42 km | `q14-scenario/results_controls.txt:8` | verified |
| Trend 36/36, 99.8% steady, flicker 0.01, median lead 4 | `finalize-trend/results_map.txt` | verified |
| F/K 0.02-0.12; effort 1.00 / 0.75 / 0.50 / 0.38 / 0.33; scale 1.49 / 0.76 / 0.68 | `finalize-anchor/results.txt`; rerun output identical | verified (F/K low end is 0.017) |
| Return constants 5.25 / 0.10 / 2.7 / 1.5 | `sysproto_q10.py:17-18` × 1.5 | verified |
| 31 migrations, 8 dissolutions; causeless 15 → 4 → 2 | `q12-events/results_lookback_map.txt` | verified |
| Glance flicker 0.06 (0.02 with hysteresis); restless 120 | `q13-glance` results (80 map + 40 island) | count verified; subset claim unverified |
| Floor 5: 1/5 at 0.1 and 0.05, 5/5 at 0 | `q11-minviable/results_island_floor5.txt` | verified |
| Gather "uncapped" | `yield_at` | corrected (0.5) |
| l15 0.57, TFR 5.7 | Gurven & Kaplan 2007 | unverified this audit (abstract only) |
| 67 pass + 1 todo; Purpose 1-5 | `vitest run` on Linux; `rng.ts` | verified (Linux, not Windows) |

Math checked in scratch scripts: binomial sampler (0 monotonicity violations in 20,000 checks; total-variation distance ≤ 2.9e-5 on a 200k u-grid; underflow only past n ≈ 1,074 at 1 − q = 0.5); diffusion stability (stable at h·D = 0.25, unstable at 0.26; n_f = 2 at prototype values); fade profile (1 at r/2, 0.5 at 0.75r, 0 at r); logistic bound; Type II forms equal.

## External checks for blockers and majors

- 1: single-cell unit test, grazing total vs V drop.
- 2: rerun `q14run.py` with volatility > 0 and count `forage_failed` whose only cause is `dry_spell_began`.
- 3, 10, 11: diff the TS forage function against `yield_at` on a fixture.
- 5, 15: property tests that bracket counts never go negative and every hunger event cites a `forage_failed`.
- 6: append a 64-bit ID payload to the event log and confirm it throws.
- Others: a second developer reading the spec cold.

## Not checked, and why

- Cross-engine state hash: no field code exists.
- Every §17 number against the log: about 20 sampled, not all.
- Prototypes other than `finalize-anchor/` were not rerun.
- Gurven & Kaplan figures: full paper not read.
- Windows `pnpm check`: CI blocked by the billing issue.
- Gemini PDFs: out of scope.

Source consulted: [Gurven & Kaplan 2007 abstract (HRAF)](https://hraf.yale.edu/ehc/documents/1294)
