# TES Architecture

## Overview

TES (**Techpronnet Engineering Skills**) is designed as a modular, local-first skill distribution architecture for autonomous AI coding agents.

```
+--------------------------------------------------------------------+
|                              TES CLI                               |
| (Typer + Rich + Pydantic + Security Engine + Manifest Manager)     |
+-------------------+--------------------+---------------------------+
                    |                    |
                    v                    v
         +--------------------+  +---------------------+
         | Registry & Bundles |  | Skills Repository   |
         | skills.yaml        |  | skills/<skill>/     |
         | bundles.yaml       |  | SKILL.md + assets   |
         +--------------------+  +---------------------+
                    |
                    v
         +---------------------------------------------+
         |               Adapter Layer                 |
         +------+--------+--------+--------+-----+-----+
                |        |        |        |     |     |
                v        v        v        v     v     v
              Hermes  OpenCode  Codex    Claude Gemini Generic
```

## Core Components

### 1. Registry Subsystem (`src/tes/registry.py`)
- Reads and parses `registry/skills.yaml` and `registry/bundles.yaml`.
- Validates skill and bundle schemas against Pydantic models.
- Provides search, inspect, and bundle resolution logic.

### 2. Adapter Layer (`src/tes/adapters/`)
- Abstract `BaseAdapter` interface defines:
  - `detect() -> bool`
  - `get_skill_dir(scope: Scope) -> Path`
  - `install_skill(skill_source: Path, skill_meta: SkillMetadata, scope: Scope) -> InstallResult`
  - `uninstall_skill(skill_id: str, scope: Scope) -> bool`
  - `list_installed(scope: Scope) -> List[InstalledSkill]`
  - `validate_target(scope: Scope) -> TargetHealth`
- Specialized adapters for each supported environment implement specific discovery and directory paths.

### 3. Manifest Subsystem (`.tes-manifest.json`)
- Every target directory retains a `.tes-manifest.json` file.
- Records installed skill IDs, versions, installation timestamps, installed files, and SHA-256 hashes.
- Enables safe uninstallation and collision prevention without risking user-owned files.

### 4. Security Subsystem (`src/tes/security.py`)
- Validates path bounds (prevents path traversal attacks like `../../etc/passwd`).
- Validates safe filenames and rejects dangerous extensions or links.
- Ensures no executable scripts are invoked during package operations.
