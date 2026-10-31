"""Adapter for Gemini CLI and Antigravity."""

import shutil
from pathlib import Path
from tes.adapters.base import BaseAdapter
from tes.config import get_user_home


class GeminiCliAdapter(BaseAdapter):
    """Integrates TES skills into Gemini CLI environments."""

    name = "Gemini CLI"
    target_id = "gemini-cli"
    default_project_rel_path = ".gemini/skills"
    default_global_rel_path = ".gemini/config/skills"

    def detect(self) -> bool:
        if shutil.which("gemini") is not None:
            return True
        gemini_home = get_user_home() / ".gemini"
        return gemini_home.exists()
