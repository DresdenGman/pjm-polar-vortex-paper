"""C09A: Inventory GRIB files — enumerate members, variables, grid, forecast hours."""
import argparse, pygrib, pandas as pd
from pathlib import Path

def inventory(grib_path):
    records = []
    grb = pygrib.open(str(grib_path))
    for msg in grb:
        records.append({
            "member": msg.messagenumber,
            "short_name": msg.shortName,
            "name": msg.name,
            "param_id": msg.paramId,
            "level": msg.level,
            "type_of_level": msg.typeOfLevel,
            "units": msg.units,
            "forecast_hour": msg.forecastTime,
            "data_date": msg.dataDate,
            "data_time": msg.dataTime,
            "valid_time": f"{msg.validDate} {msg.validTime:04d}",
            "Ni": msg.Ni,
            "Nj": msg.Nj,
            "lat_first": msg.latitudeOfFirstGridPointInDegrees,
            "lon_first": msg.longitudeOfFirstGridPointInDegrees,
            "lat_last": msg.latitudeOfLastGridPointInDegrees,
            "lon_last": msg.longitudeOfLastGridPointInDegrees,
            "i_direction_increment": msg.iDirectionIncrementInDegrees,
            "j_direction_increment": msg.jDirectionIncrementInDegrees,
            "scanning_mode": msg.scanningMode,
        })
    grb.close()
    return pd.DataFrame(records)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("grib_path", help="Path to GRIB2 file")
    parser.add_argument("--output", "-o", default="grib_inventory.csv")
    args = parser.parse_args()
    
    df = inventory(args.grib_path)
    df.to_csv(args.output, index=False)
    print(f"Inventoried {len(df)} records from {args.grib_path}")
    print(f"  Variables: {df['short_name'].unique().tolist()}")
    print(f"  Forecast hours: {sorted(df['forecast_hour'].unique())}")
    print(f"  Grid: {df['Ni'].iloc[0]}×{df['Nj'].iloc[0]}, {df['i_direction_increment'].iloc[0]:.4f}°")
    print(f"  Saved to {args.output}")

if __name__ == "__main__":
    main()
