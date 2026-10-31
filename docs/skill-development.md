# TES Skill Development Guide

Skills in TES follow the open Agent Skills standard. A skill is a self-contained directory with a `SKILL.md` entry point.

## Directory Structure

```text
skills/<skill-name>/
├── SKILL.md             # Required: YAML frontmatter + core intelligence & instructions
├── references/          # Optional: Deep architectural guidelines, standards, and manuals
│   └── reference-doc.md
├── templates/           # Optional: Starter templates, file boilerplates
│   └── template.md
├── checklists/          # Optional: Verification and audit checklists
│   └── checklist.md
├── scripts/             # Optional: Deterministic helper scripts (sandboxed, explicit execution)
│   └── helper.py
└── examples/            # Optional: Before/after code snippets or case studies
    └── example.md
```

## SKILL.md Specifications

A valid `SKILL.md` starts with a strict YAML frontmatter block:

```markdown
---
name: my-engineering-skill
description: Comprehensive description explaining exact triggers, capabilities, and outputs.
version: 1.0.0
category: engineering
tags:
  - architecture
  - quality
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Skill Title

## Overview
What this skill teaches the AI agent.

## Activation Triggers
When the agent should invoke this skill.

## Core Workflows
Step-by-step guidance.

## Verification & Outputs
Expected deliverables and validation criteria.
```

## Progressive Disclosure Philosophy
Keep the initial `name` and `description` concise and trigger-rich (~100-200 tokens). Place specialized or exhaustive specifications into `references/` so the agent loads them only when needed.
