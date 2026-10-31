---
name: deployment-verification
description: Post-deployment smoke testing, canary verification, synthetic transactions, and rollback validation. Use when validating deployed releases or staging environments.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Deployment Verification

## Purpose & Activation
`deployment-verification` teaches agents to execute structured post-deployment health checks, canary validations, synthetic transactions, and rollback verifications to ensure releases function correctly in target environments.

- **Primary Skill For:** Verifying freshly deployed applications, running post-release smoke tests, validating staging environments, and confirming rollback readiness.
- **Composition:** Pair with `devops-engineering` as the final stage of an automated deployment pipeline.
- **Ownership Boundary:** Authoring CI/CD pipelines and container builds belongs to `devops-engineering`.

---

## 1. Post-Deployment Verification Protocol

```
[Deploy Execution] -> [Infrastructure Health] -> [Static Assets & SSL] -> [Synthetic Transactions] -> [Canary Analysis] -> [Sign-off / Rollback]
```

1. **DNS & Transport:** Confirm target domain resolves and TLS/SSL certificate is valid and not expired.
2. **HTTP Ingress & Assets:** Verify `/healthz` or status endpoint returns HTTP 200; verify core static asset bundles load with appropriate caching headers.
3. **Database & Cache Connectivity:** Verify application reads and writes to backend datastores without timeout.
4. **Synthetic User Flow:** Execute an automated synthetic transaction covering the primary user journey (e.g. login, query, item creation).
5. **Telemetry & Error Budgets:** Monitor logs and error tracking for spike in HTTP 5xx errors or unhandled exceptions.

---

## 2. Rollback Triggers & Safety
- **Immediate Rollback Trigger:** Trigger automated or human-alerted rollback if:
  - The health check endpoint fails consecutively for 60 seconds.
  - HTTP 5xx error rate exceeds 1% of total requests.
  - P99 latency degrades by more than 2x baseline.
- **Data Safety:** Never execute destructive schema migrations without a verified zero-downtime rollback path.

---

## 3. Expected Deliverables
1. **Verification Report:** Structured sign-off documenting each verification check and result.
2. **Latency & Error Metrics:** Baseline measurements captured during the verification window.
3. **Rollback Plan Status:** Confirmed active rollback path in case of post-cutover regression.

---

## 4. Progressive Disclosure (Reference Documents)
Consult these bundled documents only when specific deep guidance is needed:

- **Smoke testing patterns and canary analysis:** Consult [smoke-testing-patterns.md](references/smoke-testing-patterns.md).
- **Post-deployment inspection checklist:** Consult [post-deployment-checklist.md](checklists/post-deployment-checklist.md).
- **Formal verification report template:** Consult [deployment-verification-report.md](templates/deployment-verification-report.md).
