"""C09A: Compare GRIB grid fingerprints across multiple sample files."""
import argparse, pygrib, pandas as pd
from pathlib import Path

def grid_fingerprint(grib_path):
    grb = pygrib.open(str(grib_path))
    msg = grb[1]  # First message
    fp = {
        "file": str(grib_path),
        "Ni": msg.Ni, "Nj": msg.Nj,
        "lat_first": msg.latitudeOfFirstGridPointInDegrees,
        "lon_first": msg.longitudeOfFirstGridPointInDegrees,
        "lat_last": msg.latitudeOfLastGridPointInDegrees,
        "lon_last": msg.longitudeOfLastGridPointInDegrees,
        "i_inc": msg.iDirectionIncrementInDegrees,
        "j_inc": msg.jDirectionIncrementInDegrees,
        "scanning_mode": msg.scanningMode,
        "grid_type": msg.gridType,
    }
    grb.close()
    return fp

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="GRIB2 files to fingerprint")
    parser.add_argument("--output", "-o", default="gfs_grid_fingerprints.csv")
    args = parser.parse_args()
    
    fps = []
    for f in args.files:
        fp = grid_fingerprint(f)
        fps.append(fp)
        print(f"  {f}: {fp['Ni']}×{fp['Nj']}, {fp['i_inc']:.4f}°, scan={fp['scanning_mode']}")
    
    df = pd.DataFrame(fps)
    df.to_csv(args.output, index=False)
    print(f"\nGrid consistency: {'ALL MATCH' if df['Ni'].nunique() == 1 and df['Nj'].nunique() == 1 else 'DIFFERENT GRIDS!'}")
    print(f"Saved to {args.output}")

if __name__ == "__main__":
    main()
