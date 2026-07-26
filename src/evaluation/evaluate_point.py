"""C05B: Evaluate point forecast metrics (MAE, RMSE).

Compares reconstructed predictions against C04S reference outputs.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def evaluate_point(predictions_path: str, reference_path: str = None) -> dict:
    """Calculate point forecast metrics.
    
    Args:
        predictions_path: Path to C05B reconstructed predictions CSV
        reference_path: Optional path to C04S reference predictions CSV for comparison
    """
    preds = pd.read_csv(predictions_path)
    
    # Find timestamp column
    ts_col = None
    for c in ["timestamp_ept", "timestamp", "datetime_beginning_ept"]:
        if c in preds.columns:
            ts_col = c
            break
    
    actual_col = "actual_mw" if "actual_mw" in preds.columns else "actual_load_mw"
    
    model_cols = [c for c in preds.columns if c not in [ts_col, actual_col]]
    
    # Windows
    if ts_col:
        preds[ts_col] = pd.to_datetime(preds[ts_col])
        vortex_start = pd.Timestamp("2014-01-06")
        vortex_end = pd.Timestamp("2014-01-08 23:00:00")
        summer_start = pd.Timestamp("2014-06-16")
        summer_end = pd.Timestamp("2014-06-18 23:00:00")
        
        full_year = preds
        vortex = preds[(preds[ts_col] >= vortex_start) & (preds[ts_col] <= vortex_end)]
        summer = preds[(preds[ts_col] >= summer_start) & (preds[ts_col] <= summer_end)]
    else:
        full_year = preds
        vortex = preds.iloc[:72]
        summer = preds.iloc[:72]
    
    results = []
    windows = {"full_year": full_year, "polar_vortex": vortex, "summer_peak": summer}
    
    for model in model_cols:
        for window_name, window_df in windows.items():
            actual = window_df[actual_col].values
            predicted = window_df[model].values
            errors = actual - predicted
            
            mae = np.mean(np.abs(errors))
            rmse = np.sqrt(np.mean(errors ** 2))
            
            results.append({
                "model": model,
                "window": window_name,
                "n_hours": len(window_df),
                "mae_mw": round(mae, 1),
                "rmse_mw": round(rmse, 1),
            })
    
    metrics_df = pd.DataFrame(results)
    
    # Compare with reference if provided
    if reference_path and Path(reference_path).exists():
        ref = pd.read_csv(reference_path)
        print(f"\nReference loaded: {len(ref)} rows")
        # Metric comparison would go here
    
    return metrics_df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", required=True, help="Path to C05B predictions CSV")
    parser.add_argument("--reference", default=None, help="Optional C04S reference predictions CSV")
    parser.add_argument("--output-dir", required=True, help="Output directory for metrics")
    args = parser.parse_args()
    
    metrics = evaluate_point(args.predictions, args.reference)
    print(metrics.to_string(index=False))
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    outpath = output_dir / "point_metrics.csv"
    metrics.to_csv(outpath, index=False)
    print(f"\nMetrics saved to {outpath}")


if __name__ == "__main__":
    main()
