# Reference: Visual Design Principles for Engineering Agents

## The Foundations of Professional UI

### 1. Typography as the Core Interface
Content is typography. Interfaces look polished when typography is disciplined:
- Set body text to 15px or 16px with line height of 1.5 to 1.6 (`leading-relaxed`).
- Keep maximum text line length between 60 and 75 characters (`max-w-prose` / ~65ch). Text that spans 1400px across a monitor is unreadable.
- Establish clean hierarchy using font weights (regular 400 for prose, medium 500 for interactive elements, semibold 600 for headings). Avoid stacking bold weights across nested headings.

### 2. Spacing and Alignment
- Align elements along a consistent baseline and grid.
- Related elements must sit closer together than unrelated elements (Gestalt Law of Proximity).
- Use multiples of 4px / 8px: 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px.

### 3. Purposeful Hierarchy & Visual Restraint
Every screen has one primary objective. Use scale and contrast to draw attention naturally to the primary action. Secondary actions should be muted or bordered.

#### The Ban on Decorative Animated Dots
Decorative animated dots (pulsing badges, blinking accents beside section titles, flashing hero elements) harm interface quality:
- **Cognitive Distraction:** The human visual cortex reflexively tracks peripheral motion. Blinking dots distract users from reading content and completing primary actions.
- **Alarm Mimicry:** Flashing or pulsing dots conventionally signal urgent errors or system alerts. Using them as decorative flair creates false urgency.
- **Amateurish Aesthetic:** Pulsing dots are a common visual gimmick used to make static websites appear artificially dynamic.
- **Prohibited Uses:**
  - Pulsing dots beside headings or section badges (e.g. `• FEATURES` with an animated dot).
  - Repeated blinking dots in navigation bars, hero headers, or footer tags.
  - Flashing dots in feature cards, pricing tables, or testimonial cards.
  - Decorative animated ellipsis or faux loading dots without background activity.
- **Functional Exceptions:** Animated status indicators are permitted solely when reflecting genuine dynamic system state:
  - Real-time connection status (WebSocket connecting, disconnected).
  - Genuine live activity (active audio/video broadcast, live screen sharing).
  - Ongoing background tasks or streaming responses.
  - Even for functional indicators, motion must be subtle (smooth fade rather than harsh flash) and must respect `@media (prefers-reduced-motion: reduce)`.

### 4. Website Copywriting & Typographic Cleanliness
Copy is an essential visual and cognitive component of interface design. High-quality websites communicate with clarity, precision, and authentic tone.

#### Eliminating Em Dash Crutches
The em dash (`—`) is frequently overused by automated generation systems as a substitute for thoughtful sentence structure. In website copy, excessive em dashes create fragmented, disjointed reading rhythms:
- **Avoid:** Using em dashes to append subordinate clauses or decorative taglines in headlines, hero banners, feature bullets, and marketing cards.
- **Prefer:** Construct cohesive sentences using prepositions, coordinating conjunctions, colons, or clean sentence splits.
- **Transformation Patterns:**
  - *Tagline pattern:* Avoid "Smart analytics — for fast-growing teams." -> Prefer "Smart analytics for fast-growing teams."
  - *Feature pattern:* Avoid "Instant deployments — without server configuration." -> Prefer "Instant deployments without server configuration."
  - *Clause pattern:* Avoid "Automate workflows — and save hours every week." -> Prefer "Automate workflows and save hours every week." or "Automate workflows to save hours every week."
  - *Specification pattern:* Avoid "Available in two editions — Cloud and Self-Hosted." -> Prefer "Available in two editions: Cloud and Self-Hosted."
- **Scope Distinction:** This rule applies to user-facing website and marketing copy. It does not restrict programming syntax, CLI flag conventions (`--flag`), mathematical ranges, or standard technical documentation where em dashes serve a precise grammatical function.

#### Professional Tone and Authentic Value
- Write clearly and concretely. Avoid empty promotional buzzwords ("supercharge", "unleash", "revolutionary", "all-in-one game-changer").
- Focus on user capability and specific outcomes rather than exaggerated self-praise.
- Keep headlines concise (typically under 8 words) and paragraphs focused (2–3 sentences max for marketing copy).
- Never fabricate customer quotes, user statistics, benchmark numbers, or unsupported claims.

### 5. Responsiveness by Default
Design fluidly and mobile-first:
- Test layouts across 375px (mobile), 768px (tablet), 1024px (laptop), and 1440px (desktop).
- Adapt navigation gracefully: present clean horizontal links on desktop and collapse to an accessible mobile hamburger menu at content-driven breakpoints.
- Never allow horizontal viewport overflow.
- Ensure touch targets are at least 44x44px on mobile viewports.

### 6. Context-Sensitive Design & Domain Adaptability
Every digital interface serves a specific user purpose. Visual design standards and layout density must adapt to the domain context rather than forcing a single template across all applications:
- **E-Commerce Storefronts:** High content density, prominent search, multi-tiered category navigation, clear promotional rhythms, and reassuring trust indicators. See [ecommerce-design-principles.md](ecommerce-design-principles.md).
- **Product Detail Pages (PDP):** Focused single-product presentation, clear buying decision hierarchy, accessible variant configuration, and technical specification tables. See [ecommerce-design-principles.md](ecommerce-design-principles.md).
- **SaaS Dashboards:** Analytical workspace cards, persistent sidebars, scannable data metrics, and live timers. See [dashboard-design-principles.md](dashboard-design-principles.md).
- **SaaS Landing Pages:** Centered editorial typography, single dominant primary CTA, and realistic product mockups. See [landing-page-design-principles.md](landing-page-design-principles.md).
- **Visual Consistency Over Imitation:** Reusable principles (spacing systems, typography scales, neutral container foundations, purposeful accent colors) are universal; brand-specific palettes (such as forest greens or electric blues) are product-specific expressions, never universal mandates.
