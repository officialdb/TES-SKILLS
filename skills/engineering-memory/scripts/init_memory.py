#!/usr/bin/env python3
"""Initialize a local-first .engineering/ memory directory in a target project."""

import sys
from pathlib import Path


def init_memory(target_dir: Path) -> Path:
    eng_dir = target_dir / ".engineering"
    eng_dir.mkdir(parents=True, exist_ok=True)
    (eng_dir / "decisions").mkdir(exist_ok=True)
    (eng_dir / "lessons").mkdir(exist_ok=True)
    (eng_dir / "tasks").mkdir(exist_ok=True)

    files = {
        "project-profile.md": (
            "# Project Profile\n\n"
            "- **Project Name:** \n"
            "- **Description:** \n"
            "- **Primary Stack:** \n"
            "- **Repository URL:** \n"
        ),
        "architecture.md": (
            "# Architecture Overview\n\n"
            "## High-Level Topology\n\n"
            "## Module Boundaries\n\n"
            "## Data Flow\n"
        ),
        "engineering-standards.md": (
            "# Engineering Standards\n\n"
            "## Code Conventions\n\n"
            "## Testing Policy\n\n"
            "## Error Handling\n"
        ),
        "design-standards.md": (
            "# Design Standards\n\n"
            "## Visual Direction\n\n"
            "## Typography & Spacing\n\n"
            "## Accessibility\n"
        ),
        "security-profile.md": (
            "# Security Profile\n\n"
            "## Trust Boundaries\n\n"
            "## Authentication & Authorization\n\n"
            "## Secrets Management\n"
        ),
    }

    for fname, content in files.items():
        fpath = eng_dir / fname
        if not fpath.exists():
            fpath.write_text(content, encoding="utf-8")

    return eng_dir


def main():
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    res = init_memory(target)
    print(f"Initialized engineering memory directory at: {res}")


if __name__ == "__main__":
    main()
