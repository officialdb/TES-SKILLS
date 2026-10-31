# Reference: Backend Architecture & Structural Organization

## Architectural Foundations

A robust backend architecture separates concerns so business logic remains independent of transport mechanisms, persistence technologies, and external integrations.

### 1. Structural Layering

Maintain clear directional dependencies (outer layers depend on inner layers, not vice versa):

```text
HTTP / CLI / Events (Transport Layer)
         │
         ▼
Controllers / Routers (Request Parsing & Status Code Mapping)
         │
         ▼
Application Services (Use Cases & Transaction Coordination)
         │
         ▼
Domain Models & Invariants (Core Business Rules)
         │
         ▼
Repositories & Adapters (Database, Caching, External APIs)
```

- **Transport / Presentation Layer:** Deserializes requests, validates wire schemas, calls application services, and maps results to HTTP response envelopes or CLI codes.
- **Application Service Layer:** Orchestrates multi-step use cases, manages database transaction boundaries, enforces high-level authorization, and dispatches domain events or background jobs.
- **Domain Layer:** Enforces business invariants, calculations, and state machine transitions. Keeps business rules isolated from SQL queries and HTTP concepts.
- **Infrastructure / Persistence Layer:** Implements database access, external HTTP clients, cache stores, and message queue producers.

### 2. Pragmatic Architecture Selection

Avoid dogmatic patterns. Select an organization matching project size and maturity:

- **Modular Monolith (Default for most applications):** Cohesive modules grouped by business capability (e.g. `billing`, `identity`, `inventory`) sharing a single deployment unit and relational database. Highly recommended before considering distributed systems.
- **Layered Architecture:** Classic 3-tier structure (`controllers/`, `services/`, `models/`), ideal for small to medium APIs.
- **Domain-Driven Design (DDD):** Appropriate when domain complexity is high. Organize around aggregates, entities, value objects, and domain events.
- **Microservices:** Warranted only when independent scaling, distinct team ownership boundaries, or isolated technology lifecycles strictly demand distributed deployment.

### 3. Framework-Specific Structural Idioms

- **Python (FastAPI / Django / Flask):**
  - *FastAPI:* Use APIRouter for route grouping, dependency injection (`Depends()`) for service and session provision, Pydantic schemas for DTOs.
  - *Django:* Keep views skinny; place business workflows in service modules (`services.py`) or selector functions rather than fat models or oversized views.
- **PHP (Laravel / Symfony):**
  - *Laravel:* Use dedicated Form Requests for validation, Single-Action Controllers or invokable controllers, Action classes for reusable business logic, and Service Providers for dependency binding.
  - *Symfony:* Utilize autowired services, message buses (Symfony Messenger), and Doctrine repositories.
- **JavaScript / TypeScript (NestJS / Express / Fastify):**
  - *NestJS:* Enforce module boundaries (`@Module`), inject services via constructor `@Injectable()`, validate via `class-validator` DTOs.
  - *Express / Fastify:* Organize by feature folder (`routes.ts`, `service.ts`, `repository.ts`, `schema.ts`) to avoid horizontal sprawling folders.
- **Java (Spring Boot):**
  - Use `@RestController`, `@Service`, and `@Repository` annotations. Declare transaction boundaries at service methods with `@Transactional`.

### 4. Configuration & Environment Management

- **Twelve-Factor Principles:** Inject all runtime configuration (database URLs, API keys, cache hosts) via environment variables. Never hardcode credentials.
- **Typed Configuration Objects:** Parse and validate environment variables at application startup into strongly-typed configuration classes. Fail fast if required variables are missing.
- **Environment Isolation:** Maintain explicit separation between local development, testing, staging, and production environments.

