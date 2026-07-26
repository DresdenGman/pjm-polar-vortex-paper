# Full Artifact Integrity Audit — Go/No-Go Verdict

**Date**: 2026-07-06  
**Status**: AUDIT COMPLETE

---

## Final Verdict Table

| Artifact | Verdict | Required Action |
|----------|---------|-----------------|
| Official PJM load 2010–2014 | **GO** | None |
| PJM Day-Ahead Forecast | **GO** | None |
| ERA5 Weather (great_lakes_core) | **GO** (retrospective only) | Label as reanalysis |
| NOAA 4-station weather | **PROVISIONAL** | Do not use as primary |
| Task07A features/predictions/metrics | **GO** | Validated by audit |
| Figure 1 final | **GO** | Caption edit only |
| Figure 3 final | **GO** | Caption edit only |
| Old figures (Fig1/2/3/5 PDFs in figures/) | **NO-GO** | Quarantine or delete |
| NASA AIRS image | **NO-GO** | Provenance unverified |
| Current paper.tex | **REWRITE_FROM** | Contains -1.8°F, NASA AIRS, winter record |
| MATLAB scripts (matlab/Figure1-5.m) | **QUARANTINE** | Embedded 143,531 data |
| MATLAB scripts (figures/src/*_final.m) | **GO** | Valid final pipeline |
| Python pipeline (src/) | **NEEDS_FIX** | Test data uses 143,531 |
| Legacy data (legacy_unverified/) | **QUARANTINED** | Never use |

---

## Critical Issues Found

### 1. paper.tex — Must Rewrite
- **`-1.8°F`** at line 243 (Table 1) — contradicted by ERA5 (actual = 2.5°F mean)
- **`NASA AIRS`** captions at lines 85 and 97 — image unverified
- **`winter record`** / **`all-time`** — contradicted by PJM (summer peak higher)
- **`perfect weather`** — overstates model assumptions
- No `\includegraphics` commands — figures need to be added

### 2. MATLAB Legacy Scripts — Must Quarantine
- `matlab/Figure1.m`: Embedded 143,531 in hardcoded CSV string
- `matlab/Figure2.m`: Hardcoded `peaks = [..., 143.531, ...]`
- `matlab/Figure3.m`, `matlab/Figure5.m`: Old embedded-data scripts
- These predate the new data pipeline and should NOT be used

### 3. Python Test Data — Must Update
- `src/data/tests/conftest.py`: Test data uses 143,531
- `src/data/tests/test_preprocess_pjm_load.py`: Asserts max = 143,531
- Should be updated to use 140,510 as reference

### 4. Old Figures — Must Remove/Quarantine
- `figures/Figure1-5_PolarVortex_*.pdf`: Generated from legacy embedded MATLAB
- `figures/NASA_AIRS_Vortex_2014.png`: Unverified provenance
- `figures/Figure4_QRGBT.tex`: Unknown origin

---

## Safe Artifacts

### Data (all AUTHORITATIVE or VALID_DERIVED)
- All `data/raw/pjm/pjm_load_20*.csv` — official PJM
- `data/raw/pjm/pjm_day_ahead_forecast_2014_clean.csv` — official PJM
- `data/processed/weather_era5_pjm_2010_2014_great_lakes_core.csv` — ERA5 CDS
- `data/processed/pjm_era5_modeling_table_2010_2014.csv` — UTC-merged
- `data/processed/modeling_features_2010_2014.csv` — Task07A features
- `data/results/baseline_*.csv` — Task07A results

### Figures (VALID for manuscript)
- `figures/output/Figure1_load_weather_forecast_final.pdf`
- `figures/output/Figure3_event_window_detail_final.pdf`

### Scripts (VALID final pipeline)
- `figures/src/Figure1_rebuild_final.m`
- `figures/src/Figure3_rebuild_final.m`

---

## Required Actions Before Task07B

| Priority | Action |
|----------|--------|
| 🔴 | Quarantine old MATLAB scripts (move `matlab/` to `legacy_unverified/`) |
| 🔴 | Remove old figures from `figures/` root (keep only in legacy_unverified) |
| 🔴 | Remove or mark NASA image as UNVERIFIED_DO_NOT_USE |
| 🟡 | Update Python test data from 143,531 to 140,510 |
| 🟡 | Remove -1.8°F, NASA AIRS, winter record from paper.tex (or defer to full rewrite) |
| 🟢 | Figure 1 & 3 captions — minor edits only |

---

## Recommendation

**Full artifact audit verdict: GO TO TASK07B** (with the above cleanups executed first).

Task07A is VALID. The modeling chain is clean. The contamination is confined to legacy scripts, old figures, and paper.tex — none of which block the quantile modeling pipeline. Clean up the 🔴 items, then proceed.
