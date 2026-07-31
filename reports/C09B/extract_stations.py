"""Extract station lat/lon from NOAA CSV headers."""
import csv, pandas as pd
from pathlib import Path

RAW = Path("data/raw/noaa")
files = sorted(RAW.glob("*_2014.csv"))
stations = []
for f in files:
    with open(f) as fh:
        reader = csv.reader(fh)
        header = [h.strip('"') for h in next(reader)]
        row = next(reader)
        lat_idx = header.index("LATITUDE")
        lon_idx = header.index("LONGITUDE")
        sid = f.stem.replace("_2014","")
        stations.append({
            "station_id": sid,
            "latitude": float(row[lat_idx]),
            "longitude": float(row[lon_idx]),
            "source_file": f.name,
        })
df = pd.DataFrame(stations)
df.to_csv("reports/C09B/station_registry.csv", index=False)
print(df.to_string())
