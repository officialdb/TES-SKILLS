# Reference: CI/CD Pipeline Standards

## Fast Feedback Loop
CI pipelines must run fast. Developers should receive feedback within 5-10 minutes.
- Cache dependencies (`~/.cache/pip`, `node_modules`, `~/.cargo`).
- Run linting and unit tests in parallel jobs.
- Fail fast on syntax or formatting errors before expensive integration builds.

## Container Hardening Rules
1. **Multi-stage builds:** Use builder stages for compilers and dev dependencies; copy only final artifacts into minimal runtime base images (e.g. `alpine`, `distroless`, `slim`).
2. **Explicit non-root user:** Add a dedicated unprivileged user (`RUN useradd -u 1000 app && USER app`).
3. **Pin base image digests or explicit tags:** Never use `latest`.
