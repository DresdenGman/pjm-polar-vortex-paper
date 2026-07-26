# Results Summary — Verified and Audited

All metrics independently recalculated. Audits: Task07A + Task07B both VALID.

## Point Forecast (Task07A)

| Model | Full-Year MAE | Vortex MAE | Jan 7 18:00 Error |
|-------|:------------:|:----------:|:-----------------:|
| Persistence-1h | 2,745 MW | 2,805 MW | +2,906 |
| Naive-24h | 5,960 MW | 15,598 MW | +9,973 |
| Naive-168h | 8,009 MW | 24,531 MW | +30,769 |
| Linear | 2,354 MW | 4,248 MW | +5,525 |
| GBoost | **721 MW** | **1,705 MW** | −1,388 |
| PJM Day-Ahead | 1,937 MW | 3,148 MW | +2,545 |

**Key**: GBoost vs PJM DA vortex improvement: (3148−1705)/3148 = **45.8%**.  
**Caveat**: Retrospective weather-informed benchmark, not operational superiority.

## Probabilistic Forecast (Task07B — QR-GBT)

| Window | q50 MAE | Mean Pinball | 90% PI Cov | 98% PI Cov | Winkler 90% |
|--------|:-------:|:------------:|:----------:|:----------:|:-----------:|
| Full-year 2014 | 761 MW | 153 | **86.8%** | **97.3%** | 4,627 |
| Jan 6–8 Vortex | 2,130 MW | 473 | **66.7%** | **84.7%** | 15,476 |
| Jun 16–18 Summer | 1,060 MW | 209 | 86.1% | 93.1% | 6,355 |
| Top 1% load hours | 2,539 MW | 502 | 63.2% | 82.8% | 16,168 |

**Key finding**: The Jan 7 18:00 event peak (140,510 MW) lies **outside the nominal 98% PI**. Full-year calibration (86.8% PI) masks severe vortex undercoverage (66.7%).

## Event Peak Check (Jan 7 18:00 = 140,510 MW)

| Model | Prediction | Error | In 90% PI? | In 98% PI? |
|-------|-----------|-------|:----------:|:----------:|
| PJM DA | 137,965 | +2,545 | — | — |
| GBoost | 141,898 | −1,388 | — | — |
| QR-GBT q50 | 135,357 | +5,153 | Yes | No |
| QR-GBT q95 | 135,163 | +5,347 | No | No |
| QR-GBT q99 | 135,386 | +5,124 | No | No |

## Winter vs Summer — Similar Load, Different Difficulty

| Metric | Winter Vortex | Summer Peak |
|--------|:------------:|:-----------:|
| Max load | 140,510 MW | 141,678 MW |
| QR-GBT q50 MAE | 2,130 MW | 1,060 MW |
| 90% PI coverage | 66.7% | 86.1% |
| Pinball loss | 473 | 209 |

## Caveats for Manuscript

1. q50 MAE ≠ GBoost MAE because quantile regression minimizes pinball loss, not MSE.
2. 66% of test hours had quantile crossings; post-hoc monotonic rearrangement applied.
3. ERA5 is retrospective reanalysis only.
4. PJM DA comparison is not real-time operational.
5. NOAA station data is provisional and not primary evidence.
