"""Registry loader and query engine for TES."""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml

from tes.config import get_registry_dir, get_skills_source_dir
from tes.models import BundleMetadata, SkillMetadata


class Registry:
    """Manages the catalogue of available skills and bundles."""

    def __init__(self, registry_dir: Optional[Path] = None, skills_source_dir: Optional[Path] = None):
        self.registry_dir = registry_dir or get_registry_dir()
        self.skills_source_dir = skills_source_dir or get_skills_source_dir()
        self._skills: Dict[str, SkillMetadata] = {}
        self._bundles: Dict[str, BundleMetadata] = {}
        self._loaded = False

    def load(self) -> None:
        """Load skills and bundles from registry YAML files."""
        skills_file = self.registry_dir / "skills.yaml"
        bundles_file = self.registry_dir / "bundles.yaml"

        if not skills_file.exists():
            raise FileNotFoundError(f"Skills registry file not found: {skills_file}")
        if not bundles_file.exists():
            raise FileNotFoundError(f"Bundles registry file not found: {bundles_file}")

        with open(skills_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            skills_list = data.get("skills", [])
            for s in skills_list:
                meta = SkillMetadata(**s)
                self._skills[meta.id] = meta

        with open(bundles_file, "r", encoding="utf-8") as f:
            bdata = yaml.safe_load(f) or {}
            bundles_list = bdata.get("bundles", [])
            for b in bundles_list:
                bmeta = BundleMetadata(**b)
                self._bundles[bmeta.id] = bmeta

        self._loaded = True

    def _ensure_loaded(self) -> None:
        if not self._loaded:
            self.load()

    def get_skill(self, skill_id: str) -> Optional[SkillMetadata]:
        self._ensure_loaded()
        return self._skills.get(skill_id)

    def get_bundle(self, bundle_id: str) -> Optional[BundleMetadata]:
        self._ensure_loaded()
        return self._bundles.get(bundle_id)

    def list_skills(self) -> List[SkillMetadata]:
        self._ensure_loaded()
        return list(self._skills.values())

    def list_bundles(self) -> List[BundleMetadata]:
        self._ensure_loaded()
        return list(self._bundles.values())

    def search_skills(self, query: str = "", category: Optional[str] = None) -> List[SkillMetadata]:
        self._ensure_loaded()
        q = query.lower().strip()
        results = []
        for s in self._skills.values():
            if category and s.category.lower() != category.lower():
                continue
            if not q:
                results.append(s)
                continue
            if (
                q in s.id.lower()
                or q in s.name.lower()
                or q in s.description.lower()
                or any(q in tag.lower() for tag in s.tags)
            ):
                results.append(s)
        return results

    def resolve_skills_to_install(self, identifier: str) -> Tuple[List[SkillMetadata], Optional[str]]:
        """Resolve an identifier (skill ID or bundle ID) into a list of SkillMetadata objects.
        
        Returns:
            Tuple of (list of SkillMetadata, bundle_id if resolved from bundle else None)
        """
        self._ensure_loaded()
        # Check if bundle
        if identifier in self._bundles:
            bundle = self._bundles[identifier]
            resolved = []
            for sid in bundle.skills:
                skill = self.get_skill(sid)
                if not skill:
                    raise ValueError(f"Bundle '{identifier}' references unknown skill '{sid}'")
                resolved.append(skill)
            return resolved, bundle.id

        # Check if skill
        if identifier in self._skills:
            return [self._skills[identifier]], None

        raise ValueError(
            f"'{identifier}' is neither a recognized skill nor a bundle. "
            f"Run 'tes search' to list available skills."
        )

    def get_skill_source_path(self, skill: SkillMetadata) -> Path:
        """Resolve the local filesystem directory containing the skill source."""
        if skill.path:
            p = self.registry_dir.parent / skill.path
            if p.exists():
                return p.resolve()
        # Fallback to skills_source_dir / skill.id
        fallback = self.skills_source_dir / skill.id
        return fallback.resolve()
