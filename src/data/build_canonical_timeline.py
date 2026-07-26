"""C07C: Build canonical UTC timeline 2010-2022.

113,952 hourly UTC timestamps covering complete PJM operating days.
All timezone/DST logic handled via America/New_York.
"""
import argparse
from pathlib import Path
import pandas as pd
import pytz


def build_canonical_timeline(output_path: str) -> pd.DataFrame:
    eastern = pytz.timezone("America/New_York")
    utc = pytz.UTC

    # Start: 2010-01-01 00:00 EPT → UTC
    start_local = eastern.localize(pd.Timestamp("2010-01-01 00:00:00"))
    start_utc = start_local.astimezone(utc)

    # End exclusive: 2023-01-01 00:00 EPT → UTC
    end_local = eastern.localize(pd.Timestamp("2023-01-01 00:00:00"))
    end_utc = end_local.astimezone(utc)

    # Generate UTC sequence
    utc_range = pd.date_range(start=start_utc, end=end_utc, freq="h", inclusive="left")
    print(f"UTC range: {utc_range[0]} to {utc_range[-1]}")
    print(f"Total hours: {len(utc_range)}")

    rows = []
    for ts_utc in utc_range:
        ts_local = ts_utc.tz_convert(eastern)
        op_date = ts_local.date()
        offset_hours = ts_local.utcoffset().total_seconds() / 3600
        dst_fold = int(ts_local.fold) if hasattr(ts_local, 'fold') else 0

        # Expected hours for this operating date
        # Will be filled after grouping
        rows.append({
            "target_time_utc": ts_utc,
            "target_time_local": ts_local,
            "local_utc_offset": offset_hours,
            "dst_fold": dst_fold,
            "operating_date": op_date,
            "calendar_hour": ts_local.hour,
            "day_of_week": ts_local.dayofweek,
            "month": ts_local.month,
            "year": ts_local.year,
            "weekend_indicator": 1 if ts_local.dayofweek >= 5 else 0,
            "holiday_indicator": 0,
        })

    df = pd.DataFrame(rows)

    # Calculate expected hours per operating date
    date_counts = df.groupby("operating_date").size()
    df["expected_hours_for_operating_date"] = df["operating_date"].map(date_counts)

    # Assertions
    assert len(df) == 113952, f"Expected 113952, got {len(df)}"
    assert df["target_time_utc"].is_unique, "UTC timestamps not unique"
    assert df["operating_date"].min() == pd.Timestamp("2010-01-01").date()
    assert df["operating_date"].max() == pd.Timestamp("2022-12-31").date()

    # DST checks
    spring_dates = df[df["expected_hours_for_operating_date"] == 23]["operating_date"].unique()
    fall_dates = df[df["expected_hours_for_operating_date"] == 25]["operating_date"].unique()
    print(f"23-hour spring days: {len(spring_dates)}")
    print(f"25-hour fall days: {len(fall_dates)}")

    # Check leap years
    for ly in [2012, 2016, 2020]:
        feb29 = df[(df["operating_date"] == pd.Timestamp(f"{ly}-02-29").date())]
        print(f"{ly}-02-29: {len(feb29)} hours")

    # Verify repeated fall-back hours
    for fd in fall_dates[:3]:
        fall_day = df[df["operating_date"] == fd]
        offsets = fall_day["local_utc_offset"].unique()
        print(f"Fall day {fd}: {len(fall_day)}h, offsets={sorted(offsets)}")

    df.to_csv(output_path, index=False)
    print(f"\nSaved to {output_path}")
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    build_canonical_timeline(args.output)


if __name__ == "__main__":
    main()
