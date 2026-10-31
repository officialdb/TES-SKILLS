# Reference: Common Repository Archetypes

## 1. Web Service (API Backend)
- **Characteristics:** Controllers/routes, serialization, database ORM/migrations, authentication middleware.
- **Key Seams:** Ingress routes, service layer, data persistence.

## 2. Single-Page Application (SPA) / Fullstack
- **Characteristics:** Component hierarchy, routing, state management (Redux, Zustand), API client queries.
- **Key Seams:** Layout templates, page views, query hooks, UI component primitives.

## 3. CLI Utility / Developer Tool
- **Characteristics:** Command parsing (Typer, Click, Cobra), configuration files, terminal I/O, subprocess execution.
- **Key Seams:** Subcommand dispatch, config loader, core operational logic.

## 4. Library / SDK
- **Characteristics:** Minimal dependencies, public exported types, backwards-compatibility constraints.
- **Key Seams:** Public API module (`__init__.py`, `index.ts`), internal implementations.
