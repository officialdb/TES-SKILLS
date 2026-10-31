# Reference: Offline Engineering Memory Protocol

## Why Markdown in Git?
- **No API keys or cloud subscriptions needed:** 100% free and portable.
- **Auditable & Version Controlled:** Changes to architectural standards travel with the code in pull requests.
- **Zero Latency:** Reading a markdown file takes under 1ms.
- **Agent Agnostic:** Every coding agent knows how to read and write Markdown.

## Partitioning Context: Project vs Global
- Project-specific constraints live in `project/.engineering/`.
- Developer-wide or global preferences belong in global agent configuration (`~/.agents` or `~/.gemini/config`).
