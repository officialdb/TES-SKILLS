# Frontend Performance & Quality Checklist

- [ ] Do all images have explicit aspect ratios or width/height dimensions?
- [ ] Are heavy third-party packages dynamically imported?
- [ ] Are CSS pulse and blink animations eliminated on decorative dots, tags, and title badges?
- [ ] Are status animations conditionally rendered only during active, dynamic state (e.g., connecting, streaming)?
- [ ] Are template strings and user-facing copy free of em dashes (—) and generic marketing buzzwords?
- [ ] Are touch targets on mobile at least 44x44px?
- [ ] Is horizontal viewport scrolling eliminated on mobile devices (no `overflow-x` leak)?
- [ ] Does mobile navigation use a semantic button with `aria-expanded`, `aria-controls`, and dynamic accessible labels?
- [ ] Does mobile navigation close cleanly on link selection and Escape key press, with body scroll locked while modal overlays are active?
- [ ] Are async loading states represented with accurately sized skeletons?
- [ ] Are error boundaries in place around external widgets or complex visualizations?
- [ ] Are inputs debounced or throttled where appropriate?
- [ ] Are component libraries evaluated using the 10-point selection criteria before introducing new UI dependencies?
- [ ] Do dashboard layouts collapse cleanly from multi-column grids to single column without horizontal overflow?
- [ ] Are above-the-fold hero mockups optimized for LCP with eager loading and explicit aspect ratios?
