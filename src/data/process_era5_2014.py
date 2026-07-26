#!/usr/bin/env python3
"""process_era5_2014.py — Aggregate ERA5 2014 to PJM weather CSV.
   Runs after era5_2014_Q*.nc files are downloaded.
   Produces 4 aggregation-method CSVs + validation report.
"""
import xarray as xr, numpy as np, pandas as pd, os, csv
from datetime import timedelta

RAW_DIR = "data/raw/era5"
OUT_DIR = "data/processed"
VALIDATION_DIR = "data/validation"

# --- Load all quarters ---
def load_era5():
    datasets = []
    for q in ['Q1','Q2','Q3','Q4']:
        path = f"{RAW_DIR}/era5_2014_{q}.nc"
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing: {path}")
        ds = xr.open_dataset(path)
        datasets.append(ds)
    return xr.concat(datasets, dim='valid_time')

def compute_aggregates(ds, label, lat_slice, lon_slice):
    """Compute hourly aggregation for a geographic subset."""
    t2m_f = (ds['t2m'].sel(latitude=lat_slice, longitude=lon_slice) - 273.15) * 9/5 + 32
    d2m_f = None
    if 'd2m' in ds:
        d2m_f = (ds['d2m'].sel(latitude=lat_slice, longitude=lon_slice) - 273.15) * 9/5 + 32
    
    u10 = ds['u10'].sel(latitude=lat_slice, longitude=lon_slice)
    v10 = ds['v10'].sel(latitude=lat_slice, longitude=lon_slice)
    ws_mps = np.sqrt(u10**2 + v10**2)
    ws_mph = ws_mps * 2.23694
    
    # Spatial means
    t_mean = t2m_f.mean(dim=['latitude','longitude'])
    d_mean = d2m_f.mean(dim=['latitude','longitude']) if d2m_f is not None else None
    w_mean = ws_mph.mean(dim=['latitude','longitude'])
    
    # Grid cell count
    n_cells = len(t2m_f.latitude) * len(t2m_f.longitude)
    
    rows = []
    for i in range(len(t_mean.valid_time)):
        dt = pd.Timestamp(t_mean.valid_time.values[i]).to_pydatetime()
        dt_ept = dt - timedelta(hours=5)
        
        t = float(t_mean.values[i])
        d = float(d_mean.values[i]) if d_mean is not None else None
        w = float(w_mean.values[i])
        
        # Wind chill (NOAA formula)
        if t <= 50 and w > 3:
            wc = 35.74 + 0.6215*t - 35.75*(w**0.16) + 0.4275*t*(w**0.16)
        else:
            wc = t
        
        hdh = max(65 - t, 0)
        cdh = max(t - 65, 0)
        
        rows.append({
            'timestamp_utc': dt.strftime('%Y-%m-%d %H:%M:%S'),
            'timestamp_ept': dt_ept.strftime('%Y-%m-%d %H:%M:%S'),
            'aggregation_method': label,
            'temperature_f': round(t, 1),
            'dewpoint_f': round(d, 1) if d is not None else '',
            'wind_speed_mph': round(w, 1),
            'wind_chill_f': round(wc, 1),
            'hdh': round(hdh, 1),
            'cdh': round(cdh, 1),
            'grid_cell_count': n_cells,
            'lat_min': float(t2m_f.latitude.min()),
            'lat_max': float(t2m_f.latitude.max()),
            'lon_min': float(t2m_f.longitude.min()),
            'lon_max': float(t2m_f.longitude.max()),
        })
    return rows

def write_csv(rows, filename):
    path = f"{OUT_DIR}/{filename}"
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print(f"  ✓ {path}: {len(rows)} hours")

def vortex_summary(rows, label):
    """Extract Jan 6-8 stats."""
    v = [r for r in rows if r['timestamp_ept'].startswith('2014-01-06') or
         r['timestamp_ept'].startswith('2014-01-07') or
         r['timestamp_ept'].startswith('2014-01-08')]
    if not v:
        return {}
    temps = [r['temperature_f'] for r in v]
    wcs = [r['wind_chill_f'] for r in v]
    hdhs = [r['hdh'] for r in v]
    return {
        'method': label,
        'mean_temp': round(sum(temps)/len(temps), 1),
        'min_temp': round(min(temps), 1),
        'max_temp': round(max(temps), 1),
        'mean_wind_chill': round(sum(wcs)/len(wcs), 1),
        'min_wind_chill': round(min(wcs), 1),
        'mean_hdh': round(sum(hdhs)/len(hdhs), 1),
        'hours': len(v),
    }

# --- Main ---
def main():
    print("Loading ERA5 2014 quarters...")
    ds = load_era5()
    
    # Define 4 aggregation domains
    domains = [
        ("full_bbox", slice(42.5, 35), slice(-88, -74)),
        ("northern_corridor", slice(42.5, 39), slice(-88, -74)),
        ("great_lakes_core", slice(42.5, 40), slice(-88, -80)),
        ("spatial_minmax", slice(42.5, 35), slice(-88, -74)),  # same bbox, different aggregation
    ]
    
    all_summaries = []
    for label, lat_s, lon_s in domains:
        print(f"\nProcessing: {label}...")
        rows = compute_aggregates(ds, label, lat_s, lon_s)
        write_csv(rows, f"weather_era5_pjm_2014_{label}.csv")
        
        if label != 'spatial_minmax':
            s = vortex_summary(rows, label)
            all_summaries.append(s)
    
    # Spatial min/max (event severity, not load input)
    t2m_f = (ds['t2m'] - 273.15) * 9/5 + 32
    vortex_t = t2m_f.sel(valid_time=slice('2014-01-06', '2014-01-08'))
    spatial_min = float(vortex_t.min().values)
    spatial_max = float(vortex_t.max().values)
    
    # Print comparison table
    print(f"\n{'='*70}")
    print(f"Jan 6-8, 2014 — Aggregation Method Comparison")
    print(f"{'='*70}")
    print(f"{'Method':<30} {'Mean T':>7} {'Min T':>7} {'Mean WC':>8} {'Min WC':>8} {'HDH':>6}")
    print(f"{'-'*70}")
    for s in all_summaries:
        print(f"{s['method']:<30} {s['mean_temp']:>6.1f}°F {s['min_temp']:>6.1f}°F {s['mean_wind_chill']:>7.1f}°F {s['min_wind_chill']:>7.1f}°F {s['mean_hdh']:>5.1f}")
    
    print(f"{'Spatial minimum (coldest cell)':<30} {'—':>7} {spatial_min:>6.1f}°F")
    print(f"\nReference values:")
    print(f"  Paper Table 1 (UNVERIFIED):  mean -1.8°F,  min -14.2°F")
    print(f"  NOAA 4-station provisional:  mean  12.7°F,  min  -3.0°F")
    
    ds.close()
    print(f"\n✓ All CSVs written to {OUT_DIR}/")

if __name__ == '__main__':
    main()
