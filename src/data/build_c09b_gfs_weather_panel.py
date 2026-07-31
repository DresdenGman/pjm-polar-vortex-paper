"""C09B: Incremental GFS weather panel builder.

Reads GRIB files in place from audited tar archives, extracts station
values via bilinear interpolation, appends partitions per sample.
"""
import argparse, json, numpy as np, pandas as pd, pygrib, tarfile, tempfile, shutil
from pathlib import Path

VARS = ['sp', '2t', '2r', '10u', '10v']
LEADS = range(18, 51, 3)  # f018..f048


def extract_sample(tar_path, stations_df):
    """Extract station values from one GFS tar archive."""
    rows = []
    with tarfile.open(tar_path) as tar:
        members = [m for m in tar.getmembers() if m.name.endswith('.grb2')]
        for member in members:
            fh = int(member.name.split('_')[-1].replace('.grb2', ''))
            if fh not in LEADS:
                continue
            with tar.extractfile(member) as f:
                tmp = tempfile.NamedTemporaryFile(suffix='.grb2', delete=False)
                shutil.copyfileobj(f, tmp)
                tmp.close()
                try:
                    grb = pygrib.open(tmp.name)
                    for msg in grb:
                        sn = msg.shortName
                        if sn not in VARS:
                            continue
                        vals = msg.values
                        Ni, Nj = msg.Ni, msg.Nj
                        lat0 = msg.latitudeOfFirstGridPointInDegrees
                        lon0 = msg.longitudeOfFirstGridPointInDegrees
                        di = abs(msg.iDirectionIncrementInDegrees)
                        dj = abs(msg.jDirectionIncrementInDegrees)
                        lats_g = np.arange(Nj) * (-dj) + lat0
                        lons_g = np.arange(Ni) * di + lon0
                        for _, stn in stations_df.iterrows():
                            lat, lon = stn['latitude'], stn['longitude']
                            lon_norm = lon % 360
                            i = int((lon_norm - lon0) / di)
                            j = int((lat0 - lat) / (-dj))
                            i = max(0, min(i, Ni - 2))
                            j = max(0, min(j, Nj - 2))
                            wx = (lon_norm - lons_g[i]) / di
                            wy = (lat - lats_g[j]) / (-dj)
                            wx = max(0, min(1, wx))
                            wy = max(0, min(1, wy))
                            val = ((1 - wy) * ((1 - wx) * vals[j, i] + wx * vals[j, i + 1])
                                   + wy * ((1 - wx) * vals[j + 1, i] + wx * vals[j + 1, i + 1]))
                            rows.append({
                                'init_date': member.name.split('_')[2],
                                'forecast_hour': fh,
                                'station_id': stn['station_id'],
                                'variable': sn,
                                'value': float(val),
                            })
                    grb.close()
                finally:
                    Path(tmp.name).unlink(missing_ok=True)
    return pd.DataFrame(rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--sample-id', required=True, help='e.g. 2014-01-06')
    p.add_argument('--tar-path', required=True)
    p.add_argument('--station-registry', default='reports/C09B/station_registry.csv')
    p.add_argument('--output', default='reports/C09B')
    p.add_argument('--append-partition', action='store_true')
    args = p.parse_args()

    stations = pd.read_csv(args.station_registry)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    df = extract_sample(args.tar_path, stations)
    print(f'{args.sample_id}: {len(df)} raw records')

    # Pivot to wide
    pivot = df.pivot_table(index=['init_date', 'forecast_hour', 'station_id'],
                           columns='variable', values='value').reset_index()
    pivot.columns.name = None
    pivot['wind_speed_10m'] = np.sqrt(pivot['10u'] ** 2 + pivot['10v'] ** 2)
    pivot['temp_2m_c'] = pivot['2t'] - 273.15

    # Save partition
    part_file = out / f'gfs_native_panel_{args.sample_id}.csv'
    pivot.to_csv(part_file, index=False)
    print(f'Saved: {part_file} ({len(pivot)} rows)')

    # Append to master if requested
    if args.append_partition:
        master = out / 'gfs_native_panel.csv'
        if master.exists() and args.sample_id != '2014-03-08':
            old = pd.read_csv(master)
            combined = pd.concat([old, pivot], ignore_index=True)
            combined.to_csv(master, index=False)
            print(f'Appended to master: {len(combined)} total rows')
        else:
            pivot.to_csv(master, index=False)
            print(f'Master initialized: {len(pivot)} rows')


if __name__ == '__main__':
    main()
