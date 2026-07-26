# C05A — Forecast Information-Set Audit

**Date:** 2026-07-26
**Branch:** C05-epsr-rebuild
**Audited by:** Hermes (Operator)

## Executive Finding

The current manuscript compares models that use **different forecast horizons and information sets**, making the headline GBoost-vs-PJM comparison invalid as a like-for-like benchmark.

---

## Information-Set Comparison

| Model | Forecast Origin | Target Time | Horizon | Latest Load Known | Weather Input | Weather Available Operationally? | Fairly Comparable with PJM? |
|-------|----------------|-------------|---------|-------------------|---------------|--------------------------------|---------------------------|
| Persistence | t | t+1h | 1h | t (same hour) | ERA5 same-hour | ❌ No (reanalysis) | ❌ |
| Naive (daily) | t (24h ago) | t | 24h | t-24h | ERA5 same-hour | ❌ No | ❌ |
| Naive (weekly) | t (168h ago) | t | 168h | t-168h | ERA5 same-hour | ❌ No | ❌ |
| Linear Regression | t-1h | t | 1h | t-1h | ERA5 same-hour | ❌ No | ❌ |
| GBoost | t-1h | t | 1h | t-1h | ERA5 same-hour | ❌ No | ❌ |
| QR-GBT | t-1h | t | 1h | t-1h | ERA5 same-hour | ❌ No | ❌ |
| PJM Day-Ahead | ~t-24h | t | ~24h | ~t-24h | NWP forecast | ✅ Yes | N/A (reference) |

## Key Gap

- **GBoost/QR-GBT**: Uses lag-1h load + same-hour ERA5 reanalysis → closest to **hour-ahead retrospective nowcast**
- **PJM Day-Ahead**: Uses forecast issued ~24h before operating day with operational NWP → actual **day-ahead operational forecast**

The comparison conflates two fundamentally different forecasting tasks.

---

## Trace: PJM Peak Hour (Jan 7, 2014, 18:00 EPT)

| Attribute | Value |
|-----------|-------|
| Target timestamp | 2014-01-07 18:00 EPT |
| GBoost prediction origin | 2014-01-07 17:00 EPT |
| Latest load known to GBoost | 2014-01-07 17:00 EPT (lag_1h) |
| ERA5 valid time | 2014-01-07 18:00 UTC (same-hour) |
| ERA5 data availability in operations | ❌ Not available — retrospective reanalysis |
| PJM forecast creation time | ~2014-01-06 12:00–18:00 EPT (day-ahead) |
| PJM forecast vintage | Day-ahead forecast for operating day Jan 7, 2014 |
| PJM weather input | Operational NWP, not ERA5 |

---

## Information Asymmetry Summary

1. **Load information**: GBoost has load up to t-1h; PJM DA has load up to ~t-24h
2. **Weather information**: GBoost has actual realized weather (ERA5); PJM DA has forecast weather (NWP)
3. **Forecast horizon**: GBoost = 1h; PJM DA = ~24h → ~24x difference
4. **Operational deployability**: GBoost cannot be deployed as tested (ERA5 not available at runtime)

## Required Decision (from ChatGPT Phase 2.1)

- **Route A**: Genuine day-ahead forecasting — requires NWP weather, common origin, only pre-origin information
- **Route B**: Hour-ahead retrospective stress testing — retain current setup but remove PJM as primary benchmark; use PJM only as contextual reference
