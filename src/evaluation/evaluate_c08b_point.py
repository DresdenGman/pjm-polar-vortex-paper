"""C08B: Evaluate point predictions — annual, event, and PJM comparison."""
import argparse, numpy as np, pandas as pd
from pathlib import Path


def load_preds(path):
    p = pd.read_csv(path, low_memory=False)
    p["target_time_utc"] = pd.to_datetime(p["target_time_utc"], utc=True)
    return p


def annual_metrics(preds, output_path):
    model_cols = [c for c in preds.columns if c.endswith("_prediction_mw")]
    years = sorted(preds["operating_date"].str[:4].unique())

    rows = []
    for year in years:
        yr = preds[preds["operating_date"].str.startswith(year)]
        n = len(yr)
        actual = yr["actual_load_mw"].values

        for mc in model_cols:
            pred = yr[mc].values
            mask = ~np.isnan(pred) & ~np.isnan(actual)
            if mask.sum() == 0:
                continue
            a, p = actual[mask], pred[mask]
            err = p - a
            mae = np.mean(np.abs(err))
            rmse = np.sqrt(np.mean(err**2))

            rows.append({
                "year": int(year), "model": mc.replace("_prediction_mw", ""),
                "expected_hours": n, "paired_hours": int(mask.sum()),
                "coverage_pct": round(mask.sum()/n*100, 1),
                "mae_mw": round(mae, 1), "rmse_mw": round(rmse, 1),
                "mean_error_mw": round(np.mean(err), 1),
                "median_absolute_error_mw": round(np.median(np.abs(err)), 1),
                "p90_absolute_error_mw": round(np.percentile(np.abs(err), 90), 1),
                "p95_absolute_error_mw": round(np.percentile(np.abs(err), 95), 1),
                "normalized_mae_pct": round(mae / np.mean(a) * 100, 2),
                "max_underforecast_mw": round(np.max(np.maximum(a - p, 0)), 1),
                "max_overforecast_mw": round(np.max(np.maximum(p - a, 0)), 1),
            })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"Annual metrics: {len(df)} rows")
    for _, r in df[df["model"] == "hist_gbr"].iterrows():
        print(f"  {r['year']}: MAE={r['mae_mw']}")
    return df


def event_metrics(preds, output_path):
    events = {
        "E2014_PV1": ("2014-01-06", "2014-01-08", 72, 63),
        "E2015_COLD_anchor": ("2015-02-20", "2015-02-20", 24, 24),
        "E2018_SNAP": ("2017-12-28", "2018-01-07", 264, 264),
        "E2022_ELLIOTT": ("2022-12-23", "2022-12-26", 96, 96),
    }
    model_cols = [c for c in preds.columns if c.endswith("_prediction_mw")]

    rows = []
    for eid, (start, end, exp, pjm_paired) in events.items():
        evt = preds[(preds["operating_date"] >= start) & (preds["operating_date"] <= end)]
        actual = evt["actual_load_mw"].values

        peak_idx = np.nanargmax(actual)
        peak_mw = actual[peak_idx]

        for mc in model_cols:
            pred = evt[mc].values
            mask = ~np.isnan(pred)
            a, p = actual[mask], pred[mask]
            if len(a) == 0:
                continue
            err = p - a
            mae = np.mean(np.abs(err))

            # Peak error
            peak_pred = pred[peak_idx] if peak_idx < len(pred) else np.nan
            peak_err = peak_pred - peak_mw if not np.isnan(peak_pred) else np.nan

            uf_hours = int(np.sum(p < a))
            uf_runs = []
            cur = 0
            for i in range(len(a)):
                if p[i] < a[i]:
                    cur += 1
                else:
                    if cur > 0:
                        uf_runs.append(cur)
                    cur = 0
            if cur > 0:
                uf_runs.append(cur)

            rows.append({
                "event_id": eid, "model": mc.replace("_prediction_mw", ""),
                "expected_hours": exp, "model_hours": len(a),
                "model_pjm_common_hours": pjm_paired,
                "mae_mw": round(mae, 1),
                "rmse_mw": round(np.sqrt(np.mean(err**2)), 1),
                "mean_error_mw": round(np.mean(err), 1),
                "underforecast_hours": uf_hours,
                "underforecast_pct": round(uf_hours/len(a)*100, 1),
                "cumulative_underforecast_mwh": round(np.sum(np.maximum(a-p, 0)), 1),
                "max_underforecast_mw": round(np.max(np.maximum(a-p, 0)), 1),
                "longest_underforecast_run_hours": max(uf_runs) if uf_runs else 0,
                "actual_event_peak_mw": round(peak_mw, 1),
                "prediction_at_peak_mw": round(peak_pred, 1) if not np.isnan(peak_pred) else None,
                "error_at_peak_mw": round(peak_err, 1) if not np.isnan(peak_err) else None,
                "abs_error_at_peak_mw": round(abs(peak_err), 1) if not np.isnan(peak_err) else None,
            })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"Event metrics: {len(df)} rows")
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    preds = load_preds(args.predictions)
    annual_metrics(preds, f"{args.output_dir}/annual_point_metrics.csv")
    event_metrics(preds, f"{args.output_dir}/event_point_metrics.csv")
    print("Evaluation complete.")


if __name__ == "__main__":
    main()
