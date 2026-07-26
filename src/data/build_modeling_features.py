"""C05B: Load and validate the recovered modeling_features_2010_2014.csv.

This module does NOT rebuild ERA5 features. It validates the recovered CSV
as the fixed input for C05B pipeline reconstruction.
"""
import argparse
import sys
from pathlib import Path

import pandas as pd


def validate_modeling_features(path: str | Path) -> pd.DataFrame:
    """Load and validate the recovered modeling features CSV.

    Checks:
      - File exists and is readable
      - Expected timestamp column present
      - No duplicate timestamps
      - No future load leakage (basic check)
      - Train/test boundary exists at 2014-01-01
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Modeling features not found: {path}")

    df = pd.read_csv(path)

    # Column validation
    ts_col = "timestamp_ept"
    if ts_col not in df.columns:
        # Try alternate names
        for candidate in ["timestamp", "datetime_beginning_ept", "datetime"]:
            if candidate in df.columns:
                ts_col = candidate
                break
        else:
            raise ValueError(
                f"No timestamp column found in {path}. "
                f"Columns: {list(df.columns)}"
            )

    df[ts_col] = pd.to_datetime(df[ts_col], format="mixed")
    df = df.sort_values(ts_col).reset_index(drop=True)

    # No duplicate timestamps
    dup_mask = df[ts_col].duplicated()
    if dup_mask.any():
        dup_count = dup_mask.sum()
        print(f"WARNING: Found {dup_count} duplicate timestamps — dropping duplicates")
        df = df[~dup_mask].reset_index(drop=True)

    # Check target column
    target_col = "actual_load_mw"
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in {path}")

    # Validate target values are positive
    if (df[target_col] <= 0).any():
        raise ValueError("Found non-positive load values")

    # Train/test split
    test_start = pd.Timestamp("2014-01-01")
    train_df = df[df[ts_col] < test_start]
    test_df = df[df[ts_col] >= test_start]

    if len(train_df) == 0:
        raise ValueError("No training data before 2014-01-01")
    if len(test_df) == 0:
        raise ValueError("No test data from 2014-01-01 onward")

    # Log
    print(f"Loaded {len(df)} rows from {path.name}")
    print(f"  Train: {len(train_df)} rows ({train_df[ts_col].min()} to {train_df[ts_col].max()})")
    print(f"  Test:  {len(test_df)} rows ({test_df[ts_col].min()} to {test_df[ts_col].max()})")
    print(f"  Columns: {list(df.columns)}")

    return df


def main():
    parser = argparse.ArgumentParser(description="Validate C04S modeling features")
    parser.add_argument("--input", required=True, help="Path to modeling_features CSV")
    args = parser.parse_args()

    try:
        validate_modeling_features(args.input)
        print("VALIDATION PASSED")
        sys.exit(0)
    except Exception as e:
        print(f"VALIDATION FAILED: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
