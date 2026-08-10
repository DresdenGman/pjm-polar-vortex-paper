# C10/C11 Preregistration Crosswalk

**Status:** READ-ONLY check against C09D preregistration (branch `C09D-2014-production-preregistration`, commit 746c4ce)
**Date:** 2026-08-08
**Method:** No modifications to preregistration. Conflicts flagged as DECISION_REQUIRED.

Prereg source: `reports/C09D/production_join_contract.md` + `acquisition_manifest_2014.csv` (365 cycles)

---

## Crosswalk Table

| Planned analysis | Preregistered? | Exact prereg clause | Implementation mapping | Potential deviation? | Requires Commander decision? |
|---|---|---|---|---|---|
| GFS initialization = 06Z D-1 | YES | "initialization_utc = 06:00 UTC on the GFS cycle date (D-1)" | C09D 06Z acquisition | No | NO |
| Forecast leads f018–f048 | YES | "forecast_hour ∈ {18,21,...,48}" (11 leads) | C09D leads constant | No | NO |
| Station panel key | YES | "initialization_utc + valid_time_utc + station_id" | C09D native/hourly key | No | NO |
| Network-feature key | YES | "initialization_utc + valid_time_utc" | trajectory panel key | No | NO |
| 365-cycle population | YES | "365 cycles for 365 operating days" | C09D acquisition manifest | **Jan 2014 subset only for C10/C11 warm-start?** | **DECISION_REQUIRED — C10/C11 uses Jan 2014 (31 cycles) as weather-integration window; prereg implies full-year production. Confirm C10 scope = January only or full year.** |
| Day-ahead origin | YES | "day_ahead_origin_pjm = 12:00 EPT on D-1 (locked C06A)" | C08A join protocol | No | NO |
| 7-hour overlap handling | YES | "valid_time_utc alone NOT unique; compound keys required" | C09D trajectory compound key | No | NO |
| Point-model baselines | PARTIAL | C08B point models (load-only) | C10A inherits | Weather augmentation not in prereg | **DECISION_REQUIRED — weather-augmented point models are new relative to prereg; confirm they are additive (C10A) not conflicting.** |
| Probabilistic models | PARTIAL | C08C probabilistic baselines (QR-GBT/QHGBR/NGBOOST) | C10B inherits | Weather-augmented probabilistic not in prereg | **DECISION_REQUIRED — same additive-vs-conflict question for C10B.** |
| Ablation (C11A) | NO | — | New planned analysis | Weather-feature ablation not preregistered | **DECISION_REQUIRED — confirm ablation is post-hoc sensitivity (allowed) vs prereg violation.** |
| Event sensitivity (C11B) | PARTIAL | C08C event definitions (E2014/E2018/E2022) | C11B inherits event set | Threshold variation post-hoc | **DECISION_REQUIRED — threshold sensitivity sweep is exploratory; confirm framing.** |
| Metrics | YES | C08C metrics (CRPS, pinball, coverage, block bootstrap) | C10B same | No | NO |
| Seed policy | YES | seed 3508246379, 2000 replicates | C10B same | No | NO |
| Weather feature construction | PARTIAL | C09B/C09C cold-weather features (wind chill, HDD, ramps, cold duration) | C10A/B feature sets | Hourly interpolation detail | NO (implementation detail) |

---

## Summary

- Conflicts: 0 (hard conflicts)
- **DECISION_REQUIRED items: 5 — ALL RESOLVED via Command 048-P2R (docs/C10_C11_DECISION_LOCK.md)**
  1. C10/C11 scope: **FULL YEAR 365 cycles** (January = milestone only; production gate = C09D_2014_FINAL_SEAL, not 31-cycle seal)
  2. C10A weather point models: **strict additive** (same folds/seeds/families/grids, weather feature block only)
  3. C10B weather probabilistic: **strict additive** (same quantiles q01..q99, no conformal/calibration/sorting/crossing changes)
  4. C11A ablation: **post-hoc explanatory sensitivity** (after C10 frozen; feature groups pre-locked from C09C taxonomy)
  5. C11B threshold sensitivity: **secondary robustness only** (official event windows immutable primary; threshold grid frozen by Commander before any run)

## Notes

- Preregistration itself: **NOT modified** (read-only)
- Provisional data: **NOT used** for any model fitting
- Unresolved methodological decisions: **0**
- January 31-cycle seal does NOT make C10 production-ready; full-year C09D_2014_FINAL_SEAL required
