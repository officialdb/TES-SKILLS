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
   - **No Decorative Animated Dots:** Prohibit decorative blinking, flashing, or pulsing dots beside headings, badges, hero sections, cards, or navigation. Animated dots used merely to appear "modern" create cognitive distraction and mimic alarms.
   - *Functional Indicator Exception:* Subtle pulsing or status dots are permissible only when communicating genuine live state (real-time connection, active streaming, background progress).

---

## 2. Website Copywriting & Presentation

1. **Avoid Em Dashes in Website Copy:**
   - Strong preference against using em dashes (`—`) across website content (headlines, section titles, subheadings, feature bullets, paragraphs, testimonials, CTAs, navigation, and metadata).
   - Rewrite sentences naturally using commas, full stops, colons, or clean phrasing. Do not mechanically swap em dashes with commas; restructure thoughts naturally.
   - *Examples:*
     - Avoid: "Build better systems — without the complexity." -> Prefer: "Build better systems without unnecessary complexity."
     - Avoid: "Everything your team needs — in one place." -> Prefer: "Everything your team needs in one place."
   - *Context Boundary:* Technical documentation, code syntax, and CLI flags are exempt when syntactically required.
2. **Authentic, Professional Tone:**
   - Write clearly and concisely without generic AI promotional jargon ("supercharge", "unleash", "cutting-edge").
   - Avoid exaggerated claims and unearned superlatives. Never fabricate testimonials, metrics, or capabilities. Adapt tone to the specific industry and user context.

---

## 3. Accessibility & Universal Usability (WCAG 2.1 AA)

- **Color Contrast:** Ensure text achieves a minimum contrast ratio of 4.5:1 against its background (3:1 for large text 18pt+). Never convey critical status by color alone.
- **Keyboard Navigation & Focus:** Every interactive element must be reachable and operable via keyboard (`Tab`, `Shift+Tab`, `Enter`, `Space`). Never remove focus rings without providing an equally visible custom focus outline.
- **Semantic HTML & Motion:** Use native semantic elements. Honor `@media (prefers-reduced-motion: reduce)` by disabling non-essential transitions.

---

## 4. Expected Deliverables
1. **Polished UI Components:** Accessible, beautifully spaced, responsive interface designs free of decorative blinking artifacts.
2. **Refined Website Copy:** Natural, human-sounding interface copy free of em dash crutches and promotional clichés.
3. **Design Specification:** Clear design tokens (typography, color, spacing) matching existing systems.
4. **Accessibility Sign-off:** Verification of keyboard navigation, screen reader labels, and contrast compliance.

---

## 5. Progressive Disclosure (Reference Documents)
Consult these bundled documents only when specific deep guidance is needed:

- **WCAG 2.1 AA accessibility guidelines:** Consult [accessibility-wcag.md](references/accessibility-wcag.md).
- **Visual design foundations and copy guidelines:** Consult [visual-design-principles.md](references/visual-design-principles.md).
- **UI/UX inspection checklist:** Consult [ui-ux-review-checklist.md](checklists/ui-ux-review-checklist.md).
- **Design specification template:** Consult [design-spec-template.md](templates/design-spec-template.md).
