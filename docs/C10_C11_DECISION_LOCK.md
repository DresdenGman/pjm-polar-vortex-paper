# C10/C11 Decision Lock

**Source:** Command 048-P2R (2026-08-08)
**Status:** LOCKED — supersedes any conflicting earlier interpretation

---

## Decision 1 — C10/C11 Scope

**RULING: FULL YEAR 365 cycles.**

- PRIMARY_PRODUCTION_SCOPE = 2014 FULL YEAR
- OPERATING_DAYS = 365
- GFS_CYCLES = 365 (2013-12-31 06Z .. 2014-12-30 06Z)
- JANUARY_31C = acquisition / engineering milestone ONLY
- JANUARY_31C ≠ production analysis population

**Gate change:**
- OLD: `require_source_verified_cycles = 31`
- NEW: `require_c09d_2014_final_seal = TRUE`

Final runner requires:
- C09D_2014_FINAL_SEAL exists
- AND seal.status == FINAL_SEALED
- AND seal.analysis_population_approved == true

364 cycles ≠ authorized production dataset (unless Commander formally approves deviation, e.g. if 01-16 unrecoverable).

---

## Decision 2 — C10A Weather-Aware Point Models

**RULING: STRICT ADDITIVE extension.**

- C08B = sealed LOAD-ONLY comparator
- C10A = C08B protocol + operational GFS weather feature block

**May change ONLY:** feature set (load-only → load + GFS weather).

**Must stay identical:** folds, train/validation/test logic, random seeds, model families, hyperparameter grids, model-selection criterion, evaluation rows, metrics.

**Hyperparameter policy:** same search space, same validation rule, rerun selection on TRAIN/VALIDATION only. No new family, no expanded grid, no manual tuning after test results.

**Naive baselines** (naive_7d, naive_latest): no weather, remain as reference.

---

## Decision 3 — C10B Weather-Aware Probabilistic

**RULING: STRICT ADDITIVE.**

- C08C = sealed load-only probabilistic comparator
- C10B = same probabilistic machinery + GFS weather

**Must stay identical:** probabilistic model families, quantile levels (q01 q05 q10 q50 q90 q95 q99), split, seeds, evaluation, quantile-crossing policy (no post-hoc sorting).

**PROHIBITED in C10B:** new quantiles, conformalization, post-hoc calibration, quantile sorting, new probabilistic architecture (unless separately preregistered as sensitivity).

**Primary estimand:** how does adding operational forecast weather change point/probabilistic performance relative to identical load-only pipeline.

---

## Decision 4 — C11A Ablation

**RULING: POST-HOC EXPLANATORY SENSITIVITY** — not a primary model competition.

**Order:** C10A FINAL → C10B FINAL → freeze primary artifacts → C11A.

**Purpose:** which predefined weather feature groups does the full model depend on? NOT "which ablation is better, promote it to primary".

**Protocol:** feature groups locked BEFORE seeing C10 test results, taken from C09C feature taxonomy. Each ablation removes one predefined group → refit with same folds/seeds/algorithm/search space/validation/metrics.

**Results labeled:** SECONDARY / EXPLANATORY.

---

## Decision 5 — C11B Threshold / Event Sensitivity

**RULING: SECONDARY ROBUSTNESS ONLY** — never redefines primary events.

- E2014 / E2018 / E2022 official windows = IMMUTABLE PRIMARY (registry: "Do not modify event windows after examining model errors")
- E2015 = locked ERA5 rule (≥48h below winter 5th percentile), sensitivity boundary resolution as defined

**Allowed in scaffolding:** threshold_sensitivity dispatcher, config schema, validation, artifact structure. NO sensitivity execution, NO numeric threshold expansion yet (grid frozen by Commander before any run).

---

## Consequences

- Even if Command 049 seals January 31/31, C09D is January-complete only — full production requires Feb 01..Dec 30 acquisition (334 cycles).
- Next priority after P2-C/D/E: **C09D Full-Year Acquisition design** (storage architecture, rolling acquisition, semantic gate, retention policy, Feb-Dec batching, full-year seal).
- 01-16 external recovery and Feb-Dec acquisition proceed in parallel.
