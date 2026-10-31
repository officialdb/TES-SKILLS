# Security Audit Checklist

- [ ] Have all dynamic queries been checked for parameterized binding?
- [ ] Are HTML outputs properly contextual-encoded against XSS?
- [ ] Are authentication endpoints protected against credential stuffing and brute force?
- [ ] Are all authorization decisions enforced on the server side (never client side)?
- [ ] Are file uploads restricted by MIME type, extension, size, and isolated from executable roots?
- [ ] Are secrets, API keys, and certificates absent from version control?
- [ ] Do outgoing HTTP requests validate destinations against private IP spaces (SSRF protection)?
- [ ] Are third-party dependencies scanned for known CVEs using automated tooling?
