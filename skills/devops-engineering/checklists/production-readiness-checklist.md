# Production Readiness Checklist

Before approving any deployment to staging or production:
- [ ] Have all automated CI checks and tests passed?
- [ ] Is configuration separated from code and supplied via environment variables?
- [ ] Are secrets managed in a secure store (e.g. Vault, AWS SSM, GitHub Secrets) and not committed?
- [ ] Have health check endpoints (`/healthz`, `/readyz`) been implemented and verified?
- [ ] Is structured JSON logging enabled with sensitive fields scrubbed?
- [ ] Is a clear rollback mechanism defined and tested?
- [ ] Has explicit human authorization been confirmed before production rollout?
