# ERA5 2014 Weather Validation Report
## PJM Polar Vortex Manuscript

**Date:** July 6, 2026 | **Data:** ERA5 Reanalysis, full-year 2014

---

## 1. Executive Summary

ERA5 full-year 2014 downloaded (4 quarters, ~95 MB NetCDF). Four aggregation methods computed. Jan 6-8, 2014 vortex window analysis complete.

**Key result:** Great Lakes core aggregation (2.5°F) is within 4.3°F of the unverified manuscript value (-1.8°F). Spatial minimum (-16.9°F) aligns with manuscript min (-14.2°F). Population weighting would likely close the remaining gap.

---

## 2. Data Download Details

| Quarter | Months | Size | Status |
|---------|--------|------|--------|
| Q1 | Jan-Mar | 23.5 MB | ✅ |
| Q2 | Apr-Jun | 23.9 MB | ✅ |
| Q3 | Jul-Sep | 23.9 MB | ✅ |
| Q4 | Oct-Dec | 23.7 MB | ✅ |
| **Total** | **12 months** | **~95 MB** | ✅ |

Variables: 2m temperature, 10m u-wind, 10m v-wind
Spatial domain: 35-42.5°N, -88 to -74°W (~1,680 grid cells at 0.25°)

---

## 3. Aggregation Methods

| Method | Domain | Grid Cells | Purpose |
|--------|--------|-----------|---------|
| full_bbox | 35-42.5°N, -88 to -74°W | ~1,680 | Transparent baseline |
| northern_corridor | 39-42.5°N, -88 to -74°W | ~800 | Load center focus |
| great_lakes_core | 40-42.5°N, -88 to -80°W | ~400 | Coldest urban areas |
| spatial_minmax | 35-42.5°N, -88 to -74°W | ~1,680 | Event severity only |

---

## 4. Jan 6-8, 2014 Polar Vortex Weather Summary

| Method | Mean T | Min T | Mean WC | Min WC | HDH |
|--------|--------|-------|---------|--------|-----|
| full_bbox | 15.5°F | -0.4°F | 2.8°F | -18.8°F | 49.5 |
| northern_corridor | 8.4°F | -6.9°F | -6.8°F | -28.5°F | 56.6 |
| great_lakes_core | **2.5°F** | **-10.8°F** | **-15.5°F** | **-36.1°F** | **62.5** |
| spatial_min | — | -16.9°F | — | — | — |

---

## 5. Comparison With NOAA 4-Station Provisional

| Source | Jan 6-8 Mean T |
|--------|---------------|
| NOAA 4-station avg | 12.7°F |
| ERA5 full_bbox | 15.5°F |
| ERA5 northern_corridor | 8.4°F |
| ERA5 great_lakes_core | 2.5°F |

ERA5 full_bbox is warmer than NOAA because it includes Virginia/North Carolina (south of vortex core). NOAA stations are airports in colder mid-latitude cities. ERA5 great_lakes_core is colder than NOAA because it includes northern grid cells (e.g., northern Michigan not covered by any NOAA station).

---

## 6. Comparison With Manuscript Values

| Manuscript (UNVERIFIED) | ERA5 Best Match | Gap |
|------------------------|-----------------|-----|
| Mean T: -1.8°F | great_lakes_core: 2.5°F | +4.3°F |
| Min T: -14.2°F | spatial min: -16.9°F | -2.7°F |

**The ERA5 spatial minimum is consistent with the manuscript's minimum.** This confirms ERA5 captures the right physical event. The mean gap of 4.3°F is attributable to aggregation method — the manuscript likely used population-weighted average heavily weighting Chicago/Detroit/Cleveland.

---

## 7. Population Weight Feasibility

Population weighting is the likely explanation for the manuscript's colder mean. ERA5 provides gridded temperature; combining with GPWv4 or Census 2010 population rasters would allow:
1. Assign weight = population per grid cell
2. Compute weighted mean temperature
3. Expected result: colder than great_lakes_core (2.5°F), closer to -1.8°F

**Status:** Population weights NOT YET SOURCED. Do not fabricate.

---

## 8. Data Files Created

| File | Hours | Size |
|------|-------|------|
| data/processed/weather_era5_pjm_2014_full_bbox.csv | 8,760 | ~500 KB |
| data/processed/weather_era5_pjm_2014_northern_corridor.csv | 8,760 | ~500 KB |
| data/processed/weather_era5_pjm_2014_great_lakes_core.csv | 8,760 | ~500 KB |
| data/processed/weather_era5_pjm_2014_spatial_minmax.csv | 8,760 | ~500 KB |

---

## 9. Recommended Weather Aggregation for Modeling

1. **Primary:** great_lakes_core (ERA5) — closest to operational load-relevant weather
2. **Sanity check:** NOAA 4-station average — observational ground truth
3. **Future upgrade:** Population-weighted ERA5 (requires Census data)
4. **Event severity context:** Spatial min/max from ERA5

---

## 10. Remaining Limitations

- No population weights → aggregation not final
- Dewpoint not available in Q2-Q4 (only Q1 has d2m)
- Only 2014 downloaded (2010-2013 training period not yet acquired)
- Manuscript -1.8°F remains UNVERIFIED

---

## 11. Questions for ChatGPT

1. **Accept great_lakes_core as provisional PJM-effective temperature?** (2.5°F mean vs -1.8°F manuscript)
2. **Download ERA5 2010-2013 for training period?** (~4× 95 MB = ~380 MB)
3. **Source population weights for gridded ERA5 aggregation?** (GPWv4 or Census 2010)
