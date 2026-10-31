"""Unit tests for environment detection, project root discovery, and multi-method discovery."""

import os
from pathlib import Path
import shutil
import subprocess
from unittest.mock import MagicMock, patch
import pytest

from tes.adapters import get_adapter, get_all_adapters
from tes.config import find_project_root, get_user_home
from tes.detector import Detector
from tes.discovery import (
    ApplicationDiscoveryEngine,
    ApplicationSpec,
    DesktopDiscoveryProvider,
    PackageManagerDiscoveryProvider,
)
from tes.models import Scope


def test_executable_present_and_functional(monkeypatch):
    adapter = get_adapter("hermes")

    fake_exe = Path("/mock/bin/hermes")
    monkeypatch.setattr(adapter, "find_executable", lambda: fake_exe)
    monkeypatch.setattr(adapter, "find_desktop_application", lambda **k: (False, None, None, None))
    monkeypatch.setattr(adapter, "find_package_manager_application", lambda: (False, None, None))
    monkeypatch.setattr(adapter, "verify_version", lambda p: (True, "1.4.0"))

    status = adapter.detect_status()
    assert status.installed is True
    assert status.application_found is True
    assert status.installation_method == "CLI"
    assert status.executable_found is True
    assert status.version_verified is True
    assert status.version == "1.4.0"
    assert "Verified CLI installation" in status.details


def test_executable_present_but_version_check_fails(monkeypatch):
    adapter = get_adapter("claude-code")

    fake_exe = Path("/mock/bin/claude")
    monkeypatch.setattr(adapter, "find_executable", lambda: fake_exe)
    monkeypatch.setattr(adapter, "find_desktop_application", lambda **k: (False, None, None, None))
    monkeypatch.setattr(adapter, "find_package_manager_application", lambda: (False, None, None))
    monkeypatch.setattr(adapter, "verify_version", lambda p: (False, None))

    status = adapter.detect_status()
    assert status.installed is False
    assert status.application_found is False
    assert status.executable_found is True
    assert status.version_verified is False
    assert status.version is None
    assert "version verification failed" in status.details


def test_executable_missing(monkeypatch):
    adapter = get_adapter("hermes")
    monkeypatch.setattr(adapter, "find_executable", lambda: None)
    monkeypatch.setattr(adapter, "find_desktop_application", lambda **k: (False, None, None, None))
    monkeypatch.setattr(adapter, "find_package_manager_application", lambda: (False, None, None))
    monkeypatch.setattr(adapter, "check_config_present", lambda: False)
    monkeypatch.setattr(adapter, "check_skills_dir_present", lambda scope=None: False)

    status = adapter.detect_status()
    assert status.installed is False
    assert status.executable_found is False
    assert status.version_verified is False
    assert status.details == "Executable absent"


def test_configuration_exists_without_application(monkeypatch):
    adapter = get_adapter("opencode")
    monkeypatch.setattr(adapter, "find_executable", lambda: None)
    monkeypatch.setattr(adapter, "find_desktop_application", lambda **k: (False, None, None, None))
    monkeypatch.setattr(adapter, "find_package_manager_application", lambda: (False, None, None))
    monkeypatch.setattr(adapter, "check_config_present", lambda: True)
    monkeypatch.setattr(adapter, "check_skills_dir_present", lambda scope=None: False)

    status = adapter.detect_status()
    assert status.installed is False
    assert status.application_found is False
    assert status.executable_found is False
    assert status.config_present is True
    assert status.details == "Configuration present without application"


def test_skills_directory_exists_without_application(monkeypatch):
    adapter = get_adapter("codex")
    monkeypatch.setattr(adapter, "find_executable", lambda: None)
    monkeypatch.setattr(adapter, "find_desktop_application", lambda **k: (False, None, None, None))
    monkeypatch.setattr(adapter, "find_package_manager_application", lambda: (False, None, None))
    monkeypatch.setattr(adapter, "check_config_present", lambda: False)
    monkeypatch.setattr(adapter, "check_skills_dir_present", lambda scope=None: True)

    status = adapter.detect_status()
    # Directory existence alone MUST NOT imply application installation
    assert status.installed is False
    assert status.application_found is False
    assert status.skills_directory_present is True


def test_generic_agent_skills_is_distribution_target_not_application():
    adapter = get_adapter("generic")
    status = adapter.detect_status()

    # Generic is a target, not a runnable application
    assert status.installed is False
    assert status.application_found is False
    assert status.executable_found is False
    assert status.version_verified is False
    assert status.available is True
    assert "Distribution target" in status.details


def test_home_directory_not_treated_as_project():
    # Ensure home directory is never automatically classified as a project root
    home = get_user_home()
    detected_root = find_project_root(start_dir=home)
    assert detected_root is None


def test_actual_project_detection(tmp_path: Path):
    # Test markers: .git, pyproject.toml, package.json, Cargo.toml, go.mod, composer.json, requirements.txt
    markers = [".git", "pyproject.toml", "package.json", "Cargo.toml", "go.mod", "composer.json", "requirements.txt"]

    for marker in markers:
        proj_dir = tmp_path / f"proj_{marker.replace('.', '_')}"
        nested_dir = proj_dir / "src" / "deep"
        nested_dir.mkdir(parents=True)

        if marker == ".git":
            (proj_dir / marker).mkdir()
        else:
            (proj_dir / marker).write_text("marker content", encoding="utf-8")

        detected = find_project_root(start_dir=nested_dir)
        assert detected == proj_dir, f"Failed to detect project with marker '{marker}'"


def test_explicit_project_path(tmp_path: Path):
    explicit_proj = tmp_path / "custom-project"
    explicit_proj.mkdir()

    report = Detector.detect_environments(project_root=explicit_proj)
    assert report.project_root == str(explicit_proj)


def test_read_only_detection(tmp_path: Path):
    empty_workspace = tmp_path / "clean-sandbox"
    empty_workspace.mkdir()

    report = Detector.detect_environments(project_root=empty_workspace)
    assert report is not None

    # Verify no agent directories were created in the clean workspace
    agent_dirs = [".hermes", ".claude", ".codex", ".gemini", ".agents", ".opencode"]
    for adir in agent_dirs:
        assert not (empty_workspace / adir).exists(), f"Detection created directory '{adir}' in workspace!"


# ==============================================================================
# OpenCode Priority Cases & Multi-Method Discovery Tests
# ==============================================================================


def test_opencode_desktop_found_cli_missing(monkeypatch):
    """Case A: Desktop found, CLI missing -> application_found=True, executable_found=False."""
    adapter = get_adapter("opencode")
    fake_launcher = Path("/usr/share/applications/ai.opencode.desktop")
    fake_bin = Path("/opt/OpenCode/ai.opencode")

    monkeypatch.setattr(adapter, "find_executable", lambda: None)
    monkeypatch.setattr(
        adapter, "find_desktop_application", lambda **k: (True, fake_launcher, fake_bin, "2.2.0")
    )
    monkeypatch.setattr(adapter, "find_package_manager_application", lambda: (False, None, None))

    status = adapter.detect_status()
    assert status.application_found is True
    assert status.installed is True
    assert status.executable_found is False
    assert status.installation_method == "Desktop"
    assert status.version == "2.2.0"
    assert status.application_path == str(fake_bin)
    assert status.executable_path is None
    assert "Verified Desktop application" in status.details


def test_opencode_cli_found_desktop_missing(monkeypatch):
    """Case B: CLI found, desktop missing -> application_found=True, executable_found=True."""
    adapter = get_adapter("opencode")
    fake_cli = Path("/usr/local/bin/opencode")

    monkeypatch.setattr(adapter, "find_executable", lambda: fake_cli)
    monkeypatch.setattr(adapter, "verify_version", lambda p: (True, "2.1.0"))
    monkeypatch.setattr(adapter, "find_desktop_application", lambda **k: (False, None, None, None))
    monkeypatch.setattr(adapter, "find_package_manager_application", lambda: (False, None, None))

    status = adapter.detect_status()
    assert status.application_found is True
    assert status.installed is True
    assert status.executable_found is True
    assert status.installation_method == "CLI"
    assert status.version == "2.1.0"
    assert "Verified CLI installation" in status.details


def test_opencode_both_desktop_and_cli_found(monkeypatch):
    """Case C: Both desktop and CLI found -> application_found=True, executable_found=True."""
    adapter = get_adapter("opencode")
    fake_cli = Path("/usr/local/bin/opencode")
    fake_launcher = Path("/usr/share/applications/ai.opencode.desktop")
    fake_bin = Path("/opt/OpenCode/ai.opencode")

    monkeypatch.setattr(adapter, "find_executable", lambda: fake_cli)
    monkeypatch.setattr(adapter, "verify_version", lambda p: (True, "2.2.0"))
    monkeypatch.setattr(
        adapter, "find_desktop_application", lambda **k: (True, fake_launcher, fake_bin, "2.2.0")
    )
    monkeypatch.setattr(adapter, "find_package_manager_application", lambda: (False, None, None))

    status = adapter.detect_status()
    assert status.application_found is True
    assert status.installed is True
    assert status.executable_found is True
    assert status.installation_method == "Desktop, CLI"
    assert status.version == "2.2.0"
    assert "Verified Desktop & CLI installation" in status.details


def test_opencode_config_only(monkeypatch):
    """Case D: Config only -> application_found=False."""
    adapter = get_adapter("opencode")
    monkeypatch.setattr(adapter, "find_executable", lambda: None)
    monkeypatch.setattr(adapter, "find_desktop_application", lambda **k: (False, None, None, None))
    monkeypatch.setattr(adapter, "find_package_manager_application", lambda: (False, None, None))
    monkeypatch.setattr(adapter, "check_config_present", lambda: True)
    monkeypatch.setattr(adapter, "check_skills_dir_present", lambda scope=None: False)

    status = adapter.detect_status()
    assert status.application_found is False
    assert status.installed is False
    assert status.config_present is True


def test_opencode_skills_dir_only(monkeypatch):
    """Case E: Skills directory only -> application_found=False."""
    adapter = get_adapter("opencode")
    monkeypatch.setattr(adapter, "find_executable", lambda: None)
    monkeypatch.setattr(adapter, "find_desktop_application", lambda **k: (False, None, None, None))
    monkeypatch.setattr(adapter, "find_package_manager_application", lambda: (False, None, None))
    monkeypatch.setattr(adapter, "check_config_present", lambda: False)
    monkeypatch.setattr(adapter, "check_skills_dir_present", lambda scope=None: True)

    status = adapter.detect_status()
    assert status.application_found is False
    assert status.installed is False
    assert status.skills_directory_present is True


def test_opencode_neither_installed(monkeypatch):
    """Case F: Neither installed -> application_found=False."""
    adapter = get_adapter("opencode")
    monkeypatch.setattr(adapter, "find_executable", lambda: None)
    monkeypatch.setattr(adapter, "find_desktop_application", lambda **k: (False, None, None, None))
    monkeypatch.setattr(adapter, "find_package_manager_application", lambda: (False, None, None))
    monkeypatch.setattr(adapter, "check_config_present", lambda: False)
    monkeypatch.setattr(adapter, "check_skills_dir_present", lambda scope=None: False)

    status = adapter.detect_status()
    assert status.application_found is False
    assert status.installed is False
    assert status.executable_found is False


def test_package_manager_application_installed(monkeypatch):
    """Application installed via package manager (e.g. dpkg) with no CLI on PATH."""
    adapter = get_adapter("hermes")
    monkeypatch.setattr(adapter, "find_executable", lambda: None)
    monkeypatch.setattr(adapter, "find_desktop_application", lambda **k: (False, None, None, None))
    monkeypatch.setattr(adapter, "find_package_manager_application", lambda: (True, "dpkg", "1.0.5"))

    status = adapter.detect_status()
    assert status.application_found is True
    assert status.installed is True
    assert status.executable_found is False
    assert status.installation_method == "Package Manager"
    assert status.version == "1.0.5"
    assert "Verified dpkg package installation" in status.details


def test_desktop_discovery_invalid_launcher_ignored(tmp_path: Path):
    """Invalid desktop launcher ignored when Exec= points to non-existent file."""
    desktop_dir = tmp_path / "applications"
    desktop_dir.mkdir()

    launcher = desktop_dir / "opencode.desktop"
    launcher.write_text(
        """[Desktop Entry]
Name=OpenCode
Exec=/nonexistent/binary/opencode-nonexistent --flag
Type=Application
""",
        encoding="utf-8",
    )

    spec = ApplicationSpec(
        adapter_id="opencode",
        display_name="OpenCode",
        desktop_names=["OpenCode"],
        desktop_file_patterns=["*opencode*.desktop"],
    )

    found, l_path, bin_path, ver = DesktopDiscoveryProvider.discover(
        spec, desktop_search_dirs=[desktop_dir]
    )
    assert found is False
    assert bin_path is None


def test_desktop_discovery_valid_launcher(tmp_path: Path):
    """Valid desktop launcher correctly detected with executable and version."""
    desktop_dir = tmp_path / "applications"
    desktop_dir.mkdir()

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_bin = bin_dir / "test-opencode"
    fake_bin.write_text("#!/bin/sh\necho test", encoding="utf-8")
    fake_bin.chmod(0o755)

    launcher = desktop_dir / "opencode.desktop"
    launcher.write_text(
        f"""[Desktop Entry]
Name=OpenCode
Exec={fake_bin} %U
Version=2.5.0
Type=Application
""",
        encoding="utf-8",
    )

    spec = ApplicationSpec(
        adapter_id="opencode",
        display_name="OpenCode",
        desktop_names=["OpenCode"],
        desktop_file_patterns=["*opencode*.desktop"],
    )

    found, l_path, bin_path, ver = DesktopDiscoveryProvider.discover(
        spec, desktop_search_dirs=[desktop_dir]
    )
    assert found is True
    assert l_path == launcher
    assert bin_path == fake_bin.resolve()
    assert ver == "2.5.0"


def test_package_manager_discovery_handled_gracefully(monkeypatch):
    """PackageManagerDiscoveryProvider handles missing package manager tools without crashing."""
    monkeypatch.setattr(shutil, "which", lambda cmd: None)

    spec = ApplicationSpec(
        adapter_id="opencode",
        display_name="OpenCode",
        package_names=["opencode"],
    )
    found, manager, ver = PackageManagerDiscoveryProvider.discover(spec)
    assert found is False
    assert manager is None
    assert ver is None


def test_host_opencode_real_detection():
    """Live environment verification on host system (Kali Linux): OpenCode desktop discovered."""
    adapter = get_adapter("opencode")
    status = adapter.detect_status()

    # The host has OpenCode installed via Desktop (/opt/OpenCode/ai.opencode)
    assert status.application_found is True
    assert status.installed is True
    assert "Desktop" in status.installation_method
    assert status.version is not None
