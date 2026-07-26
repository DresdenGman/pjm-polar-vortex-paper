import pandas as pd

tl = pd.read_csv("data/processed/C07A/canonical_timeline_2010_2022.csv")
al = pd.read_csv("data/processed/C07A/pjm_actual_load_2010_2022.csv")
vtg = pd.read_csv("data/processed/C07A/pjm_selected_vintages_2010_2022.csv")

tl["target_time_utc"] = pd.to_datetime(tl["target_time_utc"], utc=True)
al["target_time_utc"] = pd.to_datetime(al["target_time_utc"], utc=True)
vtg["target_time_utc"] = pd.to_datetime(vtg["target_time_utc"], utc=True)

panel = tl.merge(al, on="target_time_utc", how="left")
panel = panel.merge(vtg, on=["target_time_utc", "operating_date"], how="left")

events = {
    "E2014_PV1": ("2014-01-06", "2014-01-08"),
    "E2015_COLD_anchor": ("2015-02-20", "2015-02-20"),
    "E2018_SNAP": ("2017-12-28", "2018-01-07"),
    "E2022_ELLIOTT": ("2022-12-23", "2022-12-26"),
}

panel["event_id"] = ""
panel["inside_official_event"] = False
panel["operating_date_dt"] = pd.to_datetime(panel["operating_date"])

for eid, (start, end) in events.items():
    mask = (panel["operating_date_dt"] >= start) & (panel["operating_date_dt"] <= end)
    panel.loc[mask, "event_id"] = eid
    panel.loc[mask, "inside_official_event"] = True

panel = panel.drop(columns=["operating_date_dt"])

print(f"Panel: {len(panel)} rows")
print(f"Actual: {panel['actual_load_available'].sum()}/{len(panel)}")
print(f"PJM: {panel['pjm_forecast_available'].sum()}/{len(panel)}")
print(f"Events: {panel['inside_official_event'].sum()} hours")

panel.to_csv("data/processed/C07A/pjm_day_ahead_panel_2010_2022.csv", index=False)
print("Saved.")
