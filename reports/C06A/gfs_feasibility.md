# C06A — GFS Feasibility Audit

**Date:** 2026-07-26
**Branch:** C06-gfs-day-ahead
**Status:** FAILED

## Archive Search Results

| Archive Path | Earliest Available | 2014 Data? |
|-------------|-------------------|------------|
| GFS 0.5° forecast | 2019-08 | ❌ NO |
| GFS 1.0° forecast | 2016-06 | ❌ NO |
| GFS Legacy grids | 2003-01 to 2005-05 | ❌ NO |
| NDGD historical | 2011-01 to 2020-05 | ✅ YES (but analysis/guidance, not forecast) |

## Conclusion

**STOP_AND_REVISE_GFS_PROTOCOL**

GFS deterministic forecast data for 2010–2014 is NOT available through the
standard NCEI public archive. All three resolution tiers (0.5°, 1.0°, legacy)
have gaps covering the study period.

## Available Weather Data for 2014

| Source | Type | Coverage | Usable as Operational? |
|--------|------|----------|----------------------|
| ERA5 | Reanalysis | 2010–2014, hourly | ❌ NO (retrospective only) |
| NDGD | Analysis/Guidance | 2011–2020, hourly | ❌ NO (not forecast, not NDFD) |
| GFS 0.5° | Forecast | 2019+ | ❌ NO (wrong period) |
| NOAA station | Observations | 2014, 9 stations | ❌ NO (point obs, not gridded forecast) |

## Recommendation

Given the comprehensive unavailability of 2014 operational weather forecasts
through public archives, the project faces a fundamental data constraint:

1. **Proceed with ERA5 oracle only** — Acknowledge the limitation explicitly
   in the manuscript. Frame the work as "retrospective stress-testing under
   idealized weather information" rather than "operational day-ahead forecasting."
   
2. **Investigate alternative sources** — Possible routes include:
   - NCAR Research Data Archive (RDA) — may hold GFS 0.5° for 2014
   - ECMWF MARS archive — operational IFS forecasts for 2014
   - Direct data request to NOAA/NCEP
   
3. **Accept the limitation and pivot** — The C04S paper's core contribution
   (extreme-event calibration failure) does NOT require operational weather
   comparison. The PJM comparator already represents the operational
   benchmark. ERA5 oracle provides the upper-bound reference.

## GFS Product Definition (for reference)

| Field | Value |
|-------|-------|
| Dataset | NCEI GFS historical forecast |
| Product | grid-004-0.5-degree |
| Format | GRIB2 |
| Cycle | 06Z (target) |
| Archive URL | https://www.ncei.noaa.gov/data/global-forecast-system/access/historical/forecast/grid-004-0.5-degree/ |
| 2014 availability | ❌ NOT AVAILABLE |
