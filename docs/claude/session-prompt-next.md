# Next session: opening prompt

Paste this as the first message of a new chat in the Living mythos Project, or of a Claude Code cloud session on `shadepants/the-living-mythos` (better for code: it can run `pnpm check`).

---

Continue from claude/handoff-living-mythos.md (handoff #15). Spec v1.0 is approved (decision log rev 50). Start the build in spec §20 order with cloud sim work, one branch and PR per logical change, tests first:

1. Binomial sampler (spec §10) with fast-check property tests (§18): exact pmf, monotone in q, result in [0, n], u = 0 gives 0 events, fallback taken only when the cumulative sum ≤ u.
2. Command log (hard rule 6) with the §20 validation errors as unit tests.
3. Entity registry: stores the lineage parent and asserts ID uniqueness (hard rule 3).

Load the determinism-rules skill before any sim-core change and run the determinism-reviewer on each diff. Merge under the rev 43 interim rule (green Linux pnpm check + clean determinism review, commit notes "Linux-verified only") until a Windows check is available again. Update CONTEXT.md after each merge.

If the spec turns out wrong or silent while building, stop and grill it in the usual format (options table, strongest counterargument, at least two failure modes, lean, external check, exact decision-log row); spec changes need a decision-log rev and a minor version bump. After each decision, update the spec, decision log and index, re-sync the repo mirror in one docs commit, and push. Flag anything that needs the laptop. "Proceed with suggested" means take your lean. Offer a handoff refresh before the chat gets long.
