# C06P — Multi-Event Study Design Protocol

**Status:** PREREGISTERED — locked before examining new model predictions
**Branch:** C06-parallel-evidence

## Candidate Named Events (PJM-documented)

| # | Event | Official Window | Duration | Source |
|---|-------|----------------|----------|--------|
| 1 | Jan 2014 Polar Vortex | Jan 6–8, 2014 | 72h | PJM, NERC reports |
| 2 | Feb 2015 Cold Event | ~Feb 14–22, 2015 ⚠️ | ~8 days ⚠️ | PJM (peak Feb 20 verified, boundaries TBD) |
| 3 | Dec 2017–Jan 2018 Cold Snap | Dec 28–Jan 7 | ~11 days | PJM |
| 4 | Winter Storm Elliott | Dec 23–25, 2022 | ~72h | PJM |

⚠️ = boundary dates need verification from official PJM documentation.

## Selection Rules (LOCKED)

1. **Event selection is independent of model forecast errors.**
2. **Official PJM named-event windows form the primary event set.**
3. **An algorithmic weather-based definition forms a sensitivity set.**
4. **Event definitions frozen before examining new predictions.**
5. **Contiguous event hours are serially dependent.**
6. **Each named event is an independent evaluation unit.**

## Algorithmic Sensitivity Definition

Uses PJM-weighted ERA5 temperature for event identification only
(NOT as forecasting input):

**Cold event:** ≥48 consecutive hours during Dec–Feb with
PJM-weighted effective temperature below the winter 5th percentile
of the full analysis period (2010–2014).

Merge two qualifying periods when gap ≤ 24 hours.

**Predefined sensitivity thresholds (run all three):**
- 2.5th percentile
- 5th percentile
- 10th percentile

Do NOT select the threshold producing the strongest result.

## Per-Event Data Requirements

For each event, record:
- event_id, official_name, official_start, official_end
- algorithmic_start, algorithmic_end
- official_source, event_selection_basis
- peak_load_time, training_cutoff
- required_PJM_load_dates, required_PJM_forecast_dates
- required_GFS_cycles (if GFS available)
- data_availability, notes

## Evaluation Protocol

- **Forecast task:** Fixed 12:00 EPT day-ahead origin
- **Validation:** Rolling-origin, expanding training window
- **Primary aggregation:** One result per event
- **Secondary aggregation:** Hourly results within each event
- **Controls:** Season- and load-matched non-extreme windows
- **Future information:** PROHIBITED

## Data Requirements Summary

| Event | PJM Load | PJM DA Forecast | GFS (if available) | ERA5 Oracle |
|-------|----------|-----------------|-------------------|-------------|
| Jan 2014 | ✅ | ✅ | Pending | ✅ |
| Feb 2015 | ✅ (need download) | ✅ (need download) | Pending | ✅ |
| Dec 2017–Jan 2018 | ❌ (need download) | ❌ | Pending | ✅ |
| Dec 2022 Elliott | ❌ (need download) | ❌ | Pending | ✅ |
