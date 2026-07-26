# Data Provenance — PJM Polar Vortex Manuscript

**Project:** Probabilistic Electricity Demand Forecasting During Extreme Winter Events
**Target Journal:** Electric Power Systems Research (Elsevier)
**Last Updated:** 2026-07-05

---

## Authoritative Data (VERIFIED)

### NOAA Weather Data (4 stations, 2014)
- **Source:** NOAA NCEI Global Hourly ISD
- **License:** Public domain (US government data)
- **Stations:** Chicago O'Hare (72530094846), Baltimore/Washington (72405013743), Philadelphia (72408013739), Cincinnati (72421093814)
- **Coverage:** Full year 2014, 52,288 hourly records after cleaning
- **Processing:** Raw ISD format → cleaned CSV with temperature (°F), wind speed (mph), dewpoint (°F), UTC+EPT timestamps
- **Vortex window:** 72 hours (Jan 6-8, 2014), simple 4-station average (PROVISIONAL)
- **Gap:** Target is 28 stations with population-weighted average. Current 4-station average is warmer than paper's PJM-effective values.

---

## Unverified Data (QUARANTINED — DO NOT USE FOR PUBLICATION)

### PJM Hourly Load (15 days, Jan 2014)
- **Status:** UNVERIFIED — 14-digit decimal precision inconsistent with real measurements
- **Issue:** Contains 153,732 MW peak at Jan 7 12:00, exceeding manuscript's 143,531 MW claim
- **Location:** `legacy_unverified/embedded_data_exports/pjm_hourly_load_2014.csv`

### Polar Vortex 72-Hour Predictions
- **Status:** UNVERIFIED — model outputs from unknown training pipeline
- **Location:** `legacy_unverified/embedded_data_exports/polar_vortex_72h_predictions.csv`

---

## Missing Data (REQUIRED for Publication)

| Dataset | Priority | Status |
|---------|----------|--------|
| PJM hourly actual load 2010-2014 | CRITICAL | Pending PJM Data Miner account approval |
| PJM day-ahead forecast full 2014 | HIGH | Pending PJM Data Miner account approval |
| NOAA weather for additional 24 stations | HIGH | Station IDs need identification |
| Station population weights (Census 2010) | MEDIUM | Not yet sourced |
| Model training outputs | CRITICAL | Pipeline not yet built |

---

## Manual Download Steps

### PJM Data Miner 2
1. Register at https://pjm.com → Tools Sign In
2. Navigate: Markets & Operations → PJM Tools → Data Miner
3. Open Data Miner 2 → feed: Hourly Loads
4. Download CSV for 2010-2014 (one year at a time to avoid timeout)

### NOAA ISD
1. Visit https://www.ncei.noaa.gov/data/global-hourly/access/
2. Navigate to year → download station CSV by USAF-WBAN ID
3. Script: `curl https://www.ncei.noaa.gov/data/global-hourly/access/{YEAR}/{STATION_ID}.csv`
