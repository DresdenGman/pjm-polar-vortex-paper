"""C10/C11 data loader scaffolding (Command 048-P2C).

Loads canonical 365-cycle panels post-final-seal, validates schema and
compound keys, and constructs the model matrix WITHOUT fitting.
Synthetic fixtures only during scaffolding.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from .gates import (
    GateError,
    check_duplicate_keys,
    check_join_keys,
    check_production_enabled,
    check_production_seal,
    check_weather_schema,
)

WEATHER_COLS = [
    "temperature_2m_celsius",
    "relative_humidity_2m_percent",
    "wind_speed_10m_mps",
    "surface_pressure_hpa",
]


class C10DataLoader:
    """Loads + validates C09D canonical panels. Never fits models."""

    def __init__(self, config: dict[str, Any], repo_root: Path):
        self.config = config
        self.repo = repo_root
        check_production_enabled(config)
        seal_path = self.repo / config.get("seal_path", "reports/C09D/C09D_2014_FINAL_SEAL.json")
        check_production_seal(seal_path)

    def load_hourly(self) -> pd.DataFrame:
        path = self.repo / self.config["hourly_panel_path"]
        df = pd.read_csv(path)
        check_weather_schema(df, WEATHER_COLS)
        keys = ["initialization_utc", "valid_time_utc", "station_id"]
        check_join_keys(keys, allow_network=False)
        check_duplicate_keys(df, keys)
        return df

    def load_network_panel(self) -> pd.DataFrame:
        path = self.repo / self.config["network_panel_path"]
        df = pd.read_csv(path)
        keys = ["initialization_utc", "valid_time_utc"]
        check_join_keys(keys, allow_network=True)
        check_duplicate_keys(df, keys)
        return df

    def construct_model_matrix(self, hourly: pd.DataFrame) -> pd.DataFrame:
        """Assemble load + weather feature block. No fitting here."""
        matrix = hourly.copy()
        # model-integration key per C09D join contract:
        # (day_ahead_origin_pjm, target_time_utc) resolved at C10 execution time
        return matrix
