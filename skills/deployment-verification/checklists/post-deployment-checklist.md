# Post-Deployment Checklist

- [ ] Does `/healthz` and `/readyz` return HTTP 200?
- [ ] Are SSL/TLS certificates active and valid?
- [ ] Do static assets load without 404 errors?
- [ ] Does test-user authentication succeed?
- [ ] Does a read query on the core database complete within latency thresholds?
- [ ] Are error rates across application logs below the alarm threshold (<0.1%)?
- [ ] Is the rollback target confirmed available in case of regression?
