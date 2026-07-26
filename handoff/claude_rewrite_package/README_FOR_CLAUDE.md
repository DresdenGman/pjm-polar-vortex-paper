# Claude Manuscript Rewrite — Handoff Package

## What This Is

This package contains everything you need to rewrite the manuscript "Probabilistic Electricity Demand Forecasting During Extreme Winter Events: A Case Study of the 2014 Polar Vortex in PJM" for submission to Electric Power Systems Research (EPSR) or a similar Elsevier power systems journal.

## What You Must Know Before Starting

1. **The old manuscript (`manuscript_legacy/paper.tex`) is NOT a reliable source of facts.** It contains invalid claims (143,531 MW peak, NASA AIRS imagery, winter-record framing) that have been disproven by official PJM data.

2. **All verified facts are in `VERIFIED_FACTSHEET.md`.** Use this as your single source of truth for numbers, dates, and data provenance.

3. **All results are in `RESULTS_SUMMARY.md`.** These were independently audited and reproduced.

4. **The figures and tables in this package are the approved publication set.** Do not reference old figures that aren't here.

5. **`FORBIDDEN_CLAIMS.md` lists what you MUST NOT write.** Every forbidden claim has an approved replacement.

## Quick Reference

| What | Where |
|------|-------|
| Verified facts (peaks, dates, sources) | `VERIFIED_FACTSHEET.md` |
| Model results (MAE, coverage, pinball) | `RESULTS_SUMMARY.md` |
| Figure-to-section mapping | `FIGURE_TABLE_MAP.md` |
| Caption drafts | `CAPTION_DRAFTS.md` |
| Must-not-write claims | `FORBIDDEN_CLAIMS.md` |
| Known limitations | `LIMITATIONS_AND_CAVEATS.md` |
| Rewrite instructions | `MANUSCRIPT_REWRITE_INSTRUCTIONS.md` |
| Old manuscript (legacy only) | `manuscript_legacy/paper.tex` |
| Final figures | `figures/` |
| Final tables | `tables/` |
| Supporting reports | `reports/` |

## Critical Rules

- **Target journal**: EPSR (non-OA path) or similar Elsevier power systems journal.
- **Tone**: Conservative, data-driven, no hype.
- **Weather caveat**: Every result using ERA5 must be labeled "retrospective reanalysis weather input."
- **Event framing**: January 2014 Polar Vortex is a near-annual-peak cold-weather stress event — NOT the annual peak, NOT a winter record.
- **Peak load**: 140,510 MW at Jan 7 18:00 EPT. NOT 143,531 MW.
- **No NASA imagery. No AI-generated photos. No legacy embedded-data figures.**
