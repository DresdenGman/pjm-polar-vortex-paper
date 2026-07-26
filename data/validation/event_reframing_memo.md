# Event Reframing Memo — PJM 2014 Polar Vortex

**Date**: 2026-07-06  
**Status**: EDITORIAL DECISION REQUIRED — for ChatGPT/core editor review before any modeling  
**Data**: AUTHORITATIVE (PJM Data Miner 2 official RTO hourly load, all 8,760 rows verified)

---

## 1. Executive Summary

Official PJM 2014 RTO hourly load data have been obtained and validated. Three core findings invalidate the old manuscript's factual basis:

1. **143,531 MW does not exist** in PJM 2014 official data.
2. **The January 7 event peak is 140,510.2 MW at 18:00 EPT** (not 143,531 at 08:00).
3. **The 2014 annual peak is 141,677.9 MW on June 17 at 17:00** — summer exceeds winter.

However, the January 2014 Polar Vortex event remains an exceptionally strong case study: the Jan 7 peak of 140,510 MW sits at the **99.98th percentile** of all 2014 hours and is only **1,168 MW (0.82%) below** the annual maximum.

**Recommended new framing**: "A near-annual-peak cold-weather stress test for probabilistic electricity demand forecasting."

---

## 2. Old Manuscript Claims Invalidated

| Old Claim | PJM Official | Verdict |
|-----------|-------------|---------|
| "143,531 MW winter peak" | 140,510.2 MW | ❌ Value fabricated or sourced from non-official data |
| "Peak at Jan 7 08:00" | Peak at Jan 7 18:00 | ❌ Wrong hour; actual peak is evening ramp, not morning |
| "Winter record peak" | Summer peak is higher | ❌ Not the annual peak |
| "Only 641 MW below all-time peak" | Not applicable | ❌ Reference value itself is invalid |
| "153,731/153,732 MW" (legacy embedded) | Not in PJM data | ❌ Legacy artifact, not PJM-verified |

**All of the above must be permanently removed from the manuscript.**

---

## 3. Official PJM 2014 Load Facts

| Statistic | Value |
|-----------|-------|
| Annual peak | **141,677.9 MW** — Jun 17, 17:00 EPT [SUMMER] |
| Jan 6–8 peak | **140,510.2 MW** — Jan 7, 18:00 EPT [WINTER] |
| Jan 7 08:00 load | 137,546.0 MW |
| Jan 7 18:00 load | 140,510.2 MW |
| Full-year mean | 91,034.4 MW |
| Full-year min | 57,569.5 MW |
| Jan 6–8 mean | 120,068.8 MW |
| Jan 7 mean | 130,545.1 MW |

### Top 10 load hours in 2014

| Rank | Timestamp | MW | Season |
|------|-----------|-----|--------|
| 1 | Jun 17 17:00 | 141,677.9 | SUMMER |
| 2 | Jun 17 16:00 | 141,356.6 | SUMMER |
| 3 | **Jan 7 18:00** | **140,510.2** | **WINTER** |
| 4 | Jan 7 19:00 | 140,128.5 | WINTER |
| 5 | Jun 17 15:00 | 139,608.4 | SUMMER |
| 6 | Jun 18 16:00 | 139,517.3 | SUMMER |
| 7 | Jul 1 17:00 | 139,379.9 | SUMMER |
| 8 | Jul 1 16:00 | 139,326.9 | SUMMER |
| 9 | Jun 17 18:00 | 139,203.3 | SUMMER |
| 10 | Jun 18 17:00 | 139,072.9 | SUMMER |

**Key observation**: The top 10 is dominated by summer (8 of 10). Jan 7 appears at #3 and #4 — it is a near-peak winter outlier, not the annual maximum.

---

## 4. Percentile Analysis

| Context | Jan 7 18:00 Percentile |
|---------|----------------------|
| Full-year 2014 (8,760 hours) | **99.98%** (rank 8,758/8,760) |
| Winter DJF only (2,160 hours) | **100.00%** (rank 2,160/2,160) |
| Jan 6–8 event window (72 hours) | **100.00%** |

| Metric | Value |
|--------|-------|
| Jan 6–8 peak / annual peak | **99.18%** |
| Gap to annual peak | 1,167.7 MW (0.82%) |

---

## 5. Legacy Value Search

| Value searched (±100 MW) | Found in PJM 2014? |
|--------------------------|---------------------|
| 143,531 MW | **NO** |
| 153,731 MW | **NO** |

Neither legacy embedded value appears anywhere in the official 2014 PJM RTO data.

---

## 6. Why the Old Winter-Record Framing Must Be Removed

1. **Factually wrong**: The event was not the annual peak, and the stated value was inaccurate.
2. **Wrong time**: The peak was at 18:00 (evening ramp), not 08:00 (morning ramp). This changes the physical interpretation — evening peaks are driven by residential heating + lighting, not industrial morning ramp.
3. **Wrong season dominance**: PJM 2014 was summer-peaking, not winter-peaking. Framing the paper around "winter record" implies the wrong grid characteristic.
4. **Credibility risk**: Any reviewer who checks PJM Data Miner 2 will immediately find these discrepancies. The paper must be correct on verifiable facts.

---

## 7. Whether Jan 2014 Still Works as a Case Study

**Yes — strongly.**

Evidence:
- Jan 7 18:00 is the **#3 highest hour of the entire year**
- It is the **#1 winter hour** (by a large margin: #2 winter hour is only 137,336 MW on Jan 28)
- **7 of the top 10 winter hours are from Jan 7 alone** — the event concentrated extreme winter load
- The gap to the annual peak is only **0.82%** — for practical grid operations, this is a near-peak event
- The event has exceptional weather severity (ERA5 Great Lakes core mean T = 2.5°F, min = -10.8°F)
- The combination of extreme cold + near-annual-peak load makes it ideal for testing forecast performance under stress

**New framing**: This is not a "record winter peak" paper. It is a **cold-weather near-annual-peak probabilistic forecasting stress test**.

---

## 8. Recommended New Framing

**Title direction** (not final):
> "Probabilistic Load Forecasting Under Extreme Cold Weather: A Near-Annual-Peak Stress Test Using the January 2014 Polar Vortex"

**Key narrative shifts**:

| Old | New |
|-----|-----|
| "Record winter peak of 143,531 MW" | "Near-annual-peak cold-weather event reaching 140,510 MW (99.2% of 2014 maximum)" |
| "Peaked at 08:00" | "Peaked at 18:00 during evening ramp" |
| "Winter-dominant grid" | "Summer-peaking grid with extreme winter outlier events" |
| "Record-setting event" | "Stress-test event: extreme cold driving load to within 1% of annual peak" |

---

## 9. Claims to Delete

Permanently remove:
- "143,531 MW"
- "winter record peak"
- "only 641 MW below all-time peak"
- "Jan 7 08:00 peak"
- "153,731/153,732 MW"
- Any reference to "NASA/AIRS" unless provenance is verified
- Any claim that PJM is winter-peaking in 2014

---

## 10. Claims That Remain Defensible

- The January 2014 Polar Vortex was an extreme cold-weather event
- PJM load reached near-annual-peak levels (within 1%)
- The event concentrated extreme winter load (7 of top 10 winter hours on Jan 7)
- Probabilistic forecasting under such conditions is a meaningful research question
- Weather-load relationships during extreme cold are worth modeling
- ERA5 and NOAA data confirm exceptional cold (mean T = 2.5°F Great Lakes core)

---

## 11. Implications for Figures and Tables

| Old Figure | Status |
|------------|--------|
| Figure 1 (load curve with 143,531 peak) | Must be regenerated from PJM official data |
| Figure 2 (capacity projection) | Removed — not relevant to new framing |
| Figure 3 (temperature back-calculated) | Must use ERA5 actual temperature |
| Figure 5 (unknown model pipeline) | Must be rebuilt from verified data |

**New figures should reflect**: near-peak framing, summer vs. winter comparison optional, Jan 7 evening peak timing, ERA5-verified weather.

---

## 12. Recommended Next Task

1. **Download PJM 2010–2013** (user manual download needed) — to establish multi-year context
2. **Download PJM day-ahead forecast 2014** — to enable forecast error analysis
3. **Merge 2014 PJM load × ERA5 weather** — diagnostic only, no modeling yet
4. **ChatGPT editorial decision** on exact framing, title direction, figure plan

---

## 13. Questions for ChatGPT/Core Editor

1. Accept "near-annual-peak cold-weather stress test" framing?
2. Should we add a summer-peak comparison section (Jun 17, 2014)?
3. Should we wait for 2010–2013 before any modeling, or proceed with 2014-only exploratory?
4. New title: keep "Polar Vortex" in title or generalize?
5. Should we add a figure showing full-year load distribution with Jan 7 marked?
