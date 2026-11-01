# Review: Gemini prompts 8-11 (2026-10-31)

Status: reviewed. Directions adopted as grilling input for the whole-system review (`design/integration-review-2026-10-30.md`, R1-R4); numbers stay [P] unless marked verified. Prompt 10 added the same day (section 3).

Reports (text extracted from Jordan's PDFs; PDFs in the repo mirror `docs/research/`):
- Prompt 8: `research/forager-famine-report-gemini.txt` ("Drought and Famine Responses in Mobile Hunter-Gatherer Societies")
- Prompt 9: `research/food-storage-report-gemini.txt` ("Hunter-Gatherer Food Storage")
- Prompt 11: `research/food-system-architecture-report-gemini.txt` ("Structural Architecture of Subsistence Systems")
- Prompt 10: `research/population-ecology-report-gemini.txt` ("Quantitative Population Ecology of Hunter-Gatherer Bands")

## 1. Spot-checks

| Claim | Report | Result |
|---|---|---|
| 1950 Caribou Inuit famine: ~60 starved after caribou migration shifted; deaths in place | 8 | Verified (Wikipedia, "1950 Caribou Inuit famine": ~60 deaths, half of affected communities; survivors relocated 1959). The report's "30-50% mortality" is consistent with "half the communities" but not stated there |
| Sadlermiut 1902-03: ~58 people, band extinct, a few children adopted out | 8 | Verified with a correction (Wikipedia, "Sadlermiut": 53 of 58 died; 5 survived, 1 woman and 4 children). Cause was mainly an introduced epidemic, so it is weak evidence for famine die-out |
| St. Lawrence Island 1878-80: 75-86% of 1,500 died (~1,000-1,300) | 8 | Conflicts. Wikipedia ("St. Lawrence Island famine"): ~1,000 died of ~4,000; ~1,500 remained. The report appears to treat the survivors as the starting population. Disease, weather and the alcohol trade are all cited causes |
| Artificial Anasazi: 800 kg/household/yr (5 persons), 2-year storage expiry, fission probability 0.125, relocation within 1 mile of water | 11 | Verified (Janssen 2009, JASSS 12(4)13, Table 2). The report's fission range "0.125-0.155" was not checked |
| Gallagher et al. 2019: yearly steps, logistic patch regrowth minus depletion, death below f_min, fission probability up to 0.14, mobility as an evolving trait; low mobility under high replenishment gives higher density and lower food income | 11 | Verified (Sci Rep 2019, s41598-019-42006-2). Correction: f_min = 1/n_max ≈ 0.167, not a fixed 0.17, and the depletion term is λ·(1 − 1/(n+1))·q, not λ·n |
| 1964-65 Kalahari drought: negligible Ju/'hoansi starvation mortality | 8 | Not verified (only catalogue hits for Lee and Howell). Plausible and widely repeated |
| Binford storage threshold at effective temperature 15.25 °C; QTSTOR shares (88% of low-latitude foragers store only days; 87% of high-latitude store major or massive amounts) | 9 | Not verified. The exact threshold and percentages could not be found; treat as [UNCERTAIN] |
| 85-90% of crises end in dissolution, 10-15% in extinction | 8 | The report itself labels this an inference; no source checked |
| Age-specific excess mortality table, fertility suppression 25-100% by tier | 8 | Labelled inference by the report; plausible shape (children and elders most vulnerable), numbers unverified |

Not checked: per-food spoilage rates (9), the Ache/Hadza model details, the Alroy 2001 and HUMLAND summaries (11).

## 2. What the reports change

**Prompt 11 (architecture)** supports the guild interface (R1 option B). Its recommended shape: a resource archetype = regrowth strategy + harvest strategy + nutrition profile, on a per-cell stock vector. Additions worth keeping:
- Regrowth classes: continuous (logistic), mobile (with diffusion), and pulsed (mast, wild grain: capacity arrives in one season, then decays). The interface must take a per-guild regrowth function, not one formula.
- Search-limited vs handling-limited resources. This needs no new term: a Type II per-worker return a·S/(1 + a·h·S) already separates search efficiency (a) from handling time (h). Game: low a (rare encounters), so the return tracks stock; grain and nuts: high a, so the return sits near its cap 1/h.
- Failure modes seen across models: game hunted to extinction when people are fed by something else (VEP, Alroy); storage expiry cliffs (Artificial Anasazi); Malthusian boom-bust (Artificial Anasazi, Sugarscape); labour deadlock when crops arrive (farming, later). The slice's proportional spoilage and capped take already avoid the first two.
- Dual currency (calories plus protein/fat) is recommended to stop runaway game collapse once plants or crops decouple people from game. Inferred: in the slice the per-season take cap (a fraction of stock) already prevents extinction, so dual currency can wait for farming.
- Behavioural prey depression (search efficiency drops with recent hunting effort) is recommended to stop extinction spirals and to drive camp moves. Prototype (`research/prototypes/q8-system/run3*.py`): as implemented, it showed no clear protective effect at these settings, and fixed-rank vs return-ordered allocation gave nearly the same results. Not adopted for R1; revisit in R2 (camp moves), where the Ache case puts it.

**Prompt 8 (famine)**:
- Escalation by consecutive shortfall seasons: diet broadening and storage (0-1 season), micro-band fission and faster camp moves (1-2), dispersal to kin 50-200 km (2-3), long-distance relocation or aggregation at refuges (3-4+), starvation in place only when exits are blocked. Shape adopted as input for R2-R3 and Q10; timings [P].
- Die-out in place is rare and needs blocked exits (circumscription, weather, closed borders, epidemics); dissolution into neighbours is the common outcome. This supports making dissolution part of R3 and choosing a test scenario where one band's exit is blocked.
- Hosts accept refugees when they are not stressed themselves and close borders under regional stress. A candidate rule for the occupied-refuge problem (review I7).
- Spatial scales: logistical 0-25 km, residential range 25-100 km, distress relocation 100-500 km. At ~3 km per cell: catchment r = 3 (9 km) fits; a home range is 8-33 cells across, larger than the prototype's r = 5; distress moves can cross most of the 128-cell slice map.
- Large ungulate recovery 10-25 years (40-100 seasons). Unverified, but it points the same way as the Q7 prototype (no stable setting under 30 seasons): rev 22's 30-50 season target may need widening at the long end.

**Prompt 9 (storage)**:
- Storage depends on climate seasonality: little to none where the growing season is long, major where it is short (threshold numbers unverified).
- Per-season losses by food type: roughly 2-5% for dry seeds and pemmican, 10-25% for acorns, jerky in warm seasons and fish, total loss within days for fresh tropical foods (ranges from the report; spot-check not done).
- Large stores tether bands (the report's rule: mobility locked above ~0.5 seasons of stores), produce depletion halos and precede domestication. Out of slice scope; relevant to farming emergence (log "Farming emergence" row).
- Slice implication: one pooled stash with proportional spoilage. Stash size is a world setting until a temperature or seasonality field exists; default ≤ 0.5 seasons of consumption, spoilage 0.15-0.25 per season [P].

## 3. Prompt 10 (population ecology)

| Claim | Result |
|---|---|
| Home range scales sub-linearly with band size, A ∝ N^0.75 (Hamilton et al. 2007) | Verified with a correction (PNAS 2007, n = 339): overall exponent 0.70 (95% CI 0.58-0.83); 0.756 ± 0.042 after controlling for ecology; hunters 0.90, gatherers 0.64 |
| Productivity raises density; biodiversity matters only at low productivity and pathogens only at high productivity (Tallavaara et al. 2018) | Verified in direction (PNAS 2018 abstract). The report's breakpoint (NPP 1,360 g C/m²/yr) and r = 0.597 were not in the abstract; unverified |
| Sustainable ungulate offtake 2.5-5.5% of standing stock per year; > 8% causes decline (Robinson & Redford 1991) | Not verified this session. The report writes the model as P = 0.5·rmax·D·F; the commonly cited form (from recall, unverified) is production 0.6·D·(λmax − 1) times 0.2/0.4/0.6 by longevity. Treat the percentages as [UNCERTAIN] |
| Binford packing threshold 9.1 persons/100 km²; mean band size 30.2 ± 14.5 | Not verified |
| Infant mortality q0 ≈ 0.27, death before 15 ≈ 47% (Gurven & Kaplan 2007) | Not verified (abstract only). Consistent with report 3's l15 ≈ 0.57 already in the log |

What it changes (input, not decisions):
- **R1:** a per-season hunt cap of ~1% of stock (the Q8 prototype's stable value; 1.5% collapsed game) is ~4% per year, inside the report's 2.5-5.5% sustainable band. If that band holds, the cap has an ecological anchor rather than being a pure tuning knob. Behavioural prey depression is recommended again (second report); the job it does in the literature is triggering camp moves while stock is intact (Vickers, Ache), so it belongs in R2.
- **R2:** bands move camp 5-15 times a year, 10-15 km a move (≈ 3-5 cells, just over twice the catchment radius: Binford's leapfrog). At seasonal ticks that is 1-4 camps per season, so a band's seasonal footprint is closer to its home range than to one 29-cell catchment. Home range 500-1,500 km² per band ≈ 55-165 cells (radius ≈ 4-7 cells). The prototype's radius 5 sits inside this.
- **R3 / Q9:** band size 25-35, fission at 45-50 (the prototype's fission at 50 fits). Long-run growth ≈ 0 with a potential of 1.5-3% per year. The report flags that balancing population by starvation alone produces boom-bust; homeostatic fertility (interbirth interval ≈ 3.5-4.5 years, kept even when fed) gives stable populations. Matches the prototype's run 1 (bands grew to 78 and drifted into hunger).
- **R4:** density target 0.05-0.15 persons/km² for terrestrial foragers (≈ 0.45-1.35 people per cell); warm-climate diet ≈ 53% plants, 26% hunting, 21% fishing (Marlowe 2005, via the report). The slice has no fish, so meat ≈ 30-50% of energy.
