# Reference: Deterministic Mocking and Test Isolation

## When to Mock vs When to Use Real Dependencies
- **Mock / Stub:**
  - Third-party HTTP APIs (Stripe, Twilio, external cloud services).
  - Non-deterministic sources (current system clock, random UUID generators).
  - Rare error simulations (disk full, network timeout).
- **Use Real Implementations:**
  - In-memory data structures.
  - Algorithms, parsers, and validators.
  - SQLite or temporary directories for file I/O tests.

## The Danger of Over-Mocking
Mocking internal implementation details couples tests to refactorings. Mock only at the architectural boundary, not every internal private method.
