# Reference: Responsive Navigation Implementation & Accessibility

## 1. Functional Architecture & State Management

Responsive navigation requires coordinating interactive toggle state, viewport transitions, and background layout behavior without introducing race conditions or memory leaks.

### State Predictability & Lifecycle
- **Single Source of Truth:** Manage mobile menu open/closed state through a simple boolean (`isOpen`) in the parent header or navigation component.
- **Route Change Closure:** Ensure mobile navigation automatically closes when a navigation link is clicked (crucial in Single Page Applications and on in-page anchor jumps).
- **Viewport Resize Sync:** Listen for viewport resize events (or leverage CSS media queries with `hidden md:flex`) to ensure an open mobile drawer does not remain visible or trapped when the user expands the viewport past the mobile breakpoint.
- **Body Scroll Locking:** When rendering a modal-style overlay or full-screen drawer, prevent the underlying page from scrolling by applying `overflow: hidden` to `document.body`. Always restore original body overflow styles when the menu closes or unmounts.

```typescript
// Example: React/Next.js scroll-lock hook pattern
useEffect(() => {
  if (!isOpen) return;
  const originalOverflow = document.body.style.overflow;
  document.body.style.overflow = "hidden";
  return () => {
    document.body.style.overflow = originalOverflow;
  };
}, [isOpen]);
```

---

## 2. Accessible Semantic Markup & ARIA Standards

Mobile navigation must be operable for screen readers, keyboard-only users, and touch interfaces alike.

### Hamburger Toggle Button
- **Semantic Element:** Always use a native `<button type="button">`, never a clickable `<div>` or `<span>`.
- **Accessible Naming:** Provide dynamic accessible labels via `aria-label`:
  - When closed: `aria-label="Open navigation menu"`
  - When open: `aria-label="Close navigation menu"`
- **State Communication:** Bind `aria-expanded={isOpen ? "true" : "false"}` dynamically.
- **Target Association:** Associate the toggle with the navigation container via `aria-controls="mobile-navigation-menu"`.

### Keyboard Navigation & Focus Trapping
- **Keyboard Operability:** Ensure the toggle button and all navigation links can be activated via `Enter` and `Space`.
- **Escape Key Dismissal:** Add a keydown listener for `Escape` to close the open menu and restore focus directly to the hamburger button:

```typescript
useEffect(() => {
  if (!isOpen) return;
  const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === "Escape") {
      setIsOpen(false);
      toggleButtonRef.current?.focus();
    }
  };
  window.addEventListener("keydown", handleKeyDown);
  return () => window.removeEventListener("keydown", handleKeyDown);
}, [isOpen]);
```

- **Focus Containment (Modal Style):** When using modal overlay navigation, keep tab navigation contained within the drawer while open, or ensure the drawer appears immediately after the toggle in DOM order.
- **Focus Rings:** Ensure all interactive elements display prominent focus rings using `:focus-visible` (e.g., `focus-visible:ring-2 focus-visible:ring-primary-500`).

---

## 3. Engineering Quality & Avoiding Bloat

### Single Source of Navigation Items
Do not duplicate link titles, URLs, and permissions across separate desktop and mobile JSX templates. Maintain a unified data configuration:

```typescript
export interface NavItem {
  label: string;
  href: string;
  isExternal?: boolean;
}

export const MAIN_NAV_ITEMS: NavItem[] = [
  { label: "Features", href: "/features" },
  { label: "Pricing", href: "/pricing" },
  { label: "Docs", href: "/docs" },
  { label: "About", href: "/about" },
];
```

Render both desktop horizontal lists and mobile drawer links from this common configuration.

### Eliminating Bloat & Third-Party Dependencies
- Use the project's existing framework primitives (e.g. React hooks, Vue refs, Svelte stores) and CSS utilities rather than introducing heavy third-party menu packages.
- Reuse the application's existing icon library (Lucide, Heroicons, Radix, or inline SVG) for the hamburger (three horizontal lines) and close (X) glyphs.
- Avoid duplicate DOM rendering where CSS media queries (`hidden md:flex`) suffice.

---

## 4. Performance & Layout Stability

- **Zero Layout Shifts (CLS < 0.1):** Place the mobile navigation container in a fixed or absolute overlay position so opening and closing never pushes down or shifts the document body.
- **Horizontal Overflow Prevention:** Ensure drawer transform animations (`translateX`) operate inside an element with `overflow-x: clip` or `overflow-x: hidden` to prevent transient horizontal scrollbars on mobile browsers.
- **Motion Restraint:** Restrict drawer transitions to standard CSS `transform` and `opacity` properties. Prohibit decorative pulsing or blinking `@keyframes`.
- **Reduced Motion:** Always wrap animated drawer slides within `@media (prefers-reduced-motion: no-preference)` or provide an instantaneous toggle fallback when reduced motion is requested.

