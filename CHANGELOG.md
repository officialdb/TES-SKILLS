# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.2] - 2026-10-31

### Changed - Website Copy & Visual Presentation Standards Refinement
- **Skill Version Increments:** Incremented `ui-ux-standards` and `frontend-quality` to `1.0.1` in the skill registry and frontmatter to enable distribution via `tes update`.
- **Prohibited Decorative Animated Dots:** Updated `ui-ux-standards` and `frontend-quality` to strictly prohibit cosmetic blinking, pulsing, or flashing dots beside titles, headings, badges, hero sections, cards, and navigation.
- **Permitted Functional Indicators:** Clearly distinguished decorative dots from genuine functional system indicators (such as WebSocket connectivity, active streaming, background progress), requiring motion in permitted indicators to be subtle and accessible.
- **Website Copywriting Standards (Eliminating Em Dashes):** Established a strong copywriting preference against using em dashes (`—`) across all user-facing website content (headlines, section titles, subheadings, feature bullets, paragraphs, testimonials, CTAs, navigation, metadata) in favor of natural sentence structure, commas, prepositions, or distinct sentences.
- **Context Boundaries Preserved:** Clarified that technical documentation, code syntax, and CLI arguments remain exempt from the em dash restriction when grammatically or syntactically appropriate.
- **CSS Motion & Template Auditing (`frontend-quality`):** Added frontend engineering rules prohibiting decorative `@keyframes` pulses/blinks in CSS, requiring status indicators to bind directly to reactive state flags, and establishing template string auditing for copy quality.
- **Updated Checklists & References:** Expanded `ui-ux-review-checklist.md`, `visual-design-principles.md`, and `frontend-performance-checklist.md` with explicit review criteria for motion restraint and website copy polish.

## [0.2.1] - 2026-10-31

### Changed - Multi-Method AI Environment Detection
- **Multi-Method Discovery Engine:** Introduced `ApplicationDiscoveryEngine` and modular discovery providers (`CLIDiscoveryProvider`, `DesktopDiscoveryProvider`, `PackageManagerDiscoveryProvider`) to detect AI coding environments regardless of installation method.
- **Desktop Application Discovery:** Added inspection of standard Linux desktop entries (`/usr/share/applications`, `~/.local/share/applications`, etc.) and standard application directories (e.g. `/opt/OpenCode/ai.opencode`). Validates that `Exec=` targets actually exist on disk and extracts version from desktop entries or application metadata files (`resources/opencode-cli.version`).
- **Package Manager Discovery:** Added query support for native package managers (`dpkg`/APT, `rpm`, `flatpak`, `snap`) to identify installed applications when CLI binaries are not linked to PATH.
- **Separated Application Discovery from CLI Discovery:** Extended `EnvironmentStatus` with `application_found`, `installation_method` (`Desktop`, `CLI`, `Package Manager`, `Desktop, CLI`), and `application_path`. An application can now be verified as installed even when its CLI executable is absent.
- **Two-Table Detection CLI (`tes detect`):**
  - *Table 1 (Detected AI Coding Environments):* Adapter, Environment, Installed, Method, CLI, Version.
  - *Table 2 (Configuration and Skills):* Adapter, Configuration, Skills Directory, TES Support.
- **Accurate OpenCode Detection:** Solved the false-negative issue where OpenCode installed as a desktop application without an `opencode` CLI binary on PATH was reported as missing. OpenCode is now properly identified with `Installed: Yes`, `Method: Desktop`, `CLI: No`, and version retrieved.

## [0.2.0] - 2026-10-31

### Changed - Environment Detection Correction
- **Separated Detection States:** Split environment detection into distinct verification properties: `installed`, `executable_found`, `version_verified`, `config_present`, `skills_directory_present`, `project_config_present`, and `available`.
- **Strict Application Verification:** Implemented environment-specific executable checks (`hermes`, `opencode`/`ai.opencode`, `codex`, `claude`, `gemini`) and version commands with non-zero exit and timeout handling.
- **Eliminated False Positives:** Directory existence (such as `~/.hermes`, `~/.claude`, `~/.gemini`, or TES-created directories) is no longer conflated with application installation.
- **Clarified Generic Agent Skills Target:** Correctly designated Generic Agent Skills as an open distribution target, not an executable application (`installed=False`).
- **Corrected Project-Root Detection:** Prevented user home directories from automatically being classified as project roots. Integrated recognized project markers (`.git`, `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, `composer.json`, `requirements.txt`).
- **Read-Only Detection:** Ensured detection and diagnostic commands never create missing directories or modify application configurations.
- **Detection CLI Output:** Updated `tes detect` output with 7 distinct columns: Adapter, Environment, Installed, Version, Configuration, Skills Directory, and TES Support. Added `--project` / `-p` option for explicit project path selection.

### Added - Token Efficiency Architecture
- **Three-Level Progressive Disclosure:**
  - *Level 1 (Discovery Metadata):* Concise YAML frontmatter descriptions (under 200 characters / 35 words) with clear triggers.
  - *Level 2 (Core Instructions):* Actionable, structured `SKILL.md` documents (350–550 words) covering purpose, workflow, autonomy guardrails, deliverables, and progressive disclosure references.
  - *Level 3 (Selective Reference Loading):* Detailed knowledge partitioned into modular files in `references/`, `checklists/`, and `templates/` with explicit conditions on when to consult each file.
- **Skill Activation & Composition Rules:** Defined clear primary versus optional skill activation boundaries to prevent context bloat from activating overlapping skills.
- **Instruction Deduplication & Clear Ownership:** Eliminated redundant copies of universal workflows, autonomy tables, and security checklists across skills. Established authoritative domain ownership across the 14 skills.
- **Selective Engineering Memory Protocol:** Updated `engineering-memory` to enforce selective retrieval rules (loading `project-profile.md`, `architecture.md`, `security-profile.md`, `design-standards.md`, or specific ADRs only when task-relevant) rather than dumping all memory files at startup.
- **Token Efficiency Diagnostics (`tes analyze`):** Introduced CLI command `tes analyze` with support for `--skill`, `--bundle`, and `--report`. Measures instruction sizes, word counts, approximate token consumption (via `tiktoken` cl100k_base), reference counts, duplicate instruction blocks, and metadata length warnings.

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
