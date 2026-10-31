# Reference: HTTP Request Lifecycle & API Engineering

## 1. The HTTP Request Lifecycle

Every API endpoint must process requests through a predictable lifecycle:

```text
Request Ingress ──> Transport Security (TLS)
                ──> Rate Limiting & DoS Protection
                ──> Correlation ID Middleware (X-Request-ID)
                ──> Authentication Middleware (Identity Verification)
                ──> Body Deserialization & Schema Validation
                ──> Route Controller & Parameter Binding
                ──> Application Service Execution
                ──> Response Serialization & Security Headers
                ──> Request Outgress & Access Logging
```

## 2. Request Validation & Boundary Defenses

- **Strict Schema Validation:** Validate request headers, query parameters, route variables, and JSON bodies against declarative schemas (Pydantic, Zod, FormRequest, Bean Validation) before reaching business logic.
- **Fail Fast with Detailed Errors:** Return `422 Unprocessable Entity` or `400 Bad Request` with field-level validation messages.
- **Mass Assignment Protection:** Never pass raw request payloads directly into ORM models. Map validated input to explicit Data Transfer Objects (DTOs) or whitelist mass-assignment attributes.
- **Request Size & Streaming Limits:** Enforce maximum body size limits (e.g. 10MB) to protect against memory exhaustion. For large file uploads, stream directly to object storage rather than buffering in memory.

## 3. Response Structure & HTTP Status Code Semantics

### Standard Status Codes
- `200 OK`: Successful retrieval or mutation with response body.
- `201 Created`: Resource successfully created (include `Location` header where appropriate).
- `204 No Content`: Successful action with empty response body (common in deletions).
- `400 Bad Request`: Malformed syntax or invalid request parameters.
- `401 Unauthorized`: Authentication missing, expired, or invalid.
- `403 Forbidden`: Authenticated user lacks authorization for the requested resource.
- `404 Not Found`: Target resource does not exist (or hidden to prevent enumeration).
- `409 Conflict`: State conflict (e.g., duplicate unique constraint, optimistic lock collision).
- `422 Unprocessable Entity`: Syntactically valid request failing semantic domain validation.
- `429 Too Many Requests`: Client exceeded rate limits (provide `Retry-After` header).
- `500 Internal Server Error`: Unhandled server exception (redact stack trace in production).

### Uniform Error Response Envelope (RFC 7807 Pattern)
```json
{
  "type": "https://api.example.com/errors/validation-failed",
  "title": "Validation Failed",
  "status": 422,
  "detail": "One or more fields failed validation checks.",
  "instance": "/api/v1/orders",
  "correlation_id": "req_8f1a92e10",
  "errors": [
    {
      "field": "quantity",
      "message": "Quantity must be an integer greater than 0"
    }
  ]
}
```

## 4. Pagination, Filtering & Sorting

- **Offset-Based Pagination (`limit`/`offset` or `page`/`per_page`):** Simple for small datasets and user interfaces with direct page jumping. Degrades on large datasets (`OFFSET 1000000`).
- **Cursor-Based Pagination (`cursor`/`limit`):** Recommended for large datasets and infinite-scrolling feeds. Provides deterministic pagination even when items are added concurrently.
- **Deterministic Ordering:** Always specify a deterministic secondary sort key (such as `id ASC`) when sorting by non-unique fields (such as `created_at`).
- **Whitelisted Filter Fields:** Strictly whitelist allowable query parameters for filtering and sorting to prevent arbitrary SQL generation.

