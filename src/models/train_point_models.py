"""C05B: Train point forecast models (Linear Regression, GBoost).

Uses documented hyperparameters from config/c04s_recovered.yaml.
Missing parameters (learning_rate) default to sklearn 1.7.2 defaults.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression

# Recovery defaults for MISSING parameters
# These are assumptions, NOT recovered C04S settings
DEFAULT_RANDOM_STATE = 42
DEFAULT_LEARNING_RATE = 0.1  # sklearn 1.7.2 HistGradientBoostingRegressor default

FEATURE_COLUMNS = [
    "hour", "day_of_week", "month", "is_weekend",
    "load_lag_1h", "load_lag_24h", "load_lag_168h",
    "rolling_mean_24h", "rolling_mean_168h",
    "t_f", "wc_f", "ws", "hdh", "cdh",
]

TARGET = "actual_load_mw"
TS_COL = "timestamp_ept"


def train_and_predict(input_path: str, output_dir: str) -> None:
    """Train Linear Regression and GBoost, export predictions for 2014."""
    df = pd.read_csv(input_path)
    df[TS_COL] = pd.to_datetime(df[TS_COL], format="mixed")
    df = df.sort_values(TS_COL).reset_index(drop=True)

    # Verify all feature columns exist
    missing = [c for c in FEATURE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing feature columns: {missing}")

    test_start = pd.Timestamp("2014-01-01")
    train_df = df[df[TS_COL] < test_start]
    test_df = df[df[TS_COL] >= test_start]

    X_train = train_df[FEATURE_COLUMNS].values
    y_train = train_df[TARGET].values
    X_test = test_df[FEATURE_COLUMNS].values

    print(f"Train: {len(X_train)} rows, Test: {len(X_test)} rows")
    print(f"Train range: {train_df[TS_COL].min()} to {train_df[TS_COL].max()}")
    print(f"Test range:  {test_df[TS_COL].min()} to {test_df[TS_COL].max()}")
    print(f"Features: {len(FEATURE_COLUMNS)} columns")

    # --- Linear Regression ---
    print("\nTraining LinearRegression...")
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_preds = lr.predict(X_test)
    print(f"  Intercept: {lr.intercept_:.1f}")

    # --- GBoost ---
    print("Training GBoost...")
    print(f"  RECOVERY ASSUMPTION: random_state={DEFAULT_RANDOM_STATE} (MISSING in C04S)")
    print(f"  RECOVERY ASSUMPTION: learning_rate={DEFAULT_LEARNING_RATE} (sklearn default, MISSING in C04S)")
    gb = HistGradientBoostingRegressor(
        max_iter=300,
        max_depth=6,
        random_state=DEFAULT_RANDOM_STATE,
        learning_rate=DEFAULT_LEARNING_RATE,
    )
    gb.fit(X_train, y_train)
    gb_preds = gb.predict(X_test)
    print(f"  Training score (R²): {gb.score(X_train, y_train):.4f}")

    # Export
    result = test_df[[TS_COL, TARGET]].copy()
    result["linear_regression"] = lr_preds
    result["gboost_point"] = gb_preds

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outpath = output_dir / "point_model_predictions.csv"
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
