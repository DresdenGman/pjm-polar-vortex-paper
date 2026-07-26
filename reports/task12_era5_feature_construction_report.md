# Task12 — ERA5 Feature Construction Report

**Date**: 2026-07-07  
**Status**: COMPLETE

---

## 1. What Is `great_lakes_core`?

| Property | Value |
|----------|-------|
| Type | Rectangular grid box, **simple spatial mean** (unweighted grid-cell average) |
| Latitude range | **40.0°N to 42.5°N** |
| Longitude range | **−88.0°W to −74.0°W** |
| Grid resolution | 0.25° × 0.25° (ERA5 native) |
| Grid cells | **11 lat × 57 lon = 627 cells** |
| Aggregation method | `t2m.mean(dim=['latitude', 'longitude'])` — simple arithmetic mean |
| Source file | `src/data/process_era5_2014.py` |

Full PJM bbox is 35.0–42.5°N, −88.0 to −74.0°W (1,680 cells). The great_lakes_core subset is the northern portion (40–42.5°N), selected because it better represents the cold-air mass affecting PJM load during winter events. No population weighting is applied.

---

## 2. ERA5 Variables Used

| Variable | ERA5 Name | Used? | Notes |
|----------|-----------|-------|-------|
| 2-metre temperature | `t2m` | ✅ | Primary temperature source |
| 2-metre dewpoint | `d2m` | ❌ NOT used | Not in downloaded ERA5 data |
| 10m u-component wind | `u10` | ✅ | Used for wind speed computation |
| 10m v-component wind | `v10` | ✅ | Used for wind speed computation |

Only **t2m, u10, v10** are in the ERA5 NetCDF files. d2m was listed in early planning documents but was not downloaded.

---

## 3. Unit Conversions and Derived Features

### Temperature

| Step | Formula |
|------|---------|
| ERA5 raw | Kelvin (K) |
| To Fahrenheit | **°F = (K − 273.15) × 9/5 + 32** |

### Wind Speed

| Step | Formula |
|------|---------|
| Wind speed magnitude | **ws = √(u10² + v10²)** in m/s |
| To mph | **mph = m/s × 2.23694** |

### Wind Chill

| Condition | Formula |
|-----------|---------|
| Valid when | **T ≤ 50°F AND wind speed > 3 mph** |
| Formula | **WC = 35.74 + 0.6215×T − 35.75×ws^0.16 + 0.4275×T×ws^0.16** |
| Otherwise | WC = T (temperature) |

This is the standard NOAA/NWS wind chill formula.

### Heating Degree Hours (HDH)

| Formula |
|---------|
| **HDH = max(65 − T°F, 0)** |

### Cooling Degree Hours (CDH)

| Formula |
|---------|
| **CDH = max(T°F − 65, 0)** |

Base temperature: **65°F** (standard U.S. degree-day convention).

---

## 4. Final Model Feature List (18 columns, 14 features)

| # | Column | Category | Description |
|---|--------|----------|-------------|
| 1 | `timestamp_utc` | Index | UTC timestamp (authoritative key) |
| 2 | `timestamp_ept` | Index | EPT timestamp (display) |
| 3 | `source_year` | Index | Year label (2010–2014) |
| 4 | `actual_load_mw` | Target | PJM RTO metered load |
| 5 | `hour` | Calendar | Hour of day (0–23, EPT) |
| 6 | `day_of_week` | Calendar | Day of week (0=Mon, 6=Sun) |
| 7 | `month` | Calendar | Month (1–12) |
| 8 | `is_weekend` | Calendar | Binary (1=Sat/Sun) |
| 9 | `load_lag_1h` | Lag | Load 1 hour prior (UTC) |
| 10 | `load_lag_24h` | Lag | Load 24 hours prior |
| 11 | `load_lag_168h` | Lag | Load 168 hours (1 week) prior |
| 12 | `rolling_mean_24h` | Rolling | Mean load over prior 24h |
| 13 | `rolling_mean_168h` | Rolling | Mean load over prior 168h |
| 14 | `t_f` | Weather | Temperature (°F) |
| 15 | `wc_f` | Weather | Wind chill (°F) |
| 16 | `ws` | Weather | Wind speed (mph) |
| 17 | `hdh` | Weather | Heating degree hours |
| 18 | `cdh` | Weather | Cooling degree hours |

---

## 5. NOAA / NASA Confirmation

| Source | Used in modeling table? |
|--------|:----------------------:|
| NOAA ISD station data | ❌ **NOT used** — provisional only, not in features |
| NASA AIRS imagery | ❌ **NOT used** — removed from project |

All weather features are from **ERA5 reanalysis only**.

---

## 6. Manuscript-Ready Description

For Section 2 (Data) or Section 3 (Forecasting Framework), use:

> Weather variables were obtained from ERA5 hourly reanalysis (Copernicus Climate Data Store) on a 0.25° grid over the PJM footprint (35.0–42.5°N, −88.0 to −74.0°W). A northern subset (great_lakes_core: 40.0–42.5°N) was used to compute spatially averaged 2-metre temperature (t2m), 10-metre wind components (u10, v10), and derived variables: wind speed magnitude (mph), NOAA wind chill temperature (°F), heating degree hours (HDH = max(65−T, 0)), and cooling degree hours (CDH = max(T−65, 0)). All weather variables represent same-hour retrospective reanalysis conditions and are not operational weather forecasts.

**Task12 verdict: ERA5 FEATURE CONSTRUCTION VERIFIED.**
