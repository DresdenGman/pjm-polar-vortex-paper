"""Unit tests for preprocess_pjm_forecast.py."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_script_blocked_without_data():
    """Graceful block when raw file missing."""
    result = os.system("python3 preprocess_pjm_forecast.py 2>&1")
    assert result != 0

def test_column_detection(synthetic_forecast_csv):
    """Detect forecast column headers."""
    import csv
    with open(synthetic_forecast_csv) as f:
        reader = csv.DictReader(f)
        row = next(reader)
        fc_col = next(c for c in ['day_ahead_forecast_mw', 'forecast_mw', 'mw'] if c in row)
        assert fc_col == 'forecast_mw'
