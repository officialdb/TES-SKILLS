# Getting Started with TES

Welcome to **TES (Techpronnet Engineering Skills)**. This guide walks you through understanding what TES does, installing your first skills into your AI coding agent, and prompting your agent to achieve high-quality engineering results.

---

## 💡 What is TES?

TES is an open, portable distribution and package management system for **AI agent skills**. It equips autonomous coding agents (such as Hermes, OpenCode, Claude Code, OpenAI Codex CLI, and Gemini CLI) with battle-tested engineering workflows, quality standards, security procedures, and memory persistence.

### Fundamental Principle
> **Skills run natively inside your AI coding agent. The TES CLI is never required during active coding sessions.**

Once you install a skill using the `tes` CLI, the skill's instructions, reference manuals, checklists, and templates live directly inside your AI agent's native skills directory. Your AI agent reads and executes these skills automatically without any background daemon or proprietary API.

---

## 🚀 4 Steps to Your First Skill

### Step 1: Check your system health & detected environments

Run `tes doctor` and `tes detect` to confirm your system is ready and see which AI coding agents are installed on your machine:

```bash
# Verify system readiness and write permissions
tes doctor

# Detect active AI environments in your project and user home
tes detect
```

`tes detect` inspects desktop application installations, CLI binaries, and configuration directories. It outputs the recognized adapter name (e.g. `opencode`, `hermes`, `claude-code`, `codex`, `gemini-cli`, or `generic`).

---

### Step 2: Browse the skills catalogue

Search available skills by keyword or domain:

```bash
# List all 15 published skills
tes search

# Search for specific engineering domains
tes search backend
tes search security
tes search design
```

Inspect a skill's purpose, principles, and bundled reference documents before installing:

```bash
tes inspect backend-engineering
```

---

### Step 3: Install a skill or bundle

Install the skill into your target AI agent:

```bash
# Install a single skill globally (available across all your projects)
tes install backend-engineering --target opencode --scope global

# Or install it locally for your current project only
tes install backend-engineering --target opencode --scope project
```

> **Note:** Replace `opencode` with your detected target adapter (e.g., `hermes`, `claude-code`, `codex`, `gemini-cli`, or `generic`).

#### Installing Bundles
You can also install complete suites of curated skills in a single command:

```bash
# Install the core engineering suite (7 foundation engineering skills)
tes install engineering-suite --target opencode --scope global

# Install all 15 TES skills across engineering, security, devops, and design
tes install complete-suite --target opencode --scope global
```

---

### Step 4: Verify the installation

Confirm that your skills were installed cleanly and that the manifest was generated:

```bash
tes list --target opencode --scope global
```

You will see each installed skill, its installed version, and the date it was installed.

---

## 🤖 Using Installed Skills with Your AI Agent

You do not need to run the `tes` CLI to use an installed skill. Simply interact with your AI coding agent as you normally would.

### How to prompt your agent
When asking your AI agent to perform work, reference the relevant TES skill so the agent knows which engineering guidelines to apply:

```text
Act as a senior backend engineer working on this project.

Use the installed TES backend-engineering skill.

Inspect the existing database schema, query patterns, and API routes.
Identify any N+1 query problems and propose practical fixes.
Do not modify files until I review your plan.
```

Your agent will locate the installed `SKILL.md` file in its skills directory, read the progressive disclosure instructions, and consult the appropriate reference manuals (such as `persistence-integration.md`).

---

## 🎯 Getting Better Results from AI Coding Agents

AI coding agents perform significantly better when you provide structured context and clear constraints:

1. **Grant Repository Access:** Ensure your agent has direct read and write access to the project repository.
2. **Inspect Before Modifying:** Always instruct the agent to inspect existing architecture, conventions, and dependencies before writing code.
3. **State Technical & Business Constraints:** Mention required frameworks, databases, backwards-compatibility requirements, and performance budgets.
4. **Demand Automated Tests & Evidence:** Require the agent to write unit or integration tests and report actual execution results.
5. **Work Incrementally:** Break complex features into phases (architecture review, data modeling, implementation, testing) rather than asking for an entire application in a single prompt.

### Reusable Prompt Template
Copy and adapt this template for any coding task:

```text
Project:
[Briefly describe your project and stack]

Task:
[What do you want to achieve?]

Requirements:
[Key functional and technical requirements]

Constraints:
[Existing conventions, dependencies, performance, or backwards compatibility]

Expected outcome:
[What code, documentation, or test results should be delivered?]

Use the relevant installed TES skills.
Inspect the existing codebase before making changes.
Preserve existing conventions and architecture.
Write automated tests and report the actual verification results.
```

---

## 📚 Next Steps

- Explore ready-to-use prompts in the [Prompt Library](prompt-library.md).
- Learn full CLI command options in the [Command Reference](commands.md).
- Solve common setup questions in the [Troubleshooting Guide](troubleshooting.md).
- Understand how adapters integrate with different agents in [Adapters Documentation](adapters.md).
