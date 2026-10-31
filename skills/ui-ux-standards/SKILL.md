---
name: ui-ux-standards
version: 1.2.0
description: Professional, accessible interface design with clear visual hierarchy, purposeful color, responsive layouts, dashboard composition, and WCAG compliance.
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

## 4. Interface Layout Patterns & Library Brand Independence

1. **Dashboard Composition (Grounded in Reference A):**
   - Structure desktop dashboards around a persistent vertical sidebar (brand top, primary/secondary links, user profile anchor at bottom) and a contextual header (greeting, search, utility icons, primary action CTA).
   - Organize multi-column workspaces into discrete card widgets grouped by purpose: analytical metrics (bar charts, circular progress), active utilities (timers, note checklists), and status trackers.
   - Balance high information density with 16–24px internal card padding and subtle 1px container borders rather than heavy drop shadows.
   - Reserve accent colors (e.g. purple) strictly for active navigation, key CTAs, and chart fills.
2. **Landing Page Architecture (Grounded in Reference B):**
   - Structure desktop headers horizontally with brand on the left, primary navigation in the center, and account links / primary CTA on the right.
   - Use centered editorial hero layouts pairing expressive serif headlines with constrained sans-serif descriptions (`max-w-2xl` / 500–680px) to maximize readability.
   - Enforce conversion action hierarchy: pair a solid primary CTA button with a complementary outlined secondary action ("Watch A Demo").
   - Feature product-led visual showcases (realistic interface mockups, outcome badges like "$5,000 collected") in place of abstract stock photos. Use generous whitespace to focus attention naturally.
3. **Component Library Brand Independence:**
   - Treat component libraries (e.g. shadcn/ui, Flowbite) as implementation building blocks, never as a default aesthetic.
   - Map library tokens (color, typography, corner radii, spacing) to the project's unique brand design tokens.
   - Ensure visual consistency across buttons, inputs, cards, dialogs, and tables. Strip out default decorative pulsing dots or noisy gradient gimmicks.

---

## 5. Accessibility & Universal Usability (WCAG 2.1 AA)

- **Color Contrast:** Ensure text achieves a minimum contrast ratio of 4.5:1 against its background (3:1 for large text 18pt+). Never convey critical status by color alone.
- **Keyboard Navigation & Focus:** Every interactive element must be reachable and operable via keyboard (`Tab`, `Shift+Tab`, `Enter`, `Space`). Never remove focus rings without providing an equally visible custom focus outline.
- **Semantic HTML & Motion:** Use native semantic elements. Honor `@media (prefers-reduced-motion: reduce)` by disabling non-essential transitions.

---

## 6. Expected Deliverables
1. **Polished UI Components:** Accessible, beautifully spaced, responsive interface designs free of decorative blinking artifacts.
2. **Dashboard & Workspace Layouts:** Structured multi-column dashboard compositions, scannable data widgets, and persistent or collapsible sidebars.
3. **High-Converting Landing Pages:** Editorial typography, clear CTA hierarchy, and product-led hero showcases.
4. **Responsive Navigation Specs:** Clean desktop layouts and mobile hamburger menu designs adapted to product architecture.
5. **Refined Website Copy:** Natural, human-sounding interface copy free of em dash crutches and promotional clichés.
6. **Design Specification:** Clear design tokens (typography, color, spacing) matching existing systems.
7. **Accessibility Sign-off:** Verification of keyboard navigation, screen reader labels, and contrast compliance.

---

## 7. Progressive Disclosure (Reference Documents)
Consult these bundled documents only when specific deep guidance is needed:

- **WCAG 2.1 AA accessibility guidelines:** Consult [accessibility-wcag.md](references/accessibility-wcag.md).
- **Visual design foundations and copy guidelines:** Consult [visual-design-principles.md](references/visual-design-principles.md).
- **Dashboard design principles and information architecture:** Consult [dashboard-design-principles.md](references/dashboard-design-principles.md).
- **Landing page design principles and visual storytelling:** Consult [landing-page-design-principles.md](references/landing-page-design-principles.md).
- **Component library design guidelines and visual consistency:** Consult [component-library-design-guidelines.md](references/component-library-design-guidelines.md).
- **Responsive navigation design patterns:** Consult [responsive-navigation-design.md](references/responsive-navigation-design.md).
- **Responsive navigation verification checklist:** Consult [responsive-navigation-checklist.md](checklists/responsive-navigation-checklist.md).
- **UI/UX inspection checklist:** Consult [ui-ux-review-checklist.md](checklists/ui-ux-review-checklist.md).
- **Design specification template:** Consult [design-spec-template.md](templates/design-spec-template.md).
