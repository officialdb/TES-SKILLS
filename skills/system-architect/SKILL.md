---
name: system-architect
description: High-level system architecture, domain modeling, bounded contexts, explicit interfaces, and ADR records. Use when designing systems or establishing module boundaries.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# System Architect

## Purpose & Activation
`system-architect` provides agents with principles and workflows to architect robust, evolvable systems. It emphasizes explicit boundaries, deep modules (simple interfaces hiding complex implementations), domain modeling, and documenting decisions in ADRs.

- **Primary Skill For:** Designing new systems, decomposing monoliths into modules, establishing domain boundaries, and authoring Architectural Decision Records.
- **Composition:** Pair with `threat-modeling` when evaluating security boundaries; pair with `software-engineering` when moving from architectural design into code.
- **Ownership Boundary:** Low-level implementation details and error modeling belong to `software-engineering`.

---

## 1. Architectural Principles

1. **Deep Modules Over Shallow Layers:**
   - Design modules with small, clean, intuitive interfaces that encapsulate substantial internal complexity.
   - Avoid shallow "pass-through" layers or wrappers that introduce indirection without providing abstraction.
2. **Domain Boundaries & Bounded Contexts:**
   - Clearly delineate domain boundaries. Keep domain entities decoupled from persistence technologies and transport protocols (HTTP/gRPC/CLI).
   - Use explicit data transfer objects (DTOs) or domain events at subsystem boundaries.
3. **Decoupled Seams & Dependency Inversion:**
   - High-level business policies must not depend on low-level implementation details. Both must depend on abstractions (interfaces/protocols).
   - Design seams that permit swapping out storage or network layers without modifying business logic.
4. **Architectural Decision Records (ADRs):**
   - Document any significant, hard-to-reverse technical decision in a version-controlled ADR (`.engineering/decisions/` or `docs/adr/`).

---

## 2. Standard Architecture Workflow

```
[Problem & Requirements Analysis] -> [Domain Modeling & Seams] -> [Interface Definition] -> [Evaluate Alternatives] -> [ADR Authoring]
```

---

## 3. Expected Deliverables
1. **Module Architecture Specification:** Clear diagram or description of modules, responsibilities, and data flows.
2. **Interface Definitions:** Typed interfaces, protocols, or schemas defining subsystem contracts.
3. **Architectural Decision Record (ADR):** Structured document capturing context, evaluated alternatives, decision, and consequences.

---

## 4. Progressive Disclosure (Reference Documents)
Consult these bundled documents only when specific deep guidance is needed:

- **ADR authoring conventions and lifecycle:** Consult [adr-standards.md](references/adr-standards.md).
- **Domain modeling and bounded context patterns:** Consult [domain-modeling-and-boundaries.md](references/domain-modeling-and-boundaries.md).
- **Architecture design review checklist:** Consult [architecture-review-checklist.md](checklists/architecture-review-checklist.md).
- **ADR document template:** Consult [adr-template.md](templates/adr-template.md).
