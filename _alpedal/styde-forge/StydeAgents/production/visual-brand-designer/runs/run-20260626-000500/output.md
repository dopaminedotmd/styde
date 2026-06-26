# Ledgr — Brand Style Guide

**Version:** 1.0 | **Date:** June 2026 | **Sector:** Fintech SaaS — Expense & Financial Operations

---

## 1. Brand Core

**Name:** Ledgr  
**Tagline:** *Money moves smarter.*  
**Archetype:** The Steward × The Innovator  
**Promise:** Ledgr gives finance teams real-time clarity and control — replacing spreadsheets and guesswork with a single, intelligent command center.

| Trait | Expression |
|---|---|
| **Trustworthy** | Steady, never flashy. Precision inspires confidence. |
| **Modern** | Clean, forward-leaning. Fintech, not legacy banking. |
| **Transparent** | Nothing hidden. Clarity in every number and interaction. |
| **Efficient** | Speed without sacrifice. Smart defaults, zero friction. |

**Design Principles:** (1) Data-first — numbers are the hero, decoration stays out of the way. (2) Breathable — ample white space; density only where insight demands it. (3) Accessible — all combinations meet WCAG 2.2 AA by default. (4) Warm trust — cool teal blues anchored by warm neutrals; never cold or sterile.

---

## 2. Color Palette

### 2.1 Primary: Teal → Trust & Growth

| Token | Hex | CSS Variable | Role |
|---|---|---|---|
| P900 | `#0B2B2E` | `--ledgr-p900` | Dark mode base, deep headers |
| P700 | `#0E474B` | `--ledgr-p700` | Secondary surfaces, footer |
| P500 | `#14A89D` | `--ledgr-p500` | **Core brand** — CTAs, links, key UI |
| P300 | `#4ECDC4` | `--ledgr-p300` | Hover states, highlights |
| P100 | `#D4F5F2` | `--ledgr-p100` | Light mode washes, highlighted rows |

### 2.2 Accent: Mint + Gold

| Token | Hex | CSS Variable | Role |
|---|---|---|---|
| Accent Mint | `#00F5A0` | `--ledgr-accent` | Success states, positive deltas, confirmations |
| Accent Gold | `#F5A623` | `--ledgr-accent-gold` | Premium cues, savings highlights, badges |
| Accent Red | `#E8453C` | `--ledgr-accent-red` | Warnings, overspend alerts, destructive actions |

### 2.3 Neutrals: Warm Gray

| Token | Hex | CSS Variable | Role |
|---|---|---|---|
| N900 | `#1A1D20` | `--ledgr-n900` | Primary text, dark surfaces |
| N700 | `#3D4247` | `--ledgr-n700` | Secondary text |
| N500 | `#737980` | `--ledgr-n500` | Tertiary, placeholders |
| N300 | `#C5C9CD` | `--ledgr-n300` | Borders, dividers |
| N100 | `#F2F4F5` | `--ledgr-n100` | Page backgrounds, cards |
| White | `#FFFFFF` | `--ledgr-white` | Elevated surfaces |

### 2.4 Data Visualization Palette

For charts, dashboards, and financial reports — 8 accessible hues:

| # | Hex | Use |
|---|---|---|
| 1 | `#14A89D` | Primary metric |
| 2 | `#4ECDC4` | Secondary metric |
| 3 | `#00F5A0` | Positive delta |
| 4 | `#0E474B` | Deep reference |
| 5 | `#F5A623` | Highlight/warning |
| 6 | `#E8453C` | Negative delta |
| 7 | `#737980` | Neutral baseline |
| 8 | `#C5C9CD` | Grid/reference lines |

### 2.5 Critical Rules

- **P500 (#14A89D)** must occupy ≥12% of color surface in any branded composition.
- **Accent Mint (#00F5A0)** is reserved for interactive/status affordance — never body text or passive fills.
- Minimum contrast: 4.5:1 for body text, 3:1 for large text (≥18px bold / ≥24px regular).
- Use tokens directly. No ad-hoc tinting or shading — especially of accent colors.
- Dark mode: invert backgrounds to P900/N900, text to N100/White. Accents remain unchanged.

---

## 3. Typography System

### 3.1 Typefaces

| Role | Family | Style | Source |
|---|---|---|---|
| Headings | **DM Sans** | Geometric sans | OFL / Google Fonts |
| Body | **Inter** | Neo-grotesque sans | OFL / Google Fonts |
| Mono / Data | **JetBrains Mono** | Developer mono | OFL / JetBrains |

### 3.2 Font Stacks

```css
--ledgr-font-heading: 'DM Sans', 'Inter', system-ui, sans-serif;
--ledgr-font-body: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
--ledgr-font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
```

### 3.3 Type Scale (Major-Third, 16px root)

| Token | Size | Line | Weight | Use |
|---|---|---|---|---|
| `text-hero` | 56px | 1.1 | 700 | Marketing hero (single headline per page max) |
| `text-h1` | 36px | 1.15 | 700 | Page titles |
| `text-h2` | 26px | 1.2 | 600 | Section headers |
| `text-h3` | 20px | 1.25 | 600 | Card headers, subsections |
| `text-h4` | 17px | 1.3 | 600 | Subheadings, sidebar labels |
| `text-lead` | 18px | 1.55 | 400 | Lead paragraphs |
| `text-body` | 16px | 1.55 | 400 | Default body |
| `text-sm` | 14px | 1.5 | 400 | Secondary, metadata |
| `text-xs` | 12px | 1.45 | 500 | Captions, labels, badges |
| `text-mono` | 14px | 1.55 | 400 | Code, financial figures |

### 3.4 Typography Rules

- **Headings:** DM Sans only for H1–H4. Inter forbidden in headings.
- **Tabular figures:** All numbers in tables, dashboards, and financial displays use JetBrains Mono with `font-feature-settings: "tnum"` for aligned columns.
- **Letter-spacing:** `-0.02em` on hero; `+0.03em` on text-xs.
- **Max line length:** 72 characters body, 48 characters headings.
- **Heading hierarchy:** Never skip levels.
- **Weight limits:** DM Sans available at 400, 500, 700. No faux bold/italic.

### 3.5 Responsive

| Breakpoint | Adjustment |
|---|---|
| ≥ 1280px | Full scale |
| 768–1279px | Hero → 42px; H1 → 30px |
| < 768px | Hero → 32px; H1 → 26px; body stays 16px |

---

## 4. Logo & Wordmark

### 4.1 Construction

The Ledgr logo is a two-part lockup:

**Symbol (Icon Mark):** A stylized ligature merging "L" and an open ledger/book spine. The vertical stroke forms the "L"; three horizontal lines (pages) emanate rightward, subtly angled upward 3° to suggest growth. The symbol is built on a 6×6 proportional grid. Never use the symbol alone except as favicon/app icon.

**Wordmark:** "Ledgr" in **DM Sans Bold**, tracked at `0.04em`. The "g" descender is shortened by 12% for tighter line spacing.

### 4.2 Variants

| Variant | Config | Background |
|---|---|---|
| Primary Horizontal | Symbol left, wordmark right | White / N100 |
| Primary Stacked | Symbol centered above wordmark | White / N100 |
| Reversed | All white, same lockups | P900 / P700 |
| Monochrome | N900 | Light backgrounds only |
| Symbol Only | Isolated mark | Favicon, app icon, social avatar |

### 4.3 Clear Space & Sizing

- **Clear space:** Equal to the wordmark "L" height on all sides.
- **Digital minimum:** 120px wide (horizontal), 96px (stacked).
- **Print minimum:** 30mm wide (horizontal).
- **Favicon:** Symbol simplified to 1.5× line weight at ≤32px; recognizable down to 16×16px.

### 4.4 Prohibitions

| ❌ Never |
|---|
| Stretch, squash, or rotate |
| Recolor outside approved variants |
| Apply shadows, glows, or effects |
| Place on busy backgrounds without a protective zone |
| Enclose in a shape (except symbol-only favicon) |
| Change the wordmark typeface |
| Use wordmark without symbol (except email signatures / plain-text) |

---

## 5. Iconography

### 5.1 System: Ledgr Icons

Custom icon set built on a 24×24dp grid.

| Property | Spec |
|---|---|
| Grid | 24 × 24 dp |
| Stroke | 2px |
| Caps / Joins | Round / Round |
| Style | Linear (default), filled (active/selected) |
| Padding | 2px internal safe zone |

### 5.2 Categories

| Category | Direction | Examples |
|---|---|---|
| Dashboard | Geometric, data-forward | Home, Reports, Analytics, Activity |
| Financial | Currency, ledger motifs | Wallet, Transaction, Invoice, Tax |
| Actions | Clear, decisive strokes | Add, Edit, Delete, Export, Filter |
| Status | Filled + color-coded | Success (Mint), Warning (Gold), Error (Red), Pending (N500) |
| Objects | Recognizable silhouettes | Bank, Card, Receipt, Team, Settings |

### 5.3 Usage

- **Sizes:** 16px (compact), 20px (inline), 24px (default), 32px (large UI), 48px (feature spot).
- **Text alignment:** `vertical-align: text-bottom` when inline with body.
- **Color:** Inherit parent text color; override only for status/alert roles.
- **No mixing:** Ledgr Icons only in product UI. Social/partner badges may use third-party icons.
- **Empty states:** Icon at 64px in `N300` on a `N100` rounded-square background (16px radius). Title in `text-h3`, description in `text-sm` at `N500`.

### 5.4 Avatar System

User avatars use a 40px circle. Default (no photo) shows DM Sans initials on a gradient background cycling through P500, P300, and Accent Gold. Financial entities (companies, vendors) use a 40px rounded square (8px radius) with a Ledgr Icon — no gradient.

---

## 6. Photography & Image Style

### 6.1 Direction

Ledgr photography communicates **calm control** in modern financial environments — never chaos, never cliché banking stock.

| Element | Direction |
|---|---|
| **Subject** | Finance professionals in modern, light-filled workspaces. Real interfaces visible but secondary. Diversity standard. |
| **Composition** | Clean symmetry or rule of thirds. Subjects centered or on the right third, looking or gesturing left (toward data). Generous negative space. |
| **Lighting** | Soft, diffused natural light (5000K–5500K). No harsh shadows. Slightly warm bias to counteract cool palette. |
| **Depth** | Moderate (f/2.8–f/5.6). Background softly defocused but recognizable — not full bokeh. |
| **Color Grade** | Lift teal shadows slightly. Warm midtones by 2–3%. Overall neutral-warm, never yellow. |
| **Aspect Ratios** | 16:9 (hero), 3:2 (cards), 1:1 (avatars), 4:3 (blog) |

### 6.2 Treatment Pipeline

1. Lift shadows +8% with teal bias (harmonizes with P500).
2. Reduce saturation by 10% in reds and oranges.
3. Apply subtle warm vignette (15% opacity).
4. Hero images: overlay left edge `rgba(11,43,46,0.25)` fading to transparent at 40% width.

### 6.3 Selection Criteria

| ✅ Use | ❌ Avoid |
|---|---|
| Modern, light-drenched workspaces | Dark, cubicle-heavy bank interiors |
| Real interfaces with blurred data | Competitor products visible |
| Collaborative scenes (2–3 people) | Isolated person-at-desk |
| Clean desks with modern hardware | Clutter, paper stacks, outdated monitors |
| Confident, calm expressions | Forced smiles, handshake clichés |

### 6.4 Channel Mix

- **Marketing pages:** 70% photography, 30% illustration/UI
- **Product UI:** 10% photography (avatars only), 90% data/iconography
- **Blog/content:** 60% photography, 40% data visualization
- **Documentation:** 0% photography, 100% diagrams/screenshots

---

## 7. Illustration & Motifs

### 7.1 Style

Flat vector with restrained gradient accents. Data-centric, never decorative for its own sake.

| Property | Spec |
|---|---|
| Style | Flat vector, geometric |
| Stroke | 2px, round caps — matches icon system |
| Palette | P500, P300, P100, Accent Mint, N300, N100 |
| Gradients | 2-stop P700→P500 on focal elements only |
| Shadows | Soft-only: `0px 6px 20px rgba(11,43,46,0.08)` |

### 7.2 Motifs

| Motif | Meaning | Use |
|---|---|---|
| **Horizontal lines (ledger)** | Records, clarity, order | Dividers, card patterns, backgrounds |
| **Upward-tilted bar** | Growth, positive trajectory | Charts, hero accents, logo |
| **Layered rectangles** | Data layers, dashboards | Empty states, feature illustrations |
| **Circle + line nodes** | Connectivity, flow | Architecture diagrams, integrations |

### 7.3 Background Patterns

- **Ledger lines:** 1px `N300` at 24px spacing, 8% opacity on `N100`.
- **Dot grid:** 1px `P300` dots at 20px spacing, 10% opacity — subtle texture on white.
- **Gradient wash:** Blurred 80px circles of P500 at 6% opacity, randomly placed — hero backdrops.

---

## 8. Spacing & Layout

### 8.1 Grid

| Property | Value |
|---|---|
| Base unit | 8px |
| Columns | 12 |
| Gutter | 24px desktop, 16px tablet, 12px mobile |
| Max width | 1280px (marketing), 1440px (dashboard) |
| Margin | 80px desktop, 32px tablet, 16px mobile |

### 8.2 Spacing Scale

| Token | Value | Use |
|---|---|---|
| `space-1` | 4px | Icon-text gap, tight inline |
| `space-2` | 8px | Internal padding, list gap |
| `space-3` | 16px | Card padding, form spacing |
| `space-4` | 24px | Section padding, modal interior |
| `space-5` | 32px | Component gap |
| `space-6` | 48px | Section gap |
| `space-7` | 64px | Major separation |
| `space-8` | 96px | Page-level gap |

### 8.3 Radius

| Token | Value | Use |
|---|---|---|
| `radius-sm` | 4px | Badges, inline code, small buttons |
| `radius-md` | 8px | Buttons, inputs, cards |
| `radius-lg` | 12px | Modals, panels |
| `radius-xl` | 16px | Empty states, feature cards |
| `radius-full` | 9999px | Pills, avatars, status dots |

---

## 9. UI Component Essentials

### 9.1 Buttons

| Variant | BG | Text | Border | Hover |
|---|---|---|---|---|
| Primary | P500 | White | — | P700 |
| Secondary | Transparent | P500 | 1.5px P500 | P100 bg |
| Ghost | Transparent | P500 | — | P100 bg |
| Accent | Accent Mint | N900 | — | 90% opacity |
| Destructive | Accent Red | White | — | Darken 12% |
| Disabled | N300 | N500 | — | — |

Button height: 44px min (touch). Padding: 16px horizontal, 12px vertical. Radius: `radius-md`.

### 9.2 Cards

- BG: White (light) / N900 at 0.6 opacity (dark)
- Border: 1px N300 (light) / 1px N700 (dark)
- Shadow: `0px 2px 8px rgba(26,29,32,0.05)` resting → `0px 8px 20px rgba(26,29,32,0.08)` hover
- Radius: `radius-md`. Padding: `space-4` (24px).

### 9.3 Inputs

- BG: White, border: 1px N300
- Focus: 2px P500 ring, offset 1px
- Error: 2px Accent Red, bg tint `rgba(232,69,60,0.03)`
- Label: `text-sm`, N700, 8px above
- Placeholder: N500, `text-body`
- Height: 44px minimum

### 9.4 Example: Token Usage in Components

```css
/* Primary button using tokens */
.btn-primary {
  background: var(--ledgr-p500);
  color: var(--ledgr-white);
  border-radius: var(--ledgr-radius-md);
  padding: 12px var(--ledgr-space-3);
  font-family: var(--ledgr-font-body);
}
.btn-primary:hover { background: var(--ledgr-p700); }

/* Card using tokens */
.card {
  background: var(--ledgr-white);
  border: 1px solid var(--ledgr-n300);
  border-radius: var(--ledgr-radius-md);
  padding: var(--ledgr-space-4);
  box-shadow: 0px 2px 8px rgba(26,29,32,0.05);
}

/* Data cell using tokens */
.data-cell {
  font-family: var(--ledgr-font-mono);
  color: var(--ledgr-n900);
  padding: 12px var(--ledgr-space-3);
  text-align: right;
}
```

### 9.5 Data Tables

A core Ledgr component — must be exceptional:

- Header: `text-xs`, N700, 500 weight, uppercase, N100 bg
- Row: `text-body`, N900, alternating White/N100 stripes (every 5 rows for large datasets)
- Hover: P100 bg on row
- Cell padding: 12px vertical, 16px horizontal
- Numeric columns: JetBrains Mono, right-aligned
- Borders: 1px N300 on rows only (horizontal), no vertical dividers

---

## 10. Voice & Tone

### 10.1 Attributes

| Attribute | Expression |
|---|---|
| **Clear** | Plain English. No jargon without immediate definition. |
| **Confident** | We know finance. We state facts, not fluff. |
| **Helpful** | Every message guides toward action. |
| **Human** | Warm but professional. "You" and "your team," never "the user." |
| **Precise** | Numbers, dates, and amounts are always exact. |

### 10.2 Tone by Surface

| Surface | Tone | Example |
|---|---|---|
| Marketing | Aspirational, sharp | *"See every dollar. Control every outcome."* |
| Product UI | Direct, actionable | *"No expenses yet. Connect your first card in 30 seconds."* |
| Error | Blame-free, specific | *"Receipt upload failed. File must be PDF or PNG under 10MB."* |
| Success | Warm, metric-driven | *"Saved $4,230 this quarter by flagging 12 duplicate invoices."* |
| Email | Personal, concise | *"Hey Taylor — your Q2 close is 94% done. 3 items need attention."* |

### 10.3 Rules

1. **Active voice only.** "Ledgr syncs your accounts" — never "Your accounts are synced by Ledgr."
2. **Sentence case in UI.** Buttons, labels, headings: "Add expense" not "Add Expense."
3. **Numbers rule:** Use digits for all financial figures, percentages, dates. Spell out one through nine in prose only.
4. **Currency:** Always show currency symbol. Format per locale. "€1,250.00" not "1250 euros."
5. **No exclamation marks in product UI.** One allowed in marketing headlines per page.
6. **"Ledgr" is singular.** "Ledgr is a financial platform."
7. **Avoid "easy," "simple," "just."** Respect user effort.
8. **Oxford comma required.**

---

## 11. Master Tokens (CSS)

```css
:root {
  /* Primary */
  --ledgr-p900: #0B2B2E;
  --ledgr-p700: #0E474B;
  --ledgr-p500: #14A89D;
  --ledgr-p300: #4ECDC4;
  --ledgr-p100: #D4F5F2;

  /* Accent */
  --ledgr-accent: #00F5A0;
  --ledgr-accent-gold: #F5A623;
  --ledgr-accent-red: #E8453C;

  /* Neutral */
  --ledgr-n900: #1A1D20;
  --ledgr-n700: #3D4247;
  --ledgr-n500: #737980;
  --ledgr-n300: #C5C9CD;
  --ledgr-n100: #F2F4F5;
  --ledgr-white: #FFFFFF;

  /* Typography */
  --ledgr-font-heading: 'DM Sans', 'Inter', system-ui, sans-serif;
  --ledgr-font-body: 'Inter', system-ui, sans-serif;
  --ledgr-font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;

  /* Spacing */
  --ledgr-space-1: 4px;
  --ledgr-space-2: 8px;
  --ledgr-space-3: 16px;
  --ledgr-space-4: 24px;
  --ledgr-space-5: 32px;
  --ledgr-space-6: 48px;
  --ledgr-space-7: 64px;
  --ledgr-space-8: 96px;

  /* Radius */
  --ledgr-radius-sm: 4px;
  --ledgr-radius-md: 8px;
  --ledgr-radius-lg: 12px;
  --ledgr-radius-xl: 16px;
  --ledgr-radius-full: 9999px;
}
```

---

*End of Brand Style Guide v1.0 — Ledgr. For questions, contact brand@ledgr.com (fictional).*
