"""Unit tests for the backend-engineering skill, its assets, and bundle integrations."""

from pathlib import Path
import pytest

from tes.adapters import get_adapter
from tes.config import get_skills_source_dir
from tes.installer import Installer
from tes.models import Scope
from tes.registry import Registry
from tes.uninstaller import Uninstaller
from tes.validator import MARKDOWN_LINK_PATTERN, parse_frontmatter


@pytest.fixture
def skills_dir() -> Path:
    return get_skills_source_dir()


def test_backend_engineering_metadata(loaded_registry: Registry, skills_dir: Path):
    skill = loaded_registry.get_skill("backend-engineering")
    assert skill is not None
    assert skill.id == "backend-engineering"
    assert skill.name == "Backend Engineering"
    assert skill.version == "1.0.0"
    assert skill.category == "engineering"
    for tag in ["backend", "api", "architecture", "business-logic", "persistence", "security", "services"]:
        assert tag in skill.tags

    # Frontmatter check
    skill_file = skills_dir / "backend-engineering" / "SKILL.md"
    assert skill_file.exists()
    fm, body, err = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
    assert err is None
    assert fm["name"] == "backend-engineering"
    assert str(fm.get("version")) == "1.0.0"


def test_backend_engineering_bundle_membership(loaded_registry: Registry):
    bundles = {b.id: b.skills for b in loaded_registry.list_bundles()}
    assert "backend-engineering" in bundles["engineering-suite"]
    assert "backend-engineering" in bundles["complete-suite"]


def test_backend_engineering_all_references_exist(skills_dir: Path):
    skill_dir = skills_dir / "backend-engineering"
    skill_md = skill_dir / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8")
    _, body, _ = parse_frontmatter(content)

    links = []
    for match in MARKDOWN_LINK_PATTERN.finditer(body):
        ref = match.group(1).split("#")[0].strip()
        if ref and not ref.startswith("http"):
            links.append(ref)

    assert len(links) == 14
    for link in links:
        target = skill_dir / link
        assert target.exists(), f"Linked file does not exist: {link}"
        assert target.is_file()


def test_backend_engineering_domain_coverage(skills_dir: Path):
    skill_dir = skills_dir / "backend-engineering"
    skill_md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

    # Ecosystem coverage
    for ecosystem in ["Python", "FastAPI", "Django", "PHP", "Laravel", "Node.js", "NestJS", "Java", "Spring Boot"]:
        assert ecosystem in skill_md

    # Core disciplines
    for discipline in ["Architecture", "Request Lifecycle", "Authentication & Authorization", "Persistence", "Background Queues", "Logging"]:
        assert discipline in skill_md


def test_backend_engineering_security_standards(skills_dir: Path):
    sec_ref = (skills_dir / "backend-engineering" / "references" / "backend-security.md").read_text(encoding="utf-8")
    for threat in ["SQL Injection", "SSRF", "IDOR", "Mass Assignment", "Rate Limiting", "Secrets Management"]:
        assert threat in sec_ref


def test_backend_engineering_installation_and_uninstallation(temp_project: Path, loaded_registry: Registry):
    adapter = get_adapter("opencode")
    installer = Installer(adapter, scope=Scope.PROJECT, project_root=temp_project)
    uninstaller = Uninstaller(adapter, scope=Scope.PROJECT, project_root=temp_project)

    skill_meta = loaded_registry.get_skill("backend-engineering")
    source_dir = loaded_registry.get_skill_source_path(skill_meta)

    # 1. Install
    record = installer.install_skill(skill_meta, source_dir)
    assert record.skill_id == "backend-engineering"
    assert record.version == "1.0.0"
    assert "SKILL.md" in record.managed_files
    assert len(record.managed_files) == 15  # SKILL.md + 14 assets

    # Check manifest
    manifest = adapter.read_manifest(Scope.PROJECT, temp_project)
    assert "backend-engineering" in manifest.skills
    assert manifest.skills["backend-engineering"].version == "1.0.0"

    # 2. Uninstall
    success = uninstaller.uninstall_skill("backend-engineering")
    assert success is True

    manifest_after = adapter.read_manifest(Scope.PROJECT, temp_project)
    assert "backend-engineering" not in manifest_after.skills

