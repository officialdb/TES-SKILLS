---
name: secure-development
description: Security-by-design implementation practices covering input sanitization, safe auth, SQLi/XSS/SSRF prevention, and secrets handling. Use when building secure code.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Secure Development

## Purpose & Activation
`secure-development` embeds defensive engineering principles into software during implementation. It ensures code is secure by default against common exploit classes, rather than relying solely on post-hoc audits.

- **Primary Skill For:** Implementing authentication systems, authorization rules, input sanitization, cryptographic operations, and database access.
- **Composition:** Pair with `software-engineering` when building REST APIs or user services; pair with `threat-modeling` when designing new security trust boundaries.
- **Ownership Boundary:** Forensic security reviews and vulnerability evidence reporting belong to `security-audit`.

---

## 1. Defensive Engineering Guardrails

1. **Input Validation & Canonicalization:**
   - Validate external input against strict allowlists (types, lengths, character sets, ranges).
   - Canonicalize file paths, URLs, and encodings before validating against access policies.
2. **Parameterized Data Access:**
   - Never concatenate raw user input into SQL queries, ORM fragments, system commands, or template strings.
   - Always use parameterized queries, prepared statements, or ORM parameter bindings.
3. **Multi-Tenant Isolation & Server-Side Authorization:**
   - Every database query for tenant data must filter by `tenant_id` at the database layer.
   - Enforce server-side role and permission checks on every single request. Never rely on client-asserted identity or roles.
4. **Cryptographic Discipline:**
   - Use standard, battle-tested cryptographic libraries (e.g. `cryptography`, `argon2`, `bcrypt`).
   - Never implement custom encryption algorithms, hashing methods, or pseudo-random generators.
5. **Secrets Hygiene:**
   - Never commit API keys, private certificates, or passwords into source files or version control.
   - Load secrets exclusively from environment variables or dedicated secret managers.

---

## 2. Common Vulnerability Defenses

- **SQL Injection:** Strict parameterized binding (`cursor.execute("SELECT ... WHERE id = %s", (user_id,))`).
- **Path Traversal:** Validate paths using `os.path.commonpath([base_dir, resolved_path]) == base_dir`.
- **Command Injection:** Avoid `shell=True` or `exec()`; pass explicit argument lists to `subprocess.run(["cmd", arg])`.
- **XSS:** Use contextual auto-escaping templating engines (e.g. React JSX, Jinja2 autoescape).
- **CSRF:** Enforce `SameSite=Lax` or `Strict` cookies and cryptographic anti-CSRF tokens for state-changing endpoints.
- **SSRF:** Validate target URLs against an explicit domain allowlist; block loopback (`127.0.0.1`), cloud metadata (`169.254.169.254`), and RFC 1918 private subnets.

---

## 3. Expected Deliverables
1. **Defensive Implementation:** Production code with robust bounds checking and boundary defenses.
2. **Security Unit Tests:** Automated regression tests demonstrating that malicious payloads (e.g. `../../etc/passwd`, `' OR 1=1 --`) are rejected with clean validation errors.

---

## 4. Progressive Disclosure (Reference Documents)
Consult these bundled documents only when specific deep guidance is needed:

- **Defense-in-depth architectural patterns:** Consult [defense-in-depth.md](references/defense-in-depth.md).
- **Pre-commit secure development checks:** Consult [secure-coding-checklist.md](checklists/secure-coding-checklist.md).
- **Security controls and threat mapping:** Consult [security-control-matrix.md](templates/security-control-matrix.md).
