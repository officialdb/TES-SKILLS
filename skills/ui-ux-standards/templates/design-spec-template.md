# Design Specification: [View / Component Name]

**Component:** [e.g. Navigation Header, Settings Form, Data Table]  
**Target Viewport:** Responsive (Mobile-first, 375px -> 1440px)  
**WCAG Target:** Level AA  

---

## 1. Visual Hierarchy & Content
- **Primary Element:** [What user sees first]
- **Primary Action (CTA):** [Button / Trigger]
- **Supporting Information:** [Labels, descriptions]

---

## 2. Design Tokens
- **Typography:**
  - Header: 24px, SemiBold, `#111827`
  - Body: 15px, Regular, leading 1.6, `#374151`
- **Colors:**
  - Surface: `#FFFFFF`
  - Border: `1px solid #E5E7EB`
  - Primary Accent: `#2563EB` (Blue 600)
  - Focus Ring: `2px solid #3B82F6` (Offset 2px)
- **Spacing:** `p-4 sm:p-6`, gap `gap-4`

---

## 3. Accessibility Notes
- Contrast Ratio: 7.2:1 (PASS)
- Keyboard Support: `Enter` submits, `Escape` dismisses
- Screen Reader: `aria-describedby` links to help text
