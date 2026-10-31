# Threat Model: [Feature / System Name]

**Date:** YYYY-MM-DD  
**Authors:** [Engineers / AI Agent]  
**Scope:** [Target service, feature, or integration]  

---

## 1. System Overview & Boundaries
- **External Entities:** Users, Browser, Stripe API
- **Processes:** FastAPI Application Server, Celery Worker
- **Data Stores:** PostgreSQL Database, Redis Cache
- **Trust Boundaries:**
  - Public Internet <-> API Gateway
  - API Gateway <-> Private VPC

---

## 2. Threat Analysis Table

| ID | Boundary / Flow | STRIDE Category | Threat Description | Severity | Planned Mitigation |
|---|---|---|---|---|---|
| T-01 | Browser -> Auth API | Spoofing | Credential stuffing on login | High | Rate limit + CAPTCHA |
| T-02 | Client -> File Upload | Tampering | Malicious executable upload | High | Check MIME + strip metadata |
| T-03 | Webhook -> Ingress | Repudiation | Stripe event forged | High | Verify Stripe HMAC signature |
| T-04 | User -> Search API | DoS | Expensive wildcard regex queries | Med | Query timeout + pagination |
