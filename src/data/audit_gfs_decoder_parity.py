"""C09A: Compare cfgrib vs pygrib decoder parity on same GRIB2 files."""
import argparse, pygrib, xarray as xr, pandas as pd
from pathlib import Path

def parity_temperature(grib_path):
    """Compare t2m from both decoders."""
    # pygrib
    grb = pygrib.open(str(grib_path))
    pyg_t2m = None
    for msg in grb:
        if msg.shortName == "2t":
            pyg_t2m = msg.values
            pyg_level = (msg.Ni, msg.Nj)
            break
    grb.close()
    
    # cfgrib
    try:
        ds = xr.open_dataset(str(grib_path), engine="cfgrib",
                             backend_kwargs={"filter_by_keys": {"shortName": "2t"}})
        cfg_t2m = ds["t2m"].values
        cfg_level = (ds.dims["longitude"], ds.dims["latitude"])
        ds.close()
    except Exception as e:
        return {"file": str(grib_path), "check": "t2m",
                "pygrib_shape": pyg_level if pyg_t2m is not None else None,
                "cfgrib_shape": None, "cfgrib_error": str(e)}
    
    match = False
    if pyg_t2m is not None and cfg_t2m is not None:
        if pyg_t2m.shape == cfg_t2m.shape:
            match = bool((pyg_t2m == cfg_t2m).all())
    
    return {"file": str(grib_path), "check": "t2m",
            "pygrib_shape": pyg_level, "cfgrib_shape": cfg_level,
            "shape_match": pyg_level == cfg_level,
            "values_match": match}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("grib_path", help="GRIB2 file to compare")
    parser.add_argument("--output", "-o", default="decoder_parity.csv")
    args = parser.parse_args()
    
    result = parity_temperature(args.grib_path)
    df = pd.DataFrame([result])
    df.to_csv(args.output, index=False)
    print(f"Decoder parity for {args.grib_path}:")
    for k, v in result.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
