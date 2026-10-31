---
name: threat-modeling
description: Structured STRIDE threat modeling, trust boundary identification, and defensive mitigation planning. Use when evaluating system risks or architectural changes.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Threat Modeling

## Purpose & Activation
`threat-modeling` teaches agents how to systematically identify security threats, analyze attack surfaces, evaluate trust boundaries, and formulate mitigations using the STRIDE methodology.

- **Primary Skill For:** Conducting architectural threat assessments, evaluating attack surfaces on new features, and designing mitigation roadmaps.
- **Composition:** Pair with `system-architect` when reviewing new system designs; pair with `security-audit` when analyzing suspected attack vectors.
- **Ownership Boundary:** Forensic code vulnerability assessment belongs to `security-audit`; secure coding implementation belongs to `secure-development`.

---

## 1. The STRIDE Framework
Evaluate every system component, interface, and boundary crossing against the six threat categories:

| Threat | Security Property Violated | Example Attack Scenario | Primary Defense |
|---|---|---|---|
| **Spoofing** | Authenticity | An attacker impersonates a valid user or service | Strong authentication, cryptographic tokens, mTLS |
| **Tampering** | Integrity | Data in transit or database state is unauthorizedly altered | Cryptographic signing, HMACs, TLS, input validation |
| **Repudiation** | Non-Repudiation | A user denies performing an action without audit trail | Append-only audit logs, immutable log stores |
| **Information Disclosure** | Confidentiality | Secrets, PII, or internal stack traces leak to clients | Encryption at rest and in transit, sanitized error responses |
| **Denial of Service** | Availability | Flooding endpoints or consuming database connection pools | Rate limiting, circuit breakers, request timeouts |
| **Elevation of Privilege** | Authorization | A standard user executes admin commands | Server-side RBAC, strict principle of least privilege |

---

## 2. Threat Modeling Workflow

```
[System Decomposition & Trust Boundaries] -> [Apply STRIDE to Crossings] -> [Score & Prioritize Risks] -> [Define Mitigations] -> [Convert to Verification Tests]
```

1. **Decompose the System:** Map external clients, web APIs, internal services, message buses, and data stores.
2. **Draw Trust Boundaries:** Identify perimeter transitions (e.g. public Internet to DMZ, DMZ to internal network, multi-tenant DB).
3. **Analyze Data Flows:** Examine every data flow that crosses a trust boundary against STRIDE.
4. **Prioritize Risks:** Score threats using impact and likelihood to focus engineering effort.
5. **Mitigation & Testing:** Define actionable mitigations that can be verified with automated tests.

---

## 3. Expected Deliverables
1. **Threat Model Document:** System overview demarcating trust boundaries and data flows.
2. **STRIDE Threat Matrix:** Identified threats categorized with severity, affected components, and risk rationale.
3. **Mitigation Roadmap:** Specific architectural controls and automated test definitions addressing high-priority threats.

---

## 4. Progressive Disclosure (Reference Documents)
Consult these bundled documents only when specific deep guidance is needed:

- **STRIDE methodology and attack vectors:** Consult [stride-framework.md](references/stride-framework.md).
- **Threat modeling inspection checklist:** Consult [threat-model-checklist.md](checklists/threat-model-checklist.md).
- **Comprehensive threat model template:** Consult [threat-model-template.md](templates/threat-model-template.md).
