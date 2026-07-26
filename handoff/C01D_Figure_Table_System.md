# C01D Figure Table System

# Task C01D — Figure and Table System

---

## Preliminary: Source Confirmation

Reading from the provided documents:

- `task08_figure_table_rebuild_report.md` ✅
- `task08c_final_figure_polish_report.md` ✅
- `FILE_TREE.md` ✅
- `all_tables.tex` — content will be inferred from Task08 reports and verified facts (file not directly provided, but structure is confirmed from the file tree)

All 6 figures confirmed READY per Task08C final QC. Font: Type1 (Helvetica). Zero legacy values. Zero NASA imagery.

---

## 1. What Each Figure Shows

**Figure 1 — `figure1_event_definition.pdf`**
Three-panel display:

- Panel (a): Full-year 2014 PJM RTO hourly load — establishes the annual load envelope and places the Polar Vortex in context relative to the summer peak
- Panel (b): Jan 1–15 zoom — isolates the event window, shows the load spike and recovery
- Panel (c): Jan 6–8 weather panel — ERA5 temperature and heating-degree-hours (HDH), with HDH legend repositioned to lower-left (Task08C fix) to avoid data overlap

This figure is entirely data-driven from verified PJM and ERA5 CSVs. The annual peak (141,678 MW, Jun 17) and event peak (140,510 MW, Jan 7) are both visible, enabling the reader to immediately verify the "near-annual-peak" framing without taking the authors' word for it.

---

**Figure 2 — `figure2_workflow_tikz.pdf`**
A TikZ-compiled conceptual schematic (31 KB, pure vector) showing the full pipeline:

> Data Sources → Feature Engineering → Model Training → Forecast Generation → Evaluation Framework

This is a **workflow diagram only** — it contains no numerical results, no performance claims, and no data-derived content. It was redrawn in TikZ (replacing an earlier Python schematic) to produce clean vector output for publication.

---

**Figure 3 — `figure3_vortex_quantile_forecast.pdf`**
Three-panel probabilistic forecast display for the Jan 6–8, 2014 Polar Vortex window (72 hours):

- Panel (a): Actual load vs QR-GBT median (q50) forecast
- Panel (b): 90% and 98% prediction intervals as shaded fans
- Panel (c): Peak zoom at Jan 7 18:00 EPT — peak annotation moved to right side with white bounding box (Task08C fix) for clarity at both column widths

This figure directly shows the PI fan failing to contain the actual peak — the visual representation of the 98% PI breach finding. Panel (c) makes the undercoverage unambiguous at a glance.

Note: PI fill in panel (b) is approximate due to quantile crossing correction — **this must be acknowledged in the caption.**

---

**Figure 4 — `figure4_calibration_breakdown.pdf`**
Calibration reliability curves comparing:

- Full-year 2014 performance (nominal vs empirical coverage)
- Jan 6–8 vortex window performance
- Ideal calibration diagonal

This figure shows the gap between aggregate calibration (close to diagonal for full year) and event-window calibration (substantially below diagonal for vortex). It is the quantitative support for the central thesis: full-year calibration metrics conceal event-window failure.

---

**Figure 5 — `figure5_winter_vs_summer.pdf`**
Side-by-side comparison of the Jan 6–8 vortex window and the Jun 16–18 summer near-peak window:

- Panel (a): MAE comparison — winter 2,130 MW vs summer 1,060 MW (2× harder)
- Panel (b): PI coverage comparison — winter 66.7% vs summer 86.1%

The two windows are matched by load magnitude (winter 140,510 MW vs summer 141,678 MW), making this a controlled natural experiment. The figure demonstrates that forecasting difficulty is driven by weather regime, not load level.

Note: PI fill is approximate due to crossing correction — same caveat as Figure 3.

---

**Figure 6 — `figure6_tail_risk_event_peak.pdf`**
Error bar / prediction check display for Jan 7, 18:00 EPT (140,510 MW) across all models:

- GBoost: 141,898 MW (−1,388 MW error) ← closest
- PJM Day-Ahead: 137,965 MW (+2,545 MW error)
- Linear Regression: 134,985 MW (+5,525 MW error)
- Persistence-1h: 137,604 MW (+2,906 MW error)
- QR-GBT q99 upper bound: 135,386 MW ← **below actual by 5,124 MW**

This figure provides single-hour evidence that the model's entire upper probability tail was below the observed peak — making the 98% PI breach visually immediate.

Key note from Task08: _"QR-GBT q95/q99 values at event peak are very close to q50 (135,163 vs 135,357) — this reflects the model's inability to differentiate upper quantiles under extreme cold."_ This must be disclosed.

---

## 2. What Each Table Contributes

**Table 1 — Data and Event Summary**
Establishes the factual record for the study:

- PJM RTO training period (2010–2013), source (Data Miner 2)
- Cold-event peak: 140,510.2 MW at Jan 7 18:00 EPT
- Annual peak: 141,677.9 MW at Jun 17 17:00 EPT
- Event-to-annual ratio: 99.18%
- ERA5 weather variables used (t2m, d2m, u10, v10)
- DST handling note
- Zero data leakage confirmation

This table is the manuscript's single-source-of-truth anchor — every factual claim in the text traces back to it.

---

**Table 2 — Model and Feature Summary**
Documents the forecasting system design:

- Model types: Persistence-1h, Naive-24h, Naive-168h, Linear Regression, GBoost, QR-GBT
- Feature sets per model
- Weather input: ERA5 retrospective reanalysis (labeled explicitly — confirmed by Task08 QC ✅)
- Quantile crossing disclosure (confirmed present in caption — Task08 QC ✅)

This table serves as the reproducibility record — a reader could reconstruct the experiment from Table 2 alone.

---

**Table 3 — Point Forecast Metrics (Task07A)**
Full results for all point-forecast models:

- Full-year MAE, RMSE for all 5 models + PJM DA benchmark
- Jan 6–8 vortex window MAE, RMSE
- Sources: verified Task07A VALID audit outputs

This is the primary evidence table for the Results — Point Forecast section. GBoost dominates (721 MW full-year, 1,705 MW vortex).

---

**Table 4 — Probabilistic Forecast Metrics (Task07B)**
Full QR-GBT calibration results:

- q50 MAE and mean pinball loss for full-year, vortex, summer, top-1% windows
- 90% PI and 98% PI empirical coverage for all windows
- Winkler scores
- Sources: verified Task07B VALID audit outputs

This table carries the most important numbers in the paper — the full-year vs vortex coverage contrast (86.8% → 66.7%) — and is the quantitative backbone of the central finding.

---

**Table 5 — Event Peak Prediction Check**
Single-row focus on Jan 7, 18:00 EPT (140,510 MW):

- All model predictions vs actual
- QR-GBT q90/q98/q99 bounds vs actual
- Errors in MW and percentage
- Verdict: peak outside all PI levels

This table is the sharpest single piece of evidence for the tail-risk finding. It complements Figure 6 (visual) with exact numbers.

---

## 3. Figure and Table → Manuscript Section Mapping

| Item         | Manuscript Section                           | Rationale                                                |
| ------------ | -------------------------------------------- | -------------------------------------------------------- |
| **Table 1**  | Section 2 — Data and Event Definition        | Anchors all factual claims at first introduction         |
| **Figure 1** | Section 2 — Data and Event Definition        | Visual event definition; shows both peaks                |
| **Figure 2** | Section 3 — Forecasting Framework            | Workflow diagram belongs with methodology                |
| **Table 2**  | Section 3 — Forecasting Framework            | Model/feature documentation belongs with methodology     |
| **Table 3**  | Section 5 — Results (Point Forecasts)        | Point forecast evidence                                  |
| **Figure 3** | Section 5 — Results (Probabilistic)          | Visual PI fan + peak breach                              |
| **Figure 4** | Section 5 — Results (Calibration)            | Calibration curve comparison                             |
| **Table 4**  | Section 5 — Results (Probabilistic)          | Numerical calibration evidence                           |
| **Figure 5** | Section 5 — Results / Section 6 — Discussion | Winter vs summer regime comparison                       |
| **Table 5**  | Section 5 — Results (Event Peak)             | Peak prediction check numbers                            |
| **Figure 6** | Section 6 — Discussion (Tail Risk)           | Tail-risk evidence; interpretation belongs in Discussion |

---

## 4. Main Claim Each Figure Supports

| Figure       | Main Claim Supported                                                                                                                                                    |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Figure 1** | "The Jan 6–8 Polar Vortex produced a near-annual-peak load of 140,510 MW (99.18% of the 2014 annual peak)"                                                              |
| **Figure 2** | "The forecasting pipeline proceeds from ERA5-aligned PJM data through feature engineering to QR-GBT evaluation" (methodology transparency)                              |
| **Figure 3** | "The 90% and 98% prediction intervals failed to contain the event peak — the actual load of 140,510 MW exceeded the q99 upper bound"                                    |
| **Figure 4** | "Full-year calibration (86.8%) conceals severe event-window undercoverage (66.7%) — aggregate metrics are insufficient diagnostics for extreme events"                  |
| **Figure 5** | "Forecasting difficulty is driven by cold-weather regime, not load magnitude — winter is 2× harder than a comparable summer peak window"                                |
| **Figure 6** | "All models underpredicted the event peak; the QR-GBT q99 bound was 5,124 MW below the actual load, indicating inadequate upper-tail representation under extreme cold" |

---

## 5. Caption Caveats That Must Be Preserved

These are non-negotiable caption elements confirmed by Task08 QC and the known results:

| Figure/Table | Required Caption Caveat                                                                                                                                              |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Figure 1** | "Weather data: same-hour ERA5 retrospective reanalysis. HDH computed from ERA5 t2m and wind components."                                                             |
| **Figure 3** | "Prediction interval fill is approximate due to post-hoc monotonic quantile rearrangement applied to 5,786 crossing hours (66% of test set)."                        |
| **Figure 4** | "Calibration curves based on full-year 2014 test set (8,760 hours) and Jan 6–8 vortex subsample (72 hours). ERA5 retrospective weather inputs."                      |
| **Figure 5** | "PI fill approximate — quantile crossing correction applied. Windows selected for near-equal load magnitude to isolate weather regime effect."                       |
| **Figure 6** | "QR-GBT q95 and q99 bounds are very close to q50 at this hour, reflecting the model's inability to differentiate upper quantiles under extreme cold conditions."     |
| **Table 2**  | "All weather-informed models use same-hour ERA5 retrospective reanalysis. Results do not represent operational forecast performance." + quantile crossing disclosure |
| **Table 4**  | "All metrics use ERA5 retrospective reanalysis weather inputs. Coverage is empirical, not guaranteed."                                                               |
| **Table 5**  | "Actual peak: 140,510.2 MW at Jan 7 18:00 EPT (PJM Data Miner 2). QR-GBT upper quantiles collapsed toward q50 under extreme cold — see text."                        |

---

## 6. Figure 2 — Confirmed as Conceptual Workflow Diagram

✅ **Confirmed.**

Figure 2 (`figure2_workflow_tikz.pdf`) is a **TikZ-compiled conceptual schematic only.** It contains:

- No numerical data
- No performance claims
- No model output values
- No ERA5 data
- No figures from the results

It must be described in the manuscript as a _"conceptual workflow diagram illustrating the forecasting and evaluation pipeline"_ — nothing stronger. It is not a results figure and should not be cited as evidence for any quantitative claim. Its role is methodology transparency and readability.

---

## 7. Confirmed Clean Figure System

All six figures are confirmed free of the following prohibited content per Task08 and Task08C QC:

| Prohibited Element     | Status                                                                  |
| ---------------------- | ----------------------------------------------------------------------- |
| NASA AIRS imagery      | ✅ **Absent from all figures**                                          |
| 143,531 MW value       | ✅ **Absent from all figures**                                          |
| 153,731 MW value       | ✅ **Absent from all figures**                                          |
| Legacy MATLAB data     | ✅ **Not used** (MATLAB figures kept as alternatives only, not primary) |
| AI-generated imagery   | ✅ **None**                                                             |
| Embedded legacy values | ✅ **None**                                                             |
| Type3 fonts            | ✅ **Fixed** — all Type1 (Helvetica)                                    |

The two legacy MATLAB figures (`Figure1_load_weather_forecast_final.pdf`, `Figure3_event_window_detail_final.pdf`) are retained as **alternatives only** — they must not be referenced in the manuscript unless explicitly substituted. The primary figure set is the Python/TikZ rebuilt versions.

---

## 8. Where the Results Narrative Should Rely on Figures vs Tables

This mapping governs how each results subsection should be written:

**Lead with Tables when:**

- Reporting exact numerical results (MAE, coverage percentages, pinball loss, Winkler scores)
- Making direct model-to-model comparisons requiring precise values
- Documenting the event peak check (Table 5 provides the authoritative numbers)
- Establishing data provenance and event definition facts (Table 1)

**Lead with Figures when:**

- Describing temporal patterns, visual trends, or regime shifts (Figure 1, Figure 3)
- Explaining calibration failure conceptually before presenting numbers (Figure 4 before Table 4)
- Arguing for the winter-vs-summer regime difference (Figure 5 is more persuasive visually than the numbers alone)
- Illustrating the tail-risk finding for a general reader (Figure 6 makes the underprediction immediately intuitive)
- Introducing the methodology (Figure 2 replaces a lengthy verbal description)

**Coordinated figure + table pairs** (use both together):

| Figure   | Companion Table  | Section                              |
| -------- | ---------------- | ------------------------------------ |
| Figure 3 | Table 5          | Results — Probabilistic + Event Peak |
| Figure 4 | Table 4          | Results — Calibration                |
| Figure 5 | Table 4 (subset) | Results / Discussion                 |
| Figure 6 | Table 5          | Results / Discussion — Tail Risk     |

**General rule**: Figures carry the narrative argument; tables carry the evidentiary numbers. The text should reference both — state the finding verbally, cite the figure for visual support, cite the table for the exact value.

---

C01D complete. Ready for C01E.
