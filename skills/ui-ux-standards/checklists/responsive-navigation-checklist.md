# Responsive Navigation Checklist

Use this checklist to verify responsive navigation behavior, mobile menu functionality, and accessibility:

- [ ] **Desktop Display:** Desktop navigation displays clean horizontal links with proper alignment and spacing.
- [ ] **Mobile Hamburger:** Mobile navigation replaces desktop links with a recognizable hamburger control at the appropriate breakpoint.
- [ ] **Menu Open:** Activating the hamburger button opens the navigation cleanly.
- [ ] **Menu Close:** Activating the close control or toggle closes the navigation.
- [ ] **Link Functionality:** All navigation links route to their correct destinations without errors.
- [ ] **Close on Selection:** Menu automatically closes after selecting a navigation link where appropriate (e.g., page navigation, section anchor jumps).
- [ ] **Escape Key Support:** Pressing the `Escape` key dismisses open overlay-style or modal navigation.
- [ ] **Keyboard Operability:** Complete navigation flow is reachable and operable via keyboard (`Tab`, `Shift+Tab`, `Enter`, `Space`).
- [ ] **ARIA States & Labels:** Hamburger button specifies semantic attributes (`aria-expanded`, `aria-controls`, and descriptive `aria-label`).
- [ ] **Touch Target Sizing:** Mobile touch targets are at least 44x44px for comfortable finger tapping.
- [ ] **Zero Horizontal Overflow:** Navigation layout introduces no horizontal scrolling (`overflow-x`) across any viewport.
- [ ] **Viewport Resilience:** Navigation remains usable and properly laid out across mobile (375px), tablet (768px), laptop (1024px), and desktop (1440px) sizes in both portrait and landscape modes.
- [ ] **Motion Preferences:** Animation transitions honor `@media (prefers-reduced-motion: reduce)`.
- [ ] **Implementation Cleanliness:** Navigation avoids unnecessary third-party dependencies and avoids duplicating desktop and mobile markup unnecessarily.

