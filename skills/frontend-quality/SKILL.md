---
name: frontend-quality
description: Frontend architecture, Core Web Vitals optimization, responsive layout resilience, and state predictability. Use when building or optimizing web interfaces.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Frontend Quality

## Purpose & Activation
`frontend-quality` provides agents with engineering standards for building fast, maintainable, responsive, and resilient frontend web applications. It emphasizes predictable state management, Core Web Vitals optimization, and component composition.

- **Primary Skill For:** Implementing frontend components, improving page load speeds, debugging layout shifts, and optimizing interactive responsiveness.
- **Composition:** Pair with `ui-ux-standards` when designing new visual components or refining user flows.
- **Ownership Boundary:** Typography scale, color palettes, and WCAG accessibility standards belong to `ui-ux-standards`.

---

## 1. Core Web Vitals & Performance Targets

| Metric | Target (Good) | Description | Key Optimizations |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | < 2.5s | Time until main hero content is rendered | Preload hero images, optimize webfonts, server-render critical markup |
| **INP** (Interaction to Next Paint) | < 200ms | Latency of page responsiveness to user inputs | Yield main thread, debounce input handlers, avoid long JavaScript tasks |
| **CLS** (Cumulative Layout Shift) | < 0.1 | Unexpected layout shifts during rendering | Explicit `width`/`height` on images and embeds, reserve space for dynamic content |

---

## 2. Frontend Architecture Standards

1. **Predictable State Management:**
   - Maintain a single source of truth for UI state. Avoid synchronizing state across multiple independent stores.
   - Keep state local to the components that need it; lift state up only when siblings share data.
2. **Component Composition:**
   - Design small, focused components with explicit props and strong TypeScript typing.
   - Separate presentational components from stateful data-fetching containers.
3. **Responsive Resilience:**
   - Build mobile-first. Ensure layouts adapt seamlessly from 320px mobile viewports to ultra-wide displays without horizontal scrolling.
   - Handle edge-case content gracefully: empty states, long unbreakable strings, missing avatars, and network error banners.

---

## 3. Expected Deliverables
1. **Quality Frontend Code:** Clean, typed component implementations without layout shift bugs.
2. **Performance Audit:** Verification that bundle sizes and Core Web Vitals fall within budget.
3. **Responsive Verification:** Evidence of verified layout integrity across mobile, tablet, and desktop breakpoints.

---

## 4. Progressive Disclosure (Reference Documents)
Consult these bundled documents only when specific deep guidance is needed:

- **Core Web Vitals deep-dive and diagnostics:** Consult [core-web-vitals.md](references/core-web-vitals.md).
- **Frontend performance verification:** Consult [frontend-performance-checklist.md](checklists/frontend-performance-checklist.md).
- **Performance audit report template:** Consult [frontend-audit-report.md](templates/frontend-audit-report.md).
