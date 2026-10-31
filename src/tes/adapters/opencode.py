"""Adapter for OpenCode AI Agent."""

from pathlib import Path
from typing import Optional
from tes.adapters.base import BaseAdapter
from tes.config import get_user_home


class OpenCodeAdapter(BaseAdapter):
    """Integrates TES skills into OpenCode coding agent environments."""

    name = "OpenCode"
    target_id = "opencode"
    default_project_rel_path = ".opencode/skills"
    default_global_rel_path = ".config/opencode/skills"

    executable_name = "opencode"
    alternative_executables = [
        ".opencode/bin/opencode",
        ".local/bin/opencode",
        "/usr/local/bin/opencode",
        "/usr/bin/opencode",
        ".npm/bin/opencode",
    ]

    # Multi-method discovery metadata
    desktop_names = ["OpenCode", "opencode", "ai.opencode"]
    desktop_file_patterns = ["*opencode*.desktop", "ai.opencode*.desktop"]
    known_app_dirs = [Path("/opt/OpenCode"), Path("/opt/opencode")]
    known_binaries = [
        Path("/opt/OpenCode/ai.opencode"),
        Path("/opt/OpenCode/opencode"),
        Path("/usr/bin/ai.opencode"),
    ]
    package_names = ["opencode"]
    flatpak_ids = ["ai.opencode.OpenCode", "com.opencode.OpenCode"]
    snap_names = ["opencode"]
    version_file_rel_paths = ["resources/opencode-cli.version", "resources/app/package.json"]

    def check_config_present(self) -> bool:
        """Check whether recognized OpenCode configuration exists."""
        home = get_user_home()
        candidates = [home / ".config" / "opencode", home / ".opencode"]
        config_files = ["opencode.json", "service.json", "config.json", "settings.json", "config.toml"]

        for cdir in candidates:
            if cdir.exists() and cdir.is_dir():
                if any((cdir / f).exists() for f in config_files):
                    return True
        return False

    def check_project_config_present(self, project_root: Optional[Path] = None) -> bool:
        """Check whether recognized project-level OpenCode configuration exists."""
        if not project_root or not project_root.exists():
            return False

        proj_markers = [
            project_root / ".opencode" / "opencode.json",
            project_root / ".opencode" / "config.json",
            project_root / "opencode.json",
        ]
        return any(p.exists() for p in proj_markers)
