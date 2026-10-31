"""Adapter for OpenAI Codex CLI."""

import shutil
from pathlib import Path
from tes.adapters.base import BaseAdapter
from tes.config import get_user_home


class CodexAdapter(BaseAdapter):
    """Integrates TES skills into OpenAI Codex CLI environments."""

    name = "OpenAI Codex CLI"
    target_id = "codex"
    default_project_rel_path = ".codex/skills"
    default_global_rel_path = ".codex/skills"

    def detect(self) -> bool:
        if shutil.which("codex") is not None:
            return True
        codex_home = get_user_home() / ".codex"
        return codex_home.exists()
