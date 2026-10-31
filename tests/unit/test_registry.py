"""Unit tests for registry and catalog queries."""

import pytest
from tes.registry import Registry


def test_registry_loading(loaded_registry: Registry):
    skills = loaded_registry.list_skills()
    bundles = loaded_registry.list_bundles()

    assert len(skills) == 15
    assert len(bundles) == 4


def test_get_individual_skill(loaded_registry: Registry):
    skill = loaded_registry.get_skill("engineering-core")
    assert skill is not None
    assert skill.name == "Engineering Core"
    assert skill.category == "engineering"
    assert "best-practices" in skill.tags


def test_search_skills_by_query_and_category(loaded_registry: Registry):
    # Query search
    security_results = loaded_registry.search_skills(query="security")
    assert len(security_results) >= 2
    assert any(s.id == "security-audit" for s in security_results)

    # Category search
    design_skills = loaded_registry.search_skills(category="design")
    assert len(design_skills) == 2
    assert {s.id for s in design_skills} == {"ui-ux-standards", "frontend-quality"}


def test_resolve_bundle_skills(loaded_registry: Registry):
    skills, bundle_id = loaded_registry.resolve_skills_to_install("security-suite")
    assert bundle_id == "security-suite"
    assert len(skills) == 3
    ids = [s.id for s in skills]
    assert "security-audit" in ids
    assert "secure-development" in ids
    assert "threat-modeling" in ids


def test_resolve_unknown_target_raises_error(loaded_registry: Registry):
    with pytest.raises(ValueError, match="neither a recognized skill nor a bundle"):
        loaded_registry.resolve_skills_to_install("nonexistent-skill-or-bundle")
