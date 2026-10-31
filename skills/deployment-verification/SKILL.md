---
name: deployment-verification
description: Post-deployment smoke testing, canary health checks, synthetic transactions, zero-downtime rollback strategies, and cutover validation. Trigger when verifying a newly deployed application, running post-release smoke tests, validating staging environments, or testing rollbacks.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Deployment Verification

## Purpose
`deployment-verification` teaches agents how to execute structured post-deployment health checks, canary verifications, synthetic transactions, and rollback validations to guarantee that releases are functioning correctly in target environments.

---

## 1. Post-Deployment Verification Protocol

```
[Deploy Execution]
         |
         v
[Stage 1: Infrastructure & Service Liveness] -> (Ping /healthz, check container state)
         |
         v
[Stage 2: Critical Path Smoke Tests]        -> (Synthetic user login, core API query)
         |
         v
[Stage 3: Telemetry & Error Log Monitoring] -> (Error rate <0.1%, latency within budget)
         |
         +----------------------------------+
         |                                  |
    (Checks Pass)                     (Checks Fail)
         |                                  |
         v                                  v
  [Sign-off Release]             [Trigger Immediate Rollback]
```

---

## 2. Core Verification Techniques

1. **Liveness & Readiness Probing:**
   - Verify `/healthz` (service alive) and `/readyz` (database, cache, and dependent microservices reachable).

2. **Synthetic End-to-End Transactions:**
   - Execute non-destructive synthetic transactions (e.g. read an existing public item, test test-account authentication).
   - Never inject polluting test data into production user accounts.

3. **Telemetry & Log Scrubbing:**
   - Monitor application logs for spike in 5xx HTTP codes or unhandled exceptions.
   - Ensure logs never print API keys, user passwords, or confidential tokens.

4. **Rollback Preparedness:**
   - Every deployment must have a verified rollback path (e.g. previous Docker image tag or previous git release).
   - If smoke tests fail, execute rollback before users encounter broad outage.

---

## 3. Deliverables & Outputs
Produce a **Deployment Verification Report**:
1. **Target Environment:** Staging, Canary, or Production URL.
2. **Release Version / Commit:** Deployed commit hash and tag.
3. **Verification Results:** Liveness checks, smoke test outcomes, and latency metrics.
4. **Final Status:** VERIFIED SUCCESS or ROLLBACK REQUIRED.
