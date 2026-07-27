"""C08B-R1: Hardened point forecast pipeline with fold-level checkpointing."""
import argparse, gc, json, os, time, warnings, numpy as np, pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor, ExtraTreesRegressor
from sklearn.model_selection import ParameterGrid

warnings.filterwarnings("ignore")
RANDOM_SEED = 42
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

CALENDAR_FEATURES = [
    "calendar_hour", "day_of_week", "month", "weekend_indicator",
    "holiday_indicator", "dst_indicator", "expected_hours_for_operating_date",
    "forecast_horizon_hours",
]
LOAD_FEATURES = [
    "load_origin_minus_1h", "load_same_hour_1d", "load_same_hour_2d",
    "load_same_hour_7d", "load_same_hour_14d",
    "previous_available_daily_peak", "previous_available_daily_mean",
]
AVAIL_FEATURES = [f"{f}_available" for f in LOAD_FEATURES]
ALL_FEATURES = CALENDAR_FEATURES + LOAD_FEATURES + AVAIL_FEATURES
FOLDS = ["Y2014", "Y2015", "Y2016", "Y2017", "Y2018", "Y2019", "Y2020", "Y2021", "Y2022"]


def load_data(panel_path, folds_path):
    p = pd.read_csv(panel_path, low_memory=False)
    f = pd.read_csv(folds_path, low_memory=False)
    p["target_utc"] = pd.to_datetime(p["target_time_utc"], utc=True)
    return p, f


def prepare_fold(p, f, fold_id):
    fm = f[f["fold_id"] == fold_id]
    p2 = p.copy()
    p2["membership"] = fm["membership"].values
    p2["same_event_blackout"] = fm["same_event_blackout"].values
    train = p2[p2["membership"] == "TRAIN"].copy()
    val_full = p2[p2["membership"] == "VALIDATION"].copy()
    val = val_full[~val_full["same_event_blackout"]].copy()
    test = p2[p2["membership"] == "TEST"].copy()
    refit = pd.concat([train, val], ignore_index=True)
    return train, val, test, refit


def featurize(df):
    X = df[ALL_FEATURES].copy().astype(float)
    y = df["actual_load_mw"].values.astype(float)
    return X, y


def train_naive_7d(train, val, test):
    return test["load_same_hour_7d"].values, {}

def train_naive_latest(train, val, test):
    preds = test["load_same_hour_1d"].fillna(test["load_same_hour_2d"].fillna(
        test["load_same_hour_7d"].fillna(test["load_same_hour_14d"]))).values
    return preds, {}

def train_ridge(train, val, test):
    X_tr, y_tr = featurize(train); X_va, y_va = featurize(val); X_te, _ = featurize(test)
    imp = SimpleImputer(strategy="median")
    X_tr_i = imp.fit_transform(X_tr); X_va_i = imp.transform(X_va); X_te_i = imp.transform(X_te)
    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_tr_i); X_va_s = scaler.transform(X_va_i); X_te_s = scaler.transform(X_te_i)
    best_mae, best_alpha = float("inf"), None
    best_model = None
    for alpha in [0.1, 1.0, 10.0, 100.0, 1000.0]:
        m = Ridge(alpha=alpha, random_state=RANDOM_SEED); m.fit(X_tr_s, y_tr)
        mae = np.mean(np.abs(m.predict(X_va_s) - y_va))
        if mae < best_mae: best_mae, best_alpha, best_model = mae, alpha, m
    X_rf, y_rf = featurize(pd.concat([train, val]))
    X_rf_i = imp.fit_transform(X_rf); X_rf_s = scaler.fit_transform(X_rf_i)
    best_model.fit(X_rf_s, y_rf)
    preds = best_model.predict(X_te_s)
    gc.collect(); return preds, {"alpha": best_alpha, "val_mae": best_mae}

def train_hist_gbr(train, val, test):
    X_tr, y_tr = featurize(train); X_va, y_va = featurize(val); X_te, _ = featurize(test)
    med = X_tr.median(); X_tr = X_tr.fillna(med); X_va = X_va.fillna(med); X_te = X_te.fillna(med)
    best_mae, best_params = float("inf"), None
    best_model = None
    grid = list(ParameterGrid({
        "learning_rate": [0.03, 0.05, 0.10], "max_iter": [200, 400],
        "max_leaf_nodes": [15, 31], "min_samples_leaf": [20, 50],
        "l2_regularization": [0.0, 1.0, 10.0],
    }))
    for params in grid:
        m = HistGradientBoostingRegressor(loss="squared_error", early_stopping=False, random_state=RANDOM_SEED, **params)
        m.fit(X_tr, y_tr)
        mae = np.mean(np.abs(m.predict(X_va) - y_va))
        if mae < best_mae: best_mae, best_params, best_model = mae, params, m
    X_rf, y_rf = featurize(pd.concat([train, val]))
    X_rf = X_rf.fillna(X_rf.median()); best_model.fit(X_rf, y_rf)
    preds = best_model.predict(X_te)
    gc.collect(); return preds, {"params": best_params, "val_mae": best_mae}

def train_extra_trees(train, val, test):
    X_tr, y_tr = featurize(train); X_va, y_va = featurize(val); X_te, _ = featurize(test)
    med = X_tr.median(); X_tr = X_tr.fillna(med); X_va = X_va.fillna(med); X_te = X_te.fillna(med)
    best_mae, best_params = float("inf"), None
    best_model = None
    grid = list(ParameterGrid({
        "max_depth": [12, 20, None], "min_samples_leaf": [1, 5, 20], "max_features": [0.7, 1.0],
    }))
    for params in grid:
        m = ExtraTreesRegressor(n_estimators=300, n_jobs=1, bootstrap=False, random_state=RANDOM_SEED, **params)
        m.fit(X_tr, y_tr)
        mae = np.mean(np.abs(m.predict(X_va) - y_va))
        if mae < best_mae: best_mae, best_params, best_model = mae, params, m
    X_rf, y_rf = featurize(pd.concat([train, val]))
    X_rf = X_rf.fillna(X_rf.median()); best_model.fit(X_rf, y_rf)
    preds = best_model.predict(X_te)
    gc.collect(); return preds, {"params": best_params, "val_mae": best_mae}

MODELS = {
    "naive_7d": train_naive_7d, "naive_latest": train_naive_latest,
    "ridge": train_ridge, "hist_gbr": train_hist_gbr, "extra_trees": train_extra_trees,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--panel", required=True); parser.add_argument("--folds", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    Path(args.output).mkdir(parents=True, exist_ok=True)
    ckpt = Path(args.output) / "checkpoints"; ckpt.mkdir(exist_ok=True)
    p, f = load_data(args.panel, args.folds)
    all_preds, all_params = [], []

    for fold_id in FOLDS:
        dfile = ckpt / f"{fold_id}_DONE.json"
        pfile = ckpt / f"{fold_id}_predictions.csv"
        afile = ckpt / f"{fold_id}_params.csv"

        if dfile.exists():
            try:
                with open(dfile) as fd: chk = json.load(fd)
                assert chk.get("status") == "COMPLETE"
                all_preds.append(pd.read_csv(pfile))
                all_params.extend(pd.read_csv(afile).to_dict("records"))
                print(f"\n=== {fold_id} (cached) === skipped")
                continue
            except Exception:
                dfile.unlink(missing_ok=True)

        print(f"\n=== {fold_id} ===")
        t0 = time.time()
        train, val, test, _ = prepare_fold(p, f, fold_id)
        print(f"  Train: {len(train)}  Val: {len(val)}  Test: {len(test)}")

        fp = pd.DataFrame({"target_time_utc": test["target_time_utc"],
            "target_time_local": test["target_time_local"], "operating_date": test["operating_date"],
            "fold_id": fold_id, "actual_load_mw": test["actual_load_mw"],
            "actual_load_available": test["actual_load_available"].astype(bool)})

        for mn, trn in MODELS.items():
            col = f"{mn}_prediction_mw"
            preds, params = trn(train, val, test)
            fp[col] = preds; params["fold_id"] = fold_id; params["model"] = mn
            all_params.append(params)
            print(f"  {mn}: MAE={np.mean(np.abs(preds - test['actual_load_mw'])):.1f}")
            gc.collect()

        all_preds.append(fp)
        fp.to_csv(pfile, index=False)
        pd.DataFrame([p for p in all_params if p.get("fold_id") == fold_id]).to_csv(afile, index=False)
        with open(dfile, "w") as fd:
            json.dump({"status": "COMPLETE", "fold_id": fold_id, "rows": len(fp),
                        "elapsed_s": round(time.time()-t0, 1)}, fd)
        print(f"  Checkpoint ({time.time()-t0:.0f}s)")

    result = pd.concat(all_preds, ignore_index=True).sort_values("target_time_utc")
    result.to_csv(f"{args.output}/point_predictions_2014_2022.csv", index=False)
    pd.DataFrame(all_params).to_csv(f"{args.output}/selected_hyperparameters_by_fold.csv", index=False)
    print(f"\nDone: {len(result)} rows")


if __name__ == "__main__":
    main()
