---
name: devops-engineering
description: Git workflows, CI/CD pipeline authoring, reproducible builds, containerization, environment hygiene, and infrastructure-as-code safety. Trigger when designing CI/CD workflows, configuring Dockerfiles, provisioning infrastructure, setting up deployment automation, or managing environments.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# DevOps Engineering

## Purpose
`devops-engineering` establishes reliable, automated, reproducible build and deployment workflows. It emphasizes immutable artifacts, minimal container footprints, robust CI testing stages, and strict separation between build-time and run-time environments.

---

## 1. Core DevOps Principles

1. **Infrastructure & Pipeline as Code:**
   - All environment definitions, build stages, and deployment scripts must be versioned in source control.
   - Avoid manual ad-hoc server configuration.

2. **Immutable Build Artifacts:**
   - Build once, test, and promote the exact same binary or container image across development, staging, and production.
   - Inject configuration (URLs, credentials, feature flags) strictly via runtime environment variables.

3. **Production Safety & Explicit Approval:**
   - Autonomous agents must never execute production deployments, terraform apply, or destructive database migrations without explicit human approval.
   - Always ensure an automated rollback path is verified before deploying.

4. **Least Privilege & Secret Protection:**
   - Never burn secrets, tokens, or private keys into Docker images or CI logs.
   - Run containers under unprivileged users (`USER nonroot` or equivalent).

---

## 2. Standard CI/CD Workflow Stages

```
[Lint & Code Hygiene]
          |
          v
[Automated Test Suite (Unit & Integration)]
          |
          v
[Security Scan (SAST & Dependencies)]
          |
          v
[Build Immutable Artifact (Docker / Package)]
          |
          v
[Staging Deployment & Smoke Verification]
          |
          v
[Production Release (Human Gate)]
```

---

## 3. Deliverables & Outputs
1. **Pipeline Configurations:** Tested CI/CD manifests (e.g. GitHub Actions, GitLab CI).
2. **Container Manifests:** Multi-stage, non-root, cache-optimized `Dockerfile` and `docker-compose.yml`.
3. **Rollback Plan:** Documented procedure to revert to the previous known good release in case of failure.
