# TES Security Model & Guardrails

## Core Principles

TES acts as a skill package manager for AI agents. It prioritizes package safety, environment protection, and deterministic boundaries.

### 1. Path Traversal Mitigation
Whenever skills or manifests are copied, linked, or uninstalled:
- Destination paths are resolved to their canonical real paths.
- Paths are strictly checked against the designated installation root.
- Any attempt to escape via relative dots (`../../`) or symlink redirects is aborted with a `SecurityException`.

### 2. Package Integrity & Manifests
- Installations create or update `.tes-manifest.json` in the target directory.
- Every installed file's relative path and SHA-256 hash are recorded.
- Uninstallation strictly deletes *only* files explicitly recorded in the manifest.
- If a user modified or introduced custom files in a skill directory, TES warns and preserves them.

### 3. Untrusted Script Execution Guard
- TES skills may contain deterministic utility scripts (e.g., repository scanners, schema inspectors).
- The TES CLI **never** executes these scripts automatically during installation, update, or uninstallation.
- Execution is delegated solely to the developer or the host AI agent under explicit user permission.

### 4. Balanced Autonomy Guardrails
TES skills instill strict autonomy levels in AI agents:
- Reading, inspection, and static analysis: Allowed automatically.
- Local code modifications & local tests: Permitted within authorized tasks.
- Remote git operations, production deployments, and database schema mutations: Require explicit human approval.
