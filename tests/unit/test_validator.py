"""Unit tests for the skill validation engine."""

from pathlib import Path
from tes.config import get_skills_source_dir
from tes.validator import SkillValidator, parse_frontmatter


def test_parse_valid_frontmatter():
    text = (
        "---\n"
        "name: test-skill\n"
        "description: This is a test skill for validation.\n"
        "---\n\n"
        "# Test Skill Body\n"
    )
    fm, body, err = parse_frontmatter(text)
    assert err is None
    assert fm["name"] == "test-skill"
    assert "Test Skill Body" in body


def test_parse_invalid_frontmatter():
    text = "name: no-delimiters\n"
    fm, body, err = parse_frontmatter(text)
    assert err is not None
    assert "Missing starting '---'" in err


def test_all_catalog_skills_pass_validation():
    skills_dir = get_skills_source_dir()
    for sdir in skills_dir.iterdir():
        if sdir.is_dir() and not sdir.name.startswith("."):
            result = SkillValidator.validate_skill_dir(sdir)
            assert result.valid is True, f"Skill '{sdir.name}' failed validation: {result.errors}"
            assert len(result.errors) == 0


def test_validate_invalid_skill_name(tmp_path: Path):
    bad_dir = tmp_path / "Bad_Name_With_Underscore"
    bad_dir.mkdir()
    (bad_dir / "SKILL.md").write_text(
        "---\n"
        "name: Bad_Name_With_Underscore\n"
        "description: Proper length description for validation.\n"
        "---\n\n# Body\n"
    )
    res = SkillValidator.validate_skill_dir(bad_dir)
    assert res.valid is False
    assert any("does not match required pattern" in e for e in res.errors)
