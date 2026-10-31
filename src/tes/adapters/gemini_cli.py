"""Adapter for Gemini CLI and Antigravity."""

from pathlib import Path
from typing import Optional
from tes.adapters.base import BaseAdapter
from tes.config import get_user_home


class GeminiCliAdapter(BaseAdapter):
    """Integrates TES skills into Gemini CLI environments."""

    name = "Gemini CLI"
    target_id = "gemini-cli"
    default_project_rel_path = ".gemini/skills"
    default_global_rel_path = ".gemini/config/skills"

    executable_name = "gemini"
    alternative_executables = [
        ".gemini/bin/gemini",
        ".local/bin/gemini",
        "/usr/local/bin/gemini",
        "/usr/bin/gemini",
        ".local/bin/gemini-cli",
    ]

    # Multi-method discovery metadata
    desktop_names = ["Gemini", "Gemini CLI", "Google Gemini"]
    desktop_file_patterns = ["*gemini*.desktop"]
    package_names = ["gemini", "gemini-cli"]
    snap_names = ["gemini"]

    def check_config_present(self) -> bool:
        """Check whether recognized Gemini CLI configuration exists."""
        gemini_dir = get_user_home() / ".gemini"
        if not gemini_dir.exists() or not gemini_dir.is_dir():
            return False

        config_markers = [
            gemini_dir / "config" / "config.json",
            gemini_dir / "settings.json",
            gemini_dir / "jetski-standalone-oauth-token",
            gemini_dir / "oauth_credentials.json",
            gemini_dir / "antigravity",
        ]
        return any(p.exists() for p in config_markers)

    def check_project_config_present(self, project_root: Optional[Path] = None) -> bool:
        """Check whether recognized project-level Gemini configuration exists."""
        if not project_root or not project_root.exists():
            return False

        proj_markers = [
            project_root / ".gemini" / "settings.json",
            project_root / ".gemini" / "config.json",
            project_root / "gemini.json",
            project_root / "GEMINI.md",
        ]
        return any(p.exists() for p in proj_markers)
