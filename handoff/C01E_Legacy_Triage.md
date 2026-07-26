# C01E Legacy Triage

# Task C01E — Legacy Manuscript Triage

---

## Preliminary Notes

The legacy `paper.tex` has been read in full. Every claim has been checked against `VERIFIED_FACTSHEET.md`, `RESULTS_SUMMARY.md`, and the forbidden claims registry from C01B. The triage below is exhaustive.

---

## CATEGORY 1: DELETE

These elements must be removed entirely. Do not adapt, quote, or reference them.

**Factual fabrications — numbers:**

- All instances of **143,531 MW** (Abstract, Section 1 ×2, Table 1, Figure 1b caption, Figure 3 caption, Section 3.4 ×2, Section 4.2, Section 5 Conclusion) — fabricated value not in PJM Data Miner 2
- "**only 641 MW below the all-time system peak at the time**" — invalid; actual 2014 annual peak was 141,677.9 MW (Jun 17); gap from the vortex peak is 1,167.7 MW, and the 141,677.9 MW figure is a 2014 all-time, not a system all-time
- "**winter record**" (Abstract, Section 1, Section 3.4) — winter-record status not verified per FORBIDDEN_CLAIMS.md
- "**annual peak**" framing for the Polar Vortex — the 2014 annual peak occurred in summer
- "**99.97th percentile of training**" (Section 4.2) — unverified; not in RESULTS_SUMMARY.md
- All temperature statistics from **Table 1** (vortex mean temperature −1.8°F, wind chill −24.6°F, etc.) — sourced from NOAA ISD 28-station population-weighted method, not the ERA5 pipeline; the −1.8°F figure is explicitly forbidden (F16)
- "**PJM-effective temperatures averaging 36°F below normal for 72 hours**" (Section 3.4) — not in verified data
- "**132,800 MW**" average load in vortex window — not in RESULTS_SUMMARY.md; unverified
- "**$1.5 billion in excess reserves**" (Section 1, Section 4, Conclusion) — unverified economic figure; not in VERIFIED_FACTSHEET.md
- "**$195 billion**" Texas 2021 damage figure — not in scope; unverified for this manuscript
- "**$1,800/MWh price spikes**" — not in verified data
- "**172 GW**" projected 2050 vortex peak — fabricated; not in any verified source
- "**CRPS 2,850 MW**", "**Winkler 9,850 MW**", "**nCRPS 2.15%**", "**empirical coverage 91.7%**" (Section 4.2) — none of these appear in Task07B VALID audit; conflict with verified results
- "**MAPE 1.82%**", "**nCRPS 0.92%**", "**CRPS 912 MW**", "**Winkler 4,210 MW**", "**coverage 89.7%**" (Table 3, Section 4.1) — none match RESULTS_SUMMARY.md verified values
- "**MAE 1.43 GW, RMSE 1.85 GW**" (Abstract) — not in RESULTS_SUMMARY.md
- "**95% PI coverage near-nominal**" (Abstract) — contradicted by verified 66.7% vortex coverage
- All Table 3 numbers (Persistence MAPE 4.85%, SARIMA-X, LSTM-QR, LightGBM-QR metrics) — none appear in Task07A/07B VALID audits; not in RESULTS_SUMMARY.md

**Fabricated model architecture claims:**

- **Quantile LSTM** as a tested model — not in Task07A/07B; LSTM not in verified model set
- **SARIMA-X** as a benchmark — not in verified model set (benchmarks are Persistence-1h, Naive-24h, Naive-168h, Linear Regression, GBoost)
- **LightGBM-QR** as a benchmark — not in verified model set
- **NGBoost** integration — not in verified model set
- "**62 features retained**", "**84 features engineered**" — not in VERIFIED_FACTSHEET.md
- "**28 representative stations**", population-weighted weather — not the ERA5 pipeline; this describes a legacy NOAA-only approach that was replaced
- "**k-nearest neighbors imputation**" for weather — not the ERA5 pipeline
- "**rolling-window cross-validation, 4 folds**" — not confirmed in VERIFIED_FACTSHEET.md
- "**Optuna, 100 trials**", "**NVIDIA RTX 3080, 45 minutes**", hyperparameter table (Table 2) — all unverified; Table 2 in the new manuscript is the model/feature summary, not a hyperparameter table
- "**extreme-boosting**" with 2× HDH>50 weighting — not in verified model design
- "**99 quantiles**" — verified model uses 7 quantiles (q01, q05, q10, q25, q50, q75, q90, q95, q99); the "99 quantiles via spline interpolation" claim is unverified
- "**wind chill's 6.76× amplification**" (Conclusion) — SHAP value; delete

**All SHAP content — mark for complete deletion:**

- Abstract: "**SHAP analysis reveals that temperature-derived features contribute over 70% to 95th-quantile predictions**" — no valid SHAP outputs provided
- Contribution 3 (Introduction): "**Quantile-specific SHAP analysis**" — delete
- Section 4.3 (Methodology — SHAP subsection) — delete entirely, including Equation (1) (SHAP formula) and all surrounding text
- Section 4.2: "**wind chill ($-46.8°F$) amplifies heating by 28% per SHAP**" — delete
- Section 4.3 (Results — ablation): "**Weather derivatives contribute 55% error reduction... per SHAP aggregation**" — delete
- Discussion Section 5.1: "**Quantile-specific SHAP extends interpretability**", "**wind chill × HDH slope doubles at τ=0.99**" — delete
- Discussion Section 5.2: "**SHAP heatmaps could integrate into PJM's eSuite dashboard**", "**wind chill alerts when contributions exceed 10,000 MW**" — delete
- Conclusion: "**interpretable insights via quantile-specific SHAP values**", "**wind chill's 6.76× amplification**", "**temperature's 35% global dominance**" — delete
- Keywords: "**SHAP interpretability**" — delete

**All NASA references:**

- Figure 1a: `\includegraphics{figures/NASA_AIRS_Vortex_2014.png}` — delete the entire subfigure
- Figure 1a caption: "NASA AIRS surface air temperature anomalies..." — delete
- Figure 1 main caption: "Sources: NASA AIRS/SVS; PJM Data Miner 2" — delete NASA portion
- Section 3.4: "**NASA and NOAA analyses confirm increasing frequency...**" — delete NASA clause
- Literature: "**NASA reports \cite{petropoulos2014horses}**" — `petropoulos2014horses` is a forecasting paper, not a NASA report; the label is misleading; delete NASA association

**Unverified imagery and figures:**

- Figure 2 (legacy): `Figure2_Sensitivity_Capacity.pdf` — "Annual winter peak load vs peak-day temperature (2010–2024)", "regression slopes indicating 2.5 GW/°F increase post-2017", "projected 2050 requirement +45 GW" — unverified; delete entirely
- Figure 4 (legacy, TikZ architecture diagram with quantile branches and pinball loss surface) — this is the old methodology figure, not the new Figure 2 TikZ workflow; delete
- Figure 5 (legacy): `Figure5_PolarVortex_Forecasts.pdf` — references 143,531 MW peak, SARIMA-X, LSTM benchmarks that are not in the verified model set; delete

**Overclaiming language — operational superiority:**

- "**outperforming PJM's operational day-ahead forecasts from the era**" (Section 4.1)
- "**QR-GBT dominates baselines across metrics**" (Section 4.3)
- "**35% CRPS reduction vs benchmarks**" (Conclusion) — unverified number
- "**saving $85M at $480/MWh peaks**" — unverified economic claim
- "**deployment pathways are clear**" (Discussion 5.2) — contradicted by ERA5 retrospective caveat
- "**fits ISO workflows like PJM's day-ahead markets**" — deployment claim; forbidden
- "**potentially saving $50–100M annually**" — unverified
- "**45-min retraining fits ISO workflows**" — operational claim; forbidden
- "**Integration with NWP ensembles could further operationalize it**" — overclaim
- "**responds to FERC's 2024 Technical Conference**" (Discussion 5.3) — unverified, likely irrelevant
- "**halves prior arts**" (nCRPS comparison to GEFCom) — overclaim; not verified
- "**superior to GEFCom2014 winners (1.2–1.5%)**" — unverified comparison
- All 2050 scenario projections and electrification scaling calculations — unverified
- "**cold snaps could intensify 2–3× by 2050 under RCP8.5**" — out of scope; unverified for this manuscript

**Unverified preprocessing claims:**

- "**Less than 0.3% missing load observations**", "**1.8% weather missingness**" — not in VERIFIED_FACTSHEET.md (factsheet states DST duplicate rows preserved, UTC-aligned; no 0.3% figure)
- "**Two anomalies corrected (July 2011 heatwave equipment failures)**" — not in verified data
- "**Increasing ~2.5 GW/year due to electrification**" (ADF test claim) — not in VERIFIED_FACTSHEET.md
- "**Kolmogorov-Smirnov tests confirming distributional consistency**" — not in verified audit
- "**Pearson r=0.96 for temperature vs load**", "**r≤0.89 for individual stations**" — derived from 28-station NOAA pipeline; not the ERA5 pipeline
- "**Spring DST transitions: duplicate hours averaged; missing fall hours linearly interpolated**" — contradicts VERIFIED*FACTSHEET.md (duplicate Nov 2 01:00 EPT rows \_preserved*, UTC-aligned; spring forward is where a gap occurs, not fall)

---

## CATEGORY 2: REWRITE

These sections contain reusable structure but need wholesale content replacement with verified data.

**Abstract** — rewrite entirely:

- Remove: Quantile LSTM, SARIMA-X, LightGBM-QR, SHAP, 143,531 MW, "winter record", "95% PI coverage", "MAE 1.43 GW"
- Replace with: verified model set (GBoost, QR-GBT), verified metrics from RESULTS_SUMMARY.md, correct event framing (near-annual-peak, 140,510 MW), ERA5 retrospective caveat, central finding (full-year calibration hides vortex undercoverage)

**Section 1 (Introduction) — most of it:**

- Retain: general STLF motivation paragraph (first paragraph, cleaned), event window (Jan 6–8), PJM context, forecast error motivation
- Rewrite: all numerical claims about peak demand, all dollar figures, all "winter record"/"all-time" framing, contribution list (remove SHAP contribution; replace with calibration-failure contribution)
- Delete: Figure 2 (sensitivity/capacity projection figure), all 2050 projections in introduction

**Section 3 (Data) — Table 1, all preprocessing statistics, weather sourcing:**

- Structure is reusable but all numbers need replacement
- Table 1: rewrite entirely using Task08/VERIFIED_FACTSHEET verified values; remove −1.8°F, 143,531 MW, wind chill statistics from NOAA pipeline
- Weather sourcing: rewrite to describe ERA5 (t2m, d2m, u10, v10), remove 28-station NOAA population-weighted description (can mention NOAA ISD as supplementary/provisional only)
- DST handling: rewrite to match VERIFIED_FACTSHEET (duplicate Nov 2 rows preserved, UTC-aligned)
- Section 3.4 case study justification: rewrite reasons 2 and 4; remove NASA reference; correct peak to 140,510 MW; remove "winter record" framing

**Section 4 (Methodology) — Table 2 and benchmark list:**

- Table 2: rewrite as model/feature summary table (not hyperparameter table); use verified model set
- Benchmark list: rewrite to Persistence-1h, Naive-24h, Naive-168h, Linear Regression — remove SARIMA-X, LSTM-QR, LightGBM-QR
- Quantile set: rewrite to 7 quantiles (q01–q99), not 99 quantiles
- Remove entire SHAP subsection (Section 4.4)
- Remove extreme-boosting description unless verified
- Keep: pinball loss equation (Equation 2 in legacy = correct formulation), monotonic rearrangement disclosure (reframe as limitation, not clean post-processing)
- Keep: general QR-GBT problem formulation structure

**Section 5 (Results) — all metric tables and figures:**

- Table 3: rewrite entirely with Task07A verified numbers (GBoost 721 MW, PJM DA 1,937 MW, etc.)
- Results narrative: rewrite all MAPE/CRPS/nCRPS/Winkler claims with verified values from RESULTS_SUMMARY.md
- Remove ablation studies referencing unverified feature counts or SHAP aggregations
- Remove all SARIMA-X/LSTM-QR/LightGBM-QR comparison text
- Add: verified calibration coverage (86.8% full-year → 66.7% vortex); 98% PI breach; winter vs summer comparison

**Section 6 (Discussion) — most subsections:**

- Subsection 5.1 (Theoretical): rewrite without SHAP, without nCRPS vs GEFCom comparisons, without extreme-boosting claims
- Subsection 5.2 (Practical): rewrite without operational superiority claims, without dollar savings, without deployment-ready language
- Subsection 5.3 (Policy): rewrite or reduce; remove FERC 2024 conference reference unless verified
- Subsection 5.4 (Limitations): rewrite with verified limitations from LIMITATIONS_AND_CAVEATS.md — ERA5 retrospective caveat, quantile crossing rate (66%), NOAA provisional, no SHAP

**Section 7 (Conclusion) — almost entirely:**

- Rewrite to reflect verified results; remove all fabricated metrics, SHAP claims, economic projections, 2050 scenarios, deployment claims

---

## CATEGORY 3: POSSIBLY SALVAGE

These elements have genuine value but require careful verification before use.

**Introduction — framing paragraphs:**
The general argument about probabilistic forecasting's value over deterministic point forecasts (paragraphs 4–5 of Section 1) is conceptually sound:

> _"Probabilistic load forecasting... directly addresses this challenge by estimating the full conditional distribution... Despite their advantages, quantile methods remain under-adopted..."_
> This can be adapted with verified framing — remove the three unverified "barriers" and replace with the actual contribution framing.

**Section 3.3 (Feature Engineering) — feature list structure:**
The categorical structure of features (calendar variables, lagged load, temperature derivatives, wind chill, interaction terms) is a reasonable starting point, but:

- Must verify which features are actually in the ERA5-aligned pipeline
- Remove population-weighted NOAA statistics
- Remove 28-station approach
- Keep the conceptual categories; replace NOAA-formula wind chill with ERA5 u10/v10-derived variables

**Section 4.1 (Problem Formulation):**
The quantile regression problem statement is technically sound:

- Equation 2 (pinball loss) — correct formulation; safe to reuse
- The conditional quantile function definition — standard and correct
- General CRPS equation (Eq. 3) — standard; safe if CRPS is actually reported in results (check RESULTS_SUMMARY.md)

**Section 4.2 (QR-GBT Model description) — GBT update equation:**

- Equation 3 (GBT update rule, `ŷ^(m) = ŷ^(m-1) + η·T_m`) — standard and correct
- The isotonic regression / monotonic rearrangement description — accurate and important to keep, but must be reframed as a limitation disclosure, not a clean fix (66% crossing rate must be stated)

**Section 6.4 (Limitations paragraph structure):**
The _types_ of limitations flagged are largely correct:

- NWP uncertainty / perfect weather foresight caveat — matches ERA5 retrospective caveat
- Generalizability to other RTOs — legitimate limitation
- Computational complexity concern — can be kept at reduced length
  These structural ideas can be kept; the specific numbers (e.g., "CRPS +4.2% with NWP noise", "PI widened by 10–15%") must be deleted as unverified.

**Data Availability statement (Section 8):**
The general structure is fine:

> _"PJM hourly load data are available from PJM Data Miner 2... NOAA ISD archives are publicly accessible..."_
> Can be reused with ERA5 added and preprocessing pipeline updated.

**Bibliography — salvageable citations:**
The following references appear legitimate and relevant to the rewritten manuscript (standard forecasting literature):

- `koenker1978regression` — foundational QR reference ✅
- `hong2016probabilistic`, `hong2016tutorial` — GEFCom and probabilistic forecasting reviews ✅
- `xie2016gefcom` — GEFCom2014 ✅
- `chen2016xgboost` — XGBoost paper ✅
- `hochreiter1997long` — LSTM reference (background only) ✅
- `lundberg2017unified` — SHAP paper (literature review only if SHAP section is retained as background) ✅
- `fan2012shortterm` — semi-parametric additive model ✅
- `taylor2010triple` — triple seasonal smoothing ✅
- `nowotarski2018recent` — probabilistic forecasting review ✅
- `hyndman2018forecasting` — forecasting textbook ✅
- `petropoulos2022forecasting` — forecasting theory and practice ✅
- `nerc2014polar` — NERC Polar Vortex Review ✅ (use carefully; cite for operational context only)
- `pjm2014polar` — PJM Polar Vortex Review ✅
- `panteli2015influence` — extreme weather resilience ✅
- `arora2018rule` — rule-based ARMA ✅
- `gaillard2016additive` — GEFCom2014 additive models ✅
- `taieb2014gradient` — gradient boosting for load forecasting ✅

**Flagged citations — use with caution or verify:**

- `auer2014polar` — "PJM Internal Report" — verify existence; used to support $7 GW forecast error claim (which may be directionally correct but unverified in exact magnitude)
- `gaudet2014north` — cited for PJM's "−7,200 MW error at peak" — verify; directional support for underprediction finding possible
- `arritt2014us` — meteorological analysis of 2014 polar vortex ✅ (useful for event context)
- `nerc2014polar` ✅

**Citations to delete from bibliography entirely:**

- `tastu2015space` — wind power space-time scenarios; cited incorrectly as PJM data source; irrelevant
- `ferc2024ai` — unverified conference proceedings
- `brattle2023pjm` — cited for 2050 projections; irrelevant to revised scope
- `zhou2016modeling` — pandemic modeling paper; incorrectly cited
- `cadini2017estimation` — cascading failures; incorrectly cited for polar vortex frequency claim
- `kahneman1979prospect` — cited to justify extreme-boosting via "prospect theory"; methodology is deleted; remove citation

---

## CATEGORY 4: SAFE TO REUSE

These elements can be carried into the new manuscript with minimal or no modification.

**LaTeX preamble and document structure:**

- All package imports (microtype, geometry, fancyhdr, booktabs, amsmath, tikz, subcaption, hyperref, etc.) ✅
- Running header: _"Probabilistic Demand Forecasting During Extreme Winter Events"_ ✅
- `\onehalfspacing`, margin settings, section title formatting ✅
- `\newcommand{\R}`, `\newcommand{\E}` ✅

**Title:**

> _"Probabilistic Electricity Demand Forecasting During Extreme Winter Events: A Case Study of the 2014 Polar Vortex in PJM"_
> ✅ Safe to reuse — accurate and appropriate.

**Author and affiliation:**

> Dresden E. Goehner, Independent Researcher
> ✅ Safe to reuse verbatim.

**Section heading structure:**
The 8-section structure from the rewrite instructions supersedes the legacy structure, but several legacy headings are directly reusable:

- "Introduction" ✅
- "Data and Case Study" → rename to "Data and Event Definition" per structure spec
- "Methodology" → rename to "Forecasting Framework" per structure spec
- "Results and Analysis" → "Results" per structure spec
- "Discussion" ✅
- "Limitations" → new standalone section (was embedded in Discussion)
- "Conclusion" ✅
- "Data Availability" ✅

**Pinball loss equation (legacy Eq. 2):**
$$L_\tau(y, \hat{Q}*\tau) = \begin{cases} \tau(y - \hat{Q}*\tau) & \text{if } y \geq \hat{Q}*\tau \ (1-\tau)(\hat{Q}*\tau - y) & \text{otherwise} \end{cases}$$
✅ Standard formulation; correct; safe to reuse.

**CRPS integral equation (legacy Eq. 3):**
$$\text{CRPS}(F,y) = \int_{-\infty}^{\infty}(F(z) - \mathbf{1}_{{z \geq y}})^2 dz$$
✅ Safe to reuse if CRPS is reported in verified results.

**GBT update equation (legacy Eq. 3 in methodology):**
$$\hat{y}^{(m)} = \hat{y}^{(m-1)} + \eta \cdot T_m(\mathbf{x}, \mathbf{r}^{(m-1)})$$
✅ Standard formulation; correct.

**Literature Review — subsection structure:**
The four-subsection structure of the literature review is well-organized for a power systems journal:

1. Deterministic → Probabilistic paradigm shift ✅
2. Quantile regression methods ✅
3. Benchmarking (SARIMA/LSTM/XGBoost) ✅
4. Gaps in extreme winter validation ✅
   The structure is safe to reuse; the specific claims within each subsection require verification checks.

**PJM background paragraph (Section 3.1, opening):**

> _"The PJM Interconnection operates the largest wholesale electricity market in the United States, serving approximately 65 million people across 13 states and the District of Columbia, with an installed capacity exceeding 180 GW during the study period."_
> ✅ Factual, standard, safe to reuse.

**Case study justification reasons 1 and 3 (Section 3.4):**

- Reason 1 (severity) — safe if "143,531 MW" and "largest sustained temperature anomaly" are removed; replace with verified ERA5 temperature and event-to-annual-peak ratio
- Reason 3 (data availability/transparency): _"Complete public records from PJM and NOAA enable exact replication"_ ✅ Safe to reuse, add ERA5

**Evaluation design sentence:**

> _"Models were trained on 2010–2013 data and evaluated on two test sets: (i) full year 2014 (generalization), and (ii) the 72-hour extreme window (tail performance)."_
> ✅ Safe to reuse — matches VERIFIED_FACTSHEET.md exactly.

**Cross-validation structure description (rolling window, train 2010–2013):**
The general description of temporal train/test integrity is correct; safe to reuse with verified fold counts.

**Data Availability section text (general structure):**
✅ Safe to reuse; add ERA5 Copernicus reference.

---

## Summary Triage Table

| Legacy Element                            | Verdict                           | Primary Reason                                       |
| ----------------------------------------- | --------------------------------- | ---------------------------------------------------- |
| Abstract                                  | DELETE + REWRITE                  | Wrong models, wrong metrics, SHAP, 143,531 MW        |
| Title                                     | SAFE TO REUSE                     | Accurate                                             |
| Author                                    | SAFE TO REUSE                     | Accurate                                             |
| Section 1 intro paragraphs (general)      | POSSIBLY SALVAGE                  | Need number replacement                              |
| Section 1 Figure 2 (sensitivity/capacity) | DELETE                            | Unverified data and projections                      |
| Section 1 contribution list               | REWRITE                           | Remove SHAP; replace with calibration finding        |
| Section 2 — all                           | POSSIBLY SALVAGE (structure only) | Standard literature review structure usable          |
| Section 3.1 PJM background                | SAFE TO REUSE                     | Factual                                              |
| Section 3.2 preprocessing                 | REWRITE                           | Wrong pipeline (NOAA 28-station vs ERA5)             |
| Section 3.3 feature engineering           | POSSIBLY SALVAGE                  | Structure reusable; numbers must be verified         |
| Section 3.4 case study justification      | REWRITE                           | 143,531 MW, NASA, winter record                      |
| Table 1                                   | DELETE + REWRITE                  | Contains 143,531 MW, −1.8°F (forbidden)              |
| Figure 1 (legacy, with NASA subfigure)    | DELETE subfigure; REWRITE caption | NASA AIRS must be removed                            |
| Figure 2 (legacy sensitivity/capacity)    | DELETE                            | Unverified                                           |
| Figure 3 (legacy weather)                 | DELETE caption                    | References 143,531 MW                                |
| Section 4 problem formulation             | POSSIBLY SALVAGE                  | Pinball/CRPS equations correct                       |
| Section 4 QR-GBT architecture             | REWRITE                           | Wrong model specs (99 quantiles, NGBoost, etc.)      |
| Section 4 SHAP subsection                 | DELETE                            | No valid SHAP outputs                                |
| Table 2 (hyperparameter table)            | DELETE + REWRITE                  | Not the right table; unverified params               |
| Figure 4 (TikZ architecture)              | DELETE                            | Not the new Figure 2 workflow                        |
| Section 5 all metrics                     | DELETE + REWRITE                  | All metric values unverified                         |
| Table 3 (legacy results)                  | DELETE + REWRITE                  | All values conflict with RESULTS_SUMMARY.md          |
| Figure 5 (legacy forecasts)               | DELETE                            | Wrong benchmarks, wrong peak value                   |
| Section 6.1 theoretical                   | REWRITE                           | Remove SHAP, remove unverified CRPS comparisons      |
| Section 6.2 practical                     | REWRITE                           | Remove operational claims, dollar savings            |
| Section 6.3 policy                        | REWRITE                           | Remove FERC 2024, unverified projections             |
| Section 6.4 limitations                   | REWRITE                           | Structure correct; replace with verified limitations |
| Conclusion                                | REWRITE                           | Remove all fabricated metrics and SHAP               |
| Data Availability                         | SAFE TO REUSE                     | Add ERA5                                             |
| Bibliography (subset)                     | POSSIBLY SALVAGE                  | ~20 citations verified; ~15 must be deleted          |
| LaTeX preamble                            | SAFE TO REUSE                     | Standard packages                                    |

---

C01E complete. Ready for C01F.
