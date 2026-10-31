"""Adapter for Generic Agent Skills-compatible environments."""

from pathlib import Path
from tes.adapters.base import BaseAdapter
from tes.config import get_user_home


class GenericAdapter(BaseAdapter):
    """Integrates TES skills into generic open Agent Skills environments (~/.agents/skills)."""

    name = "Generic Agent Skills"
    target_id = "generic"
    default_project_rel_path = ".agents/skills"
    default_global_rel_path = ".agents/skills"

    def detect(self) -> bool:
        # Standard generic open agent directory exists or universal default
        agents_home = get_user_home() / ".agents"
        return agents_home.exists()
