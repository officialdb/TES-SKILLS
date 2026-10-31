# TES Adapter Architecture

TES supports multiple AI coding environments using isolated, decoupled adapters. No adapter depends on another.

## Adapter Matrix

| Environment | Key | Global Path | Project Path | Detection Heuristic |
|---|---|---|---|---|
| **Hermes** | `hermes` | `~/.hermes/skills` | `.hermes/skills` | Executable `hermes` or `~/.hermes` exists |
| **OpenCode** | `opencode` | `~/.config/opencode/skills` | `.opencode/skills` | Executable `opencode`/`ai.opencode` or `~/.config/opencode` exists |
| **OpenAI Codex CLI** | `codex` | `~/.codex/skills` | `.codex/skills` | Executable `codex` or `~/.codex` exists |
| **Claude Code** | `claude-code` | `~/.claude/skills` | `.claude/skills` | Executable `claude` or `~/.claude` exists |
| **Gemini CLI** | `gemini-cli` | `~/.gemini/config/skills` | `.gemini/skills` | Executable `gemini` or `~/.gemini` exists |
| **Generic** | `generic` | `~/.agents/skills` | `.agents/skills` | Fallback / default standard directory |

## Adding a Custom Adapter

1. Subclass `BaseAdapter` in `src/tes/adapters/`.
2. Implement:
   - `name`: Human readable name
   - `identifier`: CLI target key (e.g., `my-agent`)
   - `detect()`: Check binary or configuration directories
   - `get_skill_dir(scope)`: Resolve installation directory
3. Register the adapter in `src/tes/adapters/__init__.py`.
