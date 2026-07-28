"""C08C-R: Rebuild prediction metadata by target_time_utc merge."""
import hashlib, numpy as np, pandas as pd
from pathlib import Path

PANEL = "data/processed/C08A/day_ahead_load_calendar_2010_2022.csv"
FOLDS = "data/processed/C08A/day_ahead_fold_membership.csv"
PREDICTIONS = "artifacts/C08C/probabilistic_predictions_2014_2022.csv"
OUTPUT = "artifacts/C08C/probabilistic_predictions.csv"

panel = pd.read_csv(PANEL, low_memory=False)
panel["target_time_utc"] = pd.to_datetime(panel["target_time_utc"], utc=True)

folds = pd.read_csv(FOLDS, low_memory=False)
folds["target_time_utc"] = pd.to_datetime(folds["target_time_utc"], utc=True)

preds = pd.read_csv(PREDICTIONS)
pred_cols = list(preds.columns)

print(f"Panel: {len(panel)}, Folds: {len(folds)}, Preds: {len(preds)}")

# Get all test rows with their fold_id
test_mask = folds["membership"] == "TEST"
test_meta = folds[test_mask][["target_time_utc", "fold_id"]].copy()
test_meta = test_meta.sort_values(["fold_id", "target_time_utc"]).reset_index(drop=True)
print(f"Test meta: {len(test_meta)} rows")

assert len(test_meta) == 78888, f"Expected 78888, got {len(test_meta)}"

# Merge with panel to get all metadata
test_full = test_meta.merge(panel, on="target_time_utc", how="left")
print(f"After merge: {len(test_full)} rows")
assert test_full["actual_load_mw"].notna().sum() > 70000, "Too many null actual_load_mw"

# Add predictions (same row order — both sorted by fold_id + target_time_utc)
test_full = pd.concat([test_full.reset_index(drop=True), preds.reset_index(drop=True)], axis=1)
print(f"Final: {len(test_full)} rows, {len(test_full.columns)} cols")

# Verify
assert "target_time_utc" in test_full.columns
assert "actual_load_mw" in test_full.columns
assert "operating_date" in test_full.columns

print(f"Fold counts:")
for y in list(range(2014,2023)):
    fid = f"Y{y}"
    cnt = (test_full["fold_id"] == fid).sum()
    print(f"  {fid}: {cnt}")

# Event counts
od = pd.to_datetime(test_full["operating_date"])
e2014 = ((od >= "2014-01-06") & (od <= "2014-01-08")).sum()
e2018 = ((od >= "2017-12-28") & (od <= "2018-01-07")).sum()
e2022 = ((od >= "2022-12-23") & (od <= "2022-12-26")).sum()
print(f"E2014: {e2014}h (expect 72)")
print(f"E2018: {e2018}h (expect 264)")
print(f"E2022: {e2022}h (expect 96)")

# Verify predictions unchanged
orig_hash = hashlib.sha256(preds.values.astype(str).tobytes()).hexdigest()
new_preds = test_full[pred_cols]
new_hash = hashlib.sha256(new_preds.values.astype(str).tobytes()).hexdigest()
print(f"Prediction hash match: {orig_hash == new_hash}")

# Save
test_full.to_csv(OUTPUT, index=False)
print(f"Saved to {OUTPUT}")
print("Done.")
