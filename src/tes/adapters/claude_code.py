"""Adapter for Claude Code."""

from pathlib import Path
from typing import Optional
from tes.adapters.base import BaseAdapter
from tes.config import get_user_home


class ClaudeCodeAdapter(BaseAdapter):
    """Integrates TES skills into Claude Code environments."""

    name = "Claude Code"
    target_id = "claude-code"
    default_project_rel_path = ".claude/skills"
    default_global_rel_path = ".claude/skills"

    executable_name = "claude"
    alternative_executables = [
        ".local/bin/claude",
        "/usr/local/bin/claude",
        ".npm/bin/claude",
        ".claude/bin/claude",
        "/usr/bin/claude",
    ]

    # Multi-method discovery metadata
    desktop_names = ["Claude", "Claude Code"]
    desktop_file_patterns = ["*claude*.desktop"]
    package_names = ["claude-code", "claude"]
    flatpak_ids = ["com.anthropic.Claude"]
    snap_names = ["claude"]

    def check_config_present(self) -> bool:
        """Check whether recognized Claude Code configuration exists."""
        home = get_user_home()
        if (home / ".claude.json").exists():
            return True

        claude_dir = home / ".claude"
        if not claude_dir.exists() or not claude_dir.is_dir():
            return False

        config_markers = ["config.json", "settings.json", "credentials", "session.json", "history.jsonl"]
        return any((claude_dir / marker).exists() for marker in config_markers)

    def check_project_config_present(self, project_root: Optional[Path] = None) -> bool:
        """Check whether recognized project-level Claude Code configuration exists."""
        if not project_root or not project_root.exists():
            return False

        proj_markers = [
            project_root / ".claude" / "config.json",
            project_root / ".claude.json",
            project_root / "CLAUDE.md",
        ]
        return any(p.exists() for p in proj_markers)
