# C06A — DSI 6182 Order Request

**Date:** 2026-07-26
**Branch:** C06-gfs-dsi6182
**Status:** SENT — 2026-07-26 13:37 ET, from dr.dresden0416@gmail.com to ncei.orders@noaa.gov

## Dataset

| Field | Value |
|-------|-------|
| Dataset name | Global Forecast System (GFS) 0.5 Degree |
| NCEI DSI | 6182 |
| Metadata ID | gov.noaa.ncdc:C00634 |
| Archive period | 2006-02-01 to present |
| Access mode | NCEI AIRS (Archive Information Request System) |
| URL | https://www.ncei.noaa.gov/has/HAS.FileAppRouter?datasetname=6182 |

## Request Details

### Sample Dates (4 operating days)
- 2014-01-07 (Polar vortex day)
- 2014-03-09 (Spring DST)
- 2014-07-15 (Summer peak)
- 2014-11-02 (Fall DST)

### For each date: 06Z cycle on D-1
| Date | Request 06Z on |
|------|---------------|
| 2014-01-07 | 2014-01-06 06Z |
| 2014-03-09 | 2014-03-08 06Z |
| 2014-07-15 | 2014-07-14 06Z |
| 2014-11-02 | 2014-11-01 06Z |

### Forecast Hours
f018, f021, f024, f027, f030, f033, f036, f039, f042, f045, f048
(18–48 hours at 3-hour intervals, covering all target leads)

### Variables Requested
- 2-m temperature (TMP)
- 2-m relative humidity (RH) or specific humidity (SPFH)
- 2-m dew-point temperature (DPT), if directly available
- 10-m U wind component (UGRD)
- 10-m V wind component (VGRD)
- Surface pressure (PRES)

### Spatial Subset (if supported)
- Latitude: 35°N to 44°N
- Longitude: 86°W to 73°W (PJM region)

## Delivery
- Method: Direct download if available, or FTP staging
- Format: GRIB2

## AIRS Order Attempt
- System URL: https://www.ncei.noaa.gov/has/HAS.FileAppRouter?datasetname=6182
- Attempted: 2026-07-26
- Result: System requires interactive form submission
- Note: AIRS may require email-based order with specific DSI/date/cycle parameters

## Contact
- ncei.orders@noaa.gov
- nomads.ncdc@noaa.gov

## Next Action
Submit formal order through AIRS web interface or email. The automated
script-based submission is not feasible — AIRS requires interactive
parameter selection.
