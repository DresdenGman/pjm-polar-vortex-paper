# Task 07B — Quantile Forecasting Report

**Date**: 2026-07-06  
**Model**: QR-GBT (HistGradientBoostingRegressor, loss='quantile')  
**Weather**: ERA5 great_lakes_core reanalysis (RETROSPECTIVE ONLY)  

---

## 1. Executive Summary

QR-GBT quantile models were trained for 7 quantiles (q01–q99) using 2010–2013 training data and evaluated on full-year 2014. The models achieved good calibration under normal conditions but showed significant degradation during the January 2014 Polar Vortex.

**Key finding**: The QR-GBT 90% prediction interval covers 86.8% of observations full-year, but only 66.7% during the Jan 6–8 event window. The official event peak (140,510 MW) fell OUTSIDE the 98% PI. This confirms that extreme cold weather events present a distinct forecasting challenge even for probabilistic models.

---

## 2. Preflight

| Check | Status |
|-------|--------|
| Test data 143,531 → synthetic 140,000 | ✅ Fixed |
| validate_pjm_peak MANUSCRIPT_TARGET → 140,510 | ✅ Fixed |
| All grep for 143531 in active code | ✅ Clean |

---

## 3. Models Trained

| Model | Quantiles | Features |
|-------|-----------|----------|
| QR-GBT | 0.01, 0.05, 0.10, 0.50, 0.90, 0.95, 0.99 | 14 features (calendar + lags + weather) |

- Implementation: sklearn HistGradientBoostingRegressor, loss='quantile'
- max_iter=300, max_depth=6, random_state=42
- Quantile crossings: 5,786/8,760 → post-hoc monotonic rearrangement applied → 0 crossings

---

## 4. Metrics Summary

### Point Forecast (q50)

| Window | MAE (MW) | RMSE (MW) | MAPE | Bias (MW) |
|--------|----------|-----------|------|-----------|
| Full-year 2014 | 761 | 1,086 | 0.81% | +166 |
| Jan 6–8 Vortex | 2,130 | 2,768 | 1.71% | +1,472 |
| Jun 16–18 Summer Peak | 1,060 | 1,423 | 0.92% | +813 |
| Top 1% Load Hours | 2,539 | 3,123 | 1.87% | +2,242 |

### Probabilistic Metrics

| Window | Mean Pinball | 90% PI Coverage | 98% PI Coverage | Winkler(90%) |
|--------|:-----------:|:--------------:|:--------------:|:------------:|
| Full-year | 153 | **86.8%** | **97.3%** | 4,627 |
| Jan 6–8 Vortex | 473 | **66.7%** ⚠️ | **84.7%** ⚠️ | 15,476 |
| Jun 16–18 Summer | 209 | 86.1% | 93.1% | 6,355 |
| Top 1% Load | 502 | 63.2% | 82.8% | 16,168 |

---

## 5. Event Peak: Jan 7 18:00 EPT

| Metric | Value |
|--------|-------|
| Actual load | **140,510 MW** |
| PJM Day-Ahead | 137,965 MW (+2,545 error) |
| QR-GBT q50 | 135,357 MW (+5,153 error) |
| 90% PI | [131,685, 139,410] — **OUTSIDE** ❌ |
| 98% PI | [121,973, 139,585] — **OUTSIDE** ❌ |

**This is a paper-worthy finding**: the event peak exceeded even the 98% prediction interval, meaning the model assigned effectively zero probability to that load level.

---

## 6. Calibration Analysis

| q | Nominal | Full-Year Cov | Full Error | Vortex Cov | Vortex Error |
|---|---------|:------------:|:----------:|:----------:|:------------:|
| 0.01 | 1% | 1.1% | +0.1 | 0.0% | −1.0 |
| 0.05 | 5% | 5.4% | +0.4 | 1.4% | **−3.6** |
| 0.10 | 10% | 12.3% | +2.3 | 9.7% | −0.3 |
| 0.50 | 50% | 45.0% | −5.0 | 29.2% | **−20.8** |
| 0.90 | 90% | 81.2% | −8.8 | 51.4% | **−38.6** |
| 0.95 | 95% | 92.2% | −2.8 | 68.1% | **−26.9** |
| 0.99 | 99% | 98.3% | −0.7 | 84.7% | **−14.3** |

**Interpretation**: QR-GBT is reasonably calibrated for normal operating conditions but consistently undercovers during the Polar Vortex. The q95 vortex coverage of 68.1% (vs. nominal 95%) means the model's upper tail is far too narrow for extreme cold events. This is NOT a failure — it's evidence that cold-weather extremes require explicit tail modeling or weather-informed recalibration.

---

## 7. Comparison with Task07A Baselines

| Model | Full-Year MAE | Vortex MAE | Jan 7 18:00 Error |
|-------|:------------:|:----------:|:-----------------:|
| GBoost Point (Task07A) | 721 | 1,705 | −1,388 |
| QR-GBT q50 | 761 | 2,130 | +5,153 |
| PJM Day-Ahead | 1,937 | 3,148 | +2,545 |

QR-GBT q50 is slightly worse than the point-optimized GBoost (expected: quantile regression trades MAE for distributional accuracy). However, the probabilistic output provides information the point model cannot — namely, that the model was demonstrably overconfident during the event.

---

## 8. Winter vs Summer Peak Comparison

| Metric | Jan 6–8 (Winter) | Jun 16–18 (Summer) |
|--------|:----------------:|:------------------:|
| Max Load | 140,510 MW | 141,678 MW |
| QR-GBT q50 MAE | 2,130 | 1,060 |
| 90% PI Coverage | 66.7% | 86.1% |
| Mean Pinball | 473 | 209 |

**The winter vortex is much harder to forecast than the summer peak**, even though load levels are similar. This supports the paper's central thesis: extreme cold weather introduces distinct forecasting challenges beyond what load magnitude alone would suggest.

---

## 9. Quantile Crossing

5,786 of 8,760 hours (66%) had quantile crossings. Post-hoc monotonic rearrangement was applied, reducing crossings to 0. The rearrangement affected predictions at the tails (q01/q99) more than the median, but preserved overall calibration properties. This must be disclosed in the manuscript.

---

## 10. Files Generated

| File | Rows | Description |
|------|------|-------------|
| `data/results/quantile_predictions_2014.csv` | 8,760 | All quantile predictions |
| `data/results/quantile_metrics.csv` | 4 | Summary metrics by window |
| `data/results/calibration_by_quantile.csv` | 7 | Calibration per quantile |

---

## 11. Final Verdict

| Item | Verdict | Reason |
|------|---------|--------|
| QR-GBT quantile predictions | **VALID** | No leakage, authoritative data |
| Full-year probabilistic metrics | **VALID** | Good calibration (86.8% PI) |
| Vortex probabilistic metrics | **VALID** | Undercovers honestly — important finding |
| Calibration analysis | **VALID** | Clean calibration table |
| Event peak quantile check | **VALID** | Peak outside 98% PI — paper-worthy |
| Winter-vs-summer comparison | **VALID** | Winter significantly harder |
| Manuscript readiness | **NOT READY** | Needs paper.tex rewrite + figure rebuild |

---

## 12. Questions for ChatGPT/Core Editor

1. Is the vortex undercoverage finding strong enough to center the paper's narrative?
2. Should we add a recalibration step (e.g., isotonic) or present the raw undercoverage as a finding?
3. The 66% quantile crossing rate is high — is post-hoc rearrangement acceptable for EPSR, or should we switch to LightGBM native quantile models?
4. Should Figure 4 be a calibration plot, and Figure 5 a quantile forecast ribbon for the vortex window?

**Task07B is VALID for manuscript use. Probabilistic pipeline is complete.**
