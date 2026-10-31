# Backend Security Checklist

Use this checklist to verify server-side security boundaries:

- [ ] **Authentication Verification:** Is every private endpoint protected by an explicit server-side authentication guard?
- [ ] **Resource-Level Authorization (IDOR):** Does every database query enforce ownership or tenancy constraints (preventing users from viewing or mutating other tenants' records)?
- [ ] **Role & Permission Checks:** Are administrative or elevated actions guarded by granular permission checks on the server?
- [ ] **SQL Injection Prevention:** Are all database queries parameterized or managed through safe ORM builders (no string concatenation in queries)?
- [ ] **Mass Assignment Protection:** Are request payloads mapped to explicit DTOs or allow-listed fields before persisting to database models?
- [ ] **SSRF Prevention:** If the backend fetches user-supplied URLs, are loopback and private IP ranges (`127.0.0.1`, `10.0.0.0/8`, `192.168.0.0/16`, AWS metadata `169.254.169.254`) blocked?
- [ ] **Path Traversal Protection:** Are uploaded filenames sanitized using basename functions and stored outside public web roots?
- [ ] **Rate Limiting:** Are public login, password reset, and registration endpoints protected by rate limiters?
- [ ] **Password Security:** Are passwords hashed using Argon2id or bcrypt (work factor >= 12)?
- [ ] **Secrets & Configuration:** Are all database credentials and API keys injected via environment variables and excluded from source control?
- [ ] **Error Sanitization:** Are stack traces, database schema details, and internal hostnames stripped from production error responses?

