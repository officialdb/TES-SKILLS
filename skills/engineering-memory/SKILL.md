---
name: engineering-memory
description: Local-first, offline project memory system using structured markdown (.engineering/) for architecture decisions, lessons, and standards. Trigger when recording technical decisions, capturing lessons learned, establishing project standards, or reading project memory.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Engineering Memory

## Purpose
`engineering-memory` establishes a persistent, local-first, offline engineering memory system for software projects. It requires no cloud database, vector store, or proprietary API — operating entirely via structured Markdown files located inside `.engineering/` in the project root.

---

## 1. Directory Structure

```text
project-root/
└── .engineering/
    ├── project-profile.md        # Core identity, mission, tech stack, and primary URLs
    ├── architecture.md           # High-level architecture, module boundaries, data flows
    ├── engineering-standards.md  # Code style, testing rules, typing, PR conventions
    ├── design-standards.md       # Visual philosophy, typography, spacing, UI tokens
    ├── security-profile.md       # Trust boundaries, auth patterns, known sensitive areas
    ├── decisions/                # Architectural Decision Records (ADRs)
    │   └── ADR-0001-init.md
    ├── lessons/                  # Retrospectives and learned invariants from past bugs
    │   └── LESSON-001.md
    └── tasks/                    # Active task specifications and historical milestones
```

---

## 2. Memory Ingestion & Updating Workflow

```
[Agent Reads .engineering/ at Startup]
                  |
                  v
[Execute Development Work Within Established Constraints]
                  |
                  v
[Identify Significant Architectural Decision or Hard Bug Lesson]
                  |
                  v
[Record Atomic Markdown Record in decisions/ or lessons/]
                  |
                  v
[Commit to Version Control alongside Code]
```

### Protocol for Recording Memories:
1. **Never Store Secrets:** Do not commit passwords, API keys, private tokens, or personal identifiers into `.engineering/`.
2. **Distinguish Policy from Temporary Context:** Only record durable engineering standards, architectural decisions, and repeatable lessons. Do not record temporary scratchpad output as permanent policy.
3. **Include Date and Context:** Always document the date, deciders, problem context, and rationale.

---

## 3. Initializing Engineering Memory

To initialize `.engineering/` in the current project, agents or developers can run the bundled initialization script:
```bash
python scripts/init_memory.py [PROJECT_DIR]
```

---

## 4. Deliverables & Outputs
1. **Durable Knowledge Records:** Version-controlled Markdown documentation preserving team knowledge across agent sessions.
2. **Zero External Dependencies:** 100% offline and searchable via standard file inspection tools.
