# Data Directory — pjm-polar-vortex-paper

## Tracked Processed Data (in Git)

| File | Description | Rows | Source |
|------|-------------|------|--------|
| `processed/modeling_features_2010_2014.csv` | Complete modeling dataset with features | 43,656 | Generated from PJM + ERA5 pipeline |
| `results/baseline_predictions_2014.csv` | Point forecast predictions (all models, 2014) | 8,760 | Model output |
| `results/quantile_predictions_2014.csv` | Quantile forecast predictions (q01–q99, 2014) | 8,760 | QR-GBT model output |
| `results/baseline_metrics.csv` | Aggregate baseline evaluation metrics | — | Computed from predictions |
| `results/quantile_metrics.csv` | Aggregate quantile evaluation metrics | — | Computed from predictions |
| `results/calibration_by_quantile.csv` | Per-quantile calibration breakdown | — | Computed from predictions |

## Excluded Raw Data (not in Git)

### ERA5 Reanalysis
| File Pattern | Provider | Resolution | Years | Regenerable? |
|-------------|----------|------------|-------|-------------|
| `raw/era5/era5_YYYY_QQ.nc` | ECMWF Copernicus CDS | Hourly, 0.25° | 2010–2014 | ✅ Yes, via CDS API |

### PJM Load Data
| File Pattern | Provider | Resolution | Years | Regenerable? |
|-------------|----------|------------|-------|-------------|
| `raw/pjm/pjm_load_YYYY_rto_hourly.csv` | PJM Data Miner 2 | Hourly, RTO-level | 2010–2014 | ✅ Yes, via PJM Data Miner 2 |

### NOAA Station Data
| File Pattern | Provider | Resolution | Years | Regenerable? |
|-------------|----------|------------|-------|-------------|
| `raw/noaa/*.csv` | NOAA NCEI | Hourly, station-level | 2014 | ✅ Yes, via NOAA API |

## Expected Local Paths

After downloading, raw data should be placed under:
```
data/raw/era5/    → ERA5 NetCDF files (excluded from Git)
data/raw/pjm/     → PJM CSV files (excluded from Git)
data/raw/noaa/    → NOAA station CSV files (excluded from Git)
```

## Regeneration

Data can be regenerated via:
1. ERA5: `src/data/download_era5.py` (to be written) — requires CDS API key
2. PJM: Manual download from PJM Data Miner 2 → place in `data/raw/pjm/`
3. Build features: `src/data/build_modeling_features.py` (to be written)

## Provenance

See `data/provenance/data_sources.csv` for detailed source tracking.
