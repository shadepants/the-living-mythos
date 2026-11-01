# Whole-system review (2026-10-30)

Status: open. Prompted by Jordan during spec Q8: "Research better solutions to this issue, even if it means revising previous decisions. ... The system needs to work as a whole. It's a simulation and will need to get deeper and more complex as systems are added." Nothing here is decided; each revision is grilled one at a time (order in section 4) and lands in the decision log only when Jordan picks.

Update 2026-10-31: Gemini prompts 8-11 run and reviewed (`research/forager-reports-review-2026-10-31.md`).

Evidence: two throwaway prototypes (Python floats, never port), filed under `research/prototypes/q8-system/`. Gemini prompts 8-11 (`research/gemini-prompts.md`) cover what needs real literature.

## 1. What the prototypes showed

**Q8 band-only prototype** (one 25-person band, lumped 29-cell catchment, rev 22 fauna, `band.py`-`band4.py`):
- The band's hunting held its catchment's game at 38-64% of the unhunted level. A take cap of 1.5% of stock per season collapsed it and caused chronic hunger with no drought.
- A fixed hunt/gather labour split kept workers on depleted game and went hungry every season where rank-and-cap did not.
- Severe 8-season drought: 5-13 hungry seasons, ending 2-6 seasons after the drought. Herds took 74-107 seasons to recover, but the band compensated with plants.

**Integrated prototype** (`sysproto.py`, `run1.py`, `run2.py`): 64×24 map, rev 21 vegetation, rev 22 fauna with diffusion, an edible-plant guild, rank-and-cap foraging, a home range with a per-season camp choice, migration, binomial demography, die-out at 5.
- Run 1 (no fission): both bands grew from 25 to 32-78 people in 100 years. Background hunger appeared without any drought (0-14 hungry seasons per 200). Both bands migrated during the drought, including the one meant to be trapped, because land nobody had foraged scored higher than its own depleted range. No die-outs, even at 16 seasons; the trapped band fell to 21-37.
- Run 2 (fission above 50, homes kept apart): the land filled with 10-13 bands, and background hunger dropped to about 0-1 season per 200. The drought produced no migrations (refuges were occupied) and no die-outs.
- Conclusion (inferred, untuned parameters): the success test is decided less by the food formula than by four things together: band size dynamics, how migration scores targets, hunger mortality, and whether refuges are free.

## 2. Issues across decisions

| # | Issue | Known vs inferred | Decisions touched |
|---|---|---|---|
| I1 | Vegetation V is herbivore forage, not human food. Spec §9 gathers ΣV directly, so grass feeds people | Known from the spec text | §9, rev 21 role of V |
| I2 | No common food currency or resource interface. Each new resource (small game, fish, nuts, wild grain, crops) would need bespoke code in forage, migration scoring and events | Inferred from the spec structure | §8-§11, log "Environment fields", "Farming emergence" |
| I3 | Fixed camp plus a 29-cell disc. Real foragers move camp often: Batek camps moved when returns fell to a threshold before depletion, which fits the marginal value theorem (Venkataraman et al. 2017; verified via Dartmouth summary: 11 camps in 93 days). Binford's data range is 0-58 residential moves per year (verified, D-PLACE B013, no distribution shown). At seasonal ticks a band is roaming a home range, not sitting at one camp | Mixed; noted per claim | rev 16 catchment, §11, log band state "home range (cells)" |
| I4 | Self-depletion has no cause in the log: hunger from the band's own hunting cites nothing | Prototype-verified | rev 17 emitter, §14 |
| I5 | Bands grow without bound in the slice (no fission), reach 70+ and sit at the hunger margin, so hunger becomes background noise. Report 3 band sizes are 15-50 | Prototype; band range from report 3 | rev 9 non-goals (fission/fusion), §10 |
| I6 | Die-out is hard to reach. Drought hunger is short (plants backfill) and the trapped band shrinks but survives. Real forager famine responses may be dispersal to kin or other bands rather than starving in place | Prototype; the dispersal claim is unverified [UNCERTAIN] (prompt 8) | §12, Q11, success test wording ("died out") |
| I7 | Migration scoring on standing stock rewards any unforaged land, so bands always find somewhere. On a filled map, territory makes refuges scarce instead | Prototype | §11, Q14 scenario |
| I8 | Calibration has no anchor: food per V and F unit versus need is arbitrary, and outcomes swing on it | Prototype | §8, §9, rev 4 tuning targets |
| I9 | The rev 21 note "a lasting post-drought shortage must come from game" isn't borne out: the band doesn't feel the herd lag | Prototype | rev 21 basis text |

## 3. Candidate architecture (for grilling, not decided)

1. **Resource guilds.** Every food source implements one interface: per-cell stock in food units, a capacity derived from fields (vegetation, moisture), a regrowth rule, a per-worker return curve (Type II), a rank (post-encounter return) and a seasonal multiplier. The slice ships two guilds: large game (stock = rev 22 herds × a food-per-herd constant) and plant foods (capacity tied to V). V stays herbivore forage. Later guilds (small game, fish, nuts, wild grain, crops) plug in without touching forage, migration scoring or events. Farming becomes a guild whose stock people create, so "grain enters the diet when large-game returns fall" (log) is the same prey-choice rule.
2. **Prey-choice foraging.** Labour goes to guilds in rank order, each capped, until need plus stash top-up is met. This is the rank-and-cap option C generalised to N guilds.
3. **Home range plus seasonal camp.** The band keeps a home range (already in log band state). Each season it forages from the best camp in that range (marginal-value style); routine camp moves are snapshot state, not events. Migration is a shift of the home range itself and is the event.
4. **Band lifecycle in the slice.** Fission above a size threshold, and dissolution (survivors scatter or join neighbours) below a viability threshold or after prolonged starvation. Dissolution is how "died out" reads in the Legends.
5. **Calibration anchors.** A food unit equals one adult's needs for a season. Guild constants are set so equilibrium densities land in the ethnographic forager range and meat shares follow the latitude pattern (prompt 10). Targets: no background hunger on filled land, and drought hunger traceable to the drought.

## 4. Proposed grill order

| # | Question | Revises |
|---|---|---|
| R1 | Resource guild interface and food currency — **settled rev 23 (option B)** | spec §8 hunting, §9; Q8 |
| R2 | Home range + seasonal camp vs fixed camp; migration = home-range shift | §9 catchment use, §11 framing; rev 16 kept as the seasonal footprint |
| R3 | Band lifecycle in the slice: fission and dissolution | rev 9 non-goals, §12, Q11 |
| R4 | Calibration anchors and targets | §8-§10 tunables |
| then | Q9 demography, Q10 migration scoring, Q12 events, Q13 glance words, Q14 scenario | — |

## 5. What stays
Q0 numbers, Q1 map size (catchment kept as the seasonal footprint), Q2 event emission, Q3 worldgen, Q4 climate, Q5 drought command, Q6 vegetation response, Q7 fauna dynamics: all compose with the candidate architecture. Only the rev 21 basis note (I9) and the hunting line of rev 22 (moves into the guild interface) change wording.
