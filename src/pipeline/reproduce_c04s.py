"""C05B: Orchestrate the complete C04S reproduction pipeline.

Order:
  1. Validate modeling features CSV
  2. Chronological train/test split
  3. Train naive baselines
  4. Train Linear + GBoost point models
  5. Train 7 independent QR-GBT quantile models
  6. Export all predictions
  7. Calculate metrics
  8. Compare with frozen C04S reference CSVs
"""
import argparse
import subprocess
import sys
from pathlib import Path


SCRIPTS = {
    "validate": "src/data/build_modeling_features.py",
    "baselines": "src/models/train_baselines.py",
    "point_models": "src/models/train_point_models.py",
    "quantile_models": "src/models/train_quantile_gbt.py",
    "evaluate": "src/evaluation/evaluate_point.py",
}


def run_step(name: str, cmd: list[str]) -> int:
    print(f"\n{'='*60}")
    print(f"STEP: {name}")
    print(f"{'='*60}")
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f"FAILED: {name} (exit {result.returncode})", file=sys.stderr)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="C05B reproduction pipeline")
    parser.add_argument("--input", required=True, help="Path to modeling_features_2010_2014.csv")
    parser.add_argument("--output-dir", default="artifacts/C05B_reproduced", help="Output directory")
    parser.add_argument("--skip-validation", action="store_true")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    steps = []

    if not args.skip_validation:
        steps.append(("validate", [
            sys.executable, SCRIPTS["validate"],
            "--input", args.input,
        ]))

    steps.extend([
        ("baselines", [
            sys.executable, SCRIPTS["baselines"],
            "--input", args.input,
            "--output-dir", str(output_dir),
        ]),
        ("point_models", [
            sys.executable, SCRIPTS["point_models"],
            "--input", args.input,
            "--output-dir", str(output_dir),
        ]),
        ("quantile_models", [
            sys.executable, SCRIPTS["quantile_models"],
            "--input", args.input,
            "--output-dir", str(output_dir),
        ]),
        ("evaluate", [
            sys.executable, SCRIPTS["evaluate"],
            "--predictions", str(output_dir / "point_model_predictions.csv"),
            "--output-dir", str(output_dir),
        ]),
    ])

    failed = []
    for name, cmd in steps:
        rc = run_step(name, cmd)
        if rc != 0:
            failed.append(name)

    if failed:
        print(f"\nFAILED STEPS: {failed}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"\n{'='*60}")
        print("PIPELINE COMPLETE")
        print(f"Output: {output_dir}")
        print(f"{'='*60}")


if __name__ == "__main__":
    main()
