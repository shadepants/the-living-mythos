# Next planning chat: opening prompt

Paste this as the first message of a new chat in the Living mythos Project.

---

Continue from claude/handoff-living-mythos.md (handoff #12). Next: review the prompt 12 report (Project file `Hunter-Gatherer Band Famine Dynamics.pdf`): spot-check its key claims, say which you verified, corrected, found conflicting or left unverified, write the review to research/, and flag anything it changes for revs 25, 26, 33, 35 or 36. Then grill spec Q14 (test scenario and pass sentence, §15 and §18), the last open question, in the same format: options table, strongest counterargument, at least two failure modes, lean, external check, exact decision-log row.

For Q14, run a throwaway prototype before I pick. Base: research/prototypes/q12-events/ (sysproto_q10.py + run5_q10.py + variants.py + q9b_modes.py; q12run.py dumps per-season facts; q12lean.py is the rev 36 emitter) and research/prototypes/q13-glance/ (q13glance.py, variant `effort` = rev 37). Run on a filled map to a density plateau (1,200 years; print density per century to confirm) plus the island scenario. Show the pass sentence rendered from a real event chain, not only on paper.

Q14 carry-ins: die-out is dissolution-led (rev 35), so the scenario needs one band with a migration target and one cut off from targets but with a host outside the drought. A 2-band island fails because both bands go hungry together. Never tune the sim for drama.

After the pick, update the spec, decision log and index, file prototype scripts, re-sync the repo mirror in one docs commit, and push. Then offer spec finalize (spec-developer Phase 3), including the §9 band-card food trend fix. My laptop screen is still broken, so flag anything that needs the laptop. "Proceed with suggested" means take your lean. Offer a handoff refresh before the chat gets long.
