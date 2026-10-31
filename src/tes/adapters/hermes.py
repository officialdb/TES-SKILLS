"""Adapter for Hermes AI Agent."""

from pathlib import Path
from typing import Optional
from tes.adapters.base import BaseAdapter
from tes.config import get_user_home


class HermesAdapter(BaseAdapter):
    """Integrates TES skills into Hermes coding agent environments."""

    name = "Hermes"
    target_id = "hermes"
    default_project_rel_path = ".hermes/skills"
    default_global_rel_path = ".hermes/skills"

    executable_name = "hermes"
    alternative_executables = [
        ".hermes/bin/hermes",
        ".local/bin/hermes",
        "/usr/local/bin/hermes",
        "/usr/bin/hermes",
    ]

    # Multi-method discovery metadata
    desktop_names = ["Hermes", "hermes"]
    desktop_file_patterns = ["*hermes*.desktop"]
    known_app_dirs = [Path("/opt/Hermes"), Path("/opt/hermes")]
    package_names = ["hermes"]
    flatpak_ids = ["ai.hermes.Hermes"]
    snap_names = ["hermes"]

    def check_config_present(self) -> bool:
        """Check whether recognized Hermes application configuration exists."""
        hermes_dir = get_user_home() / ".hermes"
        if not hermes_dir.exists() or not hermes_dir.is_dir():
            return False

        config_markers = ["config.json", "config.yaml", "config.toml", "hermes.json", ".env", "credentials"]
        return any((hermes_dir / marker).exists() for marker in config_markers)

    def check_project_config_present(self, project_root: Optional[Path] = None) -> bool:
        """Check whether recognized project-level Hermes configuration exists."""
        if not project_root or not project_root.exists():
            return False

        proj_markers = [
            project_root / ".hermes" / "config.json",
            project_root / ".hermes" / "hermes.json",
            project_root / ".hermes" / "config.yaml",
            project_root / "hermes.json",
        ]
        return any(p.exists() for p in proj_markers)
