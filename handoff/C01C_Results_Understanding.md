# C01C Results Understanding

# Task C01C — Results Understanding

---

## 1. Point-Forecast Results Summary

All figures from Task07A (VALID audit).

**Full-Year 2014 (8,760 hours):**

| Model             | MAE (MW) | Notes                      |
| ----------------- | -------- | -------------------------- |
| Persistence-1h    | 2,745    | Simple but decent baseline |
| Naive-24h         | 5,960    | Fails on trend shifts      |
| Naive-168h        | 8,009    | Worst full-year baseline   |
| Linear Regression | 2,354    | Competitive but limited    |
| **GBoost**        | **721**  | Best point forecast        |
| PJM Day-Ahead     | 1,937    | External benchmark         |

**Jan 6–8 Vortex Window (72 hours):**

| Model             | MAE (MW)  | Notes                                      |
| ----------------- | --------- | ------------------------------------------ |
| Persistence-1h    | 2,805     | Degrades modestly                          |
| Naive-24h         | 15,598    | Catastrophic failure                       |
| Naive-168h        | 24,531    | Catastrophic failure — prior week was warm |
| Linear Regression | 4,248     | Meaningful degradation                     |
| **GBoost**        | **1,705** | Best vortex performance                    |
| PJM Day-Ahead     | 3,148     | Systematic underprediction                 |

**Event Peak (Jan 7, 18:00 EPT = 140,510 MW):**

| Model             | Prediction | Error        |
| ----------------- | ---------- | ------------ |
| GBoost            | 141,898    | −1,388 MW ✅ |
| PJM Day-Ahead     | 137,965    | +2,545 MW    |
| Linear Regression | 134,985    | +5,525 MW    |
| Persistence-1h    | 137,604    | +2,906 MW    |

Key ratio: GBoost vortex MAE improvement over PJM Day-Ahead = **45.8%** (3,148 → 1,705 MW). This is a retrospective weather-informed improvement, not operational superiority.

---

## 2. Probabilistic Forecasting Results Summary

All figures from Task07B (VALID audit). Model: QR-GBT (7 quantiles, q01–q99).

**Coverage and Calibration by Window:**

| Window            | q50 MAE  | Pinball | 90% PI Coverage | 98% PI Coverage | Winkler 90% |
| ----------------- | -------- | ------- | --------------- | --------------- | ----------- |
| Full-year 2014    | 761 MW   | 153     | **86.8%**       | **97.3%**       | 4,627       |
| Jan 6–8 Vortex    | 2,130 MW | 473     | **66.7%** ⚠️    | **84.7%** ⚠️    | 15,476      |
| Jun 16–18 Summer  | 1,060 MW | 209     | 86.1%           | 93.1%           | 6,355       |
| Top 1% load hours | 2,539 MW | 502     | 63.2%           | 82.8%           | 16,168      |

**Event Peak Quantile Check (Jan 7, 18:00 = 140,510 MW):**

| Threshold  | PI Range            | Verdict                  |
| ---------- | ------------------- | ------------------------ |
| 90% PI     | [131,685 — 139,410] | ❌ Peak **outside**      |
| 98% PI     | [121,973 — 139,585] | ❌ Peak **outside**      |
| QR-GBT q99 | 135,386             | Below actual by 5,124 MW |

**Quantile crossing**: 5,786 of 8,760 hours (66%) had crossings → post-hoc monotonic rearrangement applied → 0 crossings remaining. Must be disclosed.

---

## 3. Main Scientific Finding — One Paragraph

Probabilistic load forecasting using gradient-boosted quantile regression achieves acceptable full-year calibration (86.8% nominal 90% PI coverage) under normal operating conditions, but this aggregate metric conceals a severe degradation during the January 2014 Polar Vortex, where 90% PI coverage collapsed to 66.7% and the official event peak of 140,510 MW fell entirely outside the 98% prediction interval. The core finding is that extreme cold-weather stress events induce a distinct load-response regime — driven by heating demand nonlinearity, wind chill amplification, and behavioral effects — that is not captured by models trained on the historical load distribution, even with ERA5 retrospective weather inputs. This means that standard aggregate calibration metrics, evaluated over a full year, are insufficient diagnostics for models intended to support grid operations during high-risk winter stress events.

---

## 4. Why the Result Is Not Simply "QR-GBT Succeeds"

The narrative must be explicitly guarded against a success-framing misread. Here is why:

- **Point forecast**: GBoost achieves 721 MW full-year MAE — strong, but this is with same-hour ERA5 retrospective weather. Under operational conditions (forecast weather), performance would degrade.
- **Probabilistic forecast**: Full-year 86.8% PI coverage sounds like a working calibration, but the vortex window reveals the model was **overconfident precisely when it mattered most** — during the highest-load, highest-risk 72-hour window of the year.
- **Event peak**: The actual load of 140,510 MW exceeded even the **q99 upper bound** (135,386 MW). The model assigned near-zero probability to the observed peak. This is a calibration failure, not a success.
- **Quantile crossing rate**: 66% of test hours required post-hoc rearrangement — a methodological limitation that must be disclosed, not minimized.
- **The correct framing**: QR-GBT is a competitive baseline that reveals the limits of standard probabilistic forecasting during cold-weather extremes — not a solved problem.

---

## 5. Why the Event Peak Outside the 98% PI Is Important

This is the paper's sharpest empirical result and must be handled carefully.

The 98% prediction interval is conventionally interpreted as containing 98% of all possible outcomes — i.e., only a 2-in-100 chance of exceedance. The model's q99 upper bound was 135,386 MW. The actual peak was 140,510 MW — a gap of **5,124 MW above the nominal 99th percentile**.

This finding matters for three reasons:

1. **Grid reliability implications**: Planning reserves and emergency procedures are calibrated against probabilistic load forecasts. A model that assigns near-zero probability to an observed near-annual-peak load could systematically under-trigger emergency reserves.

2. **Distributional shift evidence**: The result is not a one-hour outlier — the entire vortex window shows consistent undercoverage across all quantiles (q50 vortex coverage = 29.2% vs nominal 50%). This is evidence of a regime shift, not noise.

3. **Scientific honesty requirement**: Reporting only the full-year 86.8% coverage without the vortex 66.7% degradation and the 98% PI breach would constitute selective reporting. The 98% PI exceedance is the finding that gives the paper its scientific contribution — it demonstrates the inadequacy of aggregate calibration metrics for extreme events.

---

## 6. Winter vs Summer Comparison

| Metric              | Jan 6–8 Vortex | Jun 16–18 Summer |
| ------------------- | -------------- | ---------------- |
| Max load            | 140,510 MW     | 141,678 MW       |
| q50 MAE             | 2,130 MW       | 1,060 MW         |
| 90% PI coverage     | 66.7%          | 86.1%            |
| Mean pinball loss   | 473            | 209              |
| Winkler score (90%) | 15,476         | 6,355            |

The comparison is scientifically important because it controls for load magnitude. The summer peak is actually **higher** (141,678 vs 140,510 MW) — so if difficulty were purely a function of load level, summer should be harder to forecast. Instead, every probabilistic metric is substantially worse for winter. The vortex q50 MAE is **2× higher**, the pinball loss is **2.3× higher**, and the Winkler score is **3.4× higher** than summer.

This directly supports the paper's central thesis: **extreme cold weather introduces a distinct forecasting regime that is harder than peak summer demand, despite similar load magnitudes.** The cause is the nonlinear relationship between heating-degree-hours, wind chill, and load response during sustained below-freezing temperatures — a regime the model, trained primarily on milder conditions, has not adequately learned.

---

## 7. Results Safe to Use in the Manuscript Without Qualification

These results are from VALID audits and can be stated directly:

✅ GBoost full-year MAE = **721 MW**
✅ GBoost vortex MAE = **1,705 MW**
✅ GBoost Jan 7 18:00 error = **−1,388 MW** (slight overprediction)
✅ PJM Day-Ahead full-year MAE = **1,937 MW**
✅ PJM Day-Ahead vortex MAE = **3,148 MW**
✅ GBoost vortex improvement over PJM DA = **45.8%**
✅ QR-GBT full-year 90% PI coverage = **86.8%**
✅ QR-GBT full-year 98% PI coverage = **97.3%**
✅ QR-GBT vortex 90% PI coverage = **66.7%**
✅ QR-GBT vortex 98% PI coverage = **84.7%**
✅ Event peak (140,510 MW) outside both 90% and 98% PI
✅ Winter q50 MAE (2,130) vs Summer q50 MAE (1,060) — 2× harder
✅ Full-year mean pinball loss = **153**; Vortex pinball loss = **473**
✅ 5,786 crossings (66%) resolved by monotonic rearrangement

---

## 8. Results That Require Caveats

These results are valid but must be accompanied by specific qualifications:

⚠️ **All GBoost and QR-GBT weather-informed metrics** → must carry: _"retrospective ERA5 reanalysis weather input — not operational"_

⚠️ **GBoost vs PJM Day-Ahead improvement (45.8%)** → must carry: _"retrospective setting only; PJM DA uses operational weather forecasts, not reanalysis"_

⚠️ **QR-GBT q50 MAE vs GBoost MAE difference** → must explain: _"q50 minimizes pinball loss, not MSE; direct MAE comparison is expected to favor GBoost"_

⚠️ **Quantile crossing resolution** → must disclose: _"66% of hours required post-hoc monotonic rearrangement; tail quantiles (q01/q99) were most affected"_

⚠️ **NOAA ISD station data** → must label: _"provisional; not primary evidence"_

⚠️ **Top 1% load hours metrics** → note that this window overlaps with, but is not identical to, the vortex window; comparison requires care

---

## 9. Results That Should Not Be Overinterpreted

These are the most dangerous misreading risks:

🔴 **Full-year 86.8% PI coverage** — must not be presented as evidence of general reliability. The vortex degradation to 66.7% is the necessary counterpoint. Presenting only full-year coverage would be selective and misleading.

🔴 **GBoost event peak error of −1,388 MW** — a single-hour result. Must not be generalized to "GBoost reliably captures extreme peaks." The vortex window MAE of 1,705 MW is the correct representative metric.

🔴 **45.8% vortex MAE improvement over PJM DA** — must not be framed as operational superiority. PJM DA operates in real-time with real weather forecasts; GBoost used ERA5 reanalysis. The comparison is methodologically asymmetric.

🔴 **"Calibration analysis shows acceptable performance"** — only acceptable at full-year scale. At every extreme-condition window (vortex, top 1% load hours), calibration fails substantially.

🔴 **Post-hoc quantile rearrangement** — must not be presented as a clean solution. A 66% crossing rate is a signal of underlying model limitations, not merely a post-processing detail. It must be disclosed as a limitation, not normalized.

🔴 **QR-GBT q99 upper bound** — must not be presented as a reliable extreme-event upper bound. It was breached by 5,124 MW at the event peak, meaning the model's representation of the upper tail is inadequate for cold-weather stress events specifically.

---

C01C complete. Ready for C01D.
