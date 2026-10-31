---
name: software-engineering
description: Implementation excellence, clean modular code, minimal abstractions, robust error handling, dependency hygiene, and maintainability. Trigger when writing production code, refactoring complex methods, handling errors, or optimizing dependencies.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Software Engineering

## Purpose
`software-engineering` guides coding agents in writing clean, reliable, efficient, and maintainable software. It emphasizes readable logic, minimal dependencies, comprehensive error handling, and test-backed modifications.

---

## 1. Core Engineering Principles

1. **Simplicity and Directness:**
   - Prefer simple, clear code over clever or obscure constructs.
   - Do not create abstract factories or multiple layers of inheritance when a simple function or dataclass suffices.

2. **Dependency Hygiene:**
   - Always prefer standard library solutions when available.
   - Every third-party dependency adds attack surface, build latency, and supply-chain maintenance overhead. Justify every addition.

3. **Explicit Error Handling:**
   - Never swallow exceptions silently (no empty `except: pass` or `catch (e) {}`).
   - Distinguish operational errors (transient network failure, invalid input) from programming bugs (null pointer, index out of range).
   - Use typed domain exceptions with informative context.

4. **Input Validation at System Boundaries:**
   - Validate and sanitize external input immediately upon entry (controllers, CLI parsers, API endpoints).
   - Once validated, trust internal domain models.

---

## 2. Refactoring Standards

When improving or modifying existing code:
- **Keep Diffs Minimal:** Do not reformat entire files or rename symbols unless requested.
- **Maintain Invariants:** Ensure that existing public contracts, return types, and side-effects remain stable.
- **Red-Green-Refactor:** Ensure existing tests pass before touching code, verify test failure with new requirement, write code to pass, refactor cleanly.

---

## 3. Deliverables & Outputs
1. **Clean Code Changes:** Well-structured, fully typed, documented implementation.
2. **Unit / Integration Tests:** Testing both the happy path and edge/failure conditions.
3. **Execution Verification:** Confirmation that linters, type checkers, and test runners exit successfully with zero errors.
