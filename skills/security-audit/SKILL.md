---
name: security-audit
description: Evidence-backed vulnerability assessments, OWASP Top 10, CWE pattern recognition, threat classification, and clear remediation guidance. Trigger when performing security reviews, auditing source code for vulnerabilities, analyzing dependencies, or verifying security posture.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Security Audit

## Purpose
`security-audit` teaches agents to conduct rigorous, evidence-based security evaluations across applications, architectures, dependencies, and deployment configurations. It enforces strict standards of proof, distinguishing verified vulnerabilities from theoretical risks.

---

## 1. Core Principles

1. **Evidence-Based Reporting:**
   - Never claim a vulnerability exists without concrete evidence (code snippet, execution trace, configuration flaw).
   - Distinguish confirmed vulnerabilities from suspicious patterns or theoretical concerns.

2. **Actionable Remediation:**
   - Every identified finding must include a clear, minimal, and secure code or configuration fix.

3. **No Secrets Leakage:**
   - Never expose active API keys, database credentials, passwords, or personally identifiable information (PII) in audit reports.

---

## 2. Audit Vectors & OWASP Alignment

Conduct audits across these key vectors:
- **Injection Flaws (A03):** SQL injection, command injection, path traversal, template injection.
- **Broken Authentication & Session Management (A07):** Insecure token storage, weak password hashing, session fixation.
- **Broken Access Control (A01):** Missing authorization checks, Insecure Direct Object References (IDOR), tenant isolation bypass.
- **Cryptographic Failures (A02):** Hardcoded secrets, weak cipher algorithms, missing TLS encryption.
- **Server-Side Request Forgery (SSRF) (A10):** Unvalidated URL fetches, internal network exposure.
- **Vulnerable & Outdated Dependencies (A06):** Known CVEs in libraries.

---

## 3. Standard Audit Workflow

```
[Scope Definition & Reconnaissance]
                 |
                 v
[Static Code & Architecture Review]
                 |
                 v
[Dependency & Configuration Audit]
                 |
                 v
[Evidence Gathering & Verification]
                 |
                 v
[Structured Report with Remediation Guidance]
```

---

## 4. Deliverables & Outputs
For each finding, provide:
- **Identifier & Title:** CWE/OWASP classification.
- **Severity Rating:** Critical, High, Medium, Low, or Informational (with CVSS rationale).
- **Location:** Specific file and line number (`file://path#L10`).
- **Proof of Concept / Evidence:** Exact vulnerable code snippet and exploitation scenario.
- **Remediation:** Step-by-step instructions and secure replacement code.
