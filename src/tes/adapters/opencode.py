"""Adapter for OpenCode AI Agent."""

import shutil
from pathlib import Path
from tes.adapters.base import BaseAdapter
from tes.config import get_user_home


class OpenCodeAdapter(BaseAdapter):
    """Integrates TES skills into OpenCode coding agent environments."""

    name = "OpenCode"
    target_id = "opencode"
    default_project_rel_path = ".opencode/skills"
    default_global_rel_path = ".config/opencode/skills"

    def detect(self) -> bool:
        if shutil.which("opencode") is not None or shutil.which("ai.opencode") is not None:
            return True
        config_dir = get_user_home() / ".config" / "opencode"
        return config_dir.exists()
