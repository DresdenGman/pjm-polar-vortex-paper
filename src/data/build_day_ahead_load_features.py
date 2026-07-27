"""C08A: Fast vectorized day-ahead load feature builder."""
import argparse, numpy as np, pandas as pd
from pathlib import Path

def build(panel_path, output_path):
    p = pd.read_csv(panel_path, low_memory=False)
    p["target_utc"] = pd.to_datetime(p["target_time_utc"], utc=True)
    p["origin_utc"] = pd.to_datetime(p["forecast_origin_utc"], utc=True, errors="coerce")
    p["op_date"] = pd.to_datetime(p["operating_date"])

    n = len(p)
    print(f"Panel: {n} rows")

    # Build result with calendar and provenance columns
    result = p[[
        "operating_date", "target_time_local", "target_time_utc",
        "local_utc_offset", "dst_fold", "calendar_hour", "day_of_week",
        "month", "year", "weekend_indicator", "holiday_indicator",
        "expected_hours_for_operating_date",
        "actual_load_mw", "actual_load_available", "actual_missing_reason",
        "pjm_forecast_mw", "pjm_forecast_available", "pjm_missing_reason",
        "selected_vintage_id", "selected_evaluated_at_utc", "vintage_age_hours",
    ]].copy()

    result["forecast_origin_utc"] = p["forecast_origin_utc"]
    result["dst_indicator"] = (p["local_utc_offset"].astype(float) != -5).astype(int)

    # Cutoff
    cutoff = p["origin_utc"] - pd.Timedelta(hours=1)
    cutoff[p["origin_utc"].isna()] = pd.NaT
    result["load_information_cutoff_utc"] = cutoff

    # Forecast horizon (only where origin valid)
    valid_o = p["origin_utc"].notna()
    fh = pd.Series(np.nan, index=p.index)
    fh[valid_o] = (p.loc[valid_o, "target_utc"] - p.loc[valid_o, "origin_utc"]).dt.total_seconds() / 3600
    result["forecast_horizon_hours"] = fh

    # --- LOAD FEATURES via timestamp-indexed merge ---
    # Build a lookup: target_utc (tz-naive int64) -> actual_load_mw
    p["utc_int"] = p["target_utc"].astype("int64")
    load_lookup = p[["utc_int", "actual_load_mw"]].drop_duplicates("utc_int").set_index("utc_int")

    # 1) load_origin_minus_1h: load at origin - 1h
    src_utc = p["origin_utc"] - pd.Timedelta(hours=1)
    result["load_origin_minus_1h_source_utc"] = src_utc
    # Merge via int64 nanosecond epoch
    src_df = pd.DataFrame({"key": src_utc.astype("int64").values, "idx": p.index})
    src_df = src_df[src_df["key"].notna()]
    merged = src_df.set_index("key").join(load_lookup, how="left")
    result["load_origin_minus_1h"] = np.nan
    result.loc[merged["idx"].values, "load_origin_minus_1h"] = merged["actual_load_mw"].values
    result["load_origin_minus_1h_available"] = result["load_origin_minus_1h"].notna()
    result["load_origin_minus_1h_missing_reason"] = np.where(
        result["load_origin_minus_1h_available"], "NONE", "SOURCE_DATA_MISSING"
    )

    # 2) Same-hour lags (1d, 2d, 7d, 14d)
    for lag_name, lag_h in [("1d", 24), ("2d", 48), ("7d", 168), ("14d", 336)]:
        col = f"load_same_hour_{lag_name}"
        src_col = f"{col}_source_utc"
        avail_col = f"{col}_available"
        reason_col = f"{col}_missing_reason"

        src_utc = p["target_utc"] - pd.Timedelta(hours=lag_h)
        result[src_col] = src_utc

        # Merge via int64
        src_df = pd.DataFrame({
            "key": src_utc.astype("int64").values,
            "idx": p.index,
            "cutoff_int": cutoff.astype("int64").values,
        })
        merged = src_df.set_index("key").join(load_lookup, how="left").reset_index()
        merged = merged.rename(columns={"actual_load_mw": col})

        result[col] = np.nan
        result.loc[merged["idx"].values, col] = merged[col].values

        # Nullify if after cutoff
        after = merged["key"] > merged["cutoff_int"]
        bad_idx = merged.loc[after, "idx"].values
        result.loc[bad_idx, col] = np.nan

        result[avail_col] = result[col].notna()

        reasons = np.full(n, "SOURCE_DATA_MISSING", dtype=object)
        reasons[result[avail_col].values] = "NONE"
        reasons[bad_idx] = "AFTER_ORIGIN_CUTOFF"
        result[reason_col] = reasons

        n_avail = result[avail_col].sum()
        n_cutoff = (result[reason_col] == "AFTER_ORIGIN_CUTOFF").sum()
        print(f"  {col}: {n_avail}/{n} avail, {n_cutoff} after-cutoff")

    # 3) Previous daily peak and mean (fast groupby)
    # For each row, find the latest complete prior day
    daily_stats = p.groupby("op_date")["actual_load_mw"].agg(["max", "mean", "count"])
    daily_stats.columns = ["peak", "mean", "count"]
    daily_stats["complete"] = daily_stats["count"] == p.groupby("op_date").size()

    # For each operating date, the previous complete day's stats
    op_dates = sorted(daily_stats.index)
    prev_peak_map = {}
    prev_mean_map = {}
    prev_date_map = {}
    last_complete_peak = np.nan
    last_complete_mean = np.nan
    last_complete_date = None
    for od in op_dates:
        prev_date_map[od] = last_complete_date
        prev_peak_map[od] = last_complete_peak
        prev_mean_map[od] = last_complete_mean
        if daily_stats.loc[od, "complete"]:
            last_complete_peak = daily_stats.loc[od, "peak"]
            last_complete_mean = daily_stats.loc[od, "mean"]
            last_complete_date = str(od.date())

    result["previous_available_daily_operating_date"] = p["op_date"].map(prev_date_map)
    result["previous_available_daily_peak"] = p["op_date"].map(prev_peak_map)
    result["previous_available_daily_mean"] = p["op_date"].map(prev_mean_map)

    for f in ["previous_available_daily_peak", "previous_available_daily_mean"]:
        result[f"{f}_available"] = result[f].notna()
        result[f"{f}_missing_reason"] = np.where(result[f].notna(), "NONE", "INSUFFICIENT_HISTORY")

    # Save
    result.to_csv(output_path, index=False)
    print(f"Saved {len(result)} rows → {output_path}")

    # Summary
    for col in ["load_origin_minus_1h", "load_same_hour_1d", "load_same_hour_2d",
                "load_same_hour_7d", "load_same_hour_14d",
                "previous_available_daily_peak", "previous_available_daily_mean"]:
        a = result[f"{col}_available"].sum() if f"{col}_available" in result.columns else result[col].notna().sum()
        print(f"  {col}: {a}/{n}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--panel", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    build(a.panel, a.output)


if __name__ == "__main__":
    main()
