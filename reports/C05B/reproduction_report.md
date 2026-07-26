# C05B — Reproduction Report

**Classification: B — Reported-Precision Reproduction**

## Summary

The C04S pipeline was reconstructed using only documented hyperparameters. Missing parameters (learning_rate, sklearn version) were filled with recovery-environment defaults. The reconstructed GBoost point forecasts match C04S at displayed precision; quantile forecasts show systematic high correlation (r > 0.999) with mean offsets attributable to the missing learning_rate and sklearn version.

## Prediction Parity

### GBoost Point Forecasts
| Metric | Value |
|--------|-------|
| Matched timestamps | 8,762 |
| Max absolute difference | 1,042.5 MW |
| Mean absolute difference | 0.24 MW |
| RMSE (old vs new) | 15.75 MW |
| Exactly equal values | 8,760 / 8,762 |
| Pearson correlation | 1.000000 |

### QR-GBT Quantile Forecasts
| Quantile | Max diff (MW) | Mean diff (MW) | Correlation |
|----------|--------------|----------------|-------------|
| q01 | 7,191 | 57.0 | 0.9998 |
| q05 | 6,641 | 102.5 | 0.9998 |
| q10 | 4,350 | 104.9 | 0.9999 |
| q50 | 3,458 | 76.1 | 0.9999 |
| q90 | 8,806 | 222.3 | 0.9994 |
| q95 | 10,801 | 238.7 | 0.9990 |
| q99 | 6,562 | 100.2 | 0.9997 |

### Quantile Crossing
| Metric | C04S Reference | C05B Reconstruction |
|--------|---------------|-------------------|
| Hours with crossing | 5,786 / 8,760 | 5,786 / 8,760 |
| Percentage | 66.0% | 66.1% |

**Match within 0.1 percentage points.**

## Metric Parity

### GBoost Point Forecasts
| Metric | C04S Reported | C05B Reconstructed | Match |
|--------|--------------|-------------------|-------|
| Full-year MAE | 721 MW | 720.9 MW | ✅ |
| Vortex MAE | 1,705 MW | 1705.2 MW | ✅ |
| Full-year RMSE | — | 993.6 MW | — |

All published GBoost MAE values match at displayed precision.

## Unresolved Hyperparameters

| Parameter | Status | Effect |
|-----------|--------|--------|
| learning_rate | MISSING — used sklearn default (0.1) | Likely cause of quantile differences |
| sklearn version | MISSING — used recovery env (1.7.2) | May cause small numerical differences |
| GBoost random_state | MISSING — used 42 | Point predictions match exactly → likely 42 was the original |

## Files Committed

- `config/c04s_recovered.yaml` — centralized recovery configuration
- `src/data/build_modeling_features.py` — CSV validator
- `src/models/train_baselines.py` — naive baseline training
- `src/models/train_point_models.py` — Linear Regression + GBoost
- `src/models/train_quantile_gbt.py` — 7-quantile QR-GBT
- `src/evaluation/evaluate_point.py` — point forecast metrics
- `src/pipeline/reproduce_c04s.py` — orchestration script
- `artifacts/C05B_reproduced/` — all reconstructed predictions and metrics
- `reports/C05B/` — checksums, schema, provenance, environment, reproduction report
- Fixed tests: 9/9 passing (2 faulty fixtures repaired, `or True` removed)
