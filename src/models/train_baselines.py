"""C05B: Train naive baseline models (Persistence, Daily, Weekly).

These are purely lag-based forecasts — no feature engineering or fitting required.
"""
import argparse
import sys
from pathlib import Path

import pandas as pd


def train_baselines(input_path: str, output_dir: str) -> None:
    """Generate naive baseline predictions for the test year (2014).

    Baselines:
      - persistence_1h: ŷ_t = y_{t-1}
      - naive_24h: ŷ_t = y_{t-24}
      - naive_168h: ŷ_t = y_{t-168}
    """
    df = pd.read_csv(input_path)
    ts_col = "timestamp_ept"
    target_col = "actual_load_mw"

    df[ts_col] = pd.to_datetime(df[ts_col], format="mixed")
    df = df.sort_values(ts_col).reset_index(drop=True)

    # Split at 2014-01-01
    test_start = pd.Timestamp("2014-01-01")
    full = df[df[ts_col] >= pd.Timestamp("2009-12-25")]  # enough for 168h lookback

    test_mask = full[ts_col] >= test_start
    test_df = full[test_mask].copy()

    print(f"Test rows: {len(test_df)}")

    # Build predictions
    test_df["persistence_1h"] = test_df[target_col].shift(1)
    test_df["naive_24h"] = test_df[target_col].shift(24)
    test_df["naive_168h"] = test_df[target_col].shift(168)

    # Drop rows where any baseline is NaN (first 168 rows of 2014)
    predictions = test_df.dropna(subset=["persistence_1h", "naive_24h", "naive_168h"])

    out_cols = [
        ts_col,
        target_col,
        "persistence_1h",
        "naive_24h",
        "naive_168h",
    ]
    result = predictions[out_cols].copy()
    result.columns = [
        "timestamp_ept",
        "actual_mw",
        "persistence_1h",
        "naive_24h",
        "naive_168h",
    ]

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outpath = output_dir / "baseline_predictions.csv"
    result.to_csv(outpath, index=False)
    print(f"Wrote {len(result)} baseline predictions to {outpath}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to modeling_features CSV")
    parser.add_argument("--output-dir", required=True, help="Directory for predictions")
    args = parser.parse_args()
    train_baselines(args.input, args.output_dir)


if __name__ == "__main__":
    main()
