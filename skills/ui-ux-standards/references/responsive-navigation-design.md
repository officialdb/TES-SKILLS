# Reference: Responsive Navigation Design

## 1. Foundations of Responsive Navigation

Navigation must adapt gracefully across viewports while preserving access to core user journeys. A layout that works on a 1440px desktop monitor will overflow or break on a 375px mobile device without intentional responsive adaptation.

### Desktop Navigation Standards
- **Clean Horizontal Layout:** Present primary destination links horizontally with consistent spacing (typically 24px to 32px gap).
- **Visual Hierarchy & Alignment:** Position branding (logo) on the left, primary navigation links in the center or left-aligned, and primary action buttons (sign in, get started CTA) on the far right.
- **Overcrowding Prevention:** Limit primary desktop navigation to 5–7 top-level links. Move secondary utility links, legal policies, and documentation into submenus, headers, or footers to preserve clean breathing room.
- **Predictable Hover & Focus States:** Highlight interactive links with subtle background fills, text color shifts, or clean bottom underlines with visible focus rings.

---

## 2. Mobile Navigation & The Hamburger Pattern

When the horizontal space becomes insufficient, replace desktop navigation links with an accessible mobile hamburger control.

### Hamburger Menu Button
- **Recognizable Iconography:** Use a standard three-line hamburger icon or an equivalent widely recognized menu glyph.
- **Generous Touch Target:** Ensure the tap area is at least 44x44px to accommodate touch input comfortably, even if the visible icon is smaller (e.g., 24x24px).
- **Clear Toggle & Close Control:** Provide an unmistakable close control when open, such as transforming into an "X" close icon or displaying an explicit close button with clear visual feedback.

### Reveal Layout & Spacing
- **Readable Typography:** Render mobile links with comfortable vertical rhythm (16px to 18px font size with 16px to 20px vertical padding per tap target).
- **Thumb-Friendly Interaction:** Arrange high-priority links within natural reach of mobile thumb zones. Avoid cramming interactive items tightly against screen edges.
- **Content Occlusion Control:** Prevent open navigation from unintentionally trapping scroll or obscuring critical alerts without user consent.
- **Consistent Visual Identity:** Match typography, background elevation, borders, and brand accents to the overall site design system.

---

## 3. Responsive Breakpoints & Device Orientation

### Content-Driven Breakpoints
Do not impose arbitrary fixed pixel breakpoints without evaluating actual content:
- Determine the collapse breakpoint where desktop links, branding, and CTA buttons begin crowding or wrapping onto multiple lines.
- For compact navigation bars with 3 links, desktop layouts may remain intact down to 640px.
- For expansive navigation bars with 7 links and search bars, collapsing at 1024px or 860px prevents awkward wrapping.

### Orientation Resilience
- **Portrait & Landscape Mobile:** Ensure the mobile menu remains scrollable vertically when opened in landscape orientation on short screens (e.g., height < 500px).
- **Zero Horizontal Overflow:** Ensure neither desktop nor mobile navigation causes horizontal page scrolling (`overflow-x` leaks).

---

## 4. Navigation Archetypes

Select the navigation archetype that best matches the application's structure and depth:

| Archetype | Best Suited For | Characteristics |
|---|---|---|
| **Dropdown Navigation** | Marketing sites with 3–5 pages | Drops down directly beneath the header bar; occupies partial screen height. |
| **Slide-In Drawer** | Web apps, dashboards, SaaS tools | Slides in smoothly from the right or left with a dimmed backdrop overlay. |
| **Full-Screen Overlay** | Portfolios, brand experiences, editorial sites | Covers the full viewport with bold typography and prominent spacing. |
| **Expandable Accordion** | Documentation, multi-level catalogues | Allows parent categories to expand and collapse secondary sub-links inline. |

Select the pattern that supports user tasks cleanly rather than forcing a single approach onto every project.

---

## 5. Visual Polish & Motion Restraint

- **Subtle Transitions:** Use gentle slide or fade transitions lasting 150ms to 250ms with standard easing (`ease-out`).
- **No Decorative Animated Dots:** Prohibit pulsing or flashing dots on menu buttons, navigation links, or mobile badges.
- **Natural Copywriting:** Keep navigation link labels concise, descriptive, and free of em dashes or unnecessary punctuation.
- **Reduced Motion:** Always disable sliding and fading transitions when `@media (prefers-reduced-motion: reduce)` is active.

