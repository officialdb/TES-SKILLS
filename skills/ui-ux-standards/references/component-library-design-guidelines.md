# Reference: Component Library Design Guidelines & Visual Consistency

This reference establishes visual design guidelines for AI coding agents when adopting and styling frontend component libraries (such as **shadcn/ui**, **Flowbite**, **Radix UI**, or **Chakra UI**). It ensures that component libraries serve as efficient implementation building blocks without compromising unique brand identity, visual restraint, or design quality.

---

## 1. Libraries as Implementation Resources, Not Design Strategies

A component library provides accessible, tested interactive primitives (buttons, dialogs, dropdowns, menus, forms). It does not provide your product's visual identity:

- **Never Accept Default Library Themes Unconditionally:** Default palettes, default border radii, and generic typography scream "unmodified template." Every project must establish its own design tokens (color palette, typographic scale, border radius, spatial rhythm).
- **Customize Foundation Tokens:** Map the library's design variables (e.g., CSS variables, Tailwind configuration, theme objects) to your project's specific design tokens.
- **Maintain Design Restraint:** Do not adopt animated gimmicks, harsh gradients, or neon badges simply because a component library demo showcases them.

---

## 2. Maintaining Visual Consistency Across Components

When assembling an interface from library components, enforce unified design rules across all elements:

### A. Button Hierarchy & Surface Styling
- **Primary Actions:** Exactly one primary button variant per view or major container (e.g., solid brand color fill).
- **Secondary Actions:** Muted outline or soft neutral background with crisp text contrast.
- **Ghost & Text Actions:** Borderless controls reserved for inline utilities, dismiss buttons, or secondary navigation links.
- **Corner Radii Consistency:** Ensure all buttons, input fields, cards, and dialogs share the exact same corner radius token (e.g., all `rounded-md` / 6px, or all `rounded-lg` / 8px). Mixing pill buttons with sharp rectangular cards creates visual discord.

### B. Form Controls & Interactive States
- **Consistent Height & Padding:** Inputs, selects, and buttons should share matching optical heights (e.g. `h-10` / 40px for default desktop controls, `h-9` / 36px for dense dashboard tables).
- **Clear Focus Outlines:** Standardize `:focus-visible` ring colors and offsets across all inputs and buttons. Never eliminate focus rings without a visible custom outline.
- **Label & Error Rhythm:** Position form labels consistently above inputs with distinct supporting help text and accessible error message slots.

### C. Overlays, Dialogs, and Menus
- **Consistent Backdrop Treatment:** Standardize modal overlays across the entire application (e.g., `bg-black/50 backdrop-blur-sm`).
- **Elevation Discipline:** Avoid stacking excessive drop shadows. Reserve subtle shadows (`shadow-sm`, `shadow-md`) for floating popovers, dropdown menus, and dialogs. Static cards on page canvases should rely on 1px borders rather than elevation shadows.

---

## 3. Preserving Design Standards within Library Primitives

Even when using off-the-shelf component libraries, strict TES standards apply:

1. **No Decorative Animated Dots:**
   - Many component libraries feature badges or pills with pulsing `@keyframes` dots. Strip out decorative pulse/ping animations.
   - Status indicators must remain static unless actively communicating live, dynamic system state (such as real-time audio broadcasting or active WebSocket synchronization).
2. **Natural Website Copywriting:**
   - Audit all library template strings, placeholders, and tooltips to eliminate em dashes (`—`).
   - Rewrite copy using natural sentence structure and commas.
3. **Contrast Compliance (WCAG 2.1 AA):**
   - Verify that custom color overrides maintain minimum contrast ratios: 4.5:1 for body text, 3:1 for large text and interactive component borders.

---

## 4. Composing Bespoke Widgets from Library Primitives

Rather than searching for an overly specialized third-party widget, assemble bespoke, polished widgets from basic library building blocks:

- **Dashboard Card Widget:**
  ```text
  <Card>
    <CardHeader>
      <CardTitle />
      <Button variant="ghost" size="sm">Details</Button>
    </CardHeader>
    <CardContent>
      [Custom Chart / Metric / Status List]
    </CardContent>
  </Card>
  ```
- **Compound User Spotlight:** Combine `Avatar`, `Badge`, `Tabs`, and `Button` primitives into a unified, high-density dashboard card matching the layout observed in Reference A.
- **Hero CTA Cluster:** Pair a primary `Button` with an outline `Button` with leading `Icon` matching the hierarchy in Reference B.
