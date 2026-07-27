"""C07E: PJM multi-event benchmark evaluator.

Computes hourly errors, event-level metrics, cross-event summaries,
and generates benchmark figures — all from the canonical panel.
"""
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path


EVENTS = {
    "E2014_PV1": {
        "label": "2014 Polar Vortex",
        "start": "2014-01-06", "end": "2014-01-08",
        "expected_hours": 72, "paired_hours": 63,
        "scope": "REGISTERED_EVENT_PAIRED_HOURS",
        "completeness": "PARTIAL_SOURCE_DATA_STRUCTURE",
    },
    "E2015_COLD_anchor": {
        "label": "2015 Feb 20 Anchor Day",
        "start": "2015-02-20", "end": "2015-02-20",
        "expected_hours": 24, "paired_hours": 24,
        "scope": "ANCHOR_DAY_ONLY",
        "completeness": "BOUNDARY_PENDING",
    },
    "E2018_SNAP": {
        "label": "2017-2018 Cold Snap",
        "start": "2017-12-28", "end": "2018-01-07",
        "expected_hours": 264, "paired_hours": 264,
        "scope": "COMPLETE_REGISTERED_EVENT",
        "completeness": "COMPLETE",
    },
    "E2022_ELLIOTT": {
        "label": "Winter Storm Elliott",
        "start": "2022-12-23", "end": "2022-12-26",
        "expected_hours": 96, "paired_hours": 96,
        "scope": "COMPLETE_REGISTERED_EVENT",
        "completeness": "COMPLETE",
    },
}


def load_panel(path):
    panel = pd.read_csv(path, low_memory=False)
    panel["target_time_utc"] = pd.to_datetime(panel["target_time_utc"], utc=True)
    panel["target_time_local"] = pd.to_datetime(panel["target_time_local"], utc=True)
    panel["operating_date"] = pd.to_datetime(panel["operating_date"])
    return panel


def compute_hourly_errors(panel, output_path):
    rows = []
    for eid, cfg in EVENTS.items():
        mask = (panel["operating_date"] >= cfg["start"]) & (panel["operating_date"] <= cfg["end"])
        evt = panel[mask].copy()

        actual = evt["actual_load_mw"]
        fcast = evt["pjm_forecast_mw"]
        paired = evt["pjm_forecast_available"]

        signed = np.where(paired, fcast - actual, np.nan)
        abs_err = np.where(paired, np.abs(fcast - actual), np.nan)
        sq_err = np.where(paired, (fcast - actual) ** 2, np.nan)
        uf = np.where(paired, np.maximum(actual - fcast, 0), np.nan)
        of = np.where(paired, np.maximum(fcast - actual, 0), np.nan)
        ape = np.where(paired, np.abs(fcast - actual) / actual * 100, np.nan)

        seg_id = 0
        seg_ids = []
        for i, p in enumerate(paired):
            if not p:
                seg_ids.append(None)
            else:
                if i == 0 or not paired.iloc[i-1]:
                    seg_id += 1
                seg_ids.append(seg_id)

        evt_hr = pd.DataFrame({
            "event_id": eid,
            "evaluation_scope": cfg["scope"],
            "operating_date": evt["operating_date"].values,
            "target_time_local": evt["target_time_local"].values,
            "target_time_utc": evt["target_time_utc"].values,
            "actual_load_mw": actual.values,
            "pjm_forecast_mw": fcast.values,
            "paired": paired.values,
            "signed_error_mw": signed,
            "absolute_error_mw": abs_err,
            "squared_error_mw2": sq_err,
            "underforecast_mw": uf,
            "overforecast_mw": of,
            "absolute_percentage_error": ape,
            "underforecast_indicator": np.where(paired, fcast < actual, np.nan),
            "overforecast_indicator": np.where(paired, fcast > actual, np.nan),
            "selected_vintage_id": evt["selected_vintage_id"].values if "selected_vintage_id" in evt.columns else "",
            "selected_evaluated_at_utc": evt["selected_evaluated_at_utc"].values if "selected_evaluated_at_utc" in evt.columns else "",
            "vintage_age_hours": evt["vintage_age_hours"].values if "vintage_age_hours" in evt.columns else None,
            "source_structure_missing": ~paired,
            "missing_reason": evt["pjm_missing_reason"].values if "pjm_missing_reason" in evt.columns else "",
            "contiguous_paired_segment_id": seg_ids,
        })
        rows.append(evt_hr)

    result = pd.concat(rows, ignore_index=True)
    result.to_csv(output_path, index=False)
    print(f"Hourly errors: {len(result)} rows → {output_path}")
    return result


def compute_event_metrics(hourly, output_path):
    summaries = []
    for eid, cfg in EVENTS.items():
        eh = hourly[hourly["event_id"] == eid]
        paired = eh[eh["paired"]]
        n_total = len(eh)
        n_paired = len(paired)

        if n_paired == 0:
            summaries.append({"event_id": eid, "paired_hours": 0})
            continue

        a = paired["actual_load_mw"].values
        f = paired["pjm_forecast_mw"].values
        n = len(paired)

        mae = np.mean(np.abs(f - a))
        rmse = np.sqrt(np.mean((f - a) ** 2))
        mean_err = np.mean(f - a)
        med_err = np.median(f - a)
        med_abs = np.median(np.abs(f - a))
        p90_abs = np.percentile(np.abs(f - a), 90)
        p95_abs = np.percentile(np.abs(f - a), 95)
        nmae = mae / np.mean(a) * 100

        uf_hours = int(np.sum(f < a))
        of_hours = int(np.sum(f > a))
        cum_uf = np.sum(np.maximum(a - f, 0))
        cum_of = np.sum(np.maximum(f - a, 0))

        # Peak
        all_a = eh["actual_load_mw"].values
        peak_idx = np.nanargmax(all_a)
        peak_mw = all_a[peak_idx]
        peak_time = eh.iloc[peak_idx]["target_time_local"]
        peak_paired = eh.iloc[peak_idx]["paired"]
        if peak_paired:
            pjm_at_peak = eh.iloc[peak_idx]["pjm_forecast_mw"]
            err_at_peak = pjm_at_peak - peak_mw
            abs_at_peak = abs(err_at_peak)
            uf_at_peak = max(peak_mw - pjm_at_peak, 0)
            ape_at_peak = abs(err_at_peak) / peak_mw * 100
        else:
            pjm_at_peak = None
            err_at_peak = None
            abs_at_peak = None
            uf_at_peak = None
            ape_at_peak = None

        # Run lengths
        uf_runs = []
        of_runs = []
        current_uf = 0
        current_of = 0
        for i in range(len(eh)):
            if eh.iloc[i]["paired"]:
                if eh.iloc[i]["signed_error_mw"] < 0:
                    current_uf += 1
                    current_of = 0
                elif eh.iloc[i]["signed_error_mw"] > 0:
                    current_of += 1
                    current_uf = 0
                else:
                    current_uf = 0
                    current_of = 0
            else:
                if current_uf:
                    uf_runs.append(current_uf)
                if current_of:
                    of_runs.append(current_of)
                current_uf = 0
                current_of = 0
        if current_uf:
            uf_runs.append(current_uf)
        if current_of:
            of_runs.append(current_of)

        max_uf_mw = np.max(np.maximum(a - f, 0)) if n_paired else None
        max_of_mw = np.max(np.maximum(f - a, 0)) if n_paired else None
        if n_paired:
            uf_argmax = int(np.argmax(np.maximum(a - f, 0)))
            of_argmax = int(np.argmax(np.maximum(f - a, 0)))
            max_uf_time = str(paired.iloc[uf_argmax]["target_time_local"])
            max_of_time = str(paired.iloc[of_argmax]["target_time_local"])
        else:
            max_uf_time = None
            max_of_time = None

        summaries.append({
            "event_id": eid, "event_label": cfg["label"],
            "evaluation_scope": cfg["scope"],
            "event_start_local": cfg["start"], "event_end_local": cfg["end"],
            "expected_hours": cfg["expected_hours"],
            "actual_available_hours": int(eh["actual_load_mw"].notna().sum()),
            "pjm_available_hours": n_paired, "paired_hours": n_paired,
            "paired_coverage_pct": round(n_paired / n_total * 100, 1),
            "comparator_completeness": cfg["completeness"],
            "mae_mw": round(mae, 1), "rmse_mw": round(rmse, 1),
            "mean_error_mw": round(mean_err, 1),
            "median_error_mw": round(med_err, 1),
            "median_absolute_error_mw": round(med_abs, 1),
            "p90_absolute_error_mw": round(p90_abs, 1),
            "p95_absolute_error_mw": round(p95_abs, 1),
            "normalized_mae_pct_mean_load": round(nmae, 2),
            "underforecast_hours": uf_hours,
            "underforecast_pct": round(uf_hours / n_paired * 100, 1),
            "overforecast_hours": of_hours,
            "overforecast_pct": round(of_hours / n_paired * 100, 1),
            "cumulative_underforecast_mwh": round(cum_uf, 1),
            "cumulative_overforecast_mwh": round(cum_of, 1),
            "maximum_underforecast_mw": round(max_uf_mw, 1) if max_uf_mw else None,
            "maximum_underforecast_time_local": str(max_uf_time),
            "maximum_overforecast_mw": round(max_of_mw, 1) if max_of_mw else None,
            "maximum_overforecast_time_local": str(max_of_time),
            "longest_underforecast_run_hours": max(uf_runs) if uf_runs else 0,
            "longest_overforecast_run_hours": max(of_runs) if of_runs else 0,
            "actual_event_peak_mw": round(peak_mw, 1),
            "actual_event_peak_time_local": str(peak_time),
            "actual_peak_paired": peak_paired,
            "pjm_forecast_at_actual_peak_mw": round(pjm_at_peak, 1) if pjm_at_peak else None,
            "signed_error_at_actual_peak_mw": round(err_at_peak, 1) if err_at_peak else None,
            "absolute_error_at_actual_peak_mw": round(abs_at_peak, 1) if abs_at_peak else None,
            "underforecast_at_actual_peak_mw": round(uf_at_peak, 1) if uf_at_peak else None,
            "absolute_percentage_error_at_actual_peak": round(ape_at_peak, 2) if ape_at_peak else None,
        })

    df = pd.DataFrame(summaries)
    df.to_csv(output_path, index=False)
    print(f"Event metrics: {len(df)} events → {output_path}")
    for _, r in df.iterrows():
        print(f"  {r['event_id']}: MAE={r['mae_mw']} RMSE={r['rmse_mw']} peak={r['actual_event_peak_mw']} paired={r['actual_peak_paired']}")
    return df


def plot_events(hourly, output_dir):
    fig_dir = Path(output_dir) / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    import pytz
    eastern = pytz.timezone("America/New_York")

    for eid, cfg in EVENTS.items():
        eh = hourly[hourly["event_id"] == eid].copy()
        eh["local_dt"] = pd.to_datetime(eh["target_time_local"])
        eh = eh.sort_values("local_dt")

        fig, ax = plt.subplots(figsize=(12, 5))

        # Actual load
        ax.plot(eh["local_dt"], eh["actual_load_mw"], "k-", linewidth=1.5, label="Actual Load")
        # PJM forecast (paired only)
        paired_mask = eh["paired"].values
        if paired_mask.any():
            ax.plot(eh.loc[paired_mask, "local_dt"], eh.loc[paired_mask, "pjm_forecast_mw"],
                    "r--", linewidth=1.2, alpha=0.8, label=f"PJM Forecast ({paired_mask.sum()}h paired)")

        # Mark actual peak
        all_a = eh["actual_load_mw"].values
        peak_idx = np.nanargmax(all_a)
        if not np.isnan(eh.iloc[peak_idx]["actual_load_mw"]):
            ax.scatter(eh.iloc[peak_idx]["local_dt"], all_a[peak_idx],
                      color="red", s=80, zorder=5, marker="*",
                      label=f"Event Peak ({all_a[peak_idx]:.0f} MW)")

        title = f"{cfg['label']}"
        if eid == "E2014_PV1":
            title += " — 63/72 paired hours"
        elif eid == "E2015_COLD_anchor":
            title += " — February 20 anchor day"

        ax.set_title(title)
        ax.set_ylabel("Load (MW)")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d\n%H:%M", tz=eastern))
        ax.legend(loc="upper left", fontsize=8)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        for ext in ["pdf", "png"]:
            dpi = 300 if ext == "png" else None
            fig.savefig(fig_dir / f"{eid}_actual_vs_pjm.{ext}", dpi=dpi, bbox_inches="tight")
        plt.close(fig)

    # Cross-event error comparison
    metrics_df = pd.read_csv(f"{output_dir}/pjm_event_summary.csv")
    complete_events = metrics_df[metrics_df["event_id"].isin(["E2018_SNAP", "E2022_ELLIOTT"])]

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    metrics = ["mae_mw", "rmse_mw", "mean_error_mw"]
    titles = ["MAE (MW)", "RMSE (MW)", "Mean Error (MW)"]
    for ax, met, ttl in zip(axes, metrics, titles):
        vals = complete_events[met].values
        labels = complete_events["event_label"].values
        ax.bar(labels, vals, color=["#1f77b4", "#ff7f0e"])
        ax.set_title(ttl)
        ax.tick_params(axis="x", rotation=15)
        ax.grid(True, alpha=0.3)
    fig.suptitle("PJM Forecast Error — Complete Events", fontweight="bold")
    fig.tight_layout()
    for ext in ["pdf", "png"]:
        dpi = 300 if ext == "png" else None
        fig.savefig(fig_dir / f"pjm_event_error_comparison.{ext}", dpi=dpi, bbox_inches="tight")
    plt.close(fig)

    print(f"Figures saved to {fig_dir}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--panel", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    panel = load_panel(args.panel)

    # Hourly errors
    hourly = compute_hourly_errors(panel, f"{args.output_dir}/pjm_event_hourly_errors.csv")

    # Event metrics
    metrics = compute_event_metrics(hourly, f"{args.output_dir}/pjm_event_summary.csv")

    # Figures
    plot_events(hourly, args.output_dir)

    print("\nC07E benchmark complete.")


if __name__ == "__main__":
    main()
