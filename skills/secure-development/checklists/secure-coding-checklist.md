# Secure Coding Checklist

- [ ] Are all database operations strictly parameterized?
- [ ] Is input validated against a strict allowlist (length, character set, format)?
- [ ] Are file operations protected against path traversal (`..` and symlink escape)?
- [ ] Are subprocess calls invoked without `shell=True`?
- [ ] Are passwords hashed using Argon2id or Bcrypt with work factors?
- [ ] Are API tokens generated using cryptographically secure random generators (`secrets` module)?
- [ ] Are authorization checks performed server-side for every requested object?
- [ ] Are errors sanitized to prevent leaking stack traces or internal paths to clients?
