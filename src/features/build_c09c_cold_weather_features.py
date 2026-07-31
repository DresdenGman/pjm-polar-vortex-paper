"""C09C: Leakage-safe cold-weather feature engineering.

Builds features on ALL 124 weather keys (4 samples x 31 hours), then
selects the 96 C08A operating-day target rows via UTC join.

Features (all computed from GFS day-ahead information only):
- wind_chill_celsius      (US NWS wind chill formula)
- heating_degree_celsius  (max(0, 18 - temp_c))
- temp_ramp_3h_celsius    (t - t-3h)
- temp_ramp_6h_celsius
- cold_duration_hours     (consecutive hours temp < 0 C)
- temp_1h_ago, temp_2h_ago (buffer lags)
"""
import numpy as np, pandas as pd
from pathlib import Path

C09B_PANEL = Path("reports/C09B/gfs_hourly_panel.csv")
C08A_PANEL = Path("data/processed/C08A/day_ahead_load_calendar_2010_2022.csv")
OUT = Path("reports/C09C/generated")
OUT.mkdir(parents=True, exist_ok=True)


def wind_chill_celsius(temp_c, wind_mps):
    """US NWS wind chill formula (valid for temp <= 10 C, wind > 4.8 km/h)."""
    wind_kmh = wind_mps * 3.6
    tc = np.asarray(temp_c, dtype=float)
    w = np.asarray(wind_kmh, dtype=float)
    result = np.full_like(tc, np.nan)
    valid = (tc <= 10) & (w > 4.8)
    result[valid] = (13.12 + 0.6215 * tc[valid] - 11.37 * w[valid] ** 0.16
                     + 0.3965 * tc[valid] * w[valid] ** 0.16)
    # When wind too low, wind chill = air temperature
    result[(tc <= 10) & ~valid] = tc[(tc <= 10) & ~valid]
    result[tc > 10] = tc[tc > 10]
    return result


def main():
    w = pd.read_csv(C09B_PANEL)
    w["valid_time_utc"] = pd.to_datetime(w["valid_time_utc"], utc=True)
    w = w.sort_values(["station_id", "init_date", "forecast_hour"]).reset_index(drop=True)

    # Per-station features (within each initialization trajectory)
    feats = []
    for (sid, init), grp in w.groupby(["station_id", "init_date"]):
        g = grp.sort_values("forecast_hour").copy()
        tc = g["temperature_2m_celsius"].values
        u = g["wind_u_10m_mps"].values
        v = g["wind_v_10m_mps"].values
        ws = np.sqrt(u**2 + v**2)

        g["wind_chill_celsius"] = wind_chill_celsius(tc, ws)
        g["heating_degree_celsius"] = np.maximum(0.0, 18.0 - tc)
        g["temp_ramp_3h_celsius"] = tc - np.roll(tc, 1)
        g["temp_ramp_3h_celsius"].iloc[0] = np.nan
        g["temp_ramp_6h_celsius"] = tc - np.roll(tc, 2)
        g["temp_ramp_6h_celsius"].iloc[:2] = np.nan
        g["temp_1h_ago_celsius"] = np.roll(tc, 1)
        g["temp_1h_ago_celsius"].iloc[0] = np.nan
        g["temp_2h_ago_celsius"] = np.roll(tc, 2)
        g["temp_2h_ago_celsius"].iloc[:2] = np.nan

        # Cold duration: consecutive hours below 0 C
        below = (tc < 0).astype(int)
        dur = []
        run = 0
        for b in below:
            run = run + 1 if b else 0
            dur.append(run)
        g["cold_duration_hours"] = dur

        feats.append(g)

    weather_feats = pd.concat(feats, ignore_index=True)
    weather_feats.to_csv(OUT / "weather_features_124.csv", index=False)
    print(f"Weather features (124 keys): {len(weather_feats)} rows")

    # Aggregate to 4-station mean per timestamp
    agg_cols = ["wind_chill_celsius", "heating_degree_celsius", "temp_ramp_3h_celsius",
                "temp_ramp_6h_celsius", "temp_1h_ago_celsius", "temp_2h_ago_celsius",
                "cold_duration_hours", "temperature_2m_celsius",
                "relative_humidity_2m_percent", "wind_speed_10m_mps",
                "surface_pressure_hpa"]
    agg = weather_feats.groupby("valid_time_utc")[agg_cols].mean().reset_index()
    agg = agg.rename(columns={c: f"pjm_{c}" for c in agg_cols})
    agg.to_csv(OUT / "pjm_weather_aggregate_124.csv", index=False)
    print(f"PJM aggregate (124 keys): {len(agg)} rows")

    # Join to C08A operating-day targets
    c08a = pd.read_csv(C08A_PANEL, low_memory=False)
    c08a["target_time_utc"] = pd.to_datetime(c08a["target_time_utc"], utc=True)
    agg["valid_time_utc"] = pd.to_datetime(agg["valid_time_utc"], utc=True)

    joined = c08a.merge(agg, left_on="target_time_utc", right_on="valid_time_utc", how="left")
    pilot = joined[joined["valid_time_utc"].notna()].copy()

    # Restrict to the four authoritative pilot operating days
    PILOT_DAYS = ["2014-01-07", "2014-03-09", "2014-07-15", "2014-11-02"]
    pilot = pilot[pilot["operating_date"].isin(PILOT_DAYS)].copy()
    print(f"Pilot join: {len(pilot)} rows with weather (expect 96)")

    # 24 target rows per operating day
    for d in pilot["operating_date"].unique():
        print(f"  {d}: {len(pilot[pilot['operating_date'] == d])} target hours")

    pilot.to_csv(OUT / "c08a_c09c_pilot_join_96.csv", index=False)
    print(f"Saved pilot join: {OUT / 'c08a_c09c_pilot_join_96.csv'}")


if __name__ == "__main__":
    main()
