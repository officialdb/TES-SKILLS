"""Adapter for Generic Agent Skills-compatible environments."""

from pathlib import Path
from typing import Optional
from tes.adapters.base import BaseAdapter
from tes.config import get_user_home


class GenericAdapter(BaseAdapter):
    """Integrates TES skills into generic open Agent Skills environments (~/.agents/skills).
    
    Generic Agent Skills is a filesystem distribution target, not a standalone AI application.
    """

    name = "Generic Agent Skills"
    target_id = "generic"
    default_project_rel_path = ".agents/skills"
    default_global_rel_path = ".agents/skills"

    executable_name = None
    alternative_executables = []
    is_application = False

    def check_config_present(self) -> bool:
        """Generic targets do not have proprietary application configuration."""
        return False

    def check_skills_dir_present(self, scope=None, project_root: Optional[Path] = None) -> bool:
        """Check whether generic ~/.agents/skills directory exists."""
        agents_skills = get_user_home() / ".agents" / "skills"
        return agents_skills.exists() and agents_skills.is_dir()

    def check_project_config_present(self, project_root: Optional[Path] = None) -> bool:
        """Check whether project contains .agents/skills directory."""
        if not project_root or not project_root.exists():
            return False
        return (project_root / ".agents" / "skills").exists()
