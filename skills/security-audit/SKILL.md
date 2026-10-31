---
name: security-audit
description: Audit applications for security vulnerabilities, misconfigurations and attack surfaces. Use when performing security assessments or investigating suspected vulnerabilities.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Security Audit

## Purpose & Activation
`security-audit` directs agents to conduct rigorous, evidence-based security evaluations across code, dependencies, architecture, and configurations. It enforces strict standards of proof, distinguishing verified vulnerabilities from theoretical risks.

- **Primary Skill For:** Auditing source code for security flaws, evaluating dependency CVEs, reviewing configuration risks, and verifying security posture.
- **Composition:** Pair with `threat-modeling` when investigating potential attack vectors; pair with `code-review` when conducting security-focused PR reviews.
- **Ownership Boundary:** Implementing defensive features belongs to `secure-development`.

---

## 1. Core Principles

1. **Evidence-Based Reporting:**
   - Never claim a vulnerability exists without concrete evidence (code snippet, execution trace, or configuration flaw).
   - Distinguish verified vulnerabilities from suspicious patterns or theoretical concerns.
2. **Actionable Remediation:**
   - Every identified finding must include a clear, minimal, and secure code or configuration remediation.
3. **No Secrets Leakage:**
   - Never expose active API keys, database credentials, passwords, or personally identifiable information (PII) in audit reports.

---

## 2. Audit Vectors & OWASP Alignment
Conduct audits across primary security vectors:
- **Injection Flaws (A03):** SQL injection, command injection, path traversal, template injection.
- **Broken Access Control (A01):** Missing authorization checks, Insecure Direct Object References (IDOR), tenant isolation bypass.
- **Broken Authentication & Sessions (A07):** Insecure token handling, weak password hashing, session fixation.
- **Cryptographic Failures (A02):** Hardcoded credentials, weak ciphers, unencrypted data in transit.
- **Server-Side Request Forgery (SSRF) (A10):** Unvalidated URL fetches and internal network probing.
- **Vulnerable Dependencies (A06):** Known CVEs in third-party libraries.

---

## 3. Standard Audit Workflow

```
[Scope Definition] -> [Static Code Review] -> [Dependency & Config Audit] -> [Evidence Verification] -> [Remediation Report]
```

---

## 4. Expected Deliverables
For each identified vulnerability, provide:
1. **Identifier & Classification:** CWE/OWASP classification.
2. **Severity Rating:** Critical, High, Medium, Low, or Informational with CVSS justification.
3. **Exact Location:** Specific file path and line number reference (`file://path#L10`).
4. **Proof of Concept / Evidence:** Vulnerable code snippet and concrete exploitation scenario.
5. **Remediation:** Step-by-step instructions and secure replacement code.

---

## 5. Progressive Disclosure (Reference Documents)
Consult these bundled documents only when specific deep guidance is needed:

- **CWE/CVSS classification methodology:** Consult [vulnerability-classification.md](references/vulnerability-classification.md).
- **Comprehensive security audit checklist:** Consult [security-audit-checklist.md](checklists/security-audit-checklist.md).
- **Formal vulnerability report structure:** Consult [vulnerability-report.md](templates/vulnerability-report.md).
