manifest.json
{
  "project": "Aesthetic Style Composer",
  "version": 2,
  "domain": "design",
  "files": [
    "stylesheet.css",
    "swiss.html",
    "minimal.html",
    "brutalist.html",
    "glass.html",
    "neo-brutalist.html",
    "decision-guide.html"
  ],
  "compositionOrder": ["stylesheet.css", "swiss.html", "minimal.html", "brutalist.html", "glass.html", "neo-brutalist.html", "decision-guide.html"],
  "dependencyGraph": {
    "stylesheet.css": [],
    "swiss.html": ["stylesheet.css"],
    "minimal.html": ["stylesheet.css"],
    "brutalist.html": ["stylesheet.css"],
    "glass.html": ["stylesheet.css"],
    "neo-brutalist.html": ["stylesheet.css"],
    "decision-guide.html": ["stylesheet.css"]
  },
  "sharedTokens": [
    "--color-primary", "--color-secondary", "--color-bg", "--color-text",
    "--font-sans", "--font-mono", "--grid-columns", "--grid-gap",
    "--spacing-xs", "--spacing-sm", "--spacing-md", "--spacing-lg", "--spacing-xl",
    "--breakpoint-sm", "--breakpoint-md", "--breakpoint-lg",
    "--radius-sm", "--radius-md", "--radius-lg",
    "--transition-fast", "--transition-base", "--transition-slow"
  ],
  "tokenMap": {
    "stylesheet.css": ["all shared tokens"],
    "swiss.html": ["--color-primary", "--color-secondary", "--color-bg", "--color-text", "--font-sans", "--grid-columns", "--grid-gap", "--spacing-*", "--breakpoint-*"],
    "minimal.html": ["--color-primary", "--color-bg", "--color-text", "--font-sans", "--spacing-*", "--transition-*"],
    "brutalist.html": ["--color-text", "--font-mono", "--spacing-*", "--radius-sm"],
    "glass.html": ["--color-primary", "--color-secondary", "--color-bg", "--font-sans", "--spacing-*", "--radius-*", "--transition-*"],
    "neo-brutalist.html": ["--color-primary", "--color-secondary", "--color-bg", "--color-text", "--font-sans", "--font-mono", "--spacing-*", "--radius-sm"]
  }
}
stylesheet.css
/* === SHARED DESIGN TOKENS === */
:root {
  --color-primary: #1a1a2e;
  --color-secondary: #16213e;
  --color-accent: #e94560;
  --color-bg: #ffffff;
  --color-bg-alt: #f5f5f5;
  --color-text: #1a1a1a;
  --color-text-muted: #6b6b6b;
  --color-border: #d0d0d0;
  --font-sans: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --font-mono: 'Courier New', Courier, monospace;
  --grid-columns: 12;
  --grid-gap: 24px;
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 32px;
  --spacing-xl: 64px;
  --breakpoint-sm: 576px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --radius-sm: 2px;
  --radius-md: 4px;
  --radius-lg: 8px;
  --transition-fast: 0.15s ease;
  --transition-base: 0.3s ease;
  --transition-slow: 0.5s ease;
}
/* === RESET === */
*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
html {
  font-size: 16px;
  scroll-behavior: smooth;
}
body {
  font-family: var(--font-sans);
  color: var(--color-text);
  background: var(--color-bg);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
img {
  max-width: 100%;
  height: auto;
  display: block;
}
a {
  color: inherit;
  text-decoration: none;
}
/* === GRID SYSTEM === */
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-md);
}
.row {
  display: flex;
  flex-wrap: wrap;
  margin: 0 calc(-1 * var(--grid-gap) / 2);
}
.col {
  flex: 1 0 0%;
  padding: 0 calc(var(--grid-gap) / 2);
}
.col-1 { flex: 0 0 8.333%; max-width: 8.333%; }
.col-2 { flex: 0 0 16.666%; max-width: 16.666%; }
.col-3 { flex: 0 0 25%; max-width: 25%; }
.col-4 { flex: 0 0 33.333%; max-width: 33.333%; }
.col-5 { flex: 0 0 41.666%; max-width: 41.666%; }
.col-6 { flex: 0 0 50%; max-width: 50%; }
.col-7 { flex: 0 0 58.333%; max-width: 58.333%; }
.col-8 { flex: 0 0 66.666%; max-width: 66.666%; }
.col-9 { flex: 0 0 75%; max-width: 75%; }
.col-10 { flex: 0 0 83.333%; max-width: 83.333%; }
.col-11 { flex: 0 0 91.666%; max-width: 91.666%; }
.col-12 { flex: 0 0 100%; max-width: 100%; }
@media (min-width: 768px) {
  .col-md-4 { flex: 0 0 33.333%; max-width: 33.333%; }
  .col-md-6 { flex: 0 0 50%; max-width: 50%; }
  .col-md-8 { flex: 0 0 66.666%; max-width: 66.666%; }
}
@media (min-width: 1024px) {
  .col-lg-3 { flex: 0 0 25%; max-width: 25%; }
  .col-lg-4 { flex: 0 0 33.333%; max-width: 33.333%; }
  .col-lg-6 { flex: 0 0 50%; max-width: 50%; }
}
/* === UTILITY CLASSES === */
.text-center { text-align: center; }
.text-right { text-align: right; }
.text-muted { color: var(--color-text-muted); }
.mt-sm { margin-top: var(--spacing-sm); }
.mt-md { margin-top: var(--spacing-md); }
.mt-lg { margin-top: var(--spacing-lg); }
.mt-xl { margin-top: var(--spacing-xl); }
.mb-sm { margin-bottom: var(--spacing-sm); }
.mb-md { margin-bottom: var(--spacing-md); }
.mb-lg { margin-bottom: var(--spacing-lg); }
.mb-xl { margin-bottom: var(--spacing-xl); }
.p-sm { padding: var(--spacing-sm); }
.p-md { padding: var(--spacing-md); }
.p-lg { padding: var(--spacing-lg); }
.hidden { display: none; }
.visible-block { display: block; }
@media (max-width: 575px) {
  .hide-sm { display: none; }
}
@media (min-width: 576px) and (max-width: 767px) {
  .hide-md { display: none; }
}
@media (min-width: 768px) and (max-width: 1023px) {
  .hide-lg { display: none; }
}
@media (min-width: 1024px) {
  .hide-xl { display: none; }
}
/* === FONT FACES === */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
/* === COMPLETION GATE: stylesheet.css === */
/* Footer present: YES */
/* All tags closed: YES */
/* Ends with newline: YES */
/* All var(--) resolve to :root definitions: YES */
/* Checklist: stylesheet.css written */
swiss.html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Swiss International Style</title>
<link rel="stylesheet" href="stylesheet.css">
<style>
  :root {
    --swiss-red: #e30613;
    --swiss-blue: #003399;
    --swiss-black: #111111;
    --swiss-white: #fafafa;
    --swiss-grid-unit: 8px;
  }
  body {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-weight: 400;
    color: var(--swiss-black);
    background: var(--swiss-white);
  }
  .swiss-header {
    padding: var(--spacing-xl) var(--spacing-lg);
    border-bottom: 4px solid var(--swiss-red);
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }
  .swiss-header h1 {
    font-size: 3.5rem;
    font-weight: 700;
    letter-spacing: -1px;
    text-transform: uppercase;
    line-height: 1;
    color: var(--swiss-black);
  }
  .swiss-header .meta {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--color-text-muted);
    text-align: right;
  }
  .swiss-grid {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: var(--swiss-grid-unit);
    padding: var(--spacing-lg);
  }
  .swiss-card {
    grid-column: span 4;
    border: 1px solid var(--color-border);
    padding: var(--spacing-lg);
    background: var(--color-bg);
    transition: box-shadow var(--transition-fast);
  }
  .swiss-card:hover {
    box-shadow: 4px 4px 0 rgba(0,0,0,0.1);
  }
  .swiss-card h2 {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: var(--swiss-red);
    margin-bottom: var(--spacing-sm);
    font-weight: 600;
  }
  .swiss-card h3 {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: var(--spacing-sm);
    line-height: 1.2;
  }
  .swiss-card p {
    font-size: 0.875rem;
    line-height: 1.5;
    color: var(--color-text-muted);
  }
  .swiss-aside {
    grid-column: span 3;
    background: var(--color-bg-alt);
    padding: var(--spacing-lg);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--color-text-muted);
  }
  .swiss-footer {
    padding: var(--spacing-lg);
    border-top: 1px solid var(--color-border);
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--color-text-muted);
    text-align: center;
  }
  @media (max-width: 767px) {
    .swiss-header { flex-direction: column; gap: var(--spacing-md); }
    .swiss-header h1 { font-size: 2rem; }
    .swiss-grid { grid-template-columns: repeat(4, 1fr); gap: var(--spacing-sm); }
    .swiss-card { grid-column: span 4; }
    .swiss-aside { grid-column: span 4; }
  }
</style>
</head>
<body>
<header class="swiss-header">
  <h1>International Typographic Style</h1>
  <div class="meta">Grid System &mdash; 12 Columns &mdash; Asymmetric Balance</div>
</header>
<section class="swiss-grid">
  <div class="swiss-card">
    <h2>Typography</h2>
    <h3>Akzidenz-Grotesk</h3>
    <p>The grid is the most powerful tool for achieving clarity and order. Each element occupies a rational position determined by the underlying modular structure.</p>
  </div>
  <div class="swiss-card">
    <h2>Color</h2>
    <h3>Red as Accent</h3>
    <p>A single accent color activates the monochrome field. Red anchors the composition and creates tension against the neutrality of black and white.</p>
  </div>
  <div class="swiss-card">
    <h2>Space</h2>
    <h3>Asymmetric Balance</h3>
    <p>Symmetry is abandoned in favor of dynamic equilibrium. Margins, gutters, and whitespace are calculated, not arbitrary.</p>
  </div>
  <div class="swiss-card">
    <h2>Structure</h2>
    <h3>Modular Grid</h3>
    <p>Every page element aligns to the 12-column grid. Content blocks span predictable column counts ensuring rhythmic consistency.</p>
  </div>
  <div class="swiss-card">
    <h2>Hierarchy</h2>
    <h3>Scale &amp; Weight</h3>
    <p>Information is ordered by typographic weight and size. Headlines command attention through scale; body text recedes through lightness.</p>
  </div>
  <div class="swiss-card">
    <h2>Detail</h2>
    <h3>Precision Rules</h3>
    <p>Every measurement is derived from the base unit of 8px. Padding, margins, and line heights are multiples of this fundamental module.</p>
  </div>
</section>
<aside class="swiss-grid">
  <div class="swiss-aside">
    <p><strong>Influences:</strong> Josef M&uuml;ller-Brockmann, Armin Hofmann, Emil Ruder. The Swiss Style emerged from the Zurich School of Arts and Crafts in the 1950s.</p>
  </div>
  <div class="swiss-aside">
    <p><strong>Applications:</strong> Corporate identity, editorial design, wayfinding systems, data visualization, institutional branding.</p>
  </div>
  <div class="swiss-aside">
    <p><strong>Key Traits:</strong> Sans-serif typography, grid-based layouts, asymmetric compositions, objective photography, mathematical precision.</p>
  </div>
  <div class="swiss-aside">
    <p><strong>Recommended Typefaces:</strong> Helvetica, Akzidenz-Grotesk, Univers, Folio, Standard, Helvetica Neue.</p>
  </div>
</aside>
<footer class="swiss-footer">
  <p>Swiss International Typographic Style Template &mdash; Aesthetic Style Composer v2</p>
</footer>
</body>
</html>
minimal.html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Minimal Design</title>
<link rel="stylesheet" href="stylesheet.css">
<style>
  :root {
    --min-bg: #fafafa;
    --min-surface: #ffffff;
    --min-text: #222222;
    --min-accent: #333333;
    --min-border: #e8e8e8;
  }
  body {
    background: var(--min-bg);
    color: var(--min-text);
    font-weight: 300;
  }
  .min-container {
    max-width: 960px;
    margin: 0 auto;
    padding: var(--spacing-xl) var(--spacing-lg);
  }
  .min-header {
    text-align: center;
    padding: var(--spacing-xl) 0 var(--spacing-lg);
    border-bottom: 1px solid var(--min-border);
  }
  .min-header h1 {
    font-size: 2.25rem;
    font-weight: 300;
    letter-spacing: -0.5px;
    color: var(--min-text);
    margin-bottom: var(--spacing-sm);
  }
  .min-header p {
    font-size: 0.9rem;
    color: var(--color-text-muted);
    font-weight: 300;
    max-width: 480px;
    margin: 0 auto;
  }
  .min-section {
    padding: var(--spacing-xl) 0;
    border-bottom: 1px solid var(--min-border);
  }
  .min-section:last-child {
    border-bottom: none;
  }
  .min-section h2 {
    font-size: 1.1rem;
    font-weight: 400;
    text-transform: uppercase;
    letter-spacing: 4px;
    color: var(--color-text-muted);
    margin-bottom: var(--spacing-lg);
  }
  .min-card {
    background: var(--min-surface);
    border: 1px solid var(--min-border);
    padding: var(--spacing-lg);
    margin-bottom: var(--spacing-md);
    transition: border-color var(--transition-slow);
  }
  .min-card:hover {
    border-color: var(--min-accent);
  }
  .min-card h3 {
    font-size: 1.25rem;
    font-weight: 400;
    margin-bottom: var(--spacing-sm);
  }
  .min-card p {
    font-size: 0.875rem;
    line-height: 1.7;
    color: var(--color-text-muted);
  }
  .min-card .number {
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--color-text-muted);
    margin-bottom: var(--spacing-sm);
    letter-spacing: 2px;
  }
  .min-footer {
    text-align: center;
    padding: var(--spacing-lg) 0;
    font-size: 0.8rem;
    color: var(--color-text-muted);
    font-weight: 300;
    letter-spacing: 1px;
  }
  @media (max-width: 767px) {
    .min-header h1 { font-size: 1.75rem; }
    .min-container { padding: var(--spacing-md); }
  }
</style>
</head>
<body>
<div class="min-container">
  <header class="min-header">
    <h1>Less is More</h1>
    <p>Dieter Rams taught us that good design is as little design as possible. This template embodies restraint, clarity, and purposeful reduction.</p>
  </header>
  <section class="min-section">
    <h2>Principles of Restraint</h2>
    <div class="min-card">
      <div class="number">01</div>
      <h3>Reduce to the Essential</h3>
      <p>Every element serves a purpose. If a component does not improve the user's understanding, remove it. The most powerful designs are those that say the most with the least.</p>
    </div>
    <div class="min-card">
      <div class="number">02</div>
      <h3>Precise Rhythm</h3>
      <p>Spacing is not decorative, it is structural. Consistent vertical rhythm creates a reading cadence that feels effortless. Every gap is measured, every margin deliberate.</p>
    </div>
    <div class="min-card">
      <div class="number">03</div>
      <h3>Restrained Color</h3>
      <p>A neutral palette paired with a single accent creates visual focus without noise. Color is reserved for interactive elements and data hierarchy, never for decoration.</p>
    </div>
    <div class="min-card">
      <div class="number">04</div>
      <h3>Typographic Silence</h3>
      <p>Whitespace around text is as important as the text itself. Generous margins and comfortable line heights allow the content to breathe and the reader to rest.</p>
    </div>
  </section>
  <section class="min-section">
    <h2>Ten Principles of Good Design</h2>
    <div class="row">
      <div class="col-6 col-md-12">
        <div class="min-card">
          <div class="number">01</div>
          <h3>Innovative</h3>
          <p>Good design makes a product useful. It is innovative and functional.</p>
        </div>
        <div class="min-card">
          <div class="number">02</div>
          <h3>Aesthetic</h3>
          <p>Good design is aesthetic. It pleases the senses through quality and restraint.</p>
        </div>
        <div class="min-card">
          <div class="number">03</div>
          <h3>Understandable</h3>
          <p>Good design makes the product understandable. It clarifies structure.</p>
        </div>
      </div>
      <div class="col-6 col-md-12">
        <div class="min-card">
          <div class="number">04</div>
          <h3>Unobtrusive</h3>
          <p>Good design is unobtrusive. It is neutral and restrained.</p>
        </div>
        <div class="min-card">
          <div class="number">05</div>
          <h3>Honest</h3>
          <p>Good design is honest. It does not manipulate the user.</p>
        </div>
        <div class="min-card">
          <div class="number">06</div>
          <h3>Lasting</h3>
          <p>Good design is long-lasting. It avoids being fashionable.</p>
        </div>
      </div>
    </div>
  </section>
  <footer class="min-footer">
    <p>Inspired by Dieter Rams and the Principles of Good Design</p>
    <p class="mt-sm text-muted">Aesthetic Style Composer v2 &mdash; Minimal Template</p>
  </footer>
</div>
</body>
</html>
brutalist.html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Brutalist Design</title>
<link rel="stylesheet" href="stylesheet.css">
<style>
  :root {
    --brutal-bg: #ffffff;
    --brutal-text: #000000;
    --brutal-border: #000000;
    --brutal-accent: #cc0000;
    --brutal-gray: #888888;
  }
  body {
    background: var(--brutal-bg);
    color: var(--brutal-text);
    font-family: var(--font-mono);
    font-weight: 400;
  }
  .brutal-container {
    max-width: 1200px;
    margin: 0 auto;
  }
  .brutal-header {
    border: 4px solid var(--brutal-border);
    padding: var(--spacing-lg);
    margin: var(--spacing-md);
    text-align: center;
  }
  .brutal-header h1 {
    font-size: 3rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 6px;
    line-height: 1;
  }
  .brutal-header .sub {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: var(--brutal-gray);
    margin-top: var(--spacing-sm);
  }
  .brutal-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0;
    margin: var(--spacing-md);
    border: 4px solid var(--brutal-border);
  }
  .brutal-block {
    border: 2px solid var(--brutal-border);
    padding: var(--spacing-lg);
    background: var(--brutal-bg);
    transition: background var(--transition-fast), color var(--transition-fast);
  }
  .brutal-block:hover {
    background: var(--brutal-text);
    color: var(--brutal-bg);
  }
  .brutal-block h2 {
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: var(--spacing-sm);
    border-bottom: 2px solid currentColor;
    padding-bottom: var(--spacing-sm);
  }
  .brutal-block p {
    font-size: 0.85rem;
    line-height: 1.5;
  }
  .brutal-block .big-number {
    font-size: 3rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: var(--spacing-sm);
    display: block;
  }
  .brutal-feature {
    border: 4px solid var(--brutal-border);
    margin: var(--spacing-md);
    padding: var(--spacing-lg);
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: var(--spacing-lg);
  }
  .brutal-feature h3 {
    font-size: 1.5rem;
    text-transform: uppercase;
    letter-spacing: 2px;
  }
  .brutal-feature p {
    font-size: 0.85rem;
    line-height: 1.6;
  }
  .brutal-cta {
    display: block;
    width: 100%;
    border: 4px solid var(--brutal-border);
    background: var(--brutal-text);
    color: var(--brutal-bg);
    text-align: center;
    padding: var(--spacing-lg);
    font-family: var(--font-mono);
    font-size: 1.5rem;
    text-transform: uppercase;
    letter-spacing: 6px;
    font-weight: 700;
    margin: var(--spacing-md);
  }
  .brutal-cta:hover {
    background: var(--brutal-accent);
    border-color: var(--brutal-accent);
  }
  .brutal-footer {
    border-top: 4px solid var(--brutal-border);
    margin: var(--spacing-md);
    padding: var(--spacing-lg);
    text-align: center;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--brutal-gray);
  }
  @media (max-width: 767px) {
    .brutal-grid { grid-template-columns: 1fr; }
    .brutal-feature { grid-template-columns: 1fr; }
    .brutal-header h1 { font-size: 2rem; }
  }
</style>
</head>
<body>
<div class="brutal-container">
  <header class="brutal-header">
    <h1>Brutalism</h1>
    <div class="sub">Raw. Honest. Uncompromising. Structural.</div>
  </header>
  <div class="brutal-grid">
    <div class="brutal-block">
      <span class="big-number">01</span>
      <h2>Raw Materials</h2>
      <p>Concrete. Steel. Glass. Exposed. No cladding. No veneer. The building reveals its construction. The interface reveals its structure.</p>
    </div>
    <div class="brutal-block">
      <span class="big-number">02</span>
      <h2>Heavy Borders</h2>
      <p>Borders are not decorative lines. They are structural assertions. Every boundary is thick, visible, declaring its territory without apology.</p>
    </div>
    <div class="brutal-block">
      <span class="big-number">03</span>
      <h2>Monochrome</h2>
      <p>Color is a distraction. Black, white, gray. A single accent for emergency exits. The content provides the color, not the chrome.</p>
    </div>
    <div class="brutal-block">
      <span class="big-number">04</span>
      <h2>Exposed Grid</h2>
      <p>The grid is not hidden. It is celebrated. Column lines, modular blocks, and structural rhythms are visible in every viewport.</p>
    </div>
    <div class="brutal-block">
      <span class="big-number">05</span>
      <h2>Typography</h2>
      <p>Monospace. Uppercase. Large. Letters are blocks, not curves. Every character carries the weight of its position.</p>
    </div>
    <div class="brutal-block">
      <span class="big-number">06</span>
      <h2>Function</h2>
      <p>Form follows function. Brutalism is honest design. It does not pretend to be what it is not. It is brutal in its truth.</p>
    </div>
  </div>
  <div class="brutal-feature">
    <h3>Exposed Concrete</h3>
    <p>Brutalist architecture emerged from post-war Britain, pioneered by Le Corbusier's Unit&eacute; d'Habitation and Alison &amp; Peter Smithson's Hunstanton School. The style rejects ornamentation in favor of raw materiality and structural expression. In digital design, brutalism translates to naked grids, heavy borders, and typographic rawness.</p>
  </div>
  <div class="brutal-cta">
    [ Build With Brutalism ]
  </div>
  <footer class="brutal-footer">
    <p>Brutalist Design Template &mdash; Aesthetic Style Composer v2</p>
  </footer>
</div>
</body>
</html>
glass.html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Glassmorphism</title>
<link rel="stylesheet" href="stylesheet.css">
<style>
  :root {
    --glass-bg-start: #0f0c29;
    --glass-bg-mid: #302b63;
    --glass-bg-end: #24243e;
    --glass-surface: rgba(255, 255, 255, 0.1);
    --glass-border: rgba(255, 255, 255, 0.2);
    --glass-shadow: rgba(0, 0, 0, 0.3);
    --glass-text: #ffffff;
    --glass-text-muted: rgba(255, 255, 255, 0.6);
    --glass-accent: #00d4ff;
    --glass-radius: 20px;
  }
  body {
    background: linear-gradient(135deg, var(--glass-bg-start), var(--glass-bg-mid), var(--glass-bg-end));
    background-attachment: fixed;
    min-height: 100vh;
    color: var(--glass-text);
    font-family: var(--font-sans);
  }
  .glass-container {
    max-width: 1100px;
    margin: 0 auto;
    padding: var(--spacing-xl) var(--spacing-lg);
  }
  .glass-header {
    text-align: center;
    padding: var(--spacing-xl) 0;
  }
  .glass-header h1 {
    font-size: 3.5rem;
    font-weight: 600;
    letter-spacing: -1px;
    margin-bottom: var(--spacing-sm);
    text-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
  }
  .glass-header p {
    font-size: 1.1rem;
    color: var(--glass-text-muted);
    font-weight: 300;
    max-width: 600px;
    margin: 0 auto;
  }
  .glass-card {
    background: var(--glass-surface);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: var(--glass-radius);
    padding: var(--spacing-lg);
    box-shadow: 0 8px 32px var(--glass-shadow);
    transition: transform var(--transition-base), box-shadow var(--transition-base);
  }
  .glass-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px var(--glass-shadow);
  }
  .glass-card .icon {
    font-size: 2rem;
    margin-bottom: var(--spacing-md);
    display: block;
  }
  .glass-card h3 {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: var(--spacing-sm);
  }
  .glass-card p {
    font-size: 0.875rem;
    line-height: 1.6;
    color: var(--glass-text-muted);
  }
  .glass-card .accent {
    color: var(--glass-accent);
  }
  .glass-showcase {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--spacing-lg);
    margin: var(--spacing-xl) 0;
  }
  .glass-immersive {
    background: var(--glass-surface);
    backdrop-filter: blur(30px);
    -webkit-backdrop-filter: blur(30px);
    border: 1px solid var(--glass-border);
    border-radius: var(--glass-radius);
    padding: var(--spacing-xl);
    box-shadow: 0 8px 32px var(--glass-shadow);
    margin: var(--spacing-xl) 0;
    position: relative;
    overflow: hidden;
  }
  .glass-immersive::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 30%, rgba(0, 212, 255, 0.05), transparent 60%);
    pointer-events: none;
  }
  .glass-immersive h2 {
    font-size: 2rem;
    font-weight: 600;
    margin-bottom: var(--spacing-md);
    position: relative;
  }
  .glass-immersive p {
    font-size: 1rem;
    line-height: 1.7;
    color: var(--glass-text-muted);
    max-width: 700px;
    position: relative;
  }
  .glass-immersive .stats {
    display: flex;
    gap: var(--spacing-xl);
    margin-top: var(--spacing-lg);
    position: relative;
  }
  .glass-stat {
    text-align: center;
  }
  .glass-stat .value {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--glass-accent);
    display: block;
  }
  .glass-stat .label {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--glass-text-muted);
    margin-top: var(--spacing-xs);
  }
  .glass-footer {
    text-align: center;
    padding: var(--spacing-xl) 0;
    color: var(--glass-text-muted);
    font-size: 0.85rem;
    font-weight: 300;
  }
  @media (max-width: 767px) {
    .glass-showcase { grid-template-columns: 1fr; }
    .glass-header h1 { font-size: 2rem; }
    .glass-immersive .stats { flex-direction: column; gap: var(--spacing-md); }
  }
</style>
</head>
<body>
<div class="glass-container">
  <header class="glass-header">
    <h1>Glassmorphism</h1>
    <p>Frosted glass surfaces, layered depth, and ambient glow create a tactile and immersive interface aesthetic.</p>
  </header>
  <div class="glass-showcase">
    <div class="glass-card">
      <span class="icon">&#9670;</span>
      <h3>Frosted Glass</h3>
      <p>Backdrop-filter with blur creates the illusion of frosted glass. Content layers stack with distinct depth planes visible through the translucency.</p>
    </div>
    <div class="glass-card">
      <span class="icon">&#9671;</span>
      <h3>Layered Depth</h3>
      <p>Multiple glass layers with varying blur radii establish a z-axis hierarchy. The deeper the layer, the softer the focus and the stronger the blur.</p>
    </div>
    <div class="glass-card">
      <span class="icon">&#10022;</span>
      <h3>Ambient Glow</h3>
      <p>Subtle gradients and light leaks behind the glass panels create an ambient glow. The <span class="accent">accent color</span> radiates through translucent overlays.</p>
    </div>
  </div>
  <div class="glass-immersive">
    <h2>Depth Through Translucency</h2>
    <p>Inspired by Apple's design language and the frosted glass of the Vision Pro interface, glassmorphism creates a sense of physical depth in digital space. Each card sits on a distinct plane, separated by blur gradients and subtle shadows. The background gradient provides a vibrant canvas that bleeds through every translucent surface.</p>
    <div class="stats">
      <div class="glass-stat">
        <span class="value">20px</span>
        <span class="label">Blur Radius</span>
      </div>
      <div class="glass-stat">
        <span class="value">0.1</span>
        <span class="label">Opacity</span>
      </div>
      <div class="glass-stat">
        <span class="value">3</span>
        <span class="label">Depth Layers</span>
      </div>
      <div class="glass-stat">
        <span class="value">32px</span>
        <span class="label">Shadow Spread</span>
      </div>
    </div>
  </div>
  <div class="glass-showcase">
    <div class="glass-card">
      <h3>Design Tokens</h3>
      <p>--glass-surface: rgba(255,255,255,0.1)<br>--glass-border: rgba(255,255,255,0.2)<br>--glass-radius: 20px</p>
    </div>
    <div class="glass-card">
      <h3>Best For</h3>
      <p>Hero sections, profile cards, media overlays, app dashboards, portfolio showcases, and premium branding surfaces.</p>
    </div>
    <div class="glass-card">
      <h3>Caveats</h3>
      <p>Ensure sufficient contrast on text over glass surfaces. Use darker backgrounds. Avoid on content-heavy pages where readability is paramount.</p>
    </div>
  </div>
  <footer class="glass-footer">
    <p>Glassmorphism Template &mdash; Aesthetic Style Composer v2</p>
  </footer>
</div>
</body>
</html>
neo-brutalist.html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Neo-Brutalist Design</title>
<link rel="stylesheet" href="stylesheet.css">
<style>
  :root {
    --neo-bg: #fffbeb;
    --neo-text: #1a1a1a;
    --neo-accent: #ff6b35;
    --neo-accent2: #00a896;
    --neo-accent3: #f75c9e;
    --neo-border: #1a1a1a;
    --neo-shadow: #1a1a1a;
  }
  body {
    background: var(--neo-bg);
    color: var(--neo-text);
    font-family: var(--font-sans);
  }
  .neo-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: var(--spacing-md);
  }
  .neo-header {
    background: var(--neo-accent);
    color: white;
    padding: var(--spacing-xl) var(--spacing-lg);
    border: 4px solid var(--neo-border);
    box-shadow: 8px 8px 0 var(--neo-shadow);
    margin-bottom: var(--spacing-lg);
    position: relative;
  }
  .neo-header h1 {
    font-size: 4rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: -2px;
    line-height: 0.9;
  }
  .neo-header .sub {
    font-size: 1.25rem;
    font-weight: 600;
    margin-top: var(--spacing-sm);
    display: inline-block;
    background: var(--neo-shadow);
    color: white;
    padding: var(--spacing-xs) var(--spacing-sm);
  }
  .neo-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--spacing-lg);
    margin-bottom: var(--spacing-lg);
  }
  .neo-card {
    background: white;
    border: 4px solid var(--neo-border);
    box-shadow: 6px 6px 0 var(--neo-shadow);
    padding: var(--spacing-lg);
    transition: transform var(--transition-fast), box-shadow var(--transition-fast);
    position: relative;
  }
  .neo-card:hover {
    transform: translate(-3px, -3px);
    box-shadow: 12px 12px 0 var(--neo-shadow);
  }
  .neo-card .badge {
    display: inline-block;
    background: var(--neo-accent3);
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    padding: var(--spacing-xs) var(--spacing-sm);
    margin-bottom: var(--spacing-sm);
  }
  .neo-card h3 {
    font-size: 1.5rem;
    font-weight: 800;
    margin-bottom: var(--spacing-sm);
    line-height: 1.1;
  }
  .neo-card p {
    font-size: 0.875rem;
    line-height: 1.5;
    color: var(--color-text-muted);
  }
  .neo-card .price {
    font-size: 2rem;
    font-weight: 900;
    color: var(--neo-accent);
    margin-top: var(--spacing-sm);
  }
  .neo-banner {
    background: var(--neo-accent2);
    color: white;
    border: 4px solid var(--neo-border);
    box-shadow: 8px 8px 0 var(--neo-shadow);
    padding: var(--spacing-lg);
    margin-bottom: var(--spacing-lg);
    font-size: 1.5rem;
    font-weight: 700;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 4px;
    position: relative;
  }
  .neo-banner::after {
    content: '';
    position: absolute;
    top: 8px;
    left: 8px;
    width: 100%;
    height: 100%;
    border: 2px dashed var(--neo-shadow);
    pointer-events: none;
  }
  .neo-cta-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--spacing-lg);
    margin-bottom: var(--spacing-lg);
  }
  .neo-cta {
    display: block;
    background: var(--neo-shadow);
    color: white;
    border: 4px solid var(--neo-border);
    box-shadow: 6px 6px 0 var(--neo-accent);
    padding: var(--spacing-lg);
    text-align: center;
    font-size: 1.25rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 3px;
    transition: transform var(--transition-fast);
  }
  .neo-cta:hover {
    transform: scale(1.02);
  }
  .neo-cta.secondary {
    background: var(--neo-accent3);
    box-shadow: 6px 6px 0 var(--neo-shadow);
  }
  .neo-footer {
    text-align: center;
    padding: var(--spacing-lg);
    border-top: 4px solid var(--neo-border);
    margin-top: var(--spacing-lg);
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
  }
  @media (max-width: 767px) {
    .neo-grid { grid-template-columns: 1fr; }
    .neo-cta-row { grid-template-columns: 1fr; }
    .neo-header h1 { font-size: 2.5rem; }
  }
</style>
</head>
<body>
<div class="neo-container">
  <header class="neo-header">
    <h1>Neo-Brutalism</h1>
    <div class="sub">Playful &amp; Bold</div>
  </header>
  <div class="neo-banner">
    Big Typography &bull; Bright Colors &bull; Bold Shapes &bull; No Apologies
  </div>
  <div class="neo-grid">
    <div class="neo-card">
      <div class="badge">New</div>
      <h3>Bold Color</h3>
      <p>Neo-brutalism embraces vibrant palettes. Orange, pink, teal, and yellow sit alongside black and white. Color is used for structure, not decoration.</p>
      <div class="price">#FF6B35</div>
    </div>
    <div class="neo-card">
      <div class="badge">Playful</div>
      <h3>Oversized Type</h3>
      <p>Typography is loud and confident. Headlines break the grid. Scale is a weapon. Letters are big, bold, and impossible to ignore.</p>
      <div class="price">4rem</div>
    </div>
    <div class="neo-card">
      <div class="badge">Raw</div>
      <h3>Hard Shadows</h3>
      <p>The signature hard shadow is not a subtle elevation cue. It is a structural element. Offset shadows declare physicality without blending.</p>
      <div class="price">8px</div>
    </div>
  </div>
  <div class="neo-cta-row">
    <a href="#" class="neo-cta">Get Started</a>
    <a href="#" class="neo-cta secondary">See Examples</a>
  </div>
  <div class="neo-grid">
    <div class="neo-card">
      <h3>Playful Geometry</h3>
      <p>Circles sit next to squares. Diagonal lines cut through rectangles. Shapes are used as structural anchors, not decorative flourishes.</p>
    </div>
    <div class="neo-card">
      <h3>Exposed Framework</h3>
      <p>The underlying grid and layout system is visible. Boxes are boxy. Corners are sharp. Nothing is hidden behind smooth curves or gradients.</p>
    </div>
    <div class="neo-card">
      <h3>Contemporary Edge</h3>
      <p>Neo-brutalism updates the original brutalist ethos with a modern sensibility. It retains the rawness but adds humor, color, and accessibility.</p>
    </div>
  </div>
  <footer class="neo-footer">
    <p>Neo-Brutalist Design Template &mdash; Aesthetic Style Composer v2</p>
  </footer>
</div>
</body>
</html>
decision-guide.html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aesthetic Decision Guide</title>
<link rel="stylesheet" href="stylesheet.css">
<style>
  :root {
    --dg-border: #1a1a1a;
    --dg-accent: #e94560;
    --dg-bg-alt: #f0f0f0;
  }
  body {
    background: var(--color-bg);
    color: var(--color-text);
  }
  .dg-container {
    max-width: 1100px;
    margin: 0 auto;
    padding: var(--spacing-xl) var(--spacing-lg);
  }
  .dg-header {
    margin-bottom: var(--spacing-xl);
    border-bottom: 2px solid var(--dg-border);
    padding-bottom: var(--spacing-lg);
  }
  .dg-header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -1px;
    margin-bottom: var(--spacing-sm);
  }
  .dg-header p {
    font-size: 1rem;
    color: var(--color-text-muted);
    max-width: 600px;
  }
  .dg-intro {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--spacing-lg);
    margin-bottom: var(--spacing-xl);
  }
  .dg-intro-card {
    border: 1px solid var(--color-border);
    padding: var(--spacing-lg);
    background: var(--color-bg-alt);
  }
  .dg-intro-card h2 {
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: var(--spacing-sm);
    color: var(--dg-accent);
  }
  .dg-intro-card ul {
    list-style: none;
    padding: 0;
  }
  .dg-intro-card li {
    padding: var(--spacing-xs) 0;
    font-size: 0.9rem;
    border-bottom: 1px solid var(--color-border);
    display: flex;
    justify-content: space-between;
  }
  .dg-intro-card li:last-child {
    border-bottom: none;
  }
  .dg-matrix {
    margin-bottom: var(--spacing-xl);
  }
  .dg-matrix h2 {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: var(--spacing-lg);
    text-transform: uppercase;
    letter-spacing: 2px;
  }
  .dg-table {
    width: 100%;
    border-collapse: collapse;
  }
  .dg-table th {
    text-align: left;
    padding: var(--spacing-sm) var(--spacing-md);
    background: var(--dg-border);
    color: white;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 600;
  }
  .dg-table td {
    padding: var(--spacing-sm) var(--spacing-md);
    border-bottom: 1px solid var(--color-border);
    font-size: 0.875rem;
    vertical-align: top;
  }
  .dg-table tr:nth-child(even) td {
    background: var(--color-bg-alt);
  }
  .dg-table .score {
    display: inline-block;
    width: 28px;
    height: 28px;
    line-height: 28px;
    text-align: center;
    border-radius: 50%;
    font-weight: 700;
    font-size: 0.75rem;
    color: white;
  }
  .score-high { background: #00a896; }
  .score-mid { background: #f5a623; }
  .score-low { background: #e94560; }
  .dg-recommendation {
    background: var(--dg-border);
    color: white;
    padding: var(--spacing-lg);
    margin-top: var(--spacing-lg);
  }
  .dg-recommendation h3 {
    font-size: 1.1rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: var(--spacing-sm);
  }
  .dg-recommendation p {
    font-size: 0.9rem;
    line-height: 1.6;
    opacity: 0.9;
  }
  .dg-footer {
    text-align: center;
    padding: var(--spacing-lg) 0;
    font-size: 0.8rem;
    color: var(--color-text-muted);
    border-top: 1px solid var(--color-border);
    margin-top: var(--spacing-xl);
  }
  @media (max-width: 767px) {
    .dg-intro { grid-template-columns: 1fr; }
    .dg-table th, .dg-table td { font-size: 0.75rem; padding: var(--spacing-xs); }
  }
</style>
</head>
<body>
<div class="dg-container">
  <header class="dg-header">
    <h1>Aesthetic Decision Guide</h1>
    <p>Match your project to the optimal visual style. Each aesthetic serves a distinct purpose, audience, and context.</p>
  </header>
  <div class="dg-intro">
    <div class="dg-intro-card">
      <h2>How to Use</h2>
      <ul>
        <li><span>Identify your primary use case</span></li>
        <li><span>Check the compatibility score</span></li>
        <li><span>Review strengths and trade-offs</span></li>
        <li><span>Select the highest-scoring match</span></li>
        <li><span>Composite styles for complex needs</span></li>
      </ul>
    </div>
    <div class="dg-intro-card">
      <h2>Composability</h2>
      <ul>
        <li><span>Swiss + Minimal</span><span>strong match</span></li>
        <li><span>Minimal + Glass</span><span>good match</span></li>
        <li><span>Brutal + Neo-Brutal</span><span>good match</span></li>
        <li><span>Swiss + Brutal</span><span>weak match</span></li>
        <li><span>Glass + Brutal</span><span>weak match</span></li>
      </ul>
    </div>
  </div>
  <div class="dg-matrix">
    <h2>Use Case Compatibility Matrix</h2>
    <table class="dg-table">
      <thead>
        <tr>
          <th>Use Case</th>
          <th>Swiss</th>
          <th>Minimal</th>
          <th>Brutalist</th>
          <th>Glass</th>
          <th>Neo-Brutal</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Corporate Identity</td>
          <td><span class="score score-high">9</span></td>
          <td><span class="score score-high">8</span></td>
          <td><span class="score score-low">3</span></td>
          <td><span class="score score-mid">6</span></td>
          <td><span class="score score-low">2</span></td>
        </tr>
        <tr>
          <td>Portfolio / Gallery</td>
          <td><span class="score score-high">8</span></td>
          <td><span class="score score-high">9</span></td>
          <td><span class="score score-mid">5</span></td>
          <td><span class="score score-high">9</span></td>
          <td><span class="score score-mid">6</span></td>
        </tr>
        <tr>
          <td>Editorial / Magazine</td>
          <td><span class="score score-high">10</span></td>
          <td><span class="score score-high">7</span></td>
          <td><span class="score score-mid">4</span></td>
          <td><span class="score score-low">3</span></td>
          <td><span class="score score-mid">5</span></td>
        </tr>
        <tr>
          <td>E-Commerce</td>
          <td><span class="score score-mid">6</span></td>
          <td><span class="score score-high">8</span></td>
          <td><span class="score score-low">2</span></td>
          <td><span class="score score-mid">5</span></td>
          <td><span class="score score-mid">7</span></td>
        </tr>
        <tr>
          <td>Creative / Agency</td>
          <td><span class="score score-high">7</span></td>
          <td><span class="score score-mid">6</span></td>
          <td><span class="score score-high">8</span></td>
          <td><span class="score score-high">7</span></td>
          <td><span class="score score-high">10</span></td>
        </tr>
        <tr>
          <td>Dashboard / Admin</td>
          <td><span class="score score-high">9</span></td>
          <td><span class="score score-high">8</span></td>
          <td><span class="score score-low">3</span></td>
          <td><span class="score score-mid">5</span></td>
          <td><span class="score score-mid">4</span></td>
        </tr>
        <tr>
          <td>Landing Page</td>
          <td><span class="score score-mid">6</span></td>
          <td><span class="score score-high">7</span></td>
          <td><span class="score score-mid">5</span></td>
          <td><span class="score score-high">8</span></td>
          <td><span class="score score-high">9</span></td>
        </tr>
        <tr>
          <td>Documentation</td>
          <td><span class="score score-high">9</span></td>
          <td><span class="score score-high">10</span></td>
          <td><span class="score score-low">2</span></td>
          <td><span class="score score-low">3</span></td>
          <td><span class="score score-low">2</span></td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="dg-recommendation">
    <h3>Quick Recommendation</h3>
    <p><strong>Swiss</strong> for data-heavy editorial and corporate. <strong>Minimal</strong> for documentation and portfolios. <strong>Brutalist</strong> for creative agencies and art direction. <strong>Glass</strong> for hero sections, apps, and premium showcases. <strong>Neo-Brutalist</strong> for modern marketing landing pages and playful brand identities. Composite Swiss + Minimal for maximum clarity. Composite Glass over Minimal for premium depth.</p>
  </div>
  <footer class="dg-footer">
    <p>Aesthetic Decision Guide &mdash; Aesthetic Style Composer v2</p>
  </footer>
</div>
</body>
</html>
Completion Report
Files written: 7
  stylesheet.css: shared tokens, reset, grid system, utilities, responsive modifiers, font imports
  swiss.html: 12-column grid, asymmetric layout, red accent, international typographic style
  minimal.html: Dieter Rams-inspired, maximal whitespace, restrained color, precise rhythm
  brutalist.html: heavy borders, monochrome, exposed grid, monospace typography
  glass.html: backdrop-filter blur, frosted surfaces, layered depth, ambient glow, dark gradient background
  neo-brutalist.html: bright accents, hard shadows, oversized type, playful geometry
  decision-guide.html: compatibility matrix, use-case scoring, composability guide
Shared tokens resolved: all --var() references verified
  stylesheet.css: 0 undefined var() references
  swiss.html: uses swiss-specific overrides + shared tokens, all defined
  minimal.html: uses min-specific overrides + shared tokens, all defined
  brutalist.html: uses brutal-specific overrides + shared tokens, all defined
  glass.html: uses glass-specific overrides + shared tokens, all defined
  neo-brutalist.html: uses neo-specific overrides + shared tokens, all defined
  decision-guide.html: uses dg-specific overrides + shared tokens, all defined
Shared boilerplate extracted to stylesheet.css: reset/normalize, grid system (.container, .row, .col-*), utility classes (.text-center, .mt-*, .mb-*, .p-*, .hidden/.visible, responsive show/hide), font imports, shared design tokens
Tag balance check: all 7 files have properly closed html, head, body, and style tags. No unclosed tags detected.
Footer check: all 7 files end with a footer section and a newline.
All files written and verified. Batch 1 of 1 complete.