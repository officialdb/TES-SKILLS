---
name: software-engineering
description: Clean modular implementation, minimal abstractions, robust error handling, and dependency hygiene. Use when writing production code or refactoring.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Software Engineering

## Purpose & Activation
`software-engineering` guides coding agents in writing clean, reliable, efficient, and maintainable software. It focuses on concrete implementation excellence, minimal dependencies, robust error handling, and test-backed code changes.

- **Primary Skill For:** Writing new application features, refactoring existing modules, implementing business logic, and optimizing code.
- **Composition:** Pair with `secure-development` when building security-sensitive endpoints or data processing; pair with `testing-strategy` when structuring extensive test suites.
- **Ownership Boundary:** Universal inspection protocols belong to `engineering-core`; security audits belong to `security-audit`.

---

## 1. Core Implementation Principles

1. **Simplicity and Directness:**
   - Prefer straightforward, readable code over clever or indirect constructs.
   - Avoid abstract factory patterns or deep inheritance hierarchies when a simple function, dataclass, or record suffices.
2. **Dependency Hygiene:**
   - Prefer standard library solutions whenever available.
   - Every external dependency increases build latency, maintenance burden, and supply chain attack surface. Justify every addition.
3. **Explicit Error Handling:**
   - Never swallow exceptions silently (no empty `except: pass` or `catch (e) {}`).
   - Distinguish expected operational errors (network timeout, invalid input) from unhandled programmer bugs (null pointer, index out of bounds).
   - Use typed domain exceptions with clear, informative failure context.
4. **Input Validation at Boundaries:**
   - Validate and sanitize external input immediately upon entering the application (controllers, CLI parsers, HTTP handlers).
   - Once validated, maintain internal domain invariants without redundant nested validations.

---

## 2. Refactoring Standards
When altering existing production code:
- **Keep Diffs Minimal:** Modify only the necessary code paths. Do not reformat intact files or rename unrelated symbols.
- **Preserve Public Invariants:** Ensure existing public API contracts, return types, and side-effects remain stable.
- **Red-Green-Refactor:** Verify existing tests pass first, write a failing test for new behavior, implement the fix, and clean up.

---

## 3. Expected Deliverables
1. **Clean Code Changes:** Well-structured, fully typed, maintainable implementation matching repo idioms.
2. **Unit / Integration Tests:** Automated tests covering both happy paths and boundary/error cases.
3. **Execution Verification:** Terminal evidence that tests, type checkers, and linters pass cleanly.

---

## 4. Progressive Disclosure (Reference Documents)
Consult these bundled documents only when specific deep guidance is needed:

- **Deep clean code paradigms:** Consult [clean-code-principles.md](references/clean-code-principles.md).
- **Domain error modeling & retry patterns:** Consult [error-handling-patterns.md](references/error-handling-patterns.md).
- **Pre-commit code quality review:** Consult [code-quality-checklist.md](checklists/code-quality-checklist.md).
