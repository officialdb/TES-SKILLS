# Reference: E-commerce Implementation, Component Architecture & Performance

This reference guides frontend engineers in implementing responsive, accessible, high-performance, and maintainable e-commerce web applications. The patterns address storefront discovery grids, category navigation, product detail pages (PDP), interactive galleries, variant selection, and Core Web Vitals optimization.

---

## 1. Responsive Implementation Architecture

E-commerce interfaces must adapt seamlessly from mobile viewports (320px–375px) to ultra-wide desktop monitors without layout shifts or horizontal overflow.

> [!NOTE]
> **Illustrative Implementation Values:**  
> All breakpoints (e.g., `640px`, `1024px`, `1280px`), CSS Grid column classes (`xl:grid-cols-5`, `grid-cols-2`), and sizing dimensions (`w-64`) in this document are **illustrative implementation examples**, not universal TES requirements. Responsive behavior must be validated against actual content, line lengths, typography scales, and available container widths.

### A. Responsive Grid Reflow Mechanics

Product grids should reflow dynamically based on container width to preserve image aspect ratios and typography readability across screen widths:

```html
<!-- Illustrative Responsive Product Grid Structure -->
<section aria-labelledby="new-arrivals-heading" class="w-full px-4 sm:px-6 lg:px-8 py-8">
  <div class="flex items-center justify-between mb-6">
    <h2 id="new-arrivals-heading" class="text-xl sm:text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
      New Arrivals
    </h2>
    <a href="/catalog/new" class="text-sm font-medium text-emerald-700 hover:text-emerald-800 dark:text-emerald-400">
      View All <span aria-hidden="true">&rarr;</span>
    </a>
  </div>

  <!-- Suggested reflow: 5 columns on desktop, 3 on tablet, 2 on mobile -->
  <div class="grid grid-cols-2 gap-3 sm:grid-cols-3 sm:gap-4 lg:grid-cols-4 xl:grid-cols-5 xl:gap-6">
    <!-- Reusable ProductCard Component Instances -->
  </div>
</section>
```

### B. Category Sidebar Adaptation
- **Desktop (1024px+):** Render the category sidebar as a persistent vertical column (`w-64`) paired with the main hero banner (`flex-1`) in a CSS Flexbox or Grid container.
- **Mobile & Tablet (<1024px):** Hide the persistent desktop sidebar (`hidden lg:block`). Mount an accessible toggle button that opens an off-canvas drawer (`Sheet` or dialog) with full keyboard trapping, or convert top categories into a horizontal scrollable chip bar.

### C. Promotional Editorial Banner Reflow
- **Desktop (1024px+):** 2-column grid (`grid-cols-2 gap-6`) presenting category highlights side-by-side with balanced image and text zones.
- **Mobile (<1024px):** Stack into a single vertical column (`grid-cols-1 gap-4`) to ensure promotional typography and discount badges do not overlap or truncate.

### D. Product Detail Page (PDP) Stacking
- **Desktop (1024px+):** Asymmetric 2-column layout (`grid grid-cols-1 lg:grid-cols-12 gap-12`). The media gallery occupies 6–7 columns, while the sticky purchasing column occupies 5–6 columns.
- **Mobile (<1024px):** Single-column stack. The product gallery sits at the top, followed immediately by title, price, configuration swatches, and primary conversion actions. Technical tabs and related recommendations render below.

### E. Responsive Specification Tables
Desktop 4-column tables (`Specification`, `Details`, `More Info`, `Remarks`) must not cause horizontal layout overflow on mobile screens:
- **Strategy 1 (Responsive Scroll):** Wrap the `<table>` in a container with `overflow-x: auto; -webkit-overflow-scrolling: touch;`. Ensure the first column (`Specification`) remains sticky or legible.
- **Strategy 2 (Adaptive Card Reflow):** On viewports below 640px, transform table rows into stacked definition lists (`<dl>`) or structured key-value cards using CSS media queries.

```css
/* Responsive Table to Definition List Transformation */
@media (max-width: 640px) {
  .responsive-spec-table thead {
    display: none;
  }
  .responsive-spec-table, 
  .responsive-spec-table tbody, 
  .responsive-spec-table tr, 
  .responsive-spec-table td {
    display: block;
    width: 100%;
  }
  .responsive-spec-table tr {
    margin-bottom: 1rem;
    border: 1px solid var(--border-color);
    border-radius: 0.5rem;
    padding: 0.75rem;
  }
  .responsive-spec-table td {
    display: flex;
    justify-content: space-between;
    padding: 0.375rem 0;
  }
  .responsive-spec-table td::before {
    content: attr(data-label);
    font-weight: 600;
    margin-right: 1rem;
  }
}
```

### F. Mobile Touch Target Usability
- Ensure every interactive control (variant swatches, quantity stepper `[-]` and `[+]`, thumbnail cards, and cart buttons) has a minimum touch target of 44x44px.
- Use CSS padding or invisible pseudo-elements (`::after`) to expand hit targets when visible icons are compact (e.g. 24x24px color chips).

---

## 2. Functional Interactions & State Management

Visually rendered controls must not be mistaken for functional implementations. Every interaction requires predictable state updates, validation, and accessible feedback.

### A. Product Image Gallery Synchronization

Selecting a thumbnail must update the active image reactively, managing loading states and alternative text:

```typescript
interface ProductImage {
  id: string;
  src: string;
  alt: string;
  width: number;
  height: number;
}

interface GalleryState {
  selectedIndex: number;
  isZoomed: boolean;
}

// React Example for Image Gallery State
function ProductGallery({ images }: { images: ProductImage[] }) {
  const [selectedIndex, setSelectedIndex] = React.useState(0);
  const activeImage = images[selectedIndex] || images[0];

  return (
    <div class="flex flex-col gap-4">
      <!-- Main Hero Display (Preserves aspect ratio to prevent CLS) -->
      <div class="relative aspect-square w-full overflow-hidden rounded-xl border border-slate-200 bg-white dark:border-slate-800">
        <img
          src={activeImage.src}
          alt={activeImage.alt}
          width={activeImage.width}
          height={activeImage.height}
          loading="eager"
          fetchpriority="high"
          class="h-full w-full object-contain p-6 transition-opacity duration-200"
        />
      </div>

      <!-- Thumbnail Strip -->
      <div role="tablist" aria-label="Product thumbnails" class="flex gap-3 overflow-x-auto pb-2">
        {images.map((img, idx) => {
          const isSelected = idx === selectedIndex;
          <!-- Visible above-the-fold thumbnails load normally; only off-screen/overflow thumbnails are lazy loaded -->
          const isInitiallyVisible = idx < 4;
          return (
            <button
              key={img.id}
              role="tab"
              aria-selected={isSelected}
              aria-label={`View image ${idx + 1}: ${img.alt}`}
              onClick={() => setSelectedIndex(idx)}
              class={`relative aspect-square h-16 w-16 flex-shrink-0 overflow-hidden rounded-lg border-2 bg-white p-1 transition-all ${
                isSelected ? 'border-blue-600 ring-2 ring-blue-600/30' : 'border-slate-200 hover:border-slate-400'
              }`}
            >
              <img
                src={img.src}
                alt=""
                class="h-full w-full object-contain"
                loading={isInitiallyVisible ? 'eager' : 'lazy'}
                decoding="async"
              />
            </button>
          );
        })}
      </div>
    </div>
  );
}
```

### B. Variant Selection (Color & Size)
- Variant chips must be implemented as semantic radio groups (`<input type="radio">` or buttons with `role="radio"` and `aria-checked`).
- Selecting a variant must synchronise:
  1. Selected SKU and variant name display.
  2. Main gallery image to match selected colorway.
  3. Inventory stock count and urgency messaging ("Only 10 items left").
  4. Dynamic price and discount calculations.

### C. Bounded Quantity Controls
Quantity steppers must enforce strict operational boundaries:
- **Minimum:** 1 (disable decrement control when value is 1).
- **Maximum:** Available inventory limit (disable increment control when stock limit is reached).
- **Input Sanitization:** Direct text entry must sanitize non-numeric input and clamp values to `[min, max]`.

```typescript
function QuantityStepper({
  quantity,
  maxStock,
  onChange,
}: {
  quantity: number;
  maxStock: number;
  onChange: (val: number) => void;
}) {
  const handleDecrement = () => onChange(Math.max(1, quantity - 1));
  const handleIncrement = () => onChange(Math.min(maxStock, quantity + 1));
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseInt(e.target.value, 10);
    if (!isNaN(val)) {
      onChange(Math.min(Math.max(1, val), maxStock));
    }
  };

  return (
    <div class="flex items-center gap-2">
      <div class="flex items-center rounded-lg border border-slate-300 bg-white dark:border-slate-700">
        <button
          type="button"
          aria-label="Decrease quantity"
          disabled={quantity <= 1}
          onClick={handleDecrement}
          class="h-10 w-10 text-lg font-medium text-slate-700 disabled:opacity-40 hover:bg-slate-100"
        >
          -
        </button>
        <input
          type="text"
          inputMode="numeric"
          pattern="[0-9]*"
          aria-label="Quantity"
          value={quantity}
          onChange={handleInputChange}
          class="h-10 w-12 text-center text-sm font-semibold text-slate-900 border-x border-slate-300"
        />
        <button
          type="button"
          aria-label="Increase quantity"
          disabled={quantity >= maxStock}
          onClick={handleIncrement}
          class="h-10 w-10 text-lg font-medium text-slate-700 disabled:opacity-40 hover:bg-slate-100"
        >
          +
        </button>
      </div>
      {maxStock <= 10 && (
        <span class="text-xs font-semibold text-amber-600 dark:text-amber-400" role="status">
          Only {maxStock} Items Left!
        </span>
      )}
    </div>
  );
}
```

### D. Conversion Actions & Mutation Lifecycle (Buy Now vs. Add to Cart)
Maintain clear separation between conversion flows:
- **Add to Cart (Asynchronous Mutation):**
  - **Mutation Lifecycle:** Every cart mutation must manage explicit states: `idle`, `pending`, `success`, and `error`.
  - **Optimistic Updates & Rollback:** When updating header badge counts or cart sidebars optimistically before network completion, save the previous state snapshot. If the server mutation fails (e.g. inventory depletion, session expiry, network timeout), **immediately roll back** the badge count and cart drawer to the previous snapshot, announce the failure to screen readers via an accessible live region (`role="alert"`), and display an actionable error message.
  - **Screen Reader Announcements:** Announce additions via `aria-live="polite"` (e.g., "Added 2 AirPods-Max to your cart").
- **Buy Now (Direct Checkout Funnel):**
  - Direct conversion action. Adds the configured SKU to the checkout session and initiates immediate route transition to the checkout funnel, preventing duplicate submissions through disabled loading states.
- **Scope Boundary:** These interactive patterns apply only when the project explicitly implements transactional cart or checkout flows. Do not introduce cart state management into informational product catalogs or read-only brochure sites.

### E. Accessible Tabbed Content
Product tabs (Description, Specifications, Reviews) must implement the WAI-ARIA tab pattern:
- The tablist container has `role="tablist"`.
- Each tab has `role="tab"`, `aria-selected="true|false"`, and `aria-controls="panel-id"`.
- Tab navigation supports horizontal arrow keys (`ArrowLeft`, `ArrowRight`) to cycle focus, with `Home` and `End` jumping to the start and end.
- Tab panels have `role="tabpanel"`, `aria-labelledby="tab-id"`, and `tabIndex={0}`.

### F. Global Search, Autocomplete & Race Condition Prevention
Where the project implements catalog search:
- **Debouncing:** Debounce input queries by 250ms–300ms before triggering API requests to prevent server flooding.
- **Race Condition Prevention:** Cancel stale in-flight requests using `AbortController` when new keystrokes occur, ensuring an earlier, slower network response cannot overwrite fresher results.
- **Keyboard Navigation:** Support `ArrowDown` to navigate into search results, `Escape` to close the dropdown, and `Enter` to submit.
- **Loading, Empty & Failure States:** Render explicit skeleton placeholders during query fetches, distinct failure alerts upon network errors, and helpful empty states ("No products found matching '...'") when queries return zero items.

### G. Newsletter Form Validation & State Machine
Where a newsletter subscription form is implemented:
- **State Machine:** Manage four distinct states: `idle`, `submitting` (disable submit button, display spinner), `success` (confirmation announcement), and `error` (actionable recovery message).
- **Validation:** Validate email syntax client-side using native HTML constraint validation (`type="email"` and `required`) plus a standard regex check.
- **Accessible Feedback:** Provide visible and audible status updates via `aria-live="polite"` or `role="status"` on successful subscription, and `role="alert"` on validation failures.

---

## 3. Accessibility Implementation Standards (WCAG 2.1 AA)

E-commerce sites are transactional engines; accessibility barriers directly cause lost revenue and legal exposure.

### A. Semantic Landmarks & Heading Architecture
- Wrap major storefront regions in native semantic landmarks: `<header>`, `<nav aria-label="Main">`, `<main>`, `<aside aria-label="Product Categories">`, `<section aria-labelledby="...">`, and `<footer>`.
- Enforce strict heading nesting:
  - Exactly one `<h1>` per page (the storefront hero headline or the PDP product title).
  - `<h2>` for major sections ("New Arrivals", "Featured Products", "Technical Specifications").
  - `<h3>` for individual product card titles in grids.
  - Never skip heading levels for visual styling.

### B. Accessible Names for Icon-Only Controls
Controls lacking visible text must provide programmatic accessible names via `aria-label`:
- Cart trigger: `<button aria-label="Shopping Cart, 3 items">`
- Wishlist trigger: `<button aria-label="Wishlist, 5 saved items">`
- Search trigger: `<button aria-label="Submit search query">`
- Thumbnail items: `<button aria-label="View product colorway Blue">`
- Quantity buttons: `<button aria-label="Increase item quantity">`

### C. Color Contrast & Indicator Redundancy
- **Text Contrast:** Ensure all body text, prices, and labels meet a minimum 4.5:1 contrast ratio against container backgrounds (3:1 for large text 18pt+).
- **Badge Contrast:** Green "New" badges and red discount badges (`-20%`) must achieve 4.5:1 text-to-background contrast.
- **Never Rely on Color Alone:** Color swatch selectors must pair visual color fills with visible tooltip labels or programmatic `aria-label="Color: Space Gray"`.

---

## 4. Performance & Core Web Vitals Optimization

E-commerce conversion rates fall rapidly as page load latency increases. Follow these concrete engineering practices to maintain good Core Web Vitals.

| Metric | Target | E-Commerce Strategy |
|---|---|---|
| **LCP** | < 2.5s | Preload hero banner and main PDP image with `fetchpriority="high"`, serve modern formats (AVIF/WebP) |
| **CLS** | < 0.1 | Explicit aspect ratio containers on all product cards (`aspect-square` or `aspect-[4/5]`) |
| **INP** | < 200ms | Debounce search inputs, defer heavy review widgets, avoid monolithic JavaScript bundles |

### A. Preventing Cumulative Layout Shift (CLS < 0.1)
- Never render raw `<img>` tags without fixed aspect-ratio containers or explicit `width` and `height` attributes.
- Use CSS aspect ratio utilities:

```html
<!-- Aspect ratio wrapper guarantees reserved layout space -->
<div class="relative w-full aspect-square bg-slate-100 overflow-hidden">
  <img
    src="/images/products/airpods-max-thumb.webp"
    alt="AirPods Max in Sky Blue"
    width="400"
    height="400"
    loading="lazy"
    decoding="async"
    class="w-full h-full object-contain"
  />
</div>
```

### B. Viewport-Driven Image Priority & Largest Contentful Paint (LCP < 2.5s)
Image loading strategy must be governed by actual viewport presence and LCP candidacy, rather than broad image categories:
- **LCP Candidate Eager Loading:** Identify the primary above-the-fold visual asset—the storefront hero banner on a homepage, or the main product photo on a PDP. Never lazy-load the primary LCP candidate. Render it eagerly with `<img loading="eager" fetchpriority="high" decoding="async">`.
- **Preloading Critical Imagery:** On product detail pages, preload the primary colorway image in the document `<head>` to minimize render delay:

```html
<!-- Preloading Main PDP Image in HTML Head -->
<link rel="preload" as="image" href="/images/products/airpods-max-blue-large.webp" type="image/webp" fetchpriority="high">
```

- **Visible Product Gallery Thumbnails:** Thumbnails positioned above the fold directly beneath or beside the hero image should **not** receive `loading="lazy"`. Applying lazy loading to initial visible thumbnails delays decoding and harms perceived responsiveness when users click to inspect alternative views. Use standard eager loading with `decoding="async"` for the first 3–4 visible thumbnails, reserving `loading="lazy"` strictly for off-screen or scrollable carousel overflow items.

### C. Lazy Loading Below-the-Fold Imagery
- Apply `loading="lazy"` and `decoding="async"` strictly to imagery positioned outside the initial viewport: below-the-fold product card grids, off-screen thumbnail carousels, editorial blog previews, and partner brand directories.
- Provide responsive image candidates using `<picture>` or `srcset` + `sizes` to prevent serving desktop-sized 1200px images to 375px mobile viewports.

---

## 5. Component Architecture & Maintainability

Build e-commerce interfaces from reusable, strongly typed presentational primitives decoupled from business and network logic.

```
+-------------------------------------------------------------+
| Presentation Layer (Stateless, Typed Primitives)            |
|  <ProductCard />    <ProductGallery />   <VariantSelector /> |
|  <QuantityStepper /> <SpecTable />       <TrustBadgeStrip /> |
+-------------------------------------------------------------+
                              |
+-------------------------------------------------------------+
| State & Business Logic Layer                                |
|  useCartStore()     useWishlist()        useVariantSync()   |
+-------------------------------------------------------------+
                              |
+-------------------------------------------------------------+
| Data Contracts & APIs                                       |
|  ProductDTO         VariantOption        InventoryRecord    |
+-------------------------------------------------------------+
```

### A. Standardized Component Boundaries
- **`<ProductCard />`:** Accepts a standardized `Product` object. Renders image container, freshness/discount badges, title, formatted price, star rating, and optional quick-add action.
- **`<ProductGallery />`:** Manages hero image display and thumbnail synchronization. Handles zoom or modal expansion without leaking state outside the gallery boundary.
- **`<VariantSelector />`:** Generic configuration component handling color chips, size buttons, or dropdown variants with uniform change handlers.
- **`<SpecTable />`:** Declarative table component accepting an array of `{ label, value, moreInfo?, remarks? }` objects, rendering desktop tables and mobile cards cleanly.

### B. Separation of Data and Presentation
Do not hardcode product data structures directly inside JSX or HTML templates. Define clean TypeScript interfaces that mirror backend or headless e-commerce API contracts:

```typescript
export interface ProductSummary {
  id: string;
  slug: string;
  title: string;
  descriptionSnippet: string;
  price: number;
  originalPrice?: number;
  currency: string;
  rating: number;
  reviewCount: number;
  badge?: {
    type: 'new' | 'discount';
    label: string;
  };
  featuredImageUrl: string;
  imageAlt: string;
}
```

This decoupling ensures components remain easily testable, reusable across storefront discovery sections and related product carousels, and independent of specific backend implementations.

