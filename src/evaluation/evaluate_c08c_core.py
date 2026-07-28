"""C08C-EVAL: Evaluate 4 probabilistic methods."""
import numpy as np, pandas as pd
from pathlib import Path

PRED = "artifacts/C08C/probabilistic_predictions.csv"
OUT = "artifacts/C08C/evaluation"
Path(OUT).mkdir(parents=True, exist_ok=True)

r = pd.read_csv(PRED, low_memory=False)
r["od"] = pd.to_datetime(r["operating_date"])
r["year"] = r["od"].dt.year

print(f"Rows: {len(r)}, unique target: {r['target_time_utc'].nunique()}")

# Methods and their quantile columns
METHODS = {
    "EMP_RESID_HOUR": [f"EMP_RESID_HOUR_q{q:02d}" for q in [1,5,10,25,50,75,90,95,99]],
    "QHGBR_RAW": [f"QHGBR_RAW_q{q:02d}" for q in [1,5,10,25,50,75,90,95,99]],
    "QHGBR_REARRANGED": [f"QHGBR_REARRANGED_q{q:02d}" for q in [1,5,10,25,50,75,90,95,99]],
}
QLIST = [0.01,0.05,0.10,0.25,0.50,0.75,0.90,0.95,0.99]
EVENTS = {"E2014_PV1":("2014-01-06","2014-01-08"),"E2018_SNAP":("2017-12-28","2018-01-07"),"E2022_ELLIOTT":("2022-12-23","2022-12-26")}
FOLDS = sorted(r["fold_id"].unique())

# 1. Fold-event counts
fec = []
for fid in FOLDS:
    m = r["fold_id"] == fid
    fec.append({"fold_id":fid, "rows":int(m.sum())})
pd.DataFrame(fec).to_csv(f"{OUT}/fold_event_counts.csv", index=False)

# 2. Input integrity
integrity = pd.DataFrame([{
    "check":"total_rows","expected":78888,"actual":len(r),"pass":len(r)==78888
},{
    "check":"unique_target","expected":True,"actual":r["target_time_utc"].is_unique,"pass":r["target_time_utc"].is_unique
},{
    "check":"actual_load_not_null","expected":78888,"actual":int(r["actual_load_mw"].notna().sum()),"pass":r["actual_load_mw"].notna().sum()==78888
}])
integrity.to_csv(f"{OUT}/input_integrity.csv", index=False)

# 3. Main metrics
actual = r["actual_load_mw"].values
all_metrics = []
for mb, cols in METHODS.items():
    if not all(c in r.columns for c in cols):
        print(f"  {mb}: missing columns"); continue
    
    # Get quantile matrix, sort to enforce monotonicity
    qv = np.sort(np.column_stack([r[c].values for c in cols]), axis=1)
    
    # Pinball loss per quantile
    pinball = []
    for i, q in enumerate(QLIST):
        err = actual - qv[:, i]
        pinball.append(np.mean(np.maximum(q * err, (q - 1) * err)))
    
    # Quantile CRPS approximation (trapezoid)
    dq = np.diff(QLIST)
    crps = np.sum(dq * np.array(pinball[:-1]))
    
    # WIS for intervals
    wis = 0
    for i_alpha, (lo, hi) in enumerate([(3,5),(1,7),(0,8)]):
        alpha = 2 * QLIST[lo]  # e.g., q25 produces 50% interval, alpha=0.5
        w = alpha / 2
        lw = qv[:, lo]
        up = qv[:, hi]
        wis_interval = (up - lw) + (2/w) * np.maximum(lw - actual, 0) + (2/w) * np.maximum(actual - up, 0)
        wis += w * wis_interval / (i_alpha + 2)
    
    # Coverage
    c50 = ((actual >= qv[:, 3]) & (actual <= qv[:, 5])).mean()
    c90 = ((actual >= qv[:, 1]) & (actual <= qv[:, 7])).mean()
    c98 = ((actual >= qv[:, 0]) & (actual <= qv[:, 8])).mean()
    
    # Width
    w50 = np.mean(qv[:, 5] - qv[:, 3])
    w90 = np.mean(qv[:, 7] - qv[:, 1])
    w98 = np.mean(qv[:, 8] - qv[:, 0])
    
    # Crossing
    cross_rows = 0
    cross_pairs = 0
    for i in range(len(qv)):
        for j in range(len(QLIST)-1):
            if qv[i, j] > qv[i, j+1]:
                cross_rows += 1
                cross_pairs += 1
    
    all_metrics.append({
        "method": mb, "mean_pinball": np.mean(pinball), "quantile_crps": crps,
        "wis": np.mean(wis), "c50": c50*100, "c90": c90*100, "c98": c98*100,
        "w50_mw": w50, "w90_mw": w90, "w98_mw": w98,
        "crossing_rows": cross_rows, "crossing_pairs": cross_pairs,
        "crossing_rate_pct": cross_rows / len(r) * 100,
        "median_mae": np.median(np.abs(actual - qv[:, 4]))
    })
    
pd.DataFrame(all_metrics).to_csv(f"{OUT}/pooled_probabilistic_metrics.csv", index=False)

# 4. Event metrics
event_metrics = []
for eid, (s, e) in EVENTS.items():
    m = (r["od"] >= s) & (r["od"] <= e)
    e_actual = r.loc[m, "actual_load_mw"].values
    print(f"\n{eid}: {e_actual.shape[0]} hours")
    
    for mb, cols in METHODS.items():
        if not all(c in r.columns for c in cols): continue
        qv = np.sort(np.column_stack([r.loc[m, c].values for c in cols]), axis=1)
        
        err = e_actual - qv[:, 4]
        mae = np.mean(np.abs(err))
        c90 = ((e_actual >= qv[:, 1]) & (e_actual <= qv[:, 7])).mean()
        c98 = ((e_actual >= qv[:, 0]) & (e_actual <= qv[:, 8])).mean()
        w90 = np.mean(qv[:, 7] - qv[:, 1])
        
        # Upper-bound exceedance
        ub = qv[:, 7]  # 90% upper bound
        exceed = e_actual - ub
        ex_hours = int(np.sum(exceed > 0))
        ex_mw = float(np.max(exceed[exceed > 0])) if ex_hours > 0 else 0
        ex_sum = float(np.sum(exceed[exceed > 0])) if ex_hours > 0 else 0
        
        # Peak
        peak_idx = np.argmax(e_actual)
        peak_val = e_actual[peak_idx]
        
        event_metrics.append({
            "event_id": eid, "method": mb, "hours": len(e_actual),
            "mae_mw": mae, "c90_pct": c90*100, "c98_pct": c98*100,
            "w90_mw": w90,
            "upper_exceed_hours": ex_hours, "max_upper_exceed_mw": ex_mw,
            "cum_upper_exceed_mwh": ex_sum,
            "actual_peak_mw": peak_val
        })
        
        print(f"  {mb}: MAE={mae:.0f}, 90%={c90*100:.0f}%, UB_ex={ex_hours}h")

pd.DataFrame(event_metrics).to_csv(f"{OUT}/event_probabilistic_metrics.csv", index=False)

print("\n--- Annual metrics ---")
# 5. Annual coverage
annual = []
for fy in sorted(r["year"].unique()):
    m = r["year"] == fy
    ay = r.loc[m]
    for mb, cols in METHODS.items():
        if not all(c in r.columns for c in cols): continue
        qv = np.sort(np.column_stack([ay[c].values for c in cols]), axis=1)
        c90 = ((ay["actual_load_mw"].values >= qv[:, 1]) & (ay["actual_load_mw"].values <= qv[:, 7])).mean()
        annual.append({"fold_id": f"Y{fy}", "method": mb, "c90_pct": c90*100})
pd.DataFrame(annual).to_csv(f"{OUT}/annual_coverage.csv", index=False)

print("\nDone. Files in", OUT)
