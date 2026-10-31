# TES Practical Prompt Library

This prompt library provides tested, copy-and-paste prompts designed to get the highest engineering quality from AI coding agents equipped with TES skills.

Each prompt leverages specific installed TES skills and enforces core engineering principles: inspecting before modifying, preserving existing architectural patterns, demanding automated testing, and providing evidence-backed results.

---

## 📋 Universal Reusable Prompt Template

Use this template to structure any custom task:

```text
Project:
[Briefly describe the project and stack]

Task:
[What do you want to achieve?]

Requirements:
[Important functional and technical requirements]

Constraints:
[Existing stack, compatibility, security, budget, or other limitations]

Expected outcome:
[What should be delivered?]

Use the relevant installed TES skills.
Inspect the existing implementation before making changes.
Preserve existing architecture where appropriate.
Test the implementation and report the actual results.
```

---

## 1. Understand an Existing Project

Use this prompt when onboarding to a new codebase or preparing to make initial architectural decisions.

**Recommended Skills:** `project-onboarding`, `engineering-core`, `system-architect`

```text
I want to understand this project before making changes.

Use the relevant installed TES engineering skills.

Inspect the repository structure, technology stack, architecture,
main modules, dependencies, database, API boundaries, and existing tests.

Explain how the project works, identify important dependencies,
and highlight architectural or technical concerns.

Do not modify any files yet.

Give me a concise engineering overview and suggest the most
important areas to understand before development.
```

---

## 2. Build a New Feature

Use this prompt to plan and implement a feature end-to-end with high architectural integrity.

**Recommended Skills:** `software-engineering`, `system-architect`, `testing-strategy`

```text
I want to implement a new feature in this project.

First inspect the existing architecture and identify the modules
that should be involved.

Use the relevant TES engineering, backend, frontend, database,
and testing skills where applicable.

Explain the implementation approach before making changes.

Preserve existing conventions and avoid unnecessary dependencies.

Implement the feature, write appropriate tests, and report
the files changed and verification results.
```

---

## 3. Backend Engineering

Use this prompt to design, review, or enhance backend services, APIs, and data pipelines.

**Recommended Skills:** `backend-engineering`, `secure-development`, `software-engineering`

```text
Act as a senior backend engineer working on this project.

Use the installed TES backend-engineering skill and other relevant
engineering and security skills.

Inspect the current backend architecture, business logic,
request handling, authentication, authorization, persistence,
error handling, and background processing.

Identify weaknesses and recommend practical improvements.

Do not rewrite working components unnecessarily.
Prioritize maintainability, security, reliability, and testability.
```

---

## 4. Frontend and UI Improvement

Use this prompt to polish frontend interfaces, establish responsive layouts, and verify mobile navigation.

**Recommended Skills:** `ui-ux-standards`, `frontend-quality`

```text
Review and improve the frontend of this project.

Use the installed TES ui-ux-standards and frontend-quality skills.

Evaluate visual hierarchy, typography, spacing, responsiveness,
navigation, accessibility, component consistency, and performance.

Pay particular attention to mobile navigation and hamburger menus.

Preserve the existing brand identity and design direction.

Avoid unnecessary animations, decorative flashing elements,
excessive gradients, and excessive card-based layouts.

Implement improvements where appropriate and verify the results
at desktop and mobile viewport sizes.
```

---

## 5. Database Review

Use this prompt to audit schemas, query performance, locking mechanisms, and migration safety.

**Recommended Skills:** `backend-engineering`, `system-architect`, `security-audit`

```text
Review the database architecture of this project.

Use relevant installed TES engineering and security skills.

Inspect the schema, relationships, indexes, constraints,
migrations, transactions, data access patterns, and tenant isolation
where applicable.

Identify integrity, security, performance, and maintainability risks.

Do not modify the database or run destructive migrations.

Provide prioritized recommendations and explain their impact.
```

---

## 6. Security Audit

Use this prompt to perform a systematic, evidence-based security assessment.

**Recommended Skills:** `security-audit`, `secure-development`, `threat-modeling`

```text
Perform a security review of this project.

Use the installed TES security-audit, secure-development,
and threat-modeling skills.

Inspect the attack surface, authentication, authorization,
input validation, session handling, secrets, dependencies,
file handling, API endpoints, and data exposure risks.

Use evidence from the actual codebase.

Classify findings by severity and provide practical remediation steps.

Do not expose secrets or perform destructive testing.
Do not claim vulnerabilities without supporting evidence.
```

---

## 7. Code Review

Use this prompt to perform dual-axis PR reviews (standards compliance + specification verification).

**Recommended Skills:** `code-review`, `software-engineering`

```text
Review my recent code changes as a senior software engineer.

Use the installed TES code-review and software-engineering skills.

Look for correctness issues, regressions, security problems,
poor abstractions, maintainability problems, and missing tests.

Prioritize actionable findings.

For every finding, explain the affected file or location,
why it matters, its severity, and a suggested correction.

Do not make changes until I approve the proposed fixes.
```

---

## 8. Testing and Quality Assurance

Use this prompt to audit test coverage, eliminate flaky tests, and implement missing edge case assertions.

**Recommended Skills:** `testing-strategy`, `software-engineering`

```text
Evaluate the testing strategy of this project.

Use the installed TES testing-strategy and relevant engineering skills.

Inspect existing unit, integration, and end-to-end tests.

Identify untested critical paths, missing edge cases,
weak assertions, unreliable mocks, and test configuration problems.

Recommend a practical testing plan.

Implement appropriate tests without changing unrelated functionality.
Run the tests and report actual results.
```

---

## 9. Production Readiness

Use this prompt before cutover, major releases, or infrastructure deployments.

**Recommended Skills:** `deployment-verification`, `devops-engineering`, `backend-engineering`, `security-audit`

```text
Prepare this project for production readiness.

Use the relevant installed TES backend, security, DevOps,
testing, and deployment-verification skills.

Evaluate configuration, environment variables, secrets management,
logging, error handling, database migrations, backups,
deployment procedures, rollback strategy, monitoring,
and security controls.

Identify what is ready, what is incomplete, and what is risky.

Produce a prioritized production-readiness checklist.

Do not deploy or modify production infrastructure without my approval.
```

---

## 10. Improve Existing Code Safely

Use this prompt for targeted refactoring without introducing regressions.

**Recommended Skills:** `software-engineering`, `code-review`, `testing-strategy`

```text
I want to improve the quality of this codebase without breaking
existing functionality.

Use the relevant TES software-engineering and code-review skills.

Inspect the existing implementation first.

Identify duplicated logic, unnecessary complexity, fragile
dependencies, unclear responsibilities, and maintainability issues.

Recommend a phased refactoring plan.

Preserve existing behavior and add or update tests
to protect against regressions.
```

