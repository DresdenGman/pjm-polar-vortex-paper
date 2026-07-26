# C01A Intake Summary

# Task C01A — Intake Summary

## 1. Project Purpose

This project rewrites an existing (legacy) journal manuscript about **probabilistic electricity demand forecasting during extreme cold-weather events**, specifically the **January 2014 Polar Vortex in the PJM interconnection**. The rewrite is necessary because the legacy draft (`manuscript_legacy/paper.tex`) contains **invalid factual claims** — including an incorrect peak load figure (143,531 MW), unsupported NASA imagery references, and improper event framing. The new manuscript must be grounded entirely in verified data from the project's audited fact and results files.

---

## 2. Manuscript Target and Tone

| Attribute               | Detail                                                                                                            |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Target journal**      | Electric Power Systems Research (EPSR), Elsevier — non-OA path                                                    |
| **Tone**                | Conservative, data-driven, scientific — no hype, no marketing language                                            |
| **Event framing**       | January 2014 Polar Vortex = near-annual-peak cold-weather stress event (NOT a winter record, NOT the annual peak) |
| **Peak load**           | 140,510 MW at Jan 7 18:00 EPT (verified)                                                                          |
| **Weather data caveat** | Every ERA5-informed result must be labeled "retrospective reanalysis weather input"                               |

---

## 3. Required Manuscript Structure

1. **Introduction** — event context, forecasting challenge, contribution
2. **Data and Event Definition** — PJM RTO, ERA5, event window, near-annual-peak framing
3. **Forecasting Framework** — features, models, quantile regression
4. **Experimental Design** — train/test split, metrics, benchmarks
5. **Results** — point forecasts, probabilistic forecasts, calibration, winter vs. summer
6. **Discussion** — undercoverage, tail risk, cold-weather regime shift
7. **Limitations** — ERA5 retrospective, quantile crossing, NOAA provisional data
8. **Conclusion**

---

## 4. Figure and Table Assignments

**Figures:**

| Figure   | Assigned Section                   |
| -------- | ---------------------------------- |
| Figure 1 | Data and Event Definition          |
| Figure 2 | Forecasting Framework (conceptual) |
| Figure 3 | Results                            |
| Figure 4 | Results                            |
| Figure 5 | Results                            |
| Figure 6 | Results / Discussion               |

**Tables:**

| Table   | Assigned Section          |
| ------- | ------------------------- |
| Table 1 | Data and Event Definition |
| Table 2 | Forecasting Framework     |
| Table 3 | Results                   |
| Table 4 | Results                   |
| Table 5 | Results                   |

---

## 5. Most Important Rules for Later Tasks

These are non-negotiable constraints I must obey in every subsequent task:

- ❌ **Never use the legacy manuscript as a source of facts.** It is for structural reference only.
- ❌ **Never invent or infer citations.** Only cite papers known to exist.
- ❌ **Never invent data or numbers.** All metrics must come from `RESULTS_SUMMARY.md`.
- ❌ **Never reference NASA imagery** or AI-generated photos.
- ❌ **Never use forbidden claims** listed in `FORBIDDEN_CLAIMS.md` — each has an approved replacement.
- ❌ **Never use SHAP** unless valid SHAP outputs are separately provided.
- ✅ **Always use** `VERIFIED_FACTSHEET.md` as the single source of truth for peaks, dates, and data provenance.
- ✅ **Always label** every ERA5-weather-informed result as "retrospective ERA5 reanalysis."
- ✅ **Always preserve** all known limitations from `LIMITATIONS_AND_CAVEATS.md`.
- ✅ **Always use** `\includegraphics{figures/figureN_*.pdf}` for figures and `\input{tables/tableN_*.tex}` for tables.
- ✅ **Always keep captions factual** per `CAPTION_DRAFTS.md`.

---

## 6. Files Needed Next (for C01B and beyond)

To proceed with actual writing, the following files are required in priority order:

| Priority  | File                          | Why Needed                                                              |
| --------- | ----------------------------- | ----------------------------------------------------------------------- |
| 🔴 High   | `VERIFIED_FACTSHEET.md`       | Single source of truth — all numbers, dates, data provenance            |
| 🔴 High   | `RESULTS_SUMMARY.md`          | All model metrics (MAE, coverage, pinball) — needed for Results section |
| 🔴 High   | `FORBIDDEN_CLAIMS.md`         | Must know every prohibited claim and its approved replacement           |
| 🟡 Medium | `LIMITATIONS_AND_CAVEATS.md`  | Required for Limitations section — must be preserved verbatim           |
| 🟡 Medium | `CAPTION_DRAFTS.md`           | Needed before writing any figure/table references                       |
| 🟡 Medium | `FIGURE_TABLE_MAP.md`         | Confirms figure filenames and exact section mappings                    |
| 🟢 Lower  | `manuscript_legacy/paper.tex` | Structure reference only — not to be read for facts                     |

---

C01A complete. Ready for C01B.
