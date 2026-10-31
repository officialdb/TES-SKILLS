# TES — Techpronnet Engineering Skills

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

> **Portable ecosystem of reusable AI engineering skills for coding agents.**

TES (**Techpronnet Engineering Skills**) is a platform-independent skill distribution and management system. It provides autonomous AI coding agents (Hermes, OpenCode, OpenAI Codex CLI, Claude Code, Gemini CLI, and generic Agent Skills environments) with structured, battle-tested engineering workflows, quality standards, security procedures, and memory persistence.

---

## 🎯 Product Vision

**Fundamental Principle:** *Skills must remain fully functional after installation, even when the TES CLI is not installed or running.*

The CLI manages discovery, installation, updates, validation, and manifests. The target AI agent natively executes the installed skills using standard `SKILL.md` workflows.

### What TES IS:
- A collection of portable, modular AI agent skills.
- A CLI-based skill distribution and package management system.
- An adapter-driven integration layer for major AI coding agents.
- A local-first engineering knowledge and memory system.
- Secure, reproducible engineering standards and guardrails.

### What TES IS NOT:
- Not a standalone AI agent.
- Not an LLM orchestration framework.
- Not a replacement for Hermes, OpenCode, Claude Code, or Codex.
- Not a mandatory cloud-hosted service or proprietary API.

---

## 🚀 Quick Start

### Installation

```bash
# Using pipx (recommended)
pipx install techpronnet-engineering-skills

# Using uv
uv tool install techpronnet-engineering-skills

# Development installation from source
git clone https://github.com/techpronnet/techpronnet-engineering-skills.git
cd techpronnet-engineering-skills
pip install -e .
```

### Basic Commands

```bash
# Verify installation and view available commands
tes --help

# Check system health, write permissions, and detected agents
tes doctor

# Detect active AI coding environments in the current project and user home
tes detect

# Search available skills in the registry
tes search
tes search security

# Inspect a specific skill's metadata and workflow
tes inspect engineering-core

# Install an individual skill into the automatically detected agent
tes install engineering-core

# Install a bundle into a specific target agent and scope
tes install complete-suite --target hermes --scope global
tes install engineering-suite --target opencode --scope project

# List currently installed TES-managed skills
tes list

# Validate skill packages for schema adherence and integrity
tes validate

# Analyze skill catalogue for token efficiency and progressive disclosure
tes analyze
tes analyze --skill security-audit
tes analyze --report

# Safe update with preview
tes update engineering-core

# Safe uninstall (preserves custom user files)
tes uninstall security-audit
```

---

## 🔌 Supported AI Coding Environments

TES features a decoupled adapter architecture:

| Environment | Adapter | Project Scope | Global Scope |
|---|---|---|---|
| **Hermes** | `hermes` | `.hermes/skills/` | `~/.hermes/skills/` |
| **OpenCode** | `opencode` | `.opencode/skills/` | `~/.config/opencode/skills/` |
| **OpenAI Codex CLI** | `codex` | `.codex/skills/` | `~/.codex/skills/` |
| **Claude Code** | `claude-code` | `.claude/skills/` | `~/.claude/skills/` |
| **Gemini CLI** | `gemini-cli` | `.gemini/skills/` | `~/.gemini/config/skills/` |
| **Generic Agent Skills** | `generic` | `.agents/skills/` | `~/.agents/skills/` |

---

## 📦 Skill Catalogue

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
- `ui-ux-standards`: Modern, restrained visual design, typography, spacing, WCAG accessibility.
- `frontend-quality`: Performance metrics (Core Web Vitals), state management, responsive integrity.

### Memory
- `engineering-memory`: Local-first, offline markdown engineering knowledge base (`.engineering/`).

---

## 📦 Bundles

- `engineering-suite`: `engineering-core`, `system-architect`, `backend-engineering`, `software-engineering`, `code-review`, `testing-strategy`, `project-onboarding`
- `security-suite`: `security-audit`, `secure-development`, `threat-modeling`
- `release-suite`: `devops-engineering`, `deployment-verification`
- `complete-suite`: All published TES skills

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
