---
name: ui-ux-standards
description: Professional, accessible interface design with clear visual hierarchy, purposeful color, clean typography, and WCAG compliance. Use for UI/UX work.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# UI/UX Standards

## Purpose & Activation
`ui-ux-standards` guides coding agents in designing and implementing professional, clean, accessible, and delightful digital user interfaces. It emphasizes restraint, typography, whitespace, purposeful color, and accessibility over noisy decorative fads.

- **Primary Skill For:** Designing user interfaces, defining visual styles, styling layouts, polishing component aesthetics, and ensuring accessibility compliance.
- **Composition:** Pair with `frontend-quality` when translating UI specs into high-performance web components.
- **Ownership Boundary:** Core Web Vitals and frontend runtime performance belong to `frontend-quality`.

---

## 1. Design Philosophy: Restraint & Clarity

1. **Clear Visual Hierarchy:**
   - Establish unambiguous visual priority: primary actions, secondary options, and background information must be instantly distinguishable through size, weight, and position.
   - Limit each view or card to one primary call-to-action (CTA).
2. **Disciplined Typography:**
   - Use a disciplined typographic scale with comfortable line heights (`leading-relaxed` for body, `leading-tight` for headings).
   - Maintain readable line lengths (45–75 characters per line for prose).
3. **Purposeful Color System:**
   - Build upon neutral, muted backgrounds (slate, zinc, or gray).
   - Reserve vibrant accent colors strictly for interactive focus, primary actions, and semantic state indicators (success, warning, destructive).
4. **Spatial Discipline:**
   - Base all margins, paddings, and component sizes on a strict 4px / 8px spatial grid.
   - Use generous whitespace to separate distinct cognitive sections rather than cluttering views with heavy divider lines.

---

## 2. Accessibility & Universal Usability (WCAG 2.1 AA)

- **Color Contrast:** Ensure text achieves a minimum contrast ratio of 4.5:1 against its background (3:1 for large text 18pt+). Never convey critical status by color alone.
- **Keyboard Navigation:** Every interactive element must be reachable and operable via keyboard (`Tab`, `Shift+Tab`, `Enter`, `Space`).
- **Focus Indicators:** Never remove focus rings (`outline: none`) without providing an equally visible custom focus outline.
- **Semantic HTML:** Use native elements (`<button>`, `<a>`, `<nav>`, `<main>`) rather than `<div>` with click listeners.
- **Motion Restraint:** Honor `@media (prefers-reduced-motion: reduce)` by disabling non-essential transitions and parallax animations.

---

## 3. Expected Deliverables
1. **Polished UI Components:** Accessible, beautifully spaced, responsive interface code.
2. **Design Specification:** Clear design tokens (typography, color, spacing) matching existing systems.
3. **Accessibility Sign-off:** Verification of keyboard navigation, screen reader labels, and contrast compliance.

---

## 4. Progressive Disclosure (Reference Documents)
Consult these bundled documents only when specific deep guidance is needed:

- **WCAG 2.1 AA accessibility guidelines:** Consult [accessibility-wcag.md](references/accessibility-wcag.md).
- **Visual design foundations and tokens:** Consult [visual-design-principles.md](references/visual-design-principles.md).
- **UI/UX inspection checklist:** Consult [ui-ux-review-checklist.md](checklists/ui-ux-review-checklist.md).
- **Design specification template:** Consult [design-spec-template.md](templates/design-spec-template.md).
