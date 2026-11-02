# Spec v1.0 audit: opening prompt

Paste the text below as the first message of a **new** session, so the auditor has not seen the chats that wrote the spec. Best place: a Claude Code cloud session on `shadepants/the-living-mythos` (it can rerun the Python prototypes and `pnpm check`). A new chat in the Living mythos Project also works, minus the reruns. In the Project, the paths below are the same without the leading `docs/`.

---

You are an independent auditor. Audit the proposed v1.0 of the Living mythos slice spec before I approve it. You did not write it; don't trust its changelog, decision trace or the handoff's summary of what was checked. Read the sources and verify for yourself. Do not edit any file and do not commit. Your output is a report.

**Read first, in this order:** `docs/claude/README.md`, `docs/design/decision-log.md` (rev 42; the source of truth, and its Rejected list is closed), `docs/design/spec_v0.1.md` (v0.27 = the v1.0 candidate), `docs/claude/handoff-living-mythos.md` (§5 corrections log: past mistakes to look for again), `CLAUDE.md` and `CONTEXT.md` (code state), and `packages/sim-core/src/` (built code the spec must match). Evidence: `docs/research/prototypes/*/README.md` and their `results_*.txt`; research reviews in `docs/research/*-review-*.md`.

**What to audit (cover every section, §1-§22):**
1. **Traceability.** Every spec rule, number and tag against the decision log row it comes from (revs 9-42). Flag contradictions `[CONFLICT]`, spec rules with no decision behind them (unrecorded fill-ins), decided items missing from the spec, and anything from the Rejected list that crept back.
2. **Internal consistency.** Same name, meaning and units everywhere. The §5 run order against what each system reads and writes (nothing reads a value before it is written that season, unless the spec says it is last season's). Every tunable used in a formula appears in §17, and every §17 field is used somewhere. Every §5.1 state field is written and read by someone. Event causes match the §14 table, at most 3, and outcomes reach `drought_began` in ≤ 3 hops.
3. **Determinism (hard rules 1-7).** Every formula uses only `+ − × ÷` and `sqrt`; every draw has a full key and its own `Purpose` code; sums have a stated order; substep counts and schedules never depend on state; config and payloads are integers with a stated scale and rounding; ties are broken explicitly everywhere a choice is made (camp, migration target, host, fission site, sort orders).
4. **Math.** Check each formula by hand or in a scratch script, not by reading: binomial inverse-CDF sampler (incl. the q > 0.5 flip with 1 − u and the underflow claim), Type II return in both forms, herd model and the `n_f` stability bound, drought fade profile, vegetation die-back and logistic branches, plant stock P, effort, shortfall, stash update, hunger counter, food-trend pressure, `stockPct`, aging remainder, fission halving.
5. **Edge cases and ordering.** Zero people, zero labour, zero stock, `K = 0`, sea and map-edge cells, empty catchments, a band that migrates and qualifies for dissolution the same season, a host that ends or splits the season it receives refugees, a daughter founded on a migration target, two bands picking the same cell, an episode open when a band ends, a drought command on a sea centre, radius 0, overlapping commands. Say for each: defined / undefined / wrong.
6. **Buildability.** Could a developer implement each system from the spec alone? List everything left implicit (e.g. season names, band names, `cellKm`, `seasonal[4]` values, reference seeds for the calibration tool, what "expected catchment return" includes).
7. **Testability.** Every MUST / MUST NOT has a test in §18; the acceptance test is executable as written (seed choice, centroid rule, window bounds, control run); slow tests are tagged.
8. **Evidence.** Spot-check at least 8 prototype or research figures that the spec or log cites (e.g. 5/6 pass rate, 36/36 warned onsets, F/K 0.02-0.12, l15 0.57, TFR 5.7) against the results files or sources. Rerun at least one prototype if you can (`finalize-trend/` or `finalize-anchor/`; the README says which base files to copy alongside). Mark each as verified, corrected, conflicting or unverified.
9. **Scope and guardrails.** Anything beyond the success-test slice (rev 9; judge against "I trigger a drought and can read in the Legends why one band migrated and another died out"). Anything that tunes the sim for drama (rev 35, rev 38). Earth-timeline anchoring.
10. **Code agreement.** Spec claims about built code (`rng.ts` purposes, `tick.ts`, `event-log.ts`, `config.ts`, test counts) match the repo as it is.

**Report format (mobile-length per finding):**
- Verdict first: approve / approve with fixes / do not approve, with the 3 findings that decide it.
- Findings table: # | severity (blocker = would produce wrong behaviour or block the build; major = ambiguity two developers would resolve differently; minor = wording or tags) | spec § | finding | evidence (quote or file:line) | proposed fix | decision-log impact (none / new rev needed).
- Evidence check table: claim | source | verified / corrected / conflicting / unverified.
- What you did not check, and why.

**Rules:** Separate what you verified from what you infer, in the sentence. Use `[NEED: ]`, `[BLOCKED: ]`, `[UNCERTAIN: ]` only where the gap could change a finding. Do not reopen anything on the Rejected list; you may flag that a rejected item reappears. Do not propose new features. No emoji, no time estimates. For each blocker or major, name the external check that would settle it.

---

## Re-audit variant (spec v0.28)

Use the same prompt in a new session, replacing its first paragraph's scope with this:

> This is a scoped re-audit. The first audit (`docs/design/spec-v1-audit-2026-11-02.md`, against v0.27) found 23 issues; spec v0.28 (decision log revs 44-48) claims to fix all of them. Check (1) each of the 23 findings: fixed / partly fixed / not fixed / fix introduced a new problem; (2) every section v0.28 changed (§4.1, §5, §5.1, §6, §7, §8, §9, §10, §11, §12, §13, §14, §15, §17, §18, §20) for new contradictions with the decision log and with untouched sections; (3) revs 45-48's options and leans for errors of fact against the prototypes they cite. Same report format, same rules; keep areas 1-10 of the full audit for the changed sections only.
