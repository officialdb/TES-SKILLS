---
name: frontend-quality
version: 1.2.0
description: Frontend architecture, Core Web Vitals, component library integration, dashboard grids, and responsive layout resilience. Use when building web apps.
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
5. **Responsive Navigation & Mobile Menu Implementation:**
   - Implement mobile hamburger navigation using semantic `<button>` elements with dynamic accessible labels (`aria-label="Open navigation menu"` / `"Close navigation menu"`), `aria-expanded`, and `aria-controls`.
   - Ensure complete keyboard operability (`Tab`, `Shift+Tab`, `Enter`, `Space`) and add an `Escape` key listener that dismisses open overlay navigation and returns focus to the toggle button.
   - Prevent background body scrolling (`overflow: hidden` on document body) when modal drawers or full-screen navigation overlays are active.
   - Close mobile navigation automatically when a link is clicked, and handle viewport resize gracefully so menus do not linger when returning to desktop views.
   - Share navigation items through a single source-of-truth data structure rather than duplicating markup across desktop and mobile templates. Avoid heavy third-party menu dependencies.
6. **Component Library Selection & Integration (shadcn/ui & Flowbite):**
   - Apply the 10-point evaluation criteria before installing UI packages: check existing project dependencies, styling approach (Tailwind, CSS modules), accessibility, and bundle impact.
   - Favor headless, locally owned primitives (shadcn/ui via Radix UI) or Tailwind-integrated suites (Flowbite) over heavy runtime CSS-in-JS libraries.
   - Reuse existing primitives for standard interactions (Dialog, DropdownMenu, Tabs, Select); customize tokens to match project identity; compose primitives for domain widgets; build custom only when interactions are genuinely unique.
   - Never invent non-existent component props or configurations. Consult the installed library version documentation directly.
7. **Dashboard & Landing Page Technical Implementation:**
   - Implement multi-column dashboard layouts using responsive CSS Grid (`grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6`), persistent or collapsible sidebars, and isolated widget error boundaries.
   - Build accessible data visualizations: circular progress rings via SVG `stroke-dashoffset` with `role="progressbar"`, accessible bar chart figures, and interval-cleared digital timers with polite screen-reader updates.
   - Prevent landing page horizontal overflow from tilted mockup cards using `overflow-x: clip`, and optimize LCP (<2.5s) with eager image preloads and explicit aspect ratios.

---

## 3. Expected Deliverables
1. **Quality Frontend Code:** Clean, typed component implementations without layout shift bugs or decorative pulsing CSS.
2. **Responsive Dashboard & Workspace Grids:** Multi-column layouts, collapsible sidebars, and accessible data widgets with independent error boundaries.
3. **High-Performance Landing Pages:** Hero assets optimized for Core Web Vitals (LCP < 2.5s, CLS < 0.1), fluid typography, and zero horizontal overflow.
4. **Vetted Component Library Integration:** Clean adoption of shadcn/ui, Flowbite, or headless primitives customized to brand tokens without dependency bloat.
5. **Responsive Navigation Components:** Accessible mobile hamburger menus with full keyboard operability, ARIA state bindings, and desktop layouts.
6. **Reviewed Template Content:** User-facing template strings free of em dash crutches and promotional clutter.
7. **Performance Audit:** Verification that bundle sizes and Core Web Vitals fall within budget.

---

## 4. Progressive Disclosure (Reference Documents)
Consult these bundled documents only when specific deep guidance is needed:

- **Core Web Vitals deep-dive and diagnostics:** Consult [core-web-vitals.md](references/core-web-vitals.md).
- **Frontend component library selection and integration:** Consult [frontend-component-library-selection.md](references/frontend-component-library-selection.md).
- **Dashboard layout implementation and data widgets:** Consult [dashboard-layout-implementation.md](references/dashboard-layout-implementation.md).
- **Landing page implementation and performance architecture:** Consult [landing-page-implementation.md](references/landing-page-implementation.md).
- **Responsive navigation implementation and accessibility:** Consult [responsive-navigation-implementation.md](references/responsive-navigation-implementation.md).
- **Frontend performance verification:** Consult [frontend-performance-checklist.md](checklists/frontend-performance-checklist.md).
- **Performance audit report template:** Consult [frontend-audit-report.md](templates/frontend-audit-report.md).
