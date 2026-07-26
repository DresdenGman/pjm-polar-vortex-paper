"""C06A-PRELOAD: GFS DSI 6182 schema and validation rules.

Defines the expected interface for decoded GFS GRIB2 files.
Does NOT contain fake weather values — this is a contract, not sample data.
"""
import numpy as np
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class GFSForecastRecord:
    """One GFS forecast field at one valid time and grid point."""
    cycle_time_utc: datetime
    forecast_hour: int
    valid_time_utc: datetime
    latitude: float
    longitude: float
    variable_short_name: str
    variable_long_name: str
    level: str
    units: str
    value: float
    source_file: str
    checksum: str
    direct_or_derived: str  # "DIRECT_GFS" or "DERIVED_FROM_GFS"


EXPECTED_VARIABLES = {
    "t": {"long_name": "2 metre temperature", "level": "surface", "units": "K", "direct": True},
    "r": {"long_name": "2 metre relative humidity", "level": "surface", "units": "%", "direct": True},
    "q": {"long_name": "2 metre specific humidity", "level": "surface", "units": "kg kg**-1", "direct": True},
    "u10": {"long_name": "10 metre U wind component", "level": "surface", "units": "m s**-1", "direct": True},
    "v10": {"long_name": "10 metre V wind component", "level": "surface", "units": "m s**-1", "direct": True},
    "sp": {"long_name": "Surface pressure", "level": "surface", "units": "Pa", "direct": True},
    "d2m": {"long_name": "2 metre dewpoint temperature", "level": "surface", "units": "K", "direct": True},
}

REQUIRED_CYCLE = 6  # 06Z only
ALLOWED_FORECAST_HOURS = set(range(18, 49))  # f018-f048 inclusive


def validate_cycle(cycle_hour: int) -> bool:
    """Reject any cycle other than 06Z."""
    if cycle_hour != REQUIRED_CYCLE:
        raise ValueError(f"Expected 06Z cycle, got {cycle_hour:02d}Z")


def validate_forecast_hour(fh: int) -> bool:
    """Reject forecast hours outside requested range."""
    if fh not in ALLOWED_FORECAST_HOURS:
        raise ValueError(f"Forecast hour {fh} not in 018-048 range")


def validate_origin(cycle_utc: datetime, origin_utc: datetime) -> bool:
    """Reject cycles after the load forecast origin."""
    if cycle_utc > origin_utc:
        raise ValueError(f"Cycle {cycle_utc} after origin {origin_utc}")


def validate_variable(name: str) -> bool:
    """Check variable is in expected set."""
    if name not in EXPECTED_VARIABLES:
        raise ValueError(f"Unknown GFS variable: {name}. Expected: {list(EXPECTED_VARIABLES)}")
    return True
