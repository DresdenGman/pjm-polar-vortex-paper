# C10/C11 Execution Spec

**Status:** READINESS PREP (no model fitting authorized)
**Date:** 2026-08-08
**Gate:** requires C09D_FINAL_SEAL = TRUE and source_verified_cycles = 31

---

## Roadmap

| Phase | Content |
|-------|---------|
| C10A | Weather-aware point models |
| C10B | Weather-aware probabilistic models |
| C11A | Full ablation |
| C11B | Event sensitivity |

## Hard Gates

- `production_enabled = false` until C09D_2014_FINAL_SEAL
- `require_c09d_2014_final_seal = true` (NOT January 31-cycle seal)
- Final seal must be FINAL_SEALED with analysis_population_approved == true
- Production population = 365 cycles (full year 2014), NOT January-only
- Runner MUST refuse to start if full-year seal absent (protects against using 30C provisional or January-only as final)
- See docs/C10_C11_DECISION_LOCK.md (Command 048-P2R) for all locked decisions

---

## C10A — Weather-Aware Point Models

**Inputs:**
- Canonical full-year 2014 hourly panel (365 cycles) — post C09D_2014_FINAL_SEAL
- C08B point-model features (load-only baseline family)
- Weather features: temperature_2m_celsius, relative_humidity_2m_percent, wind_speed_10m_mps, surface_pressure_hpa

**Outputs:**
- Point forecasts per PJM operating day (full-year 2014, 365 days), f018..f048 horizons

**Train/validation/test contract:**
- Inherit C08B protocol exactly (no new splits)
- Cold-event test days: E2014, E2018, E2022 (from C08C event definitions)
- Population: full-year 2014 (365 operating days) — January is milestone only (DECISION_LOCK #1)

**Feature sets:**
- Baseline: C08B features only
- +Weather: baseline + GFS weather features

**Baseline comparison:**
- Persistence, load-only QR-GBT point predictions (C08B), weather-augmented

**Metrics:**
- MAE, RMSE, peak-day error (PDE) — same as C08B

**Random seeds:**
- Same seed policy as C08C (seed 3508246379 family, 2000 replicates where applicable)

**Artifact paths:**
- `artifacts/C10A/...` (mirror C08B structure)

**Failure gates:**
- No final seal → refuse
- Weather features missing → refuse
- Event days missing → refuse

**Execution order:**
1. Data loader validation
2. Baseline reproduce (C08B parity)
3. Weather-augmented fit
4. Event-day evaluation

---

## C10B — Weather-Aware Probabilistic Models

**Inputs:**
- Canonical 31-cycle hourly panel + C08C probabilistic feature panel

**Outputs:**
- Quantile forecasts (same quantile grid as C08C) + prediction intervals

**Methods (inherit C08C, no new models):**
- QR-GBT (7 quantiles), QHGBR, NGBOOST_NORMAL (C08C gap closure optional per Commander)

**Metrics:**
- CRPS, pinball, coverage, interval width — same as C08C

**Probabilistic evaluation:**
- Block bootstrap (seed 3508246379, 2000 replicates)
- Event coverage: E2014/E2018/E2022 (C08C framework)

**Execution order:**
1. C10A parity checkpoint
2. Probabilistic fit
3. Event-coverage evaluation

---

## C11A — Full Ablation

Ablate weather feature groups independently:
- Temperature only
- Humidity only
- Wind only
- Pressure only
- All weather
- No weather (baseline)

**Question:** which GFS fields drive the coverage collapse improvement (or lack thereof)?

**Execution:** one fit per ablation arm, same splits/seeds/metrics.

---

## C11B — Event Sensitivity

- Vary cold-event threshold definitions (C08C event set)
- Sensitivity of coverage to event severity ranking
- Report per-event coverage table (E2014/E2018/E2022) across ablation arms

---

## Constraints

- NO new model architectures beyond C08/C09 inherited methods
- NO provisional-data performance inspection
- NO hyperparameter tuning on 30C provisional
- All results only after C09D FINAL SEAL (31/31)

## Artifact Layout

```
artifacts/C10A/   point models + metrics
artifacts/C10B/   probabilistic models + coverage
artifacts/C11A/   ablation matrix
artifacts/C11B/   event sensitivity
```
