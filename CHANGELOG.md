# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-10-31

### Added
- Initial project architecture and foundation.
- Comprehensive registry system (`skills.yaml` and `bundles.yaml`).
- Core CLI framework built with Typer and Rich (`tes`).
- Initial foundation skills:
  - `engineering-core`
  - `system-architect`
  - `software-engineering`
  - `security-audit`
  - `devops-engineering`
- Complete skills catalogue:
  - `code-review`
  - `project-onboarding`
  - `testing-strategy`
  - `secure-development`
  - `threat-modeling`
  - `deployment-verification`
  - `ui-ux-standards`
  - `frontend-quality`
  - `engineering-memory`
- Adapter layer for:
  - Hermes (`.hermes/skills`, `~/.hermes/skills`)
  - OpenCode (`.opencode/skills`, `~/.config/opencode/skills`)
  - OpenAI Codex CLI (`.codex/skills`, `~/.codex/skills`)
  - Claude Code (`.claude/skills`, `~/.claude/skills`)
  - Gemini CLI (`.gemini/skills`, `~/.gemini/config/skills`)
  - Generic Agent Skills (`.agents/skills`, `~/.agents/skills`)
- Manifest tracking and safe uninstallation engine.
- Path traversal and security protections.
- Environment detection and `tes doctor` diagnostics.
