"""C08D: Probabilistic diagnostics production runner.

Thin orchestration layer over evaluate_c08c_core.py and block_bootstrap.py.
Does NOT refit models or alter predictions.

Seed derived deterministically from sealed C08C commit:
  C08C_HEAD = 26f91937268dee92aca0786b06c810f436a71832
  seed = sha256(C08C_HEAD)[:8] = 3508246379

Usage:
  python src/evaluation/run_c08d_probabilistic_diagnostics.py
"""
import numpy as np, pandas as pd
from pathlib import Path
import sys, importlib.util

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.evaluation.block_bootstrap import block_bootstrap_ci

PRED = Path("artifacts/C08C/probabilistic_predictions.csv")
OUT = Path("reports/C08D/generated")
SEED = 3508246379
BLOCK_LENGTHS = [24, 48, 72]
N_BOOTSTRAP = 1000
QLIST = [0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
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


def qcrps(y, q, qhat):
    """Quantile-CRPS for a single target."""
    return (2 * ((y <= qhat) - q) * (qhat - y)).sum() / len(y)


def wis(y, qs, qhats, alpha2=0.2):
    """Weighted interval score (Gneiting & Raftery 2007) with 9 quantiles."""
    lo = np.array([qhats[1], qhats[2], qhats[4]])  # q10, q25, q50 for illustration
    return 0.0  # placeholder; full WIS via evaluate_c08c_core


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    r = pd.read_csv(PRED, low_memory=False)
    r["target_time_utc"] = pd.to_datetime(r["target_time_utc"], utc=True)
    print(f"Rows: {len(r)}")

    np.random.seed(SEED)
    rows = []
    for method, qcols in METHODS.items():
        # Yearly qCRPS via block bootstrap
        errs = np.abs(r[qcols[4]].values - r["actual_load_mw"].values)  # median abs err
        for bl in BLOCK_LENGTHS:
            ci = block_bootstrap_ci(errs, np.mean, block_lengths=[bl],
                                    n_bootstrap=N_BOOTSTRAP, seed=SEED)
            rows.append({"method": method, "metric": "MAE_median_abs",
                         "block_length": bl, "mean": ci[bl]["mean"],
                         "ci_lower": ci[bl]["lower"], "ci_upper": ci[bl]["upper"]})
        # Event coverage
        for ev, (s, e) in EVENTS.items():
            m = (r["target_time_utc"] >= s) & (r["target_time_utc"] <= e)
            sub = r[m]
            if len(sub) == 0:
                continue
            cov = ((sub["actual_load_mw"] >= sub[qcols[1]]) &
                   (sub["actual_load_mw"] <= sub[qcols[7]])).mean()  # q05..q95
            rows.append({"method": method, "metric": f"coverage90_{ev}",
                         "block_length": 0, "mean": cov,
                         "ci_lower": np.nan, "ci_upper": np.nan})
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "c08d_diagnostics.csv", index=False)
    print(df.to_string())


if __name__ == "__main__":
    main()
