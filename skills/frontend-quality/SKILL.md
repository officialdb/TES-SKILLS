---
name: frontend-quality
description: Modern frontend architecture, responsive resilience, Core Web Vitals performance, component composition, and state predictability. Trigger when developing frontend web applications, optimizing rendering performance, refactoring components, or debugging layout shifts.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# Frontend Quality

## Purpose
`frontend-quality` provides agents with engineering standards for building fast, maintainable, responsive, and resilient frontend applications. It emphasizes predictable state management, Core Web Vitals optimization, and component composition.

---

## 1. Core Web Vitals & Performance Engineering

Target thresholds for production web applications:

| Metric | Target (Good) | Description | Primary Optimizations |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | **<= 2.5s** | Loading speed of main visual content | Compress images (WebP/AVIF), preload hero assets, SSR |
| **INP** (Interaction to Next Paint) | **<= 200ms** | Responsiveness to user input/clicks | Debounce expensive handlers, yield to main thread, avoid long tasks |
| **CLS** (Cumulative Layout Shift) | **<= 0.1** | Visual stability during render | Explicit aspect ratios on images/videos, reserve skeleton dimensions |

---

## 2. Component Architecture Principles

1. **Unidirectional Data Flow & State Locality:**
   - Keep state as close to where it is used as possible. Do not lift state into global stores unless shared across distant modules.
   - Separate stateful container components from pure, presentational UI primitives.

2. **Error Boundaries & Graceful Degradation:**
   - Wrap risky widget components (charts, third-party embeds) in React/framework Error Boundaries to prevent a local failure from crashing the entire page.

3. **Responsive Resilience:**
   - Test layout integrity on mobile viewports (320px–375px), avoiding text overflow, horizontal scroll leaks, and touch targets smaller than 44x44px.

4. **Bundle & Asset Hygiene:**
   - Use dynamic imports / code-splitting for heavy routes and third-party visualization libraries.
   - Avoid importing entire utility libraries when only a single function is needed.

---

## 3. Deliverables & Outputs
1. **High-Performance Components:** Typed, modular UI code with minimal re-renders.
2. **Performance Audit:** Measurement of bundle size, layout shift prevention, and response times.
