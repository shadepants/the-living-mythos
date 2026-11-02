# Next session: opening prompt

Paste this as the first message of a new chat in the Living mythos Project (it works in a Claude Code cloud session too).

---

Continue from claude/handoff-living-mythos.md (handoff #14, updated for rev 43). I ran claude/audit-prompt-spec-v1.md in a fresh session: [paste the audit report / "audit skipped"]. Turn its blockers and majors into spec fixes and decision-log revisions, one at a time in the usual grill format. Then: [approve spec v1.0 / list changes]. On approval, set Version 1.0 and Status Approved with a changelog entry and a decision-log header note.

Then continue cloud sim work, one branch and PR per logical change, tests first: the binomial sampler with its fast-check property tests (spec §10: exact pmf, monotone in q, never n at u = 1 − 2^-32), then the command log (hard rule 6) with the §20 validation errors, then the entity registry. Load the determinism-rules skill before sim-core changes and run the determinism-reviewer on each diff. Merge under the rev 43 interim rule (green Linux pnpm check + clean determinism review, commit notes "Linux-verified only") until a Windows check is available again.

After each decision, update the spec, decision log and index, re-sync the repo mirror in one docs commit, and push. Flag anything that needs the laptop. "Proceed with suggested" means take your lean. Offer a handoff refresh before the chat gets long.
