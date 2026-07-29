"""C09A: Safely extract GFS tar archive and inventory GRIB members."""
import argparse, os, shutil, tarfile, hashlib, pygrib, pandas as pd
from pathlib import Path

def extract(tar_path, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Validate tar
    if not tarfile.is_tarfile(tar_path):
        raise ValueError(f"Not a valid tar: {tar_path}")
    
    member_count = 0
    with tarfile.open(tar_path, "r") as tar:
        for member in tar.getmembers():
            # Security: reject absolute paths and symlink escapes
            if member.name.startswith("/") or ".." in member.name:
                raise SecurityError(f"Path traversal detected: {member.name}")
            tar.extract(member, path=output_dir)
            member_count += 1
    
    # Inventory all GRIB files
    records = []
    for grib_path in sorted(output_dir.glob("*.grb2")):
        try:
            grb = pygrib.open(str(grib_path))
            for msg in grb:
                records.append({
                    "file": grib_path.name,
                    "member": msg.messagenumber,
                    "short_name": msg.shortName,
                    "param_id": msg.paramId,
                    "level": msg.level,
                    "type_of_level": msg.typeOfLevel,
                    "units": msg.units,
                    "forecast_hour": msg.forecastTime,
                    "data_date": msg.dataDate,
                    "data_time": msg.dataTime,
                    "Ni": msg.Ni,
                    "Nj": msg.Nj,
                })
            grb.close()
        except Exception as e:
            records.append({"file": grib_path.name, "error": str(e)})
    
    return pd.DataFrame(records), member_count

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tar_path", help="Path to GFS tar archive")
    parser.add_argument("--output", "-o", default="grib_inventory.csv")
    parser.add_argument("--extract-dir", default="extracted")
    args = parser.parse_args()
    
    df, count = extract(args.tar_path, args.extract_dir)
    df.to_csv(args.output, index=False)
    
    print(f"Extracted {count} members from {args.tar_path}")
    print(f"  GRIB inventory: {len(df)} messages")
    if "short_name" in df.columns and not df["short_name"].isna().all():
        print(f"  Variables: {df['short_name'].unique().tolist()}")
        print(f"  Forecast hours: {sorted(df['forecast_hour'].unique())}")
    print(f"  Saved to {args.output}")

if __name__ == "__main__":
    main()
