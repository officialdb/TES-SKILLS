# Reference: Server-Side Security & Threat Mitigation

## 1. Fundamental Principle: Zero Trust at the Server Boundary

Never trust client-side validation as a security mechanism. Every authentication, authorization, input validation, and business rule constraint must be enforced authoritatively on the server.

## 2. Server-Side Vulnerability Mitigation

### SQL Injection (SQLi)
- Always use parameterized queries or ORM abstractions.
- Never concatenate user strings directly into SQL statements:
  ```python
  # VULNERABLE
  cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")

  # SECURE (Parameterized)
  cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
  ```

### Server-Side Request Forgery (SSRF)
When the backend makes outbound HTTP requests based on user-supplied URLs (webhooks, avatar imports):
- Validate the URL against an explicit allowed scheme (`https://`).
- Resolve the target IP address before connecting and reject private / loopback IP ranges (`127.0.0.1`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.169.254` AWS metadata endpoint).
- Disable automatic redirect following on untrusted outbound requests.

### Insecure Direct Object References (IDOR)
- Never rely solely on an entity's primary key (`id`) from a URL or body payload without validating that the authenticated session owns that record.
- Always include tenant / user ownership constraints in query filters (`filter(id=req_id, organization_id=current_user.org_id)`).

### Mass Assignment & Over-Posting
- Restrict incoming payloads to strictly defined DTO fields or explicit ORM allow-lists.
- Prevent malicious clients from injecting elevated permissions (e.g. `{"is_admin": true, "role": "superuser"}`).

### Path Traversal & File Upload Security
- When accepting filenames from users, sanitize using safe basename functions (e.g. `os.path.basename(filename)`).
- Validate uploaded file MIME types using magic byte inspection (e.g. `python-magic`) rather than relying on the client-supplied `Content-Type` header or file extension.
- Store uploaded files outside the web root or upload directly to secure cloud object storage (S3, GCS) with randomized UUID keys.

### Rate Limiting & DoS Mitigation
- Implement token-bucket or sliding-window rate limiting on all public authentication endpoints (`/login`, `/register`, `/password-reset`, `/oauth/token`).
- Return `429 Too Many Requests` with a `Retry-After` header when limits are exceeded.

## 3. Secrets Management & Configuration Safety
- Never check credentials, private keys, database passwords, or API tokens into Git source control.
- Inject secrets via environment variables or cloud secret managers (AWS Secrets Manager, HashiCorp Vault).
- Verify that `.gitignore` excludes `.env` and local credential files.

