"""Safe atomic installer for TES skills and bundles."""

from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
from typing import Dict, List, Optional, Tuple

from tes.adapters import BaseAdapter
from tes.models import InstalledSkillManifest, Scope, SkillMetadata
from tes.security import compute_sha256, resolve_safe_path, SecurityException


class InstallationError(Exception):
    """Raised when skill installation fails."""
    pass


class SkillConflictError(InstallationError):
    """Raised when an existing unmanaged/user-owned skill would be overwritten."""
    pass


class Installer:
    """Orchestrates atomic, safe skill installations."""

    def __init__(self, adapter: BaseAdapter, scope: Scope = Scope.PROJECT, project_root: Optional[Path] = None):
        self.adapter = adapter
        self.scope = scope
        self.project_root = project_root

    def install_skill(
        self,
        skill_meta: SkillMetadata,
        source_dir: Path,
        force: bool = False
    ) -> InstalledSkillManifest:
        """Install an individual skill directory into the target environment.
        
        Guarantees:
        - Path traversal protection.
        - Preserves user-owned skills (detects unmanaged directory collisions).
        - Atomic file copy.
        - Manifest tracking with SHA-256 integrity digests.
        """
        if not source_dir.exists() or not source_dir.is_dir():
            raise InstallationError(f"Skill source directory not found: {source_dir}")

        dest_base = self.adapter.get_skill_dir(self.scope, self.project_root)
        dest_base.mkdir(parents=True, exist_ok=True)

        target_skill_dir = resolve_safe_path(dest_base, skill_meta.id)
        manifest = self.adapter.read_manifest(self.scope, self.project_root)

        # Conflict check: does the folder already exist without being in TES manifest?
        if target_skill_dir.exists() and skill_meta.id not in manifest.skills and not force:
            raise SkillConflictError(
                f"Directory '{target_skill_dir}' already exists and is not managed by TES. "
                "Aborting installation to prevent overwriting user-owned files. Use force=True to override."
            )

        # Atomic copy: stage files into temporary staging directory first
        staging_dir = resolve_safe_path(dest_base, f".staging_{skill_meta.id}_{os.getpid()}")
        if staging_dir.exists():
            shutil.rmtree(staging_dir)

        managed_rel_files: List[str] = []
        file_hashes: Dict[str, str] = {}

        try:
            staging_dir.mkdir(parents=True, exist_ok=True)

            # Copy all files from source_dir to staging_dir
            for root, _, files in os.walk(source_dir):
                for fname in files:
                    src_file = Path(root) / fname
                    rel_p = src_file.relative_to(source_dir)
                    dest_file = resolve_safe_path(staging_dir, rel_p)
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, dest_file)

                    rel_str = str(rel_p)
                    managed_rel_files.append(rel_str)
                    file_hashes[rel_str] = compute_sha256(dest_file)

            # If target exists and was previously managed, remove old target before moving
            backup_dir = None
            if target_skill_dir.exists():
                backup_dir = resolve_safe_path(dest_base, f".backup_{skill_meta.id}_{os.getpid()}")
                target_skill_dir.rename(backup_dir)

            # Move staging into target location
            staging_dir.rename(target_skill_dir)

            # Clean up backup
            if backup_dir and backup_dir.exists():
                shutil.rmtree(backup_dir, ignore_errors=True)

            # Update manifest
            record = InstalledSkillManifest(
                skill_id=skill_meta.id,
                version=skill_meta.version,
                installed_at=datetime.now(timezone.utc).isoformat(),
                scope=self.scope,
                target=self.adapter.target_id,
                managed_files=sorted(managed_rel_files),
                hashes=file_hashes
            )
            manifest.skills[skill_meta.id] = record
            self.adapter.write_manifest(manifest, self.scope, self.project_root)

            return record

        except Exception as e:
            # Cleanup staging on failure
            if staging_dir.exists():
                shutil.rmtree(staging_dir, ignore_errors=True)
            raise InstallationError(f"Failed to install '{skill_meta.id}': {e}") from e

    def install_multiple(
        self,
        skills_with_paths: List[Tuple[SkillMetadata, Path]],
        force: bool = False
    ) -> List[InstalledSkillManifest]:
        """Install a collection of skills (e.g. from a bundle)."""
        results = []
        for meta, path in skills_with_paths:
            rec = self.install_skill(meta, path, force=force)
            results.append(rec)
        return results
