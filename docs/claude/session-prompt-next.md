# Next planning chat: opening prompt

Paste this as the first message of a new chat in the Living mythos Project.

---

Continue from claude/handoff-living-mythos.md (handoff #11). Next: spec Q12 (event set, thresholds and causes, §14), then Q13 and Q14 in the §20 order, one at a time, same format: options table, strongest counterargument, at least two failure modes, lean, external check, exact decision-log row.

For consequential models, verify claims and run a throwaway prototype before I pick. Base: research/prototypes/q11-minviable/ (sysproto_q10.py + run5_q10.py + variants.py, `variants.apply('share', S, R)`, `S.MIN_VIABLE = 5`; q11.py has the map and island scenarios). Run on a filled map to a density plateau (1,200 years; print density per century to confirm) plus the island scenario. For Q12, check the emitter rules against real prototype event streams, not only on paper.

Q12 carry-ins: add `band_split` (daughter ID in payload); `band_died_out` `outcome` and host ID; a cause for self-inflicted depletion (I4); a cause rule for calm-time perishing (decline with no hunger event); every band outcome reaches `drought_began` in ≤ 3 hops when a drought is involved. Q14 carry-in: die-out is dissolution-led (rev 35), so the scenario needs a band cut off from migration targets but with a host. Never tune the sim for drama.

After each pick, update the spec, decision log and index, file prototype scripts, re-sync the repo mirror in one docs commit, and push. My laptop screen is still broken, so flag anything that needs the laptop. "Proceed with suggested" means take your lean. Offer a handoff refresh before the chat gets long.
