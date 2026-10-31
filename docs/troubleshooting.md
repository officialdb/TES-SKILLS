# TES Troubleshooting Guide

This guide provides practical solutions to common issues encountered when installing, configuring, and using TES skills.

---

## 1. `tes: command not found`

### Cause
The directory containing the installed `tes` binary is not in your system's `PATH` environment variable.

### Solution

#### If installed using `uv tool`:
`uv` installs binaries into `~/.local/bin`. Ensure this directory is in your `PATH`:

```bash
# Check if ~/.local/bin is in PATH
echo $PATH | grep -q "$HOME/.local/bin" && echo "Present" || echo "Missing"

# Add to ~/.bashrc or ~/.zshrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### If installed in a Python virtual environment:
Ensure your virtual environment is activated:

```bash
source .venv/bin/activate
which tes
```

#### If installed via `pip install -e .` without virtualenv:
Python user scripts are typically in `~/.local/bin`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

## 2. Python Version or Package Installation Errors

### Error: `requires Python '>=3.10'`
TES requires Python 3.10 or higher. If your default python version is older (e.g. Python 3.8 or 3.9 on older LTS distributions):

```bash
# Check your Python version
python3 --version
```

### Solution:
Install Python 3.10+ using `pyenv`, `uv`, or your system package manager:

```bash
# Using uv (fastest)
uv python install 3.11

# On Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip
```

---

## 3. AI Coding Environment Not Detected

### Symptoms:
Running `tes detect` shows `Installed: No` for an application you have installed.

### Explanation:
TES uses multi-method discovery to check desktop application files (`.desktop`), standard binary locations on `PATH`, and package manager databases (`dpkg`, `rpm`, `flatpak`, `snap`).

### Solutions:
1. **Desktop vs. CLI:** If OpenCode or Hermes is installed as a desktop application without adding its binary to `PATH`, TES v0.2.1+ detects the desktop installation automatically. If you are on an older version of TES, update your installation.
2. **Manual Target Selection:** You do not need `tes detect` to report `Installed: Yes` in order to install skills. You can explicitly specify your agent adapter using `--target`:
   ```bash
   tes install backend-engineering --target opencode --scope global
   ```
   TES will write the skill files to OpenCode's standard global skill directory (`~/.config/opencode/skills/`).

---

## 4. Skill Exists in Catalogue but is Not Installed

### Symptoms:
You ran `tes search` and found `backend-engineering`, but your AI agent cannot find it, or `tes list` does not display it.

### Explanation:
`tes search` searches the **catalogue of available skills**. Finding a skill in the search results does not mean it is installed on your computer yet.

### Solution:
Install the skill explicitly:

```bash
tes install backend-engineering --target opencode --scope global
```

Verify that it is now installed:

```bash
tes list --target opencode --scope global
```

---

## 5. Global vs. Project Installation Scope Confusion

### Difference:
- **`--scope global`:** Installs skills into your user home directory (e.g. `~/.config/opencode/skills/` or `~/.hermes/skills/`). The skill is available to your agent across **all repositories** on your machine.
- **`--scope project` (Default):** Installs skills into the current repository's root (e.g. `.opencode/skills/` or `.hermes/skills/`). The skill is available only when working inside this specific project.

### When to use which:
- **Use `global`** for foundational skills you always want available (e.g., `engineering-core`, `code-review`, `backend-engineering`, `ui-ux-standards`).
- **Use `project`** for team repositories where you want skills committed to version control so all teammates and CI agents use the exact same standards.

---

## 6. Skill Installed but Not Being Discovered by Agent

### Checklist:
1. **Confirm the installation path:**
   Run `tes list --target <your-agent> --scope <global|project>` to verify where TES placed the files.
2. **Check Agent Target Match:**
   Ensure you installed to the adapter your agent actually uses:
   - Hermes: `--target hermes`
   - OpenCode: `--target opencode`
   - Claude Code: `--target claude-code`
   - OpenAI Codex CLI: `--target codex`
   - Gemini CLI: `--target gemini-cli`
   - Generic: `--target generic`
3. **Prompt the Agent Explicitly:**
   Tell the agent to check its skills directory:
   *"Use the installed TES backend-engineering skill in your skills folder to review this service."*

---

## 7. Newly Installed Skill Not Appearing Until Agent Restart

### Symptoms:
You installed a skill using `tes install`, but your active agent session does not acknowledge it.

### Explanation:
Some AI coding agents (such as desktop applications or persistent CLI sessions) index skill directories only at startup or session initialization.

### Solution:
Restart your coding agent session or open a new terminal window after installing new skills. Once reloaded, the agent will scan the skills folder and index the new `SKILL.md` file.

---

## 8. Updating Existing Skills vs. Installing New Ones

### Key Distinction:
- **`tes install`:** Used to install a **new** skill or bundle that has not been installed yet.
- **`tes update`:** Used to check for and apply updates to skills **already installed** on your machine.

Running `tes update` will **not** install new skills that you have never installed before.

### How to update:
```bash
# 1. Preview which installed skills have updates available
tes update --target opencode --scope global --preview

# 2. Apply updates
tes update --target opencode --scope global
```
