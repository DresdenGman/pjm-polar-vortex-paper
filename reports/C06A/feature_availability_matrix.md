# C06A — Feature Availability Matrix

**Branch:** C06-preload-readiness
**Source:** `modeling_features_2010_2014.csv` (18 columns)

## C04S Feature Audit

| # | Feature | Construction Rule | Latest Source Timestamp | Available at 12:00 D-1? | Classification | Replacement |
|---|---------|-------------------|------------------------|------------------------|----------------|-------------|
| 1 | hour | Calendar | N/A | ✅ | DAY_AHEAD_ALLOWED | — |
| 2 | day_of_week | Calendar | N/A | ✅ | DAY_AHEAD_ALLOWED | — |
| 3 | month | Calendar | N/A | ✅ | DAY_AHEAD_ALLOWED | — |
| 4 | is_weekend | Calendar derivative | N/A | ✅ | DAY_AHEAD_ALLOWED | — |
| 5 | load_lag_1h | t-1h load | t-1h | ❌ (t-1h > origin-1h) | PROHIBITED_LEAKAGE | load_origin_minus_1h |
| 6 | load_lag_24h | t-24h load | t-24h | ✅ | DAY_AHEAD_ALLOWED | load_same_hour_1d |
| 7 | load_lag_168h | t-168h load | t-168h | ✅ | DAY_AHEAD_ALLOWED | load_same_hour_7d |
| 8 | rolling_mean_24h | Windows ending at t | t | ❌ (contains t-1h..t) | PROHIBITED_LEAKAGE | previous_daily_mean |
| 9 | rolling_mean_168h | Windows ending at t | t | ❌ (contains t-1h..t) | PROHIBITED_LEAKAGE | remove or lag-corrected |
| 10 | t_f | ERA5 same-hour temperature | t | ❌ (ERA5 not operational) | ORACLE_ONLY | GFS temperature |
| 11 | wc_f | ERA5 wind chill (derived) | t | ❌ (ERA5 not operational) | ORACLE_ONLY | GFS wind chill |
| 12 | ws | ERA5 wind speed (derived) | t | ❌ (ERA5 not operational) | ORACLE_ONLY | GFS wind speed |
| 13 | hdh | ERA5 heating degree hours | t | ❌ (ERA5 not operational) | ORACLE_ONLY | GFS heating degree |
| 14 | cdh | ERA5 cooling degree hours | t | ❌ (ERA5 not operational) | ORACLE_ONLY | GFS cooling degree |
| 15 | timestamp_utc | Not a feature | N/A | N/A | NOT_USED_IN_C06 | — |
| 16 | timestamp_ept | Not a feature | N/A | N/A | NOT_USED_IN_C06 | — |
| 17 | source_year | Not a feature | N/A | N/A | NOT_USED_IN_C06 | — |
| 18 | actual_load_mw | Target variable | N/A | N/A | NOT_USED_IN_C06 | — |

## Summary

| Classification | Count |
|----------------|-------|
| DAY_AHEAD_ALLOWED | 5 |
| ORACLE_ONLY | 5 |
| PROHIBITED_LEAKAGE | 3 |
| NOT_USED_IN_C06 | 5 |
| **Total** | **18** |

## Key Removals

1. **load_lag_1h** → PROHIBITED. Replaced by `load_origin_minus_1h`
2. **rolling_mean_24h, rolling_mean_168h** → PROHIBITED. Windows include post-origin data
3. **All ERA5 weather** → ORACLE_ONLY. Not available at forecast origin
