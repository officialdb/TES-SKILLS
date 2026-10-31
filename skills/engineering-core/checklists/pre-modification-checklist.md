# Pre-Modification Checklist

Before editing any file:
- [ ] Have I identified the repository's programming language and runtime version?
- [ ] Have I checked for existing linters and formatting rules (`.editorconfig`, `eslint`, `black`, `ruff`)?
- [ ] Have I located existing tests for this module or feature?
- [ ] Does the current test suite pass cleanly before my changes?
- [ ] Have I identified whether this component touches authentication, database queries, or external network requests?
- [ ] Is my planned change the minimal necessary diff, or does it unnecessarily re-architect working code?
