# TES Installation and Usage Guide

## Requirements
- Python 3.10+
- Linux (Ubuntu, Debian, Kali, Fedora, Arch), macOS, or Windows WSL2

## Installation

### User Installation via pipx (Recommended)
```bash
pipx install techpronnet-engineering-skills
```

### Local Editable Development Installation
```bash
git clone https://github.com/techpronnet/techpronnet-engineering-skills.git
cd techpronnet-engineering-skills
pip install -e .
```

## Command Reference

### `tes version`
Displays current CLI version and environment details.

### `tes doctor`
Diagnoses the runtime environment:
- Python interpreter and version
- User and project write permissions
- Detected agent configurations
- Manifest integrity checks

### `tes detect`
Scans for installed AI coding agent environments in both project and global scopes.

### `tes search [QUERY]`
Searches the local TES registry for skills by name, tag, or description.

### `tes inspect <SKILL-ID>`
Inspects metadata, description, dependencies, and bundled assets for a specific skill.

### `tes install <SKILL-OR-BUNDLE> [--target <TARGET>] [--scope <project|global>]`
Installs an individual skill or bundle.
Targets: `hermes`, `opencode`, `codex`, `claude-code`, `gemini-cli`, `generic`.
Scopes: `project` (default when in a project), `global`.

### `tes list [--target <TARGET>] [--scope <project|global>]`
Lists all TES-managed skills currently installed in target directories.

### `tes update <SKILL-OR-ALL> [--preview]`
Safely checks for and applies updates to installed skills.

### `tes uninstall <SKILL-ID> [--target <TARGET>] [--scope <project|global>]`
Safely removes a TES-managed skill. Rejects removal of non-TES skills.

### `tes validate [PATH]`
Validates skill directory integrity and frontmatter schema.
