"""Pytest configuration and shared test fixtures."""

from pathlib import Path
import pytest
from typer.testing import CliRunner

from tes.config import get_registry_dir, get_skills_source_dir
from tes.registry import Registry


@pytest.fixture
def runner():
    """Typer CLI test runner."""
    return CliRunner()


@pytest.fixture
def loaded_registry():
    """Loaded production registry."""
    reg = Registry(get_registry_dir(), get_skills_source_dir())
    reg.load()
    return reg


@pytest.fixture
def temp_project(tmp_path: Path):
    """Isolated project directory fixture."""
    proj = tmp_path / "my-project"
    proj.mkdir(parents=True, exist_ok=True)
    return proj
