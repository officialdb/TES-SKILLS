"""Environment detection and discovery for AI coding agents."""

from pathlib import Path
from typing import Optional

from tes.adapters import get_all_adapters
from tes.config import find_project_root
from tes.models import DetectionReport, EnvironmentStatus


class Detector:
    """Discovers installed AI coding agent environments with strict verification.
    
    Detection is strictly read-only and does not create directories or mutate configuration.
    """

    @classmethod
    def detect_environments(cls, project_root: Optional[Path] = None) -> DetectionReport:
        root = project_root.resolve() if project_root else find_project_root()
        adapters = get_all_adapters()

        statuses = []
        installed_adapters = []
        configured_adapters = []

        for adapter in adapters:
            status = adapter.detect_status(project_root=root)
            statuses.append(status)

            if status.installed and adapter.target_id != "generic":
                installed_adapters.append(adapter.target_id)
            elif (status.config_present or status.skills_directory_present) and adapter.target_id != "generic":
                configured_adapters.append(adapter.target_id)

        # Recommendation logic:
        # 1. Prefer actually verified installed applications
        # 2. Next check environments with existing configs or skills directories
        # 3. Fallback to open generic standard
        if installed_adapters:
            primary = installed_adapters[0]
        elif configured_adapters:
            primary = configured_adapters[0]
        else:
            primary = "generic"

        return DetectionReport(
            project_root=str(root) if root else None,
            detected_environments=statuses,
            primary_recommended=primary,
        )
