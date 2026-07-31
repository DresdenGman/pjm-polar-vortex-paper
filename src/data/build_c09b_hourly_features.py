"""C09B: Build hourly weather panel via UTC linear interpolation.

Native leads f018-f048 (3-hourly) -> hourly panel f018-f048 inclusive.
relative_horizon_hour = forecast_hour - 18.
"""
import numpy as np, pandas as pd
from pathlib import Path
from zoneinfo import ZoneInfo

NATIVE = Path("reports/C09B/gfs_native_panel.csv")
OUT = Path("reports/C09B/gfs_hourly_panel.csv")
LEADS = list(range(18, 49))  # 18..48 hourly
PJM_TZ = ZoneInfo("America/New_York")


def main():
    df = pd.read_csv(NATIVE)
    # Validate native panel
    assert len(df) == 176, f"native rows {len(df)} != 176"
    assert df["forecast_hour"].nunique() == 11

    rows = []
    for (sid, init_date), grp in df.groupby(["station_id", "init_date"]):
        grp = grp.sort_values("forecast_hour")
        assert len(grp) == 11, f"{sid} {init_date}: {len(grp)} native leads"
        for var in ["2t", "2r", "10u", "10v", "sp"]:
            interp = np.interp(LEADS, grp["forecast_hour"].values, grp[var].values)
            for fh, val in zip(LEADS, interp):
                rows.append({
                    "station_id": sid,
                    "init_date": init_date,
                    "forecast_hour": fh,
                    "relative_horizon_hour": fh - 18,
                    "variable": var,
                    "value": val,
                })
    hourly = pd.DataFrame(rows)
    # Pivot
    piv = hourly.pivot_table(index=["station_id", "init_date", "forecast_hour", "relative_horizon_hour"],
                             columns="variable", values="value").reset_index()
    piv.columns.name = None
    # Rename to canonical names
    piv = piv.rename(columns={
        "2t": "temperature_2m_kelvin", "2r": "relative_humidity_2m_percent",
        "10u": "wind_u_10m_mps", "10v": "wind_v_10m_mps", "sp": "surface_pressure_pa",
    })
    piv["surface_pressure_hpa"] = piv["surface_pressure_pa"] / 100
    piv["temperature_2m_celsius"] = piv["temperature_2m_kelvin"] - 273.15
    piv["wind_speed_10m_mps"] = np.sqrt(piv["wind_u_10m_mps"]**2 + piv["wind_v_10m_mps"]**2)

    # valid_time_utc = 06Z init + forecast_hour
    init_utc = pd.to_datetime(piv["init_date"], format="ISO8601") + pd.Timedelta(hours=6)
    piv["initialization_utc"] = init_utc
    piv["valid_time_utc"] = init_utc + pd.to_timedelta(piv["forecast_hour"], unit="h")
    piv["valid_time_pjm"] = piv["valid_time_utc"].dt.tz_localize("UTC").dt.tz_convert(PJM_TZ)

    assert len(piv) == 496, f"hourly rows {len(piv)} != 496"
    piv.to_csv(OUT, index=False)
    print(f"Hourly panel: {len(piv)} rows x {len(piv.columns)} cols")
    print(piv.head().to_string())
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    main()
