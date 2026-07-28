"""C09A: Validate GFS GRIB variable identity across sample files."""
import argparse, pygrib, pandas as pd
from pathlib import Path

def variable_map(grib_path):
    grb = pygrib.open(str(grib_path))
    vars = {}
    for msg in grb:
        key = (msg.shortName, msg.paramId, msg.level, msg.typeOfLevel)
        if key not in vars:
            vars[key] = {
                "short_name": msg.shortName, "param_id": msg.paramId,
                "name": msg.name, "level": msg.level, "type_of_level": msg.typeOfLevel,
                "units": msg.units, "forecast_hours": set()
            }
        vars[key]["forecast_hours"].add(msg.forecastTime)
    grb.close()
    for v in vars.values():
        v["forecast_hours"] = sorted(v["forecast_hours"])
        v["n_forecast_hours"] = len(v["forecast_hours"])
        v["file"] = str(grib_path)
    return list(vars.values())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="GRIB2 files to compare")
    parser.add_argument("--output", "-o", default="gfs_variable_mapping.csv")
    args = parser.parse_args()
    
    all_vars = []
    for f in args.files:
        vars = variable_map(f)
        all_vars.extend(vars)
    
    df = pd.DataFrame(all_vars)
    df.to_csv(args.output, index=False)
    
    # Consistency check
    files = df["file"].unique()
    print(f"Files compared: {len(files)}")
    for f in files:
        sub = df[df["file"] == f]
        print(f"  {f}: {len(sub)} variable groups")
    
    # Check if variable set is consistent
    var_sets = df.groupby("file")["short_name"].apply(lambda x: tuple(sorted(set(x))))
    print(f"\nVariable consistency: {'ALL MATCH' if var_sets.nunique() == 1 else 'DIFFERENT! Sets: ' + str(var_sets.tolist())}")
    print(f"Saved to {args.output}")

if __name__ == "__main__":
    main()
