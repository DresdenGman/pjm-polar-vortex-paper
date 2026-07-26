# Limitations and Caveats — Must Be Preserved in Manuscript

These limitations must appear in the Limitations section (Section 7) of the rewritten manuscript. They may be rephrased for flow but must not be softened, removed, or contradicted elsewhere in the paper.

---

## 1. ERA5 Retrospective Reanalysis (Primary Limitation)

All weather-informed model results use same-hour ERA5 retrospective reanalysis weather inputs. ERA5 is a reanalysis product that incorporates observations after the fact and is not available in real-time operations. This represents an idealized weather scenario: model performance under operational conditions, where only forecast (NWP) weather is available, would be worse. The reported results should be interpreted as an upper bound on accuracy achievable with perfect weather foresight.

**Required text**: Every section reporting ERA5-informed model results must include the phrase "same-hour ERA5 retrospective reanalysis weather input" at first mention.

---

## 2. No Operational NWP Forecast Comparison

Because this study uses ERA5 reanalysis, it cannot quantify the additional forecast degradation attributable to weather forecast error. A future study pairing this modeling approach with ensemble NWP forecasts (e.g., ECMWF, GEFS) would provide operationally realistic uncertainty bounds. The undercoverage documented here is therefore a lower bound — real operational uncertainty would be wider.

---

## 3. Event Framing: Near-Annual-Peak, Not Annual Peak

The January 2014 Polar Vortex produced a near-annual-peak RTO load of 140,510 MW (99.18% of the 2014 annual peak of 141,678 MW, which occurred on June 17). The event is NOT the 2014 annual peak and is NOT a verified winter record. The manuscript must consistently use "near-annual-peak cold-weather stress event" rather than "annual peak," "winter record," or "all-time peak."

---

## 4. Event Peak Outside 98% Prediction Interval

The official cold-event peak (140,510 MW at Jan 7 18:00 EPT) lies outside the QR-GBT nominal 98% prediction interval. The model assigned near-zero probability to the observed peak load. This is a calibration failure, not a model success, and must be presented honestly as such.

---

## 5. Full-Year Calibration Does Not Guarantee Event-Window Calibration

QR-GBT 90% PI empirical coverage is 86.8% for full-year 2014 but degrades to 66.7% during the Jan 6–8 Polar Vortex window. The 98% PI coverage similarly degrades from 97.3% to 84.7%. Aggregate annual calibration metrics conceal severe event-window undercoverage. The manuscript must not present full-year coverage as evidence of general model reliability without the vortex-window counterpoint.

---

## 6. Quantile Crossing and Post-Hoc Rearrangement

QR-GBT produced quantile crossings in 66% of test hours (5,786 of 8,760). These were corrected via post-hoc monotonic rearrangement. While this is a standard correction, the high crossing rate indicates that the model's joint quantile structure is poorly calibrated. The correction is post-hoc rather than architecturally enforced. This must be disclosed in the Methods, Results, and Limitations sections.

---

## 7. NOAA Station Data — Provisional Only

Any NOAA ISD station data referenced in the manuscript carry NOAA's standard provisional data caveat and have not been fully quality-controlled at the time of analysis. ERA5 reanalysis is the primary weather source. NOAA ISD figures should not be treated as authoritative or primary evidence unless explicitly qualified.

---

## 8. SHAP Interpretability — Not Computed

SHAP (SHapley Additive exPlanations) analysis has not been computed as part of this study. No claims about individual feature contributions, feature importance, or quantile-specific driver analysis can be made. Any SHAP-related content from the legacy manuscript must be deleted entirely. If SHAP outputs become available in a later phase, they must be validated before inclusion.

---

## 9. NASA AIRS Imagery — Provenance Unverified

A NASA AIRS surface temperature anomaly image appeared in the legacy manuscript. Its provenance (exact product, date, license, source URL) could not be verified. It has been removed from the manuscript and must not be referenced under any circumstances.

---

## 10. Model Comparison to PJM Day-Ahead — Retrospective Only

The comparison between GBoost/QR-GBT and the PJM day-ahead forecast is a retrospective weather-informed benchmark, not a real-time operational comparison. The PJM day-ahead forecast was produced operationally using forecast weather; GBoost/QR-GBT used ERA5 retrospective reanalysis. The 46% vortex MAE improvement must be framed as "retrospective benchmark improvement," not "operational superiority over PJM."

---

## 11. Single-System Case Study

All results are specific to the PJM Interconnection's service territory, load profile, and the meteorological character of the January 2014 Polar Vortex. Generalizability to other ISOs/RTOs (ERCOT, MISO, ISO-NE, CAISO) or to different types of extreme events (heat waves, ice storms, hurricanes) is not established and requires separate investigation.

---

## 12. No Deployment Readiness Claim

This is a retrospective research study. The model has not been tested in real-time operations, does not use operational weather forecasts, and does not meet the reliability requirements for grid operations. Claims of deployment readiness, operational superiority, or ISO integration readiness are forbidden.

---

## 13. Forbidden Claims (Reference)

The following claims must not appear in the manuscript. See `FORBIDDEN_CLAIMS.md` for approved replacements:

- "143,531 MW" / "153,731 MW" / "153,732 MW" — fabricated values
- "winter record peak" / "all-time peak" — not verified
- "annual peak during the Polar Vortex" — factually incorrect
- "NASA AIRS" — unverified imagery
- "operational superiority over PJM" — overstates retrospective results
- "deployment-ready" — not tested operationally
- "perfect weather forecast" — misrepresents ERA5 reanalysis
- "state-of-the-art" / "first-ever" / "unprecedented" — unverified superlatives
- "guaranteed coverage" — contradicted by observed 66.7% vortex coverage
- "reliable during the vortex" — contradicted by undercoverage finding
