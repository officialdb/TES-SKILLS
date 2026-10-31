# TES Installation Guide

This guide walks you through installing and configuring **TES (Techpronnet Engineering Skills)** on your system.

---

## 📋 System Prerequisites

Before installing TES, ensure your environment meets the following requirements:

- **Python:** Python 3.10 or higher (`python3 --version`).
- **Git:** Git installed and accessible on PATH (`git --version`).
- **Operating System:** Linux (Ubuntu, Debian, Kali, Fedora, Arch), macOS, or Windows via WSL2.
- **AI Coding Agent:** An installed coding agent such as OpenCode, Hermes, Claude Code, OpenAI Codex CLI, Gemini CLI, or a Generic Agent Skills environment.

> **Note on Package Distribution:** TES is currently distributed directly from its official GitHub repository at [`https://github.com/officialdb/TES-SKILLS`](https://github.com/officialdb/TES-SKILLS). It is not distributed as a standalone package on PyPI.

---

## 🛠️ Installation Methods

### Method 1: Using `uv` (Recommended)

[`uv`](https://github.com/astral-sh/uv) provides fast, isolated tool installation. If you have `uv` installed:

```bash
uv tool install git+https://github.com/officialdb/TES-SKILLS.git
```

This installs the `tes` CLI into `~/.local/bin/tes` with an isolated virtual environment.

---

### Method 2: Source Clone with `uv`

If you prefer to clone the repository first:

```bash
git clone https://github.com/officialdb/TES-SKILLS.git
cd TES-SKILLS
uv tool install .
```

---

### Method 3: Using `pipx` from Git

[`pipx`](https://pypa.github.io/pipx/) installs CLI tools in isolated environments:

```bash
pipx install git+https://github.com/officialdb/TES-SKILLS.git
```

---

### Method 4: Editable Development Installation with `pip`

For contributors or developers who want to modify skills locally:

```bash
git clone https://github.com/officialdb/TES-SKILLS.git
cd TES-SKILLS
pip install -e .
```

Verify that Python's script directory (`~/.local/bin`) is in your system's `PATH`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

## ✅ Verifying Your Installation

After installation, run these four commands to verify that TES is operating correctly:

```bash
# 1. Verify CLI binary is reachable
tes --help

# 2. Check installed version and runtime
tes version

# 3. Run automated system diagnostics and permission checks
tes doctor

# 4. Detect installed AI coding environments
tes detect
```

When all diagnostic checks in `tes doctor` report `PASS`, TES is ready to manage skills.

---

## 📦 Installing Your First Skill

To install a skill into your AI coding agent:

```bash
# 1. Search for skills
tes search backend

# 2. Inspect a skill's contents
tes inspect backend-engineering

# 3. Install it globally into your target agent
tes install backend-engineering --target opencode --scope global
```

### Installation Scopes
- `--scope global`: Installs to user directory (e.g., `~/.config/opencode/skills/`). Available across all projects.
- `--scope project`: Installs to repository directory (e.g., `.opencode/skills/`). Available only in this project.

### Supported Target Adapters
| Target Flag | AI Coding Agent | Global Skill Directory | Project Skill Directory |
|---|---|---|---|
| `--target hermes` | Hermes | `~/.hermes/skills/` | `.hermes/skills/` |
| `--target opencode` | OpenCode | `~/.config/opencode/skills/` | `.opencode/skills/` |
| `--target codex` | OpenAI Codex CLI | `~/.codex/skills/` | `.codex/skills/` |
| `--target claude-code` | Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| `--target gemini-cli` | Gemini CLI | `~/.gemini/config/skills/` | `.gemini/skills/` |
| `--target generic` | Generic Agent Skills | `~/.agents/skills/` | `.agents/skills/` |

---

## 🔄 Updating TES

To update the `tes` CLI to the latest version:

### If installed with `uv`:
```bash
uv tool upgrade techpronnet-engineering-skills
```

### If installed from source clone:
```bash
cd TES-SKILLS
git pull origin develop
pip install -e .
```

---

## 🗑️ Uninstalling TES

### Remove CLI tool:
```bash
# With uv
uv tool uninstall techpronnet-engineering-skills

# With pipx
pipx uninstall techpronnet-engineering-skills

# With pip
pip uninstall techpronnet-engineering-skills
```

Skills previously installed into your agents will remain fully functional in their native directories unless explicitly removed via `tes uninstall <skill-id>`.
