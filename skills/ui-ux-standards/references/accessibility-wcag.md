# Reference: WCAG 2.1 AA Accessibility Standards

## Key Requirements for Web Applications

### 1. Color Contrast
- Normal text (< 18pt or < 14pt bold): Minimum contrast ratio of **4.5:1** against the background.
- Large text (>= 18pt or >= 14pt bold): Minimum contrast ratio of **3.0:1**.
- UI components and graphical objects: Minimum contrast ratio of **3.0:1**.
- Never communicate information exclusively via color (e.g., provide an icon or text label alongside red/green indicators).

### 2. Keyboard Navigation
- Every interactive control (button, link, input, tab) must be focusable via `Tab`.
- Focus indicators must be prominent and visible (e.g. `focus-visible:ring-2 focus-visible:ring-blue-500`).
- No keyboard traps: users must always be able to tab away.

### 3. Semantic HTML & ARIA
- Use native HTML elements (`<button>`, `<a>`, `<dialog>`, `<nav>`, `<main>`) rather than `div` with click handlers.
- When creating custom components, supply proper ARIA attributes (`aria-expanded`, `aria-label`, `aria-controls`).
