# Task11 — Table 5 Quantile Ordering Audit Report

**Date**: 2026-07-07  
**Status**: COMPLETE — **TABLE 5 CORRECTED**

---

## Root Cause

Table 5 in `all_tables.tex` was generated before post-hoc monotonic rearrangement was applied to the quantile predictions. The Task07B script captured event-peak values mid-pipeline, before the rearrangement step that resolved 5,786 quantile crossings. The values persisted into the final report and table despite the source CSV (`quantile_predictions_2014.csv`) containing correct post-rearrangement values.

## Verified Post-Rearrangement Values (Jan 7 18:00 EPT)

| Quantile | Old Table 5 | Correct (Post-Rearrangement) |
|----------|:-----------:|:---------------------------:|
| q01 | — | 121,973 |
| q05 | — | 131,685 |
| q10 | — | 132,591 |
| q50 | 135,357 | **135,357** (unchanged) |
| q90 | — | 138,627 |
| q95 | 135,163 | **139,410** (+4,247 correction) |
| q99 | 135,386 | **139,585** (+4,199 correction) |
| Actual | 140,510 | 140,510 |
| Actual - q99 | — | **925 MW** (not 5,124 MW) |

## Monotonicity Check

Post-rearrangement values are strictly monotonic:
$$q01 < q05 < q10 < q50 < q90 < q95 < q99$$

✅ No violations.

## Key Finding Still Holds

The actual load (140,510 MW) still exceeds q99 (139,585 MW) by 925 MW. The event peak remains outside the 98% prediction interval. The correction makes the finding **cleaner**: the model differentiates quantiles properly, but the actual peak still breaches the upper bound.

## Files Updated

| File | Change |
|------|--------|
| `tables/output/all_tables.tex` | q95: 135,163 → 139,410; q99: 135,386 → 139,585; errors recalculated |
| `CAPTION_DRAFTS.md` | Removed "q95/q99 collapse toward q50" narrative; updated with correct values |
| `claude_rewrite_package.zip` | Rebuilt with corrected files |

## What Previously Said "Quantile Collapse Toward q50"

This was an artifact of pre-rearrangement values. Post-rearrangement, the quantiles are properly differentiated. The corrected narrative: the model does differentiate upper quantiles, but even the 99th percentile bound (139,585 MW) falls below the actual load (140,510 MW). This is a cleaner and stronger finding.

**Task11 verdict: TABLE 5 QUANTILE STATUS VERIFIED AND CORRECTED.**
