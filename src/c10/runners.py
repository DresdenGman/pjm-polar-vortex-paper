"""C10 point/probabilistic runner interface (Command 048-P2C).

Interface only — .fit() is gated by production_enabled + full-year seal.
Scaffolding phase: no real model fitting on provisional data.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd

from .gates import GateError, check_production_enabled


@dataclass
class RunnerResult:
    status: str = "NOT_RUN"
    artifact_dir: Path | None = None
    notes: list[str] = field(default_factory=list)


class PointRunner:
    """C10A — weather-aware point models. Additive to C08B protocol."""

    def __init__(self, config: dict[str, Any], repo_root: Path):
        self.config = config
        self.repo = repo_root
        check_production_enabled(config)

    def prepare(self, matrix: pd.DataFrame) -> RunnerResult:
        """Build design matrix + create artifact dirs. No fit."""
        check_production_enabled(self.config)
        if "production_enabled" in self.config and not self.config["production_enabled"]:
            raise GateError("point runner refuses: production_enabled=false")
        artifact_dir = self.repo / "artifacts" / "C10A"
        artifact_dir.mkdir(parents=True, exist_ok=True)
        return RunnerResult(status="PREPARED", artifact_dir=artifact_dir, notes=["synthetic only"])


class ProbabilisticRunner:
    """C10B — weather-aware probabilistic. Additive to C08C machinery."""

    QUANTILES = [0.01, 0.05, 0.10, 0.50, 0.90, 0.95, 0.99]

    def __init__(self, config: dict[str, Any], repo_root: Path):
        self.config = config
        self.repo = repo_root
        check_production_enabled(config)

    def prepare(self, matrix: pd.DataFrame) -> RunnerResult:
        check_production_enabled(self.config)
        artifact_dir = self.repo / "artifacts" / "C10B"
        artifact_dir.mkdir(parents=True, exist_ok=True)
        return RunnerResult(status="PREPARED", artifact_dir=artifact_dir, notes=["synthetic only"])
