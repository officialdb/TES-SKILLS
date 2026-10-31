# Backend Code Review Checklist

Use this checklist when creating or reviewing backend pull requests:

- [ ] **Architecture & Layering:** Are business rules cleanly isolated in application services rather than scattered in route controllers or database triggers?
- [ ] **API Contract:** Are response envelopes consistent, and do HTTP status codes accurately reflect outcomes (200, 201, 204, 400, 401, 403, 404, 409, 422)?
- [ ] **Input Validation:** Is all external input strictly validated and sanitized before reaching domain logic?
- [ ] **Database Hygiene:** Are database queries eager-loaded to prevent N+1 query performance problems?
- [ ] **Transaction Boundaries:** Are multi-table mutations wrapped in atomic database transactions?
- [ ] **No Slow Calls in Transactions:** Are slow external HTTP requests executed outside open database transaction blocks?
- [ ] **Pagination & Ordering:** Do list endpoints enforce maximum page sizes and deterministic secondary sort orders?
- [ ] **Asynchronous Offloading:** Are slow or third-party communications (emails, webhooks, heavy compute) offloaded to background queues?
- [ ] **Idempotency:** Are background workers and payment/webhook handlers designed to be safely idempotent?
- [ ] **Error Handling:** Are domain exceptions caught gracefully by central middleware without leaking internal stack traces or raw SQL errors to clients?
- [ ] **Structured Logging:** Are logs emitted as structured JSON with correlation IDs (`X-Request-ID`), and are secrets/passwords/tokens redacted?
- [ ] **Automated Testing:** Are unit and integration tests present, verifying both happy path and edge/failure conditions?

