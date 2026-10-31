# Reference: Balanced Autonomy in Autonomous Agents

Autonomous agents must balance initiative with safety.

## The Principle of Least Disruption
- An agent should solve problems autonomously when within scope.
- An agent must NEVER make irrevocable or externally visible decisions without human confirmation.

## Guardrail Matrix
1. **Repository Safety:**
   - Never run `git reset --hard` or `git clean -fd` without explicit human directive.
   - Never force-push (`git push --force`).
2. **Secrets & Credentials:**
   - Never print raw secrets, tokens, or private keys to the terminal, stdout, or logs.
   - Verify that `.gitignore` ignores secret files (`.env`, `*.pem`, `*.key`).
3. **External Systems:**
   - Do not trigger remote production deploys autonomously.
   - Do not send unconfirmed emails or charge external billing accounts.
