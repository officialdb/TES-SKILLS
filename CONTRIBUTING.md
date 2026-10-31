# Contributing to TES

Thank you for your interest in contributing to Techpronnet Engineering Skills (TES).

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/officialdb/TES-SKILLS.git
   cd TES-SKILLS
   ```

2. Create a virtual environment or use existing Python 3.10+:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

3. Run the test suite:
   ```bash
   pytest
   ```

## Branching Strategy

TES uses a dual-branch model:
- **`main`**: Production-ready, stable releases. Direct commits are restricted to tagged release promotions.
- **`develop`**: Active integration branch for ongoing development, new features, and bug fixes. Feature branches should branch from and open pull requests against `develop`.

## Authoring New Skills

Every skill must adhere to the Agent Skills open standard:
1. Reside in `skills/<skill-name>/` with a lowercase alphanumeric hyphen-separated name (`^[a-z0-9]+(-[a-z0-9]+)*$`).
2. Provide a valid `SKILL.md` with YAML frontmatter containing `name` and `description`.
3. Provide supporting subdirectories where relevant:
   - `references/`: Architectural guidelines, checklists, background references.
   - `templates/`: Boilerplate files, markdown templates, configuration snippets.
   - `checklists/`: Actionable verification lists.
   - `scripts/`: Optional helper scripts (deterministic, with no network side-effects unless explicitly required).
   - `examples/`: Realistic before/after examples.
4. Run `tes validate` to ensure your skill passes all integrity and schema checks.

## Code Standards
- Adhere to PEP 8 standards.
- Use explicit type annotations everywhere.
- Maintain comprehensive unit and integration tests.
