# Review: vegetation drought decline and recovery (Gemini prompt 7)

Reviewed 2026-10-30. Report: `research/vegetation-drought-report-gemini.txt` (text extracted from the PDF `research/Vegetation Drought Decline and Recovery.pdf`). Feeds spec Q6 (vegetation) and Q7 (large fauna); its storage and forager-mobility sections also bear on Q8 and Q10.

## Verdict
Same pattern as report 3: the directions are usable, the specific numbers and attributions are not. Use it for shape (fast grass, slow forest, decline faster than recovery, herbivores lag and recover slowly), not for values. Its Python sketch is not usable (floats in thresholds, ad hoc constants, a floor at 5% of K).

## Spot-checks
| Claim | Result |
|---|---|
| "Wilcox et al. 2024, Science, EDGE network, n = 170 sites: severe 1-year drought cut ANPP 35%" | **Partly verified, misattributed.** The 35% figure matches Smith et al. 2024, *PNAS* (International Drought Experiment, 100 sites, 6 continents): extreme (1-in-100-year) drought cut ANPP 35% vs 21% for nominal drought, with larger losses in drier sites (Carnegie Science summary). Author, journal and site count in the report are wrong. Its recovery claim ("~80% recovered within 1 season") is not in that source as far as checked: unverified |
| "Gherardi & Sala 2015, PNAS, meta-analysis of 13 LTER sites" | **Wrong.** It is a 6-year field experiment manipulating precipitation variability (Jornada, per the Jornada LTER archive listing); perennial grass productivity fell 81% and shrub productivity rose 67% (Sala lab summary). It does support the report's shrub-encroachment tipping point |
| "Schwalm et al. 2017, Nature: grasslands recover in <6 months, forests 12-28 months" | **Paper verified; numbers not.** The paper exists and finds recovery times lengthening everywhere, longest in the tropics and northern high latitudes (NASA JPL summary). No months by vegetation type found in the summaries checked |
| Ciais et al. 2005: ~30% GPP drop in Europe in 2003 | Consistent with recall; not re-checked |
| Herbivore lag 1-2 seasons, recovery 3-7 years, r_max 0.15-0.25/yr (Mduma 1999, Ogutu 2014) | **Not verified** (searches returned no usable source text). Plausible from demography (1 calf/yr, maturity 1.5-3 yr), but treat as [P] |

## Adopted as shape (not values)
- Grass-like (dry) cells: large, fast drops (roughly half or more in 1-2 seasons under severe drought) and fast recovery, often within the drought's own length.
- Forest-like (wet) cells: smaller drops spread over several seasons and slower recovery, longer than the drought.
- Decline is faster than recovery.
- Heavy grazing during or after drought slows recovery (emerges from the grazing term; no extra rule needed).
- Large herbivores lag vegetation by 1-2 seasons and rebuild over years, so the lasting food shortage after a drought comes from game, not plants (relevant to Q7 and the success test).

## Not adopted (out of slice scope)
- Tipping points with permanent capacity loss (woody encroachment, forest die-off, desertification): need soil/fire fields; revisit with those.
- Social storage (hxaro kin networks), water refugia: no relations or water field in the slice.
