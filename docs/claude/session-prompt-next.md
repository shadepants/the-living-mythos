# Next session: opening prompt

Paste this as the first message of a new chat in the Living mythos Project (it works in a Claude Code cloud session too).

---

Continue from claude/handoff-living-mythos.md (handoff #14, updated for rev 42). First: [approve spec v1.0 / list changes]. On approval, set Version 1.0 and Status Approved with a changelog entry and a decision-log header note.

CI: the check workflow stopped on a GitHub billing issue; it is [fixed / still blocked]. If it's fixed and green on Windows, merge PR #1 (Purpose codes 6-12) and update CONTEXT.md.

Then start cloud sim work under rev 42, one branch and PR per logical change, tests first: the binomial sampler with its fast-check property tests (spec §10: exact pmf, monotone in q, never n at u = 1 − 2^-32), then the command log (hard rule 6) with the §20 validation errors, then the entity registry. Load the determinism-rules skill before sim-core changes and run the determinism-reviewer on each diff. Nothing merges into Main-REPO until pnpm check passes on Windows.

After each decision, update the spec, decision log and index, re-sync the repo mirror in one docs commit, and push. Flag anything that needs the laptop. "Proceed with suggested" means take your lean. Offer a handoff refresh before the chat gets long.
