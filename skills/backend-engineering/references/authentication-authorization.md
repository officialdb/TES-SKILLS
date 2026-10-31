# Reference: Authentication, Authorization & Identity Control

## 1. Authentication vs. Authorization

Maintain a strict conceptual and architectural separation:
- **Authentication (AuthN):** *Who is the client?* Verifies identity through credentials, sessions, tokens, or cryptographic signatures.
- **Authorization (AuthZ):** *What is the authenticated identity permitted to do?* Verifies permissions, roles, ownership, and scope for a specific resource and action.

An authenticated identity must **never** automatically be presumed authorized to access arbitrary resources.

## 2. Authentication Implementations

### Session-Based Authentication (Stateful)
- Standard for server-rendered web applications and first-party monolithic frontends.
- Store session IDs in secure HTTP-only, SameSite cookies (`Secure; HttpOnly; SameSite=Lax`).
- Back session state with high-speed key-value stores (Redis) or relational databases with automatic TTL expiration.
- Implement explicit session revocation upon logout, password change, or suspicious activity.

### Token-Based Authentication (Stateless / Hybrid JWT)
- Common for distributed services, native mobile apps, and decoupled SPAs.
- Sign tokens using asymmetric keys (RS256, EdDSA) so microservices can verify without accessing private signing secrets.
- Keep access tokens short-lived (5–15 minutes). Use revocable refresh tokens stored securely for session extension.
- Implement token revocation via revocation lists (Redis bloom filters or blacklists) or rotating token families.

### Password Hashing Standards
- Always use modern, memory-hard key derivation functions: **Argon2id** (preferred) or **bcrypt** (work factor >= 12).
- Never use MD5, SHA-1, SHA-256, or plain cryptographic digests for password storage.

## 3. Authorization Models

### Role-Based Access Control (RBAC)
- Map permissions to roles (e.g. `admin`, `editor`, `viewer`), and assign roles to users.
- Check granular permissions in code (`user.can('posts.publish')`) rather than hardcoding role checks (`user.role == 'admin'`).

### Resource-Level Authorization & IDOR Prevention
Insecure Direct Object Reference (IDOR) occurs when an endpoint accepts a resource ID from user input without verifying that the requesting identity owns or has access to that specific record.

- **Bad (Vulnerable to IDOR):**
  ```python
  # Fetches order by ID without checking tenant/owner
  order = db.query(Order).filter(Order.id == order_id).first()
  ```
- **Good (Scoped Query):**
  ```python
  # Scopes query strictly to authenticated user's organization
  order = db.query(Order).filter(
      Order.id == order_id,
      Order.organization_id == current_user.org_id
  ).first_or_404()
  ```

### Multi-Tenant Data Isolation
- Enforce tenancy boundaries at the query layer via global query scopes, tenant middleware, or schema isolation.
- Every read, update, and delete operation must explicitly scope to the authenticated tenant.

