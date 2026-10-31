"""Configuration and path resolution for TES."""

import os
from pathlib import Path
from typing import Optional

MANIFEST_FILE_NAME = ".tes-manifest.json"

PROJECT_MARKERS = [
    ".git",
    "pyproject.toml",
    "package.json",
    "Cargo.toml",
    "go.mod",
    "composer.json",
    "requirements.txt",
]


def get_user_home() -> Path:
    """Return user home directory."""
    return Path.home().resolve()


def find_project_root(start_dir: Optional[Path] = None, allow_home: bool = False) -> Optional[Path]:
    """Find the root of the current project by walking upwards.
    
    Checks for recognized project markers:
    .git, pyproject.toml, package.json, Cargo.toml, go.mod, composer.json, requirements.txt.
    
    The user's home directory is never automatically classified as a project root.
    Returns None if no project root marker is found.
    """
    current = (start_dir or Path.cwd()).resolve()
    home = get_user_home()

    candidate = current
    while True:
        # The home directory must not automatically be classified as a project
        if candidate == home and not allow_home:
            break

        for marker in PROJECT_MARKERS:
            if (candidate / marker).exists():
                return candidate

        if candidate.parent == candidate:
            break
        candidate = candidate.parent

    return None


def get_tes_package_root() -> Path:
    """Return the root directory of the TES installation or repository."""
    # First check env var override
    env_root = os.getenv("TES_ROOT")
    if env_root and Path(env_root).exists():
        return Path(env_root).resolve()

    # Next check if we are running in repo (e.g. src/tes/config.py -> ../../)
    candidate = Path(__file__).resolve().parent.parent.parent
    if (candidate / "registry" / "skills.yaml").exists():
        return candidate

    # Fallback to current working directory if registry exists there
    cwd_candidate = Path.cwd().resolve()
    if (cwd_candidate / "registry" / "skills.yaml").exists():
        return cwd_candidate

    return candidate


def get_registry_dir() -> Path:
    """Return the registry directory containing skills.yaml and bundles.yaml."""
    return get_tes_package_root() / "registry"


def get_skills_source_dir() -> Path:
    """Return the directory containing skill sources."""
    return get_tes_package_root() / "skills"
