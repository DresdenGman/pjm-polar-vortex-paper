# Caption Drafts — Figures and Tables

All captions use verified facts only. See `VERIFIED_FACTSHEET.md` and `RESULTS_SUMMARY.md` for source data.

---

## Figure 1 — Official PJM 2014 Load and Event Definition

**Draft caption:**

> Figure 1. PJM RTO hourly load and ERA5 weather conditions during the January 2014 Polar Vortex. Panel (a) shows full-year 2014 PJM RTO metered load, with the cold-event peak (140,510 MW, Jan 7 18:00 EPT) and the 2014 annual peak (141,678 MW, Jun 17 17:00 EPT) marked. Panel (b) shows the Jan 1–15 zoom with the Jan 6–8 event window shaded. Panel (c) shows ERA5 great_lakes_core temperature, wind chill, and heating degree hours (HDH) during the Jan 6–8 event window. All load data are from PJM Data Miner 2; weather data are same-hour ERA5 retrospective reanalysis.

**Key verified numbers**: 140,510 MW, 141,678 MW, Jan 6–8 window, ERA5 great_lakes_core.

---

## Figure 2 — Forecasting and Evaluation Workflow

**Draft caption:**

> Figure 2. Conceptual workflow diagram illustrating the forecasting and evaluation pipeline. Official PJM RTO load (2010–2014) and ERA5 retrospective reanalysis weather are combined via feature engineering (calendar variables, load lags, rolling means, and weather features) and passed to point baseline models and QR-GBT quantile models. Evaluation compares full-year 2014 performance against Jan 6–8 Polar Vortex stress-window performance and against the PJM day-ahead forecast as an external benchmark.

**Key verified numbers**: None (conceptual schematic only). Must state "conceptual workflow diagram" in caption.

---

## Figure 3 — Retrospective Probabilistic Forecast During Jan 6–8 Polar Vortex

**Draft caption:**

> Figure 3. QR-GBT retrospective probabilistic forecast for the Jan 6–8, 2014 Polar Vortex event window (72 hours). Panel (a) compares actual PJM RTO load with the QR-GBT median (q50) forecast and the PJM day-ahead forecast. Panel (b) shows the 90% and 98% prediction intervals as shaded fans around the q50 forecast. Panel (c) zooms to Jan 7 18:00 EPT, the cold-event peak (140,510 MW); the actual load lies outside the nominal 98% prediction interval. All model results use same-hour ERA5 retrospective reanalysis weather input. Prediction interval fill is approximate due to post-hoc monotonic quantile rearrangement applied to 66% of test hours.

**Key verified numbers**: 140,510 MW, 72-hour window, 90% PI, 98% PI, ERA5 retrospective caveat.

---

## Figure 4 — Calibration Breakdown

**Draft caption:**

> Figure 4. Empirical coverage versus nominal quantile level for QR-GBT probabilistic forecasts. Panel (a) shows full-year 2014 calibration, where empirical coverage tracks the nominal diagonal reasonably well (90% PI coverage = 86.8%). Panel (b) shows the same calibration curve for the Jan 6–8 Polar Vortex window only, where empirical coverage falls substantially below nominal (90% PI coverage = 66.7%). All model results use same-hour ERA5 retrospective reanalysis weather input.

**Key verified numbers**: 86.8% full-year, 66.7% vortex, ERA5 retrospective caveat.

---

## Figure 5 — Winter vs Summer Near-Peak Forecast Difficulty

**Draft caption:**

> Figure 5. Comparison of QR-GBT forecast performance between the Jan 6–8, 2014 cold-event window (winter vortex, peak 140,510 MW) and the Jun 16–18, 2014 near-peak window (summer, peak 141,678 MW). Despite similar load magnitudes, the vortex window exhibits substantially higher forecast difficulty: QR-GBT q50 MAE = 2,130 MW (vortex) versus 1,060 MW (summer), and 90% PI coverage = 66.7% (vortex) versus 86.1% (summer). All model results use same-hour ERA5 retrospective reanalysis weather input. Prediction interval fill is approximate due to quantile crossing correction.

**Key verified numbers**: 2,130 vs 1,060 MW, 66.7% vs 86.1%, 140,510 vs 141,678 MW, ERA5 retrospective caveat.

---

## Figure 6 — Tail-Risk Event Peak Error

**Draft caption:**

> Figure 6. Prediction errors at the official cold-event peak hour (Jan 7, 2014 18:00 EPT, actual load = 140,510 MW) for all evaluated models. Positive values indicate underprediction. The actual load exceeds the QR-GBT q99 upper quantile bound (139,585 MW) by 925 MW, falling outside the 98% prediction interval. The QR-GBT q50 median forecast is 135,357 MW. All weather-informed model results use same-hour ERA5 retrospective reanalysis weather input.

**Key verified numbers**: 140,510 MW, PJM DA +2,545 MW, GBoost −1,388 MW, QR-GBT q95 = 139,410 MW, QR-GBT q99 = 139,585 MW (925 MW below actual). ERA5 retrospective caveat.

---

## Table 1 — Data and Event Summary

**Draft caption:**

> Table 1. Summary of the PJM RTO hourly load dataset and the January 2014 Polar Vortex event window. Training uses 2010–2013 data; the 2014 test year includes the full-year evaluation period and the Jan 6–8 cold-event window (72 hours). The event peak (140,510 MW at Jan 7 18:00 EPT) represents 99.18% of the 2014 annual peak (141,678 MW at Jun 17 17:00 EPT). Weather variables are from ERA5 great_lakes_core retrospective reanalysis. All load data are from PJM Data Miner 2.

**Key verified numbers**: 140,510 MW, 141,678 MW, 99.18%, ERA5 great_lakes_core, PJM Data Miner 2.

---

## Table 2 — Model and Feature Summary

**Draft caption:**

> Table 2. Models evaluated and their feature sets. All weather-informed models use same-hour ERA5 retrospective reanalysis weather inputs; results do not represent operational forecast performance. The PJM day-ahead forecast is included as an external benchmark and was not used in model training. QR-GBT quantile predictions were post-processed with monotonic rearrangement to correct quantile crossings (66% of test hours affected).

**Key verified numbers**: ERA5 retrospective caveat, 66% crossing rate, PJM DA as external benchmark.

---

## Table 3 — Point Forecast Metrics

**Draft caption:**

> Table 3. Point forecast performance on the 2014 test set. Metrics are reported for the full year (8,760 hours) and the Jan 6–8 Polar Vortex event window (72 hours). The Jan 7 18:00 EPT column reports the error at the cold-event peak (140,510 MW). All weather-informed models (Linear, GBoost) use same-hour ERA5 retrospective reanalysis weather input. Positive errors indicate underprediction.

**Key verified numbers**: GBoost 721/1,705 MW, PJM DA 1,937/3,148 MW, 140,510 MW, ERA5 retrospective caveat.

---

## Table 4 — Probabilistic Forecast Metrics

**Draft caption:**

> Table 4. QR-GBT probabilistic forecast performance across evaluation windows. Full-year 90% PI empirical coverage is 86.8% but degrades to 66.7% during the Jan 6–8 Polar Vortex. The 98% PI coverage similarly degrades from 97.3% to 84.7%. The event peak (140,510 MW at Jan 7 18:00 EPT) falls outside the nominal 98% PI. All metrics use same-hour ERA5 retrospective reanalysis weather inputs; empirical coverage is observed, not guaranteed.

**Key verified numbers**: 86.8% → 66.7%, 97.3% → 84.7%, 140,510 MW outside 98% PI, ERA5 retrospective caveat.

---

## Table 5 — Event Peak Prediction Check

**Draft caption:**

> Table 5. Prediction check at the official cold-event peak (Jan 7, 2014 18:00 EPT, actual load = 140,510 MW). Positive errors indicate underprediction. The actual load exceeds the QR-GBT q95 (139,410 MW) and q99 (139,585 MW) upper quantile bounds and falls outside both the 90% and 98% prediction intervals. All weather-informed predictions use same-hour ERA5 retrospective reanalysis weather input.

**Key verified numbers**: 140,510 MW, PJM DA +2,545, GBoost −1,388, QR-GBT q99 = 139,585 MW (925 MW below actual).
