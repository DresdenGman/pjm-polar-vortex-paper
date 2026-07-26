#!/usr/bin/env python3
"""Full-year 2014 metrics. SKELETON — do not run until PJM data obtained."""
import sys, os

DATA_REQUIRED = "data/predictions/full_year_2014.csv"

def main():
    if not os.path.exists(DATA_REQUIRED):
        print(f"BLOCKED: {DATA_REQUIRED} not available.")
        print("Waiting for PJM account approval and data download.")
        sys.exit(1)
    raise NotImplementedError("Not yet implemented — waiting for verified PJM data.")

if __name__ == "__main__":
    main()
