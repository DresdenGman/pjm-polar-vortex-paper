# C05B — Hyperparameter Provenance

Extracted from paper.tex and repository reports. MISSING = no record found; do not guess.

## GBoost (Point Forecast)

| Parameter | Value | Evidence Source | Status |
|-----------|-------|----------------|--------|
| algorithm | sklearn HistGradientBoostingRegressor | task07a_validity_audit.md | Verified |
| max_iter | 300 | task07a_validity_audit.md, paper.tex consensus | Verified |
| max_depth | 6 | task07a_validity_audit.md | Verified |
| random_state | — | No record found | MISSING |
| learning_rate | — | No record found | MISSING |
| library_version (sklearn) | — | No record found | MISSING |
| Features | 14 (calendar + lags + weather) | paper.tex Section 3 | Verified |

## QR-GBT (Quantile Forecast)

| Parameter | Value | Evidence Source | Status |
|-----------|-------|----------------|--------|
| algorithm | sklearn HistGradientBoostingRegressor, loss='quantile' | task07b report | Verified |
| max_iter | 300 | task07b report | Verified |
| max_depth | 6 | task07b report | Verified |
| random_state | 42 | task07b report | Verified |
| quantiles | q01, q05, q10, q50, q90, q95, q99 (7 quantiles) | prediction CSV columns | Verified |
| learning_rate | — | No record found | MISSING |
| library_version (sklearn) | — | No record found | MISSING |
| Features | Same 14 as GBoost | paper.tex Section 3 | Verified |

## Baselines

| Model | Method | Evidence |
|-------|--------|----------|
| Persistence | ŷ_t = y_{t-1} | paper.tex Section 3.3 |
| Naive 24h | ŷ_t = y_{t-24} | paper.tex Section 3.3 |
| Naive 168h | ŷ_t = y_{t-168} | paper.tex Section 3.3 |
| Linear Regression | sklearn LinearRegression | reports consensus |
| PJM Day-Ahead | PJM published forecast | paper.tex |

## Feature Construction

| Feature | Source | Evidence |
|---------|--------|----------|
| hour, day_of_week, month | Calendar | paper.tex Section 3.1 |
| load_lag_1h, load_lag_24h, load_lag_168h | PJM load | paper.tex Section 3.2 |
| load_rolling_mean_24h, load_rolling_std_24h | PJM load | paper.tex Section 3.2 |
| load_rolling_mean_168h | PJM load | paper.tex Section 3.2 |
| t_f (°F) | ERA5 2m temperature (great_lakes_core mean) | paper.tex Section 2.2 |
| wind_chill (°F) | NOAA formula from t_f + wind_speed | paper.tex Section 2.2 |
| wind_speed (mph) | sqrt(u10²+v10²) from ERA5 | paper.tex Section 2.2 |
| HDH | max(65 - t_f, 0) | paper.tex Section 2.2 |
| CDH | max(t_f - 65, 0) | paper.tex Section 2.2 |

## Data Split

| Parameter | Value | Evidence |
|-----------|-------|----------|
| Training period | 2010–2013 | paper.tex |
| Test period | 2014 (full year) | paper.tex |
| Train rows | 34,896 | reports |
| Test rows | 8,760 | reports |
| Split type | Chronological (no shuffling) | reports |
| Max lookback | 168 hours (dropped from start) | paper.tex |

## Post-processing

| Parameter | Value | Evidence |
|-----------|-------|----------|
| Quantile crossing rate | 5,786/8,760 (66%) | task07b report |
| Post-hoc fix | Monotonic rearrangement | task07b report |
| After fix | 0 crossings | task07b report |
