# Reference: The Dual-Axis Code Review Model

## Why Two Axes?
Most code reviews fail because reviewers conflate style with correctness, or get distracted by variable naming while missing that the underlying business logic solves the wrong problem.

### Axis 1: Standards Compliance
Focuses on internal software hygiene:
- Consistency with local idioms and patterns.
- Error handling thoroughness.
- Test coverage and determinism.
- Static typing and lint cleanliness.

### Axis 2: Specification Alignment
Focuses on external customer value and requirements:
- Does the code satisfy the acceptance criteria?
- Does it preserve backward compatibility for existing consumers?
- Are performance budgets respected?
