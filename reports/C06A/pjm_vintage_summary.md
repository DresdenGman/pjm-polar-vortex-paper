# C06A — PJM Vintage Inventory Summary

**Date:** 2026-07-26
**Branch:** C06-day-ahead

## Audit Results

| Metric | Value |
|--------|-------|
| Total forecast rows (2014) | 8,759 |
| Unique forecast creation times | 1,826 |
| Avg vintages per day | ~5 |
| Creation time range | 2013-12-31 to 2014-12-30 |
| Operating days | 365 |
| **Protocol-qualifying days** | **365/365 (100%)** |
| Age at origin (mean) | 0.2 hours |

## Key Finding

All 365 operating days in 2014 have a PJM forecast vintage available at or
before the 12:00 EPT origin, within the 12-hour age limit. The strict
protocol can be applied without excluding any days.

The 8,759 rows (vs 8,760 expected hours) is consistent with the March 2014
DST "spring forward" transition, which produces a 23-hour day.

## Vintage Structure

The CSV appears to contain pre-selected vintages (one per forecast issuance),
not all possible PJM forecast revisions. Each row's `evaluated_at_ept` is
the publication time for that specific hourly forecast value. The close
proximity to 12:00 EPT (mean age 0.2h) suggests these are the standard
day-ahead forecast publications used operationally.

## Data Quality

- No duplicate target hours detected
- All days have complete hourly coverage
- DST transition handled correctly (23h on Mar 9, 25h on Nov 2)

## Selected Vintage Convention

For C06 model training, the current PJM CSV represents a clean,
protocol-compliant benchmark without needing additional filtering.
Each row's `day_ahead_forecast_mw` is the value to compare against.
