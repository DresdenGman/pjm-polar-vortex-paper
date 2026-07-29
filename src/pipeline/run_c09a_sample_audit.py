"""C09A: Pipeline entry point — audit one or more GFS tar archives."""
import argparse, subprocess, shutil
from pathlib import Path

SCRIPTS = {
    "extract": "src/data/safe_extract_gfs_archive.py",
    "inventory": "src/data/inventory_gfs_grib.py",
    "grid": "src/data/audit_gfs_grid_homogeneity.py",
    "variables": "src/data/map_gfs_variables.py",
    "decoder": "src/data/audit_gfs_decoder_parity.py",
}

def run_script(name, *args):
    spath = SCRIPTS[name]
    cmd = ["python", spath] + list(args)
    print(f">>> {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR [{name}]: {result.stderr[:500]}")
        return False
    print(result.stdout[:500])
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="GFS tar archives to audit")
    parser.add_argument("--output-dir", default="artifacts/C09A")
    args = parser.parse_args()
    
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    
    extract_dir = out / "extracted"
    
    for f in args.files:
        fpath = Path(f)
        print(f"\n{'='*60}")
        print(f"Auditing: {fpath.name}")
        print(f"{'='*60}")
        
        # Extract
        inv_csv = out / f"{fpath.stem}_inventory.csv"
        run_script("extract", str(fpath), "--output", str(inv_csv),
                   "--extract-dir", str(extract_dir / fpath.stem))
        
        # Grid fingerprint
        grid_csv = out / f"{fpath.stem}_grid.csv"
        first_grib = next((extract_dir / fpath.stem).glob("*.grb2"), None)
        if first_grib:
            run_script("grid", str(first_grib), "--output", str(grid_csv))
    
    print(f"\nDone. Outputs in {out}")

if __name__ == "__main__":
    main()
