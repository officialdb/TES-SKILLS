# Backend Production Readiness Checklist

Verify these operational requirements before deploying backend applications:

- [ ] **Liveness Probe (`/health/live`):** Is a lightweight endpoint available verifying process responsiveness without downstream database coupling?
- [ ] **Readiness Probe (`/health/ready`):** Does a readiness check verify database and cache connectivity before accepting load balancer traffic?
- [ ] **Graceful Shutdown:** Does the server trap `SIGTERM` / `SIGINT`, drain in-flight requests, complete active worker jobs, and cleanly close connection pools?
- [ ] **Database Migrations:** Are migrations deterministic, version-controlled, backward-compatible, and executed in a pre-flight deployment phase?
- [ ] **Connection Pool Limits:** Are database and cache connection pools sized according to available database connections and server CPU cores?
- [ ] **Worker Queue Supervision:** Are background workers supervised (systemd, Supervisor, Kubernetes) with automatic restarts on crashes?
- [ ] **Dead-Letter Queue (DLQ):** Are unrecoverable failed jobs routed to a dead-letter queue with operational alerting?
- [ ] **Memory & Resource Caps:** Are container resource limits configured to prevent runaway memory leaks from affecting host nodes?
- [ ] **Startup Environment Validation:** Does the application validate all required environment variables at startup and fail fast if keys are missing?

