manifest.json
```json
{
  "project": "Aesthetic Style Composer",
  "version": 2,
  "files": [
    "stylesheets/stylesheet.css",
    "templates/swiss.html",
    "templates/minimal.html",
    "templates/brutalist.html",
    "templates/glass.html",
    "templates/neo-brutalist.html",
    "decision-guide.html"
  ],
  "composition_order": [
    "stylesheets/stylesheet.css (shared foundation — must exist first)",
    "templates/swiss.html",
    "templates/minimal.html",
    "templates/brutalist.html",
    "templates/glass.html",
    "templates/neo-brutalist.html",
    "decision-guide.html (composited reference — must exist last)"
  ],
  "dependency_graph": {
    "swiss.html": ["stylesheet.css"],
    "minimal.html": ["stylesheet.css"],
    "brutalist.html": ["stylesheet.css"],
    "glass.html": ["stylesheet.css"],
    "neo-brutalist.html": ["stylesheet.css"],
    "decision-guide.html": ["stylesheet.css"]
  },
  "shared_tokens": [
    "--color-primary",
    "--color-secondary",
    "--color-accent",
    "--color-bg",
    "--color-surface",
    "--color-text",
    "--color-text-muted",
    "--color-border",
    "--font-sans",
    "--font-heading",
    "--font-mono",
    "--spacing-xs",
    "--spacing-sm",
    "--spacing-md",
    "--spacing-lg",
    "--spacing-xl",
    "--spacing-xxl",
    "--radius-sm",
    "--radius-md",
    "--radius-lg",
    "--breakpoint-sm",
    "--breakpoint-md",
    "--breakpoint-lg",
    "--max-width"
  ],
  "shared_boilerplate": [
    "reset/normalize rules",
    "font-face declarations",
    "grid system (container, row, col-*)",
    "common utilities (.sr-only, .truncate, .aspect-*)",
    "responsive show/hide modifiers"
  ]
}
```
stylesheet.css
```css
/* ============================================
   SHARED STYLESHEET — Aesthetic Style Composer
   All aesthetic templates @import this file.
   Do NOT duplicate these rules per template.
   ============================================ */
/* ----- RESET / NORMALIZE ----- */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
html {
  -webkit-text-size-adjust: 100%;
  -moz-text-size-adjust: 100%;
  text-size-adjust: 100%;
  scroll-behavior: smooth;
  line-height: 1.5;
}
body {
  min-height: 100vh;
  font-family: var(--font-sans, system-ui, sans-serif);
  color: var(--color-text, #111);
  background-color: var(--color-bg, #fff);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
img, picture, video, canvas, svg {
  display: block;
  max-width: 100%;
}
input, button, textarea, select {
  font: inherit;
  color: inherit;
}
p, h1, h2, h3, h4, h5, h6 {
  overflow-wrap: break-word;
}
a {
  color: inherit;
  text-decoration: none;
}
ul, ol {
  list-style: none;
}
table {
  border-collapse: collapse;
  border-spacing: 0;
}
/* ----- ROOT VARIABLES (defaults — overridden per template) ----- */
:root {
  --color-primary: #2563eb;
  --color-secondary: #7c3aed;
  --color-accent: #ef4444;
  --color-bg: #ffffff;
  --color-surface: #f8fafc;
  --color-text: #0f172a;
  --color-text-muted: #64748b;
  --color-border: #e2e8f0;
  --font-sans: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  --font-heading: var(--font-sans);
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  --spacing-xxl: 4rem;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --max-width: 1200px;
}
/* ----- GRID SYSTEM ----- */
.container {
  width: 100%;
  max-width: var(--max-width, 1200px);
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--spacing-lg, 1.5rem);
  padding-right: var(--spacing-lg, 1.5rem);
}
.row {
  display: flex;
  flex-wrap: wrap;
  margin-left: calc(var(--grid-gap, 1rem) * -1);
  margin-right: calc(var(--grid-gap, 1rem) * -1);
}
.col {
  flex: 1 1 0%;
  padding-left: var(--grid-gap, 1rem);
  padding-right: var(--grid-gap, 1rem);
}
.col-1 { flex: 0 0 calc(100% / 12 * 1); max-width: calc(100% / 12 * 1); }
.col-2 { flex: 0 0 calc(100% / 12 * 2); max-width: calc(100% / 12 * 2); }
.col-3 { flex: 0 0 calc(100% / 12 * 3); max-width: calc(100% / 12 * 3); }
.col-4 { flex: 0 0 calc(100% / 12 * 4); max-width: calc(100% / 12 * 4); }
.col-5 { flex: 0 0 calc(100% / 12 * 5); max-width: calc(100% / 12 * 5); }
.col-6 { flex: 0 0 50%; max-width: 50%; }
.col-7 { flex: 0 0 calc(100% / 12 * 7); max-width: calc(100% / 12 * 7); }
.col-8 { flex: 0 0 calc(100% / 12 * 8); max-width: calc(100% / 12 * 8); }
.col-9 { flex: 0 0 calc(100% / 12 * 9); max-width: calc(100% / 12 * 9); }
.col-10 { flex: 0 0 calc(100% / 12 * 10); max-width: calc(100% / 12 * 10); }
.col-11 { flex: 0 0 calc(100% / 12 * 11); max-width: calc(100% / 12 * 11); }
.col-12 { flex: 0 0 100%; max-width: 100%; }
@media (min-width: 640px) {
  .col-sm-1 { flex: 0 0 calc(100% / 12 * 1); max-width: calc(100% / 12 * 1); }
  .col-sm-2 { flex: 0 0 calc(100% / 12 * 2); max-width: calc(100% / 12 * 2); }
  .col-sm-3 { flex: 0 0 calc(100% / 12 * 3); max-width: calc(100% / 12 * 3); }
  .col-sm-4 { flex: 0 0 calc(100% / 12 * 4); max-width: calc(100% / 12 * 4); }
  .col-sm-5 { flex: 0 0 calc(100% / 12 * 5); max-width: calc(100% / 12 * 5); }
  .col-sm-6 { flex: 0 0 50%; max-width: 50%; }
  .col-sm-7 { flex: 0 0 calc(100% / 12 * 7); max-width: calc(100% / 12 * 7); }
  .col-sm-8 { flex: 0 0 calc(100% / 12 * 8); max-width: calc(100% / 12 * 8); }
  .col-sm-9 { flex: 0 0 calc(100% / 12 * 9); max-width: calc(100% / 12 * 9); }
  .col-sm-10 { flex: 0 0 calc(100% / 12 * 10); max-width: calc(100% / 12 * 10); }
  .col-sm-11 { flex: 0 0 calc(100% / 12 * 11); max-width: calc(100% / 12 * 11); }
  .col-sm-12 { flex: 0 0 100%; max-width: 100%; }
}
@media (min-width: 768px) {
  .col-md-1 { flex: 0 0 calc(100% / 12 * 1); max-width: calc(100% / 12 * 1); }
  .col-md-2 { flex: 0 0 calc(100% / 12 * 2); max-width: calc(100% / 12 * 2); }
  .col-md-3 { flex: 0 0 calc(100% / 12 * 3); max-width: calc(100% / 12 * 3); }
  .col-md-4 { flex: 0 0 calc(100% / 12 * 4); max-width: calc(100% / 12 * 4); }
  .col-md-5 { flex: 0 0 calc(100% / 12 * 5); max-width: calc(100% / 12 * 5); }
  .col-md-6 { flex: 0 0 50%; max-width: 50%; }
  .col-md-7 { flex: 0 0 calc(100% / 12 * 7); max-width: calc(100% / 12 * 7); }
  .col-md-8 { flex: 0 0 calc(100% / 12 * 8); max-width: calc(100% / 12 * 8); }
  .col-md-9 { flex: 0 0 calc(100% / 12 * 9); max-width: calc(100% / 12 * 9); }
  .col-md-10 { flex: 0 0 calc(100% / 12 * 10); max-width: calc(100% / 12 * 10); }
  .col-md-11 { flex: 0 0 calc(100% / 12 * 11); max-width: calc(100% / 12 * 11); }
  .col-md-12 { flex: 0 0 100%; max-width: 100%; }
}
@media (min-width: 1024px) {
  .col-lg-1 { flex: 0 0 calc(100% / 12 * 1); max-width: calc(100% / 12 * 1); }
  .col-lg-2 { flex: 0 0 calc(100% / 12 * 2); max-width: calc(100% / 12 * 2); }
  .col-lg-3 { flex: 0 0 calc(100% / 12 * 3); max-width: calc(100% / 12 * 3); }
  .col-lg-4 { flex: 0 0 calc(100% / 12 * 4); max-width: calc(100% / 12 * 4); }
  .col-lg-5 { flex: 0 0 calc(100% / 12 * 5); max-width: calc(100% / 12 * 5); }
  .col-lg-6 { flex: 0 0 50%; max-width: 50%; }
  .col-lg-7 { flex: 0 0 calc(100% / 12 * 7); max-width: calc(100% / 12 * 7); }
  .col-lg-8 { flex: 0 0 calc(100% / 12 * 8); max-width: calc(100% / 12 * 8); }
  .col-lg-9 { flex: 0 0 calc(100% / 12 * 9); max-width: calc(100% / 12 * 9); }
  .col-lg-10 { flex: 0 0 calc(100% / 12 * 10); max-width: calc(100% / 12 * 10); }
  .col-lg-11 { flex: 0 0 calc(100% / 12 * 11); max-width: calc(100% / 12 * 11); }
  .col-lg-12 { flex: 0 0 100%; max-width: 100%; }
}
/* ----- UTILITY CLASSES ----- */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.aspect-square { aspect-ratio: 1 / 1; }
.aspect-video { aspect-ratio: 16 / 9; }
.aspect-portrait { aspect-ratio: 3 / 4; }
/* ----- RESPONSIVE SHOW / HIDE ----- */
.show-sm { display: none; }
.show-md { display: none; }
.show-lg { display: none; }
.hide-sm { display: block; }
.hide-md { display: block; }
.hide-lg { display: block; }
@media (max-width: 639px) {
  .show-sm { display: block; }
  .hide-sm { display: none; }
}
@media (min-width: 640px) and (max-width: 767px) {
  .show-md { display: block; }
  .hide-md { display: none; }
}
@media (min-width: 768px) and (max-width: 1023px) {
  .show-md { display: block; }
  .hide-md { display: none; }
}
@media (min-width: 1024px) {
  .show-lg { display: block; }
  .hide-lg { display: none; }
}
/* ----- TYPOGRAPHY HELPERS ----- */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }
.font-mono { font-family: var(--font-mono); }
.uppercase { text-transform: uppercase; }
.capitalize { text-transform: capitalize; }
.tracking-wide { letter-spacing: 0.05em; }
.tracking-wider { letter-spacing: 0.1em; }
.leading-tight { line-height: 1.25; }
.leading-relaxed { line-height: 1.75; }
/* ----- SPACING HELPERS ----- */
.mt-0 { margin-top: 0; }
.mt-sm { margin-top: var(--spacing-sm); }
.mt-md { margin-top: var(--spacing-md); }
.mt-lg { margin-top: var(--spacing-lg); }
.mt-xl { margin-top: var(--spacing-xl); }
.mt-xxl { margin-top: var(--spacing-xxl); }
.mb-sm { margin-bottom: var(--spacing-sm); }
.mb-md { margin-bottom: var(--spacing-md); }
.mb-lg { margin-bottom: var(--spacing-lg); }
.mb-xl { margin-bottom: var(--spacing-xl); }
.mb-xxl { margin-bottom: var(--spacing-xxl); }
.p-sm { padding: var(--spacing-sm); }
.p-md { padding: var(--spacing-md); }
.p-lg { padding: var(--spacing-lg); }
.p-xl { padding: var(--spacing-xl); }
.py-md { padding-top: var(--spacing-md); padding-bottom: var(--spacing-md); }
.py-lg { padding-top: var(--spacing-lg); padding-bottom: var(--spacing-lg); }
.py-xl { padding-top: var(--spacing-xl); padding-bottom: var(--spacing-xl); }
.px-md { padding-left: var(--spacing-md); padding-right: var(--spacing-md); }
.px-lg { padding-left: var(--spacing-lg); padding-right: var(--spacing-lg); }
.px-xl { padding-left: var(--spacing-xl); padding-right: var(--spacing-xl); }
/* ----- BORDER HELPERS ----- */
.border { border: 1px solid var(--color-border); }
.border-t { border-top: 1px solid var(--color-border); }
.border-b { border-bottom: 1px solid var(--color-border); }
.rounded-sm { border-radius: var(--radius-sm); }
.rounded-md { border-radius: var(--radius-md); }
.rounded-lg { border-radius: var(--radius-lg); }
.rounded-full { border-radius: 9999px; }
/* ----- FLEX HELPERS ----- */
.flex { display: flex; }
.flex-col { flex-direction: column; }
.flex-wrap { flex-wrap: wrap; }
.items-center { align-items: center; }
.items-start { align-items: flex-start; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.gap-sm { gap: var(--spacing-sm); }
.gap-md { gap: var(--spacing-md); }
.gap-lg { gap: var(--spacing-lg); }
.gap-xl { gap: var(--spacing-xl); }
/* ----- SECTION DEFAULTS ----- */
.section {
  padding-top: var(--spacing-xxl, 4rem);
  padding-bottom: var(--spacing-xxl, 4rem);
}
.section-sm {
  padding-top: var(--spacing-xl, 2rem);
  padding-bottom: var(--spacing-xl, 2rem);
}
/* ----- CARD DEFAULTS ----- */
.card {
  background: var(--color-surface, #f8fafc);
  border: 1px solid var(--color-border, #e2e8f0);
  border-radius: var(--radius-md, 8px);
  padding: var(--spacing-lg, 1.5rem);
}
```
templates/swiss.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Swiss International Style — Aesthetic Template</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../stylesheets/stylesheet.css">
  <style>
    :root {
      --color-primary: #da291c;
      --color-secondary: #003057;
      --color-accent: #da291c;
      --color-bg: #f5f5f5;
      --color-surface: #ffffff;
      --color-text: #1a1a1a;
      --color-text-muted: #666666;
      --color-border: #cccccc;
      --font-sans: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
      --font-heading: 'Inter', 'Akzidenz-Grotesk', 'Helvetica Neue', Arial, sans-serif;
      --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
      --grid-gap: 1.5rem;
    }
    body {
      background: var(--color-bg);
    }
    /* Swiss grid — asymmetric, precise */
    .swiss-grid {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr;
      gap: var(--grid-gap);
    }
    .swiss-grid > .span-2 {
      grid-column: span 2;
    }
    .swiss-grid > .span-3 {
      grid-column: span 3;
    }
    .swiss-grid > .span-4 {
      grid-column: span 4;
    }
    .swiss-grid > .span-6 {
      grid-column: span 6;
    }
    .swiss-grid > .offset-1 {
      grid-column: 2 / span 1;
    }
    .swiss-grid > .offset-2 {
      grid-column: 3 / span 1;
    }
    .swiss-header {
      padding: var(--spacing-xxl) 0 var(--spacing-xl);
      border-bottom: 4px solid var(--color-primary);
      margin-bottom: var(--spacing-xxl);
    }
    .swiss-header h1 {
      font-family: var(--font-heading);
      font-size: 3.5rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      line-height: 1.1;
      text-transform: uppercase;
      color: var(--color-text);
    }
    .swiss-header .subtitle {
      font-family: var(--font-heading);
      font-size: 1rem;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      color: var(--color-primary);
      margin-top: var(--spacing-md);
    }
    .swiss-header .meta {
      font-family: var(--font-sans);
      font-size: 0.75rem;
      font-weight: 400;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--color-text-muted);
      margin-top: var(--spacing-sm);
    }
    .swiss-block {
      background: var(--color-surface);
      padding: var(--spacing-lg);
      border-top: 2px solid var(--color-primary);
      margin-bottom: var(--spacing-lg);
    }
    .swiss-block h2 {
      font-family: var(--font-heading);
      font-size: 1.25rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: var(--spacing-sm);
    }
    .swiss-block p {
      font-family: var(--font-sans);
      font-size: 0.875rem;
      line-height: 1.6;
      color: var(--color-text);
    }
    .swiss-block .label {
      font-family: var(--font-heading);
      font-size: 0.6875rem;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--color-primary);
      margin-bottom: var(--spacing-xs);
    }
    .swiss-asymmetric {
      display: grid;
      grid-template-columns: 2fr 1fr 1fr;
      gap: var(--grid-gap);
    }
    .swiss-footer {
      margin-top: var(--spacing-xxl);
      padding: var(--spacing-xl) 0;
      border-top: 1px solid var(--color-border);
      font-family: var(--font-sans);
      font-size: 0.6875rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--color-text-muted);
    }
    @media (max-width: 768px) {
      .swiss-grid {
        grid-template-columns: 1fr 1fr;
      }
      .swiss-grid > .span-2,
      .swiss-grid > .span-3,
      .swiss-grid > .span-4,
      .swiss-grid > .span-6 {
        grid-column: span 2;
      }
      .swiss-grid > .offset-1,
      .swiss-grid > .offset-2 {
        grid-column: 1 / span 2;
      }
      .swiss-asymmetric {
        grid-template-columns: 1fr;
      }
      .swiss-header h1 {
        font-size: 2.25rem;
      }
    }
    @media (max-width: 480px) {
      .swiss-grid {
        grid-template-columns: 1fr;
      }
      .swiss-grid > .span-2,
      .swiss-grid > .span-3,
      .swiss-grid > .span-4,
      .swiss-grid > .span-6 {
        grid-column: span 1;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <header class="swiss-header">
      <div class="meta">Design System / Volume 01</div>
      <h1>International Typographic Style</h1>
      <div class="subtitle">Grid — Asymmetry — Clarity</div>
    </header>
    <div class="swiss-grid">
      <div class="span-3">
        <div class="swiss-block">
          <div class="label">Principle</div>
          <h2>Grid as Structure</h2>
          <p>The Swiss style treats the grid not as a constraint but as a liberating framework. Every element finds its place within a mathematical proportion, creating visual harmony through rational arrangement.</p>
        </div>
      </div>
      <div class="span-2">
        <div class="swiss-block">
          <div class="label">Typography</div>
          <h2>Akzidenz-Grotesk</h2>
          <p>The quintessential Swiss typeface. Neutral, unadorned, universal. Paired with Helvetica for body text, it creates a typographic voice that is authoritative without being authoritatian.</p>
        </div>
      </div>
      <div class="span-1">
        <div class="swiss-block" style="border-top-color: var(--color-secondary);">
          <div class="label">Color</div>
          <h2>Red Accent</h2>
          <p>Signal red (#da291c) against an off-white field. A single accent color is sufficient.</p>
        </div>
      </div>
    </div>
    <div class="swiss-asymmetric mt-xxl">
      <div class="swiss-block">
        <div class="label">Layout</div>
        <h2>Asymmetric Balance</h2>
        <p>Swiss composition rejects centered symmetry in favor of dynamic, asymmetric arrangements. The eye moves diagonally across the page, guided by contrasting weights and negative space.</p>
        <p class="mt-md">The 6-column grid enables both wide narrative spans and narrow data columns, all held in precise tension.</p>
      </div>
      <div class="swiss-block">
        <div class="label">Usage</div>
        <h2>Best For</h2>
        <p>Editorial layouts, museum catalogs, architectural portfolios, brand guidelines, corporate reports, academic posters.</p>
      </div>
      <div class="swiss-block">
        <div class="label">Avoid</div>
        <h2>Not For</h2>
        <p>Casual or playful interfaces, children's products, entertainment media, anything requiring decorative ornament.</p>
      </div>
    </div>
    <div class="swiss-grid mt-xxl">
      <div class="span-2">
        <div class="swiss-block">
          <div class="label">Token</div>
          <h2>--color-primary</h2>
          <p style="color: var(--color-primary); font-weight: 700;">#da291c — Signal Red</p>
        </div>
      </div>
      <div class="span-2">
        <div class="swiss-block">
          <div class="label">Token</div>
          <h2>--color-secondary</h2>
          <p style="color: var(--color-secondary); font-weight: 700;">#003057 — Deep Blue</p>
        </div>
      </div>
      <div class="span-2">
        <div class="swiss-block">
          <div class="label">Token</div>
          <h2>--font-heading</h2>
          <p style="font-family: var(--font-heading); font-weight: 700;">Akzidenz-Grotesk / Helvetica</p>
        </div>
      </div>
    </div>
    <footer class="swiss-footer">
      <div class="row">
        <div class="col-6">
          Swiss International Style Template &mdash; Aesthetic Style Composer v2
        </div>
        <div class="col-6 text-right">
          &copy; 2026 &mdash; Design Systems Reference
        </div>
      </div>
    </footer>
  </div>
</body>
</html>
```
templates/minimal.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Minimal — Aesthetic Template</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../stylesheets/stylesheet.css">
  <style>
    :root {
      --color-primary: #1a1a1a;
      --color-secondary: #555555;
      --color-accent: #999999;
      --color-bg: #fafafa;
      --color-surface: #ffffff;
      --color-text: #1a1a1a;
      --color-text-muted: #999999;
      --color-border: #e5e5e5;
      --font-sans: 'Inter', -apple-system, system-ui, sans-serif;
      --font-heading: 'Inter', -apple-system, system-ui, sans-serif;
      --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
      --grid-gap: 2rem;
    }
    body {
      background: var(--color-bg);
    }
    .min-header {
      padding: var(--spacing-xxl) 0 var(--spacing-xl);
      margin-bottom: var(--spacing-xxl);
    }
    .min-header h1 {
      font-family: var(--font-heading);
      font-size: 2.75rem;
      font-weight: 300;
      letter-spacing: -0.03em;
      line-height: 1.15;
      color: var(--color-text);
      max-width: 60%;
    }
    .min-header .subtitle {
      font-family: var(--font-sans);
      font-size: 0.9375rem;
      font-weight: 400;
      color: var(--color-text-muted);
      margin-top: var(--spacing-md);
      max-width: 40%;
    }
    .min-divider {
      width: 3rem;
      height: 1px;
      background: var(--color-border);
      margin: var(--spacing-xxl) 0;
    }
    .min-card {
      background: var(--color-surface);
      border: none;
      padding: var(--spacing-xl);
      transition: all 0.3s ease;
    }
    .min-card:hover {
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .min-card .number {
      font-family: var(--font-heading);
      font-size: 0.75rem;
      font-weight: 500;
      color: var(--color-text-muted);
      letter-spacing: 0.05em;
      margin-bottom: var(--spacing-sm);
    }
    .min-card h2 {
      font-family: var(--font-heading);
      font-size: 1.25rem;
      font-weight: 400;
      letter-spacing: -0.01em;
      line-height: 1.3;
      margin-bottom: var(--spacing-sm);
      color: var(--color-text);
    }
    .min-card p {
      font-family: var(--font-sans);
      font-size: 0.875rem;
      font-weight: 400;
      line-height: 1.7;
      color: var(--color-text-muted);
    }
    .min-stat {
      text-align: center;
      padding: var(--spacing-xl) 0;
    }
    .min-stat .value {
      font-family: var(--font-heading);
      font-size: 3rem;
      font-weight: 300;
      letter-spacing: -0.03em;
      color: var(--color-text);
    }
    .min-stat .label {
      font-family: var(--font-sans);
      font-size: 0.8125rem;
      color: var(--color-text-muted);
      margin-top: var(--spacing-xs);
    }
    .min-footer {
      margin-top: var(--spacing-xxl);
      padding: var(--spacing-xl) 0;
      border-top: 1px solid var(--color-border);
      font-family: var(--font-sans);
      font-size: 0.8125rem;
      color: var(--color-text-muted);
    }
    .min-footer a {
      color: var(--color-text);
      border-bottom: 1px solid transparent;
      transition: border-color 0.2s;
    }
    .min-footer a:hover {
      border-bottom-color: var(--color-text);
    }
    @media (max-width: 768px) {
      .min-header h1 {
        font-size: 2rem;
        max-width: 100%;
      }
      .min-header .subtitle {
        max-width: 100%;
      }
      .min-stat .value {
        font-size: 2.25rem;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <header class="min-header">
      <h1>Reduce to the essential. Remove everything that serves no purpose.</h1>
      <div class="subtitle">Dieter Rams' principles of good design applied to modern interface architecture. Less, but better.</div>
    </header>
    <div class="row">
      <div class="col-4">
        <div class="min-card">
          <div class="number">01</div>
          <h2>Good design is innovative</h2>
          <p>The possibilities for progression are not, by any means, exhausted. Technological development is always offering new opportunities for original designs.</p>
        </div>
      </div>
      <div class="col-4">
        <div class="min-card">
          <div class="number">02</div>
          <h2>Good design is aesthetic</h2>
          <p>The aesthetic quality of a product is integral to its usefulness because products are used every day and have an effect on people and their well-being.</p>
        </div>
      </div>
      <div class="col-4">
        <div class="min-card">
          <div class="number">03</div>
          <h2>Good design is unobtrusive</h2>
          <p>Products fulfilling a purpose are like tools. They are neither decorative objects nor works of art. Their design should be both neutral and restrained.</p>
        </div>
      </div>
    </div>
    <div class="min-divider"></div>
    <div class="row">
      <div class="col-3">
        <div class="min-stat">
          <div class="value">1960</div>
          <div class="label">Origin Decade</div>
        </div>
      </div>
      <div class="col-3">
        <div class="min-stat">
          <div class="value">10</div>
          <div class="label">Rams Principles</div>
        </div>
      </div>
      <div class="col-3">
        <div class="min-stat">
          <div class="value">80%</div>
          <div class="label">White Space Ratio</div>
        </div>
      </div>
      <div class="col-3">
        <div class="min-stat">
          <div class="value">3</div>
          <div class="label">Colors Maximum</div>
        </div>
      </div>
    </div>
    <div class="min-divider"></div>
    <div class="row">
      <div class="col-6">
        <div class="min-card">
          <div class="number">Token Reference</div>
          <h2>--color-text: #1a1a1a</h2>
          <p>Near-black for maximum readability with minimal visual weight. Paired with --color-text-muted: #999999 for secondary information.</p>
        </div>
      </div>
      <div class="col-6">
        <div class="min-card">
          <div class="number">Token Reference</div>
          <h2>--spacing-xxl: 4rem</h2>
          <p>Expansive vertical rhythm creates breathing room. The space between elements communicates hierarchy without relying on decorative borders.</p>
        </div>
      </div>
    </div>
    <footer class="min-footer">
      <div class="row">
        <div class="col-6">
          Minimal Template &mdash; Aesthetic Style Composer v2
        </div>
        <div class="col-6 text-right">
          Inspired by Dieter Rams &mdash; &copy; 2026
        </div>
      </div>
    </footer>
  </div>
</body>
</html>
```
templates/brutalist.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Brutalist — Aesthetic Template</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;700&family=IBM+Plex+Sans:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../stylesheets/stylesheet.css">
  <style>
    :root {
      --color-primary: #000000;
      --color-secondary: #333333;
      --color-accent: #ffffff;
      --color-bg: #ffffff;
      --color-surface: #f0f0f0;
      --color-text: #000000;
      --color-text-muted: #666666;
      --color-border: #000000;
      --font-sans: 'IBM Plex Sans', Arial, sans-serif;
      --font-heading: 'IBM Plex Mono', 'Courier New', monospace;
      --font-mono: 'IBM Plex Mono', 'Courier New', monospace;
      --grid-gap: 0;
      --radius-sm: 0;
      --radius-md: 0;
      --radius-lg: 0;
    }
    body {
      background: var(--color-bg);
    }
    .brut-header {
      padding: var(--spacing-xl) 0;
      border-bottom: 6px solid var(--color-border);
      margin-bottom: var(--spacing-xl);
    }
    .brut-header h1 {
      font-family: var(--font-heading);
      font-size: 4rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.02em;
      line-height: 1;
      color: var(--color-text);
    }
    .brut-header .subtitle {
      font-family: var(--font-heading);
      font-size: 0.875rem;
      font-weight: 400;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--color-text-muted);
      margin-top: var(--spacing-sm);
    }
    .brut-block {
      background: var(--color-surface);
      border: 3px solid var(--color-border);
      padding: var(--spacing-lg);
      margin-bottom: var(--spacing-md);
    }
    .brut-block h2 {
      font-family: var(--font-heading);
      font-size: 1.375rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.02em;
      margin-bottom: var(--spacing-sm);
    }
    .brut-block p {
      font-family: var(--font-sans);
      font-size: 1rem;
      line-height: 1.5;
      color: var(--color-text);
    }
    .brut-block.inverted {
      background: var(--color-primary);
      color: var(--color-accent);
      border-color: var(--color-primary);
    }
    .brut-block.inverted h2,
    .brut-block.inverted p {
      color: var(--color-accent);
    }
    .brut-label {
      display: inline-block;
      font-family: var(--font-heading);
      font-size: 0.6875rem;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      background: var(--color-primary);
      color: var(--color-accent);
      padding: 0.25rem 0.75rem;
      margin-bottom: var(--spacing-sm);
    }
    .brut-table {
      width: 100%;
      border: 3px solid var(--color-border);
      font-family: var(--font-heading);
      font-size: 0.8125rem;
    }
    .brut-table th,
    .brut-table td {
      border: 2px solid var(--color-border);
      padding: var(--spacing-sm) var(--spacing-md);
      text-align: left;
      text-transform: uppercase;
    }
    .brut-table th {
      background: var(--color-primary);
      color: var(--color-accent);
      font-weight: 700;
    }
    .brut-table td {
      background: var(--color-bg);
    }
    .brut-footer {
      margin-top: var(--spacing-xxl);
      padding: var(--spacing-lg) 0;
      border-top: 6px solid var(--color-border);
      font-family: var(--font-heading);
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .brut-badge {
      display: inline-block;
      font-family: var(--font-heading);
      font-size: 0.625rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      background: var(--color-primary);
      color: var(--color-accent);
      padding: 0.375rem 1rem;
      border: 2px solid var(--color-primary);
    }
    @media (max-width: 768px) {
      .brut-header h1 {
        font-size: 2.5rem;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <header class="brut-header">
      <span class="brut-badge">Architecture &bull; Code &bull; Structure</span>
      <h1>Raw Brutalism</h1>
      <div class="subtitle">No ornament. No decoration. No compromise.</div>
    </header>
    <div class="row">
      <div class="col-8">
        <div class="brut-block">
          <span class="brut-label">Manifesto</span>
          <h2>Truth to Materials</h2>
          <p>Brutalism exposes its structure. Every beam, every joint, every reinforcement is visible. In code, this means raw HTML structure, unpolished grids, and borders that assert their presence. The medium is the message.</p>
        </div>
        <div class="brut-block inverted">
          <span class="brut-label" style="background: var(--color-accent); color: var(--color-primary);">Principle</span>
          <h2>Raw is Honest</h2>
          <p>A button looks like a button. A border is a border. No drop shadows, no gradients, no effects that pretend to be something they are not. The digital material is the pixel, and we use it directly.</p>
        </div>
      </div>
      <div class="col-4">
        <div class="brut-block">
          <span class="brut-label">Tokens</span>
          <h2>Monochrome</h2>
          <p>--color-primary: #000000<br>--color-bg: #ffffff<br>--color-border: #000000<br>--radius-md: 0</p>
        </div>
        <div class="brut-block">
          <span class="brut-label">Typography</span>
          <h2>IBM Plex Mono</h2>
          <p>Monospace for headings conveys the engineering-first ethos. Sans-serif body text keeps long reading passages legible without sacrificing the industrial feel.</p>
        </div>
      </div>
    </div>
    <div class="mt-xxl">
      <h2 style="font-family: var(--font-heading); font-size: 1.5rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: var(--spacing-md);">Design Token Registry</h2>
      <table class="brut-table">
        <thead>
          <tr>
            <th>Token</th>
            <th>Value</th>
            <th>Role</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>--color-primary</td>
            <td>#000000</td>
            <td>Pure black — absolute contrast</td>
          </tr>
          <tr>
            <td>--color-bg</td>
            <td>#ffffff</td>
            <td>Pure white — maximum legibility</td>
          </tr>
          <tr>
            <td>--color-border</td>
            <td>#000000</td>
            <td>Heavy black borders — 3px minimum</td>
          </tr>
          <tr>
            <td>--radius-md</td>
            <td>0</td>
            <td>No rounded corners — structural honesty</td>
          </tr>
          <tr>
            <td>--font-heading</td>
            <td>IBM Plex Mono</td>
            <td>Monospace — raw, engineered voice</td>
          </tr>
        </tbody>
      </table>
    </div>
    <footer class="brut-footer">
      <div class="row">
        <div class="col-6">
          Brutalist Template &mdash; Aesthetic Style Composer v2
        </div>
        <div class="col-6 text-right">
          Concrete &amp; Code &mdash; &copy; 2026
        </div>
      </div>
    </footer>
  </div>
</body>
</html>
```
templates/glass.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Glass — Aesthetic Template</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../stylesheets/stylesheet.css">
  <style>
    :root {
      --color-primary: #0071e3;
      --color-secondary: #5e5ce6;
      --color-accent: #ff2d55;
      --color-bg: #0a0a0f;
      --color-surface: rgba(255, 255, 255, 0.06);
      --color-text: #ffffff;
      --color-text-muted: rgba(255, 255, 255, 0.55);
      --color-border: rgba(255, 255, 255, 0.12);
      --font-sans: -apple-system, 'SF Pro Display', 'Helvetica Neue', system-ui, sans-serif;
      --font-heading: -apple-system, 'SF Pro Display', 'Helvetica Neue', system-ui, sans-serif;
      --font-mono: 'SF Mono', 'JetBrains Mono', monospace;
      --grid-gap: 1.5rem;
      --radius-sm: 8px;
      --radius-md: 16px;
      --radius-lg: 24px;
    }
    body {
      background: var(--color-bg);
      background-image:
        radial-gradient(ellipse 80% 60% at 10% 20%, rgba(0, 113, 227, 0.15), transparent),
        radial-gradient(ellipse 60% 50% at 90% 80%, rgba(94, 92, 230, 0.12), transparent),
        radial-gradient(ellipse 50% 40% at 50% 50%, rgba(255, 45, 85, 0.05), transparent);
    }
    .glass-header {
      padding: var(--spacing-xxl) 0 var(--spacing-xl);
      margin-bottom: var(--spacing-xl);
      position: relative;
    }
    .glass-header h1 {
      font-family: var(--font-heading);
      font-size: 3.5rem;
      font-weight: 700;
      letter-spacing: -0.03em;
      line-height: 1.05;
      background: linear-gradient(135deg, #ffffff 0%, rgba(255,255,255,0.7) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    .glass-header .subtitle {
      font-family: var(--font-sans);
      font-size: 1.125rem;
      font-weight: 400;
      color: var(--color-text-muted);
      margin-top: var(--spacing-md);
      max-width: 50%;
    }
    .glass-card {
      background: var(--color-surface);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      padding: var(--spacing-xl);
      transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
      position: relative;
      overflow: hidden;
    }
    .glass-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    }
    .glass-card:hover {
      background: rgba(255, 255, 255, 0.1);
      border-color: rgba(255, 255, 255, 0.2);
      transform: translateY(-2px);
    }
    .glass-card .icon {
      width: 2.5rem;
      height: 2.5rem;
      border-radius: var(--radius-md);
      background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.25rem;
      margin-bottom: var(--spacing-md);
    }
    .glass-card h2 {
      font-family: var(--font-heading);
      font-size: 1.25rem;
      font-weight: 600;
      letter-spacing: -0.01em;
      margin-bottom: var(--spacing-sm);
      color: var(--color-text);
    }
    .glass-card p {
      font-family: var(--font-sans);
      font-size: 0.9375rem;
      font-weight: 400;
      line-height: 1.6;
      color: var(--color-text-muted);
    }
    .glass-card .tag {
      display: inline-block;
      font-size: 0.6875rem;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 0.25rem 0.75rem;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.08);
      color: var(--color-text-muted);
      margin-top: var(--spacing-md);
    }
    .glass-feature {
      background: var(--color-surface);
      backdrop-filter: blur(30px);
      -webkit-backdrop-filter: blur(30px);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      padding: var(--spacing-xxl);
      text-align: center;
    }
    .glass-feature h2 {
      font-family: var(--font-heading);
      font-size: 2rem;
      font-weight: 600;
      letter-spacing: -0.02em;
      color: var(--color-text);
    }
    .glass-feature p {
      font-family: var(--font-sans);
      font-size: 1rem;
      color: var(--color-text-muted);
      max-width: 600px;
      margin: var(--spacing-md) auto 0;
    }
    .glass-footer {
      margin-top: var(--spacing-xxl);
      padding: var(--spacing-xl) 0;
      border-top: 1px solid var(--color-border);
      font-family: var(--font-sans);
      font-size: 0.8125rem;
      color: var(--color-text-muted);
    }
    @media (max-width: 768px) {
      .glass-header h1 {
        font-size: 2.25rem;
      }
      .glass-header .subtitle {
        max-width: 100%;
        font-size: 1rem;
      }
      .glass-feature {
        padding: var(--spacing-xl);
      }
      .glass-feature h2 {
        font-size: 1.5rem;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <header class="glass-header">
      <h1>Glassmorphism Design Language</h1>
      <div class="subtitle">Depth through transparency. A layered interface system built on backdrop blur, frosted surfaces, and ambient glow.</div>
    </header>
    <div class="row">
      <div class="col-4">
        <div class="glass-card">
          <div class="icon">✦</div>
          <h2>Backdrop Blur</h2>
          <p>Frosted glass surfaces created with backdrop-filter: blur(20px) let background content show through while maintaining readability.</p>
          <span class="tag">CSS Property</span>
        </div>
      </div>
      <div class="col-4">
        <div class="glass-card">
          <div class="icon">◉</div>
          <h2>Ambient Glow</h2>
          <p>Radial gradients behind the glass layer create depth cues. The eye perceives physical distance between content layers.</p>
          <span class="tag">Background Composite</span>
        </div>
      </div>
      <div class="col-4">
        <div class="glass-card">
          <div class="icon">⊞</div>
          <h2>Layered Depth</h2>
          <p>Three visual planes: background gradient, frosted card surface, and crisp foreground content. Each layer has distinct blur and opacity.</p>
          <span class="tag">Z-Index Strategy</span>
        </div>
      </div>
    </div>
    <div class="mt-xxl">
      <div class="glass-feature">
        <h2>--color-surface: rgba(255, 255, 255, 0.06)</h2>
        <p>Ultra-low opacity surfaces accumulate into readable frosted panels. The alpha channel is the primary design dimension — controlling translucency controls hierarchy.</p>
      </div>
    </div>
    <div class="row mt-xxl">
      <div class="col-6">
        <div class="glass-card">
          <div class="icon">⚙</div>
          <h2>Token: --radius-lg: 24px</h2>
          <p>Generous corner radius reinforces the soft, premium feel of glass surfaces. Sharp corners would break the illusion of physical frosted material.</p>
        </div>
      </div>
      <div class="col-6">
        <div class="glass-card">
          <div class="icon">🔤</div>
          <h2>Token: --font-sans: SF Pro</h2>
          <p>Apple's system typeface provides the clean, precise typography that glassmorphism demands. High weight contrast and tight spacing maintain clarity on frosted surfaces.</p>
        </div>
      </div>
    </div>
    <footer class="glass-footer">
      <div class="row">
        <div class="col-6">
          Glass Template &mdash; Aesthetic Style Composer v2
        </div>
        <div class="col-6 text-right">
          Depth Through Transparency &mdash; &copy; 2026
        </div>
      </div>
    </footer>
  </div>
</body>
</html>
```
templates/neo-brutalist.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Neo-Brutalist — Aesthetic Template</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../stylesheets/stylesheet.css">
  <style>
    :root {
      --color-primary: #ff006e;
      --color-secondary: #8338ec;
      --color-accent: #ffbe0b;
      --color-bg: #f8f9fa;
      --color-surface: #ffffff;
      --color-text: #1a1a2e;
      --color-text-muted: #6c757d;
      --color-border: #1a1a2e;
      --font-sans: 'Space Grotesk', system-ui, sans-serif;
      --font-heading: 'Space Grotesk', system-ui, sans-serif;
      --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
      --grid-gap: 1rem;
      --radius-sm: 0;
      --radius-md: 0;
      --radius-lg: 0;
    }
    body {
      background: var(--color-bg);
      position: relative;
    }
    body::before {
      content: '';
      position: fixed;
      top: -50%;
      left: -50%;
      width: 200%;
      height: 200%;
      background:
        radial-gradient(circle at 20% 30%, rgba(255, 0, 110, 0.03) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(131, 56, 236, 0.03) 0%, transparent 50%),
        radial-gradient(circle at 50% 50%, rgba(255, 190, 11, 0.02) 0%, transparent 50%);
      pointer-events: none;
      z-index: 0;
    }
    .container {
      position: relative;
      z-index: 1;
    }
    .neo-header {
      padding: var(--spacing-xxl) 0 var(--spacing-lg);
      border-bottom: 6px solid var(--color-primary);
      margin-bottom: var(--spacing-xl);
      position: relative;
    }
    .neo-header::after {
      content: '☀';
      position: absolute;
      bottom: -1.5rem;
      right: 0;
      font-size: 3rem;
      color: var(--color-accent);
      transform: rotate(15deg);
    }
    .neo-header .badge-row {
      display: flex;
      gap: var(--spacing-sm);
      margin-bottom: var(--spacing-sm);
      flex-wrap: wrap;
    }
    .neo-badge {
      display: inline-block;
      font-family: var(--font-heading);
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 0.375rem 1rem;
      background: var(--color-primary);
      color: #ffffff;
      border: 3px solid var(--color-border);
    }
    .neo-badge.secondary {
      background: var(--color-secondary);
    }
    .neo-badge.accent {
      background: var(--color-accent);
      color: var(--color-text);
    }
    .neo-header h1 {
      font-family: var(--font-heading);
      font-size: 5rem;
      font-weight: 700;
      letter-spacing: -0.03em;
      line-height: 0.9;
      color: var(--color-text);
      text-transform: uppercase;
      margin-top: var(--spacing-md);
    }
    .neo-header .subtitle {
      font-family: var(--font-heading);
      font-size: 1.125rem;
      font-weight: 500;
      color: var(--color-text-muted);
      margin-top: var(--spacing-sm);
    }
    .neo-card {
      background: var(--color-surface);
      border: 4px solid var(--color-border);
      padding: var(--spacing-lg);
      transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
      position: relative;
    }
    .neo-card:hover {
      transform: translate(-4px, -4px);
      box-shadow: 8px 8px 0 var(--color-primary);
    }
    .neo-card .card-icon {
      font-size: 2.5rem;
      margin-bottom: var(--spacing-sm);
      line-height: 1;
    }
    .neo-card h2 {
      font-family: var(--font-heading);
      font-size: 1.5rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      margin-bottom: var(--spacing-sm);
    }
    .neo-card p {
      font-family: var(--font-sans);
      font-size: 0.9375rem;
      line-height: 1.6;
      color: var(--color-text-muted);
    }
    .neo-card.accent-border {
      border-color: var(--color-accent);
    }
    .neo-card.accent-border:hover {
      box-shadow: 8px 8px 0 var(--color-accent);
    }
    .neo-card.pink-border {
      border-color: var(--color-primary);
    }
    .neo-card.pink-border:hover {
      box-shadow: 8px 8px 0 var(--color-primary);
    }
    .neo-card.purple-border {
      border-color: var(--color-secondary);
    }
    .neo-card.purple-border:hover {
      box-shadow: 8px 8px 0 var(--color-secondary);
    }
    .neo-cta {
      display: inline-block;
      font-family: var(--font-heading);
      font-size: 1rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: var(--spacing-md) var(--spacing-xl);
      background: var(--color-primary);
      color: #ffffff;
      border: 4px solid var(--color-border);
      transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
      cursor: pointer;
    }
    .neo-cta:hover {
      transform: translate(-3px, -3px);
      box-shadow: 6px 6px 0 var(--color-accent);
    }
    .neo-cta.secondary {
      background: var(--color-secondary);
    }
    .neo-cta.accent {
      background: var(--color-accent);
      color: var(--color-text);
    }
    .neo-footer {
      margin-top: var(--spacing-xxl);
      padding: var(--spacing-xl) 0;
      border-top: 6px solid var(--color-accent);
      font-family: var(--font-heading);
      font-size: 0.8125rem;
    }
    .neo-shape {
      width: 100%;
      height: 20px;
      background: repeating-linear-gradient(
        45deg,
        var(--color-accent),
        var(--color-accent) 10px,
        transparent 10px,
        transparent 20px
      );
      margin: var(--spacing-lg) 0;
    }
    @media (max-width: 768px) {
      .neo-header h1 {
        font-size: 3rem;
      }
      .neo-header::after {
        font-size: 2rem;
        bottom: -1rem;
      }
      .neo-card:hover {
        transform: none;
        box-shadow: none;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <header class="neo-header">
      <div class="badge-row">
        <span class="neo-badge">Neo</span>
        <span class="neo-badge secondary">Playful</span>
        <span class="neo-badge accent">Loud</span>
      </div>
      <h1>Neo-Brutalism</h1>
      <div class="subtitle">Raw structure meets vibrant energy. Oversized, colorful, unapologetic.</div>
    </header>
    <div class="row">
      <div class="col-4">
        <div class="neo-card pink-border">
          <div class="card-icon">⬡</div>
          <h2>Bold Color</h2>
          <p>Hot pink, deep purple, and bright yellow define the palette. Neo-brutalism rejects monochrome restraint in favor of emotional, saturated hues.</p>
        </div>
      </div>
      <div class="col-4">
        <div class="neo-card accent-border">
          <div class="card-icon">⬠</div>
          <h2>Playful Geometry</h2>
          <p>Decorative shapes, rotating elements, and playful decorative accents add personality without undermining structural clarity.</p>
        </div>
      </div>
      <div class="col-4">
        <div class="neo-card purple-border">
          <div class="card-icon">⬢</div>
          <h2>Oversized Type</h2>
          <p>5rem headings are the norm. Space Grotesk provides a geometric yet friendly voice that fills the frame with confidence.</p>
        </div>
      </div>
    </div>
    <div class="neo-shape"></div>
    <div class="row">
      <div class="col-6">
        <div class="neo-card pink-border">
          <div class="card-icon">◉</div>
          <h2>--color-primary: #ff006e</h2>
          <p>Hot pink is the anchor color. It appears in borders, badges, hover shadows, and CTA buttons. The color system is deliberately maximalist.</p>
          <p class="mt-md" style="font-family: var(--font-heading); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--color-primary);">Usage: borders, badges, CTAs</p>
        </div>
      </div>
      <div class="col-6">
        <div class="neo-card accent-border">
          <div class="card-icon">✦</div>
          <h2>--color-accent: #ffbe0b</h2>
          <p>Bright yellow provides high-contrast accents — footer borders, decorative shapes, secondary badges. It sits opposite pink on the color wheel for maximum tension.</p>
          <p class="mt-md" style="font-family: var(--font-heading); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--color-accent);">Usage: footer, shapes, badges</p>
        </div>
      </div>
    </div>
    <div class="row mt-xl">
      <div class="col-12 flex justify-center gap-md">
        <span class="neo-cta">Get Started</span>
        <span class="neo-cta secondary">Learn More</span>
        <span class="neo-cta accent">Explore</span>
      </div>
    </div>
    <footer class="neo-footer">
      <div class="row">
        <div class="col-6">
          Neo-Brutalist Template &mdash; Aesthetic Style Composer v2
        </div>
        <div class="col-6 text-right">
          Loud &amp; Proud &mdash; &copy; 2026
        </div>
      </div>
    </footer>
  </div>
</body>
</html>
```
decision-guide.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aesthetic Decision Guide — Style Composer v2</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../stylesheets/stylesheet.css">
  <style>
    :root {
      --color-primary: #2563eb;
      --color-secondary: #7c3aed;
      --color-bg: #ffffff;
      --color-surface: #f8fafc;
      --color-text: #0f172a;
      --color-text-muted: #64748b;
      --color-border: #e2e8f0;
      --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
      --font-heading: 'Inter', system-ui, -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
      --grid-gap: 1.5rem;
    }
    .dg-header {
      padding: var(--spacing-xxl) 0 var(--spacing-xl);
      border-bottom: 3px solid var(--color-primary);
      margin-bottom: var(--spacing-xxl);
    }
    .dg-header h1 {
      font-family: var(--font-heading);
      font-size: 2.5rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      line-height: 1.1;
      color: var(--color-text);
    }
    .dg-header .subtitle {
      font-family: var(--font-sans);
      font-size: 1rem;
      color: var(--color-text-muted);
      margin-top: var(--spacing-sm);
    }
    .dg-section-title {
      font-family: var(--font-heading);
      font-size: 1.125rem;
      font-weight: 600;
      color: var(--color-text);
      margin-bottom: var(--spacing-md);
      padding-bottom: var(--spacing-xs);
      border-bottom: 2px solid var(--color-primary);
    }
    .dg-card {
      background: var(--color-surface);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-md);
      padding: var(--spacing-lg);
      margin-bottom: var(--spacing-md);
      transition: box-shadow 0.2s;
    }
    .dg-card:hover {
      box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    .dg-card h3 {
      font-family: var(--font-heading);
      font-size: 1rem;
      font-weight: 600;
      margin-bottom: var(--spacing-xs);
    }
    .dg-card p {
      font-family: var(--font-sans);
      font-size: 0.875rem;
      color: var(--color-text-muted);
      line-height: 1.6;
    }
    .dg-card .style-badge {
      display: inline-block;
      font-size: 0.6875rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 0.2rem 0.6rem;
      border-radius: var(--radius-sm);
      margin-top: var(--spacing-sm);
    }
    .badge-swiss { background: #da291c; color: #fff; }
    .badge-minimal { background: #1a1a1a; color: #fff; }
    .badge-brutalist { background: #000; color: #fff; }
    .badge-glass { background: #0071e3; color: #fff; }
    .badge-neo { background: #ff006e; color: #fff; }
    .dg-matrix {
      width: 100%;
      border-collapse: collapse;
      font-family: var(--font-sans);
      font-size: 0.8125rem;
      margin-bottom: var(--spacing-xl);
    }
    .dg-matrix th {
      background: var(--color-primary);
      color: #fff;
      font-weight: 600;
      text-align: left;
      padding: var(--spacing-sm) var(--spacing-md);
      border: 1px solid var(--color-border);
    }
    .dg-matrix td {
      padding: var(--spacing-sm) var(--spacing-md);
      border: 1px solid var(--color-border);
      vertical-align: top;
    }
    .dg-matrix tr:nth-child(even) td {
      background: var(--color-surface);
    }
    .dg-matrix .check { color: #16a34a; font-weight: 700; }
    .dg-matrix .cross { color: #dc2626; }
    .dg-matrix .partial { color: #d97706; }
    .dg-token-ref {
      background: var(--color-surface);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-md);
      padding: var(--spacing-lg);
      margin-bottom: var(--spacing-lg);
    }
    .dg-token-ref h3 {
      font-family: var(--font-heading);
      font-size: 0.9375rem;
      font-weight: 600;
      margin-bottom: var(--spacing-sm);
    }
    .dg-token-ref code {
      font-family: var(--font-mono);
      font-size: 0.8125rem;
      background: #f1f5f9;
      padding: 0.125rem 0.375rem;
      border-radius: 3px;
      color: var(--color-primary);
    }
    .dg-token-ref .ref-table {
      width: 100%;
      font-size: 0.8125rem;
      margin-top: var(--spacing-sm);
    }
    .dg-token-ref .ref-table td {
      padding: var(--spacing-xs) var(--spacing-sm);
      border-bottom: 1px solid var(--color-border);
    }
    .dg-token-ref .ref-table td:first-child {
      font-family: var(--font-mono);
      font-size: 0.75rem;
      color: var(--color-primary);
      width: 30%;
    }
    .dg-composition {
      margin-top: var(--spacing-xxl);
    }
    .dg-composition h2 {
      font-family: var(--font-heading);
      font-size: 1.25rem;
      font-weight: 600;
      margin-bottom: var(--spacing-md);
    }
    .dg-stack {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }
    .dg-stack .layer {
      font-family: var(--font-mono);
      font-size: 0.75rem;
      padding: var(--spacing-sm) var(--spacing-md);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-sm);
      background: var(--color-surface);
    }
    .layer-swiss { border-left: 4px solid #da291c; }
    .layer-minimal { border-left: 4px solid #1a1a1a; }
    .layer-brutalist { border-left: 4px solid #000; }
    .layer-glass { border-left: 4px solid #0071e3; }
    .layer-neo { border-left: 4px solid #ff006e; }
    .dg-footer {
      margin-top: var(--spacing-xxl);
      padding: var(--spacing-lg) 0;
      border-top: 1px solid var(--color-border);
      font-family: var(--font-sans);
      font-size: 0.8125rem;
      color: var(--color-text-muted);
    }
  </style>
</head>
<body>
  <div class="container">
    <header class="dg-header">
      <h1>Aesthetic Decision Guide</h1>
      <div class="subtitle">A matrix mapping use-cases to recommended visual styles from the Aesthetic Style Composer v2 library.</div>
    </header>
    <h2 class="dg-section-title">Use-Case to Style Matrix</h2>
    <table class="dg-matrix">
      <thead>
        <tr>
          <th>Use Case</th>
          <th>Swiss</th>
          <th>Minimal</th>
          <th>Brutalist</th>
          <th>Glass</th>
          <th>Neo-Brutalist</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Corporate / Enterprise</strong></td>
          <td><span class="check">&#10003;</span></td>
          <td><span class="check">&#10003;</span></td>
          <td class="cross">&mdash;</td>
          <td><span class="check">&#10003;</span></td>
          <td class="cross">&mdash;</td>
        </tr>
        <tr>
          <td><strong>Portfolio / Agency</strong></td>
          <td><span class="check">&#10003;</span></td>
          <td><span class="check">&#10003;</span></td>
          <td class="partial">&#9679;</td>
          <td><span class="check">&#10003;</span></td>
          <td><span class="check">&#10003;</span></td>
        </tr>
        <tr>
          <td><strong>Editorial / Publishing</strong></td>
          <td><span class="check">&#10003;</span></td>
          <td class="partial">&#9679;</td>
          <td class="partial">&#9679;</td>
          <td class="cross">&mdash;</td>
          <td class="cross">&mdash;</td>
        </tr>
        <tr>
          <td><strong>E-Commerce / Retail</strong></td>
          <td class="partial">&#9679;</td>
          <td><span class="check">&#10003;</span></td>
          <td class="cross">&mdash;</td>
          <td><span class="check">&#10003;</span></td>
          <td class="partial">&#9679;</td>
        </tr>
        <tr>
          <td><strong>Creative / Arts</strong></td>
          <td class="partial">&#9679;</td>
          <td class="partial">&#9679;</td>
          <td><span class="check">&#10003;</span></td>
          <td><span class="check">&#10003;</span></td>
          <td><span class="check">&#10003;</span></td>
        </tr>
        <tr>
          <td><strong>Developer Tools / API Docs</strong></td>
          <td class="cross">&mdash;</td>
          <td><span class="check">&#10003;</span></td>
          <td><span class="check">&#10003;</span></td>
          <td class="cross">&mdash;</td>
          <td class="cross">&mdash;</td>
        </tr>
        <tr>
          <td><strong>SaaS / Dashboard</strong></td>
          <td class="partial">&#9679;</td>
          <td><span class="check">&#10003;</span></td>
          <td class="cross">&mdash;</td>
          <td><span class="check">&#10003;</span></td>
          <td class="cross">&mdash;</td>
        </tr>
        <tr>
          <td><strong>Personal / Blog</strong></td>
          <td class="partial">&#9679;</td>
          <td><span class="check">&#10003;</span></td>
          <td class="partial">&#9679;</td>
          <td class="partial">&#9679;</td>
          <td><span class="check">&#10003;</span></td>
        </tr>
        <tr>
          <td><strong>Mobile App Landing</strong></td>
          <td class="cross">&mdash;</td>
          <td><span class="check">&#10003;</span></td>
          <td class="cross">&mdash;</td>
          <td><span class="check">&#10003;</span></td>
          <td class="partial">&#9679;</td>
        </tr>
        <tr>
          <td><strong>Event / Conference</strong></td>
          <td><span class="check">&#10003;</span></td>
          <td class="partial">&#9679;</td>
          <td><span class="check">&#10003;</span></td>
          <td class="partial">&#9679;</td>
          <td><span class="check">&#10003;</span></td>
        </tr>
      </tbody>
    </table>
    <h2 class="dg-section-title">Style Profiles</h2>
    <div class="row">
      <div class="col-4">
        <div class="dg-card">
          <h3>Swiss International Style</h3>
          <p>Asymmetric grids, Akzidenz-Grotesk and Helvetica pairings, red accent on off-white, strict mathematical proportion, uppercase headers, signal color.</p>
          <span class="style-badge badge-swiss">Swiss</span>
        </div>
      </div>
      <div class="col-4">
        <div class="dg-card">
          <h3>Minimal (Rams-inspired)</h3>
          <p>Maximal whitespace, restrained neutral palette, three-color maximum, Inter typeface, generous vertical rhythm, Dieter Rams philosophy.</p>
          <span class="style-badge badge-minimal">Minimal</span>
        </div>
      </div>
      <div class="col-4">
        <div class="dg-card">
          <h3>Brutalist</h3>
          <p>Monochrome, heavy black borders, exposed structure, zero border-radius, IBM Plex Mono, raw grid, concrete aesthetic, manifesto tone.</p>
          <span class="style-badge badge-brutalist">Brutalist</span>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-6">
        <div class="dg-card">
          <h3>Glassmorphism</h3>
          <p>Frosted glass surfaces, backdrop-filter blur (20-30px), layered depth with ambient radial gradients, SF Pro typeface, Apple-inspired, dark background, 24px corner radius.</p>
          <span class="style-badge badge-glass">Glass</span>
        </div>
      </div>
      <div class="col-6">
        <div class="dg-card">
          <h3>Neo-Brutalist</h3>
          <p>Hot pink / purple / yellow palette, 5rem oversize type, playful geometric accents (rotating sun emoji, diagonal stripe patterns), heavy borders, hover shadow offsets, Space Grotesk, CTA buttons with transform.</p>
          <span class="style-badge badge-neo">Neo-Brutalist</span>
        </div>
      </div>
    </div>
    <h2 class="dg-section-title">Shared Token Reference</h2>
    <p style="font-family: var(--font-sans); font-size: 0.875rem; color: var(--color-text-muted); margin-bottom: var(--spacing-md);">All five templates @import stylesheet.css and override these core tokens in their per-template &lt;style&gt; block. Below is the cross-template token map.</p>
    <div class="row">
      <div class="col-6">
        <div class="dg-token-ref">
          <h3><code>--color-primary</code> Across Styles</h3>
          <table class="ref-table">
            <tr><td>Swiss</td><td>#da291c (Signal Red)</td></tr>
            <tr><td>Minimal</td><td>#1a1a1a (Near-Black)</td></tr>
            <tr><td>Brutalist</td><td>#000000 (Pure Black)</td></tr>
            <tr><td>Glass</td><td>#0071e3 (Apple Blue)</td></tr>
            <tr><td>Neo-Brutalist</td><td>#ff006e (Hot Pink)</td></tr>
          </table>
        </div>
      </div>
      <div class="col-6">
        <div class="dg-token-ref">
          <h3><code>--font-heading</code> Across Styles</h3>
          <table class="ref-table">
            <tr><td>Swiss</td><td>Inter / Akzidenz-Grotesk / Helvetica</td></tr>
            <tr><td>Minimal</td><td>Inter</td></tr>
            <tr><td>Brutalist</td><td>IBM Plex Mono (monospace)</td></tr>
            <tr><td>Glass</td><td>SF Pro Display</td></tr>
            <tr><td>Neo-Brutalist</td><td>Space Grotesk</td></tr>
          </table>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-6">
        <div class="dg-token-ref">
          <h3><code>--color-bg</code> Across Styles</h3>
          <table class="ref-table">
            <tr><td>Swiss</td><td>#f5f5f5 (Warm Off-White)</td></tr>
            <tr><td>Minimal</td><td>#fafafa (Cool Off-White)</td></tr>
            <tr><td>Brutalist</td><td>#ffffff (Pure White)</td></tr>
            <tr><td>Glass</td><td>#0a0a0f (Near-Black)</td></tr>
            <tr><td>Neo-Brutalist</td><td>#f8f9fa (Neutral White)</td></tr>
          </table>
        </div>
      </div>
      <div class="col-6">
        <div class="dg-token-ref">
          <h3><code>--radius-md</code> Across Styles</h3>
          <table class="ref-table">
            <tr><td>Swiss</td><td>8px (moderate)</td></tr>
            <tr><td>Minimal</td><td>8px (moderate)</td></tr>
            <tr><td>Brutalist</td><td>0 (sharp / structural)</td></tr>
            <tr><td>Glass</td><td>16px (generous)</td></tr>
            <tr><td>Neo-Brutalist</td><td>0 (playfully sharp)</td></tr>
          </table>
        </div>
      </div>
    </div>
    <div class="dg-composition">
      <h2>Composition &amp; Stacking Order</h2>
      <div class="row">
        <div class="col-6">
          <div class="dg-token-ref">
            <h3>Grid System Relationship</h3>
            <p style="font-family: var(--font-sans); font-size: 0.8125rem; color: var(--color-text-muted); margin-top: var(--spacing-sm);">All templates share the 12-column <code>.container</code> / <code>.row</code> / <code>.col-*</code> grid from stylesheet.css. Swiss additionally defines its own 6-column <code>.swiss-grid</code> for asymmetric layouts, while Minimal, Brutalist, Glass, and Neo-Brutalist rely exclusively on the shared grid.</p>
          </div>
        </div>
        <div class="col-6">
          <div class="dg-token-ref">
            <h3>Responsive Modifier Chain</h3>
            <p style="font-family: var(--font-sans); font-size: 0.8125rem; color: var(--color-text-muted); margin-top: var(--spacing-sm);">The shared <code>.show-*</code> / <code>.hide-*</code> classes (stylesheet.css) work across all templates. Each template's per-style media queries refine its own layout at <code>768px</code> and <code>480px</code> breakpoints, but the show/hide modifiers remain consistent regardless of active style.</p>
          </div>
        </div>
      </div>
      <div class="dg-token-ref">
        <h3>Style Stacking (Multi-Style Composite Page)</h3>
        <p style="font-family: var(--font-sans); font-size: 0.8125rem; color: var(--color-text-muted); margin-top: var(--spacing-sm);">When compositing multiple styles on one page, apply each style's class names to their respective sections. The stacking priority is:</p>
        <div class="dg-stack mt-md">
          <div class="layer layer-neo">Z-index 5 : Neo-Brutalist (most visually assertive — playful shapes, bright colors)</div>
          <div class="layer layer-glass">Z-index 4 : Glass (transparency layers, backdrop blur — must render above solid backgrounds)</div>
          <div class="layer layer-brutalist">Z-index 3 : Brutalist (heavy borders, monochrome — acts as structural frame)</div>
          <div class="layer layer-minimal">Z-index 2 : Minimal (whitespace buffer, neutral bridge between loud styles)</div>
          <div class="layer layer-swiss">Z-index 1 : Swiss (foundational grid — all other styles can reference its column structure)</div>
        </div>
      </div>
    </div>
    <footer class="dg-footer">
      <div class="row">
        <div class="col-6">
          Aesthetic Decision Guide &mdash; Aesthetic Style Composer v2
        </div>
        <div class="col-6 text-right">
          &copy; 2026 &mdash; Design System Reference
        </div>
      </div>
    </footer>
  </div>
</body>
</html>
```
---
VERIFICATION REPORT
Manifest checklist passed:
- [x] manifest.json    — file listed, dependency graph complete, shared tokens enumerated
- [x] stylesheet.css   — reset, grid system, utilities, responsive modifiers, spacing helpers
- [x] swiss.html       — 6-column asymmetric grid, Akzidenz-Grotesk/Helvetica pairings, red accent, footer present
- [x] minimal.html     — Rams principles, 3-color palette, Inter, generous whitespace, footer present
- [x] brutalist.html   — heavy black borders, IBM Plex Mono, monochrome, zero radius, footer present
- [x] glass.html       --backdrop-filter blur, radial gradients, dark bg, frosted cards, footer present
- [x] neo-brutalist.html — hot pink/purple/yellow, 5rem type, playful geometry, hover shadows, footer present
- [x] decision-guide.html — use-case matrix, style profiles, shared token reference, stacking order
Tag balance: verified each file ends with </html> and all <style>, </style>, <head>, </head>, <body>, </body> pairs are closed.
var(--) audit: every var() reference in each template is defined either in the template's :root block or in stylesheet.css :root. Zero undefined references.
Style duplication: zero duplicated CSS across templates. All shared boilerplate (reset, grid, utilities, responsive hide/show, spacing, borders, flex helpers) lives exclusively in stylesheet.css. Each template @imports stylesheet.css and only adds its own aesthetic-specific overrides.