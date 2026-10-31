---
name: ui-ux-standards
description: Professional, restrained, accessible interface design with clear hierarchy, purposeful color, clean typography, and WCAG compliance. Trigger when designing web interfaces, creating UI components, styling layouts, reviewing UX flows, or ensuring accessibility.
compatibility:
  - hermes
  - opencode
  - codex
  - claude-code
  - gemini-cli
  - generic
---

# UI/UX Standards

## Purpose
`ui-ux-standards` guides coding agents in designing and implementing professional, clean, accessible, and delightful digital user interfaces. It emphasizes restraint, typography, whitespace, purposeful color, and accessibility over noisy decorative fads.

---

## 1. Design Philosophy: Restraint & Clarity

### What We Prioritize
1. **Clear Visual Hierarchy:** Primary actions, secondary actions, and informational content must be instantly distinguishable through size, weight, and position.
2. **Clean Typography:** Legible type scales with comfortable line heights (`leading-relaxed`), proper font tracking, and optical sizing.
3. **Purposeful Use of Color:** Neutral canvas with high-contrast, deliberate accent colors for focus, calls-to-action, and status feedback (success, warning, destructive).
4. **Functional Spacing & Rhythm:** Generous, consistent spacing system (4px / 8px grid). Spacing creates breathing room and communicates visual grouping.
5. **Universal Accessibility (WCAG 2.1 AA):** High contrast ratios (>= 4.5:1 for normal text, >= 3:1 for large text), visible focus rings, ARIA landmarks, and keyboard navigability.

### What to Avoid
- **No Electric / Neon Colors:** Avoid eye-straining fluorescent neons, intense saturated glows, and chaotic rainbow palettes.
- **No Gratuitous Gradients:** Avoid heavy multicolor background gradients that reduce readability and look dated.
- **No Excessive Cardification:** Do not wrap every single paragraph or metric in its own heavy, rounded border card. Use clean typography and spacing instead.
- **No Hyper-Rounded Containers:** Avoid bloated pill borders (`rounded-3xl` on everything) that waste screen real estate.
- **No Unnecessary Animations:** Motion should be subtle, quick (150ms-250ms), purposeful, and respect `prefers-reduced-motion`. Never delay user interaction with decorative entrance animations.

---

## 2. Standard Design System Foundations

### Typography Scales
- **Display / H1:** 32px–40px (Bold/SemiBold, tight tracking, line-height 1.1–1.2)
- **H2:** 24px–28px (SemiBold, line-height 1.25)
- **H3:** 18px–20px (Medium/SemiBold, line-height 1.3)
- **Body:** 14px–16px (Regular, line-height 1.5–1.6)
- **Caption / Meta:** 12px–13px (Regular/Medium, line-height 1.4, subtle muted color)

### Color Palette Strategy
- **Backgrounds:** Clean, neutral light canvas (`#FFFFFF`, `#F9FAFB`) with crisp borders (`#E5E7EB`). Dark mode surfaces should use subtle neutral zinc/slate rather than pure black.
- **Text:** High contrast primary text (`#111827`), secondary muted text (`#4B5563`).
- **Brand / Primary Accent:** One cohesive primary hue (e.g. deep navy, refined royal blue, forest green, warm charcoal) used deliberately.
- **Semantic Feedback:** Emerald for success, Amber for warning, Crimson for error, Sky for informational.

---

## 3. Deliverables & Outputs
1. **Accessible UI Components:** Accessible HTML/CSS/Tailwind implementations with semantic tags and keyboard support.
2. **Responsive Verification:** Layouts tested across mobile (375px), tablet (768px), and desktop (1280px+).
3. **Contrast & Accessibility Audit:** Color contrast ratios and ARIA annotations.
