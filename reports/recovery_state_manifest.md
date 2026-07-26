# Recovery State Manifest

**Generated**: 2026-07-06 08:30  
**Trigger**: Cross-chat confusion recovery  

## File Inventory (SHA256 truncated to 16 chars)

| Path | Size | Rows | SHA256 | Status |
|------|------|------|--------|--------|
| data/processed/modeling_features_2010_2014.csv | 6,801,298 | 43,656 | 29df94f19d26639c | VALID |
| data/results/baseline_predictions_2014.csv | 1,127,325 | 8,760 | eeebe5582b32510a | VALID |
| data/results/baseline_metrics.csv | 1,749 | 12 | fc2107c062a6c809 | VALID |
| data/processed/pjm_era5_modeling_table_2010_2014.csv | 4,371,221 | 43,824 | f65063450604984b | AUTHORITATIVE |
| data/raw/pjm/pjm_load_2010_rto_hourly.csv | 653,036 | 8,760 | 8192732c82feb869 | AUTHORITATIVE |
| data/raw/pjm/pjm_load_2011_rto_hourly.csv | 653,217 | 8,760 | b9bc6a4f262ceb1b | AUTHORITATIVE |
| data/raw/pjm/pjm_load_2012_rto_hourly.csv | 655,532 | 8,784 | de97e455b6864696 | AUTHORITATIVE |
| data/raw/pjm/pjm_load_2013_rto_hourly.csv | 654,134 | 8,760 | cc5114bcfcfa8114 | AUTHORITATIVE |
| data/raw/pjm/pjm_load_2014_rto_hourly.csv | 654,437 | 8,760 | 2521669aa2c3c76c | AUTHORITATIVE |
| data/raw/pjm/pjm_load_2010_2014_rto_hourly.csv | 3,489,088 | 43,824 | af7f0f9220e3bfbe | AUTHORITATIVE |
| data/raw/pjm/pjm_day_ahead_forecast_2014_clean.csv | 621,615 | 8,759 | 692c6a569f0d1280 | AUTHORITATIVE |
| data/processed/weather_era5_pjm_2010_2014_great_lakes_core.csv | 2,715,806 | 43,829 | b309bd30f1748b96 | AUTHORITATIVE |
| reports/task07a_baseline_modeling_report.md | 3,709 | — | — | PROVISIONAL (superseded by audit) |
| reports/task07a_validity_audit.md | — | — | — | AUTHORITATIVE (this audit) |

## Provenance

All PJM data: PJM Data Miner 2, downloaded 2026-07-06 by user  
All ERA5 data: CDS API, reanalysis-era5-single-levels, great_lakes_core aggregation  
Day-ahead forecast: PJM Historical Load Forecasts feed  
No legacy_unverified data used in Task07A  

## Task07A Validity

**VERDICT: VALID** — see `reports/task07a_validity_audit.md` for full audit.
