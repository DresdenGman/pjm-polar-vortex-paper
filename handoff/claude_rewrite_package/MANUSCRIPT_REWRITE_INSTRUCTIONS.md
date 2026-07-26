# Manuscript Rewrite Instructions for Claude

## 1. Source Material

- **Old manuscript** (`manuscript_legacy/paper.tex`): Legacy draft only. Contains invalid claims. Use for structure inspiration, NOT for facts.
- **Facts**: `VERIFIED_FACTSHEET.md` — single source of truth.
- **Results**: `RESULTS_SUMMARY.md` — all metrics verified.
- **Forbidden**: `FORBIDDEN_CLAIMS.md` — do not use any claim listed there.
- **Limitations**: `LIMITATIONS_AND_CAVEATS.md` — must be preserved in the new manuscript.

## 2. Target

Electric Power Systems Research (Elsevier) — non-OA path.  
Conservative, data-driven scientific tone. No marketing language.

## 3. Manuscript Structure

1. **Introduction** — event context, forecasting challenge, contribution
2. **Data and Event Definition** — PJM RTO, ERA5, event window, near-annual-peak framing
3. **Forecasting Framework** — features, models, quantile regression
4. **Experimental Design** — train/test split, metrics, benchmarks
5. **Results** — point forecasts, probabilistic forecasts, calibration, winter vs summer
6. **Discussion** — undercoverage, tail risk, cold-weather regime shift
7. **Limitations** — ERA5 retrospective, quantile crossing, NOAA provisional
8. **Conclusion**

## 4. Figure and Table Assignment

| Figure | Section |
|--------|---------|
| Figure 1 | Data and Event Definition |
| Figure 2 | Forecasting Framework (conceptual) |
| Figure 3 | Results |
| Figure 4 | Results |
| Figure 5 | Results |
| Figure 6 | Results / Discussion |

| Table | Section |
|-------|---------|
| Table 1 | Data and Event Definition |
| Table 2 | Forecasting Framework |
| Table 3 | Results |
| Table 4 | Results |
| Table 5 | Results |

## 5. Rules

- Do NOT invent citations. Only cite papers you know exist.
- Do NOT invent data. All numbers must come from `RESULTS_SUMMARY.md`.
- Do NOT use SHAP unless valid SHAP outputs are provided separately.
- Do NOT reference NASA imagery.
- Every weather-informed result must include "retrospective ERA5 reanalysis" caveat.
- Keep captions factual — see `CAPTION_DRAFTS.md`.
- Use `\includegraphics{figures/figureN_*.pdf}` for figures, `\input{tables/tableN_*.tex}` for tables.
