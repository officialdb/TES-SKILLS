# Security Policy

Techpronnet Technologies takes the security of the TES ecosystem seriously.

## Threat Model & Boundaries

TES is an AI skill distribution package manager. It manages files installed directly into host AI agent skill paths.

Key security controls implemented in TES:
1. **Path Traversal Mitigation:** All skill copy, extract, and uninstall operations validate target paths to prevent escaping designated skill directories.
2. **Untrusted Script Execution Guard:** The CLI never automatically executes scripts or binaries bundled within skills upon installation.
3. **Overwrite & Ownership Guards:** Skills not tracked by TES manifests will not be deleted or overwritten without explicit warning.
4. **Offline Local First:** The core CLI operates completely offline with zero telemetry or network calls required for local skills and registry operations.
5. **No Secrets Logging:** TES commands never log credentials, API keys, or environment secrets.

## Reporting a Vulnerability

If you discover a security vulnerability within TES:
- Do not disclose it publicly on GitHub issues or forums.
- Email `security@techpronnet.com` with a description of the issue, proof of concept, and impact assessment.
- You will receive an acknowledgment within 48 hours.
