---
name: system-architect
description: System architecture design, domain modeling, bounded contexts, explicit interfaces, deep module design, and Architectural Decision Records (ADRs). Trigger when designing new systems, breaking monoliths into modules, establishing boundaries, or documenting critical architectural decisions.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# System Architect

## Purpose
`system-architect` provides agents with principles and workflows to architect robust, evolvable systems. It emphasizes explicit boundaries, deep modules (simple interfaces hiding complex implementations), domain modeling, and documenting decisions in ADRs.

---

## 1. Architectural Principles

1. **Deep Modules Over Shallow Layers:**
   - Design modules with small, clean, intuitive interfaces that encapsulate substantial internal complexity.
   - Avoid "pass-through" layers or shallow wrappers that add indirection without adding value.

2. **Explicit Interfaces & Contracts:**
   - Define data shapes and boundaries using strict schemas (e.g. Pydantic models, TypeScript interfaces, Protobufs).
   - Never pass untyped generic dictionaries or bags of state across domain boundaries.

3. **Separation of Concerns:**
   - Separate business logic (domain) from persistence (database), presentation (API/UI), and transport (HTTP/gRPC/queues).

4. **Right-Sized Abstraction:**
   - Do not design for hypothetical multi-cloud setups when deploying to a single target.
   - Implement for current scale with clear seams for future evolution.

---

## 2. Architecture Workflow

```
[Problem Discovery & Domain Exploration]
                   |
                   v
[Define Bounded Contexts & Entities]
                   |
                   v
[Draft Interfaces & Seam Boundaries]
                   |
                   v
[Draft Architectural Decision Record (ADR)]
                   |
                   v
[Review with Stakeholders]
```

### Step 1: Clarify Domain Concepts
- Define ubiquitous language. Ensure terminology is consistent across documentation, database tables, and code symbols.
- Map relationships: Aggregates, Entities, Value Objects, Domain Events.

### Step 2: Establish Module Boundaries
- Group related business capabilities together.
- Minimize coupling between modules: communication occurs solely via explicit service interfaces or asynchronous events.

### Step 3: Record Architectural Decisions
- Whenever introducing a major architectural pattern, database choice, or framework seam, draft an ADR in `docs/decisions/` or `.engineering/decisions/`.
- Use `templates/adr-template.md`.

---

## 3. Deliverables & Outputs
1. **Domain Model / Architecture Overview:** Diagram or markdown specification of components and data flows.
2. **Interface Definitions:** Typed API or module signatures.
3. **Architectural Decision Record (ADR):** Documenting context, alternatives evaluated, decision, and consequences.
