"""C05B: Train QR-GBT quantile regression models.

Trains 7 independent HistGradientBoostingRegressor models (loss='quantile'),
one per quantile level: q01, q05, q10, q50, q90, q95, q99.

Quantile crossing is PRESERVED (not sorted) in this phase unless
C04S documentation proves sorting was used.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

# Recovery defaults for MISSING parameters
DEFAULT_LEARNING_RATE = 0.1

QUANTILES = [0.01, 0.05, 0.10, 0.50, 0.90, 0.95, 0.99]
N_ITER = 300
MAX_DEPTH = 6
RANDOM_STATE = 42

FEATURE_COLUMNS = [
    "hour", "day_of_week", "month", "is_weekend",
    "load_lag_1h", "load_lag_24h", "load_lag_168h",
    "rolling_mean_24h", "rolling_mean_168h",
    "t_f", "wc_f", "ws", "hdh", "cdh",
]
TARGET = "actual_load_mw"
TS_COL = "timestamp_ept"


def count_quantile_crossings(df: pd.DataFrame) -> int:
    """Count hours where at least one quantile pair crosses."""
    q_cols = [f"qr_gbt_q{int(q*100):02d}" for q in QUANTILES]
    crossings = 0
    for i in range(len(q_cols) - 1):
        crossings += (df[q_cols[i]] > df[q_cols[i + 1]]).sum()
    # Count hours with ANY crossing
    hour_crossings = 0
    for _, row in df[q_cols].iterrows():
        values = row.values
        if not np.all(np.diff(values) >= 0):
            hour_crossings += 1
    return hour_crossings


def train_and_predict(input_path: str, output_dir: str) -> None:
    df = pd.read_csv(input_path)
    df[TS_COL] = pd.to_datetime(df[TS_COL], format="mixed")
    df = df.sort_values(TS_COL).reset_index(drop=True)

    missing = [c for c in FEATURE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing feature columns: {missing}")

    test_start = pd.Timestamp("2014-01-01")
    train_df = df[df[TS_COL] < test_start]
    test_df = df[df[TS_COL] >= test_start]

    X_train = train_df[FEATURE_COLUMNS].values
    y_train = train_df[TARGET].values
    X_test = test_df[FEATURE_COLUMNS].values

    print(f"Train: {len(X_train)}, Test: {len(X_test)}")
    print(f"Quantiles: {QUANTILES}")
    print(f"RECOVERY ASSUMPTION: learning_rate={DEFAULT_LEARNING_RATE} (sklearn default, MISSING in C04S)")

    result = test_df[[TS_COL, TARGET]].copy()

    for q in QUANTILES:
        col_name = f"qr_gbt_q{int(q*100):02d}"
        print(f"\nTraining QR-GBT q={q:.2f}...")
        model = HistGradientBoostingRegressor(
            loss="quantile",
            quantile=q,
            max_iter=N_ITER,
            max_depth=MAX_DEPTH,
            random_state=RANDOM_STATE,
            learning_rate=DEFAULT_LEARNING_RATE,
        )
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        result[col_name] = preds
        print(f"  Score: {model.score(X_train, y_train):.4f}")

    # Count crossings (PRESERVED — not sorted)
    crossing_hours = count_quantile_crossings(result)
    crossing_pct = crossing_hours / len(result) * 100
    print(f"\nQuantile crossing: {crossing_hours}/{len(result)} hours ({crossing_pct:.1f}%)")
    print("NOTE: Quantile crossing is PRESERVED (not sorted) per C05B rules.")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outpath = output_dir / "quantile_predictions.csv"
    result.to_csv(outpath, index=False)
    print(f"\nWrote {len(result)} predictions to {outpath}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to modeling_features CSV")
    parser.add_argument("--output-dir", required=True, help="Directory for predictions")
    args = parser.parse_args()
    train_and_predict(args.input, args.output_dir)


if __name__ == "__main__":
    main()
