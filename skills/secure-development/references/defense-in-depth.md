# Reference: Defense in Depth for Software Engineers

## The Multi-Layer Strategy
No single security control is infallible. Systems must employ redundant defenses:
1. **Network Layer:** WAF, TLS termination, reverse proxy rate limiting.
2. **Application Boundary:** Schema validation, CSRF middleware, authentication checks.
3. **Domain Layer:** Business invariant enforcement, RBAC/ABAC authorization checks.
4. **Data Persistence Layer:** Parameterized queries, least-privilege DB users, encryption at rest.
