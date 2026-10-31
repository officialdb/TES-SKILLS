"""Compatibility tests for all supported AI agent adapters."""

from pathlib import Path
from tes.adapters import get_adapter, get_all_adapters
from tes.models import InstalledSkillManifest, Scope, TargetManifest


def test_all_six_adapters_registered():
    adapters = get_all_adapters()
    adapter_ids = {a.target_id for a in adapters}
    expected = {"hermes", "opencode", "codex", "claude-code", "gemini-cli", "generic"}
    assert adapter_ids == expected


def test_adapter_aliases():
    assert get_adapter("claude").target_id == "claude-code"
    assert get_adapter("gemini").target_id == "gemini-cli"
    assert get_adapter("agent").target_id == "generic"


def test_adapter_directory_resolution(tmp_path: Path):
    proj_root = tmp_path / "mock-project"
    proj_root.mkdir()

    # Hermes
    hermes = get_adapter("hermes")
    assert hermes.get_skill_dir(Scope.PROJECT, proj_root) == (proj_root / ".hermes/skills").resolve()
    assert ".hermes/skills" in str(hermes.get_skill_dir(Scope.GLOBAL))

    # OpenCode
    opencode = get_adapter("opencode")
    assert opencode.get_skill_dir(Scope.PROJECT, proj_root) == (proj_root / ".opencode/skills").resolve()
    assert ".config/opencode/skills" in str(opencode.get_skill_dir(Scope.GLOBAL))

    # Codex
    codex = get_adapter("codex")
    assert codex.get_skill_dir(Scope.PROJECT, proj_root) == (proj_root / ".codex/skills").resolve()
    assert ".codex/skills" in str(codex.get_skill_dir(Scope.GLOBAL))

    # Claude Code
    claude = get_adapter("claude-code")
    assert claude.get_skill_dir(Scope.PROJECT, proj_root) == (proj_root / ".claude/skills").resolve()
    assert ".claude/skills" in str(claude.get_skill_dir(Scope.GLOBAL))

    # Gemini CLI
    gemini = get_adapter("gemini-cli")
    assert gemini.get_skill_dir(Scope.PROJECT, proj_root) == (proj_root / ".gemini/skills").resolve()
    assert ".gemini/config/skills" in str(gemini.get_skill_dir(Scope.GLOBAL))

    # Generic
    generic = get_adapter("generic")
    assert generic.get_skill_dir(Scope.PROJECT, proj_root) == (proj_root / ".agents/skills").resolve()
    assert ".agents/skills" in str(generic.get_skill_dir(Scope.GLOBAL))


def test_adapter_manifest_roundtrip(tmp_path: Path):
    proj_root = tmp_path / "mock-project"
    proj_root.mkdir()

    adapter = get_adapter("hermes")
    initial_manifest = adapter.read_manifest(Scope.PROJECT, proj_root)
    assert len(initial_manifest.skills) == 0

    # Write a test manifest record
    record = InstalledSkillManifest(
        skill_id="engineering-core",
        version="1.0.0",
        installed_at="2026-10-31T08:00:00Z",
        scope=Scope.PROJECT,
        target="hermes",
        managed_files=["SKILL.md"],
        hashes={"SKILL.md": "testhash123"}
    )
    manifest = TargetManifest(skills={"engineering-core": record})
    adapter.write_manifest(manifest, Scope.PROJECT, proj_root)

    # Read back and verify
    reloaded = adapter.read_manifest(Scope.PROJECT, proj_root)
    assert "engineering-core" in reloaded.skills
    assert reloaded.skills["engineering-core"].hashes["SKILL.md"] == "testhash123"
