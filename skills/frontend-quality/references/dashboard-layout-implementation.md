# Reference: Dashboard Layout Implementation & Data Widget Architecture

This reference guides frontend engineers in implementing high-performance, accessible, and responsive dashboard applications. The patterns are derived from real-world multi-column dashboard architectures (exemplified by Reference A: HR Management Dashboard "Githr").

---

## 1. Multi-Column Dashboard Layout Architecture

### A. Shell Structure (Sidebar + Workspace Header + Content)
Structure dashboard shells using CSS Grid or Flexbox to ensure the sidebar remains fixed or collapsible while the workspace content scrolls independently:

```html
<div class="flex min-h-screen bg-slate-50 dark:bg-slate-950">
  <!-- Desktop Persistent Sidebar -->
  <aside class="hidden lg:flex lg:w-64 flex-col border-r border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
    <!-- Brand Identity (Top) -->
    <!-- Primary & Secondary Navigation -->
    <!-- User Profile Card (Bottom) -->
  </aside>

  <!-- Main Workspace -->
  <div class="flex flex-1 flex-col min-w-0">
    <!-- Top Workspace Header (Greeting, Search, Actions) -->
    <header class="sticky top-0 z-10 flex h-16 items-center justify-between border-b border-slate-200 bg-white/80 px-6 backdrop-blur dark:border-slate-800 dark:bg-slate-900/80">
      <!-- Header content -->
    </header>

    <!-- Scrollable Workspace Canvas -->
    <main class="flex-1 p-6">
      <!-- Multi-Column Widget Grid -->
      <div class="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">
        <!-- Dashboard Widgets -->
      </div>
    </main>
  </div>
</div>
```

---

## 2. Responsive Grid Collapse & Sidebar Mechanics

### A. Responsive Grid Reflow
- **Desktop (1280px+):** 3 equal columns (`xl:grid-cols-3 gap-6`). Complex widgets (such as wide charts or project tables) can span two columns (`xl:col-span-2`).
- **Tablet (768px–1279px):** 2 columns (`md:grid-cols-2 gap-6`).
- **Mobile (<768px):** 1 column (`grid-cols-1 gap-4`). High-urgency action widgets (active timers, notifications) stack at the top.

### B. Sidebar Transformation on Mobile
On mobile viewports, the desktop `<aside>` is hidden (`hidden lg:flex`). A semantic hamburger `<button>` in the top header triggers an accessible off-canvas drawer (such as a shadcn/ui `Sheet` or Flowbite drawer):
- Prevent background body scrolling (`overflow: hidden` on document body) while the drawer is open.
- Handle `Escape` key dismissal and restore focus to the hamburger button upon closing.

---

## 3. Data Widget Component Implementation

### A. Circular Progress Ring (Accessible SVG)
Render circular progress indicators using SVG with `stroke-dasharray` and `stroke-dashoffset`. Never use heavy animation libraries for static or periodic progress updates:

```tsx
interface ProgressRingProps {
  percentage: number;
  size?: number;
  strokeWidth?: number;
}

export function ProgressRing({ percentage, size = 80, strokeWidth = 8 }: ProgressRingProps) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <div 
      role="progressbar" 
      aria-valuenow={percentage} 
      aria-valuemin={0} 
      aria-valuemax={100}
      aria-label="Course completion progress"
      class="relative inline-flex items-center justify-center"
      style={{ width: size, height: size }}
    >
      <svg width={size} height={size} class="rotate-[-90deg]">
        <!-- Background Track -->
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="currentColor"
          strokeWidth={strokeWidth}
          fill="transparent"
          class="text-slate-200 dark:text-slate-800"
        />
        <!-- Progress Fill -->
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="currentColor"
          strokeWidth={strokeWidth}
          fill="transparent"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          class="text-purple-600 transition-[stroke-dashoffset] duration-500 ease-out"
        />
      </svg>
      <span class="absolute text-sm font-semibold text-slate-900 dark:text-white">
        {percentage}%
      </span>
    </div>
  );
}
```

### B. Accessible Bar Charts
- Use semantic SVG or charting libraries (e.g. Recharts, Tremor) that output clean SVG elements.
- Ensure the chart container provides an accessible text description:
  ```html
  <figure role="figure" aria-label="Quarterly Training Analysis Chart">
    <svg role="img" aria-label="Bar chart showing 12 courses completed across 8 weeks">
      <!-- Bars with keyboard accessible tooltips -->
    </svg>
    <figcaption class="sr-only">Detailed course completion breakdown by week...</figcaption>
  </figure>
  ```

### C. Digital Timer Widget & Interval Hygiene
Timers must run reliably without leaking intervals or freezing the main thread:
- **Clean Intervals:** Always clear `setInterval` on component unmount.
- **Screen Reader Politeness:** Do not trigger screen reader announcements on every single second tick. Use `aria-live="polite"` only on state changes (e.g. "Timer started", "Timer paused").

```tsx
useEffect(() => {
  if (!isRunning) return;
  const timer = setInterval(() => {
    setSeconds((prev) => prev + 1);
  }, 1000);
  return () => clearInterval(timer);
}, [isRunning]);
```

---

## 4. Performance & Layout Stability (Core Web Vitals)

- **Eliminating Cumulative Layout Shift (CLS < 0.1):** Set explicit `min-height` or skeleton placeholders matching widget card dimensions while async dashboard data is loading.
- **Independent Error Boundaries:** Wrap each dashboard widget in an isolated React/Vue Error Boundary. If the third-party analytics API fails, the Time Tracker and Status Tracker must continue functioning.
