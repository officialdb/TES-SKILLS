---
name: code-review
description: Dual-axis code review evaluating repository standards compliance and specification alignment with constructive, actionable feedback. Trigger when reviewing pull requests, auditing code diffs, or validating changes before merge.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Code Review

## Purpose
`code-review` conducts dual-axis evaluations of pull requests, commits, and diffs. It separates code review into two distinct, rigorous investigations:
1. **Standards Compliance:** Does the diff follow the repository's established conventions, types, architecture, tests, and formatting?
2. **Specification Alignment:** Does the diff accurately and completely satisfy the originating issue, acceptance criteria, and user story?

---

## 1. The Dual-Axis Review Methodology

```
                       [Incoming Code Diff]
                                |
             +------------------+------------------+
             |                                     |
             v                                     v
   [Axis 1: Standards]                    [Axis 2: Specification]
   - Coding conventions                  - Solves originating issue
   - Type safety & tests                 - Acceptance criteria met
   - Security & error handling           - Edge cases accounted for
   - Architectural boundaries            - No accidental regressions
             |                                     |
             +------------------+------------------+
                                |
                                v
               [Consolidated Review Deliverable]
```

---

## 2. Review Workflow

### Phase 1: Baseline Context
- Read the originating issue, ticket, or task prompt to establish the **Ground Truth Specification**.
- Inspect project conventions (`CONTRIBUTING.md`, linter configs, existing codebase patterns).

### Phase 2: Axis 1 Evaluation (Standards & Health)
- **Architecture:** Does the change respect module boundaries? Are abstractions deep rather than shallow?
- **Code Quality:** Are edge cases handled? Are exceptions caught specifically?
- **Testing:** Are new tests provided? Do all tests pass?
- **Security:** Does the code introduce injection sinks, hardcoded secrets, or insecure auth?

### Phase 3: Axis 2 Evaluation (Specification Fulfillment)
- Did the author fulfill every requirement stated in the spec?
- Did the author introduce unintended side effects, scope creep, or omit requested functionality?

---

## 3. Constructive Feedback Standards
- Formulate comments constructively: explain *why* an issue matters, not merely *what* is wrong.
- Provide concrete replacement snippets whenever requesting changes.
- Categorize comments using clear severity prefixes:
  - `[BLOCKING]`: Must be fixed before merge (correctness, security, data loss).
  - `[RECOMMENDATION]`: Strongly advised improvement (readability, minor perf).
  - `[NIT]`: Minor style, spelling, or non-blocking polish.
