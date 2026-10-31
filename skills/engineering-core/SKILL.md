---
name: engineering-core
description: Universal engineering workflow, understand-before-modifying protocol, balanced autonomy, and non-destructive modification standards. Use when starting tasks on existing repos.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Engineering Core

## Purpose & Activation
`engineering-core` establishes universal engineering discipline for autonomous coding agents. It governs pre-modification inspection, calibrated autonomy, minimal invasiveness, and verification standards.

- **Primary Skill For:** General repository maintenance, bug investigations, and engineering tasks requiring balanced autonomy.
- **Composition:** Pair with `software-engineering` for new feature development, or `project-onboarding` when first encountering an unfamiliar codebase.
- **Do Not Activate If:** The task is purely domain-specific (e.g., UI styling alone) where specialized skills suffice.

---

## 1. Understand Before Modifying
Before proposing or applying any code or configuration change:

1. **Repository Structure:** Map top-level directories, source trees, and documentation roots.
2. **Runtime & Languages:** Identify primary languages, compiler/interpreter versions, and package managers (`pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`).
3. **Dependencies & Frameworks:** Review direct dependencies, lockfiles, and active framework patterns.
4. **Conventions & Style:** Respect existing naming schemes, linter configs, formatting rules, and idioms.
5. **Test & Build Tooling:** Locate test harnesses, test commands, and CI workflow configurations.
6. **Security Seams:** Identify auth boundaries, cryptographic keys, database connections, and inputs.
7. **Production Context:** Check container definitions, environment configs, and deployment targets.

> **Rule:** Never introduce an unrequested framework, library, or architectural rewrite. Preserve working code.

---

## 2. Balanced Autonomy Guardrails

| Operation Class | Action | Permitted Autonomy |
|---|---|---|
| **Inspection & Analysis** | Reading repo files, searching symbols, profiling | **Automatic** (No confirmation needed) |
| **Local Verification** | Running tests, linters, static analyzers | **Automatic** (No confirmation needed) |
| **In-Scope Edits** | Editing source files in task scope, updating docs | **Autonomous within task** |
| **Local Commits** | Creating local git commits or local branches | **Follow project convention** |
| **Network Mutations** | Git push, PR creation, external API mutation | **Requires Explicit User Approval** |
| **Infrastructure / Release** | Production deployment, cloud provisioning | **Requires Explicit User Approval** |
| **Data Destruction** | Database drops, volume deletions, truncations | **Requires Explicit User Approval** |

---

## 3. Standard Execution Workflow

```
[Inspect & Understand] -> [Plan Minimal Seam] -> [Verify Baseline] -> [Execute Edit] -> [Verify Tests] -> [Report Evidence]
```

1. **Exploration:** Read relevant docs (`README.md`, `.engineering/`) and recent commits (`git log -n 5 --oneline`).
2. **Minimal Invasiveness:** Plan edits at the exact interface seam. Keep diffs minimal and atomic.
3. **Verification:** Run existing tests before editing. Add regression tests for touched code. Confirm linters pass.

---

## 4. Expected Deliverables
Every completed task must provide:
1. **Summary of Change:** High-level description of what was changed and the technical rationale.
2. **Files Touched:** Complete list of modified, added, or removed file paths.
3. **Verification Evidence:** Terminal output demonstrating passing tests, linting runs, or validation checks.
4. **Residual Risks:** Document any remaining edge cases, performance considerations, or migration requirements.

---

## 5. Progressive Disclosure (Reference Documents)
Consult these bundled documents only when specific deep guidance is needed:

- **Detailed exploration patterns:** Consult [understand-before-modifying.md](references/understand-before-modifying.md).
- **Autonomy boundaries & permissions:** Consult [balanced-autonomy.md](references/balanced-autonomy.md).
- **Pre-change verification:** Consult [pre-modification-checklist.md](checklists/pre-modification-checklist.md).
- **Task completion verification:** Consult [task-completion-checklist.md](checklists/task-completion-checklist.md).
- **Complex debugging log format:** Consult [investigation-log.md](templates/investigation-log.md).
