"""Safe uninstaller for TES skills."""

import os
from pathlib import Path
import shutil
from typing import Optional

from tes.adapters import BaseAdapter
from tes.models import Scope
from tes.security import resolve_safe_path


class UninstallationError(Exception):
    """Raised when skill uninstallation fails."""
    pass


class UnmanagedSkillError(UninstallationError):
    """Raised when attempting to uninstall a skill not managed by TES."""
    pass


class Uninstaller:
    """Safely uninstalls TES skills while protecting user-owned files."""

    def __init__(self, adapter: BaseAdapter, scope: Scope = Scope.PROJECT, project_root: Optional[Path] = None):
        self.adapter = adapter
        self.scope = scope
        self.project_root = project_root

    def uninstall_skill(self, skill_id: str) -> bool:
        """Uninstall a TES-managed skill.
        
        Guarantees:
        - Refuses to delete skills not tracked in the TES manifest.
        - Preserves any files created by the user inside the skill directory.
        - Cleans up empty directories and updates manifest atomically.
        """
        dest_base = self.adapter.get_skill_dir(self.scope, self.project_root)
        manifest = self.adapter.read_manifest(self.scope, self.project_root)

        skill_dir = resolve_safe_path(dest_base, skill_id)

        # Check if skill is recorded in manifest
        if skill_id not in manifest.skills:
            if skill_dir.exists():
                raise UnmanagedSkillError(
                    f"Directory '{skill_dir}' exists but is not recorded in the TES manifest. "
                    "Refusing to delete unmanaged or user-owned skill."
                )
            return False

        record = manifest.skills[skill_id]

        # Delete only managed files
        if skill_dir.exists():
            for rel_str in record.managed_files:
                try:
                    fpath = resolve_safe_path(skill_dir, rel_str)
                    if fpath.exists() and fpath.is_file():
                        fpath.unlink()
                except Exception:
                    pass

            # Check if any user files remain
            remaining_files = []
            for root, _, files in os.walk(skill_dir):
                for f in files:
                    remaining_files.append(Path(root) / f)

            if not remaining_files:
                # Safe to remove empty directory
                shutil.rmtree(skill_dir, ignore_errors=True)

        # Remove from manifest
        del manifest.skills[skill_id]
        self.adapter.write_manifest(manifest, self.scope, self.project_root)

        return True
