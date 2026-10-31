---
name: project-onboarding
description: Rapid comprehension and mapping of unknown codebases, dependency configurations, frameworks, test setups, and conventions without disruption. Trigger when encountering a new codebase, joining an existing project, or producing initial architecture summaries.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Project Onboarding

## Purpose
`project-onboarding` teaches agents how to rapidly explore, map, and comprehend unfamiliar repositories without disrupting existing code or making unfounded assumptions.

---

## 1. Onboarding Reconnaissance Protocol

Perform systematic reconnaissance in 5 stages:

```
[1. Topology & Manifests] -> [2. Runtimes & Dependencies] -> [3. Build & Test Harnesses]
                                                                     |
                                                                     v
                                     [5. Onboarding Dossier] <- [4. Architecture & Entry Points]
```

### Stage 1: Directory Topology
- Scan root directories. Ignore noisy folders (`node_modules`, `.git`, `__pycache__`, `venv`, `dist`, `build`).
- Identify documentation roots (`docs/`, `README.md`, `ARCHITECTURE.md`, `.engineering/`).

### Stage 2: Runtimes & Package Managers
- Identify package manifests (`pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`).
- Read runtime engine versions (e.g. `.nvmrc`, `.python-version`, Dockerfile).

### Stage 3: Test and Quality Harness
- Locate test runner configs (`pytest.ini`, `jest.config.js`, `Makefile`).
- Run dry-run or quick test commands to verify test baseline.

### Stage 4: Entry Points & Key Data Flows
- Locate application entry points (`main.py`, `src/index.ts`, `cmd/server/main.go`).
- Trace request flow: Route -> Handler -> Service/Domain -> Repository -> Database.

### Stage 5: Security & Infrastructure
- Review `.env.example` or deployment descriptors for external dependencies (Redis, Postgres, S3).

---

## 2. Deliverables & Outputs
Produce an initial **Project Onboarding Dossier**:
1. **Core Purpose:** 1-sentence product summary.
2. **Tech Stack:** Languages, frameworks, primary database, caching layer.
3. **Run Commands:** How to install, run locally, test, and lint.
4. **Critical Modules:** Map of core packages and their responsibilities.
5. **Key Invariants & Gotchas:** Non-standard conventions or known constraints.
