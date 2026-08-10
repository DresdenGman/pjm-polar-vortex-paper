"""C10/C11 shared data gates (Command 048-P2R).

Enforces:
- C09D_2014_FINAL_SEAL required (not January seal, not 30C provisional)
- compound-key weather joins only (no valid_time_utc-only)
- production_enabled=false blocks all model fitting
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class GateError(Exception):
    """Raised when a production gate rejects execution."""


def load_seal(seal_path: Path) -> dict[str, Any]:
    if not seal_path.exists():
        raise GateError(f"C09D_2014_FINAL_SEAL missing: {seal_path}")
    return json.loads(seal_path.read_text())


def check_production_seal(seal_path: Path) -> dict[str, Any]:
    """Full-year seal gate. Rejects missing seal, January-only, or provisional."""
    seal = load_seal(seal_path)
    if seal.get("status") != "FINAL_SEALED":
        raise GateError(
            f"seal.status={seal.get('status')!r} != FINAL_SEALED — "
            "30C provisional / January milestone is NOT a production population"
        )
    if not seal.get("analysis_population_approved", False):
        raise GateError("analysis_population_approved != true")
    n_cycles = seal.get("source_verified_cycles")
    if n_cycles is not None and n_cycles < 365:
        raise GateError(
            f"source_verified_cycles={n_cycles} < 365 — full-year population required "
            "(January 31/31 does not make C09D production complete)"
        )
    return seal


def check_production_enabled(config: dict[str, Any]) -> None:
    if not config.get("production_enabled", False):
        raise GateError("production_enabled=false — model fitting refused")


def check_join_keys(join_keys: list[str], allow_network: bool = False) -> None:
    """Compound-key join gate. Rejects valid_time_utc-only joins (7h overlap)."""
    if join_keys == ["valid_time_utc"]:
        raise GateError(
            "valid_time_utc-only join refused — adjacent f018..f048 trajectories "
            "overlap by 7 valid hours (C09D production join contract)"
        )
    if allow_network:
        required = {"initialization_utc", "valid_time_utc"}
    else:
        required = {"initialization_utc", "valid_time_utc", "station_id"}
    if not required.issubset(set(join_keys)):
        raise GateError(f"join keys {join_keys} missing required compound keys {required}")


def check_weather_schema(df: Any, required_cols: list[str]) -> None:
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise GateError(f"weather schema incomplete — missing columns: {missing}")


def check_duplicate_keys(df: Any, keys: list[str]) -> None:
    n = int(df.duplicated(keys).sum())
    if n > 0:
        raise GateError(f"duplicate compound weather keys: {n}")
