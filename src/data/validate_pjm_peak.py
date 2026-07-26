#!/usr/bin/env python3
"""validate_pjm_peak.py — Peak consistency checker for PJM Polar Vortex.
   Usage: python3 validate_pjm_peak.py
   Reads data/interim/pjm_hourly_actual_load_2010_2014_clean.csv
   Reports: Jan 1-15 peak, Jan 6-8 peak, 143,531 MW status
"""
import csv, os, sys
from datetime import datetime

CLEAN_PATH = "data/interim/pjm_hourly_actual_load_2010_2014_clean.csv"
MANUSCRIPT_TARGET = 140510  # MW (official PJM Jan 7 18:00 peak)

def main():
    if not os.path.exists(CLEAN_PATH):
        print("BLOCKED: PJM clean data not available.")
        print("Run preprocess_pjm_load.py first after obtaining raw PJM data.")
        sys.exit(1)
    
    rows = []
    with open(CLEAN_PATH) as f:
        for r in csv.DictReader(f):
            rows.append({
                'dt': datetime.strptime(r['timestamp_ept'], '%Y-%m-%d %H:%M:%S'),
                'mw': float(r['actual_load_mw'])
            })
    
    jan15 = [r for r in rows if r['dt'].year == 2014 and r['dt'].month == 1 and r['dt'].day <= 15]
    jan68 = [r for r in jan15 if 6 <= r['dt'].day <= 8]
    
    print("=" * 60)
    print("PJM PEAK VERIFICATION")
    print("=" * 60)
    
    if jan15:
        peak = max(jan15, key=lambda r: r['mw'])
        print(f"\nJan 1-15, 2014 MAXIMUM:")
        print(f"  {peak['mw']:,.0f} MW at {peak['dt']}")
        
        # Top 5
        top5 = sorted(jan15, key=lambda r: r['mw'], reverse=True)[:5]
        print(f"\nTop 5 loads Jan 1-15:")
        for i, r in enumerate(top5):
            print(f"  {i+1}. {r['mw']:,.0f} MW at {r['dt']}")
    
    if jan68:
        peak68 = max(jan68, key=lambda r: r['mw'])
        print(f"\nJan 6-8, 2014 MAXIMUM:")
        print(f"  {peak68['mw']:,.0f} MW at {peak68['dt']}")
    
    # Check 143,531
    target_rows = [r for r in jan15 if abs(r['mw'] - MANUSCRIPT_TARGET) < 1]
    print(f"\n143,531 MW CHECK:")
    if target_rows:
        print(f"  ✓ FOUND at {target_rows[0]['dt']}")
        print(f"  Rank in Jan 1-15: #{sum(1 for r in jan15 if r['mw'] > target_rows[0]['mw']) + 1}")
    else:
        closest = min(jan15, key=lambda r: abs(r['mw'] - MANUSCRIPT_TARGET))
        print(f"  ✗ NOT FOUND. Closest: {closest['mw']:,.0f} MW at {closest['dt']}")
    
    # Verdict
    print(f"\n{'='*60}")
    if jan15:
        true_max = max(jan15, key=lambda r: r['mw'])
        if abs(true_max['mw'] - MANUSCRIPT_TARGET) < 1:
            print("VERDICT: Manuscript peak claim (143,531 MW) IS the verified maximum.")
            print("         No manuscript revision needed for peak value.")
        elif true_max['mw'] > MANUSCRIPT_TARGET:
            print(f"VERDICT: Manuscript peak claim (143,531 MW) is BELOW verified maximum ({true_max['mw']:,.0f} MW).")
            print(f"         Manuscript MUST be revised to reflect verified data.")
        else:
            print(f"VERDICT: Manuscript peak claim (143,531 MW) exceeds verified maximum ({true_max['mw']:,.0f} MW).")
            print(f"         Manuscript MUST be revised.")
    else:
        print("VERDICT: INCONCLUSIVE — no Jan 2014 data available.")

if __name__ == '__main__':
    main()
