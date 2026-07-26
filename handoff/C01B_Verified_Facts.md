# C01B Verified Facts

# Task C01B — Verified Facts and Forbidden Claims Extraction

---

## 1. Official PJM Load Facts

All numbers below come exclusively from `VERIFIED_FACTSHEET.md` and supersede any value appearing in the legacy manuscript.

| Fact                  | Verified Value                                           |
| --------------------- | -------------------------------------------------------- |
| Data source           | PJM Data Miner 2 — Hourly Load: Metered                  |
| Training period       | 2010–2013 (43,824 rows; 2012 is leap year at 8,784 rows) |
| Cold-event peak       | **140,510.2 MW** at **Jan 7 18:00 EPT**                  |
| 2014 annual peak      | **141,677.9 MW** at **Jun 17 17:00 EPT**                 |
| Event-to-annual ratio | **99.18%**                                               |
| DST handling          | Duplicate Nov 2 01:00 EPT rows preserved; UTC-aligned    |
| 2014 rows in training | **0** (zero leakage confirmed — Task07A/07B VALID)       |

**Key implication**: Summer 2014 peak (141,677.9 MW) is strictly greater than the Polar Vortex peak (140,510.2 MW). The January event is NOT the annual peak.

---

## 2. Corrected Event Framing

| ❌ Old (Forbidden) Framing       | ✅ Required Replacement                                                       |
| -------------------------------- | ----------------------------------------------------------------------------- |
| Jan 2014 = annual peak event     | Jan 2014 = **near-annual-peak cold-weather stress event**                     |
| Jan 2014 = winter record         | "near-annual-peak" — winter-record status **not verified**                    |
| Polar Vortex produced 143,531 MW | Polar Vortex produced **140,510.2 MW** (Jan 7 18:00 EPT)                      |
| Event-to-annual ratio not stated | **99.18%** of 2014 annual peak — use this to justify "near-annual-peak" label |

The approved framing sentence:

> _"The January 6–8, 2014 Polar Vortex produced a near-annual-peak RTO load of 140,510 MW (99.18% of the 2014 annual peak of 141,678 MW recorded on June 17), representing one of the most severe cold-weather demand stress events in PJM history."_

---

## 3. Weather Data Caveat

| Source                               | Status        | Required Label                                    |
| ------------------------------------ | ------------- | ------------------------------------------------- |
| ERA5 reanalysis (t2m, d2m, u10, v10) | AUTHORITATIVE | **"retrospective ERA5 reanalysis weather input"** |
| NOAA ISD (4 stations)                | PROVISIONAL   | Must be labeled provisional — not primary         |
| NASA AIRS imagery                    | UNVERIFIED    | ❌ **Do not reference under any circumstances**   |

**The mandatory ERA5 caveat** — must appear every time ERA5-informed model results are reported:

> _"All weather-informed model results were produced using same-hour ERA5 retrospective reanalysis inputs. This represents an idealized weather scenario; operational deployment would require real-time or forecast weather data."_

This caveat is non-negotiable in the Limitations section and must also appear at first mention in the Results section.

---

## 4. PJM Day-Ahead Forecast Status

| Property     | Value                                        |
| ------------ | -------------------------------------------- |
| Source       | PJM Data Miner 2 — Historical Load Forecasts |
| Coverage     | Full-year 2014, 8,759 hours (DST-aligned)    |
| Role         | **External benchmark only**                  |
| Training use | ❌ Not used in model training                |

**Critical handling rule**: The PJM Day-Ahead forecast must never be described as an internal model component. Its only role is as a benchmark comparator in the Results/Discussion sections. Any claim that our models "outperform PJM operationally" is **forbidden** — the approved replacement is "improves point forecasts in a retrospective weather-informed setting."

---

## 5. Complete Forbidden Claims Registry

| #   | ❌ Forbidden Claim                               | ✅ Safe Replacement                                                    |
| --- | ------------------------------------------------ | ---------------------------------------------------------------------- |
| F01 | "143,531 MW"                                     | "140,510 MW (official PJM Jan 7 18:00 peak)"                           |
| F02 | "153,731 MW" / "153,732 MW"                      | Do not reference — not in official PJM data                            |
| F03 | "winter record peak"                             | "near-annual-peak cold-weather stress event"                           |
| F04 | "all-time peak"                                  | "The 2014 annual peak occurred in summer (141,678 MW, Jun 17)"         |
| F05 | "annual peak during the Polar Vortex"            | "The Polar Vortex produced a near-annual-peak load"                    |
| F06 | "NASA AIRS" (any reference)                      | Do not reference — unverified image removed entirely                   |
| F07 | "operational superiority over PJM"               | "improves point forecasts in a retrospective weather-informed setting" |
| F08 | "deployment-ready"                               | Do not claim — retrospective experiment only                           |
| F09 | "perfect weather forecast"                       | "ERA5 same-hour retrospective reanalysis weather"                      |
| F10 | "state-of-the-art"                               | "compare favorably to baselines" or omit                               |
| F11 | "first-ever"                                     | Avoid — not verified                                                   |
| F12 | "unprecedented"                                  | Avoid entirely                                                         |
| F13 | "reliable during the vortex"                     | "90% PI coverage degraded from 86.8% to 66.7% during the vortex"       |
| F14 | "guaranteed coverage"                            | "empirical coverage of X% was observed"                                |
| F15 | "QR-GBT reliably captures the Polar Vortex peak" | "QR-GBT improves point forecasts but undercovers the cold-event peak"  |
| F16 | "-1.8°F PJM-effective temperature"               | "ERA5 great_lakes_core mean temperature of 2.5°F"                      |
| F17 | "record-setting demand"                          | "near-annual-peak demand"                                              |

---

## 6. How to Replace the 143,531 MW Framing

The legacy manuscript's use of 143,531 MW is **factually invalid** — it does not appear anywhere in official PJM Data Miner 2 records and must be treated as a fabricated artifact. The replacement protocol is:

**Step 1 — Retire the number entirely.** Never mention 143,531 MW, not even to refute it (doing so gives it false prominence).

**Step 2 — Substitute the verified peak.** Every occurrence must be replaced with **140,510.2 MW at Jan 7 18:00 EPT**, sourced explicitly to PJM Data Miner 2 — Hourly Load: Metered.

**Step 3 — Anchor the framing to the ratio.** The approved narrative anchor is the 99.18% event-to-annual-peak ratio, which simultaneously establishes severity _and_ corrects the false "annual peak" claim.

**Step 4 — State the summer comparison.** The 2014 annual peak (141,677.9 MW, Jun 17 17:00 EPT) must be introduced early — ideally in Section 2 (Data and Event Definition) — to prevent any reader from inferring that the Polar Vortex set the annual record.

---

## 7. How the ERA5 Retrospective Reanalysis Caveat Must Be Handled

The caveat is **not optional** and must appear in three locations:

| Location                | Handling                                                                                                                 |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Section 2 (Data)        | First mention: define ERA5 as "same-hour retrospective reanalysis" and explain it is not an operational weather forecast |
| Section 5 (Results)     | At first table/figure citing model results: tag all ERA5-informed outputs with "retrospective weather input"             |
| Section 7 (Limitations) | Dedicated sub-point: explain the ERA5 idealization gap and its implications for real-time deployment                     |

The caveat must prevent any reader from concluding the system is "deployment-ready." Any model performance number (MAE, coverage, pinball loss) reported alongside ERA5 weather inputs carries this caveat implicitly, but the Limitations section must make it explicit.

---

## 8. Absolutely Unsafe Claims for the Manuscript

These are the highest-risk violations — any one of them would compromise the manuscript's factual integrity or invite rejection:

🔴 **Critical / Immediately Disqualifying:**

- Any use of **143,531 MW**, **153,731 MW**, or **153,732 MW** — fabricated figures
- Any claim that the Polar Vortex was the **annual peak** or a **winter record**
- Any reference to **NASA AIRS imagery** — unverified and removed
- Any claim the system is **"deployment-ready"** — contradicted by ERA5 retrospective design
- Any use of **"-1.8°F PJM-effective temperature"** — superseded by ERA5 2.5°F value

🟠 **High Risk / Likely to Draw Reviewer Rejection:**

- **"operational superiority over PJM"** — overstates retrospective results
- **"guaranteed coverage"** — contradicted by observed 66.7% vortex coverage
- **"QR-GBT reliably captures the vortex peak"** — contradicted by undercoverage finding
- **"unprecedented"** / **"first-ever"** — unverified superlatives
- **"state-of-the-art"** — unverified comparative claim

🟡 **Medium Risk / Must Be Replaced with Approved Phrasing:**

- Any ERA5-informed result presented **without the retrospective label**
- PJM Day-Ahead benchmark described as anything other than an **external comparator**
- Any NOAA ISD result presented **without the "provisional" qualifier**

---

C01B complete. Ready for C01C.
