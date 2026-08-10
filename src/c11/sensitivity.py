"""C11 ablation + event sensitivity scaffolding (Command 048-P2C).

- C11A: post-hoc explanatory — requires C10 frozen
- C11B: secondary robustness — requires locked threshold grid
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..c10.gates import GateError, check_production_enabled


@dataclass
class C11Result:
    status: str = "NOT_RUN"
    artifact_dir: Path | None = None
    role: str = ""


class AblationRunner:
    """C11A — remove one predefined weather feature group at a time."""

    def __init__(self, config: dict[str, Any], repo_root: Path):
        self.config = config
        self.repo = repo_root
        check_production_enabled(config)
        if config.get("requires_c10a_frozen") is not True:
            raise GateError("C11A refuses: requires_c10a_frozen != true")
        if config.get("requires_c10b_frozen") is not True:
            raise GateError("C11A refuses: requires_c10b_frozen != true")
        if config.get("analysis_role") != "secondary_explanatory":
            raise GateError("C11A refuses: analysis_role must be secondary_explanatory")

    def prepare(self) -> C11Result:
        artifact_dir = self.repo / "artifacts" / "C11A"
        artifact_dir.mkdir(parents=True, exist_ok=True)
        return C11Result(status="PREPARED", artifact_dir=artifact_dir, role="secondary_explanatory")


class EventSensitivityRunner:
    """C11B — threshold sensitivity. Primary events immutable."""

    def __init__(self, config: dict[str, Any], repo_root: Path):
        self.config = config
        self.repo = repo_root
        check_production_enabled(config)
        if config.get("primary_event_registry_immutable") is not True:
            raise GateError("C11B refuses: primary_event_registry_immutable != true")
        if config.get("analysis_role") != "secondary_robustness":
            raise GateError("C11B refuses: analysis_role must be secondary_robustness")
        if config.get("threshold_grid_locked") is not True:
            raise GateError(
                "C11B execution refuses: threshold_grid_locked != true "
                "(grid must be frozen by Commander before any run)"
            )

    def prepare(self) -> C11Result:
        artifact_dir = self.repo / "artifacts" / "C11B"
        artifact_dir.mkdir(parents=True, exist_ok=True)
        return C11Result(status="PREPARED", artifact_dir=artifact_dir, role="secondary_robustness")
