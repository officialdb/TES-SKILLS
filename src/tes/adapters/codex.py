"""Adapter for OpenAI Codex CLI."""

from pathlib import Path
from typing import Optional
from tes.adapters.base import BaseAdapter
from tes.config import get_user_home


class CodexAdapter(BaseAdapter):
    """Integrates TES skills into OpenAI Codex CLI environments."""

    name = "OpenAI Codex CLI"
    target_id = "codex"
    default_project_rel_path = ".codex/skills"
    default_global_rel_path = ".codex/skills"

    executable_name = "codex"
    alternative_executables = [
        ".codex/bin/codex",
        ".local/bin/codex",
        "/usr/local/bin/codex",
        "/usr/bin/codex",
    ]

    # Multi-method discovery metadata
    desktop_names = ["Codex", "OpenAI Codex"]
    desktop_file_patterns = ["*codex*.desktop"]
    package_names = ["codex", "codex-cli"]
    snap_names = ["codex"]

    def check_config_present(self) -> bool:
        """Check whether recognized Codex configuration exists."""
        codex_dir = get_user_home() / ".codex"
        if not codex_dir.exists() or not codex_dir.is_dir():
            return False

        config_markers = ["config.toml", "version.json", "installation_id", "models_cache.json", "sessions"]
        return any((codex_dir / marker).exists() for marker in config_markers)

    def check_project_config_present(self, project_root: Optional[Path] = None) -> bool:
        """Check whether recognized project-level Codex configuration exists."""
        if not project_root or not project_root.exists():
            return False

        proj_markers = [
            project_root / ".codex" / "config.toml",
            project_root / "codex.toml",
        ]
        return any(p.exists() for p in proj_markers)
