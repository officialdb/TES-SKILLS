# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.3] - 2026-11-01

### Enhanced - E-commerce Storefront & Product Detail Design Reference Architecture (v1.3.0)
- **Skill Version Increments:** Incremented `ui-ux-standards` and `frontend-quality` to `1.3.0` in the registry and frontmatter.
- **E-Commerce Design Principles & Product Experience (`ui-ux-standards`):**
  - Extracted evidence-based design principles from Reference A (ZenVora E-commerce Storefront): promotional announcement bars, 3-zone brand/search/utility headers, persistent category sidebars with promotional hero balance, 5-column product discovery grids with status badges, 2-column promotional editorial banners, blog previews, brand directories, and 5-column footers.
  - Extracted buying decision hierarchy from Reference B (SoundWave Product Detail Page): breadcrumb navigation, asymmetric 2-column PDP layout, dominant product galleries with thumbnail variations, star rating placement, current vs. previous strikethrough pricing, color variant chips, bounded quantity steppers, dual CTA hierarchy ("Buy Now" vs. "Add to Cart"), trust reassurance micro-services, and 4-column technical specification tables.
  - Established context-sensitive design principles in `visual-design-principles.md` enforcing domain adaptability across e-commerce storefronts, PDPs, SaaS dashboards, and landing pages without forcing one archetype's template onto another.
  - Added reference manual `references/ecommerce-design-principles.md` and updated `checklists/ui-ux-review-checklist.md`.
- **E-Commerce Implementation, Component Architecture & Performance (`frontend-quality`):**
  - Documented responsive product grid reflow mechanics (`xl:grid-cols-5` -> `lg:grid-cols-4` -> `md:grid-cols-3` -> `grid-cols-2`), category sidebar drawer collapse, mobile 2-column to 1-column promotional banner stacking, and responsive specification table horizontal scroll or mobile definition list cards (`<dl>`).
  - Implemented functional interactive standards: debounced search queries (250–300ms), reactive product gallery thumbnail synchronization, variant selection state binding, bounded quantity steppers, distinct async "Add to Cart" vs direct "Buy Now" flows, and WAI-ARIA tabbed specifications (`role="tablist"`).
  - Enforced Core Web Vitals targets: eliminating layout shifts (CLS < 0.1) via fixed aspect ratio wrappers (`aspect-square` or `aspect-[4/5]`), optimizing LCP (<2.5s) via eager loading and head preloads for primary hero/PDP images, and lazy-loading below-the-fold grids.
  - Added reference manual `references/ecommerce-implementation.md` and updated `checklists/frontend-performance-checklist.md`.
- **Test Suite Updates:** Expanded unit test suite in `tests/unit/test_ui_ux_standards.py` with tests for v1.3.0 registry and frontmatter updates, update detection, and e-commerce design and implementation standards; updated catalogue reference file count assertion to 74 in `tests/unit/test_token_efficiency.py`.

## [0.2.2] - 2026-10-31

### Enhanced - Frontend Design Knowledge Base & Component Library Ecosystems (v1.2.0)
- **Skill Version Increments:** Incremented `ui-ux-standards` and `frontend-quality` to `1.2.0` in the registry and frontmatter.
- **Dashboard Design & Information Architecture (`ui-ux-standards`):**
  - Extracted reusable design principles from Reference A (HR Management Dashboard "Githr"): persistent sidebar layouts, contextual header action clusters, 3-column workspace grids, information density with subtle 1px container borders, scannable data metrics, and purposeful accent restraint (purple).
  - Added reference manual `references/dashboard-design-principles.md` and updated `checklists/ui-ux-review-checklist.md`.
- **Landing Page Design & Visual Storytelling (`ui-ux-standards`):**
  - Extracted reusable design principles from Reference B (Minimalist Finance SaaS Landing Page "Zubaz"): centered editorial serif hero typography, conversion action hierarchy (solid primary CTA vs outlined secondary), product-led visual showcases (realistic mobile interface mockup, benefit outcome pills), and whitespace discipline.
  - Added reference manual `references/landing-page-design-principles.md`.
- **Component Library Design Guidelines (`ui-ux-standards`):**
  - Established standards for component library brand independence: treating libraries as implementation resources rather than design templates, customizing foundation tokens, preserving visual consistency, and prohibiting decorative blinking dots.
  - Added reference manual `references/component-library-design-guidelines.md`.
- **Frontend Component Library Selection & Integration (`frontend-quality`):**
  - Established a 10-point evaluation checklist before introducing UI library dependencies.
  - In-depth implementation guidance for `shadcn/ui` (locally owned code in `components/ui/`, Radix primitives, Tailwind CSS variables) and `Flowbite` (Tailwind plugin, dashboard and modal components).
  - Decision framework for reusing vs customizing vs composing vs custom-building components, and documentation verification rules to prevent API hallucinations.
  - Added reference manual `references/frontend-component-library-selection.md`.
- **Dashboard Layout Implementation (`frontend-quality`):**
  - Documented multi-column CSS Grid collapse mechanics (`xl:grid-cols-3` -> `md:grid-cols-2` -> `grid-cols-1`), sidebar collapse to compact rail or mobile off-canvas drawer, accessible SVG circular progress rings, accessible bar chart figures, and interval-cleaned digital timers.
  - Added reference manual `references/dashboard-layout-implementation.md`.
- **Landing Page Implementation & Core Web Vitals (`frontend-quality`):**
  - Documented fluid clamp typography, horizontal scrollbar protection (`overflow-x: clip`), responsive product mockup containers eliminating CLS (<0.1), and hero asset preloading for LCP (<2.5s).
  - Added reference manual `references/landing-page-implementation.md` and updated `checklists/frontend-performance-checklist.md`.

### Documentation - Beginner-Friendly Installation & Getting Started Guide
- **README Quick Start Overhaul:** Structured the README to answer beginner questions in order: What is TES, prerequisites, installation methods, first-time verification, installing first skill/bundle, and agent usage.
- **Canonical Repository URLs:** Updated all documentation and contribution guides to reference the canonical GitHub repository (`https://github.com/officialdb/TES-SKILLS.git`).
- **Verified Installation Instructions:** Replaced unverified PyPI claims with tested, copy-and-paste commands using `uv tool install git+...`, `pipx install git+...`, and source installations.
- **Dedicated Getting Started Guide (`docs/getting-started.md`):** Detailed walkthrough of the TES mental model, 4-step quickstart, how skills work under the hood, and tips for getting the best results from AI coding agents.
- **Practical Prompt Library (`docs/prompt-library.md`):** Curated 10 copy-and-paste prompts for project understanding, feature development, backend engineering, frontend/UI, database review, security audits, code reviews, testing, production readiness, and refactoring, plus a universal prompt template.
- **Complete CLI Reference (`docs/commands.md`):** In-depth reference for all 11 `tes` CLI commands, flags, and options with realistic examples.
- **Beginner Troubleshooting Guide (`docs/troubleshooting.md`):** Practical solutions for `tes: command not found` PATH issues, Python version checks, environment discovery, scope differences, and agent cache reloading.

### Enhanced - Responsive Navigation & Mobile Hamburger Menus (v1.1.0)
- **Skill Version Increments:** Incremented `ui-ux-standards` and `frontend-quality` to `1.1.0` in the registry and frontmatter.
- **Responsive Navigation Design (`ui-ux-standards`):**
  - Added dedicated standards for desktop horizontal navigation layouts (branding alignment, link volume caps to prevent overcrowding, visual hierarchy).
  - Established mobile hamburger menu standards (recognizable three-line icon, minimum 44x44px touch targets, clear toggle/close states, occlusion prevention).
  - Defined content-driven responsive breakpoints and device orientation resilience (portrait and landscape usability, zero horizontal overflow).
  - Documented navigation archetypes (dropdown, slide-in side drawer, full-screen overlay, expandable accordion) to allow project-appropriate architecture.
  - Added reference manual `references/responsive-navigation-design.md` and reusable verification checklist `checklists/responsive-navigation-checklist.md`.
- **Responsive Navigation Implementation & Accessibility (`frontend-quality`):**
  - Added implementation standards covering state predictability, auto-closing on route navigation, viewport resize sync, and body scroll locking (`overflow: hidden`) during modal navigation overlays.
  - Established WCAG accessibility requirements: semantic `<button>` trigger, dynamic accessible names (`aria-label`), `aria-expanded`, `aria-controls`, full keyboard navigation, `Escape` key dismissal with focus restoration to trigger, and `:focus-visible` styling.
  - Enforced single-source-of-truth navigation data items to eliminate duplicated markup across desktop and mobile views, while eliminating unnecessary third-party menu dependencies.
  - Added reference manual `references/responsive-navigation-implementation.md` and updated `checklists/frontend-performance-checklist.md`.

### Added - Backend Engineering Skill (v1.0.0)
- **New Foundation Skill (`backend-engineering`):** Created a comprehensive, framework-independent, language-agnostic, and production-oriented backend engineering skill (`skills/backend-engineering/SKILL.md`) structured under TES's 3-level progressive disclosure architecture.
- **Reference Manuals (Level 3 Knowledge):** Added 10 specialized backend engineering reference documents in `skills/backend-engineering/references/`:
  - `backend-architecture.md`: Clean architecture, modular monoliths, DDD, dependency injection, and 12-factor configuration.
  - `api-and-http.md`: Ingress/egress request lifecycle, HTTP status codes, uniform RFC 7807 error envelopes, and pagination strategies.
  - `authentication-authorization.md`: AuthN vs AuthZ, session vs JWT lifecycles, Argon2id/bcrypt password hashing, RBAC/ABAC, IDOR mitigation, and multi-tenancy.
  - `business-logic.md`: Service layer pattern, transactional boundaries, state machines, domain events, and typed exceptions.
  - `persistence-integration.md`: ORM hygiene, N+1 query elimination via eager loading, optimistic/pessimistic locking, and zero-downtime expand/contract schema migrations.
  - `background-processing.md`: Asynchronous task execution, idempotent job keys, exponential backoff with jitter, and dead-letter queues.
  - `performance-and-caching.md`: Profiling-driven optimization, multi-tier caching (in-memory & distributed Redis/Memcached), cache stampede mitigation, and event-driven cache invalidation.
  - `error-handling-and-logging.md`: Structured JSON logging, correlation IDs (`X-Request-ID`), sensitive credential/PII redaction, and client error sanitization.
  - `backend-security.md`: Zero-trust server boundaries, parameterized SQL queries, SSRF IP/DNS filtering, mass-assignment DTO validation, and timing attack prevention.
  - `production-readiness.md`: Container runtime requirements, separate liveness (`/health/live`) and readiness (`/health/ready`) probes, graceful `SIGTERM` shutdown drains, and worker concurrency tuning.
- **Actionable Checklists & Templates:**
  - `checklists/backend-review-checklist.md`: Engineering review criteria across design, reliability, performance, and operational telemetry.
  - `checklists/backend-security-checklist.md`: Comprehensive security verification gate for backend code changes.
  - `checklists/production-readiness-checklist.md`: Deployment gate for operational health, graceful shutdown, migrations, and alerting.
  - `templates/service-spec-template.md`: Standard specification template for planning new backend services and APIs.
- **Registry & Bundle Membership:** Registered `backend-engineering` in `registry/skills.yaml` and bundled into `engineering-suite` and `complete-suite` in `registry/bundles.yaml`.

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
