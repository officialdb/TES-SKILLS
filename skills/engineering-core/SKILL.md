---
name: engineering-core
description: Fundamental software engineering principles, understand-before-modifying protocol, balanced autonomy, quality gates, and non-destructive modification standards. Trigger when starting tasks on existing repositories, designing architecture, modifying codebases, or establishing engineering guardrails.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Engineering Core

## Purpose
`engineering-core` instills foundational engineering discipline into autonomous coding agents. It ensures that agents understand the existing system prior to making changes, operate within calibrated autonomy boundaries, preserve working functionality, and verify every step.

---

## 1. The Prime Directive: Understand Before Modifying

Before proposing or executing any code or configuration change:

1. **Repository Structure Inspection:** Map out top-level folders, source trees, configuration roots, and documentation.
2. **Languages & Runtime Environment:** Identify primary languages, compiler/interpreter versions, and package managers (e.g., Python `pyproject.toml`, Node `package.json`, Go `go.mod`, Rust `Cargo.toml`).
3. **Dependency & Framework Topography:** Review direct dependencies, lockfiles, and framework paradigms.
4. **Existing Architecture & Conventions:** Determine modular boundaries, naming schemes, linter configs, formatting conventions, and architectural styles.
5. **Testing & Tooling Topography:** Identify test frameworks, test suites, coverage setups, build scripts, and CI workflows.
6. **Security-Sensitive Seams:** Locate authentication mechanisms, cryptographic keys, database connections, and ingress/egress validation.
7. **Production Context:** Check environment configs, container definitions, and cloud deployment manifests.

> **Rule:** Never impose an arbitrary new framework, library, or architectural rewrite unless explicitly mandated by the user. Preserve working software.

---

## 2. Balanced Autonomy Guardrails

Agents must exercise calibrated autonomy:

| Operation Class | Action | Permitted Autonomy |
|---|---|---|
| **Inspection & Analysis** | Reading repo files, searching symbols, profiling | **Automatic** (No confirmation needed) |
| **Local Verification** | Running unit tests, linters, static analyzers | **Automatic** (No confirmation needed) |
| **Task-authorized Edits** | Editing source files in task scope, updating docs | **Autonomous within task** |
| **Version Control Commits**| Creating local commits or local branches | **Follow project convention** |
| **Network Mutations** | Git push, PR creation, external API mutation | **Requires Explicit Approval** |
| **Infrastructure & Release**| Production deployment, Terraform apply | **Requires Explicit Human Approval** |
| **Data Destruction** | Database drops, truncations, volume removals | **Requires Explicit Human Approval** |

---

## 3. Standard Execution Workflow

```
[Inspect & Understand]
         |
         v
[Hypothesize & Plan Seam]
         |
         v
[Verify Test Baseline]
         |
         v
[Execute Minimal Change]
         |
         v
[Run Tests & Static Checks]
         |
         v
[Report Results & Evidence]
```

### Phase A: Exploration
- Read existing documentation (`README.md`, `ARCHITECTURE.md`, `.engineering/`).
- Inspect recent commits to understand ongoing work (`git log -n 5 --oneline`).
- Formulate a precise understanding of the bug or feature request.

### Phase B: Planning & Minimal Invasiveness
- Identify the exact interface seam where the modification belongs.
- Choose the simplest solution that fulfills the requirement without overengineering.
- Consult `references/understand-before-modifying.md` and check `checklists/pre-modification-checklist.md`.

### Phase C: Implementation & Verification
- Make atomic, cohesive edits. Do not modify unrelated whitespace or reformat intact files.
- Run tests before completing the task.
- If no tests exist for the touched seam, write unit or integration tests that prove correctness and prevent regressions.

---

## 4. Deliverables & Outputs
At the conclusion of any task, provide:
1. **Summary of Change:** High-level description of what was changed and why.
2. **Files Touched:** Specific file paths modified or created.
3. **Verification Evidence:** Terminal output showing passing test suites, linting runs, or validation checks.
4. **Residual Risks / Follow-up:** Any edge cases, performance considerations, or migration steps.
