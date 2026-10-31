# Reference: Frontend Component Library Selection & Integration

This reference provides AI coding agents with a structured methodology for evaluating, selecting, integrating, and customizing frontend component libraries.

---

## 1. The 10-Point Library Selection Checklist

Before selecting or installing any frontend UI library, evaluate these 10 criteria against the project:

1. **Existing Framework & Dependencies:** Inspect `package.json` to identify the framework (React, Next.js, Vue, Nuxt, Svelte, Angular, Astro) and current version.
2. **Current Styling Approach:** Determine whether the project uses Tailwind CSS, CSS Modules, Styled Components, Emotion, Sass, or vanilla CSS.
3. **Existing Installed Libraries:** Check whether a component library is already present in `package.json` (e.g. Radix, Headless UI, shadcn components in `components/ui`). Always prefer extending existing infrastructure over introducing competing libraries.
4. **Framework & Version Compatibility:** Confirm the library explicitly supports the installed framework version (e.g., React Server Components, Next.js App Router, Vue 3 Composition API).
5. **Accessibility & Keyboard Navigation (WCAG 2.1 AA):** Ensure primitives include keyboard interaction (`Tab`, `Enter`, `Space`, `Escape`, arrow keys), focus trapping, and dynamic ARIA state management (`aria-expanded`, `aria-controls`, `aria-selected`).
6. **Customization Flexibility:** Favor headless or copy-paste architectures (like Radix UI or shadcn/ui) that grant full control over markup and styling over monolithic libraries with hard-coded styles.
7. **Bundle Size & Runtime Overhead:** Evaluate runtime footprint. Prefer zero-runtime, tree-shakeable libraries (Tailwind-based, headless) over heavy runtime CSS-in-JS libraries that degrade Interaction to Next Paint (INP).
8. **Maintenance Status & Documentation:** Choose actively maintained libraries with official TypeScript typings, comprehensive API documentation, and active community adoption.
9. **Licensing & Project Constraints:** Verify permissive open-source licenses (MIT, Apache-2.0, BSD) that comply with commercial requirements.
10. **Single Library Principle:** Avoid installing multiple overlapping component libraries (e.g. mixing MUI with Mantine and Chakra UI). One robust foundation is sufficient.

---

## 2. In-Depth Component Ecosystems

### A. shadcn/ui
- **Architecture:** Copy-paste component model built on top of **Radix UI** headless primitives and styled with **Tailwind CSS**. Components live directly inside your project (typically `src/components/ui/` or `components/ui/`), giving you 100% ownership of source code.
- **Theme & Token Integration:** Configured via CSS variables in `globals.css` (mapping `--background`, `--foreground`, `--primary`, `--muted`, `--radius`) and integrated into `tailwind.config.js`.
- **Selective Installation:** Never mass-install the entire catalogue. Install only the specific components required for the task:
  ```bash
  npx shadcn@latest add button card tabs dialog
  ```
- **Customization Pattern:** Modify the generated component files directly to match project typography, paddings, and unique states without breaking updates.

### B. Flowbite
- **Architecture:** Open-source UI ecosystem built directly upon **Tailwind CSS**. Provides accessible interactive UI components for rapid application and dashboard development.
- **Core Primitives:** Excels at dashboard layouts, sidebars, navigation bars, dropdowns, tables, and modal dialogs.
- **Integration Modes:**
  - *Tailwind Plugin:* Configured in `tailwind.config.js` via `plugins: [require('flowbite/plugin')]`.
  - *Framework Wrappers:* Available as `flowbite-react` or `flowbite-vue` with typed component interfaces.
- **Customization Pattern:** Override Tailwind theme colors and classes via Tailwind config extensions rather than editing compiled node_modules.

### C. Other Major Component Ecosystems
- **Radix UI:** Unstyled, accessible headless primitives for React. Ideal foundation when building a bespoke, high-end design system from scratch.
- **Headless UI:** Official unstyled, accessible UI components from the Tailwind team, perfectly integrated with Tailwind transitions.
- **DaisyUI:** Pure Tailwind CSS component class library (no JavaScript runtime). Highly lightweight, customizable via CSS themes.
- **Material UI (MUI):** Comprehensive React component suite following Google's Material Design. Includes powerful enterprise data tables (`@mui/x-data-grid`). Uses runtime emotion styling; monitor bundle size and INP impact.
- **Ant Design / Chakra UI:** Comprehensive enterprise design systems with extensive pre-built forms and tables.

---

## 3. Decision Framework: Existing vs. Custom Components

Follow this decision tree when adding UI components:

```text
Do we need a standard interactive primitive (Dialog, Dropdown, Tabs, Button, Select)?
├── YES: Does an installed or approved library provide this primitive?
│   ├── YES: Reuse the existing component.
│   │   └── Does it require visual or behavior tweaks?
│   │       ├── YES: Customize via props, variant classes, or token overrides.
│   │       └── NO:  Use directly.
│   └── NO:  Install the headless/accessible primitive (e.g. npx shadcn add dropdown-menu).
└── NO:  Is the component unique to the business domain (e.g. TimeTracker, EmployeeSpotlight)?
    ├── Compose multiple basic library primitives (Card + Avatar + Badge + Button).
    └── Build custom only when interaction logic is genuinely bespoke.
```

### Golden Rules:
- **Never Rebuild Complex Primitives:** Do not hand-code custom modal dialogs, accessible selects, comboboxes, or popovers with plain `<div>` tags. You will inevitably introduce keyboard traps, broken focus management, and missing ARIA attributes.
- **Never Add Dependencies for Trivial Elements:** Do not install an npm package for a simple divider, badge, or card container that can be built in 5 lines of semantic HTML and CSS.

---

## 4. Documentation & API Verification Rules

When implementing library components:
1. **Consult Official Docs:** Verify component names, prop interfaces, and slot patterns against the installed library version.
2. **Never Hallucinate APIs:** Do not invent non-existent props (e.g., `<Button iconRight="chevron" />` when the library uses children composition `<Button><span>Text</span><ChevronIcon /></Button>`).
3. **Verify Interactive Behavior:** Ensure keyboard navigation (`Tab`, `Enter`, `Escape`), focus rings, and screen-reader announcements work correctly in the rendered DOM.
