# TES — Techpronnet Engineering Skills

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Repository](https://img.shields.io/badge/GitHub-officialdb%2FTES--SKILLS-blue?logo=github)](https://github.com/officialdb/TES-SKILLS)

> **Portable ecosystem of reusable AI engineering skills for coding agents.**

---

## 💡 What is TES?

TES (**Techpronnet Engineering Skills**) is an open, platform-independent skill distribution and package management system for AI coding agents.

It equips autonomous AI agents (such as **OpenCode**, **Hermes**, **Claude Code**, **OpenAI Codex CLI**, **Gemini CLI**, and **Generic Agent Skills** environments) with battle-tested engineering standards, structured workflows, security procedures, and memory persistence.

### Fundamental Principle
> **Skills run natively inside your AI agent. The TES CLI is never required during active coding sessions.**

The `tes` CLI handles discovering, installing, updating, and validating skills. Once installed, the target AI agent natively reads and follows the standard `SKILL.md` instructions and bundled reference manuals in its own directory.

---

## 📋 What Do I Need Before Installing?

- **Python:** Python 3.10 or higher (`python3 --version`).
- **Git:** Git installed on your system (`git --version`).
- **An AI Coding Agent:** An installed coding agent such as OpenCode, Hermes, Claude Code, OpenAI Codex CLI, or Gemini CLI.
- **Package Tool (Recommended):** [`uv`](https://github.com/astral-sh/uv) or [`pipx`](https://pypa.github.io/pipx/).

---

## 🛠️ How Do I Install TES?

TES is currently distributed directly from its official repository: [`https://github.com/officialdb/TES-SKILLS`](https://github.com/officialdb/TES-SKILLS).

### Method 1: Using `uv` (Recommended)

```bash
uv tool install git+https://github.com/officialdb/TES-SKILLS.git
```

### Method 2: Using `pipx` from Git

```bash
pipx install git+https://github.com/officialdb/TES-SKILLS.git
```

### Method 3: Development Installation from Source

```bash
git clone https://github.com/officialdb/TES-SKILLS.git
cd TES-SKILLS
pip install -e .
```

*Ensure `~/.local/bin` is in your `PATH` so the `tes` command is accessible from any terminal.*

---

## ✅ First-Time Verification

Verify your installation with these four commands:

```bash
# 1. Verify the CLI is installed and view available commands
tes --help

# 2. Check system health, write permissions, and diagnostic status
tes doctor

# 3. Detect installed AI coding environments on your machine
tes detect

# 4. Search all available engineering skills in the catalogue
tes search
```

---

## 📦 How Do I Install My First Skill?

### 1. Search and Inspect
Find the skill you need and inspect its bundled documents:

```bash
# Search for backend skills
tes search backend

# Inspect the backend-engineering skill
tes inspect backend-engineering
```

### 2. Install into Your Coding Agent
Install the skill into your preferred AI agent:

```bash
# Install globally (available across all projects on your machine)
tes install backend-engineering --target opencode --scope global

# Or install locally for the current project repository only
tes install backend-engineering --target opencode --scope project
```

- **`--target`**: Specifies your AI agent adapter (`hermes`, `opencode`, `codex`, `claude-code`, `gemini-cli`, or `generic`). Defaults to the first detected agent if omitted.
- **`--scope global`**: Installs into your user directory (e.g. `~/.config/opencode/skills/`).
- **`--scope project`**: Installs into the current repository (e.g. `.opencode/skills/`).
- **`tes install` vs `tes update`**: Use `tes install` to add new skills. Use `tes update` to check for and apply updates to already-installed skills.

### 3. Installing Skill Bundles
You can install an entire suite of skills in a single command:

```bash
# Install the core engineering suite (7 foundation engineering skills)
tes install engineering-suite --target opencode --scope global

# Install the complete catalogue (all 15 skills)
tes install complete-suite --target opencode --scope global
```

### 4. Verify Installed Skills
Confirm that skills are installed and tracked in your manifest:

```bash
tes list --target opencode --scope global
```

---

## 🤖 Getting the Best Out of TES

You do not need to run the `tes` CLI when writing code. Your AI agent reads the installed skills natively from its skills directory.

### How to Instruct Your AI Agent
Simply chat with your coding agent and instruct it to use the relevant installed TES skills:

```text
Act as a senior backend engineer working on this project.

Use the installed TES backend-engineering skill.

Inspect the current backend architecture, business logic,
request handling, and database queries.
Identify any N+1 query risks and propose practical improvements.

Do not modify files until I approve your plan.
```

The agent will locate the installed `SKILL.md` file, follow its progressive disclosure rules, and consult the relevant reference manuals (e.g. `persistence-integration.md`).

### Practical Prompt Library
TES includes ready-to-use, copy-and-paste prompts for common engineering workflows:

- [Understand an existing project](docs/prompt-library.md#1-understand-an-existing-project)
- [Build a new feature](docs/prompt-library.md#2-build-a-new-feature)
- [Backend engineering review](docs/prompt-library.md#3-backend-engineering)
- [Frontend and UI improvement](docs/prompt-library.md#4-frontend-and-ui-improvement)
- [Database review](docs/prompt-library.md#5-database-review)
- [Security audit](docs/prompt-library.md#6-security-audit)
- [Code review](docs/prompt-library.md#7-code-review)
- [Testing strategy](docs/prompt-library.md#8-testing-and-quality-assurance)
- [Production readiness](docs/prompt-library.md#9-production-readiness)
- [Safe refactoring](docs/prompt-library.md#10-improve-existing-code-safely)

Explore all prompts and the universal prompt template in the **[Prompt Library](docs/prompt-library.md)**.

---

## 🔌 Supported AI Coding Environments

TES features a decoupled adapter architecture:

| Environment | Adapter Flag | Project Scope Directory | Global Scope Directory |
|---|---|---|---|
| **Hermes** | `--target hermes` | `.hermes/skills/` | `~/.hermes/skills/` |
| **OpenCode** | `--target opencode` | `.opencode/skills/` | `~/.config/opencode/skills/` |
| **OpenAI Codex CLI** | `--target codex` | `.codex/skills/` | `~/.codex/skills/` |
| **Claude Code** | `--target claude-code` | `.claude/skills/` | `~/.claude/skills/` |
| **Gemini CLI** | `--target gemini-cli` | `.gemini/skills/` | `~/.gemini/config/skills/` |
| **Generic Agent Skills** | `--target generic` | `.agents/skills/` | `~/.agents/skills/` |

> *Note: Support is adapter-based. Application detection confirms that an application or its configuration exists, but does not represent an endorsement or certified vendor integration.*

---

## 📦 Skill Catalogue (15 Skills)

### Engineering
- `engineering-core`: Fundamental principles, understand-before-modifying, balanced autonomy, quality gates.
- `system-architect`: Domain modeling, architectural decision records (ADRs), module boundary design.
- `backend-engineering`: Production backend architecture, business services, API lifecycle, persistence integration, background tasks, and security boundaries.
- `software-engineering`: Clean code, dependency hygiene, error handling, refactoring patterns.
- `code-review`: Dual-axis PR review (standards compliance + specification verification).
- `project-onboarding`: Fast repository structure comprehension and dependency mapping.
- `testing-strategy`: Test pyramid, integration testing, boundary analysis, deterministic mocking.

### Security
- `security-audit`: OWASP Top 10, CWE patterns, evidence-backed vulnerability analysis.
- `secure-development`: Threat-resistant development, input sanitization, authentication, secrets handling.
- `threat-modeling`: STRIDE threat modeling, trust boundaries, attack surface reduction.

### DevOps
- `devops-engineering`: CI/CD pipelines, container hygiene, infrastructure as code, rollback strategy.
- `deployment-verification`: Post-deployment smoke tests, canary health checks, zero-downtime cutover.

### Design and Frontend
- `ui-ux-standards`: Modern, restrained visual design, typography, spacing, responsive navigation, WCAG accessibility.
- `frontend-quality`: Performance metrics (Core Web Vitals), state management, responsive navigation implementation, layout resilience.

### Memory
- `engineering-memory`: Local-first, offline markdown engineering knowledge base (`.engineering/`).

### Bundles
- `engineering-suite`: `engineering-core`, `system-architect`, `backend-engineering`, `software-engineering`, `code-review`, `testing-strategy`, `project-onboarding`
- `security-suite`: `security-audit`, `secure-development`, `threat-modeling`
- `release-suite`: `devops-engineering`, `deployment-verification`
- `complete-suite`: All 15 published TES skills

---

## 📚 Documentation Index

- **[Getting Started Guide](docs/getting-started.md)**: Beginner walk-through and mental model.
- **[Installation Guide](docs/installation.md)**: Detailed prerequisites, installation options, and updates.
- **[Prompt Library](docs/prompt-library.md)**: 10 copy-and-paste prompts and a universal template.
- **[Command Reference](docs/commands.md)**: Complete guide to all 11 `tes` CLI commands.
- **[Troubleshooting Guide](docs/troubleshooting.md)**: Solutions for common issues and PATH errors.
- **[Adapters Guide](docs/adapters.md)**: Deep dive into AI coding agent integration paths.
- **[Architecture](docs/architecture.md)**: Decoupled system design and progressive disclosure.
- **[Security Model](docs/security-model.md)**: Path traversal protections and script quarantine.

---

## 🛡️ Security & Package Integrity

- **Path Traversal Protection:** All target paths and archive extractions are validated against destination bounds.
- **Untrusted Script Quarantine:** Scripts bundled in skills are never executed automatically by the CLI.
- **Non-destructive Installation:** User-owned skills are detected and never silently overwritten.
- **Manifest Tracking:** Every installation writes an atomic `.tes-manifest.json` tracking hashes and managed files.
- **Safe Backups:** Pre-update snapshots allow rollback on interrupted operations.

---

## 📄 License

Licensed under the [Apache License, Version 2.0](LICENSE).  
Copyright (c) 2026 Techpronnet Technologies.
