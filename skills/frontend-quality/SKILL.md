---
name: frontend-quality
version: 1.0.1
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
`frontend-quality` provides agents with engineering standards for building fast, maintainable, responsive, and resilient frontend web applications. It emphasizes predictable state management, Core Web Vitals optimization, CSS motion discipline, and component composition.

- **Primary Skill For:** Implementing frontend components, optimizing interactive responsiveness, auditing template copy, and eliminating unnecessary CSS animation overhead.
- **Composition:** Pair with `ui-ux-standards` when designing visual layouts or defining design tokens.
- **Ownership Boundary:** Visual design foundations, color palettes, and typographic scales belong to `ui-ux-standards`.

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
2. **Component Composition & Resilience:**
   - Design small, focused components with explicit props and strong TypeScript typing. Separate presentational components from stateful data-fetching containers.
   - Build mobile-first. Ensure layouts adapt seamlessly from 320px mobile viewports to ultra-wide displays without horizontal scrolling.
3. **CSS Motion Hygiene (Eliminate Decorative Blinking):**
   - Avoid unnecessary blinking and pulsing CSS animations. Prohibit `@keyframes` pulse or blink animations on decorative elements (e.g., `animate-pulse` or `animate-ping` on static section badges or title dots).
   - Identify decorative animated dots during frontend reviews and remove them.
   - Preserve functional animations when genuinely necessary (active streaming, real-time connecting); require animated status indicators (such as `<LiveBadge />`) to bind directly to reactive state boolean flags (`isStreaming`, `isConnecting`). When state is idle or static, animations must be inactive.
   - Wrap continuous keyframe animations inside `@media (prefers-reduced-motion: no-preference)`.
4. **Template String & Copy Auditing:**
   - Avoid excessive em dashes in user-facing website strings. Review headings, descriptions, paragraphs, buttons, and marketing copy across JSX templates, HTML files, and localization records to eliminate em dashes (`—`).
   - Refactor copy into natural grammatical structures (commas, prepositions, or distinct sentences). Preserve functional animations and technical uses of the em dash where appropriate (such as code identifiers and CLI arguments).

---

## 3. Expected Deliverables
1. **Quality Frontend Code:** Clean, typed component implementations without layout shift bugs or decorative pulsing CSS.
2. **Reviewed Template Content:** User-facing template strings free of em dash crutches and promotional clutter.
3. **Performance Audit:** Verification that bundle sizes and Core Web Vitals fall within budget.
4. **Responsive Verification:** Evidence of verified layout integrity across mobile, tablet, and desktop breakpoints.

---

## 4. Progressive Disclosure (Reference Documents)
Consult these bundled documents only when specific deep guidance is needed:

- **Core Web Vitals deep-dive and diagnostics:** Consult [core-web-vitals.md](references/core-web-vitals.md).
- **Frontend performance verification:** Consult [frontend-performance-checklist.md](checklists/frontend-performance-checklist.md).
- **Performance audit report template:** Consult [frontend-audit-report.md](templates/frontend-audit-report.md).
