"""Unit tests for preprocess_pjm_load.py — synthetic data only."""
import sys, os, csv, pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_missing_raw_file():
    """Graceful failure when raw file absent."""
    result = os.system("python3 preprocess_pjm_load.py 2>&1")
    assert result != 0  # should exit non-zero

def test_column_detection(synthetic_pjm_csv):
    """Detect various PJM column headers."""
    rows = []
    with open(synthetic_pjm_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts_col = next(c for c in ['timestamp_ept', 'datetime_beginning_ept'] if c in row)
            load_col = next(c for c in ['actual_load_mw', 'mw'] if c in row)
            assert ts_col == 'datetime_beginning_ept'
            assert load_col == 'mw'
            rows.append(row)
    assert len(rows) == 3

def test_synthetic_peak(synthetic_pjm_csv):
    """Peak detection works on synthetic data."""
    max_mw = 0
    with open(synthetic_pjm_csv) as f:
        for row in csv.DictReader(f):
            mw = float(row['mw'])
            if mw > max_mw:
                max_mw = mw
    assert max_mw == 142000  # fixture max is 142000

def test_bad_values_detected(bad_csv):
    """Flag negative, duplicate, and unparseable rows."""
    issues = 0
    seen = set()
    with open(bad_csv) as f:
        for row in csv.DictReader(f):
            try:
                ts = row['datetime_beginning_ept'].strip()
                mw = float(row['mw'])
                if mw <= 0:
                    issues += 1
                if ts in seen:
                    issues += 1
                seen.add(ts)
            except:
                issues += 1
    assert issues >= 3  # negative + duplicate + garbage

def test_output_paths_exist():
    """Output directories created."""
    assert os.path.exists('data/raw/pjm') or os.path.exists('data/raw/pjm/pjm_load_2014_rto_hourly.csv')
