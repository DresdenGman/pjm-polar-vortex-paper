# C06A — DSI 6182 Delivery Runbook

**Branch:** C06-preload-readiness
**Status:** AWAITING NCEI DELIVERY

## After NCEI delivers the 4-date GFS sample:

### 1. Save files
```bash
mkdir -p data/raw/gfs_dsi6182/
# Copy delivered GRIB2 files to data/raw/gfs_dsi6182/
```

### 2. Generate checksums
```bash
find data/raw/gfs_dsi6182/ -name "*.grb2" -exec sha256sum {} \; > reports/C06A/dsi6182_checksums.txt
```

### 3. Inventory GRIB messages
```bash
python src/weather/inventory_gfs_dsi6182.py \
  --input data/raw/gfs_dsi6182/ \
  --output reports/C06A/dsi6182_sample_inventory.csv
```

### 4. Verify cycle and forecast hours
```bash
python src/weather/validate_gfs_dsi6182.py \
  --inventory reports/C06A/dsi6182_sample_inventory.csv
```

### 5. Decode required variables
```bash
python src/weather/decode_gfs_dsi6182.py \
  --input data/raw/gfs_dsi6182/ \
  --output data/processed/gfs_dsi6182_decoded.csv
```

### 6. Run sample coverage audit
```bash
python src/weather/gfs_sample_coverage.py \
  --decoded data/processed/gfs_dsi6182_decoded.csv \
  --output reports/C06A/dsi6182_feasibility.md
```

### 7. Build four-date aligned weather sample
```bash
python src/data/build_day_ahead_weather_sample.py \
  --load data/processed/day_ahead_load_calendar_2010_2014.csv \
  --gfs data/processed/gfs_dsi6182_decoded.csv \
  --output data/samples/C06A/day_ahead_gfs_sample.csv
```

### 8. Classify feasibility
```bash
python -m pytest tests/test_gfs_integration.py -q
```

**Pass threshold:** ≥95% joint coverage, all cycles before origin, one 06Z vintage per day.

### 9. Authorize or reject full retrieval
- If PROCEED: order full 2010-2014 GFS via same NCEI channel
- If STOP: redesign paper as ERA5 oracle stress test
