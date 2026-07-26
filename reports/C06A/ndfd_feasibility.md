# C06A — NDFD Feasibility Audit

**Date:** 2026-07-26
**Branch:** C06-day-ahead

## Archive Access

| Field | Value |
|-------|-------|
| Archive | NOAA NCEI National Digital Guidance Database (NDGD) |
| URL | `https://www.ncei.noaa.gov/data/national-digital-guidance-database/access/historical/` |
| Coverage | 2011-01 through 2020-05 |
| 2014 data | ✅ AVAILABLE (201401 through 201412) |
| Format | GRIB2 (NCEP/WMO standard) |
| Organization | Year-month / day / product_directory |
| Product checked | LEIA98_KWBR (total precipitation) |

## Sample Test: Jan 6, 2014 (Polar Vortex Day -1)

| Field | Value |
|-------|-------|
| Issue time | 00:00, 06:00, 12:00, 18:00 UTC (synoptic cycles) |
| Lead time | 1 hour (step=3600s) |
| Variables in LEIA98 | tp (total precipitation) only |
| Temperature product | NOT in LEIA98 — needs different product code |
| Dew point product | NOT in LEIA98 |
| Wind speed product | NOT in LEIA98 |

## Products Needed (Not Yet Identified)

For full day-ahead protocol, we need GRIB2 products containing:
- 2m temperature (TMP)
- 2m dew point (DPT)
- 10m wind speed (WIND)
- Issued at 00Z or 06Z with lead times ≥ 24h (to cover D with issue time ≤ 12:00 EPT = 17:00 UTC)

## Archive Limitation

The LEIA98 product contains only precipitation at 1h lead. For temperature/wind,
different NDFD/NCEP product codes must be identified. The NDGD archive likely
contains these under different directory names (e.g., LEIxxx codes).

## Coverage Assessment (PRELIMINARY)

| Variable | 2014 Available? | Format | Issue ≤ Origin? | Lead ≥ 24h? |
|----------|----------------|--------|-----------------|-------------|
| Temperature | ❓ Unknown | Need product code | ❓ | ❓ |
| Dew point | ❓ Unknown | Need product code | ❓ | ❓ |
| Wind speed | ❓ Unknown | Need product code | ❓ | ❓ |
| Precipitation | ✅ LEIA98 | GRIB2, 1h steps | ✅ (00/06/12/18Z) | ❌ (1h only) |

## Decision Status

**PRELIMINARY: CANNOT yet confirm NDFD feasibility.** The archive exists and
2014 data is accessible, but the specific temperature/dew point/wind speed
products with sufficient lead time (≥24h from a pre-origin issue time) have
not been identified. Full product code inventory needed.

## Next Step (if PROCEED)

1. Inventory all NDGD product codes for 2014-01-07
2. Identify temperature/dew point/wind products with ≥24h lead
3. Download 10-date sample and verify spatial coverage over PJM domain
4. Verify all issue times ≤ 12:00 EPT origin

## Recommendation

**STOP_AND_REVISE_PROTOCOL** — The operational weather input track cannot
currently be validated as feasible. Recommend either:
- (a) Proceed with ERA5 oracle benchmark while continuing NDFD investigation, or
- (b) Investigate alternative operational weather archives (GFS, NAM, RAP)
  that may have more accessible 2014 forecast data
