"""Adapter for Hermes AI Agent."""

import shutil
from pathlib import Path
from tes.adapters.base import BaseAdapter
from tes.config import get_user_home


class HermesAdapter(BaseAdapter):
    """Integrates TES skills into Hermes coding agent environments."""

    name = "Hermes"
    target_id = "hermes"
    default_project_rel_path = ".hermes/skills"
    default_global_rel_path = ".hermes/skills"

    def detect(self) -> bool:
        # Check if hermes command is on PATH or ~/.hermes exists
        if shutil.which("hermes") is not None:
            return True
        global_hermes = get_user_home() / ".hermes"
        return global_hermes.exists()
