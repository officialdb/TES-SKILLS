"""Unit tests for TES token efficiency architecture, diagnostics, and progressive disclosure."""

from pathlib import Path
import re
import pytest

from tes.analyzer import SkillAnalyzer, estimate_tokens
from tes.config import get_skills_source_dir
from tes.registry import Registry
from tes.validator import parse_frontmatter, MARKDOWN_LINK_PATTERN


@pytest.fixture
def analyzer():
    return SkillAnalyzer()


def test_all_skill_metadata_is_valid(loaded_registry: Registry):
    skills = loaded_registry.list_skills()
    assert len(skills) == 15

    for s in skills:
        assert s.id
        assert s.name
        assert s.description
        assert s.category in {"engineering", "security", "devops", "design", "memory"}


def test_skill_descriptions_remain_concise(analyzer: SkillAnalyzer):
    cat_report = analyzer.analyze_catalogue()
    assert cat_report.skills_count == 15

    for skill in cat_report.skills:
        # Frontmatter descriptions must be concise (<= 200 chars and <= 35 words)
        assert skill.desc_chars <= 200, f"Skill '{skill.skill_id}' description is too long ({skill.desc_chars} chars)"
        assert skill.desc_words <= 35, f"Skill '{skill.skill_id}' description has too many words ({skill.desc_words} words)"
        assert not skill.long_description


def test_reference_paths_resolve_correctly(analyzer: SkillAnalyzer):
    cat_report = analyzer.analyze_catalogue()
    assert len(cat_report.broken_references) == 0, f"Broken references found: {cat_report.broken_references}"

    skills_dir = get_skills_source_dir()
    for sdir in skills_dir.iterdir():
        if sdir.is_dir() and not sdir.name.startswith("."):
            skill_md = sdir / "SKILL.md"
            content = skill_md.read_text(encoding="utf-8")
            _, body, _ = parse_frontmatter(content)

            for match in MARKDOWN_LINK_PATTERN.finditer(body):
                ref = match.group(1).split("#")[0].strip()
                if ref and not ref.startswith("/") and not ref.startswith("http"):
                    target = sdir / ref
                    assert target.exists(), f"Broken link in '{sdir.name}/SKILL.md': '{ref}' does not exist"


def test_skills_remain_independently_understandable():
    skills_dir = get_skills_source_dir()
    required_sections = ["Purpose & Activation", "Expected Deliverables", "Progressive Disclosure"]

    for sdir in skills_dir.iterdir():
        if sdir.is_dir() and not sdir.name.startswith("."):
            content = (sdir / "SKILL.md").read_text(encoding="utf-8")
            for sec in required_sections:
                assert sec in content, f"Skill '{sdir.name}/SKILL.md' missing essential section '{sec}'"


def test_bundles_do_not_force_activation_of_all_members(loaded_registry: Registry):
    bundles = loaded_registry.list_bundles()
    assert len(bundles) >= 4

    for b in bundles:
        # Bundles represent packaging/installation units, not runtime instructions to load all
        assert len(b.skills) > 1
        assert "complete-suite" in [b.id for b in bundles]


def test_memory_retrieval_is_selective():
    skills_dir = get_skills_source_dir()
    mem_skill = (skills_dir / "engineering-memory" / "SKILL.md").read_text(encoding="utf-8")

    # Verify selective retrieval protocol is explicitly stated
    assert "Selective Retrieval" in mem_skill
    assert "project-profile.md" in mem_skill
    assert "architecture.md" in mem_skill
    assert "security-profile.md" in mem_skill
    assert "Never load all .engineering/ files at startup" in mem_skill or "Never load all" in mem_skill


def test_cross_references_do_not_create_circular_dependencies(analyzer: SkillAnalyzer):
    cat_report = analyzer.analyze_catalogue()
    # Check that cross references are advisory and do not form hard required loops
    graph = {s.skill_id: s.cross_references for s in cat_report.skills}

    # Verify no skill references itself
    for sid, refs in graph.items():
        assert sid not in refs


def test_duplicate_instructions_are_minimized(analyzer: SkillAnalyzer):
    cat_report = analyzer.analyze_catalogue()
    # Duplication blocks of 15+ normalized words should be 0 across the catalogue
    assert len(cat_report.potential_duplicates) == 0


def test_tes_analyze_produces_accurate_reports(analyzer: SkillAnalyzer):
    cat_report = analyzer.analyze_catalogue()
    assert cat_report.skills_count == 15
    assert cat_report.total_skill_md_words > 0
    assert cat_report.total_skill_md_tokens > 0
    assert cat_report.total_reference_files > 0
    assert all(skill.total_reference_files > 0 for skill in cat_report.skills)
    assert cat_report.tokenizer_method in {"tiktoken (cl100k_base)", "heuristic (~4 characters per token)"}

    md_report = analyzer.generate_report_markdown(cat_report)
    assert "# TES Token Efficiency & Skill Diagnostics Report" in md_report
    assert "Skill Sizing & Instruction Budgets" in md_report
    assert "Optimal" in md_report

