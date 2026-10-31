---
name: testing-strategy
description: Comprehensive testing methodology, test pyramid, deterministic unit tests, integration testing, boundary analysis, and regression prevention. Trigger when designing test suites, writing unit or integration tests, debugging test flakiness, or establishing QA standards.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Testing Strategy

## Purpose
`testing-strategy` teaches agents how to structure, implement, and maintain automated test suites that provide high confidence, run quickly, and avoid flakiness.

---

## 1. The Practical Test Pyramid

```
        /  E2E / Smoke Tests  \        <- Minimal, high confidence, tests critical user paths
       /------------------------\
      /    Integration Tests     \     <- Moderate volume, validates real boundaries (DB, HTTP)
     /----------------------------\
    /       Unit Test Base         \   <- Vast majority, fast (<1ms), isolated, deterministic
   /--------------------------------\
```

### Unit Tests
- Fast, deterministic, in-memory.
- Exercise core business logic, validation, algorithm edge cases.
- Avoid external I/O (disk, network, system clocks) — mock or stub dependencies at the boundary.

### Integration Tests
- Verify that components work together across real boundaries (database queries, serialization, filesystem).
- Use temporary directories (`tmp_path`) or ephemeral test containers.
- Never touch production resources.

### End-to-End & Smoke Tests
- Test critical user flows from entry point to output.
- Validate happy paths and critical security barriers.

---

## 2. Test Design Principles

1. **Arrange-Act-Assert (AAA):**
   - Keep test structure clear: setup data (Arrange), execute function (Act), verify expectations (Assert).

2. **One Primary Concept per Test:**
   - Test a single behavior or edge condition per test function. Avoid monster tests with 50 assertions.

3. **Boundary Value Testing:**
   - Always test boundaries: zero, negative numbers, empty arrays, maximum lengths, unicode characters, null/None.

4. **Flakiness Zero-Tolerance:**
   - Flaky tests destroy developer confidence. Eliminate non-deterministic factors: sleep statements, random generators without seeds, and shared global state.

---

## 3. Deliverables & Outputs
1. **Automated Test Files:** Co-located or placed in `tests/` following project conventions.
2. **Deterministic Mocking:** Fakes and stubs implementing interfaces accurately.
3. **Execution Report:** Terminal evidence demonstrating 100% pass rate.
