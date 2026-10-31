# Reference: Understand Before Modifying

## The Cost of Premature Mutation
When an agent or engineer alters code without adequate context:
- Working edge-case handling is accidentally deleted.
- Conventions established across months of team work are broken.
- Unnecessary dependencies are introduced when native or existing helpers already exist.
- Security assumptions (e.g. CSRF tokens, tenant IDs, input escaping) are bypassed.

## Systematic Exploration Steps

### 1. Build and Dependency Manifests
Always inspect:
- `pyproject.toml`, `requirements.txt`, `Pipfile` (Python)
- `package.json`, `package-lock.json`, `pnpm-lock.yaml` (Node.js/TypeScript)
- `go.mod`, `go.sum` (Go)
- `Cargo.toml`, `Cargo.lock` (Rust)
- `pom.xml`, `build.gradle` (Java/Kotlin)

### 2. Configuration & Environment Files
Check for `.env.example`, `config.yaml`, `docker-compose.yml`, or similar infrastructure descriptions to identify required environment variables and service dependencies.

### 3. Test Suites
Check `tests/`, `spec/`, or co-located `*.test.ts` / `*_test.py` files. Run existing test runners:
```bash
pytest
npm test
cargo test
go test ./...
```
Establish whether the baseline tests pass *before* introducing your change.
