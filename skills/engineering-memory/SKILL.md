---
name: engineering-memory
description: Local-first, offline project memory system using structured markdown (.engineering/) for architecture decisions and lessons. Use when recording or recalling project knowledge.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Engineering Memory

## Purpose & Activation
`engineering-memory` establishes a persistent, local-first, offline engineering memory system using structured Markdown files inside `.engineering/`. It requires no external cloud databases, vector stores, or APIs.

- **Primary Skill For:** Recording Architectural Decision Records (ADRs), capturing lessons learned from hard bugs, and retrieving project-specific conventions.
- **Composition:** Combine with any implementation skill when an architectural pivot occurs or durable lessons need recording.
- **Cardinal Rule: Selective Retrieval:** Never load all `.engineering/` files at startup. Load only the specific document relevant to the immediate task.

---

## 1. Directory Structure

```text
.engineering/
├── project-profile.md        # Core identity, stack, repository URLs, and conventions
├── architecture.md           # High-level architecture, module boundaries, data flows
├── engineering-standards.md  # Code conventions, testing policy, PR standards
├── design-standards.md       # Visual direction, typography, design tokens
├── security-profile.md       # Trust boundaries, auth patterns, sensitive areas
├── decisions/                # Architectural Decision Records (ADR-0001-*.md)
├── lessons/                  # Learned invariants from past bugs (LESSON-001.md)
└── tasks/                    # Active task specifications and historical milestones
```

---

## 2. Selective Retrieval Protocol
Agents must load knowledge selectively to conserve context tokens:

1. **Project Profile:** Read `project-profile.md` only when initial project context or repository identity is needed.
2. **Architecture:** Read `architecture.md` only when architectural, modular, or cross-service integration changes are involved.
3. **Security Profile:** Read `security-profile.md` only when touching authentication, secrets, or sensitive boundaries.
4. **Design Standards:** Read `design-standards.md` only for interface, styling, or UX component work.
5. **Decisions & Lessons:** Read specific files in `decisions/` or `lessons/` only when relevant to the subsystem being modified.
6. **Task Histories:** Do not load completed task logs from `tasks/` unless explicitly requested.
7. **Context Deduplication:** Do not re-read memory files if their contents are already present in the active conversation context.

---

## 3. Protocol for Recording Memories

1. **No Secrets:** Never commit API keys, tokens, passwords, or personal data into `.engineering/`.
2. **Durable Knowledge Only:** Record durable policies, architecture choices, and bug invariants. Do not save temporary scratchpad output as permanent policy.
3. **Structured Attribution:** Always include the date, author, context, evaluated alternatives, and consequences.
4. **Version Control:** Commit `.engineering/` updates alongside the corresponding code changes in Git.

---

## 4. Expected Deliverables
1. **Durable Knowledge Records:** Version-controlled Markdown files in `.engineering/decisions/` or `.engineering/lessons/`.
2. **Project Profile Setup:** Initialized `.engineering/` workspace via `python scripts/init_memory.py [DIR]`.

---

## 5. Progressive Disclosure (Reference Documents)
Consult these bundled documents only when specific deep guidance is needed:

- **Offline memory protocol details:** Consult [offline-memory-protocol.md](references/offline-memory-protocol.md).
- **Memory hygiene checklist:** Consult [memory-hygiene-checklist.md](checklists/memory-hygiene-checklist.md).
- **ADR template:** Consult [decision.md](templates/decision.md).
- **Bug retrospective template:** Consult [lesson.md](templates/lesson.md).
- **Project profile template:** Consult [project-profile.md](templates/project-profile.md).
- **Workspace initializer script:** Available at `scripts/init_memory.py`.
