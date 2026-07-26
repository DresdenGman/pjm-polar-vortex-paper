#!/usr/bin/env python3
"""preprocess_pjm_forecast.py — Clean PJM day-ahead forecast CSV.
   Reads data/raw/pjm/pjm_day_ahead_forecast_2014_raw.csv
   Writes data/interim/pjm_day_ahead_forecast_2014_clean.csv
   Note: Run only after PJM data obtained. Currently blocks on missing raw file.
"""
import csv, os, sys
from datetime import datetime

RAW_PATH = "data/raw/pjm/pjm_day_ahead_forecast_2014_raw.csv"
CLEAN_PATH = "data/interim/pjm_day_ahead_forecast_2014_clean.csv"

def main():
    if not os.path.exists(RAW_PATH):
        print("BLOCKED: PJM day-ahead forecast data not obtained.")
        print(f"Expected: {RAW_PATH}")
        sys.exit(1)
    
    clean_rows = []
    with open(RAW_PATH, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                ts_col = next(c for c in ['timestamp_ept', 'datetime_ept', 'date'] if c in row)
                fc_col = next(c for c in ['day_ahead_forecast_mw', 'forecast_mw', 'mw'] if c in row)
                
                ts_str = row[ts_col].strip()
                fc_val = float(row[fc_col].replace(',', ''))
                
                for fmt in ['%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M']:
                    try:
                        dt = datetime.strptime(ts_str, fmt)
                        break
                    except:
                        continue
                
                clean_rows.append({
                    'timestamp_ept': dt.strftime('%Y-%m-%d %H:%M:%S'),
                    'day_ahead_forecast_mw': str(fc_val),
                })
            except:
                pass
    
    os.makedirs(os.path.dirname(CLEAN_PATH), exist_ok=True)
    with open(CLEAN_PATH, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp_ept', 'day_ahead_forecast_mw'])
        writer.writeheader()
        writer.writerows(clean_rows)
    
    print(f"✓ {CLEAN_PATH}: {len(clean_rows)} rows")

if __name__ == '__main__':
    main()
