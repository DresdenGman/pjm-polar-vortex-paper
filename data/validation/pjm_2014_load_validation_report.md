# PJM 2014 Hourly Load — Official Data Validation Report

**Date**: 2026-07-06  
**Source**: PJM Data Miner 2 — Hourly Load: Metered  
**Account**: dr.dresden0416@gmail.com  
**Download params**: Start 1/1/2014 00:00, End 12/31/2014 23:59, Market Region = RTO  
**Raw file**: `~/Downloads/Hourly Load Metered.csv` (15 MB, 201,480 rows all zones)  
**Archived**: `data/raw/pjm/pjm_load_2014_rto_hourly.csv` (549 KB, 8,760 rows RTO only)

---

## 1. Raw Data Overview

| Field | Value |
|-------|-------|
| Total rows (all zones) | 201,480 |
| RTO aggregate rows | 8,760 |
| Unique RTO timestamps | 8,759 (1 DST duplicate, correct) |
| Time range | 2014-01-01 00:00 → 2014-12-31 23:00 EPT |
| Verification | 8,760 / 8,760 rows verified = True |
| DST handling | Nov 2 01:00 EPT appears twice (EDT→EST fallback); both rows retained with `dst_flag` column |

## 2. Load Statistics

| Statistic | Value |
|-----------|-------|
| Full-year minimum | **57,569.5 MW** |
| Full-year maximum | **141,677.9 MW** (Jun 17 17:00 EPT) |
| Full-year mean | (TBD) |

## 3. Winter Peak (Jan 6–8, 2014 Polar Vortex)

| Statistic | Value |
|-----------|-------|
| Jan 7 minimum | 119,189.9 MW |
| Jan 7 maximum | **140,510.2 MW** (18:00 EPT) |
| Jan 7 mean | 130,545.1 MW |
| Jan 7 08:00 (old claim) | 137,546.0 MW |
| Jan 7 18:00 (actual peak) | 140,510.2 MW |

## 4. Comparison: Old Manuscript vs. PJM Official

| Claim | Old Manuscript | PJM Official | Match? |
|-------|---------------|-------------|--------|
| Winter peak value | 143,531 MW | **140,510.2 MW** | ❌ Off by 3,021 MW |
| Winter peak time | Jan 7 08:00 | Jan 7 18:00 | ❌ Wrong hour |
| Full-year peak | (not claimed) | 141,677.9 MW (Jun 17) | — Summer peak > winter peak |
| Peak season | Implied winter-dominant | **Summer-dominant** | ❌ Fundamental framing issue |

## 5. Key Findings

1. **The old manuscript value 143,531 MW is NOT found in official PJM data.** The actual winter peak is 140,510.2 MW at 18:00 on Jan 7, 2014.

2. **The full-year peak (141,677.9 MW) occurred in summer (Jun 17), not winter.** This challenges the implicit framing of winter as the peak-demand season for PJM.

3. **The old claim of 08:00 peak is wrong.** The winter event peak occurred at 18:00 (evening ramp), consistent with residential heating load.

4. **This is AUTHORITATIVE data.** All 8,760 rows are marked `is_verified=True` by PJM.

## 6. Data Quality

- ✅ 8,760 hours = 365 days × 24 hours
- ✅ No missing hours
- ✅ 1 DST duplicate (Nov 2, correctly handled)
- ✅ All rows verified by PJM
- ✅ EPT timestamps present
- ✅ UTC timestamps present

## 7. Archived Files

| File | Description |
|------|-------------|
| `data/raw/pjm/pjm_load_2014_rto_hourly.csv` | RTO aggregate, 8,760 rows, 549 KB |

## 8. Next Steps

- [ ] Merge with ERA5 weather data → `pjm_weather_modeling_table_2014.csv`
- [ ] Verify Jan 7 18:00 peak against day-ahead forecast (if available)
- [ ] Decide: does the summer-higher-than-winter pattern affect paper framing?
- [ ] ChatGPT editorial decision: keep the winter focus or add summer comparison?

---

**Status**: AUTHORITATIVE
