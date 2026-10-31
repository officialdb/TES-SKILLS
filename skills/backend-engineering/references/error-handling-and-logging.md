# Reference: Structured Logging, Exception Handling & Observability

## 1. Structured Logging Standards

Plain text logs (`print()` or unformatted string concatenations) cannot be searched, aggregated, or queried effectively in production log management systems.

### Structured JSON Logging Format
Emit logs as structured JSON objects containing standardized metadata:

```json
{
  "timestamp": "2026-10-31T12:00:00.124Z",
  "level": "INFO",
  "message": "User checkout completed successfully",
  "correlation_id": "req_9f821ac3",
  "user_id": "usr_48102",
  "organization_id": "org_991",
  "duration_ms": 142.5,
  "service": "checkout-service",
  "environment": "production"
}
```

### Correlation & Request Tracing
- Assign a unique Correlation ID (`X-Request-ID` / Trace ID) to every incoming HTTP request or message queue job via ingress middleware.
- Propagate the correlation ID across all log statements, database queries, and outbound HTTP requests. This allows tracing a single user transaction across all backend components.

### Log Severity Guidelines
- `DEBUG`: Detailed diagnostic information useful for local development and troubleshooting.
- `INFO`: Significant lifecycle events (application startup, successful user registration, payment processing).
- `WARN`: Handled, recoverable anomalies (retry attempts, fallback cache usage, rate-limit thresholds reached).
- `ERROR`: Unhandled operational failures affecting a specific request (database connection timeout, unhandled domain exception).
- `CRITICAL`: System-wide fatal failures requiring immediate on-call engineering intervention.

## 2. Sensitive Data Redaction

Never emit sensitive information to application logs:
- **Redaction Whitelist/Blacklist:** Automatically mask or strip:
  - Passwords and password hashes
  - Authentication tokens, bearer tokens, API secrets, private keys
  - Credit card numbers (PCI-DSS compliance)
  - Personally Identifiable Information (PII) such as social security numbers, passport numbers, and unencrypted identity documents.

## 3. Centralized Exception Handling

Implement a global exception interceptor / middleware to capture unhandled exceptions:
- **Sanitized Client Responses:** In production environments, never expose raw internal stack traces, SQL syntax errors, database hostnames, or library versions to client applications.
- **Client Error Format:** Return a clean error payload with the correlation ID so users can quote it to support.
- **Sentry / APM Integration:** Report full stack traces, environment details, and execution context to private application performance monitoring systems.

