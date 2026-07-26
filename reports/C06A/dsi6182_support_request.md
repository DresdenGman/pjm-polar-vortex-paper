# C06A — DSI 6182 Support Request

**Date:** 2026-07-26
**Attempted contact:** ncei.orders@noaa.gov

## Request

We are requesting historical GFS 0.5-degree operational forecast data
for a small sample of 4 dates in 2014:

**Dataset:** NCEI DSI 6182 (Global Forecast System 0.5 Degree)
**Format:** GRIB2
**Cycle:** 06Z only

**Sample dates and 06Z cycle files needed:**
- 2014-01-06 06Z (forecast hours 018–048, for target date 2014-01-07)
- 2014-03-08 06Z (forecast hours 018–048, for target date 2014-03-09)
- 2014-07-14 06Z (forecast hours 018–048, for target date 2014-07-15)
- 2014-11-01 06Z (forecast hours 018–048, for target date 2014-11-02)

**Variables needed:**
- 2-m temperature
- 2-m relative humidity or specific humidity
- 2-m dew-point temperature (if directly available)
- 10-m U and V wind components
- Surface pressure

**Spatial subset (if supported):** 35°N–44°N, 86°W–73°W

**Status:** AIRS web system returned 500 error on 2026-07-26.
Awaiting response from NCEI.

## AIRS Attempt Log
- URL: https://www.ncei.noaa.gov/has/HAS.FileAppRouter?datasetname=6182
- Result: HTTP 500 Internal Server Error
- Timestamp: 2026-07-26T20:17:06Z
