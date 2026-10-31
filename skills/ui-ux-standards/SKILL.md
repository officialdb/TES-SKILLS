---
name: ui-ux-standards
version: 1.1.0
description: Professional, accessible interface design with clear visual hierarchy, purposeful color, responsive navigation, and WCAG compliance. Use for UI/UX work.
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
`ui-ux-standards` guides coding agents in designing clean, professional, accessible, and delightful digital user interfaces. It emphasizes visual restraint, typography, whitespace, purposeful color, and authentic copywriting over noisy decorative fads.

- **Primary Skill For:** Designing user interfaces, defining visual styles, styling layouts, establishing copy presentation standards, and ensuring accessibility compliance.
- **Composition:** Pair with `frontend-quality` when translating UI specs into high-performance web components.
- **Ownership Boundary:** CSS animation implementation and Core Web Vitals belong to `frontend-quality`.

---

## 1. Design Philosophy: Restraint & Clarity

1. **Clear Visual Hierarchy:**
   - Establish unambiguous visual priority: primary actions, secondary options, and background information must be instantly distinguishable through size, weight, and position.
   - Limit each view or card to one primary call-to-action (CTA).
2. **Disciplined Typography & Spacing:**
   - Use a disciplined typographic scale with comfortable line heights (`leading-relaxed` for body, `leading-tight` for headings).
   - Maintain readable line lengths (45–75 characters per line for prose).
   - Base margins, paddings, and component sizes on a strict 4px / 8px spatial grid. Use whitespace rather than heavy divider lines.
3. **Purposeful Color & Motion Restraint:**
   - Build upon neutral, muted backgrounds (slate, zinc, or gray). Reserve vibrant accent colors strictly for interactive focus, primary actions, and semantic state indicators.
   - **No Decorative Animated Dots:** Prohibit decorative blinking, flashing, or pulsing dots. No unnecessary animated dot indicators in headings, hero sections, navigation, backgrounds, or content. Animated dots used merely to appear "modern" create cognitive distraction and mimic alarms.
   - **Functional Indicators Permitted:** Functional loading, connection, and status indicators remain permitted when genuinely necessary (real-time connection, active streaming, background progress). Prefer subtle, purposeful animation over distracting visual effects.

---

## 2. Website Copywriting & Presentation

1. **Avoid Em Dashes in Website Copy:**
   - Strong preference to avoid em dashes (`—`) in website copy across headings, hero sections, navigation, descriptions, paragraphs, buttons, testimonials, CTAs, and metadata.
   - Prefer natural sentence construction, commas, full stops, and colons. Do not mechanically replace em dashes with commas; rewrite sentences naturally.
   - *Examples:*
     - Avoid: "Build better systems — without the complexity." -> Prefer: "Build better systems without unnecessary complexity."
     - Avoid: "Everything your team needs — in one place." -> Prefer: "Everything your team needs in one place."
     - Avoid: "We help businesses grow — with technology that works." -> Prefer: "We help businesses grow with technology that works."
   - *Context Boundary:* Technical documentation, code syntax, and CLI flags remain exempt when syntactically required.
2. **Authentic, Professional Tone:**
   - Write clearly and concisely without generic AI promotional jargon ("supercharge", "unleash", "cutting-edge").
   - Avoid exaggerated claims and unearned superlatives. Never fabricate testimonials, metrics, or capabilities. Adapt tone to the specific industry and user context.

---

## 3. Responsive Navigation Design

1. **Desktop Navigation Architecture:**
   - Display primary navigation links in a clean, accessible horizontal layout with consistent spacing (24–32px gap).
   - Maintain clear visual hierarchy: brand logo left-aligned, navigation links centered or left-aligned, and primary action CTAs on the right.
   - Prevent overcrowding by limiting top-level links to 5–7 items; route secondary utility links to submenus or footers.
2. **Mobile Hamburger Menu:**
   - Replace horizontal links with a recognizable hamburger control (three horizontal lines or equivalent menu icon) at the responsive breakpoint.
   - Reveal navigation links in a readable layout with generous touch-friendly targets (minimum 44x44px tap area).
   - Provide an unambiguous close control (distinct close icon or animated toggle state) and ensure open menus do not unnecessarily obscure content.
   - Preserve the website's brand identity across typography, elevation, and accent styling.
3. **Responsive Breakpoint Behavior:**
   - Define collapse breakpoints based on content width and link volume rather than blindly forcing an arbitrary fixed pixel threshold.
   - Ensure fluid layout resilience across mobile (375px), tablet (768px), laptop (1024px), and desktop (1440px) in both portrait and landscape modes without horizontal overflow.
4. **Pattern Selection:**
   - Choose the navigation archetype that fits the product: dropdown navigation (compact sites), slide-in side drawer (web applications and dashboards), full-screen overlay (editorial or portfolio), or expandable accordion panel (hierarchical sites). Adapt to project architecture rather than forcing a single style.

---

## 4. Accessibility & Universal Usability (WCAG 2.1 AA)

- **Color Contrast:** Ensure text achieves a minimum contrast ratio of 4.5:1 against its background (3:1 for large text 18pt+). Never convey critical status by color alone.
- **Keyboard Navigation & Focus:** Every interactive element must be reachable and operable via keyboard (`Tab`, `Shift+Tab`, `Enter`, `Space`). Never remove focus rings without providing an equally visible custom focus outline.
- **Semantic HTML & Motion:** Use native semantic elements. Honor `@media (prefers-reduced-motion: reduce)` by disabling non-essential transitions.

---

## 5. Expected Deliverables
1. **Polished UI Components:** Accessible, beautifully spaced, responsive interface designs free of decorative blinking artifacts.
2. **Responsive Navigation Specs:** Clean desktop layouts and mobile hamburger menu designs adapted to product architecture.
3. **Refined Website Copy:** Natural, human-sounding interface copy free of em dash crutches and promotional clichés.
4. **Design Specification:** Clear design tokens (typography, color, spacing) matching existing systems.
5. **Accessibility Sign-off:** Verification of keyboard navigation, screen reader labels, and contrast compliance.

---

## 6. Progressive Disclosure (Reference Documents)
Consult these bundled documents only when specific deep guidance is needed:

- **WCAG 2.1 AA accessibility guidelines:** Consult [accessibility-wcag.md](references/accessibility-wcag.md).
- **Visual design foundations and copy guidelines:** Consult [visual-design-principles.md](references/visual-design-principles.md).
- **Responsive navigation design patterns:** Consult [responsive-navigation-design.md](references/responsive-navigation-design.md).
- **Responsive navigation verification checklist:** Consult [responsive-navigation-checklist.md](checklists/responsive-navigation-checklist.md).
- **UI/UX inspection checklist:** Consult [ui-ux-review-checklist.md](checklists/ui-ux-review-checklist.md).
- **Design specification template:** Consult [design-spec-template.md](templates/design-spec-template.md).
