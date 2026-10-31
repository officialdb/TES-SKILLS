---
name: secure-development
description: Security-by-design development practices covering input sanitization, safe auth/RBAC, tenant isolation, SQLi/XSS/SSRF prevention, and secrets handling. Trigger when writing security-sensitive code, authentication systems, authorization rules, or handling user inputs and files.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Secure Development

## Purpose
`secure-development` teaches agents to build software that is secure by default. Rather than relying solely on post-hoc audits, it ensures defensive engineering principles are embedded into architecture and code implementation from day one.

---

## 1. Defensive Engineering Guardrails

1. **Input Validation & Canonicalization:**
   - Validate input against strict allowlists (types, lengths, character sets).
   - Canonicalize paths, URLs, and encodings before checking against security policies.

2. **Parameterized Data Access:**
   - Never concatenate raw user input into SQL queries, ORM fragments, system commands, or template engines.
   - Always use parameterized queries or prepared statements.

3. **Multi-Tenant Isolation & Authorization:**
   - Every database query for tenant data must filter by `tenant_id` at the database layer.
   - Enforce server-side role and permission checks on every single request. Never trust client-provided IDs.

4. **Cryptographic Discipline:**
   - Use standard, battle-tested cryptographic libraries (e.g. `cryptography`, `argon2`, `bcrypt`).
   - Never roll custom encryption algorithms or random generators.

5. **Secrets Hygiene:**
   - Never commit API keys, private certificates, or passwords into source files or version control.
   - Load secrets exclusively from environment variables or dedicated secret managers.

---

## 2. Standard Defenses Against Common Vulnerabilities

- **SQL Injection:** Parameterized queries (`cursor.execute("SELECT ... %s", (val,))`).
- **Path Traversal:** Check `os.path.commonpath([base_dir, resolved_path]) == base_dir`.
- **Command Injection:** Avoid `shell=True` or `exec()`; pass argument lists directly to `subprocess.run(["cmd", arg])`.
- **XSS:** Use contextual auto-escaping templating engines (e.g. React, Jinja2 with autoescape=True).
- **CSRF:** Use SameSite cookie attributes and cryptographic CSRF tokens on state-changing requests.
- **SSRF:** Validate target URLs against an allowlist; block loopback (`127.0.0.1`), metadata services (`169.254.169.254`), and RFC 1918 private subnets.

---

## 3. Deliverables & Outputs
1. **Defensive Code:** Clean implementations with robust bounds checking.
2. **Security Unit Tests:** Tests asserting that malicious payloads (e.g. `../../etc/passwd`, `' OR 1=1 --`) are rejected with clean validation errors.
