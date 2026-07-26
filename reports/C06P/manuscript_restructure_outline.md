# C06P — Manuscript Restructure Outline

**Status:** Architecture draft — no prose, no numerical results
**Branch:** C06-parallel-evidence

## Proposed Structure

| Section | Title | Key Content | Status |
|---------|-------|------------|--------|
| 1 | Introduction | Operational motivation, research gap, contributions | PENDING_MULTIEVENT |
| 2 | Event-Conditioned Probabilistic Stress-Testing Framework | Framework definition, event selection logic | PENDING_MULTIEVENT |
| 3 | Forecast Origins and Information Availability | Day-ahead protocol, information cutoffs, weather tracks | PENDING_GFS |
| 4 | Data and Multi-Event Protocol | PJM data, ERA5, candidate events, evaluation windows | PARTIALLY_SUPPORTED |
| 5 | Point and Probabilistic Benchmark Methods | Baselines, GBoost, QR-GBT, new probabilistic baselines | PENDING_GFS |
| 6 | Aggregate Forecasting Performance | Full-year metrics, all models, all events | PENDING_GFS |
| 7 | Conditional Reliability During Extreme Events | Per-event breakdown, calibration failure patterns | PENDING_MULTIEVENT |
| 8 | Operational Implications | Reserve margin, peak risk, upper-bound exceedance | PENDING_MULTIEVENT |
| 9 | Oracle vs Operational Weather Sensitivity | ERA5 oracle vs GFS operational comparison | PENDING_GFS |
| 10 | Limitations and Conclusion | Boundary of evidence, next validation steps | PARTIALLY_SUPPORTED |

## Claim-Evidence Map

| Claim ID | Section | Claim | Required Evidence | Current Status |
|----------|---------|-------|-------------------|---------------|
| C01 | 1 | Aggregate calibration masks extreme-event undercoverage | C04S 86.8% → 66.7% gap | VERIFIED |
| C02 | 2 | Event-conditioned framework detects systematic tail risk | Multi-event results | PENDING_MULTIEVENT |
| C03 | 3 | Day-ahead protocol eliminates information leakage | C06 audit | VERIFIED |
| C04 | 5 | QR-GBT as baseline, new methods as contribution | New baseline comparison | PENDING_GFS |
| C05 | 6 | Point forecast performance comparable to operational | Like-for-like GFS comparison | PENDING_GFS |
| C06 | 7 | Cold-weather events consistently degrade PIs | Multi-event coverage results | PENDING_MULTIEVENT |
| C07 | 7 | Quantile crossing contributes to tail failure | Raw vs sorted comparison | VERIFIED (66% in C05B) |
| C08 | 8 | Upper-bound exceedance has operational reserve implications | Exceedance magnitude/duration | VERIFIED (11h, 1,343 MW mean) |
| C09 | 9 | ERA5 oracle shows achievable upper bound | ERA5 vs GFS comparison | PENDING_GFS |
| C10 | 10 | Framework provides stress-testing, not operational superiority | Limitation statement | VERIFIED |

## Target Reductions

- Main text: 8,000–9,000 words (from current ~11,300)
- Conclusion: 250–350 words (from current ~775)
- Remove manuscript TOC, consolidate ERA5 caveats
- References: 45+ (from current 10)
