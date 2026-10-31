# Reference: Core Web Vitals Optimization Guide

## Eliminating Layout Shifts (CLS)
- **Image Sizing:** Always set explicit `width` and `height` attributes on `<img>` tags, or use CSS `aspect-ratio: 16/9`.
- **Dynamic Content:** When fetching async data, render skeleton placeholders matching the exact final container dimensions.
- **Web Fonts:** Use `font-display: swap` or preload critical fonts to eliminate flash of invisible/unstyled text (FOIT/FOUT).

## Minimizing Interaction Latency (INP)
- Avoid expensive computations directly in click or input event handlers.
- Use `requestAnimationFrame` or `setTimeout(..., 0)` to allow the browser to paint before executing heavy calculations.
- Use virtualized lists (`react-virtual` or equivalent) when rendering datasets over 100 items.
