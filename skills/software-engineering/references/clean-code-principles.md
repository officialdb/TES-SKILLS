# Reference: Clean Code Principles for Agents

## Readability Over Cleverness
Code is read far more often than it is written.
- Name variables, functions, and classes after their domain intent (e.g., `calculate_order_subtotal` instead of `calc_sub`).
- Avoid deep nesting; use guard clauses and early returns.
- Keep function signatures short and purposeful (ideally <= 3 parameters). Group related parameters into a typed configuration or request object.

## Dependency Assessment Rules
Before adding any new dependency:
1. Does the language standard library already provide this capability (e.g., Python `urllib`, `dataclasses`, `pathlib`, `json`)?
2. Is the dependency actively maintained, well-tested, and secure?
3. Does it introduce transitive dependencies with large footprints?
