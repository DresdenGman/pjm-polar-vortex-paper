# C06A — Decision Summary

**Date:** 2026-07-26
**Branch:** C06-day-ahead

## PJM Forecast Vintage Audit

| Metric | Value |
|--------|-------|
| PJM qualifying operating days | 365/365 |
| PJM accounted target hours | 8,759 |
| PJM missing target hours | 1 (Nov 2 DST fallback hour) |
| PJM one-vintage integrity | ❓ NOT VERIFIED — audit script needs per-day creation-time grouping |
| March DST (spring forward) | ✅ 23 hours on 2014-03-09 |
| November DST (fall back) | ⚠️ 24 hours on 2014-11-02 (expected 25) |

**PJM coverage: 99.99% (8,759/8,760).** One hour missing due to DST fall-back collapse.

## NDFD Weather Audit

| Metric | Value |
|--------|-------|
| NDFD temperature coverage | ❓ UNKNOWN |
| NDFD dew-point coverage | ❓ UNKNOWN |
| NDFD wind-speed coverage | ❓ UNKNOWN |
| NDFD joint coverage | ❓ UNKNOWN |
| NDFD issue-time integrity | ❓ UNKNOWN |
| NDFD one-vintage integrity | ❓ UNKNOWN |
| Archive accessibility | ✅ NDGD accessible, 2014 data exists |
| Temperature product identified | ❌ NOT YET (LEIA98 = precipitation only) |
| ≥24h lead products confirmed | ❌ NOT YET (LEIA98 = 1h lead only) |

## Leakage Audit

| Class | Count |
|-------|-------|
| Features audited in modeling_features | 17 columns |
| DAY_AHEAD_ALLOWED | TBD |
| ORACLE_ONLY | TBD |
| PROHIBITED_LEAKAGE | TBD |
| NOT_APPLICABLE | TBD |

(A full feature-availability matrix is pending — the protocol was just locked this session.)

## Decision

**STOP_AND_REVISE_PROTOCOL**

PJM vintage audit is near-complete (99.99% coverage, one DST hour to resolve).
However, the NDFD operational weather track CANNOT currently be validated:
- Temperature/dew/wind products with ≥24h lead times not yet identified
- Without these, the strict day-ahead protocol lacks a weather input

### Recommended Revision

Option A (recommended by operator): Proceed with ERA5 oracle track for C06
model training while continuing NDFD product code investigation in parallel.
This allows progress on all other C06 tasks (multi-event design, probabilistic
baselines, expanded metrics) while resolving the weather data issue separately.

The protocol is otherwise sound: PJM vintage selection works, the forecast
origin (12:00 EPT D-1) is well-defined, and load-information cutoff is clear.
