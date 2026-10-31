# Reference: Landing Page Implementation & Performance Architecture

This reference guides frontend engineers in implementing high-performance, responsive, and visually engaging SaaS landing pages. The implementation patterns are derived from real-world product-led landing pages (exemplified by Reference B: Minimalist Finance SaaS Landing Page "Zubaz").

---

## 1. Centered Hero Section Architecture

### A. Fluid Typography & Measure Constraints
Implement hero headlines and descriptions that scale smoothly between mobile and desktop viewports without abrupt layout jumps:

```html
<section class="relative overflow-x-clip bg-white px-6 pt-16 pb-24 dark:bg-slate-950">
  <div class="mx-auto max-w-5xl text-center">
    <!-- Editorial Headline with CSS clamp -->
    <h1 class="font-serif text-4xl sm:text-5xl md:text-6xl tracking-tight text-slate-900 dark:text-white leading-[1.15]">
      Manage your money better than ever
    </h1>

    <!-- Constrained Measure Supporting Description -->
    <p class="mx-auto mt-6 max-w-2xl text-base sm:text-lg text-slate-600 dark:text-slate-400 leading-relaxed">
      Our finance app is designed to help individuals and businesses manage their financial activities and transactions with complete clarity.
    </p>

    <!-- Responsive CTA Action Cluster -->
    <div class="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
      <a href="#trial" class="w-full sm:w-auto inline-flex items-center justify-center rounded-md bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 transition-colors">
        Start Your Free Trial
      </a>
      <button type="button" class="w-full sm:w-auto inline-flex items-center justify-center rounded-md border border-slate-300 bg-white px-6 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 transition-colors">
        <svg aria-hidden="true" class="mr-2 h-4 w-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
          <path d="M6.3 2.841A1.5 1.5 0 004 4.11v11.78a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/>
        </svg>
        Watch A Demo
      </button>
    </div>
  </div>
</section>
```

---

## 2. Product-Led Showcase & Floating Card Implementation

### A. Preventing Horizontal Scrollbar Leaks (`overflow-x: clip`)
Tilted floating cards and offset illustration doodles can easily extend beyond viewport boundaries on mobile screens:
- Apply `overflow-x: clip` or `overflow-x: hidden` to the outermost container section.
- Wrap floating cards in responsive breakpoints (hide or nest them beneath the mockup on narrow screens `<640px`).

### B. Responsive Product Mockup Container
To achieve perfect Cumulative Layout Shift (CLS < 0.1), reserve the exact space for the device mockup before images load:

```html
<div class="relative mx-auto mt-12 max-w-xs sm:max-w-sm md:max-w-md">
  <!-- Centered Smartphone Mockup -->
  <div class="aspect-[9/19] w-full overflow-hidden rounded-[2.5rem] border-[6px] border-slate-900 bg-slate-950 shadow-2xl">
    <img 
      src="/mockup-screen.webp" 
      alt="Zubaz mobile application balance interface"
      width="390" 
      height="844"
      loading="eager"
      fetchpriority="high"
      class="h-full w-full object-cover"
    />
  </div>

  <!-- Floating Outcome Badge (Left) -->
  <div class="hidden sm:flex absolute -left-12 top-1/4 items-center gap-2 rounded-full border border-green-300 bg-green-50 px-4 py-2 shadow-sm dark:border-green-800 dark:bg-green-950/80">
    <span class="flex h-2 w-2 rounded-full bg-green-500" aria-hidden="true"></span>
    <span class="text-xs font-semibold text-green-800 dark:text-green-300">$5,000 collected</span>
  </div>

  <!-- Tilted Photo Validation Card (Right) -->
  <div class="hidden sm:block absolute -right-16 bottom-12 rotate-6 rounded-xl border-2 border-slate-900 bg-white p-2 shadow-lg dark:bg-slate-900">
    <img 
      src="/customer-portrait.webp" 
      alt="Customer using mobile application" 
      width="120" 
      height="140" 
      loading="lazy"
      class="h-28 w-24 rounded-lg object-cover"
    />
  </div>
</div>
```

---

## 3. Optimizing Core Web Vitals on Landing Pages

1. **Largest Contentful Paint (LCP < 2.5s):**
   - The hero product mockup is typically the LCP element. Use `loading="eager"` and `fetchpriority="high"`.
   - Serve modern formats (WebP or AVIF) with appropriate `srcset` for standard and retina displays.
   - Preload hero webfonts (especially custom serif fonts) via `<link rel="preload" as="font" crossorigin>`.
2. **Cumulative Layout Shift (CLS < 0.1):**
   - Always declare explicit `width` and `height` or `aspect-ratio` on hero mockups and floating cards.
3. **Interaction to Next Paint (INP < 200ms):**
   - Keep hero interactive scripts (e.g. video modal launchers, mobile menu toggles) lightweight and unbundled from heavy application logic.
