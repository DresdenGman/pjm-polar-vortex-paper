"""C08D: Reconciliation audit — direct point-estimate comparison vs sealed C08C.

Computes coverage directly from sealed prediction rows, independently of
bootstrap summaries. Compares annual + event coverage per method.
"""
import numpy as np, pandas as pd
from pathlib import Path

PRED = Path("artifacts/C08C/probabilistic_predictions.csv")
OUT = Path("reports/C08D/generated")
OUT.mkdir(parents=True, exist_ok=True)

METHODS = {
    "EMP_RESID_HOUR": [f"EMP_RESID_HOUR_q{q:02d}" for q in [1, 5, 10, 25, 50, 75, 90, 95, 99]],
    "QHGBR_RAW": [f"QHGBR_RAW_q{q:02d}" for q in [1, 5, 10, 25, 50, 75, 90, 95, 99]],
    "QHGBR_REARRANGED": [f"QHGBR_REARRANGED_q{q:02d}" for q in [1, 5, 10, 25, 50, 75, 90, 95, 99]],
}
EVENTS = {
    "E2014_PV1": ("2014-01-06", "2014-01-08"),
    "E2018_SNAP": ("2017-12-28", "2018-01-07"),
    "E2022_ELLIOTT": ("2022-12-23", "2022-12-26"),
}


def coverage(sub, qlo_col, qhi_col):
    """90% interval coverage: q05 <= observed <= q95."""
    if len(sub) == 0:
        return np.nan, 0
    covered = ((sub["actual_load_mw"] >= sub[qlo_col]) &
               (sub["actual_load_mw"] <= sub[qhi_col])).sum()
    return covered / len(sub), len(sub)


def main():
    r = pd.read_csv(PRED, low_memory=False)
    r["target_time_utc"] = pd.to_datetime(r["target_time_utc"], utc=True)
    r["od"] = pd.to_datetime(r["operating_date"])
    r["year"] = r["od"].dt.year
    print(f"Rows: {len(r)}, years: {sorted(r['year'].unique())}")

    rows = []
    for method, qcols in METHODS.items():
        qlo, qhi = qcols[1], qcols[7]  # q05, q95

        # Annual (all years pooled)
        cov, n = coverage(r, qlo, qhi)
        rows.append({"method": method, "scope": "annual", "coverage": cov, "n": n})

        # Event scopes (filter on operating_date, matching sealed C08C)
        for ev, (s, e) in EVENTS.items():
            m = (r["od"] >= s) & (r["od"] <= e)
            sub = r[m]
            cov, n = coverage(sub, qlo, qhi)
            rows.append({"method": method, "scope": ev, "coverage": cov, "n": n})

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "c08c_c08d_point_estimate_comparison.csv", index=False)
    print(df.to_string())

    # Event population comparison (operating_date filter, matching C08C)
    pop = []
    for ev, (s, e) in EVENTS.items():
        m = (r["od"] >= s) & (r["od"] <= e)
        pop.append({"event": ev, "window": f"{s}..{e}", "rows": int(m.sum())})
    pd.DataFrame(pop).to_csv(OUT / "event_population_comparison.csv", index=False)
    print("\nEvent populations:")
    print(pd.DataFrame(pop).to_string())


if __name__ == "__main__":
    main()
