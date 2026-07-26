"""Unit-test fixtures — SYNTHETIC, not real data."""
import csv, os, pytest

TEST_DIR = os.path.dirname(__file__)

@pytest.fixture
def synthetic_pjm_csv(tmp_path):
    """Create a tiny synthetic PJM CSV for unit testing."""
    path = tmp_path / "test_load.csv"
    with open(path, 'w') as f:
        f.write("datetime_beginning_ept,mw\n")
        f.write("2014-01-07 18:00:00,140000\n")
        f.write("2014-01-07 09:00:00,142000\n")
        f.write("2014-01-07 10:00:00,141500\n")
    return str(path)

@pytest.fixture
def synthetic_forecast_csv(tmp_path):
    """Tiny synthetic forecast CSV."""
    path = tmp_path / "test_forecast.csv"
    with open(path, 'w') as f:
        f.write("datetime_ept,forecast_mw\n")
        f.write("2014-01-07 08:00:00,136000\n")
    return str(path)

@pytest.fixture
def bad_csv(tmp_path):
    """CSV with bad values."""
    path = tmp_path / "bad.csv"
    with open(path, 'w') as f:
        f.write("datetime_beginning_ept,mw\n")
        f.write("2014-01-07 08:00:00,-500\n")   # negative
        f.write("2014-01-07 08:00:00,140000\n")  # duplicate timestamp
        f.write("garbage,not_a_number\n")          # unparseable
    return str(path)
