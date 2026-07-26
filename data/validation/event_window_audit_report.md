# Event Window Audit Report — Jan 6–8, 2014

**Date**: 2026-07-06
**Source**: `pjm_era5_modeling_table_2010_2014.csv` (43,824 rows, UTC-merged, all validated)

---

## 1. Row Count Verification

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Event window rows | 72 | **72** | ✅ |
| Min timestamp | Jan 6 00:00 EPT | `1/6/2014 12:00:00 AM` | ✅ |
| Max timestamp | Jan 8 23:00 EPT | `1/8/2014 11:00:00 PM` | ✅ |
| Forecast matched | 72 | **72** | ✅ |

## 2. Event Peak Verification

| Metric | Value |
|--------|-------|
| Peak load | **140,510.2 MW** (140.510 GW) |
| Peak timestamp | Jan 7, 2014 18:00 EPT |
| Temperature at peak | **2.1 °F** |
| Wind chill at peak | **-15.6 °F** |
| HDH at peak | **62.9 °F·h** |

## 3. Forecast Error Summary (72 matched hours)

| Metric | Value |
|--------|-------|
| MAE | 3,148 MW (3.15 GW) |
| RMSE | 3,809 MW |
| MAPE | 2.58% |
| Mean bias | **+2,402 MW** (systematic underprediction) |
| Max underprediction | -6,611 MW at Jan 8 23:00 EPT |
| Max overprediction | +6,865 MW at Jan 6 23:00 EPT |

## 4. Forbidden Values Check

| Value | Found? |
|-------|--------|
| 143,531 MW | ❌ Not found |
| 153,731 MW | ❌ Not found |
| 130,443 MW | ❌ Not found |

## 5. Data Files Generated

| File | Rows | Description |
|------|------|-------------|
| `figures/data/figure1_jan5_9_data.csv` | 120 | Jan 5–9 load + weather + forecast |
| `figures/data/figure3_jan6_8_data.csv` | 72 | Jan 6–8 load + weather |
| `data/validation/event_window_forecast_error.csv` | 72 | Jan 6–8 forecast errors |

## 6. MATLAB Scripts

| File | Description |
|------|-------------|
| `figures/src/Figure1_rebuild.m` | 2-panel: load+forecast, weather (Jan 5–9) |
| `figures/src/Figure3_rebuild.m` | 3-panel: load, T+WC, error+HDH (Jan 6–8) |

## 7. Conclusion

Event window audit passed. All 72 hours present and matched with day-ahead forecast.
Peak load 140,510 MW confirmed. No legacy values (143,531/153,731/130,443) present in any data file.
Ready for figure generation.
