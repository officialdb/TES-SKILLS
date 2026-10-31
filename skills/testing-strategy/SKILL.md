---
name: testing-strategy
description: Comprehensive testing methodology, test pyramid, deterministic unit tests, and integration testing. Use when designing test suites or debugging flaky tests.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Testing Strategy

## Purpose & Activation
`testing-strategy` teaches agents how to structure, implement, and maintain automated test suites that provide high confidence, execute rapidly, and remain completely deterministic.

- **Primary Skill For:** Designing test suites, establishing test patterns, improving test coverage, and debugging flaky or slow tests.
- **Composition:** Pair with `software-engineering` during feature implementation or refactoring; pair with `deployment-verification` for post-deploy smoke checks.
- **Ownership Boundary:** Universal pre-modification checks belong to `engineering-core`.

---

## 1. The Practical Test Pyramid

```
        /   E2E / Smoke Tests (5–10%)   \        <- Critical user paths, high confidence
       /---------------------------------\
      /     Integration Tests (15–20%)    \      <- Real boundaries: DB, local HTTP, file I/O
     /-------------------------------------\
    /          Unit Tests (70–80%)          \    <- Fast, pure logic, boundary conditions
```

1. **Unit Tests:** Fast, isolated, and in-memory. Test algorithmic branches, validation rules, state transitions, and edge cases.
2. **Integration Tests:** Verify communication across real boundaries (database repositories, message brokers, HTTP routers) using ephemeral or containerized resources.
3. **End-to-End Tests:** Reserved strictly for core user journeys. Kept minimal to avoid execution bloat and brittleness.

---

## 2. Determinism & Mocking Discipline

1. **Zero Flakiness:**
   - Never use wall-clock `sleep()` statements to wait for async operations. Use polling with timeouts or event hooks.
   - Inject clock providers or freeze time rather than checking `datetime.now()`.
2. **Hermetic Test Isolation:**
   - Every test must be completely independent. Never share mutable global state across test cases.
   - Use isolated temporary directories (`tmp_path`) for file operations and clean up after execution.
3. **Judicious Mocking:**
   - Mock at the architectural perimeter (external billing APIs, third-party webhooks, email providers).
   - Avoid mocking internal domain entities or data transfer objects; test domain logic with real instances.

---

## 3. Expected Deliverables
1. **Automated Test Suites:** Deterministic unit and integration tests covering positive and negative paths.
2. **Test Plan Specification:** Clear strategy detailing coverage goals, test levels, and fixtures.
3. **Execution Evidence:** Terminal verification showing passing test suites with zero warnings or hangs.

---

## 4. Progressive Disclosure (Reference Documents)
Consult these bundled documents only when specific deep guidance is needed:

- **Test pyramid and mocking strategies:** Consult [test-pyramid-and-mocking.md](references/test-pyramid-and-mocking.md).
- **Test suite hygiene checklist:** Consult [testing-checklist.md](checklists/testing-checklist.md).
- **Comprehensive test plan template:** Consult [test-plan-template.md](templates/test-plan-template.md).
