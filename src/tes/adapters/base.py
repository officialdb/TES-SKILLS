"""Abstract base adapter for AI coding agent environments."""

from abc import ABC, abstractmethod
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from tes.config import MANIFEST_FILE_NAME, find_project_root, get_user_home
from tes.models import InstalledSkillManifest, Scope, TargetManifest


class BaseAdapter(ABC):
    """Abstract base class that all environment adapters must implement."""

    name: str
    target_id: str
    default_project_rel_path: str
    default_global_rel_path: str

    @abstractmethod
    def detect(self) -> bool:
        """Detect whether this agent environment is installed or configured on the system."""
        pass

    def get_skill_dir(self, scope: Scope, project_root: Optional[Path] = None) -> Path:
        """Resolve the skill directory for the requested scope."""
        if scope == Scope.PROJECT:
            root = project_root or find_project_root()
            return (root / self.default_project_rel_path).resolve()
        else:
            return (get_user_home() / self.default_global_rel_path).resolve()

    def get_manifest_path(self, scope: Scope, project_root: Optional[Path] = None) -> Path:
        """Return the manifest file path for this target and scope."""
        return self.get_skill_dir(scope, project_root) / MANIFEST_FILE_NAME

    def read_manifest(self, scope: Scope, project_root: Optional[Path] = None) -> TargetManifest:
        """Read and parse the TES manifest in the target directory."""
        mpath = self.get_manifest_path(scope, project_root)
        if not mpath.exists():
            return TargetManifest()
        try:
            content = mpath.read_text(encoding="utf-8")
            return TargetManifest.model_validate_json(content)
        except Exception:
            return TargetManifest()

    def write_manifest(self, manifest: TargetManifest, scope: Scope, project_root: Optional[Path] = None) -> None:
        """Write the updated manifest atomically to the target directory."""
        skill_dir = self.get_skill_dir(scope, project_root)
        skill_dir.mkdir(parents=True, exist_ok=True)
        mpath = skill_dir / MANIFEST_FILE_NAME
        tmp_path = skill_dir / f"{MANIFEST_FILE_NAME}.tmp"
        tmp_path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
        tmp_path.replace(mpath)

    def list_installed(self, scope: Scope, project_root: Optional[Path] = None) -> List[InstalledSkillManifest]:
        """List all TES-managed skills recorded in this adapter's manifest."""
        manifest = self.read_manifest(scope, project_root)
        return list(manifest.skills.values())

    def validate_target(self, scope: Scope, project_root: Optional[Path] = None) -> Dict[str, Any]:
        """Verify write access and state of the target directory."""
        skill_dir = self.get_skill_dir(scope, project_root)
        writable = False
        try:
            skill_dir.mkdir(parents=True, exist_ok=True)
            test_file = skill_dir / ".tes_write_test"
            test_file.write_text("ok", encoding="utf-8")
            test_file.unlink()
            writable = True
        except Exception:
            writable = False

        manifest_exists = (skill_dir / MANIFEST_FILE_NAME).exists()
        managed_count = len(self.read_manifest(scope, project_root).skills)

        return {
            "adapter": self.target_id,
            "name": self.name,
            "scope": scope.value,
            "path": str(skill_dir),
            "exists": skill_dir.exists(),
            "writable": writable,
            "manifest_exists": manifest_exists,
            "managed_skills_count": managed_count,
        }
