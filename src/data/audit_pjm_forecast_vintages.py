"""C06A: Audit PJM Day-Ahead forecast vintages for 2014.

Analyses the PJM forecast feed to understand vintage structure:
- Unique forecast creation times
- Age of forecast at the 12:00 EPT origin
- Completeness per operating day
- Which vintages pass the strict protocol selection rules
"""
import argparse
import sys
from pathlib import Path

import pandas as pd


def audit_pjm_vintages(input_path: str, output_dir: str) -> pd.DataFrame:
    """Audit PJM forecast vintages and select qualifying vintages per protocol."""
    df = pd.read_csv(input_path)
    
    # Parse timestamps
    df["forecast_hour_ept"] = pd.to_datetime(df["forecast_hour_beginning_ept"])
    df["forecast_hour_utc"] = pd.to_datetime(df["forecast_hour_beginning_utc"])
    df["created_at_ept"] = pd.to_datetime(df["evaluated_at_ept"])
    
    # Extract operating date (local EPT calendar date)
    df["operating_date"] = df["forecast_hour_ept"].dt.date
    
    # Unique forecast creation times
    unique_creations = df["created_at_ept"].drop_duplicates().sort_values()
    
    print(f"Total forecast rows: {len(df)}")
    print(f"Unique creation times: {len(unique_creations)}")
    print(f"Creation time range: {unique_creations.min()} to {unique_creations.max()}")
    print(f"Operating days: {df['operating_date'].nunique()}")
    
    # For each operating date, find the forecast origin (12:00 EPT on D-1)
    # and check which vintage was used
    results = []
    
    for op_date, group in df.groupby("operating_date"):
        op_date_ts = pd.Timestamp(op_date)
        
        # Forecast origin: 12:00 EPT on D-1
        origin = (op_date_ts - pd.Timedelta(days=1)).replace(
            hour=12, minute=0, second=0, microsecond=0
        )
        
        # Available vintages for this day
        vintages = group["created_at_ept"].drop_duplicates().sort_values()
        
        # Find latest vintage at or before origin, within 12h
        qualifying = vintages[vintages <= origin]
        if len(qualifying) == 0:
            best_vintage = None
            best_age = None
            selected = False
            exclusion = "No vintage before origin"
        else:
            best_vintage = qualifying.iloc[-1]
            best_age_hours = (origin - best_vintage).total_seconds() / 3600
            if best_age_hours > 12:
                selected = False
                exclusion = f"Vintage too old ({best_age_hours:.1f}h > 12h max)"
            else:
                selected = True
                exclusion = ""
                best_age = round(best_age_hours, 1)
        
        # Count target hours
        n_target_hours = len(group)
        n_unique_hours = group["forecast_hour_ept"].nunique()
        expected_hours = 24  # nominal; DST days may differ
        
        results.append({
            "operating_date": op_date,
            "forecast_creation_time_local": str(best_vintage) if best_vintage is not None else "",
            "forecast_creation_time_utc": "",
            "selected_origin_local": str(origin),
            "age_at_origin_hours": best_age,
            "forecast_area": "PJM RTO",
            "expected_target_hours": expected_hours,
            "available_target_hours": n_target_hours,
            "unique_target_hours": n_unique_hours,
            "complete_day": n_target_hours == n_unique_hours,
            "selected": selected,
            "exclusion_reason": exclusion,
        })
    
    inventory = pd.DataFrame(results)
    
    # Summary statistics
    n_selected = inventory["selected"].sum()
    n_total = len(inventory)
    print(f"\nProtocol-qualifying days: {n_selected}/{n_total} ({n_selected/n_total*100:.1f}%)")
    print(f"Rejected: {n_total - n_selected}")
    
    if n_selected > 0:
        ages = inventory[inventory["selected"]]["age_at_origin_hours"]
        print(f"Age at origin (qualifying): {ages.min():.1f}h to {ages.max():.1f}h (mean {ages.mean():.1f}h)")
    
    # Save
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    csv_path = output_dir / "pjm_vintage_inventory.csv"
    inventory.to_csv(csv_path, index=False)
    print(f"\nInventory saved: {csv_path}")
    
    return inventory


def main():
    parser = argparse.ArgumentParser(description="Audit PJM forecast vintages")
    parser.add_argument("--input", required=True, help="Path to PJM day-ahead forecast CSV")
    parser.add_argument("--output-dir", required=True, help="Output directory for audit results")
    args = parser.parse_args()
    
    inventory = audit_pjm_vintages(args.input, args.output_dir)
    
    # Print exclusion breakdown
    rejected = inventory[~inventory["selected"]]
    if len(rejected) > 0:
        print("\nExclusion reasons:")
        for reason, count in rejected["exclusion_reason"].value_counts().items():
            print(f"  {reason}: {count} days")


if __name__ == "__main__":
    main()
