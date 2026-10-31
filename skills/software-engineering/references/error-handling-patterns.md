# Reference: Error Handling and Resilience Patterns

## The Three Rules of Error Handling

1. **Catch Specific Exceptions:**
   - Never catch base `Exception` or `Throwable` unless re-raising or logging at the top-level application boundary.
   - Always catch specific errors (e.g., `FileNotFoundError`, `ValueError`, `KeyError`).

2. **Preserve Context & Stack Traces:**
   - When wrapping an exception, chain the original cause (e.g. `raise CustomDomainError("...") from err`).

3. **Graceful Degradation & Cleanup:**
   - Always release resources using context managers (`with` statements, `try...finally`).
   - Leave the system in a consistent state if an operation fails halfway through.
