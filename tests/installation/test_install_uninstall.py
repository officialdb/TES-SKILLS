"""Installation, update, and uninstallation lifecycle tests."""

from pathlib import Path
import pytest

from tes.adapters import get_adapter
from tes.installer import Installer, SkillConflictError
from tes.models import Scope
from tes.registry import Registry
from tes.uninstaller import Uninstaller, UnmanagedSkillError
from tes.updater import Updater


def test_install_individual_skill(temp_project: Path, loaded_registry: Registry):
    adapter = get_adapter("opencode")
    installer = Installer(adapter, scope=Scope.PROJECT, project_root=temp_project)

    skill_meta = loaded_registry.get_skill("engineering-core")
    source_dir = loaded_registry.get_skill_source_path(skill_meta)

    record = installer.install_skill(skill_meta, source_dir)
    assert record.skill_id == "engineering-core"
    assert "SKILL.md" in record.managed_files

    target_dir = adapter.get_skill_dir(Scope.PROJECT, temp_project) / "engineering-core"
    assert target_dir.exists()
    assert (target_dir / "SKILL.md").exists()

    # Verify manifest entry
    manifest = adapter.read_manifest(Scope.PROJECT, temp_project)
    assert "engineering-core" in manifest.skills


def test_install_conflict_protection_for_user_skills(temp_project: Path, loaded_registry: Registry):
    adapter = get_adapter("claude-code")
    skill_dir = adapter.get_skill_dir(Scope.PROJECT, temp_project) / "security-audit"
    skill_dir.mkdir(parents=True, exist_ok=True)
    # Create an unmanaged user file
    (skill_dir / "my_custom_notes.txt").write_text("User owned content", encoding="utf-8")

    installer = Installer(adapter, scope=Scope.PROJECT, project_root=temp_project)
    skill_meta = loaded_registry.get_skill("security-audit")
    source_dir = loaded_registry.get_skill_source_path(skill_meta)

    # Attempting to install without force must raise SkillConflictError
    with pytest.raises(SkillConflictError, match="already exists and is not managed by TES"):
        installer.install_skill(skill_meta, source_dir, force=False)

    # Verify user file was preserved
    assert (skill_dir / "my_custom_notes.txt").exists()


def test_install_bundle(temp_project: Path, loaded_registry: Registry):
    adapter = get_adapter("generic")
    installer = Installer(adapter, scope=Scope.PROJECT, project_root=temp_project)

    skills, bundle_id = loaded_registry.resolve_skills_to_install("release-suite")
    assert bundle_id == "release-suite"
    skills_with_paths = [(s, loaded_registry.get_skill_source_path(s)) for s in skills]

    records = installer.install_multiple(skills_with_paths)
    assert len(records) == 2
    installed_ids = {r.skill_id for r in records}
    assert installed_ids == {"devops-engineering", "deployment-verification"}


def test_safe_uninstallation_preserves_user_files(temp_project: Path, loaded_registry: Registry):
    adapter = get_adapter("hermes")
    installer = Installer(adapter, scope=Scope.PROJECT, project_root=temp_project)
    uninstaller = Uninstaller(adapter, scope=Scope.PROJECT, project_root=temp_project)

    skill_meta = loaded_registry.get_skill("testing-strategy")
    source_dir = loaded_registry.get_skill_source_path(skill_meta)

    # 1. Install
    installer.install_skill(skill_meta, source_dir)
    skill_dest = adapter.get_skill_dir(Scope.PROJECT, temp_project) / "testing-strategy"
    assert (skill_dest / "SKILL.md").exists()

    # 2. User adds custom file inside skill folder
    user_file = skill_dest / "my_custom_tests.py"
    user_file.write_text("# User custom file", encoding="utf-8")

    # 3. Uninstall
    success = uninstaller.uninstall_skill("testing-strategy")
    assert success is True

    # 4. Managed files are removed, but user file and directory are preserved
    assert not (skill_dest / "SKILL.md").exists()
    assert user_file.exists()

    # 5. Manifest no longer tracks the skill
    manifest = adapter.read_manifest(Scope.PROJECT, temp_project)
    assert "testing-strategy" not in manifest.skills


def test_uninstall_refuses_to_delete_unmanaged_skill(temp_project: Path):
    adapter = get_adapter("gemini-cli")
    uninstaller = Uninstaller(adapter, scope=Scope.PROJECT, project_root=temp_project)

    skill_dest = adapter.get_skill_dir(Scope.PROJECT, temp_project) / "user-custom-skill"
    skill_dest.mkdir(parents=True, exist_ok=True)
    (skill_dest / "SKILL.md").write_text("Custom user skill", encoding="utf-8")

    with pytest.raises(UnmanagedSkillError, match="not recorded in the TES manifest"):
        uninstaller.uninstall_skill("user-custom-skill")

    assert (skill_dest / "SKILL.md").exists()


def test_update_preview_and_apply(temp_project: Path, loaded_registry: Registry):
    adapter = get_adapter("codex")
    installer = Installer(adapter, scope=Scope.PROJECT, project_root=temp_project)
    updater = Updater(adapter, loaded_registry, scope=Scope.PROJECT, project_root=temp_project)

    skill_meta = loaded_registry.get_skill("engineering-core")
    source_dir = loaded_registry.get_skill_source_path(skill_meta)

    installer.install_skill(skill_meta, source_dir)

    # Preview update
    preview_res = updater.update_skill("engineering-core", preview=True)
    assert preview_res["preview"] is True

    # Check update status
    statuses = updater.check_updates("engineering-core")
    assert len(statuses) == 1
    assert statuses[0].skill_id == "engineering-core"
