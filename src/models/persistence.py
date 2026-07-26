#!/usr/bin/env python3
"""Naive persistence baseline. SKELETON — do not run until PJM data obtained."""
import sys, os

DATA_REQUIRED = "data/processed/pjm_load_2010_2014.csv"

def main():
    if not os.path.exists(DATA_REQUIRED):
        print(f"BLOCKED: {DATA_REQUIRED} not available.")
        print("Waiting for PJM account approval and data download.")
        sys.exit(1)
    raise NotImplementedError("Not yet implemented — waiting for verified PJM data.")

if __name__ == "__main__":
    main()
