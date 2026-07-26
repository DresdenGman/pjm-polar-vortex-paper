"""C07C: Generate coverage reports and event precheck."""
import pandas as pd

vtg = pd.read_csv("data/processed/C07A/pjm_selected_vintages_2010_2022.csv")
vtg["operating_date"] = pd.to_datetime(vtg["operating_date"])
vtg["year"] = vtg["operating_date"].dt.year

# Annual coverage
coverage = []
for year in range(2010, 2023):
    yr = vtg[vtg["year"] == year]
    if len(yr) == 0:
        continue
    ops = yr["operating_date"].nunique()
    qual = yr.groupby("operating_date")["pjm_forecast_available"].all().sum()
    expected_hrs = len(yr)
    paired = int(yr["pjm_forecast_available"].sum())
    nolatest = int((yr.groupby("operating_date")["latest_candidate_complete"].first() == False).sum())
    fallbacks = int((yr.groupby("operating_date")["older_vintage_fallback_used"].first() == True).sum())
    noelig = int(yr[yr["pjm_missing_reason"] == "NO_ELIGIBLE_VINTAGE"]["operating_date"].nunique())
    ages = yr[yr["vintage_age_hours"].notna()].groupby("operating_date")["vintage_age_hours"].first()
    
    day_hrs = yr.groupby("operating_date").size()
    
    coverage.append({
        "year": year, "expected_operating_days": ops, "qualifying_operating_days": int(qual),
        "expected_target_hours": expected_hrs, "paired_target_hours": paired,
        "missing_forecast_hours": expected_hrs - paired,
        "incomplete_latest_vintage_days": nolatest - noelig,
        "older_vintage_fallback_days": fallbacks,
        "excluded_days": ops - int(qual),
        "median_vintage_age_hours": round(ages.median(), 1) if len(ages) else None,
        "p95_vintage_age_hours": round(ages.quantile(0.95), 1) if len(ages) else None,
        "max_vintage_age_hours": round(ages.max(), 1) if len(ages) else None,
        "no_eligible_days": noelig,
    })

cov = pd.DataFrame(coverage)
cov.to_csv("reports/C07A/pjm_vintage_coverage_by_year.csv", index=False)
print("=== COVERAGE BY YEAR ===")
print(cov.to_string(index=False))

# Exclusions
excl = vtg[vtg["pjm_missing_reason"] != "NONE"].groupby(
    ["operating_date", "pjm_missing_reason"]).size().reset_index(name="hours")
excl.to_csv("reports/C07A/pjm_vintage_exclusions.csv", index=False)

# Event precheck
events = {
    "E2014_PV1": ("2014-01-06", "2014-01-08", 72),
    "E2015_COLD_anchor": ("2015-02-20", "2015-02-20", 24),
    "E2018_SNAP": ("2017-12-28", "2018-01-07", 264),
    "E2022_ELLIOTT": ("2022-12-23", "2022-12-26", 96),
}

precheck = []
for eid, (start, end, exp_hrs) in events.items():
    mask = (vtg["operating_date"] >= start) & (vtg["operating_date"] <= end)
    evt = vtg[mask]
    fcast = int(evt["pjm_forecast_available"].sum())
    same_vin = (evt.groupby("operating_date")["selected_vintage_id"].nunique() == 1).all()
    missing_dates = sorted(evt[~evt["pjm_forecast_available"]]["operating_date"].unique())
    
    if eid == "E2015_COLD_anchor":
        status = "READY" if fcast == exp_hrs else "PJM_COMPARATOR_INCOMPLETE"
    else:
        status = "READY" if fcast == exp_hrs and same_vin else "PJM_COMPARATOR_INCOMPLETE"
    
    precheck.append({
        "event_id": eid, "evaluation_scope": "full_window",
        "expected_hours": exp_hrs, "pjm_forecast_hours": fcast,
        "same_vintage_integrity": same_vin,
        "missing_dates": ",".join(str(d) for d in missing_dates) if missing_dates else "NONE",
        "status": status,
    })

pre = pd.DataFrame(precheck)
pre.to_csv("reports/C07A/event_forecast_availability_precheck.csv", index=False)
print("\n=== EVENT PRECHECK ===")
print(pre.to_string(index=False))

print("\nDone.")
