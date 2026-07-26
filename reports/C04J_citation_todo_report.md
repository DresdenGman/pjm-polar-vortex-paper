# C04J — Citation Blocker Resolution and Final TODO Review

**Date**: 2026-07-07  
**Status**: READY FOR FINAL REPLACEMENT AFTER CITATION FIX

---

## A. Executive Verdict

**READY FOR FINAL REPLACEMENT AFTER CITATION FIX** — one hard blocker identified; safe resolution available via conservative rewrite. Remaining 13 placeholders are non-blocking for draft replacement (6 already mapped to verified bibliography entries; 7 need author confirmation but have plausible candidates).

---

## B. Location of `[CITATION: distributional robustness]`

| Field | Value |
|-------|-------|
| **Section** | §1.3 — Extreme Cold as a Tail-Risk Forecasting Problem |
| **Line** | 66 of `paper_C04I_compile_precheck.tex` |
| **Paragraph** | ¶2 of §1.3 (the second and final paragraph) |
| **Position** | Final sentence of paragraph |

---

## C. Surrounding Text

The full paragraph (§1.3, paragraph 2):

> Extreme cold-weather events present a qualitatively distinct forecasting challenge. In large interconnections with significant heating load, cold air outbreaks drive demand responses that differ materially from the moderate-winter conditions that dominate any multi-year training dataset. The load-temperature relationship is nonlinear: each additional degree of cold below the heating base temperature drives progressively larger demand increases as less-efficient heating systems engage and as behavioral responses compound meteorological forcing [CITATION: load-temperature nonlinearity reference]. A data-driven forecasting model trained primarily on moderate winters will have seen few or no examples of the load levels that arise during a severe cold air outbreak, placing the event in or near the extrapolation regime of the model's learned input-output mapping. Under these conditions, a model may produce point forecasts with acceptable average error while simultaneously constructing prediction intervals that are far too narrow — assigning insufficient probability mass to the load levels that actually occur at the peak hour. **This distinction between average-case and tail-case probabilistic performance is not captured by full-year aggregate evaluation metrics, and the gap between them has direct implications for how probabilistic forecasters should be validated before being relied upon for grid reliability decisions [CITATION: distributional robustness -- TODO: NO VERIFIED CANDIDATE].**

The sentence is **the concluding sentence of §1.3** and bridges the Introduction's argument (why extreme cold is a tail-risk problem) with the paper's domain (PJM Polar Vortex, introduced in §1.4). It is **important to the manuscript's argument flow** — it states the paper's evaluation philosophy — but it makes a claim that is **already proven by this study's own Results** (86.8% → 66.7% coverage gap), not by any external distributional robustness literature.

---

## D. Recommended Resolution

### Recommendation: **Option B — Conservative Rewrite**

**Option A (deletion)**: Delete the sentence entirely. The paragraph would end at "…far too narrow — assigning insufficient probability mass to the load levels that actually occur at the peak hour."  
*Drawback*: Loses the explicit framing that aggregate metrics are insufficient for tail-risk evaluation, which is the paper's core contribution.

**Option B (conservative rewrite — RECOMMENDED)**:

Replace:
> This distinction between average-case and tail-case probabilistic performance is not captured by full-year aggregate evaluation metrics, and the gap between them has direct implications for how probabilistic forecasters should be validated before being relied upon for grid reliability decisions [CITATION: distributional robustness -- TODO: NO VERIFIED CANDIDATE].

With:
> This distinction between average-case and tail-case probabilistic performance — directly observable in the present case study, where QR-GBT achieves 86.8% full-year coverage but only 66.7% during the vortex window — underscores the importance of evaluating probabilistic forecasters on disaggregated extreme-event windows rather than relying solely on full-year aggregate calibration diagnostics.

**Rationale for Option B**:
1. Removes the unresolvable citation entirely — no new citation required.
2. Grounds the claim in **this study's own verified results** rather than an external literature appeal.
3. Preserves the paper's core argument about disaggregated evaluation.
4. Introduces the 86.8% → 66.7% number early, giving the Introduction concrete empirical grounding.
5. Does not introduce any new technical or literature claims.
6. The sentence is still conservative — "underscores the importance" is softer than "has direct implications for how..."

---

## E. Remaining Citation Placeholder Audit

| # | Placeholder | Section | Status | Candidate |
|---|-------------|---------|:------:|-----------|
| 1 | `[CITATION: power systems operations reference]` | §1.1 | ⚠️ Author | None in bbl |
| 2 | `[CITATION: NERC reliability standards reference]` | §1.1 | ⚠️ Author | None in bbl |
| 3 | `[CITATION: probabilistic load forecasting review]` | §1.2 | ✅ Mapped | hong2016probabilistic (in bbl) |
| 4 | `[CITATION: probabilistic forecasting in power systems]` | §1.2 | ✅ Mapped | hong2016tutorial (in bbl) |
| 5 | `[CITATION: load-temperature nonlinearity reference]` | §1.3 | ⚠️ Author | fan2012shortterm or taylor2010triple (not in bbl) |
| 6 | `[CITATION: NERC Polar Vortex Review 2014]` | §1.4, §2.4 | ✅ Mapped | nerc2014polar (in bbl) |
| 7 | `[CITATION: PJM Polar Vortex Review 2014]` | §1.4, §2.4 | ✅ Mapped | pjm2014polar (in bbl) |
| 8 | `[CITATION: meteorological analysis of 2014 polar vortex]` | §1.4, §2.4 | ✅ Mapped | arritt2014us (in bbl) |
| 9 | `[CITATION: ERA5 reanalysis]` | §2.2, §4.6 | ✅ Mapped | hersbach2020era5 (in bbl) |
| 10 | `[CITATION: gradient boosting reference]` | §3.3 | ⚠️ Author | friedman2001greedy (not in bbl) |
| 11 | `[CITATION: quantile regression reference]` | §3.4 | ✅ Mapped | koenker1978regression (in bbl) |
| 12 | `[CITATION: gradient boosting quantile regression]` | §3.4 | ⚠️ Author | friedman2001 or meinshausen2006 (not in bbl) |
| 13 | `[CITATION: quantile crossing reference]` | §6.5 | ⚠️ Author | Chernozhukov 2010 (not in bbl) |
| 🔴 | `[CITATION: distributional robustness]` | §1.3 | **BLOCKED** | **Option B rewrite** |

**Summary**: 14 total placeholders. 6 mapped to verified bibliography entries (ready for `\cite{}` replacement). 7 need author confirmation of citation key + bbl entry. **1 is the hard blocker** — resolved via Option B rewrite.

---

## F. Data Availability Status

Current text (§9 — Data Availability):

> The PJM RTO hourly metered load data used in this study are publicly available from PJM Data Miner 2. ERA5 retrospective reanalysis fields are publicly available from the Copernicus Climate Data Store. The analysis codebase, including the ERA5 great_lakes_core spatial aggregation procedure (src/data/process_era5_2014.py), will be made available in a public repository upon publication.

**Classification**: **Acceptable placeholder for draft review.** ⚠️ Not acceptable for journal submission without final confirmation.

Issues:
- "will be made available in a public repository" — this is a forward-looking statement that requires follow-through. Author must confirm repository exists (e.g., GitHub, Zenodo DOI) before submission.
- No DOI or permanent archive link is provided.
- EPSR typically requires a Data Availability Statement confirming public access or explaining restrictions.

---

## G. Final Replacement Readiness

| Readiness Level | Status | Reason |
|-----------------|:------:|--------|
| Internal review PDF | ✅ **READY** | Compiles clean; 0 errors/warnings; all figures/tables present |
| Final `paper.tex` replacement | ⚠️ **READY AFTER CITATION FIX** | Option B rewrite resolves the only hard blocker |
| Journal submission | ❌ **NOT READY** | 7 citation placeholders need author mapping; bibliography incomplete; data availability not finalized |

---

## H. Recommended Next Action

1. **Apply Option B rewrite** to resolve `[CITATION: distributional robustness]` — the only hard blocker
2. **Replace `paper.tex`** with the fixed `paper_C04I_compile_precheck.tex`
3. **Author maps** 7 remaining citation placeholders to `\cite{key}` + `\bibitem` entries
4. **Author finalizes** Data Availability statement with confirmed repository/archive link
5. **Run production compile** cycle: `pdflatex → bibtex → pdflatex × 2`
6. **Submit** to Electric Power Systems Research (Elsevier)

---

**C04J citation TODO review complete. Awaiting editor authorization before applying citation fix.**
