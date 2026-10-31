---
name: project-onboarding
description: Rapid reconnaissance and mapping of unfamiliar codebases, dependency configurations, and conventions without disruption. Use when exploring new repositories.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Project Onboarding

## Purpose & Activation
`project-onboarding` teaches agents how to rapidly explore, map, and comprehend unfamiliar repositories without disrupting existing code or making unfounded assumptions.

- **Primary Skill For:** Exploring unfamiliar codebases, mapping architectural topology, identifying dependencies, and establishing baseline verification commands.
- **Composition:** Pair with `engineering-core` when onboarding directly precedes making code modifications.
- **Ownership Boundary:** Storing persistent architectural records belongs to `engineering-memory`.

---

## 1. Onboarding Reconnaissance Protocol

Execute systematic reconnaissance in 5 non-destructive stages:

```
[1. Topology & Manifests] -> [2. Runtimes & Dependencies] -> [3. Build & Test Harnesses] -> [4. Entry Points & Seams] -> [5. Architecture Synthesis]
```

1. **Topology & Manifests:**
   - Inspect directory structure and root manifests (`pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`).
   - Identify version control conventions and git history recency (`git log -n 5 --oneline`).
2. **Runtimes & Dependencies:**
   - Identify runtime versions and package managers.
   - Review direct dependencies and note major frameworks (e.g. FastAPI, Next.js, Django, Actix).
3. **Build & Test Tooling:**
   - Locate test frameworks, test directories, and CI pipeline configurations.
   - Run the baseline test suite in a read-only manner to verify passing status.
4. **Entry Points & Critical Seams:**
   - Locate application entry points (CLI entrypoints, web servers, background task queues).
   - Trace core data flow from ingress through service logic to persistence.
5. **Documentation & Memory:**
   - Review `README.md`, `ARCHITECTURE.md`, or `.engineering/` to capture known team conventions.

---

## 2. Reconnaissance Guardrails
- **Strictly Read-Only:** Do not reformat code, add dependencies, or commit files during the onboarding phase.
- **Preserve Conventions:** Note established idioms (typing, error handling, formatting) so subsequent work conforms naturally.

---

## 3. Expected Deliverables
1. **System Overview Summary:** High-level architectural map describing modules, data flows, and runtime tech stack.
2. **Operational Commands:** Verified commands for building, running, and testing the project.
3. **Key Seam Identification:** Pinpointed locations of core business logic, database models, and API boundaries.

---

## 4. Progressive Disclosure (Reference Documents)
Consult these bundled documents only when specific deep guidance is needed:

- **Common repository archetypes and layouts:** Consult [repo-archetypes.md](references/repo-archetypes.md).
- **Comprehensive onboarding checklist:** Consult [onboarding-checklist.md](checklists/onboarding-checklist.md).
- **System overview report template:** Consult [system-overview-template.md](templates/system-overview-template.md).
