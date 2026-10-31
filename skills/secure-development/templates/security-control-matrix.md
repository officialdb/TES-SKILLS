# Security Control Matrix

| Component / Boundary | Threat Considered | Implemented Control | Verification Mechanism |
|---|---|---|---|
| User Login Endpoint | Brute force / credential stuffing | Rate limiting + lockout policy | Integration test with 10 requests |
| Profile Image Upload | Malicious executable upload | MIME check, UUID rename, S3 store | Unit test rejecting `.php`/`.py` files |
| SQL Query Layer | SQL Injection | Parameterized query placeholders | Unit test with payload `' OR 1=1 --` |
| Tenant API | Cross-tenant data leakage | Tenant ID filter in DB repository | Multi-tenant integration test |
