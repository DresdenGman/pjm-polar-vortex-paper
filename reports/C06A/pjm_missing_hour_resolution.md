# C06A — PJM Missing Hour Diagnosis

**Date:** 2026-07-26
**Classification:** SOURCE_DATA_MISSING

## Missing UTC Timestamp
- **UTC:** 2014-11-02 05:00:00
- **Local (EPT):** 2014-11-02 01:00:00 EDT (first occurrence of repeated hour)
- **UTC offset:** -04:00 (EDT, before fall-back)
- **DST fold:** 0 (first of two 01:00-02:00 EPT hours)

## Diagnostic Results

| Check | Result |
|-------|--------|
| Expected 2014 UTC hours | 8,760 |
| Metered load coverage | 8,760 (100%) |
| PJM forecast coverage | 8,759 (99.99%) |
| Missing from PJM | 1 hour |
| Missing from load | 0 hours |
| Mar 9 DST (spring forward) | ✅ 23 local hours preserved |
| Nov 2 DST (fall back) | ⚠️ 24 hours in PJM (expected 25) |

## Root Cause

The PJM day-ahead forecast CSV contains 8,759 rows for 2014. The missing
row corresponds to the first occurrence of 01:00 EPT on November 2, 2014
(DST fall-back). On this date, the local clock repeats 01:00-02:00: once
at UTC-04:00 (EDT) and once at UTC-05:00 (EST). The PJM file captures
only the second occurrence (UTC 06:00 = 01:00 EST), collapsing the
repeated hour.

The first 5 UTC hours of January 1 (00:00-04:00) are pre-2014 EPT hours
(Dec 31, 2013 in local time) and are correctly absent from the 2014
operating-year forecast.

## Impact on C06 Protocol

| Metric | Value |
|--------|-------|
| PJM paired target hours | 8,759 / 8,760 |
| PJM complete operating days | 364 / 365 |
| Affected day | 2014-11-02 |

## Resolution

The missing hour is **not** recoverable from the source file. The PJM
comparator for 2014-11-02 will have 24 paired hours instead of 25.
The model dataset retains all 8,760 actual-load targets.

Missing PJM values for the affected hour should be recorded as null
with an explicit `exclusion_reason` column in the C06 dataset.

## Context

The 8,759-row count in the original C04S `quantile_predictions_2014.csv`
(which combines PJM day-ahead with model predictions) is therefore
explained: it inherits the same DST fall-back collapse from the PJM
source data.
