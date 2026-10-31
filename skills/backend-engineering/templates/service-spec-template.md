# Service Specification Template

Use this template when designing or refactoring a backend domain service or module:

```markdown
# Service: [ServiceName]

## 1. Overview & Responsibility
- **Domain Context:** [e.g. Identity, Billing, Orders]
- **Core Purpose:** [Single sentence summarizing what this service accomplishes]
- **Collaborating Services:** [e.g. UserRepository, PaymentGateway, AuditLogger]

## 2. Ingress & Contract
- **Trigger:** [HTTP endpoint, Background Queue Worker, CLI Command, or Domain Event]
- **Input Parameters (DTO):**
  - `param_one` (type, required/optional): [description]
  - `param_two` (type, required/optional): [description]
- **Output (DTO / Domain Entity):**
  - [Return structure specification]

## 3. Transaction & Invariant Boundaries
- **Preconditions:** [e.g. User account must be active, inventory balance >= requested quantity]
- **Atomic Transaction:** [Yes/No - detail database operations wrapped in the transaction block]
- **External Network Calls:** [Detail calls executed outside the database transaction block]
- **Side-Effects Dispatched:** [e.g. Domain events emitted, background worker jobs enqueued]

## 4. Error Handling & Failure Modes
| Failure Scenario | Domain Exception | HTTP Status Code | Handling / Fallback |
|---|---|---|---|
| Entity not found | `ResourceNotFoundError` | 404 | Return standard error envelope |
| Duplicate key conflict | `DuplicateEntityError` | 409 | Rollback transaction, notify caller |
| Downstream API timeout | `GatewayTimeoutError` | 504 | Retry with exponential backoff |

## 5. Security & Authorization
- **Authentication Required:** [Yes/No]
- **Authorization Check:** [e.g. User must possess permission `orders.create` AND belong to target `org_id`]
- **IDOR Protection:** [Detail how tenant/user ownership of target entity is enforced]
- **Sensitive Data Handling:** [Detail fields requiring encryption or log redaction]
```

