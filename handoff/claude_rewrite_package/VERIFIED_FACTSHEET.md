# Verified Factsheet — Single Source of Truth

## Official PJM Load Data

| Fact | Value |
|------|-------|
| Data source | PJM Data Miner 2 — Hourly Load: Metered |
| Period | 2010–2014, RTO-only, hourly |
| Rows per year | 8,760 (2012: 8,784 leap year) |
| Total rows | 43,824 |
| All verified by PJM | Yes |
| DST handling | Duplicate Nov 2 01:00 EPT rows preserved; forecast aligned via UTC |

| Claim | Old Manuscript | Official PJM | Status |
|-------|---------------|-------------|--------|
| Winter peak value | 143,531 MW | **140,510.2 MW** | ❌ Old value invalid |
| Winter peak time | Jan 7 08:00 | **Jan 7 18:00 EPT** | ❌ Wrong hour |
| Annual peak 2014 | Not claimed | **141,677.9 MW** (Jun 17 17:00) | Summer > winter |
| 153,731/153,732 MW | Legacy artifact | **Not in PJM data** | ❌ Fabricated |

## Event Definition

| Property | Value |
|----------|-------|
| Cold-event window | Jan 6–8, 2014 (72 hours) |
| Cold-event peak | 140,510.2 MW at Jan 7 18:00 EPT |
| Annual peak 2014 | 141,677.9 MW at Jun 17 17:00 EPT |
| Event-to-annual ratio | 99.18% (near-annual-peak) |
| Summer comparison window | Jun 16–18, 2014 (72 hours) |

**Framing**: The January 2014 Polar Vortex is a near-annual-peak cold-weather stress event. It is NOT the annual peak and NOT a verified winter record.

## Weather Data

| Source | Variables | Coverage | Status |
|--------|-----------|----------|--------|
| ERA5 reanalysis | t2m, d2m, u10, v10 | 2010–2014, hourly | AUTHORITATIVE |
| Aggregation | great_lakes_core (40–42.5°N, −88 to −74°W) | — | AUTHORITATIVE |
| NOAA ISD | 4 stations (provisional only) | 2014 | PROVISIONAL |
| NASA AIRS image | — | — | UNVERIFIED — DO NOT USE |

**Critical caveat**: ERA5 is same-hour retrospective reanalysis, NOT an operational weather forecast. All weather-informed model results must be labeled "retrospective reanalysis weather input."

## PJM Day-Ahead Forecast

| Property | Value |
|----------|-------|
| Source | PJM Data Miner 2 — Historical Load Forecasts |
| Coverage | Full-year 2014, 8,759 hours (DST-aligned) |
| Evaluation | Used as external benchmark only — not used in model training |

## Modeling Pipeline

| Property | Value |
|----------|-------|
| Training period | 2010–2013 |
| Test period | 2014 |
| 2014 rows in training | **0** (verified) |
| Features | Calendar + load lags (1h, 24h, 168h) + rolling means + ERA5 weather |
| Models | Persistence-1h, Naive-24h, Naive-168h, Linear, GBoost, QR-GBT (q01–q99) |
| Audit status | Task07A VALID, Task07B VALID |
| Data leakage | None found |
