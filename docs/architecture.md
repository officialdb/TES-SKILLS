# TES Architecture

## Overview

TES (**Techpronnet Engineering Skills**) is designed as a modular, local-first skill distribution architecture for autonomous AI coding agents.

```text
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
         |     Multi-Method Discovery Subsystem        |
         | (CLI + Desktop + Package Manager + Config)  |
         +---------------------------------------------+
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

### 1. Multi-Method Discovery Subsystem (`src/tes/discovery.py`)
- **Decoupled Application Discovery:** Discovers applications independently of whether their CLI executable is linked on `$PATH`.
- **Discovery Providers:**
  - `CLIDiscoveryProvider`: Searches system `$PATH` and known executable locations; validates version output safely.
  - `DesktopDiscoveryProvider`: Inspects standard Linux `.desktop` entries in `/usr/share/applications`, `~/.local/share/applications`, and Flatpak/Snap roots. Validates `Exec=` targets on disk without executing scripts. Checks `/opt` application bundles.
  - `PackageManagerDiscoveryProvider`: Safely queries `dpkg`, `rpm`, `flatpak`, and `snap` when installed.
- **Synthesized Evidence:** Emits an `EnvironmentStatus` with discrete properties: `application_found`, `installation_method`, `executable_found`, `version_verified`, `application_path`, `config_present`, `skills_directory_present`, and `available`.

### 2. Registry Subsystem (`src/tes/registry.py`)
- Reads and parses `registry/skills.yaml` and `registry/bundles.yaml`.
- Validates skill and bundle schemas against Pydantic models.
- Provides search, inspect, and bundle resolution logic.

### 3. Adapter Layer (`src/tes/adapters/`)
- Abstract `BaseAdapter` interface defines:
  - `detect_status() -> EnvironmentStatus`
  - `get_skill_dir(scope: Scope) -> Path`
  - `read_manifest(scope: Scope) -> TargetManifest`
  - `write_manifest(manifest: TargetManifest, scope: Scope) -> None`
  - `list_installed(scope: Scope) -> List[InstalledSkill]`
  - `validate_target(scope: Scope) -> TargetHealth`
- Specialized adapters for Hermes, OpenCode, Codex, Claude Code, Gemini CLI, and Generic Agent Skills.

### 4. Token Efficiency Subsystem (`src/tes/analyzer.py`)
- **Three-Level Progressive Disclosure:**
  - *Level 1 (Discovery Metadata):* Compact YAML frontmatter (<= 200 characters) containing identifier, description, and trigger hints.
  - *Level 2 (Core Instructions):* Structured, actionable `SKILL.md` documents (350–550 words) defining workflow, constraints, autonomy boundaries, and deliverables.
  - *Level 3 (Selective Reference Loading):* Deep reference manuals, checklists, and templates stored in subdirectories (`references/`, `checklists/`, `templates/`), loaded selectively by the agent only when required.
- **Diagnostic Engine (`tes analyze`):**
  - Audits skill instruction sizes, word counts, and approximate token counts via `tiktoken` (`cl100k_base`).
  - Identifies duplicate instruction blocks across skills.
  - Verifies local reference link integrity and flags overly verbose metadata.
- **Selective Engineering Memory (`.engineering/`):**
  - Local-first, offline architecture decision records and bug lessons.
  - Strict selective loading rules preventing full-directory context dumping into LLM prompts.

### 5. Security Subsystem (`src/tes/security.py`)
- Validates path bounds (prevents path traversal attacks like `../../etc/passwd`).
- Validates safe filenames and rejects dangerous extensions or links.
- Ensures no executable scripts are invoked during package operations.
