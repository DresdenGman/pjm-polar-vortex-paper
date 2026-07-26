#!/usr/bin/env python3
"""preprocess_pjm_load.py — Clean and validate PJM hourly actual load CSV.
   Reads data/raw/pjm/pjm_hourly_actual_load_2010_2014_raw.csv
   Writes data/interim/pjm_hourly_actual_load_2010_2014_clean.csv
   Usage: python3 preprocess_pjm_load.py
"""
import csv, sys, os
from datetime import datetime
from collections import Counter

RAW_PATH = "data/raw/pjm/pjm_hourly_actual_load_2010_2014_raw.csv"
CLEAN_PATH = "data/interim/pjm_hourly_actual_load_2010_2014_clean.csv"
REPORT_PATH = "data/validation/pjm_load_validation.txt"

def main():
    if not os.path.exists(RAW_PATH):
        print(f"BLOCKED: {RAW_PATH} not found. Waiting for PJM account approval.")
        print("Place downloaded PJM CSV at this path and re-run.")
        sys.exit(1)
    
    issues = []
    clean_rows = []
    timestamps_seen = set()
    
    with open(RAW_PATH, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            try:
                # Detect column names (PJM uses various headers)
                ts_col = next(c for c in ['timestamp_ept', 'datetime_beginning_ept', 
                                           'datetime_ept', 'datetime', 'date'] if c in row)
                load_col = next(c for c in ['actual_load_mw', 'mw', 'total_load_mw', 'load'] if c in row)
                
                ts_str = row[ts_col].strip()
                load_val = float(row[load_col].replace(',', ''))
                
                # Parse timestamp
                for fmt in ['%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M', '%Y-%m-%dT%H:%M:%S']:
                    try:
                        dt = datetime.strptime(ts_str, fmt)
                        break
                    except:
                        continue
                else:
                    issues.append(f"Row {i}: cannot parse timestamp '{ts_str}'")
                    continue
                
                # Validate
                if load_val <= 0:
                    issues.append(f"{dt}: load={load_val} MW (non-positive)")
                if load_val > 200000:
                    issues.append(f"{dt}: load={load_val} MW (implausible)")
                
                ts_key = dt.strftime('%Y-%m-%d %H:%M')
                if ts_key in timestamps_seen:
                    issues.append(f"{dt}: duplicate timestamp")
                timestamps_seen.add(ts_key)
                
                clean_rows.append({
                    'timestamp_ept': dt.strftime('%Y-%m-%d %H:%M:%S'),
                    'actual_load_mw': str(load_val),
                })
            except Exception as e:
                issues.append(f"Row {i}: {e}")
    
    # Check gaps
    if clean_rows:
        dts = sorted([datetime.strptime(r['timestamp_ept'], '%Y-%m-%d %H:%M:%S') for r in clean_rows])
        for i in range(1, len(dts)):
            gap = (dts[i] - dts[i-1]).total_seconds() / 3600
            if gap > 1.1:
                issues.append(f"Gap: {dts[i-1]} → {dts[i]} ({gap:.1f}h)")
    
    # Peak analysis
    jan15 = [r for r in clean_rows if r['timestamp_ept'].startswith('2014-01-') and 
             int(r['timestamp_ept'][8:10]) <= 15]
    jan68 = [r for r in jan15 if 6 <= int(r['timestamp_ept'][8:10]) <= 8]
    
    if jan15:
        max_row = max(jan15, key=lambda r: float(r['actual_load_mw']))
        print(f"Jan 1-15 peak: {max_row['actual_load_mw']} MW at {max_row['timestamp_ept']}")
    
    if jan68:
        max68 = max(jan68, key=lambda r: float(r['actual_load_mw']))
        print(f"Jan 6-8 peak:  {max68['actual_load_mw']} MW at {max68['timestamp_ept']}")
    
    # Check for 143,531
    target = 140510  # Official PJM Jan 7 18:00 peak
    found = [r for r in clean_rows if abs(float(r['actual_load_mw']) - target) < 1]
    print(f"143,531 MW: {'FOUND' if found else 'NOT FOUND'}")
    if found:
        print(f"  at {found[0]['timestamp_ept']}")
    
    # Write clean file
    os.makedirs(os.path.dirname(CLEAN_PATH), exist_ok=True)
    with open(CLEAN_PATH, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp_ept', 'actual_load_mw'])
        writer.writeheader()
        writer.writerows(clean_rows)
    
    # Write report
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, 'w') as f:
        f.write(f"PJM Load Validation Report\n{'='*40}\n")
        f.write(f"Total rows: {len(clean_rows)}\n")
        f.write(f"Unique timestamps: {len(timestamps_seen)}\n")
        f.write(f"Issues: {len(issues)}\n")
        for iss in issues[:50]:
            f.write(f"  - {iss}\n")
    
    print(f"\n✓ Clean: {CLEAN_PATH} ({len(clean_rows)} rows)")
    print(f"✓ Report: {REPORT_PATH} ({len(issues)} issues)")
    if not issues:
        print("✓ DATA VALID — no issues found")

if __name__ == '__main__':
    main()
