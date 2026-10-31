---
name: backend-engineering
version: 1.0.0
description: Production backend architecture, business services, API lifecycle, persistence integration, background tasks, and security boundaries. Use for backend systems.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Backend Engineering

## Purpose & Activation
`backend-engineering` guides coding agents in designing, implementing, reviewing, testing, and maintaining production-grade backend systems. It emphasizes framework-independent architectural discipline, robust business logic encapsulation, secure persistence patterns, and reliable asynchronous operations across Python (FastAPI, Django, Flask), PHP (Laravel, Symfony), JavaScript/TypeScript (Node.js, Express, NestJS, Fastify), Java (Spring Boot), and other backend runtimes.

- **Primary Skill For:** Building API endpoints, structuring service layers, managing database transactions, configuring background queues, securing backend boundaries, and optimizing server performance.
- **Composition:** Pair with `system-architect` for high-level domain boundaries; pair with `testing-strategy` for test suite design; pair with `secure-development` for specialized threat mitigation; pair with `devops-engineering` for deployment infrastructure.
- **Ownership Boundary:** High-level system topology and ADRs belong to `system-architect`; client-side rendering and Web Vitals belong to `frontend-quality`; CI/CD runner pipelines belong to `devops-engineering`.

---

## 1. Project-Aware Engineering Workflow
Before writing or modifying backend code, execute this systematic process:
1. **Stack & Convention Discovery:** Identify the backend language, framework, ORM, and dependency manager. Inspect repository layout and adhere to existing naming and layering conventions.
2. **Entry Points & Request Flow:** Trace the request lifecycle from routing/controllers through validation middleware, service orchestrators, persistence layers, and response serializers.
3. **Data & State Inspection:** Examine database schemas, active migrations, transaction boundaries, connection pooling settings, and caching layers.
4. **Security & Boundary Analysis:** Verify server-side authentication, role/permission authorization, tenant isolation, and sensitive field redaction. Never rely on frontend validation.
5. **Architectural Alignment:** Choose patterns matching actual project requirements. Avoid forcing microservices, clean architecture, or repository patterns onto cohesive modular monoliths.
6. **Minimal, Test-Backed Implementation:** Implement the smallest cohesive change. Write unit and integration tests covering happy paths, edge cases, and failure scenarios.

---

## 2. Core Backend Disciplines

1. **Architecture & Service Boundaries:**
   - Enforce separation of concerns: controllers handle HTTP parsing and status codes; services encapsulate business logic and transactions; repositories/models manage persistence.
   - Keep business rules out of route handlers, database triggers, and UI components.
2. **Request Lifecycle & API Engineering:**
   - Validate and sanitize external input at the HTTP boundary. Return uniform, predictable response envelopes with semantic HTTP status codes (200, 201, 400, 401, 403, 404, 409, 422, 500).
   - Implement cursor or offset pagination, deterministic sorting, filtering, and strict request size limits on file uploads.
3. **Authentication & Authorization:**
   - Separate authentication (verifying identity via sessions, JWTs, or OAuth2/OIDC) from authorization (verifying permissions and tenant ownership).
   - Enforce resource-level authorization on every mutation and retrieval to prevent Insecure Direct Object References (IDOR).
4. **Persistence & Data Integrity:**
   - Execute multi-table mutations inside atomic database transactions with appropriate isolation levels.
   - Eliminate N+1 query antipatterns via eager loading (`select_related`, `with`, `include`). Manage connection pooling and concurrency safely.
5. **Asynchronous Jobs & Background Queues:**
   - Offload long-running operations (emails, webhooks, heavy exports) to background worker queues.
   - Ensure background tasks are idempotent, implement exponential backoff retries, and route unrecoverable failures to dead-letter queues.
6. **Logging, Observability & Error Handling:**
   - Emit structured JSON logs with correlation IDs. Redact secrets, tokens, passwords, and PII.
   - Catch unexpected exceptions gracefully and return sanitized error responses without leaking internal stack traces or database errors.

---

## 3. Expected Deliverables
1. **Production Backend Implementation:** Idiomatic, cleanly layered, fully typed server code matching codebase conventions.
2. **Automated Test Coverage:** Integration and unit tests verifying business rules, boundary validations, and security authorization checks.
3. **Database Migration & Schema Alignment:** Deterministic schema migrations and entity models.
4. **Execution Evidence:** Verification that linters, tests, and database migrations pass cleanly without regressions.

---

## 4. Progressive Disclosure (Reference Documents)
Consult these bundled documents only when specific deep guidance is needed:

- **Architectural patterns and layering:** Consult [backend-architecture.md](references/backend-architecture.md).
- **HTTP request lifecycle and API design:** Consult [api-and-http.md](references/api-and-http.md).
- **Authentication, RBAC, and IDOR prevention:** Consult [authentication-authorization.md](references/authentication-authorization.md).
- **Service layer and business logic encapsulation:** Consult [business-logic.md](references/business-logic.md).
- **Database persistence, transactions, and N+1 prevention:** Consult [persistence-integration.md](references/persistence-integration.md).
- **Background queues, workers, and idempotency:** Consult [background-processing.md](references/background-processing.md).
- **Caching strategies and query performance:** Consult [performance-and-caching.md](references/performance-and-caching.md).
- **Structured logging, correlation, and exception handling:** Consult [error-handling-and-logging.md](references/error-handling-and-logging.md).
- **Server-side vulnerability prevention and defense in depth:** Consult [backend-security.md](references/backend-security.md).
- **Health checks, graceful shutdown, and zero-downtime readiness:** Consult [production-readiness.md](references/production-readiness.md).
- **Pre-merge backend code review checklist:** Consult [backend-review-checklist.md](checklists/backend-review-checklist.md).
- **Backend security audit checklist:** Consult [backend-security-checklist.md](checklists/backend-security-checklist.md).
- **Production deployment readiness checklist:** Consult [production-readiness-checklist.md](checklists/production-readiness-checklist.md).
- **Backend service specification template:** Consult [service-spec-template.md](templates/service-spec-template.md).

