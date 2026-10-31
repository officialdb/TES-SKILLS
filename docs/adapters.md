# TES Adapter Architecture

TES supports multiple AI coding environments using isolated, decoupled adapters. No adapter depends on another.

## Multi-Method Environment Discovery Architecture

Beginning in v0.2.1, TES decouples **Application Discovery** from **Skill Integration**. AI coding applications can be installed via multiple channels (Desktop GUI, CLI on PATH, native package manager, or manual directory installations). Relying solely on CLI binary existence on `$PATH` causes false negatives when an application is installed primarily as a desktop application (such as OpenCode).

```text
TES Detection Engine
│
├── Application Discovery (Multi-Method)
│   ├── CLI Discovery (PATH & known binary locations)
│   ├── Desktop Application Discovery (.desktop launchers & /opt directories)
│   ├── Package Manager Discovery (dpkg/apt, rpm, flatpak, snap)
│   └── Manual Directory Discovery (/opt/AppName, /usr/lib/AppName)
│
├── Configuration Discovery
│   ├── Global Configuration (~/.config/<app>/, ~/.<app>/)
│   ├── Project Configuration (.<app>/)
│   └── Native Skills Directories
│
└── Environment Adapters
    ├── Hermes
    ├── OpenCode
    ├── Codex
    ├── Claude Code
    ├── Gemini CLI
    └── Generic Agent Skills
```

## Adapter Matrix

| Environment | Key | Global Path | Project Path | Executable Discovery | Desktop Discovery | Package Discovery | Recognized Configuration |
|---|---|---|---|---|---|---|---|
| **Hermes** | `hermes` | `~/.hermes/skills` | `.hermes/skills` | `hermes` | `hermes.desktop` | `hermes` | `~/.hermes/config.json`, `hermes.json` |
| **OpenCode** | `opencode` | `~/.config/opencode/skills` | `.opencode/skills` | `opencode`, `ai.opencode` | `*opencode*.desktop`, `/opt/OpenCode/ai.opencode` | `opencode` (dpkg/rpm/snap/flatpak) | `~/.config/opencode/opencode.json` |
| **OpenAI Codex CLI** | `codex` | `~/.codex/skills` | `.codex/skills` | `codex` | `*codex*.desktop` | `codex` | `~/.codex/config.toml`, `version.json` |
| **Claude Code** | `claude-code` | `~/.claude/skills` | `.claude/skills` | `claude` | `*claude*.desktop` | `claude`, `claude-code` | `~/.claude/config.json`, `~/.claude.json` |
| **Gemini CLI** | `gemini-cli` | `~/.gemini/config/skills` | `.gemini/skills` | `gemini` | `*gemini*.desktop` | `gemini-cli` | `~/.gemini/config/config.json` |
| **Generic** | `generic` | `~/.agents/skills` | `.agents/skills` | N/A (Target) | N/A | N/A | Open Agent Skills Standard |

## Independent Detection Properties

Each environment adapter evaluates independent properties to ensure complete accuracy without false positives or false negatives:

- `application_found`: Verified presence of the actual application via Desktop launcher, Package Manager, or CLI.
- `installation_method`: How the application was installed (`Desktop`, `CLI`, `Package Manager`, `Desktop, CLI`, `Manual`, or `—`).
- `executable_found`: Usable CLI binary discovered on system `$PATH` or known executable paths.
- `version_verified`: Version successfully extracted from CLI, desktop metadata, or version files.
- `application_path`: Verified path to the desktop binary or CLI executable.
- `config_present`: Recognized vendor configuration files exist (directory presence alone or TES-created directories do NOT trigger this).
- `skills_directory_present`: Native skill directory exists.
- `project_config_present`: Project-level agent configuration exists.
- `available`: TES supports skill distribution to this target.
- `installed`: Compatibility alias reflecting verified application installation (`application_found`).

Generic Agent Skills is treated strictly as an open distribution target, not an executable application (`installed=False`, `is_application=False`).

## Desktop Discovery Rules

The `DesktopDiscoveryProvider`:
1. Scans standard desktop entry locations (`/usr/share/applications`, `/usr/local/share/applications`, `~/.local/share/applications`, Flatpak, and Snap application directories).
2. Parses matching `.desktop` entries without executing untrusted scripts.
3. Extracts and validates the binary target specified in `Exec=`. If the target binary does not exist on disk, the launcher is safely ignored.
4. Checks known installation directories (`/opt/OpenCode`, etc.) for application binaries and metadata files (e.g. `resources/opencode-cli.version`).

## Detection Safety & Project Root

Environment detection is strictly read-only:
- No directories or files are created during detection or diagnostic checks.
- Project root discovery walks upwards looking for recognized markers (`.git`, `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, `composer.json`, `requirements.txt`).
- The user's home directory is never automatically classified as a project root.
- Explicit project root paths can be specified via `tes detect --project <path>`.

## Adding a Custom Adapter

1. Subclass `BaseAdapter` in `src/tes/adapters/`.
2. Implement:
   - `name`: Human readable name
   - `target_id`: CLI target key (e.g., `my-agent`)
   - `get_app_spec()`: Return `ApplicationSpec` with CLI, desktop, and package manager patterns.
   - `get_skill_dir(scope)`: Resolve installation directory
3. Register the adapter in `src/tes/adapters/__init__.py`.
