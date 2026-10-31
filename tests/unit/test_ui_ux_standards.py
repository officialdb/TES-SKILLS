"""Unit tests for website copy and visual presentation standards in ui-ux-standards and frontend-quality."""

from pathlib import Path
import pytest

from tes.adapters import get_adapter
from tes.analyzer import SkillAnalyzer
from tes.config import get_skills_source_dir
from tes.models import InstalledSkillManifest, Scope, TargetManifest
from tes.registry import Registry
from tes.updater import Updater
from tes.validator import parse_frontmatter


@pytest.fixture
def skills_dir() -> Path:
    return get_skills_source_dir()


def test_ui_ux_standards_prohibits_decorative_blinking_dots(skills_dir: Path):
    skill_file = skills_dir / "ui-ux-standards" / "SKILL.md"
    content = skill_file.read_text(encoding="utf-8")

    # Prohibits decorative animated / blinking / pulsing dots
    assert "No Decorative Animated Dots" in content
    assert "blinking" in content.lower()
    assert "pulsing" in content.lower()
    assert "cognitive distraction" in content.lower()

    # Checklist verification
    checklist_file = skills_dir / "ui-ux-standards" / "checklists" / "ui-ux-review-checklist.md"
    cl_content = checklist_file.read_text(encoding="utf-8")
    assert "blinking" in cl_content.lower() or "pulsing" in cl_content.lower()

    # Reference documentation verification
    ref_file = skills_dir / "ui-ux-standards" / "references" / "visual-design-principles.md"
    ref_content = ref_file.read_text(encoding="utf-8")
    assert "The Ban on Decorative Animated Dots" in ref_content
    assert "Cognitive Distraction" in ref_content
    assert "Alarm Mimicry" in ref_content


def test_ui_ux_standards_website_copy_avoids_em_dashes(skills_dir: Path):
    skill_file = skills_dir / "ui-ux-standards" / "SKILL.md"
    content = skill_file.read_text(encoding="utf-8")

    # Preference against em dashes in website copy
    assert "Avoid Em Dashes in Website Copy" in content
    assert "—" in content
    assert "Rewrite sentences naturally" in content or "naturally" in content

    # Contains concrete rewrite examples
    assert "Avoid:" in content
    assert "Prefer:" in content

    # Context boundary preserved: technical docs, code syntax, CLI flags exempt
    assert "Technical documentation" in content
    assert "exempt" in content

    # Tone standards
    assert "Authentic, Professional Tone" in content
    assert "jargon" in content.lower()

    # Checklist verification
    checklist_file = skills_dir / "ui-ux-standards" / "checklists" / "ui-ux-review-checklist.md"
    cl_content = checklist_file.read_text(encoding="utf-8")
    assert "em dashes" in cl_content.lower()


def test_frontend_quality_css_motion_and_copy_auditing(skills_dir: Path):
    skill_file = skills_dir / "frontend-quality" / "SKILL.md"
    content = skill_file.read_text(encoding="utf-8")

    # CSS motion hygiene prohibiting decorative keyframe animations
    assert "CSS Motion Hygiene" in content
    assert "keyframes" in content.lower()
    assert "pulse" in content.lower() or "blink" in content.lower()
    assert "prefers-reduced-motion" in content

    # Status indicators must bind to reactive state
    assert "reactive state" in content.lower()

    # Template string and copy auditing
    assert "Template String & Copy Auditing" in content
    assert "em dashes" in content.lower() or "—" in content

    # Checklist verification
    checklist_file = skills_dir / "frontend-quality" / "checklists" / "frontend-performance-checklist.md"
    cl_content = checklist_file.read_text(encoding="utf-8")
    assert "pulse" in cl_content.lower() or "blink" in cl_content.lower()
    assert "em dashes" in cl_content.lower() or "—" in cl_content


def test_functional_status_indicators_remain_permitted(skills_dir: Path):
    ui_content = (skills_dir / "ui-ux-standards" / "SKILL.md").read_text(encoding="utf-8")
    fq_content = (skills_dir / "frontend-quality" / "SKILL.md").read_text(encoding="utf-8")

    # Both skills explicitly permit functional indicators communicating genuine live system state
    assert "Functional Indicators Permitted" in ui_content
    assert "Functional loading, connection, and status indicators remain permitted" in ui_content
    assert "reactive state" in fq_content.lower()


def test_no_duplicate_instruction_blocks_between_ui_skills():
    analyzer = SkillAnalyzer()
    cat_report = analyzer.analyze_catalogue()
    # Ensure no 15+ normalized word duplicate blocks were introduced
    assert len(cat_report.potential_duplicates) == 0, f"Duplicate blocks found: {cat_report.potential_duplicates}"


def test_skills_versioned_at_1_0_1(loaded_registry: Registry, skills_dir: Path):
    """Verify ui-ux-standards and frontend-quality are versioned at 1.0.1 in registry and frontmatter."""
    ui_meta = loaded_registry.get_skill("ui-ux-standards")
    fq_meta = loaded_registry.get_skill("frontend-quality")

    assert ui_meta is not None
    assert ui_meta.version == "1.0.1"

    assert fq_meta is not None
    assert fq_meta.version == "1.0.1"

    # Verify unrelated skills remain at 1.0.0
    for sid in ["engineering-core", "software-engineering", "security-audit", "devops-engineering"]:
        assert loaded_registry.get_skill(sid).version == "1.0.0"

    # Verify frontmatter version fields
    ui_fm, _, _ = parse_frontmatter((skills_dir / "ui-ux-standards" / "SKILL.md").read_text(encoding="utf-8"))
    fq_fm, _, _ = parse_frontmatter((skills_dir / "frontend-quality" / "SKILL.md").read_text(encoding="utf-8"))

    assert str(ui_fm.get("version")) == "1.0.1"
    assert str(fq_fm.get("version")) == "1.0.1"


def test_update_mechanism_identifies_1_0_1_as_newer(temp_project: Path, loaded_registry: Registry):
    """Verify TES update mechanism identifies 1.0.1 as an available update over installed 1.0.0."""
    adapter = get_adapter("opencode")
    manifest = TargetManifest(
        skills={
            "ui-ux-standards": InstalledSkillManifest(
                skill_id="ui-ux-standards",
                version="1.0.0",
                installed_at="2026-10-31T10:51:00Z",
                scope=Scope.PROJECT,
                target="opencode",
                managed_files=["SKILL.md"],
                hashes={"SKILL.md": "fakehash1"},
            ),
            "frontend-quality": InstalledSkillManifest(
                skill_id="frontend-quality",
                version="1.0.0",
                installed_at="2026-10-31T10:51:00Z",
                scope=Scope.PROJECT,
                target="opencode",
                managed_files=["SKILL.md"],
                hashes={"SKILL.md": "fakehash2"},
            ),
            "engineering-core": InstalledSkillManifest(
                skill_id="engineering-core",
                version="1.0.0",
                installed_at="2026-10-31T10:51:00Z",
                scope=Scope.PROJECT,
                target="opencode",
                managed_files=["SKILL.md"],
                hashes={"SKILL.md": "fakehash3"},
            ),
        }
    )
    adapter.write_manifest(manifest, Scope.PROJECT, temp_project)

    updater = Updater(adapter, loaded_registry, scope=Scope.PROJECT, project_root=temp_project)
    statuses = updater.check_updates()

    status_map = {s.skill_id: s for s in statuses}

    # ui-ux-standards update available (1.0.0 -> 1.0.1)
    assert status_map["ui-ux-standards"].update_available is True
    assert status_map["ui-ux-standards"].installed_version == "1.0.0"
    assert status_map["ui-ux-standards"].latest_version == "1.0.1"

    # frontend-quality update available (1.0.0 -> 1.0.1)
    assert status_map["frontend-quality"].update_available is True
    assert status_map["frontend-quality"].installed_version == "1.0.0"
    assert status_map["frontend-quality"].latest_version == "1.0.1"

    # engineering-core is up to date (1.0.0 == 1.0.0)
    assert status_map["engineering-core"].update_available is False
    assert status_map["engineering-core"].installed_version == "1.0.0"
    assert status_map["engineering-core"].latest_version == "1.0.0"

