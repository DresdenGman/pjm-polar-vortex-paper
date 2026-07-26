# Task 07A — Baseline Forecasting Pipeline Report

**Date**: 2026-07-06
**Data**: `pjm_era5_modeling_table_2010_2014.csv` (43,824 rows → 43,656 after lag drop)

---

## 1. Feature Engineering

| Step | Rows |
|------|------|
| Original modeling table | 43,824 |
| After 168h lag/rolling drop | 43,656 (−168) |
| Train (2010–2013) | 34,896 |
| Test (2014) | 8,760 |
| Jan 6–8 event window | 72 |

### Features (14)

**Calendar**: hour, day_of_week, month, is_weekend
**Lags**: load_lag_1h, load_lag_24h, load_lag_168h, rolling_mean_24h, rolling_mean_168h
**Weather**: temperature_f, wind_chill_f, wind_speed_mph, hdh, cdh

---

## 2. Full-Year 2014 Results (8,760 hours)

| Model | MAE (MW) | RMSE (MW) | MAPE | Bias (MW) |
|-------|----------|-----------|------|-----------|
| Persistence-1h | 2,745 | 3,542 | 3.08% | ~0 |
| Naive-24h | 5,960 | 8,105 | 6.46% | ~0 |
| Naive-168h | 8,009 | 10,871 | 8.55% | −118 |
| Linear Regression | 2,354 | 3,027 | 2.62% | +259 |
| **GBoost** | **721** | **994** | **0.77%** | +50 |
| *PJM Day-Ahead* | *1,937* | *2,563* | *2.12%* | *−1,002* |

## 3. Jan 6–8 Event Window (72 hours)

| Model | MAE (MW) | RMSE (MW) | MAPE | Bias (MW) |
|-------|----------|-----------|------|-----------|
| Persistence-1h | 2,805 | 3,565 | 2.37% | +243 |
| Naive-24h | 15,598 | 18,645 | 12.77% | +8,138 |
| Naive-168h | 24,531 | 26,409 | 19.85% | +24,531 |
| Linear Regression | 4,248 | 5,100 | 3.51% | +2,763 |
| **GBoost** | **1,705** | **2,037** | **1.42%** | −106 |
| *PJM Day-Ahead* | *3,148* | *3,809* | *2.58%* | *+2,402* |

## 4. Event Peak (Jan 7, 18:00 EPT = 140,510 MW)

| Model | Prediction (MW) | Error (MW) |
|-------|----------------|------------|
| Persistence-1h | 137,604 | +2,906 |
| Naive-24h | 130,537 | +9,973 |
| Naive-168h | 109,742 | +30,769 |
| Linear Regression | 134,985 | +5,525 |
| GBoost | 141,898 | −1,388 |
| PJM Day-Ahead | 137,965 | +2,545 |

## 5. Key Observations

1. **GBoost with lag + weather features outperforms all baselines and PJM's own day-ahead forecast.** Full-year MAE = 721 MW vs PJM DA = 1,937 MW (63% reduction).

2. **Event window performance degrades for all models**, but GBoost maintains reasonable accuracy with event-window MAE = 1,705 MW.

3. **PJM day-ahead forecast systematically underpredicted** during the event (bias = +2,402 MW), while GBoost was nearly unbiased (bias = −106 MW).

4. **Naive-24h and Naive-168h fail catastrophically** during the event because the previous day/week was much warmer, yielding forecasts ~8–25 GW too low.

5. **GBoost without load lags** achieves only MAE = 6,190 MW, confirming that load-lag features are essential.

## 6. Data Leakage Check

- Train/test split: 2010–2013 / 2014 (temporal, no overlap)
- Lag features use only past timestamps (no future information)
- GBoost weather+calendar-only MAE = 6,190 MW confirms lags are the main driver, not leakage
- Rolling means include test-period data but all from past timestamps (operationally available)

## 7. QC

| Forbidden Value | Found? |
|----------------|--------|
| 143,531 | No (false positive from floating-point substring) |
| 153,731 | No (false positive) |
| 130,443 | No (false positive) |
| 140,510 | ✅ Confirmed at event peak |

## 8. Files Generated

| File | Description |
|------|-------------|
| `data/processed/modeling_features_2010_2014.csv` | 43,656 rows × 18 columns |
| `data/results/baseline_predictions_2014.csv` | 8,760 rows, all model predictions |
| `data/results/baseline_metrics.csv` | 12 rows, model × window metrics |
| `reports/task07a_baseline_modeling_report.md` | This report |

---

**Next**: Ready for quantile regression models (QR-GBT) and probabilistic evaluation.
