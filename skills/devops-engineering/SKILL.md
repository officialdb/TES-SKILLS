---
name: devops-engineering
description: CI/CD automation, reproducible builds, container hardening, and infrastructure-as-code safety. Use when authoring pipelines, Dockerfiles, or deployment workflows.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# DevOps Engineering

## Purpose & Activation
`devops-engineering` establishes reliable, automated, reproducible build and deployment workflows. It emphasizes immutable artifacts, minimal container footprints, robust CI testing stages, and strict separation between build-time and runtime environments.

- **Primary Skill For:** Authoring CI/CD pipelines, Dockerfiles, container configurations, build automation scripts, and infrastructure-as-code manifests.
- **Composition:** Pair with `deployment-verification` when orchestrating complete deployment workflows; pair with `security-audit` when scanning pipelines for secrets or CVEs.
- **Ownership Boundary:** Post-deployment smoke testing and rollback validation belong to `deployment-verification`.

---

## 1. Core DevOps Principles

1. **Infrastructure & Pipeline as Code:**
   - All environment definitions, build stages, and deployment scripts must be versioned in source control.
   - Avoid manual ad-hoc server configuration.
2. **Container Hardening:**
   - Use multi-stage Docker builds to separate compiler toolchains from final minimal runtime images (e.g. `distroless`, `alpine`, `slim`).
   - Run containers under an explicit unprivileged user (`USER app`). Never run application containers as root.
   - Pin base image tags or SHA-256 digests; avoid mutable `latest` tags.
3. **Fast Feedback Loops:**
   - Keep CI runs under 10 minutes by caching dependency stores (`pip`, `node_modules`, `cargo`).
   - Run linters, unit tests, and security scans in parallel jobs. Fail early on fast syntax or formatting errors.
4. **Environment Hygiene:**
   - Strict separation between development, staging, and production configurations.
   - Inject secrets exclusively at runtime via environment variables or secret vaults.

---

## 2. Safety & Autonomy Guardrail
- Autonomous agents may inspect, author, lint, and test pipeline configs and Dockerfiles locally.
- **Explicit Approval Required:** Triggering remote production deployments, modifying cloud infrastructure, or deleting remote resources requires explicit human authorization.

---

## 3. Expected Deliverables
1. **Pipeline Definitions:** Tested, reproducible CI/CD configurations (e.g. GitHub Actions, GitLab CI).
2. **Hardened Container Manifests:** Multi-stage, unprivileged Dockerfiles with `.dockerignore` hygiene.
3. **Execution Evidence:** Successful local linting, build runs, or test pipeline execution logs.

---

## 4. Progressive Disclosure (Reference Documents)
Consult these bundled documents only when specific deep guidance is needed:

- **CI/CD pipeline standards and caching:** Consult [cicd-pipeline-standards.md](references/cicd-pipeline-standards.md).
- **Production readiness checklist:** Consult [production-readiness-checklist.md](checklists/production-readiness-checklist.md).
- **Reference CI workflow template:** Consult [github-actions-ci.yml](templates/github-actions-ci.yml).
