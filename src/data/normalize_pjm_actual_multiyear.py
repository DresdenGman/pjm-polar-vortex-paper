"""C07C: Normalize PJM actual load 2010-2022 onto canonical timeline.

Filters to RTO rows only, handles duplicates, reports quality.
"""
import argparse
import hashlib
from pathlib import Path
import pandas as pd
import pytz


def normalize_actual_load(timeline_path: str, output_path: str, quality_path: str) -> pd.DataFrame:
    eastern = pytz.timezone("America/New_York")
    utc_tz = pytz.UTC

    # Load canonical timeline
    timeline = pd.read_csv(timeline_path)
    timeline["target_time_utc"] = pd.to_datetime(timeline["target_time_utc"], utc=True)

    # Load all years of load data
    all_load = []
    quality_rows = []

    for year in range(2010, 2023):
        fname = f"data/raw/pjm/pjm_load_{year}_rto_hourly.csv"
        try:
            df = pd.read_csv(fname)
        except FileNotFoundError:
            quality_rows.append({"year": year, "status": "FILE_MISSING", "expected_utc": 8784 if year in (2012, 2016, 2020) else 8760})
            continue

        # Filter to RTO rows
        rto_mask = (df["nerc_region"] == "RTO") & (df["mkt_region"] == "RTO") & (df["zone"] == "RTO")
        df_rto = df[rto_mask].copy()

        # Parse UTC
        df_rto["utc"] = pd.to_datetime(df_rto["datetime_beginning_utc"])
        df_rto = df_rto.sort_values("utc")

        expected = 8784 if year in (2012, 2016, 2020) else 8760

        # Duplicate checks
        dup_mask = df_rto["utc"].duplicated(keep=False)
        exact_dups = df_rto[df_rto.duplicated(subset=["utc", "mw"], keep="first")]
        conflict_dups = df_rto[dup_mask & ~df_rto.index.isin(exact_dups.index)]

        unique_utc = df_rto["utc"].nunique()
        missing = expected - unique_utc
        null_load = df_rto["mw"].isna().sum()
        neg_load = (df_rto["mw"] < 0).sum()

        all_load.append(df_rto[["utc", "mw"]])

        quality_rows.append({
            "year": year,
            "expected_utc_hours": expected,
            "raw_RTO_rows": len(df_rto),
            "unique_utc_hours": unique_utc,
            "exact_duplicate_rows": len(exact_dups),
            "conflicting_duplicate_rows": len(conflict_dups),
            "missing_utc_hours": max(0, missing),
            "null_load_rows": null_load,
            "negative_load_rows": neg_load,
            "first_timestamp_utc": str(df_rto["utc"].min()),
            "last_timestamp_utc": str(df_rto["utc"].max()),
            "status": "OK" if missing == 0 and null_load == 0 and neg_load == 0 else "ISSUES",
        })

    # Merge all years — strip tz for join
    combined = pd.concat(all_load)
    combined["utc_clean"] = combined["utc"].dt.tz_localize(None)
    combined = combined.drop_duplicates(subset=["utc_clean"], keep="first")

    # Join with canonical timeline (use tz-naive for merge)
    tl_merge = timeline.copy()
    tl_merge["utc_clean"] = tl_merge["target_time_utc"].dt.tz_localize(None)

    result = tl_merge.merge(
        combined[["utc_clean", "mw"]].rename(columns={"mw": "actual_load_mw"}),
        on="utc_clean",
        how="left",
    )
    result = result.drop(columns=["utc_clean"])

    result["actual_load_available"] = result["actual_load_mw"].notna()
    result["actual_missing_reason"] = result["actual_load_mw"].apply(
        lambda x: "NONE" if pd.notna(x) else "SOURCE_DATA_MISSING"
    )
    result["source_year"] = result["target_time_utc"].dt.year

    # Source file checksum (use 2014 as representative)
    result["source_file_checksum"] = hashlib.sha256(
        open("data/raw/pjm/pjm_load_2014_rto_hourly.csv", "rb").read()
    ).hexdigest()[:16]

    # Select output columns
    out = result[[
        "target_time_utc", "actual_load_mw", "actual_load_available",
        "actual_missing_reason", "source_year", "source_file_checksum",
    ]]

    out.to_csv(output_path, index=False)
    print(f"Normalized load: {len(out)} rows saved to {output_path}")
    print(f"  Available: {out['actual_load_available'].sum()} hours")
    print(f"  Missing: {(~out['actual_load_available']).sum()} hours")

    # Save quality report
    quality = pd.DataFrame(quality_rows)
    quality.to_csv(quality_path, index=False)
    print(f"\nQuality report: {quality_path}")
    print(quality.to_string(index=False))

    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeline", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--quality-report", required=True)
    args = parser.parse_args()
    normalize_actual_load(args.timeline, args.output, args.quality_report)


if __name__ == "__main__":
    main()
