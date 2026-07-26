# C06A — Forecast Protocol Documentation

**Branch:** C06-day-ahead
**Date:** 2026-07-26
**Purpose:** Define a leakage-free, like-for-like day-ahead forecasting protocol

---

## 1. Problem Statement

C04S compared a 1-hour-ahead model (using same-hour ERA5 reanalysis) against PJM's ~24-hour-ahead
operational forecast. This is not a like-for-like comparison because:
- Different forecast horizons (1h vs ~24h)
- Different load-information cutoffs (t-1h vs ~t-24h)
- Different weather information (retrospective reanalysis vs operational NWP)

C06A establishes a strict protocol where ALL models use the same forecast origin,
load-information cutoff, and weather forecast vintage.

---

## 2. Forecast Origin

**Rule:** 12:00 America/New_York (EPT) on day D-1

For each operating date D, all predictions are issued from a single forecast
origin at noon EPT on the day before. This yields target-hour leads of
approximately 12–35 hours across the following operating day.

## 3. Load-Information Cutoff

**Rule:** Latest usable metered load = forecast_origin - 1 hour

No predictor may use a load observation later than 11:00 EPT on D-1.

## 4. PJM Comparator Selection

For each target operating date:
1. Select the latest PJM forecast created at or before 12:00 EPT origin
2. Require creation time ≤ 12 hours before origin
3. Use ONLY forecast values from that selected vintage
4. Never select a later revision per target hour
5. Exclude days with no qualifying complete vintage

## 5. Weather Forecast Vintage

**Rule:** weather_issue_time ≤ forecast_origin

All target-hour weather values must come from ONE forecast vintage available
by the origin. Do not cherry-pick the best cycle after seeing realized errors.

## 6. Three Weather Tracks

### Track A: Operational — NDFD
- **Source:** NOAA/NWS National Digital Forecast Database
- **Type:** Archived operational gridded forecasts
- **Role:** PRIMARY weather input for C06 models
- **Status:** To be downloaded

### Track B: Oracle — ERA5
- **Source:** ECMWF ERA5 Reanalysis
- **Type:** Retrospective same-hour reanalysis
- **Role:** Upper-bound benchmark (perfect weather knowledge)
- **Status:** Already downloaded
- ⚠️ MUST NOT be described as operational input

### Track C: Sensitivity — GEFSv12
- **Source:** NOAA GEFSv12 Reforecasts
- **Type:** Fixed-model retrospective forecasts (00 UTC daily)
- **Role:** Hindcast sensitivity analysis
- **Status:** Not yet downloaded
- ⚠️ NOT actual historical forecast vintages

## 7. Daylight Saving Time

Do NOT delete or duplicate DST transition hours. Operating days may
contain 23, 24, or 25 hourly observations. All timestamps converted
to UTC internally; America/New_York retained as calendar timezone.

## 8. Implementation

PRIMARY NDFD source. GEFSv12 for sensitivity only.

## 9. Next Steps after Protocol Lock

1. Audit PJM forecast vintages for 2014
2. Download NDFD operational forecasts for 2010–2014
3. Construct aligned feature set with common load cutoff
4. Retrain all models under strict day-ahead protocol
5. Compare against PJM using like-for-like vintages
