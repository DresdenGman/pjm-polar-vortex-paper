# C04M — Citation Finalization Plan

**Date**: 2026-07-07  
**Status**: **CITATION PLAN READY — NEEDS AUTHOR INPUT**

---

## 1. Complete Placeholder Inventory

13 unique placeholders, 17 total occurrences across `paper.tex`.

| # | Placeholder | Occurrences | § | Surrounding Context |
|---|-------------|:----------:|:--:|---------------------|
| 1 | `[CITATION: power systems operations reference]` | 1 | §1.1 | "System operators depend on accurate hourly demand forecasts..." |
| 2 | `[CITATION: NERC reliability standards reference]` | 1 | §1.1 | "...reserve margins erode, emergency procedures may be triggered..." |
| 3 | `[CITATION: probabilistic load forecasting review]` | 1 | §1.2 | "...typically expressed as quantile forecasts or prediction intervals" |
| 4 | `[CITATION: probabilistic forecasting in power systems]` | 1 | §1.2 | "...procuring reserves calibrated to the tail of the demand distribution..." |
| 5 | `[CITATION: load-temperature nonlinearity reference]` | 1 | §1.3 | "...each additional degree of cold below the heating base temperature drives progressively larger demand increases..." |
| 6 | `[CITATION: NERC Polar Vortex Review 2014]` | 2 | §1.4, §2.4 | "...detailed post-event reviews by both NERC and PJM..." |
| 7 | `[CITATION: PJM Polar Vortex Review 2014]` | 2 | §1.4, §2.4 | (same sentence as #6) |
| 8 | `[CITATION: meteorological analysis of 2014 polar vortex]` | 2 | §1.4, §2.4 | "...the meteorological character of the event is well-characterized..." |
| 9 | `[CITATION: ERA5 reanalysis]` | 2 | §2.2, §4.6 | "ERA5 reanalysis dataset produced by ECMWF..." |
| 10 | `[CITATION: gradient boosting reference]` | 1 | §3.3 | "...each successive tree fitted to the residuals of the preceding ensemble" |
| 11 | `[CITATION: quantile regression reference]` | 1 | §3.4 | "Rather than minimizing squared error, QR-GBT fits..." |
| 12 | `[CITATION: gradient boosting quantile regression]` | 1 | §3.4 | (same paragraph as #11) |
| 13 | `[CITATION: quantile crossing reference]` | 1 | §6.5 | "...consistent with findings in the broader quantile regression literature" |

✅ Confirmed: `distributional robustness` absent. No Category C blockers.

---

## 2. Category A — Safe Direct Replacement (7 placeholders)

These have verified `\bibitem{}` entries already in `paper.tex`. Can be replaced directly.

| Placeholder | Replace With | Count | § | Risk |
|-------------|-------------|:---:|:--:|:----:|
| `[CITATION: probabilistic load forecasting review]` | `\cite{hong2016probabilistic}` | 1 | §1.2 | ✅ Safe |
| `[CITATION: probabilistic forecasting in power systems]` | `\cite{hong2016tutorial}` | 1 | §1.2 | ✅ Safe |
| `[CITATION: NERC Polar Vortex Review 2014]` | `\cite{nersc2014polar}` | 2 | §1.4, §2.4 | ✅ Safe |
| `[CITATION: PJM Polar Vortex Review 2014]` | `\cite{pjm2014polar}` | 2 | §1.4, §2.4 | ✅ Safe |
| `[CITATION: meteorological analysis of 2014 polar vortex]` | `\cite{arritt2014us}` | 2 | §1.4, §2.4 | ✅ Safe |
| `[CITATION: ERA5 reanalysis]` | `\cite{hersbach2020era5}` | 2 | §2.2, §4.6 | ✅ Safe |
| `[CITATION: quantile regression reference]` | `\cite{koenker1978regression}` | 1 | §3.4 | ✅ Safe |

**Total**: 7 placeholders → 11 replacements (accounting for multi-occurrence). All bibliography entries verified from C01E audit.

---

## 3. Category B — Needs Author Confirmation (6 placeholders)

### B1: `[CITATION: power systems operations reference]` — §1.1
**Sentence**: "System operators depend on accurate hourly demand forecasts to schedule generating units, procure operating reserves, clear day-ahead energy markets, and manage transmission constraints."
**Issue**: No bibitem in manuscript. This is standard power systems operations knowledge.
**Options**:
- Author supplies a power systems operations textbook (e.g., Wood & Wollenberg, or a PJM training manual)
- Conservative: delete the citation — the sentence is factual background that doesn't strictly need a reference

### B2: `[CITATION: NERC reliability standards reference]` — §1.1
**Sentence**: "...reserve margins erode, emergency procedures may be triggered, and real-time prices can spike sharply..."
**Issue**: No bibitem. NERC BAL-001 or similar reliability standard.
**Options**:
- Author supplies specific NERC standard (e.g., NERC BAL-001-2)
- Conservative: delete citation — description of consequences is generic

### B3: `[CITATION: load-temperature nonlinearity reference]` — §1.3
**Sentence**: "...each additional degree of cold below the heating base temperature drives progressively larger demand increases as less-efficient heating systems engage..."
**Issue**: No bibitem. C01E identified candidates: `fan2012shortterm` or `taylor2010triple`.
**Options**:
- Author adds bibitem for fan2012shortterm or taylor2010triple
- Conservative: the sentence describes standard heating-degree-day behavior; could remove citation

### B4: `[CITATION: gradient boosting reference]` — §3.3
**Sentence**: "Gradient boosted trees construct an ensemble of shallow decision trees in a stagewise additive manner, with each successive tree fitted to the residuals of the preceding ensemble."
**Issue**: No bibitem. C01E identified `friedman2001greedy`. Manuscript already has `chen2016xgboost` in bbl (unused).
**Options**:
- Author adds `friedman2001greedy` bibitem — canonical GBT paper
- Could cite `chen2016xgboost` for the XGBoost implementation (already in bbl), but this is weaker for "GBT" generally
- Conservative: Friedman (2001) is the standard reference; author should add bibitem

### B5: `[CITATION: gradient boosting quantile regression]` — §3.4
**Sentence**: "...QR-GBT fits a separate gradient boosted ensemble for each target quantile level by minimizing the pinball loss at that quantile."
**Issue**: No bibitem. Could reuse `friedman2001greedy` (pinball loss as special case) or `meinshausen2006quantile`.
**Options**:
- If author adds friedman2001greedy for B4, reuse here: gradient boosting + pinball = same reference
- Author supplies meinshausen2006quantile for quantile regression forests context
- NOTE: Do not create new bibitem unless author approves

### B6: `[CITATION: quantile crossing reference]` — §6.5
**Sentence**: "...consistent with findings in the broader quantile regression literature."
**Issue**: No bibitem. C04E/C04F reports suggested Chernozhukov et al. (2010).
**Options**:
- Author adds Chernozhukov 2010 bibitem ("Quantile and Probability Curves Without Crossing")
- Conservative: soften sentence to avoid citation — "is a known limitation of the independently fitted quantile approach" (no citation needed)

---

## 4. Bibliography Inventory

8 `\bibitem{}` entries in `paper.tex`:

| Key | Description | Supports | Cited? |
|-----|-------------|----------|:------:|
| `koenker1978regression` | Quantile regression (1978) | Cat A #11 | ❌ Not yet |
| `hong2016probabilistic` | GEFCom 2014 review | Cat A #3 | ❌ Not yet |
| `hong2016tutorial` | Probabilistic forecasting tutorial | Cat A #4 | ❌ Not yet |
| `chen2016xgboost` | XGBoost (2016) | Cat B #4 (weak) | ❌ **Unused** |
| `nersc2014polar` | NERC Polar Vortex Review | Cat A #6 | ❌ Not yet |
| `pjm2014polar` | PJM Polar Vortex Review | Cat A #7 | ❌ Not yet |
| `arritt2014us` | Meteorological analysis 2014 | Cat A #8 | ❌ Not yet |
| `hersbach2020era5` | ERA5 reanalysis (2020) | Cat A #9 | ❌ Not yet |

All currently uncited — placeholders haven't been mapped to `\cite{}` yet.

---

## 5. Replacement Plan (Author-Review Table)

| # | Placeholder | Occur. | Recommended Action | Needs Author? | Risk |
|---|-------------|:------:|---------------------|:------------:|:----:|
| A1 | `[CITATION: probabilistic load forecasting review]` | 1 | → `\cite{hong2016probabilistic}` | No | ✅ Low |
| A2 | `[CITATION: probabilistic forecasting in power systems]` | 1 | → `\cite{hong2016tutorial}` | No | ✅ Low |
| A3 | `[CITATION: NERC Polar Vortex Review 2014]` | 2 | → `\cite{nersc2014polar}` | No | ✅ Low |
| A4 | `[CITATION: PJM Polar Vortex Review 2014]` | 2 | → `\cite{pjm2014polar}` | No | ✅ Low |
| A5 | `[CITATION: meteorological analysis of 2014 polar vortex]` | 2 | → `\cite{arritt2014us}` | No | ✅ Low |
| A6 | `[CITATION: ERA5 reanalysis]` | 2 | → `\cite{hersbach2020era5}` | No | ✅ Low |
| A7 | `[CITATION: quantile regression reference]` | 1 | → `\cite{koenker1978regression}` | No | ✅ Low |
| B1 | `[CITATION: power systems operations reference]` | 1 | Author supplies OR remove citation | **Yes** | 🟡 Medium |
| B2 | `[CITATION: NERC reliability standards reference]` | 1 | Author supplies OR remove citation | **Yes** | 🟡 Medium |
| B3 | `[CITATION: load-temperature nonlinearity reference]` | 1 | Author supplies fan2012shortterm/taylor2010triple OR remove | **Yes** | 🟡 Medium |
| B4 | `[CITATION: gradient boosting reference]` | 1 | Author adds friedman2001greedy OR uses chen2016xgboost | **Yes** | 🟡 Medium |
| B5 | `[CITATION: gradient boosting quantile regression]` | 1 | Reuse friedman2001greedy OR author supplies meinshausen2006 | **Yes** | 🟡 Medium |
| B6 | `[CITATION: quantile crossing reference]` | 1 | Author supplies Chernozhukov2010 OR soften sentence | **Yes** | 🟡 Medium |

---

## 6. Data Availability Next-Step Plan

**Current statement (§9)**:
> The PJM RTO hourly metered load data used in this study are publicly available from PJM Data Miner 2. ERA5 retrospective reanalysis fields are publicly available from the Copernicus Climate Data Store. The analysis codebase, including the ERA5 great_lakes_core spatial aggregation procedure (src/data/process_era5_2014.py), will be made available in a public repository upon publication.

**Classification**: OK for internal review. ⚠️ Not OK for submission.

**Author choices**:

**Option A** — Repository/DOI available:
Replace "will be made available in a public repository upon publication" with actual repository URL or Zenodo DOI.
Example: "The analysis codebase is archived at [DOI/URL]."

**Option B** — Repository not ready:
Use a journal-compliant statement. For EPSR (Elsevier), acceptable if code will be archived:
> "The analysis codebase, including the ERA5 great_lakes_core spatial aggregation procedure, will be deposited in a public repository and assigned a DOI upon acceptance."
Or, if author prefers a more conservative approach:
> "The processed data and analysis code are available from the corresponding author upon reasonable request."

Do not edit Data Availability yet — awaiting author decision.

---

## 7. Verdict

**CITATION PLAN READY — NEEDS AUTHOR INPUT**

- **7 of 13 placeholders** can be resolved immediately via safe `\cite{}` replacement (Category A)
- **6 placeholders** require author to supply references, approve existing candidates, or authorize citation removal (Category B)
- **0 Category C blockers** — `distributional robustness` confirmed absent
- **Data Availability** needs author choice between Option A (DOI) or Option B (conservative statement)

---

**C04M citation finalization plan complete. Awaiting author/editor citation decisions before editing paper.tex.**
