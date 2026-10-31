---
name: threat-modeling
description: Structured STRIDE threat modeling, trust boundary identification, attack vector mapping, and defensive mitigation planning. Trigger when designing new system features, reviewing architectural changes, evaluating third-party integrations, or performing security risk assessments.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Threat Modeling

## Purpose
`threat-modeling` teaches agents how to systematically identify security threats, analyze attack surfaces, evaluate trust boundaries, and formulate mitigations using the STRIDE methodology.

---

## 1. The STRIDE Framework

Evaluate every component and interface against the six core threat categories:

| Threat | Security Property Violated | Example Scenario | Primary Defense |
|---|---|---|---|
| **S**poofing | Authenticity | Attacker impersonates another user or service | Strong authentication, mTLS, signed JWTs |
| **T**ampering | Integrity | Attacker modifies data in transit or at rest | Cryptographic signatures, checksums, HMAC |
| **R**epudiation | Non-repudiability | User denies performing an action | Tamper-evident audit logging |
| **I**nformation Disclosure | Confidentiality | Sensitive data or secrets leaked to unauthorized parties | Encryption (TLS, AES-GCM), data redaction |
| **D**enial of Service | Availability | System overwhelmed or crashed by malicious input | Rate limiting, timeouts, resource caps |
| **E**levation of Privilege | Authorization | Unprivileged user gains administrator rights | Server-side RBAC, principle of least privilege |

---

## 2. Threat Modeling Workflow

```
[1. Deconstruct the System]
           |
           v
[2. Identify Trust Boundaries & Data Flows]
           |
           v
[3. Enumerate Threats via STRIDE]
           |
           v
[4. Score Risk & Formulate Mitigations]
           |
           v
[5. Validate Mitigations in Implementation]
```

### Step 1: Deconstruct System
- Identify external entities (users, third-party APIs), processes (API servers, background workers), data stores (databases, caches), and data flows.

### Step 2: Draw Trust Boundaries
- Mark where data crosses from an untrusted zone (e.g. public Internet) to a trusted zone (e.g. internal VPC). Every crossing point requires authentication, authorization, and validation.

### Step 3: Enumerate Threats
- Apply STRIDE systematically to each interaction crossing a trust boundary.

### Step 4: Mitigate and Verify
- Propose concrete, engineering-led controls to eliminate or mitigate each threat.

---

## 3. Deliverables & Outputs
Produce a structured **Threat Model Document**:
1. **Data Flow Diagram / Architecture Description:** Explicit trust boundaries.
2. **Threat Table:** Classified using STRIDE with risk ratings.
3. **Mitigation Plan:** Exact architectural or code changes required.
