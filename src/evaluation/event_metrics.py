"""C06P: Legacy C04S probabilistic diagnostics.

Runs the new evaluation toolkit against the frozen C04S prediction files
and produces extended metrics not present in the original analysis.
All results labeled LEGACY_RETROSPECTIVE_NOWCAST_DIAGNOSTIC.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from probabilistic_metrics import (
    mean_pinball_loss,
    quantile_crps_approximation,
    interval_coverage,
    interval_width,
    winkler_score,
    weighted_interval_score,
    reliability_deviation,
    quantile_crossing_diagnostics,
    event_peak_error,
    upper_bound_exceedance,
)
from block_bootstrap import block_bootstrap_ci


def run_legacy_diagnostics(
    predictions_path: str,
    output_dir: str,
) -> None:
    """Run extended metrics on frozen C04S predictions."""
    df = pd.read_csv(predictions_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    actual = df["actual_load_mw"].values

    # Quantile columns
    q_cols = {
        "qr_gbt_q01_mw": 0.01,
        "qr_gbt_q05_mw": 0.05,
        "qr_gbt_q10_mw": 0.10,
        "qr_gbt_q50_mw": 0.50,
        "qr_gbt_q90_mw": 0.90,
        "qr_gbt_q95_mw": 0.95,
        "qr_gbt_q99_mw": 0.99,
    }

    available_cols = {k: v for k, v in q_cols.items() if k in df.columns}
    quantiles = list(available_cols.values())
    preds = {tau: df[col].values for col, tau in available_cols.items()}

    print(f"Quantiles available: {len(available_cols)}/{len(q_cols)}")
    print(f"Rows: {len(df)}")

    results = {
        "label": "LEGACY_RETROSPECTIVE_NOWCAST_DIAGNOSTIC",
        "n_hours": len(df),
    }

    # Pinball + CRPS
    results["mean_pinball_loss"] = round(mean_pinball_loss(actual, preds), 2)
    results["quantile_crps_approximation"] = round(
        quantile_crps_approximation(actual, preds, quantiles), 2
    )

    # 90% interval
    if 0.05 in preds and 0.95 in preds:
        lower90, upper90 = preds[0.05], preds[0.95]
        results["p90_coverage"] = round(interval_coverage(actual, lower90, upper90) * 100, 1)
        results["p90_width_mw"] = round(interval_width(lower90, upper90), 1)
        results["p90_winkler"] = round(winkler_score(actual, lower90, upper90, 0.10), 2)

    # 98% interval
    if 0.01 in preds and 0.99 in preds:
        lower98, upper98 = preds[0.01], preds[0.99]
        results["p98_coverage"] = round(interval_coverage(actual, lower98, upper98) * 100, 1)
        results["p98_width_mw"] = round(interval_width(lower98, upper98), 1)
        results["p98_winkler"] = round(winkler_score(actual, lower98, upper98, 0.02), 2)

    # WIS
    results["weighted_interval_score"] = round(weighted_interval_score(actual, preds, quantiles), 2)

    # Reliability
    reliab = reliability_deviation(actual, preds, quantiles)
    results["reliability_deviation"] = reliab

    # Quantile crossing
    crossing = quantile_crossing_diagnostics(preds, quantiles)
    results["quantile_crossing"] = crossing

    # Event windows
    if "timestamp_ept" in df.columns:
        df["ts"] = pd.to_datetime(df["timestamp_ept"])
        vortex = df[(df["ts"] >= "2014-01-06") & (df["ts"] <= "2014-01-08 23:00:00")]
        summer = df[(df["ts"] >= "2014-06-16") & (df["ts"] <= "2014-06-18 23:00:00")]

        for name, window_df in [("polar_vortex", vortex), ("summer_peak", summer)]:
            wa = window_df["actual_load_mw"].values
            wp = {tau: window_df[col].values for col, tau in available_cols.items()}
            results[f"{name}_pinball"] = round(mean_pinball_loss(wa, wp), 2)
            results[f"{name}_crps"] = round(quantile_crps_approximation(wa, wp, quantiles), 2)
            if 0.05 in wp:
                results[f"{name}_p90_coverage"] = round(
                    interval_coverage(wa, wp[0.05], wp[0.95]) * 100, 1
                )
            if 0.99 in wp:
                peak = event_peak_error(wa, wp[0.99])
                results[f"{name}_peak_error"] = peak
                exceed = upper_bound_exceedance(wa, wp[0.99])
                results[f"{name}_q99_exceedance"] = exceed

    # Bootstrap CI for pinball loss
    pinball_series = np.zeros(len(actual))
    for tau in quantiles:
        residuals = actual - preds[tau]
        pinball_series += np.where(residuals >= 0, tau * residuals, (tau - 1) * residuals)
    pinball_series /= len(quantiles)

    bs_results = block_bootstrap_ci(pinball_series, np.mean)
    results["bootstrap_pinball_ci"] = bs_results

    # Save
    diagnostics = []
    for key, value in results.items():
        if isinstance(value, dict):
            diagnostics.append({"metric": key, **{f"v_{k}": v for k, v in value.items()}})
        elif isinstance(value, list):
            diagnostics.append({"metric": key, "values": str(value)})
        else:
            diagnostics.append({"metric": key, "value": value})

    diag_df = pd.DataFrame(diagnostics)
    diag_path = output_dir / "c04s_probabilistic_diagnostics.csv"
    diag_df.to_csv(diag_path, index=False)
    print(f"\nDiagnostics saved to {diag_path}")

    # Print key findings
    print(f"\nKey Results:")
    print(f"  CRPS (quantile approx): {results['quantile_crps_approximation']:.1f} MW")
    print(f"  90% PI coverage: {results['p90_coverage']}%")
    print(f"  Crossing: {crossing['crossing_hours']}/{crossing['total_hours']} ({crossing['crossing_pct']}%)")
    print(f"  Mean crossing magnitude: {crossing['mean_crossing_magnitude_mw']} MW")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", required=True, help="C04S quantile predictions CSV")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    run_legacy_diagnostics(args.predictions, args.output_dir)


if __name__ == "__main__":
    main()
