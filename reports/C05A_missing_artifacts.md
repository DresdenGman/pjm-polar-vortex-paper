# C05A — Missing Artifacts Report

**Date:** 2026-07-26
**Branch:** C05-epsr-rebuild

## Artifacts Present (Found During Recovery Search)

| Filename | Role | Location | Status |
|----------|------|----------|--------|
| modeling_features_2010_2014.csv | Primary modeling dataset | data/processed/ | ✅ FOUND (6.5MB) |
| baseline_predictions_2014.csv | Point forecast predictions | data/results/ | ✅ FOUND (1.1MB) |
| quantile_predictions_2014.csv | Quantile forecast predictions | data/results/ | ✅ FOUND (2.3MB) |
| pjm_load_2010_2014_rto_hourly.csv | Raw PJM load | data/raw/pjm/ | ✅ FOUND |
| pjm_day_ahead_forecast_2014_clean.csv | PJM DA forecast | data/raw/pjm/ | ✅ FOUND |
| pjm_era5_modeling_table_2010_2014.csv | Merged modeling table | data/processed/ | ✅ FOUND |
| weather_era5_pjm_2010_2014_great_lakes_core.csv | ERA5 weather features | data/processed/ | ✅ FOUND |
| baseline_metrics.csv | Baseline evaluation metrics | data/results/ | ✅ FOUND |
| quantile_metrics.csv | Quantile evaluation metrics | data/results/ | ✅ FOUND |
| calibration_by_quantile.csv | Calibration per quantile | data/results/ | ✅ FOUND |

## Artifacts Missing

| Filename | Role | Recoverable? | Reconstruction Source | Would Reproduce C04S? |
|----------|------|-------------|----------------------|----------------------|
| **Actual training script for baselines** | src/models/train_baselines.py raises NotImplementedError | ❓ Unknown | Need original script or rewrite from reports | Partial (hyperparams documented in reports) |
| **Actual training script for QR-GBT** | src/models/train_qr_gbt.py raises NotImplementedError | ❓ Unknown | Need original script or rewrite from reports | Partial |
| **Actual evaluation scripts** | src/evaluation/*.py raise NotImplementedError | ❓ Unknown | Need original scripts | Partial |
| **environment.yml / requirements.txt** | Package versions | ❌ Missing | Reconstruct from venv (if still intact) | Approximate |
| **README.md** | Project documentation | ❌ Missing | Write from scratch | N/A |
| **PJM raw data for years 2010-2013** | Individual year files exist in data/raw/pjm/ | ✅ Present | N/A | Yes |
| **ERA5 raw data** | Not found in repo | ❓ Unknown | May be in external storage | Would need re-download |
| **Data download scripts** | PJM Data Miner 2 / ERA5 CDS download | ❌ Missing | Write from documentation | Approximate |

## Script Status Detail

### src/models/train_baselines.py
- **Current state:** Skeleton with NotImplementedError
- **Expected functionality:** Train Persistence, Naive(daily), Naive(weekly), Linear Regression, GBoost
- **Recoverability:** Reports describe GBoost hyperparams (max_iter=300, max_depth=6, learning_rate unreported)
- **Reconstruction:** Can be rewritten from report descriptions + modeling_features_2010_2014.csv

### src/models/train_qr_gbt.py
- **Current state:** Skeleton with NotImplementedError
- **Expected functionality:** Train QR-GBT for quantiles q01–q99
- **Recoverability:** Reports describe quantile set but not full training config
- **Reconstruction:** Can be rewritten from quantile_predictions_2014.csv output shape

### src/evaluation/evaluate_full_year.py
- **Current state:** Skeleton with NotImplementedError
- **Recoverability:** Output metrics exist in baseline_metrics.csv and quantile_metrics.csv
- **Reconstruction:** Can be rewritten to reproduce metrics from predictions CSVs

## Environment

- The venv at `venv/` contains installed packages but no export file
- Key packages likely: scikit-learn, numpy, pandas, matplotlib
- No conda environment.yml or pip requirements.txt found
