"""Adapter for Claude Code."""

import shutil
from pathlib import Path
from tes.adapters.base import BaseAdapter
from tes.config import get_user_home


class ClaudeCodeAdapter(BaseAdapter):
    """Integrates TES skills into Claude Code environments."""

    name = "Claude Code"
    target_id = "claude-code"
    default_project_rel_path = ".claude/skills"
    default_global_rel_path = ".claude/skills"

    def detect(self) -> bool:
        if shutil.which("claude") is not None:
            return True
        claude_home = get_user_home() / ".claude"
        return claude_home.exists()
