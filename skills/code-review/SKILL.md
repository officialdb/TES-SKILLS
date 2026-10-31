---
name: code-review
description: Dual-axis code review evaluating repository standards compliance and specification alignment with actionable feedback. Use when reviewing pull requests or diffs.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Code Review

## Purpose & Activation
`code-review` conducts dual-axis evaluations of pull requests, commits, and diffs. It separates code review into two distinct, rigorous investigations: standards compliance and specification alignment.

- **Primary Skill For:** Reviewing incoming pull requests, inspecting code diffs, evaluating patch safety, and verifying criteria completion.
- **Composition:** Pair with `security-audit` when reviewing security-critical changes or user-data processing.
- **Ownership Boundary:** Authoring original implementation code belongs to `software-engineering`.

---

## 1. The Dual-Axis Review Methodology

```
                          [Incoming Code Diff]
                                   |
                  +----------------+----------------+
                  |                                 |
                  v                                 v
      [Axis 1: Standards Compliance]     [Axis 2: Specification Alignment]
      • Idioms and patterns              • Acceptance criteria fulfilled
      • Static types & linting           • Edge cases addressed
      • Error handling & tests           • Backward compatibility preserved
                  |                                 |
                  +----------------+----------------+
                                   |
                                   v
             [Actionable Review Report & Clear Verdict]
```

1. **Axis 1: Standards Compliance (Internal Hygiene):**
   - Does the diff adhere to the repository's established conventions, naming idioms, and formatting?
   - Are static types complete and verified by the compiler or type checker?
   - Are errors handled explicitly without swallowing exceptions?
   - Are new code paths accompanied by automated tests?
2. **Axis 2: Specification Alignment (External Correctness):**
   - Does the change directly satisfy the user requirement or originating issue?
   - Does it preserve existing public contracts and avoid breaking backward compatibility?
   - Does it introduce unintended performance regressions or memory leaks?

---

## 2. Review Protocol & Tone
- **Constructive & Specific:** Point directly to file paths and line numbers. Explain *why* a pattern is problematic and suggest a concrete, typed alternative.
- **Clear Severity Labels:** Clearly separate **Blocking Issues** (correctness bugs, regressions, missing tests) from **Non-Blocking Suggestions** (idiomatic improvements, minor nits).
- **Verify Test Evidence:** Confirm that tests pass and actually assert on the modified behaviors.

---

## 3. Expected Deliverables
1. **Dual-Axis Review Report:** Structured feedback evaluating both standards compliance and specification alignment.
2. **Actionable Suggestions:** Specific inline code replacements for identified issues.
3. **Explicit Verdict:** Clear decision (Approve, Request Changes, or Comment).

---

## 4. Progressive Disclosure (Reference Documents)
Consult these bundled documents only when specific deep guidance is needed:

- **Dual-axis review model and principles:** Consult [dual-axis-review.md](references/dual-axis-review.md).
- **PR review inspection checklist:** Consult [pr-review-checklist.md](checklists/pr-review-checklist.md).
- **Structured review summary template:** Consult [code-review-template.md](templates/code-review-template.md).
