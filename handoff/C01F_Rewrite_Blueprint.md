# C01F Rewrite Blueprint

# C01F — Manuscript Rewrite Blueprint

---

## 1. Title Options

**Option A:**
_Probabilistic Electricity Demand Forecasting During Extreme Winter Events: A Quantile Regression Case Study of the 2014 Polar Vortex in PJM_

**Option B:**
_Calibration Failure at the Tail: Quantile Regression Forecasting of the 2014 Polar Vortex Load Peak in PJM_

**Option C:**
_Full-Year Calibration Masks Tail Undercoverage: A Probabilistic Load Forecasting Case Study of the 2014 Polar Vortex_

**Recommended: Option A**

Rationale: Option A accurately describes the method (quantile regression), the domain (electricity demand), the scope (extreme winter events), the system (PJM), and the event (2014 polar vortex) — all verifiable. Options B and C foreground the calibration finding, which is a strong result but risks sounding like a methods critique paper rather than a forecasting paper. Option A fits power systems journal conventions and sets reader expectations correctly. The calibration finding is still reported prominently in results; it does not need to be the title.

---

## 2. New Central Thesis

Gradient boosted quantile regression (QR-GBT), trained on 2010–2013 PJM hourly load data and evaluated against the January 6–8, 2014 polar vortex event — when PJM load reached 140,510 MW, within roughly 2.4% of the 2014 annual peak of 144,072 MW — substantially outperforms persistence and climatological baselines on point forecast accuracy (MAE ~721 MW vs ~1,937 MW for PJM day-ahead in the same window), but its 98% prediction interval fails to contain the observed event peak, and its full-year empirical coverage of 86.8% collapses to 66.7% during the 72-hour vortex window, revealing that aggregate calibration metrics systematically conceal tail undercoverage under distribution-shifting conditions that were not represented in the training period. The paper's primary argument is therefore not that QR-GBT solves extreme-event forecasting, but that standard full-year calibration diagnostics are insufficient for evaluating probabilistic forecasters in tail-risk regimes, and that evaluating models on disaggregated extreme windows is a necessary complement to aggregate metrics.

---

## 3. Revised Contribution List

**Contribution 1 — Empirical evaluation under genuine distribution shift:**
We provide a rigorous retrospective evaluation of QR-GBT on the 2014 PJM polar vortex, demonstrating that a model with strong full-year point accuracy (GBoost MAE ~721 MW) and acceptable aggregate PI coverage (86.8%) nonetheless fails to cover the event peak at the 98% level, documenting a concrete case of calibration failure under out-of-distribution extreme cold.

**Contribution 2 — Disaggregated calibration analysis (full-year vs. extreme window):**
We show quantitatively that the 19.8-percentage-point gap between full-year empirical coverage (86.8%) and vortex-window coverage (66.7%) would be invisible to any researcher reporting only aggregate annual metrics, making the case that probabilistic forecasting benchmarks for grid reliability must include disaggregated tail-event evaluation windows.

**Contribution 3 — Reproducible open benchmark on a historically significant event:**
Using publicly available PJM Data Miner 2 load records and ERA5 reanalysis weather data, all results are fully reproducible, providing a transparent baseline against which future extreme-event probabilistic forecasting methods can be compared.

---

## 4. Full Manuscript Outline

---

### Section 1: Introduction

**Purpose:** Establish the operational stakes of load forecasting under extreme weather, identify the gap in probabilistic forecasting evaluation methodology, and state the paper's contributions.

**Key facts/results to include:**

- PJM operates the largest wholesale electricity market in the US, serving ~65 million people across 13 states + DC, installed capacity exceeding 180 GW during the study period
- The January 2014 polar vortex produced PJM load of 140,510 MW on Jan 7, 2014 — a near-annual-peak event (within ~2.4% of the 2014 summer annual peak)
- Probabilistic forecasting is under-evaluated in extreme regimes; most benchmarks report aggregate annual metrics only
- Transition from deterministic to probabilistic evaluation paradigm is the motivating gap

**Figure/table references:** None in introduction; event context can be stated in prose

**Claims to avoid:**

- Do not state Jan 2014 was the annual peak or a "winter record"
- Do not claim 143,531 MW
- Do not use "unprecedented", "all-time", or "record-breaking" without verified attribution
- Do not state dollar savings or operational deployment claims
- Do not reference NASA
- No SHAP contributions

**Approximate paragraph plan (5–6 paragraphs):**

1. Opening: Grid reliability stakes — why load forecasting accuracy matters at system peak; what happens when forecasts fail (reserve shortfalls, price spikes, emergency procedures)
2. From deterministic to probabilistic: Why point forecasts are insufficient for capacity planning; value of prediction intervals and quantile coverage
3. Extreme weather as the hardest test: Distribution shift problem — training on normal conditions, evaluating on tail events; brief motivation for polar vortex as case study
4. The evaluation gap: Most studies report aggregate calibration; no guarantee aggregate coverage holds during tail events; the disaggregated evaluation contribution
5. Paper scope and contributions: State the 3 contributions; describe dataset, method, evaluation design in one sentence each
6. Paper organization: One sentence per section

---

### Section 2: Data and Event Definition

**Purpose:** Define the dataset, describe preprocessing, characterize the polar vortex event, and justify its selection as a case study.

**Key facts/results to include:**

- PJM hourly load: 2010–2014 from PJM Data Miner 2 (metered load, MW); training period 2010–2013; evaluation 2014
- ERA5 reanalysis: t2m (2-metre air temperature), d2m (dewpoint), u10/v10 (wind components); single grid-point representative of PJM footprint or area-weighted average (state exact configuration used in pipeline)
- DST handling: UTC-aligned throughout; duplicate Nov 2 01:00 EPT rows preserved; spring forward gap handled as per pipeline
- Event definition: Jan 6–8, 2014 (72-hour window); PJM load peak 140,510 MW on Jan 7; near-annual-peak context (2014 annual peak 144,072 MW on Jun 11 or closest verified date)
- Event justification: severity relative to 2014 load distribution; complete public data availability for exact replication; historical significance in NERC/PJM grid reliability reports

**Figure/table references:**

- **Table 1:** Summary statistics — full-year 2014 and vortex window (load mean, max, min; ERA5 temperature mean, min; HDH/CDH aggregate); all values from verified pipeline
- **Figure 1:** Time series plot — PJM hourly load Jan 1–15, 2014 with vortex window shaded; ERA5 t2m on secondary axis; peak annotated at 140,510 MW (no NASA subfigure)

**Claims to avoid:**

- Do not state 143,531 MW anywhere
- Do not state "winter record" or "all-time record"
- Do not use NOAA 28-station population-weighted statistics as primary data source (may note as supplementary/provisional with explicit caveat)
- Do not claim "−1.8°F average temperature" (F16 forbidden claim)
- Do not report −24.6°F wind chill from NOAA ISD pipeline
- Do not state "less than 0.3% missing load observations" (unverified)
- Do not reference NASA AIRS

**Approximate paragraph plan (4–5 paragraphs):**

1. Load data: Source (PJM Data Miner 2), temporal resolution, coverage, units, any known data quality notes from verified pipeline
2. Weather data: ERA5 source (Copernicus CDS), variables used, spatial configuration, temporal alignment with load series; note ERA5 is reanalysis, not real-time NWP (limitation flagged here, elaborated in Section 7)
3. Preprocessing: UTC alignment, DST handling (exact method per VERIFIED_FACTSHEET), derived features (HDH, CDH, wind speed from u10/v10 components, dew point depression)
4. Event definition and characterization: Jan 6–8 window selection rationale; verified peak value; position relative to 2014 annual distribution; NERC/PJM report references for historical context
5. Case study justification: Severity (near-annual-peak load); data completeness (public sources, replicable); historical significance without overclaiming records

---

### Section 3: Forecasting Framework

**Purpose:** Define the quantile regression problem, describe QR-GBT model architecture, specify the feature set, and describe benchmark models.

**Key facts/results to include:**

- Quantile regression objective: conditional quantile function; pinball loss formulation (Equation 1)
- QR-GBT: gradient boosted trees with pinball loss; quantiles q01, q05, q10, q25, q50, q75, q90, q95, q99 (7–9 verified quantiles per pipeline)
- Feature categories: calendar (hour of day, day of week, month, holiday indicator), lagged load (24h, 48h, 168h), ERA5-derived temperature variables (t2m, HDH, CDH, dew point depression, wind speed magnitude), interaction terms (temperature × hour, temperature × weekday/weekend) — include only features verified in pipeline
- Benchmarks: Persistence-1h, Naive-24h, Naive-168h, Linear Regression, GBoost (deterministic) — no SARIMA-X, no LSTM-QR, no LightGBM-QR
- Post-processing: Monotonic rearrangement for quantile crossing correction (note: 66% crossing rate must be disclosed here as a transparency item)
- CRPS as primary probabilistic metric; Winkler score; empirical coverage (Equation 2 if CRPS integral form used)

**Figure/table references:**

- **Table 2:** Model and feature summary (not a hyperparameter table); columns: model name, type (deterministic/probabilistic), feature set, quantile set, notes
- **Figure 2:** TikZ workflow diagram (already built in rewrite instructions) — ERA5/PJM inputs → feature engineering → QR-GBT training → prediction intervals → evaluation

**Claims to avoid:**

- Do not claim 99 quantiles via spline interpolation
- Do not include NGBoost, SARIMA-X, LSTM-QR, LightGBM-QR
- Do not claim 84 features engineered / 62 retained (unverified counts)
- Do not claim Optuna 100 trials or specific hardware/runtime
- Do not claim 28-station population-weighted NOAA temperature as the primary pipeline
- Do not include SHAP methodology
- Do not claim "extreme boosting" with 2× HDH weighting unless verified

**Approximate paragraph plan (4–5 paragraphs):**

1. Problem formulation: Conditional quantile function definition; why quantile regression for prediction intervals; pinball loss equation (Eq. 1)
2. QR-GBT model: GBT update structure; pinball loss as the training objective; verified quantile set; why GBT for tabular load data (interpretability, non-parametric, handles interactions)
3. Feature engineering: Calendar features; lagged load features; ERA5-derived weather features; interaction terms — with rationale for each group
4. Benchmarks: Name and briefly describe each verified benchmark; rationale for including (persistence as operational lower bound, naive seasonal as strong baseline, LR as linear reference)
5. Post-processing and evaluation metrics: Monotonic rearrangement with crossing rate disclosure; CRPS, Winkler, empirical coverage definitions; evaluation windows (full-year 2014 and 72-hour vortex)

---

### Section 4: Experimental Design

**Purpose:** Describe the train/test split, evaluation protocol, and how the two-window evaluation design captures both aggregate and tail performance.

**Key facts/results to include:**

- Training: 2010–2013 (hourly, ~35,000 observations)
- Test set 1 (generalization): Full year 2014
- Test set 2 (tail): Jan 6–8, 2014 (72-hour vortex window, ~72 observations)
- No data leakage: Strict temporal split; no future information in features
- Evaluation metrics defined operationally: What MAPE measures (point accuracy), what empirical coverage measures (PI reliability), what CRPS measures (probabilistic sharpness + calibration jointly)
- Two-window design rationale: Full-year metrics alone conceal tail failure; vortex window isolates distribution-shift regime

**Figure/table references:**

- No new figures required; may include a simple timeline schematic inline or as a small figure showing train/test periods

**Claims to avoid:**

- Do not claim rolling-window cross-validation with 4 folds (unverified)
- Do not claim specific hyperparameters (Optuna, learning rate, tree depth) unless verified

**Approximate paragraph plan (3 paragraphs):**

1. Train/test protocol: Dates, sizes, temporal integrity rationale (why no CV across years for final evaluation)
2. Two-window evaluation design: Rationale for reporting both full-year and vortex-window metrics; what each window captures; why the gap between them is the paper's main diagnostic
3. Metric definitions recap and threshold choices: Why 98% PI for peak coverage check; why empirical coverage at 90% nominal level is the primary calibration diagnostic

---

### Section 5: Results

**Purpose:** Report verified numerical results in a clear, honest order that builds from point accuracy to probabilistic calibration to tail failure.

**Key facts/results to include (all from RESULTS_SUMMARY.md):**

- GBoost MAE ~721 MW (full year); PJM DA ~1,937 MW in vortex window (if verified for comparison)
- Full-year empirical coverage at 90% nominal: 86.8%
- Vortex-window empirical coverage at 90% nominal: 66.7%
- Coverage gap: 19.8 percentage points
- 98% PI breach: Event peak (140,510 MW) falls outside the 98% prediction interval
- Winter vs summer calibration comparison (if verified in RESULTS_SUMMARY.md)
- Benchmark comparison on point metrics (GBoost vs Persistence, Naive, LR)

**Figure/table references:**

- **Table 3:** Main results table — rows: GBoost, QR-GBT, Persistence-1h, Naive-24h, Naive-168h, LR; columns: MAPE (full year), MAE (full year), CRPS (full year), empirical coverage (full year), empirical coverage (vortex window); all verified values only
- **Figure 3:** Forecast vs actual time series — Jan 6–8 with 50%, 90%, 98% PI bands; observed peak at 140,510 MW annotated; PI breach visually evident
- **Figure 4:** Calibration plot or coverage bar chart — full-year vs vortex-window coverage at multiple nominal levels (80%, 90%, 95%, 98%); shows the systematic collapse

**Claims to avoid:**

- Do not report CRPS 2,850 MW / Winkler 9,850 MW / nCRPS 2.15% / coverage 91.7% (these are legacy fabricated values)
- Do not report MAPE 1.82%, nCRPS 0.92%, CRPS 912 MW (unverified)
- Do not claim "outperforms PJM operational forecasts" globally
- Do not claim "95% PI coverage near-nominal"
- Do not reference SARIMA-X, LSTM-QR, LightGBM-QR results
- Do not use "dominates" or similar superiority language

**Approximate paragraph plan (5–6 paragraphs):**

1. Point forecast results: GBoost vs baselines on full-year 2014; honest framing of relative accuracy
2. Probabilistic results — full year: CRPS, Winkler, empirical coverage at 90%; aggregate picture looks reasonable
3. The calibration break: Vortex-window coverage collapses to 66.7%; introduce the gap explicitly; 98% PI fails to cover the 140,510 MW peak
4. Visual evidence: Reference Figure 3 (PI bands during vortex); describe what the figure shows
5. Winter vs summer comparison: If verified — seasonal breakdown of coverage; winter already lower than summer before the vortex window
6. Summary of the pattern: Full-year aggregate metric misleads; tail-window disaggregation is necessary

---

### Section 6: Discussion

**Purpose:** Interpret the results, explain the mechanisms behind calibration failure, connect to broader forecasting literature, and draw practical implications without overclaiming.

**Key facts/results to include:**

- Distribution shift: Training data (2010–2013) did not contain a comparable extreme cold event; model was extrapolating beyond its training support
- HDH/temperature feature nonlinearity at extreme cold: The load-temperature relationship is nonlinear at very high HDH values; a model trained mostly on moderate-cold winters underestimates the tail
- Full-year calibration masking: The 86.8% full-year coverage is within acceptable range for many practitioners; only disaggregated analysis reveals the 66.7% vortex collapse
- ERA5 retrospective caveat: Even with perfect ERA5 reanalysis weather, the model undercovers — meaning the problem is model calibration, not just weather forecast uncertainty; in real operations, NWP forecast errors would add further uncertainty
- Practical implication: Probabilistic forecasters deployed for grid reliability should be evaluated on historical extreme windows, not just annual aggregate metrics; this is a systems-level recommendation, not a claim that QR-GBT is operationally ready

**Figure/table references:** Reference Figure 4 (calibration plot) and Table 3 in interpretation

**Claims to avoid:**

- Do not claim deployment readiness
- Do not claim dollar savings
- Do not compare favorably to GEFCom2014 winners with unverified numbers
- Do not reference SHAP
- Do not reference FERC 2024 conference
- Do not make 2050 projections
- Do not claim "fits ISO workflows"

**Approximate paragraph plan (4–5 paragraphs):**

1. Why calibration fails under distribution shift: Training support, temperature nonlinearity, HDH extreme values not represented in 2010–2013
2. The masking problem: Why full-year aggregate metrics are genuinely misleading (not just imprecise); quantify the masking effect; connect to evaluation methodology literature
3. ERA5 caveat and what it implies: The undercoverage is a lower bound on operational uncertainty; real operations face additional NWP error; this strengthens the case for wider PIs in extreme regimes
4. Practical interpretation: What grid operators and forecast practitioners should take from this; case for disaggregated evaluation windows as a reliability standard; conservative framing without deployment claims
5. Connection to literature: Briefly connect to broader probabilistic forecasting and distributional robustness literature (citations needed here — see Section 9)

---

### Section 7: Limitations

**Purpose:** State all verified limitations honestly and specifically. This section strengthens rather than undermines the paper.

**Key facts/results to include:** All six limitations listed below

**Figure/table references:** None required

**Claims to avoid:** Do not minimize limitations; do not claim limitations are mitigated unless mitigation is verified

**Approximate paragraph plan (6 short paragraphs or one structured list):**

1. **ERA5 retrospective reanalysis (primary limitation):** Weather inputs are ERA5 reanalysis, not real-time NWP forecasts. ERA5 represents observed meteorological conditions with high fidelity but is unavailable in real-time operations. Results therefore represent an upper bound on accuracy achievable with perfect weather foresight; operational performance would be lower due to NWP forecast errors, particularly during rapidly evolving cold air outbreaks.

2. **No operational NWP forecast comparison:** Because the study uses ERA5, it cannot directly measure the additional forecast degradation attributable to weather forecast uncertainty. A future study pairing this approach with ensemble NWP forecasts would provide operationally realistic uncertainty bounds.

3. **Quantile crossing and post-hoc monotonic rearrangement:** QR-GBT produced quantile crossings in approximately 66% of forecast instances, corrected via isotonic regression / monotonic rearrangement. While this is a standard fix, the high crossing rate indicates that the model's joint quantile structure is poorly calibrated, and the correction is post-hoc rather than architecturally enforced. Results should be interpreted with this caveat.

4. **No SHAP or feature attribution analysis:** Interpretability analysis (e.g., SHAP values) was not computed as part of this study. Claims about individual feature contributions cannot be made. This limits the mechanistic interpretation of why calibration fails.

5. **NOAA ISD provisional status:** Where NOAA ISD station data is referenced (supplementary), it carries NOAA's standard provisional data caveat and has not been fully quality-controlled at the time of analysis. ERA5 is the primary weather source; NOAA ISD figures should not be treated as authoritative.

6. **Single-system case study:** All results are specific to PJM's footprint, load profile, and the meteorological character of the January 2014 event. Generalizability to other ISOs/RTOs (ERCOT, MISO, ISO-NE) or to different types of extreme events (heat waves, ice storms) is not established and requires separate investigation.

---

### Section 8: Conclusion

**Purpose:** Restate the main finding, summarize contributions, and identify the most important direction for future work — all conservatively and accurately.

**Key facts/results to include:**

- GBoost achieves strong point accuracy (~721 MW MAE) vs baselines
- Full-year QR-GBT coverage: 86.8% (near 90% nominal)
- Vortex-window coverage: 66.7%; 98% PI breached at event peak (140,510 MW)
- Main finding: Aggregate calibration metrics are insufficient for tail-risk evaluation
- Future work: Disaggregated evaluation windows as standard; conformal prediction or distributional robustness methods; ensemble NWP integration

**Figure/table references:** None; reference Table 3 and Figure 4 briefly if needed

**Claims to avoid:**

- No fabricated metrics
- No SHAP
- No deployment claims
- No dollar savings
- No 2050 projections
- No operational superiority claims

**Approximate paragraph plan (3 paragraphs):**

1. Summary of findings: What was done, what was found; state verified numbers
2. Implications: What the calibration gap means for how probabilistic forecasters should be evaluated; the paper's methodological contribution to evaluation practice
3. Future work: Disaggregated evaluation as a standard; distributional robustness methods; ERA5 → NWP ensemble transition; multi-system replication

---

## 5. Abstract Plan (5-Sentence Structure)

| Sentence | Purpose                    | Content                                                                                                                                                                                                                                                           |
| -------- | -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1        | Context and motivation     | Extreme weather events pose acute challenges for short-term load forecasting; standard evaluation metrics aggregate performance across all conditions and may conceal failure at the tail                                                                         |
| 2        | Data and method            | Quantile regression gradient boosted trees (QR-GBT) trained on 2010–2013 PJM hourly load data with ERA5 reanalysis weather inputs are evaluated on the January 6–8, 2014 polar vortex event, when PJM load reached 140,510 MW                                     |
| 3        | Point forecast result      | On point accuracy, the gradient boosted model achieves substantially lower error than persistence and seasonal naive baselines across full-year 2014 evaluation                                                                                                   |
| 4        | Calibration failure result | Despite 86.8% full-year empirical coverage at the 90% nominal level, vortex-window coverage collapses to 66.7%, and the 140,510 MW event peak falls outside the model's 98% prediction interval                                                                   |
| 5        | Implication                | These results demonstrate that aggregate calibration metrics systematically conceal tail undercoverage under distribution-shifting extreme cold, and that disaggregated evaluation on historical extreme windows is a necessary complement to annual benchmarking |

---

## 6. Results Narrative Plan

The results section should build in five stages, each adding a layer to the main argument:

**Stage 1 — Point forecast baselines:**
Open with the simplest question: how well does the point forecaster (GBoost) perform against baselines? Report full-year 2014 MAPE/MAE for GBoost, Persistence-1h, Naive-24h, Naive-168h, and LR. Establish that GBoost is the strongest point forecaster. This stage sets up the reader to trust the model's general competence before the calibration failure is revealed. Do not yet mention the vortex window.

**Stage 2 — Full-year probabilistic performance:**
Report QR-GBT full-year CRPS, Winkler, and empirical coverage (86.8% at 90% nominal). Characterize this as "acceptable by standard annual benchmarking criteria." This is the setup for the contrast. The reader should momentarily think the model is performing well probabilistically.

**Stage 3 — Probabilistic undercoverage in the vortex window:**
Now disaggregate. Report vortex-window empirical coverage: 66.7% vs 86.8% full-year. State the gap: 19.8 percentage points. Explain that this gap is invisible if only full-year metrics are reported. This is the paper's central empirical finding. Reference Figure 4 (calibration bar chart).

**Stage 4 — Event peak outside 98% PI:**
Sharpen the finding: the 140,510 MW peak on Jan 7 falls outside the model's 98% prediction interval. This is not a marginal calibration shortfall — it is a complete tail failure at the most consequential forecast hour of the year. Reference Figure 3 (time series with PI bands). This is the most striking single result in the paper.

**Stage 5 — Winter vs summer comparison:**
Contextualize by season: if verified results show winter coverage is lower than summer coverage even outside the vortex window, report that here. This suggests the calibration problem is not unique to the 72-hour vortex window but is a broader feature of cold-weather load regimes that the model underrepresents. This extends the finding from a single-event anomaly to a structural observation about seasonal calibration.

**Bridge to Discussion:**
Close the results section with one sentence framing the transition: the pattern observed — strong aggregate performance, severe tail failure — motivates the distributional shift analysis in the Discussion.

---

## 7. Discussion Narrative Plan

**Thread 1 — Distribution shift (paragraphs 1–2):**
Begin with the mechanism: the 2010–2013 training period did not contain a polar vortex event of comparable severity. The model's representation of extreme HDH values (high heating degree hours) is sparse in training. At the tail of the temperature distribution, the load-temperature relationship becomes highly nonlinear and the model extrapolates into a regime it has not learned. This is not a failure of the QR-GBT method per se — it is a fundamental challenge for any data-driven method trained on historical data. Connect briefly to the broader distributional robustness literature (citations: relevant forecasting and ML robustness papers — see Section 9).

**Thread 2 — Cold-weather stress as a structural forecasting problem (paragraph 2–3):**
Cold-weather load stress is qualitatively different from hot-weather stress in PJM's service territory. Heating load is more diffuse, more weather-sensitive, and involves a larger share of less-efficient older heating stock. The ERA5 temperature features capture the meteorological severity, but the load response at extreme cold is a behavioral and infrastructure phenomenon that the model cannot fully learn from moderate winters. Frame this as a domain-specific observation, not a model flaw.

**Thread 3 — Full-year calibration masking (paragraph 3):**
Return to the evaluation methodology point: a researcher reporting only 86.8% full-year coverage would conclude the model is "slightly undercovering at 90% nominal" — a result many practitioners would accept. The disaggregated analysis reveals this is deeply misleading for the specific hours that matter most to grid reliability. Make the methodological point explicitly: the choice of evaluation window is a model selection and reporting decision with real consequences for how probabilistic forecasters are trusted and deployed.

**Thread 4 — ERA5 retrospective caveat and what it implies (paragraph 4):**
Be precise: the undercoverage documented here is a lower bound. ERA5 provides essentially perfect weather foresight. Real operational forecasters work with NWP ensemble forecasts that carry their own uncertainty, particularly during rapidly evolving polar air intrusions. The implication is not that QR-GBT is particularly bad — it is that even under ideal weather conditions, the model undercovers the tail. Under real operational conditions, the PI would need to be materially wider to achieve nominal coverage.

**Thread 5 — Practical interpretation without overclaiming (paragraph 5):**
The paper does not claim that QR-GBT is ready for operational deployment, nor that any specific PI width solves the problem. The practical takeaway is methodological: evaluation frameworks for probabilistic load forecasters used in reliability contexts should include disaggregated historical extreme-event windows alongside annual aggregate metrics. This is achievable with public data and standard software. Frame as a recommendation for benchmark design, not a product endorsement.

---

## 8. Limitations Plan

Six limitations, ordered from most impactful to most standard:

| #   | Limitation                                        | Why it matters                                                                                    | What it does NOT mean                                                                                     |
| --- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| 1   | ERA5 retrospective reanalysis                     | Results are an upper bound on accuracy; operational performance is lower                          | Does not invalidate findings — undercoverage is a lower bound, making the finding conservative            |
| 2   | No operational NWP forecast                       | Cannot quantify additional degradation from weather forecast error                                | A future study can extend this directly                                                                   |
| 3   | Quantile crossing (66% rate, post-hoc correction) | Model's joint quantile structure is poorly calibrated; correction is not architecturally enforced | Corrected outputs are used throughout; the crossing rate is disclosed for transparency                    |
| 4   | No SHAP / no feature attribution                  | Cannot make claims about individual feature contributions                                         | Feature importance is an open direction; it does not affect the calibration finding                       |
| 5   | NOAA ISD provisional status                       | Any NOAA ISD supplementary figures carry a quality caveat                                         | ERA5 is the primary source; NOAA is supplementary                                                         |
| 6   | Single-system case study (PJM only)               | Generalizability to other ISOs/RTOs not established                                               | PJM is the largest US wholesale market; the finding is likely relevant elsewhere but requires replication |

---

## 9. Citation Needs

The following are specific locations where literature citations are needed, with the type of citation required. No citations are invented — only types are specified; verified bibliography entries (from C01E Category 3) are matched where applicable.

| Location                                        | Citation need                                              | Verified candidate (from C01E)                                      |
| ----------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------- |
| Section 1 ¶1 (grid reliability stakes)          | Forecasting errors and reserve shortfalls in power systems | `panteli2015influence`; NERC/PJM polar vortex reports               |
| Section 1 ¶2 (probabilistic vs deterministic)   | Review of probabilistic load forecasting                   | `hong2016probabilistic`, `hong2016tutorial`, `nowotarski2018recent` |
| Section 1 ¶3 (extreme weather forecasting gap)  | Extreme weather and load forecasting challenges            | `nerc2014polar`, `pjm2014polar`                                     |
| Section 2 ¶4 (event context, NERC/PJM review)   | NERC and PJM polar vortex operational reports              | `nerc2014polar`, `pjm2014polar`                                     |
| Section 2 ¶4 (meteorological event description) | Meteorological analysis of 2014 polar vortex               | `arritt2014us`                                                      |
| Section 3 ¶1 (quantile regression foundation)   | Original quantile regression paper                         | `koenker1978regression`                                             |
| Section 3 ¶2 (gradient boosting)                | XGBoost / GBT foundational paper                           | `chen2016xgboost`                                                   |
| Section 3 ¶2 (pinball loss / QR for load)       | Gradient boosting for load forecasting                     | `taieb2014gradient`                                                 |
| Section 3 ¶4 (CRPS definition)                  | Probabilistic forecasting evaluation                       | `hong2016probabilistic` or `nowotarski2018recent`                   |
| Section 3                                       |                                                            |                                                                     |
