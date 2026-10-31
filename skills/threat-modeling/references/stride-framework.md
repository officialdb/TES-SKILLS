# Reference: Applying STRIDE to Modern Architectures

## Trust Boundaries
A trust boundary is an interface where privilege levels change. Examples:
- Web browser to API gateway.
- API gateway to internal microservice.
- Application code to third-party SaaS webhook.
- User-supplied file upload to background parsing worker.

## Common Modern Threat Vectors
1. **Webhook Tampering:** Third-party payloads intercepted or forged -> Mitigate via cryptographic HMAC signature verification (`X-Signature-256`).
2. **Server-Side Request Forgery (SSRF):** User specifies custom callback URL -> Mitigate by resolving DNS and rejecting private IP ranges.
3. **Replay Attacks:** Stolen API request retransmitted -> Mitigate via timestamps and nonce validation.
