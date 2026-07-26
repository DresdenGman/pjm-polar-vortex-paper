# C06A — GFS Product Definition

**Status:** NOT AVAILABLE for 2014

| Field | Value |
|-------|-------|
| Dataset identifier | NCEI GFS historical forecast |
| Product family | GFS deterministic |
| Grid resolution | 0.5° (grid-004) |
| File format | GRIB2 |
| Target cycle | 06Z |
| Forecast-hour range | 0–384h (nominal) |
| Archive endpoint | ncei.noaa.gov/data/global-forecast-system/access/historical/forecast/grid-004-0.5-degree/ |
| Variable names (expected) | TMP (2m temp), RH (2m RH), UGRD/VGRD (10m wind) |
| Units | K, %, m/s |
| 2014 availability | ❌ Earliest available: 2019-08 |
| Fallback 1.0° | ❌ Earliest available: 2016-06 |
| Fallback legacy grids | ❌ Range: 2003-01 to 2005-05 |
| December 2014 transition | N/A — no 2014 data |

## Archive Search Summary

```
GFS 0.5° forecast: 201908 → 202005 (earliest available)
GFS 1.0° forecast: 201606 → present (gap: 2010–2015)
GFS Legacy grids:  200301 → 200505 (pre-2015 upgrade)
NDGD analysis:     201101 → 202005 (available for 2014, but analysis/guidance)
```

## NCEI GFS Archive Structure

```
ncei.noaa.gov/data/global-forecast-system/access/
├── grid-003-1.0-degree/
│   ├── analysis/     → current only (2025+)
│   └── forecast/     → 202512+, historical: 201606+
├── grid-004-0.5-degree/
│   ├── analysis/     → current only
│   └── forecast/     → 202512+, historical: 201908+
└── historical/
    ├── analysis/     → empty
    └── forecast/
        ├── grid-003-1.0-degree/  → 201606+
        ├── grid-004-0.5-degree/  → 201908+
        └── legacy-grids/         → 200301–200505
```

## Conclusion

GFS 2014 data gap is comprehensive: no 0.5°, 1.0°, or legacy product covers
2010–2014. This is a permanent archive limitation, not a temporary outage.
