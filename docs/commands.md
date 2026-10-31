# TES CLI Command Reference

This document provides a complete reference for all commands available in the `tes` CLI.

---

## Global Options

- `--help`: Show command description and usage instructions.

```bash
tes --help
tes <command> --help
```

---

## 1. `tes version`

Display current TES CLI version, Python environment, and operating system details.

```bash
tes version
```

**Output:**
- TES package version (e.g. `0.2.2`)
- Python version and interpreter path
- Platform and system architecture

---

## 2. `tes doctor`

Run comprehensive diagnostic checks on your environment, file write permissions, and registry integrity.

```bash
tes doctor
```

**Checks Performed:**
- Python runtime compatibility (`>= 3.10`)
- Registry file presence (`registry/skills.yaml`, `registry/bundles.yaml`)
- Schema and manifest integrity
- Write permissions for all 6 environment adapters across both `project` and `global` scopes

---

## 3. `tes detect`

Scan for active AI coding agent environments and skill directories.

```bash
# Detect environments in current working directory and user home
tes detect

# Explicitly specify a target project path
tes detect --project /path/to/my-project
```

**Options:**
- `--project`, `-p`: Explicit path to inspect for project-level configurations.

**Output Tables:**
1. **Detected AI Coding Environments:** Displays Adapter, Application Name, Installed status, Installation Method (Desktop, CLI, Package Manager), CLI presence, and Version.
2. **Configuration and Skills:** Displays Adapter, Configuration Path, Native Skills Directory, and TES Support status.

---

## 4. `tes search`

Search the skills catalogue by keyword, domain, or tag.

```bash
# List all skills in the catalogue
tes search

# Search by keyword
tes search backend
tes search security
tes search "ui-ux"

# Filter by category (engineering, security, devops, design, memory)
tes search --category engineering
```

**Options:**
- `QUERY`: Optional keyword search string.
- `--category`, `-c`: Filter by category.

---

## 5. `tes inspect`

Inspect full metadata, core principles, tags, compatibility, and bundled assets for a skill.

```bash
tes inspect backend-engineering
tes inspect ui-ux-standards
```

**Arguments:**
- `SKILL_ID`: Required skill identifier (e.g. `backend-engineering`).

**Output:**
- ID, Name, Version, Category, Tags, Compatibility list
- Full description
- Complete manifest of bundled assets (`SKILL.md`, references, checklists, templates)

---

## 6. `tes install`

Install an individual skill or bundle into a target AI coding environment.

```bash
# Install a single skill globally
tes install backend-engineering --target opencode --scope global

# Install a single skill locally in the current project
tes install software-engineering --target hermes --scope project

# Install a bundle
tes install engineering-suite --target opencode --scope global
tes install complete-suite --target claude-code --scope global

# Force overwrite of an existing skill
tes install backend-engineering --target opencode --scope global --force
```

**Arguments:**
- `TARGET_IDENTIFIER`: Required skill ID or bundle ID.

**Options:**
- `--target`, `-t`: Target AI agent (`hermes`, `opencode`, `codex`, `claude-code`, `gemini-cli`, `generic`). Defaults to the first detected agent if omitted.
- `--scope`, `-s`: Installation scope (`project` or `global`). Default: `project`.
- `--force`, `-f`: Overwrite destination directory if it already exists.

---

## 7. `tes list`

List all TES-managed skills currently installed in a target environment.

```bash
# List globally installed skills for OpenCode
tes list --target opencode --scope global

# List project-installed skills for Hermes
tes list --target hermes --scope project
```

**Options:**
- `--target`, `-t`: Target agent adapter.
- `--scope`, `-s`: Installation scope (`project` or `global`). Default: `project`.

**Output:**
- Skill ID, installed version, installation timestamp, and number of managed files tracked in `.tes-manifest.json`.

---

## 8. `tes update`

Check for and safely apply updates to installed skills.

```bash
# Preview available updates without making changes
tes update --target opencode --scope global --preview

# Apply updates to all outdated skills in an environment
tes update --target opencode --scope global

# Update a single specific skill
tes update ui-ux-standards --target opencode --scope global
```

**Arguments:**
- `[SKILL_ID]`: Optional skill ID to update. Omit to check and update all installed skills.

**Options:**
- `--target`, `-t`: Target agent adapter.
- `--scope`, `-s`: Scope (`project` or `global`). Default: `project`.
- `--preview`, `-p`: Show available updates in a table without modifying files.

---

## 9. `tes uninstall`

Safely remove a TES-managed skill. Rejects removal of user-created, unmanaged skills.

```bash
# Uninstall a globally installed skill
tes uninstall backend-engineering --target opencode --scope global

# Uninstall a project-level skill
tes uninstall testing-strategy --target hermes --scope project
```

**Arguments:**
- `SKILL_ID`: Required skill ID to remove.

**Options:**
- `--target`, `-t`: Target agent adapter.
- `--scope`, `-s`: Scope (`project` or `global`). Default: `project`.

---

## 10. `tes validate`

Validate skill packages against open Agent Skills specifications and schema rules.

```bash
# Validate all skills in the default repository catalogue
tes validate

# Validate a specific skill directory
tes validate skills/backend-engineering
```

**Checks Performed:**
- YAML frontmatter presence and schema conformance (`name`, `version`, `description`, `compatibility`)
- File existence and non-empty instruction body
- Reference link resolution (ensures all Markdown links resolve to real files)

---

## 11. `tes analyze`

Analyze the skills catalogue for token efficiency, word budgets, and duplicate instruction blocks.

```bash
# Run full catalogue token analysis
tes analyze

# Analyze a single skill
tes analyze --skill backend-engineering

# Analyze a bundle
tes analyze --bundle engineering-suite

# Generate a detailed Markdown diagnostic report
tes analyze --report
```

**Options:**
- `--skill`, `-s`: Analyze a specific skill.
- `--bundle`, `-b`: Analyze all skills in a bundle.
- `--report`, `-r`: Generate a comprehensive markdown report.

