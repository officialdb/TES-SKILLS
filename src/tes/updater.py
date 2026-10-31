"""Updater engine for TES skills."""

from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel

from tes.adapters import BaseAdapter
from tes.installer import Installer
from tes.models import InstalledSkillManifest, Scope, SkillMetadata
from tes.registry import Registry


class SkillUpdateStatus(BaseModel):
    skill_id: str
    installed_version: str
    latest_version: str
    update_available: bool
    scope: Scope
    target: str


class Updater:
    """Manages update checks and safe upgrades of installed skills."""

    def __init__(
        self,
        adapter: BaseAdapter,
        registry: Registry,
        scope: Scope = Scope.PROJECT,
        project_root: Optional[Path] = None
    ):
        self.adapter = adapter
        self.registry = registry
        self.scope = scope
        self.project_root = project_root

    def check_updates(self, skill_id: Optional[str] = None) -> List[SkillUpdateStatus]:
        """Check for available updates for installed skills."""
        manifest = self.adapter.read_manifest(self.scope, self.project_root)
        results = []

        to_check = [skill_id] if skill_id else list(manifest.skills.keys())

        for sid in to_check:
            if not sid or sid not in manifest.skills:
                continue
            installed_meta = manifest.skills[sid]
            registry_meta = self.registry.get_skill(sid)

            if not registry_meta:
                continue

            update_avail = installed_meta.version != registry_meta.version
            results.append(
                SkillUpdateStatus(
                    skill_id=sid,
                    installed_version=installed_meta.version,
                    latest_version=registry_meta.version,
                    update_available=update_avail,
                    scope=self.scope,
                    target=self.adapter.target_id
                )
            )

        return results

    def update_skill(
        self,
        skill_id: str,
        preview: bool = False
    ) -> Dict[str, any]:
        """Update a skill to the latest registry version."""
        manifest = self.adapter.read_manifest(self.scope, self.project_root)
        if skill_id not in manifest.skills:
            raise ValueError(f"Skill '{skill_id}' is not currently installed.")

        registry_meta = self.registry.get_skill(skill_id)
        if not registry_meta:
            raise ValueError(f"Skill '{skill_id}' not found in registry.")

        source_dir = self.registry.get_skill_source_path(registry_meta)

        if preview:
            return {
                "skill_id": skill_id,
                "current_version": manifest.skills[skill_id].version,
                "new_version": registry_meta.version,
                "preview": True,
                "action": "Will update files from registry source",
            }

        installer = Installer(self.adapter, self.scope, self.project_root)
        new_record = installer.install_skill(registry_meta, source_dir, force=True)

        return {
            "skill_id": skill_id,
            "previous_version": manifest.skills[skill_id].version,
            "new_version": new_record.version,
            "preview": False,
            "status": "updated",
        }
