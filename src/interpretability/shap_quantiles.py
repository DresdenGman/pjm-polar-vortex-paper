#!/usr/bin/env python3
"""Quantile-specific SHAP. SKELETON — do not run until PJM data obtained."""
import sys, os

DATA_REQUIRED = "data/predictions/vortex_predictions.csv"

def main():
    if not os.path.exists(DATA_REQUIRED):
        print(f"BLOCKED: {DATA_REQUIRED} not available.")
        print("Waiting for PJM account approval and data download.")
        sys.exit(1)
    raise NotImplementedError("Not yet implemented — waiting for verified PJM data.")

if __name__ == "__main__":
    main()
