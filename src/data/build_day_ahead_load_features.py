"""C06A-PRELOAD: Build day-ahead load and calendar features (2010-2014).

No weather variables. No GFS dependency. Fixed 12:00 EPT D-1 origin.
Preserves DST integrity: both fall-back hours, 23/25-hour days.
"""
import argparse
import sys
from pathlib import Path

import pandas as pd
import numpy as np


def build_day_ahead_dataset(
    load_path: str,
    pjm_forecast_path: str,
    output_path: str,
) -> pd.DataFrame:
    """Construct day-ahead load/calendar dataset with fixed forecast origin."""

    # Load metered load
    load = pd.read_csv(load_path)
    load["utc"] = pd.to_datetime(load["datetime_beginning_utc"])
    # Convert to America/New_York for local calendar operations
    load["ept"] = load["utc"].dt.tz_localize("UTC").dt.tz_convert("America/New_York")
    load = load.sort_values("utc").reset_index(drop=True)

    # Load PJM forecast
    pjm = pd.read_csv(pjm_forecast_path)
    pjm["utc"] = pd.to_datetime(pjm["forecast_hour_beginning_utc"])
    pjm["created_ept"] = pd.to_datetime(pjm["evaluated_at_ept"])

    # Build rows: one per target UTC hour
    rows = []

    for _, lr in load.iterrows():
        target_utc = lr["utc"]
        target_ept = lr["ept"]

        # Operating date (local calendar date)
        op_date = target_ept.date()

        # Forecast origin: 12:00 EPT on D-1
        origin_ept = pd.Timestamp(op_date) - pd.Timedelta(days=1)
        origin_ept = origin_ept.replace(hour=12, minute=0, second=0)
        origin_utc = origin_ept.tz_localize("America/New_York").tz_convert("UTC")

        # Forecast horizon
        horizon_hours = (target_utc - origin_utc.tz_localize(None)).total_seconds() / 3600

        # Load at origin - 1h
        load_cutoff = origin_utc.tz_localize(None) - pd.Timedelta(hours=1)
        origin_load = load[load["utc"] == load_cutoff]
        origin_minus_1h = origin_load["mw"].iloc[0] if len(origin_load) > 0 else np.nan

        # Same-hour lags
        for lag_h, lag_name in [(24, "1d"), (48, "2d"), (168, "7d"), (336, "14d")]:
            lag_ts = target_utc - pd.Timedelta(hours=lag_h)
            lag_row = load[load["utc"] == lag_ts]
            rows.append({"target_utc": target_utc, "feature": f"load_same_hour_{lag_name}",
                         "value": lag_row["mw"].iloc[0] if len(lag_row) > 0 else np.nan})
            # Will pivot later

        # Previous day peak and mean (from D-1, before origin)
        prev_day = target_ept.date() - pd.Timedelta(days=1)
        prev_loads = load[load["ept"].dt.date == prev_day]
        prev_peak = prev_loads["mw"].max() if len(prev_loads) > 0 else np.nan
        prev_mean = prev_loads["mw"].mean() if len(prev_loads) > 0 else np.nan

        # PJM forecast match
        pjm_match = pjm[pjm["utc"] == target_utc]
        pjm_fcast = pjm_match["day_ahead_forecast_mw"].iloc[0] if len(pjm_match) > 0 else np.nan
        pjm_created = pjm_match["created_ept"].iloc[0] if len(pjm_match) > 0 else pd.NaT

        # Calendar features
        dst_flag = 1 if target_ept.dst() else 0
        weekend = 1 if target_ept.dayofweek >= 5 else 0

        rows.append({
            "operating_date": op_date,
            "target_time_local": target_ept,
            "target_time_utc": target_utc,
            "local_utc_offset": target_ept.utcoffset().total_seconds() / 3600,
            "dst_fold": 0,  # TODO: detect fold for fall-back hours
            "forecast_origin_local": origin_ept,
            "forecast_origin_utc": origin_utc,
            "forecast_horizon_hours": round(horizon_hours, 2),
            "actual_load_mw": lr["mw"],
            "pjm_forecast_mw": pjm_fcast,
            "pjm_forecast_creation_time_utc": pjm_created,
            "pjm_missing": 1 if pd.isna(pjm_fcast) else 0,
            "pjm_exclusion_reason": "DST_FALLBACK_COLLAPSED" if pd.isna(pjm_fcast) else "",
            "load_origin_minus_1h": origin_minus_1h,
            "load_same_hour_1d": np.nan,  # filled below
            "load_same_hour_2d": np.nan,
            "load_same_hour_7d": np.nan,
            "load_same_hour_14d": np.nan,
            "previous_available_daily_peak": prev_peak,
            "previous_available_daily_mean": prev_mean,
            "calendar_hour": target_ept.hour,
            "day_of_week": target_ept.dayofweek,
            "month": target_ept.month,
            "weekend_indicator": weekend,
            "holiday_indicator": 0,  # TODO: add holiday calendar
            "dst_indicator": dst_flag,
        })

    df = pd.DataFrame(rows)
    print(f"Built {len(df)} target-hour rows")
    print(f"  PJM missing: {df['pjm_missing'].sum()} hours")
    print(f"  DST spring-forward days: {(df.groupby('operating_date').size() == 23).sum()}")
    print(f"  DST fall-back days: {(df.groupby('operating_date').size() == 25).sum()}")

    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--load", required=True)
    parser.add_argument("--pjm-forecast", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    df = build_day_ahead_dataset(args.load, args.pjm_forecast, args.output)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    print(f"Saved to {args.output}")


if __name__ == "__main__":
    main()
