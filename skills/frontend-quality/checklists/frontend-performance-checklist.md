# Frontend Performance & Quality Checklist

- [ ] Do all images have explicit aspect ratios or width/height dimensions?
- [ ] Are heavy third-party packages dynamically imported?
- [ ] Are touch targets on mobile at least 44x44px?
- [ ] Is horizontal viewport scrolling eliminated on mobile devices (no `overflow-x` leak)?
- [ ] Are async loading states represented with accurately sized skeletons?
- [ ] Are error boundaries in place around external widgets or complex visualizations?
- [ ] Are inputs debounced or throttled where appropriate?
