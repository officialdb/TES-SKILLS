"""Environment detection and discovery for AI coding agents."""

from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from tes.adapters import get_all_adapters
from tes.config import find_project_root, get_user_home
from tes.models import Scope


class EnvironmentStatus(BaseModel):
    adapter_id: str
    name: str
    detected_system: bool
    detected_project: bool
    global_path: str
    project_path: str


class DetectionReport(BaseModel):
    project_root: str
    detected_environments: List[EnvironmentStatus]
    primary_recommended: Optional[str] = None


class Detector:
    """Discovers installed AI coding agent environments."""

    @classmethod
    def detect_environments(cls, project_root: Optional[Path] = None) -> DetectionReport:
        root = project_root or find_project_root()
        home = get_user_home()
        adapters = get_all_adapters()

        statuses = []
        primary = None

        for adapter in adapters:
            sys_detected = adapter.detect()
            proj_dir = adapter.get_skill_dir(Scope.PROJECT, root)
            proj_detected = proj_dir.parent.exists() or proj_dir.exists()

            global_dir = adapter.get_skill_dir(Scope.GLOBAL, root)

            status = EnvironmentStatus(
                adapter_id=adapter.target_id,
                name=adapter.name,
                detected_system=sys_detected,
                detected_project=proj_detected,
                global_path=str(global_dir),
                project_path=str(proj_dir),
            )
            statuses.append(status)

            if not primary and (sys_detected or proj_detected) and adapter.target_id != "generic":
                primary = adapter.target_id

        if not primary:
            primary = "generic"

        return DetectionReport(
            project_root=str(root),
            detected_environments=statuses,
            primary_recommended=primary
        )
