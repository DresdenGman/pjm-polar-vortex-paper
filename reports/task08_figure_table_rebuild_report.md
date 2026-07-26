# Task08 — Figure and Table Rebuild Report

**Date**: 2026-07-06  
**Status**: COMPLETE  

---

## Executive Summary

Six main-text figures and five LaTeX tables were rebuilt from verified Task07A/Task07B outputs. All figures read from CSV data files — no embedded data, no legacy values, no NASA imagery. All forbidden values (143,531 / 153,731) are absent from all outputs.

---

## Figures Generated

| Figure | PDF | Description |
|--------|-----|-------------|
| Figure 1 | `figure1_event_definition.pdf` | Full-year load + Jan 1-15 zoom + Jan 6-8 weather |
| Figure 2 | `figure2_workflow.pdf` | Schematic: data → features → models → evaluation |
| Figure 3 | `figure3_vortex_quantile_forecast.pdf` | 72h vortex: load, 90/98% PI, peak-zoom |
| Figure 4 | `figure4_calibration_breakdown.pdf` | Full-year vs vortex calibration curves |
| Figure 5 | `figure5_winter_vs_summer.pdf` | Side-by-side: winter MAE 2× summer, PI 66.7% vs 86.1% |
| Figure 6 | `figure6_tail_risk_event_peak.pdf` | Jan 7 18:00 prediction check (all models underpredicted) |

**Previously approved (MATLAB):**
- `Figure1_load_weather_forecast_final.pdf` — kept as alternative
- `Figure3_event_window_detail_final.pdf` — kept as alternative

## Tables Generated

| Table | Content |
|-------|---------|
| Table 1 | Data and event summary |
| Table 2 | Model summary with weather caveat |
| Table 3 | Point forecast metrics (Task07A) |
| Table 4 | Probabilistic metrics (Task07B) |
| Table 5 | Event peak prediction check |

## QC Results

| Check | Status |
|-------|--------|
| 143,531 in outputs | ✅ Absent |
| 153,731 in outputs | ✅ Absent |
| NASA imagery | ✅ None |
| Legacy data used | ✅ None |
| ERA5 labeled retrospective | ✅ Yes (Table 2) |
| Peak: 140,510 MW | ✅ Used throughout |
| Quantile crossing disclosed | ✅ Table 2 caption |

## Known Caveats

1. Figure 2 is a schematic — clean but simple. Can be redrawn in TikZ later.
2. Figure 5 panel (a/b) uses 72h windows — PI fill is approximate due to crossing correction.
3. Tables use manual LaTeX — verify alignment in final document.
4. QR-GBT q95/q99 values at event peak are very close to q50 (135,163 vs 135,357) — this reflects the model's inability to differentiate upper quantiles under extreme cold.

## Figures NOT Generated

- SHAP figure: SHAP not yet computed → deferred
- Supplementary figures (S1/S2/S3): deferred for manuscript revision

## Verdict

| Item | Verdict | Reason |
|------|---------|--------|
| Figure 1 | **READY** | Data-driven, correct peaks |
| Figure 2 | **READY** | Clean schematic |
| Figure 3 | **READY** | Quantile fan + zoom |
| Figure 4 | **READY** | Calibration curves verified |
| Figure 5 | **READY** | Winter vs summer comparison |
| Figure 6 | **READY** | Event peak error bars |
| Tables 1–5 | **READY** | Values match verified CSVs |
| Manuscript rewrite | **READY** | All source data frozen |

**Task08 verdict: READY FOR MANUSCRIPT REWRITE.**
