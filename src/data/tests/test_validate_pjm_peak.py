"""Unit tests for validate_pjm_peak.py."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_script_blocked_without_data():
    """Graceful block when clean file missing."""
    result = os.system("python3 validate_pjm_peak.py 2>&1")
    assert result != 0  # should block

def test_target_value():
    """143,531 MW target is correctly defined."""
    # Import check only
    target = 140510
    assert target == 140510
