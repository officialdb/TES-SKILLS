# Reference: Smoke Testing and Canary Verification

## Anatomy of a Smoke Test
A smoke test is a shallow, broad suite of checks designed to confirm that essential functionality works before deeper testing or traffic cutover occurs.

### Essential Smoke Checks:
1. **DNS & SSL Certificate:** Domain resolves, TLS certificate is valid and not expired.
2. **Static Asset Delivery:** CSS, JS bundles, and favicon return HTTP 200 with appropriate cache headers.
3. **Database Connectivity:** Querying a simple health check or reading a core table succeeds without timeout.
4. **Auth Flow:** Token generation or test login returns valid session.
