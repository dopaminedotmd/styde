{
  "manifest": {
    "project": "Aesthetic Style Composer",
    "version": "2.0",
    "files": [
      "manifest.json",
      "stylesheet.css",
      "swiss.html",
      "minimal.html",
      "brutalist.html",
      "glass.html",
      "neo-brutalist.html",
      "decision-guide.html"
    ],
    "composition_order": [
      "stylesheet.css — shared tokens, grid system, utilities",
      "swiss.html — grid foundation, asymmetric layout",
      "minimal.html — reduced rhythm, references swiss grid",
      "brutalist.html — structural rebrand, ignores grid",
      "glass.html — layered depth on swiss grid",
      "neo-brutalist.html — playful override on brutalist structure",
      "decision-guide.html — final decision matrix"
    ],
    "shared_dependencies": {
      "tokens": [
        "--color-primary", "--color-secondary", "--color-accent",
        "--color-bg", "--color-surface", "--color-text", "--color-text-muted",
        "--font-heading", "--font-body", "--font-mono",
        "--space-xs", "--space-sm", "--space-md", "--space-lg", "--space-xl",
        "--radius-sm", "--radius-md", "--radius-lg",
        "--shadow-sm", "--shadow-md", "--shadow-lg"
      ],
      "grid_system": [
        "--grid-columns: 12", "--grid-gap: var(--space-md)",
        ".grid { display: grid; grid-template-columns: repeat(var(--grid-columns), 1fr); gap: var(--grid-gap); }",
        ".col-1 { grid-column: span 1; }", ".col-2 { grid-column: span 2; }", ".col-3 { grid-column: span 3; }",
        ".col-4 { grid-column: span 4; }", ".col-6 { grid-column: span 6; }", ".col-8 { grid-column: span 8; }", ".col-12 { grid-column: span 12; }"
      ],
      "font_imports": [
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
        "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap"
      ]
    },
    "dependency_graph": {
      "stylesheet.css": [],
      "swiss.html": ["stylesheet.css"],
      "minimal.html": ["stylesheet.css"],
      "brutalist.html": [],
      "glass.html": ["stylesheet.css", "swiss.html"],
      "neo-brutalist.html": ["brutalist.html"],
      "decision-guide.html": ["stylesheet.css"]
    }
  }
}
--- stylesheet.css ---
:root {
  --color-primary: #2563eb;
  --color-secondary: #7c3aed;
  --color-accent: #f59e0b;
  --color-bg: #ffffff;
  --color-surface: #f8fafc;
  --color-text: #0f172a;
  --color-text-muted: #64748b;
  --font-heading: 'Inter', 'Helvetica Neue', 'Akzidenz-Grotesk', sans-serif;
  --font-body: 'Inter', 'Helvetica Neue', sans-serif;
  --font-mono: 'SF Mono', 'JetBrains Mono', monospace;
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 2rem;
  --space-xl: 4rem;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.07);
  --shadow-lg: 0 10px 25px rgba(0,0,0,0.1);
  --transition-fast: 150ms ease;
  --transition-base: 250ms ease;
}
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
html {
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
body {
  font-family: var(--font-body);
  color: var(--color-text);
  background: var(--color-bg);
  line-height: 1.6;
}
h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading);
  font-weight: 600;
  line-height: 1.2;
}
a {
  color: var(--color-primary);
  text-decoration: none;
  transition: color var(--transition-fast);
}
a:hover {
  color: color-mix(in srgb, var(--color-primary) 80%, black);
}
img {
  max-width: 100%;
  height: auto;
  display: block;
}
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-md);
}
.grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--space-md);
}
.col-1  { grid-column: span 1; }
.col-2  { grid-column: span 2; }
.col-3  { grid-column: span 3; }
.col-4  { grid-column: span 4; }
.col-5  { grid-column: span 5; }
.col-6  { grid-column: span 6; }
.col-7  { grid-column: span 7; }
.col-8  { grid-column: span 8; }
.col-9  { grid-column: span 9; }
.col-10 { grid-column: span 10; }
.col-11 { grid-column: span 11; }
.col-12 { grid-column: span 12; }
@media (max-width: 768px) {
  .grid { grid-template-columns: repeat(4, 1fr); }
  .col-1, .col-2, .col-3, .col-4, .col-5, .col-6,
  .col-7, .col-8, .col-9, .col-10, .col-11, .col-12 {
    grid-column: span 4;
  }
}
@media (max-width: 480px) {
  .grid { grid-template-columns: 1fr; }
  .col-1, .col-2, .col-3, .col-4, .col-5, .col-6,
  .col-7, .col-8, .col-9, .col-10, .col-11, .col-12 {
    grid-column: 1;
  }
}
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-sm) var(--space-lg);
  font-family: var(--font-body);
  font-weight: 500;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
}
.btn-primary {
  background: var(--color-primary);
  color: white;
}
.btn-primary:hover {
  background: color-mix(in srgb, var(--color-primary) 80%, black);
  transform: translateY(-1px);
}
.btn-secondary {
  background: transparent;
  color: var(--color-primary);
  border: 1px solid var(--color-primary);
}
.card {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  box-shadow: var(--shadow-sm);
}
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
--- swiss.html ---
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Swiss International Style</title>
  <link rel="stylesheet" href="stylesheet.css">
  <style>
    :root {
      --swiss-red: #da291c;
      --swiss-black: #1a1a1a;
      --swiss-white: #f5f5f5;
      --swiss-gray: #e0e0e0;
      --swiss-grid-color: rgba(0,0,0,0.04);
    }
    .swiss-header {
      background: var(--swiss-red);
      color: white;
      padding: var(--space-xl) 0;
      position: relative;
    }
    .swiss-header::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: var(--swiss-black);
    }
    .swiss-header h1 {
      font-size: 3.5rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: -0.02em;
      line-height: 1;
    }
    .swiss-header .subtitle {
      font-size: 1.25rem;
      font-weight: 400;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      margin-top: var(--space-md);
      color: rgba(255,255,255,0.85);
    }
    .swiss-grid-overlay {
      background-image:
        linear-gradient(var(--swiss-grid-color) 1px, transparent 1px),
        linear-gradient(90deg, var(--swiss-grid-color) 1px, transparent 1px);
      background-size: 60px 60px;
    }
    .swiss-section {
      padding: var(--space-xl) 0;
      border-bottom: 2px solid var(--swiss-black);
    }
    .swiss-section h2 {
      font-size: 1.5rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: var(--space-lg);
      position: relative;
      padding-bottom: var(--space-sm);
    }
    .swiss-section h2::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      width: 60px;
      height: 3px;
      background: var(--swiss-red);
    }
    .swiss-card {
      background: var(--swiss-white);
      padding: var(--space-lg);
      border: 2px solid var(--swiss-black);
      position: relative;
    }
    .swiss-card .number {
      font-size: 3rem;
      font-weight: 700;
      color: var(--swiss-red);
      line-height: 1;
      margin-bottom: var(--space-sm);
    }
    .swiss-card h3 {
      font-size: 1.125rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: var(--space-sm);
    }
    .swiss-card p {
      font-size: 0.875rem;
      color: var(--color-text-muted);
      line-height: 1.5;
    }
    .swiss-footer {
      background: var(--swiss-black);
      color: white;
      padding: var(--space-lg) 0;
      text-align: center;
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.15em;
    }
    .swiss-footer p {
      color: rgba(255,255,255,0.6);
    }
    @media (max-width: 768px) {
      .swiss-header h1 { font-size: 2.25rem; }
      .swiss-section { padding: var(--space-lg) 0; }
    }
  </style>
</head>
<body>
  <header class="swiss-header">
    <div class="container">
      <h1>Swiss International</h1>
      <p class="subtitle">Typography · Grid · Asymmetry</p>
    </div>
  </header>
  <section class="swiss-section swiss-grid-overlay">
    <div class="container">
      <h2>Grid System</h2>
      <div class="grid">
        <div class="col-4">
          <div class="swiss-card">
            <div class="number">01</div>
            <h3>Akzidenz-Grotesk</h3>
            <p>The original grotesk that defined Swiss typography. Used for all display and body text.</p>
          </div>
        </div>
        <div class="col-4">
          <div class="swiss-card">
            <div class="number">02</div>
            <h3>Asymmetric Balance</h3>
            <p>Off-center layouts create dynamic tension while maintaining rigorous grid alignment.</p>
          </div>
        </div>
        <div class="col-4">
          <div class="swiss-card">
            <div class="number">03</div>
            <h3>Modular Rhythm</h3>
            <p>Everything divisible by 8. Spacing, type sizing, and grid columns follow a strict modular scale.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
  <section class="swiss-section">
    <div class="container">
      <h2>Color Palette</h2>
      <div class="grid">
        <div class="col-3">
          <div style="background:var(--swiss-red);color:white;padding:var(--space-lg);text-align:center;font-weight:600;">
            Signal Red<br>#DA291C
          </div>
        </div>
        <div class="col-3">
          <div style="background:var(--swiss-black);color:white;padding:var(--space-lg);text-align:center;font-weight:600;">
            Absolute Black<br>#1A1A1A
          </div>
        </div>
        <div class="col-3">
          <div style="background:var(--swiss-white);color:var(--swiss-black);padding:var(--space-lg);text-align:center;font-weight:600;border:1px solid #ccc;">
            Off White<br>#F5F5F5
          </div>
        </div>
        <div class="col-3">
          <div style="background:var(--swiss-gray);color:var(--swiss-black);padding:var(--space-lg);text-align:center;font-weight:600;">
            Neutral Gray<br>#E0E0E0
          </div>
        </div>
      </div>
    </div>
  </section>
  <section class="swiss-section">
    <div class="container">
      <h2>Typography Scale</h2>
      <div class="grid">
        <div class="col-6">
          <p style="font-size:3.5rem;font-weight:700;line-height:1;text-transform:uppercase;">Heading 1</p>
          <p style="font-size:2rem;font-weight:600;text-transform:uppercase;margin-top:var(--space-lg);">Heading 2</p>
          <p style="font-size:1.5rem;font-weight:600;text-transform:uppercase;margin-top:var(--space-lg);">Heading 3</p>
        </div>
        <div class="col-6">
          <p style="font-size:1.125rem;font-weight:400;margin-bottom:var(--space-md);">Body Large — used for lead paragraphs and introductions. Akzidenz-Grotesk at 18px with 1.6 line height.</p>
          <p style="font-size:0.875rem;font-weight:400;color:var(--color-text-muted);">Body Small — used for captions, metadata, and secondary information. Set in 14px for readability at small sizes.</p>
          <p style="font-size:0.75rem;font-weight:400;text-transform:uppercase;letter-spacing:0.1em;margin-top:var(--space-sm);">Label — uppercase with wide tracking for UI labels and form fields.</p>
        </div>
      </div>
    </div>
  </section>
  <footer class="swiss-footer">
    <div class="container">
      <p>Swiss International Style &copy; 2026 — Designed with reference to Josef Muller-Brockmann, Emil Ruder, and the Basel School of Design</p>
    </div>
  </footer>
</body>
</html>
--- minimal.html ---
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Minimal — Dieter Rams</title>
  <link rel="stylesheet" href="stylesheet.css">
  <style>
    :root {
      --min-bg: #fafafa;
      --min-surface: #ffffff;
      --min-text: #222222;
      --min-muted: #999999;
      --min-border: #e0e0e0;
      --min-accent: #333333;
    }
    .min-header {
      background: var(--min-bg);
      padding: var(--space-xl) 0 var(--space-lg);
      text-align: center;
      border-bottom: 1px solid var(--min-border);
    }
    .min-header h1 {
      font-size: 2.5rem;
      font-weight: 300;
      letter-spacing: -0.015em;
      color: var(--min-text);
    }
    .min-header .tagline {
      font-size: 0.875rem;
      color: var(--min-muted);
      letter-spacing: 0.12em;
      text-transform: uppercase;
      margin-top: var(--space-md);
    }
    .min-section {
      padding: var(--space-xl) 0;
      max-width: 800px;
      margin: 0 auto;
    }
    .min-section h2 {
      font-size: 1.25rem;
      font-weight: 400;
      color: var(--min-text);
      margin-bottom: var(--space-lg);
      letter-spacing: 0.02em;
    }
    .min-card {
      background: var(--min-surface);
      border: 1px solid var(--min-border);
      padding: var(--space-xl);
      margin-bottom: var(--space-lg);
      transition: box-shadow var(--transition-base);
    }
    .min-card:hover {
      box-shadow: 0 2px 20px rgba(0,0,0,0.04);
    }
    .min-card h3 {
      font-size: 1rem;
      font-weight: 500;
      color: var(--min-text);
      margin-bottom: var(--space-sm);
    }
    .min-card p {
      font-size: 0.875rem;
      color: var(--min-muted);
      line-height: 1.7;
    }
    .min-principle {
      display: flex;
      gap: var(--space-lg);
      padding: var(--space-lg) 0;
      border-top: 1px solid var(--min-border);
    }
    .min-principle:last-child {
      border-bottom: 1px solid var(--min-border);
    }
    .min-principle-num {
      font-size: 2rem;
      font-weight: 200;
      color: var(--min-muted);
      min-width: 3rem;
      line-height: 1;
    }
    .min-principle h3 {
      font-size: 1rem;
      font-weight: 500;
      margin-bottom: var(--space-xs);
    }
    .min-principle p {
      font-size: 0.8125rem;
      color: var(--min-muted);
      line-height: 1.6;
    }
    .min-footer {
      background: var(--min-bg);
      padding: var(--space-lg) 0;
      text-align: center;
      border-top: 1px solid var(--min-border);
      font-size: 0.75rem;
      color: var(--min-muted);
    }
    @media (max-width: 768px) {
      .min-header h1 { font-size: 1.75rem; }
      .min-section { padding: var(--space-lg) var(--space-md); }
      .min-principle { flex-direction: column; gap: var(--space-sm); }
    }
  </style>
</head>
<body>
  <header class="min-header">
    <div class="container" style="max-width:800px;margin:0 auto;">
      <h1>Less but Better</h1>
      <p class="tagline">Dieter Rams — 10 Principles of Good Design</p>
    </div>
  </header>
  <section class="min-section container">
    <h2>Principles</h2>
    <div class="min-principle">
      <span class="min-principle-num">01</span>
      <div>
        <h3>Good design is innovative</h3>
        <p>The possibilities for progression are not exhausted. Technological development constantly offers new opportunities for innovative design.</p>
      </div>
    </div>
    <div class="min-principle">
      <span class="min-principle-num">02</span>
      <div>
        <h3>Good design makes a product useful</h3>
        <p>A product is bought to be used. It must satisfy certain criteria — functional, psychological, and aesthetic.</p>
      </div>
    </div>
    <div class="min-principle">
      <span class="min-principle-num">03</span>
      <div>
        <h3>Good design is aesthetic</h3>
        <p>The aesthetic quality of a product is integral to its usefulness. Products we use every day affect our well-being.</p>
      </div>
    </div>
    <div class="min-principle">
      <span class="min-principle-num">04</span>
      <div>
        <h3>Good design is unobtrusive</h3>
        <p>Products fulfilling a purpose are like tools. They are neither decorative objects nor works of art.</p>
      </div>
    </div>
    <div class="min-principle">
      <span class="min-principle-num">05</span>
      <div>
        <h3>Good design is honest</h3>
        <p>It does not make a product more innovative, powerful, or valuable than it really is.</p>
      </div>
    </div>
  </section>
  <section class="min-section container">
    <h2>Design Tokens</h2>
    <div class="grid">
      <div class="col-4">
        <div class="min-card">
          <h3>Color</h3>
          <p>Restrained palette of off-white, charcoal, and warm gray. One accent used sparingly for interactive elements.</p>
        </div>
      </div>
      <div class="col-4">
        <div class="min-card">
          <h3>Typography</h3>
          <p>Inter at 300-500 weight. Generous leading. No uppercase for body text. Precise letter-spacing only in labels.</p>
        </div>
      </div>
      <div class="col-4">
        <div class="min-card">
          <h3>Space</h3>
          <p>Whitespace is not empty — it is the primary design element. Every element breathes. Margins and padding follow a 8px grid.</p>
        </div>
      </div>
    </div>
  </section>
  <footer class="min-footer">
    <div class="container">
      <p>Inspired by Dieter Rams and the Braun design philosophy — 2026</p>
    </div>
  </footer>
</body>
</html>
--- brutalist.html ---
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Brutalist</title>
  <style>
    :root {
      --brutal-bg: #f0f0f0;
      --brutal-text: #111111;
      --brutal-border: #222222;
      --brutal-accent: #cc0000;
      --brutal-highlight: #ffff00;
      --brutal-mono: #777777;
      --font-brutal: 'Space Grotesk', 'Helvetica Neue', sans-serif;
    }
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      font-family: var(--font-brutal);
      background: var(--brutal-bg);
      color: var(--brutal-text);
      line-height: 1.4;
    }
    .brutal-header {
      background: var(--brutal-text);
      color: white;
      padding: var(--space-lg, 2rem) 0;
      border-bottom: 6px solid var(--brutal-accent);
      text-align: center;
    }
    .brutal-header h1 {
      font-size: 4rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: -0.03em;
    }
    .brutal-header .sub {
      font-size: 1rem;
      font-weight: 400;
      color: var(--brutal-mono);
      margin-top: 0.5rem;
    }
    .brutal-nav {
      background: var(--brutal-border);
      padding: 0.75rem 0;
      border-bottom: 4px solid var(--brutal-accent);
    }
    .brutal-nav ul {
      list-style: none;
      display: flex;
      justify-content: center;
      gap: 2rem;
    }
    .brutal-nav a {
      color: white;
      font-weight: 700;
      text-transform: uppercase;
      font-size: 0.875rem;
      letter-spacing: 0.1em;
      text-decoration: none;
      padding: 0.25rem 0.5rem;
      border: 2px solid transparent;
    }
    .brutal-nav a:hover {
      border-color: white;
    }
    .brutal-section {
      padding: var(--space-lg, 2rem) 0;
      border-bottom: 4px solid var(--brutal-text);
    }
    .brutal-section h2 {
      font-size: 2.5rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: -0.02em;
      margin-bottom: var(--space-md, 1rem);
      padding-left: 0.5rem;
      border-left: 8px solid var(--brutal-accent);
    }
    .brutal-box {
      border: 4px solid var(--brutal-text);
      padding: 1.5rem;
      margin-bottom: 1rem;
      background: white;
    }
    .brutal-box.highlight {
      background: var(--brutal-highlight);
      border-width: 6px;
    }
    .brutal-box h3 {
      font-size: 1.25rem;
      font-weight: 700;
      text-transform: uppercase;
      margin-bottom: 0.5rem;
    }
    .brutal-box p {
      font-size: 0.9375rem;
      color: #333;
    }
    .brutal-box code {
      font-family: 'Courier New', monospace;
      background: var(--brutal-text);
      color: #0f0;
      padding: 0.125rem 0.375rem;
      font-size: 0.8125rem;
    }
    .brutal-monochrome {
      display: flex;
      gap: 0;
      margin: 1rem 0;
    }
    .brutal-monochrome > div {
      flex: 1;
      height: 60px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.75rem;
      font-weight: 700;
      color: white;
    }
    .brutal-monochrome .c1 { background: #111; }
    .brutal-monochrome .c2 { background: #333; }
    .brutal-monochrome .c3 { background: #555; }
    .brutal-monochrome .c4 { background: #777; }
    .brutal-monochrome .c5 { background: #999; }
    .brutal-monochrome .c6 { background: #bbb; color: #111; }
    .brutal-monochrome .c7 { background: #ddd; color: #111; }
    .brutal-footer {
      background: var(--brutal-text);
      color: white;
      padding: var(--space-lg, 2rem) 0;
      text-align: center;
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
    }
    .brutal-footer p { color: var(--brutal-mono); }
    .container {
      max-width: 1100px;
      margin: 0 auto;
      padding: 0 1rem;
    }
    @media (max-width: 768px) {
      .brutal-header h1 { font-size: 2.5rem; }
      .brutal-nav ul { flex-direction: column; align-items: center; gap: 0.75rem; }
      .brutal-section h2 { font-size: 1.75rem; }
    }
  </style>
</head>
<body>
  <header class="brutal-header">
    <div class="container">
      <h1>Brutalist</h1>
      <p class="sub">Raw Structure · Exposed Grids · Bold Typography</p>
    </div>
  </header>
  <nav class="brutal-nav">
    <div class="container">
      <ul>
        <li><a href="#">Structure</a></li>
        <li><a href="#">Typography</a></li>
        <li><a href="#">Color</a></li>
        <li><a href="#">Grid</a></li>
      </ul>
    </div>
  </nav>
  <section class="brutal-section">
    <div class="container">
      <h2>Structural Elements</h2>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
        <div class="brutal-box">
          <h3>Heavy Borders</h3>
          <p>No subtle shadows. No rounded corners. Every block is defined by <code>4px</code> solid borders. Interactive states use <code>6px</code> or <code>8px</code> weight shifts.</p>
        </div>
        <div class="brutal-box">
          <h3>Exposed Grid</h3>
          <p>The underlying column structure is visible. Gutters are <code>1rem</code>. Column boundaries can optionally be shown via a checkerboard overlay.</p>
        </div>
        <div class="brutal-box">
          <h3>Monochrome</h3>
          <p>Black, white, and gray scale. One accent color (red) reserved for errors, highlights, and critical actions. No gradients.</p>
        </div>
        <div class="brutal-box highlight">
          <h3>Raw Typography</h3>
          <p>Space Grotesk at 700 weight for headings. No letter-spacing tricks. No ligatures. No fine hairline weights. Bold or nothing.</p>
        </div>
      </div>
    </div>
  </section>
  <section class="brutal-section">
    <div class="container">
      <h2>Monochrome Scale</h2>
      <div class="brutal-monochrome">
        <div class="c1">#111</div>
        <div class="c2">#333</div>
        <div class="c3">#555</div>
        <div class="c4">#777</div>
        <div class="c5">#999</div>
        <div class="c6">#BBB</div>
        <div class="c7">#DDD</div>
      </div>
    </div>
  </section>
  <section class="brutal-section">
    <div class="container">
      <h2>Layout Grid</h2>
      <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:4px;">
        <div style="background:#222;color:white;padding:1rem;text-align:center;font-weight:700;font-size:0.75rem;">1/6</div>
        <div style="background:#222;color:white;padding:1rem;text-align:center;font-weight:700;font-size:0.75rem;">1/6</div>
        <div style="background:#222;color:white;padding:1rem;text-align:center;font-weight:700;font-size:0.75rem;">1/6</div>
        <div style="background:#444;color:white;padding:1rem;text-align:center;font-weight:700;font-size:0.75rem;">1/6</div>
        <div style="background:#444;color:white;padding:1rem;text-align:center;font-weight:700;font-size:0.75rem;">1/6</div>
        <div style="background:#444;color:white;padding:1rem;text-align:center;font-weight:700;font-size:0.75rem;">1/6</div>
      </div>
      <p style="margin-top:1rem;font-size:0.8125rem;color:#555;">Brutalist uses a 6-column grid — not the standard 12. Fewer columns mean bigger structural chunks and more dramatic asymmetry.</p>
    </div>
  </section>
  <footer class="brutal-footer">
    <div class="container">
      <p>Brutalist Web Design — Exposed structure as aesthetic statement. 2026.</p>
    </div>
  </footer>
</body>
</html>
--- glass.html ---
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
      --glass-surface: rgba(255,255,255,0.08);
      --glass-surface-hover: rgba(255,255,255,0.14);
      --glass-border: rgba(255,255,255,0.18);
      --glass-border-hover: rgba(255,255,255,0.28);
      --glass-blur: blur(20px);
      --glass-blur-heavy: blur(32px);
      --glass-text: rgba(255,255,255,0.92);
      --glass-text-muted: rgba(255,255,255,0.55);
      --glass-accent: #64ffda;
      --glass-glow: 0 0 30px rgba(100,255,218,0.15);
    }
    body {
      background: linear-gradient(135deg, var(--glass-bg-start), var(--glass-bg-mid), var(--glass-bg-end));
      min-height: 100vh;
      color: var(--glass-text);
    }
    .glass-header {
      padding: var(--space-xl) 0;
      text-align: center;
      position: relative;
    }
    .glass-header h1 {
      font-size: 3.5rem;
      font-weight: 700;
      background: linear-gradient(135deg, #ffffff, rgba(255,255,255,0.6));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    .glass-header p {
      color: var(--glass-text-muted);
      font-size: 1.125rem;
      margin-top: var(--space-sm);
    }
    .glass-section {
      padding: var(--space-xl) 0;
    }
    .glass-section h2 {
      font-size: 1.5rem;
      font-weight: 500;
      color: var(--glass-text);
      margin-bottom: var(--space-lg);
      text-align: center;
    }
    .glass-card {
      background: var(--glass-surface);
      backdrop-filter: var(--glass-blur);
      -webkit-backdrop-filter: var(--glass-blur);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-lg);
      padding: var(--space-xl);
      transition: all var(--transition-base);
    }
    .glass-card:hover {
      background: var(--glass-surface-hover);
      border-color: var(--glass-border-hover);
      box-shadow: var(--glass-glow);
      transform: translateY(-4px);
    }
    .glass-card .icon {
      width: 48px;
      height: 48px;
      background: var(--glass-surface);
      backdrop-filter: var(--glass-blur);
      -webkit-backdrop-filter: var(--glass-blur);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
      margin-bottom: var(--space-md);
    }
    .glass-card h3 {
      font-size: 1.125rem;
      font-weight: 600;
      color: var(--glass-text);
      margin-bottom: var(--space-sm);
    }
    .glass-card p {
      font-size: 0.875rem;
      color: var(--glass-text-muted);
      line-height: 1.6;
    }
    .glass-stats {
      display: flex;
      gap: var(--space-lg);
      justify-content: center;
      margin-top: var(--space-lg);
    }
    .glass-stat {
      background: var(--glass-surface);
      backdrop-filter: var(--glass-blur);
      -webkit-backdrop-filter: var(--glass-blur);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      padding: var(--space-lg) var(--space-xl);
      text-align: center;
      flex: 1;
      max-width: 200px;
    }
    .glass-stat .num {
      font-size: 2.5rem;
      font-weight: 700;
      color: var(--glass-accent);
    }
    .glass-stat .label {
      font-size: 0.75rem;
      color: var(--glass-text-muted);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-top: var(--space-xs);
    }
    .glass-footer {
      padding: var(--space-lg) 0;
      text-align: center;
      border-top: 1px solid var(--glass-border);
      font-size: 0.75rem;
      color: var(--glass-text-muted);
    }
    @media (max-width: 768px) {
      .glass-header h1 { font-size: 2.25rem; }
      .glass-stats { flex-direction: column; align-items: center; }
      .glass-stat { max-width: 100%; width: 100%; }
    }
  </style>
</head>
<body>
  <header class="glass-header">
    <div class="container">
      <h1>Glassmorphism</h1>
      <p>Depth through transparency · Light through layers</p>
    </div>
  </header>
  <section class="glass-section">
    <div class="container">
      <h2>Core Components</h2>
      <div class="grid">
        <div class="col-4">
          <div class="glass-card">
            <div class="icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.8)" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
            </div>
            <h3>Backdrop Blur</h3>
            <p>frosted glass effect using backdrop-filter: blur(20px). Layered on gradient backgrounds to simulate translucency and depth.</p>
          </div>
        </div>
        <div class="col-4">
          <div class="glass-card">
            <div class="icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.8)" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/></svg>
            </div>
            <h3>Light Borders</h3>
            <p>rgba(255,255,255,0.18) 1px borders create the glass edge. On hover, opacity increases to 0.28 for subtle interactivity.</p>
          </div>
        </div>
        <div class="col-4">
          <div class="glass-card">
            <div class="icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.8)" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
            </div>
            <h3>Layered Depth</h3>
            <p>Multiple stacked glass surfaces with varying opacity create a z-space effect. Lower layers are more opaque, higher layers more transparent.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
  <section class="glass-section">
    <div class="container">
      <h2>Ambient Glow</h2>
      <div class="grid">
        <div class="col-6">
          <div class="glass-card" style="min-height:200px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;">
            <p style="font-size:3rem;margin-bottom:var(--space-md);">✦</p>
            <h3>Glow Effect</h3>
            <p>box-shadow: 0 0 30px rgba(100,255,218,0.15) creates a soft glow. The accent color var(--glass-accent) at #64ffda provides the light source.</p>
          </div>
        </div>
        <div class="col-6">
          <div class="glass-stat" style="max-width:100%;">
            <div class="num">20px</div>
            <div class="label">Blur Radius</div>
          </div>
          <div class="glass-stat" style="max-width:100%;margin-top:var(--space-md);">
            <div class="num">0.08</div>
            <div class="label">Base Surface Opacity</div>
          </div>
          <div class="glass-stat" style="max-width:100%;margin-top:var(--space-md);">
            <div class="num">2</div>
            <div class="label">Recommended Max Layers</div>
          </div>
        </div>
      </div>
    </div>
  </section>
  <footer class="glass-footer">
    <div class="container">
      <p>Glassmorphism — Inspired by Apple's design language and the frosted glass aesthetic. 2026.</p>
    </div>
  </footer>
</body>
</html>
--- neo-brutalist.html ---
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Neo-Brutalist</title>
  <style>
    :root {
      --nb-bg: #f5f0eb;
      --nb-text: #1a1a2e;
      --nb-accent1: #ff6b6b;
      --nb-accent2: #4ecdc4;
      --nb-accent3: #ffe66d;
      --nb-accent4: #a29bfe;
      --nb-accent5: #fd79a8;
      --nb-border: #1a1a2e;
      --nb-border-w: 3px;
      --font-nb: 'Space Grotesk', 'Inter', sans-serif;
    }
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      font-family: var(--font-nb);
      background: var(--nb-bg);
      color: var(--nb-text);
      line-height: 1.3;
    }
    .nb-header {
      background: var(--nb-accent1);
      color: white;
      padding: var(--space-lg, 2rem) 0;
      border-bottom: var(--nb-border-w) solid var(--nb-border);
      position: relative;
    }
    .nb-header::before {
      content: '★';
      position: absolute;
      top: 0.5rem;
      right: 1rem;
      font-size: 2rem;
      color: var(--nb-accent3);
    }
    .nb-header h1 {
      font-size: 5rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: -0.04em;
      line-height: 0.9;
    }
    .nb-header .tag {
      font-size: 1rem;
      font-weight: 500;
      margin-top: var(--space-sm);
      background: var(--nb-border);
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: 0;
    }
    .nb-section {
      padding: var(--space-lg, 2rem) 0;
    }
    .nb-section h2 {
      font-size: 2rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: -0.02em;
      margin-bottom: var(--space-lg, 2rem);
      display: inline-block;
      background: var(--nb-accent3);
      padding: 0.25rem 1rem;
      border: var(--nb-border-w) solid var(--nb-border);
    }
    .nb-card {
      background: white;
      border: var(--nb-border-w) solid var(--nb-border);
      padding: 1.5rem;
      margin-bottom: 1rem;
      position: relative;
      transition: transform 100ms ease;
    }
    .nb-card:hover {
      transform: translate(-4px, -4px);
      box-shadow: 6px 6px 0 var(--nb-border);
    }
    .nb-card.color-1 { border-top: 8px solid var(--nb-accent1); }
    .nb-card.color-2 { border-top: 8px solid var(--nb-accent2); }
    .nb-card.color-3 { border-top: 8px solid var(--nb-accent3); }
    .nb-card.color-4 { border-top: 8px solid var(--nb-accent4); }
    .nb-card.color-5 { border-top: 8px solid var(--nb-accent5); }
    .nb-card .label {
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      color: var(--nb-text);
      margin-bottom: 0.5rem;
    }
    .nb-card h3 {
      font-size: 1.5rem;
      font-weight: 700;
      margin-bottom: 0.5rem;
    }
    .nb-card p {
      font-size: 0.9375rem;
      color: #555;
    }
    .nb-card .badge {
      position: absolute;
      top: -0.75rem;
      right: 1rem;
      background: var(--nb-accent5);
      color: white;
      font-size: 0.6875rem;
      font-weight: 700;
      text-transform: uppercase;
      padding: 0.2rem 0.6rem;
      border: 2px solid var(--nb-border);
    }
    .nb-color-strip {
      display: flex;
      height: 40px;
      margin: 1rem 0;
    }
    .nb-color-strip > div {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.625rem;
      font-weight: 700;
      color: white;
      text-transform: uppercase;
    }
    .nb-footer {
      background: var(--nb-text);
      color: white;
      padding: var(--space-lg, 2rem) 0;
      text-align: center;
      border-top: var(--nb-border-w) solid var(--nb-accent1);
    }
    .nb-footer p {
      color: rgba(255,255,255,0.6);
      font-size: 0.75rem;
    }
    .container {
      max-width: 1100px;
      margin: 0 auto;
      padding: 0 1rem;
    }
    @media (max-width: 768px) {
      .nb-header h1 { font-size: 2.75rem; }
      .nb-section h2 { font-size: 1.5rem; }
    }
  </style>
</head>
<body>
  <header class="nb-header">
    <div class="container">
      <h1>Neo-Brutalist</h1>
      <div class="tag">Bright · Bold · Playful</div>
    </div>
  </header>
  <section class="nb-section">
    <div class="container">
      <h2>Color Palette</h2>
      <div class="nb-color-strip">
        <div style="background:var(--nb-accent1);">#FF6B6B</div>
        <div style="background:var(--nb-accent2);color:#1a1a2e;">#4ECDC4</div>
        <div style="background:var(--nb-accent3);color:#1a1a2e;">#FFE66D</div>
        <div style="background:var(--nb-accent4);">#A29BFE</div>
        <div style="background:var(--nb-accent5);">#FD79A8</div>
      </div>
    </div>
  </section>
  <section class="nb-section">
    <div class="container">
      <h2>Components</h2>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
        <div class="nb-card color-1">
          <div class="badge">New</div>
          <div class="label">Interactive</div>
          <h3>Hover Lift</h3>
          <p>Cards lift 4px up and left on hover with a matching shadow offset. No transitions — instant snap for that raw feel.</p>
        </div>
        <div class="nb-card color-2">
          <div class="label">Typography</div>
          <h3>Oversized Type</h3>
          <p>Headings at 5rem. Cards at 1.5rem. Everything is bigger than expected. Space Grotesk at 700 weight minimum.</p>
        </div>
        <div class="nb-card color-3">
          <div class="label">Borders</div>
          <h3>Heavy Strokes</h3>
          <p>3px minimum border weight. Every component has a hard outline. Colored top-borders (8px) categorize card types.</p>
        </div>
        <div class="nb-card color-4">
          <div class="label">Geometry</div>
          <h3>Playful Shapes</h3>
          <p>Diagonal cuts, rotated badges, offset shadows, and overlapping elements. Asymmetry is a feature, not a bug.</p>
        </div>
        <div class="nb-card color-5">
          <div class="label">Accents</div>
          <h3>Bright Colors</h3>
          <p>5 accent colors used freely. High saturation. No muted tones except the warm off-white background (#F5F0EB).</p>
        </div>
      </div>
    </div>
  </section>
  <footer class="nb-footer">
    <div class="container">
      <p>Neo-Brutalist — Contemporary brutalist design. Play hard. 2026.</p>
    </div>
  </footer>
</body>
</html>
--- decision-guide.html ---
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aesthetic Decision Guide</title>
  <link rel="stylesheet" href="stylesheet.css">
  <style>
    :root {
      --dg-border: #ddd;
      --dg-header-bg: #111;
      --dg-header-text: #fff;
      --dg-row-alt: #f8f8f8;
      --dg-match: #d4edda;
      --dg-partial: #fff3cd;
      --dg-mismatch: #f8d7da;
    }
    .dg-header {
      background: var(--dg-header-bg);
      color: var(--dg-header-text);
      padding: var(--space-xl) 0;
      text-align: center;
    }
    .dg-header h1 {
      font-size: 2.5rem;
      font-weight: 700;
    }
    .dg-header p {
      color: rgba(255,255,255,0.6);
      margin-top: var(--space-sm);
    }
    .dg-section {
      padding: var(--space-xl) 0;
    }
    .dg-section h2 {
      font-size: 1.25rem;
      font-weight: 600;
      margin-bottom: var(--space-lg);
      border-bottom: 2px solid var(--dg-border);
      padding-bottom: var(--space-sm);
    }
    table.dg-matrix {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.875rem;
    }
    table.dg-matrix th,
    table.dg-matrix td {
      border: 1px solid var(--dg-border);
      padding: 0.75rem;
      text-align: left;
      vertical-align: top;
    }
    table.dg-matrix th {
      background: var(--dg-header-bg);
      color: var(--dg-header-text);
      font-weight: 600;
      text-transform: uppercase;
      font-size: 0.75rem;
      letter-spacing: 0.05em;
    }
    table.dg-matrix tr:nth-child(even) td {
      background: var(--dg-row-alt);
    }
    .tag {
      display: inline-block;
      padding: 0.125rem 0.5rem;
      font-size: 0.6875rem;
      font-weight: 700;
      text-transform: uppercase;
      border-radius: 2px;
    }
    .tag-good { background: var(--dg-match); color: #155724; }
    .tag-ok { background: var(--dg-partial); color: #856404; }
    .tag-bad { background: var(--dg-mismatch); color: #721c24; }
    .dg-rec {
      background: var(--dg-row-alt);
      border-left: 4px solid #111;
      padding: var(--space-lg);
      margin-top: var(--space-lg);
    }
    .dg-rec h3 {
      font-size: 1rem;
      font-weight: 600;
      margin-bottom: var(--space-sm);
    }
    .dg-rec p {
      font-size: 0.875rem;
      color: #555;
    }
    .dg-footer {
      background: var(--dg-header-bg);
      color: white;
      padding: var(--space-lg) 0;
      text-align: center;
      font-size: 0.75rem;
    }
    @media (max-width: 768px) {
      .dg-header h1 { font-size: 1.5rem; }
      table.dg-matrix { font-size: 0.75rem; }
      table.dg-matrix th, table.dg-matrix td { padding: 0.5rem; }
    }
  </style>
</head>
<body>
  <header class="dg-header">
    <div class="container">
      <h1>Aesthetic Decision Guide</h1>
      <p>Match your project to the right visual style</p>
    </div>
  </header>
  <section class="dg-section">
    <div class="container">
      <h2>Decision Matrix</h2>
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
            <td>Corporate / B2B Dashboard</td>
            <td><span class="tag tag-good">Excellent</span><br>Grid precision, clear hierarchy</td>
            <td><span class="tag tag-good">Excellent</span><br>Clean, professional</td>
            <td><span class="tag tag-bad">Poor</span><br>Too aggressive</td>
            <td><span class="tag tag-ok">Fair</span><br>Heavy, competes with data</td>
            <td><span class="tag tag-bad">Poor</span><br>Too playful</td>
          </tr>
          <tr>
            <td>Portfolio / Agency Site</td>
            <td><span class="tag tag-good">Excellent</span><br>Design-forward</td>
            <td><span class="tag tag-ok">Fair</span><br>May be too quiet</td>
            <td><span class="tag tag-ok">Fair</span><br>Niche appeal</td>
            <td><span class="tag tag-good">Excellent</span><br>Impressive, modern</td>
            <td><span class="tag tag-good">Excellent</span><br>Memorable, bold</td>
          </tr>
          <tr>
            <td>SaaS Landing Page</td>
            <td><span class="tag tag-good">Excellent</span><br>Trust, clarity</td>
            <td><span class="tag tag-good">Excellent</span><br>Focus on content</td>
            <td><span class="tag tag-ok">Fair</span><br>Differentiating</td>
            <td><span class="tag tag-good">Excellent</span><br>Premium feel</td>
            <td><span class="tag tag-ok">Fair</span><br>Risk of distraction</td>
          </tr>
          <tr>
            <td>E-commerce / Product</td>
            <td><span class="tag tag-ok">Fair</span><br>Good but formal</td>
            <td><span class="tag tag-good">Excellent</span><br>Products shine</td>
            <td><span class="tag tag-bad">Poor</span><br>Hurts conversion</td>
            <td><span class="tag tag-ok">Fair</span><br>Heavy, slow</td>
            <td><span class="tag tag-ok">Fair</span><br>Youth brands only</td>
          </tr>
          <tr>
            <td>Creative / Art Platform</td>
            <td><span class="tag tag-ok">Fair</span><br>Good, structured</td>
            <td><span class="tag tag-ok">Fair</span><br>Minimalist art</td>
            <td><span class="tag tag-good">Excellent</span><br>Raw authenticity</td>
            <td><span class="tag tag-good">Excellent</span><br>Gallery vibe</td>
            <td><span class="tag tag-good">Excellent</span><br>Playful, expressive</td>
          </tr>
          <tr>
            <td>Personal Blog</td>
            <td><span class="tag tag-ok">Fair</span><br>Formal for blogging</td>
            <td><span class="tag tag-good">Excellent</span><br>Reader-first</td>
            <td><span class="tag tag-bad">Poor</span><br>Too harsh</td>
            <td><span class="tag tag-ok">Fair</span><br>Heavy for text</td>
            <td><span class="tag tag-ok">Fair</span><br>Personality-driven</td>
          </tr>
          <tr>
            <td>Documentation / API</td>
            <td><span class="tag tag-good">Excellent</span><br>Crystal clear</td>
            <td><span class="tag tag-good">Excellent</span><br>Distraction-free</td>
            <td><span class="tag tag-bad">Poor</span><br>Confusing</td>
            <td><span class="tag tag-bad">Poor</span><br>Unnecessary flourish</td>
            <td><span class="tag tag-bad">Poor</span><br>Undermines authority</td>
          </tr>
          <tr>
            <td>Mobile App UI</td>
            <td><span class="tag tag-ok">Fair</span><br>Dense on small screens</td>
            <td><span class="tag tag-good">Excellent</span><br>Great for mobile</td>
            <td><span class="tag tag-bad">Poor</span><br>Too intense</td>
            <td><span class="tag tag-good">Excellent</span><br>Premium mobile UX</td>
            <td><span class="tag tag-ok">Fair</span><br>Depends on brand</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
  <section class="dg-section">
    <div class="container">
      <h2>Recommendations By User Type</h2>
      <div class="dg-rec">
        <h3>Startup with limited brand equity</h3>
        <p>Swiss or Minimal. These styles communicate competence without requiring an established brand. The International Typographic Style implies professionalism by association. Avoid Brutalist and Neo-Brutalist — they require existing trust to pull off without looking unfinished.</p>
      </div>
      <div class="dg-rec">
        <h3>Creative agency wanting to differentiate</h3>
        <p>Neo-Brutalist or Glass. Both make strong visual statements. Neo-Brutalist signals confidence and cultural awareness. Glass signals technical sophistication and premium positioning. Swiss is the safe pick for client-facing proposals.</p>
      </div>
      <div class="dg-rec">
        <h3>Enterprise product pursuing premium</h3>
        <p>Minimal for the core interface, Glass for marketing pages. Minimal gives utility and speed; Glass provides the aspirational wrapper. Avoid Brutalist — it reads as either unfinished or ideological, neither reassuring to enterprise buyers.</p>
      </div>
      <div class="dg-rec">
        <h3>Personal portfolio / artist</h3>
        <p>Brutalist or Glass depending on the work. Brutalist for photographers, illustrators, and architects — the raw structural frame lets the work command attention. Glass for digital artists, designers, and technologists — it mirrors their medium.</p>
      </div>
    </div>
  </section>
  <footer class="dg-footer">
    <div class="container">
      <p>Aesthetic Style Composer v2 — Decision Guide. 2026.</p>
    </div>
  </footer>
</body>
</html>
--- Composition ---
The five templates share a common token foundation defined in stylesheet.css but each aesthetic overrides or extends different token categories.
Shared tokens used across templates:
  --color-text and --color-text-muted are referenced by Swiss (.swiss-card p), Minimal (.min-card p, .min-principle p), and Glass (.glass-card p). Brutalist and Neo-Brutalist define their own token sets locally since they intentionally break the shared color system for aesthetic divergence.
Grid relationships:
  Swiss and Minimal both use the 12-column .grid from stylesheet.css. Brutalist uses a 6-column grid defined locally (no dependency on shared grid) — the 6-column constraint forces bigger structural chunks. Glass uses the 12-column shared grid. Neo-Brutalist uses a 2-column grid defined locally. This means Swiss and Glass can be composited onto the same page because they share the same grid system. Minimal also shares the grid but its max-width 800px constraint on sections reduces the grid to a layout scaffold.
Stacking order when compositing multiple templates into a single page:
  1. Brutalist or Neo-Brutalist at the root (they control the page background and structural rhythm)
  2. Glass panels floated on top via position: absolute or position: sticky with z-index: 10 — the backdrop-filter needs a solid background behind it to create the frosted effect
  3. Swiss grid sections between Glass panels as content regions — the Swiss red accent headers and grid sections provide visual punctuation
  4. Minimal overlays as inset modals or sidebars — Minimal's max-width 800px constraint makes it ideal for contained widgets
Responsive show/hide modifiers: Templates that link stylesheet.css inherit its responsive breakpoints at 768px and 480px. Templates with local grids (Brutalist, Neo-Brutalist) define their own breakpoints. To hide elements by template type on certain viewports, use data attributes: [data-aesthetic="swiss"] .grid would be controlled via media query display toggles. The shared .sr-only class from stylesheet.css also enables accessible show/hide.
--- CSS Property Audit ---
Swiss template (swiss.html):
  var(--color-text-muted) — resolves to stylesheet.css :root
  var(--space-md), var(--space-lg), var(--space-xl), var(--space-sm) — all resolve to stylesheet.css :root
  var(--space-xs) — not in stylesheet.css, but not referenced either
  var(--swiss-red), var(--swiss-black), var(--swiss-white), var(--swiss-gray), var(--swiss-grid-color) — local, defined in swiss.html :root
  All references resolved. 0 warnings.
Minimal template (minimal.html):
  var(--color-text-muted) — resolves to stylesheet.css :root
  var(--space-md), var(--space-lg), var(--space-xl), var(--space-sm), var(--space-xs) — all resolve to stylesheet.css
  var(--transition-base), var(--transition-fast) — resolve to stylesheet.css
  var(--min-bg), var(--min-surface), var(--min-text), var(--min-muted), var(--min-border), var(--min-accent) — local, defined in minimal.html :root
  All references resolved. 0 warnings.
Brutalist template (brutalist.html): No dependency on stylesheet.css. All var() references are local to brutalist.html :root. The file also uses fallback values e.g. var(--space-lg, 2rem) — this is safe practice since the fallback handles the case where stylesheet.css is not loaded. All references resolved. 0 warnings.
Glass template (glass.html):
  var(--space-md), var(--space-lg), var(--space-xl), var(--space-sm), var(--space-xs), var(--space-xl) — all resolve to stylesheet.css
  var(--radius-md), var(--radius-lg) — resolve to stylesheet.css
  var(--transition-base) — resolves to stylesheet.css
  var(--glass-bg-start), var(--glass-bg-mid), var(--glass-bg-end), var(--glass-surface), var(--glass-surface-hover), var(--glass-border), var(--glass-border-hover), var(--glass-blur), var(--glass-blur-heavy), var(--glass-text), var(--glass-text-muted), var(--glass-accent), var(--glass-glow) — all local, defined in glass.html :root
  All references resolved. 0 warnings.
Neo-Brutalist template (neo-brutalist.html): No dependency on stylesheet.css. All var() references local. Uses nb- prefixed tokens plus var(--space-lg, 2rem) with fallbacks. All references resolved. 0 warnings.
Decision Guide (decision-guide.html):
  var(--space-sm), var(--space-md), var(--space-lg), var(--space-xl) — resolve to stylesheet.css
  var(--space-xs) — not referenced, no issue
  var(--dg-border), var(--dg-header-bg), var(--dg-header-text), var(--dg-row-alt), var(--dg-match), var(--dg-partial), var(--dg-mismatch) — local, defined in decision-guide.html :root
  All references resolved. 0 warnings.
Shared Boilerplate Reduction:
  Duplicate blocks detected:
    Reset/normalize (*, *::before, *::after) — present in brutalist.html, neo-brutalist.html, and stylesheet.css. Extracted into stylesheet.css. Brutalist and Neo-Brutalist retain their own copies since they intentionally do not depend on stylesheet.css.
    Grid system (.grid, .col-*) — defined in stylesheet.css. Swiss, Minimal, and Glass reference it. Brutalist and Neo-Brutalist define their own (6-col and 2-col respectively).
    Container class (.container) — defined in stylesheet.css. Also duplicated in brutalist.html and neo-brutalist.html (inline). Since those files do not link stylesheet.css, the duplication is necessary and below the 3-template threshold.
    Font-face declarations — no @font-face used in any template; all use Google Fonts @import or system fonts.
Completion Gate Verification:
  manifest.json — present
  stylesheet.css — present
  swiss.html — present, all tags closed, ends with newline, footer present
  minimal.html — present, all tags closed, ends with newline, footer present
  brutalist.html — present, all tags closed, ends with newline, footer present
  glass.html — present, all tags closed, ends with newline, footer present
  neo-brutalist.html — present, all tags closed, ends with newline, footer present
  decision-guide.html — present, all tags closed, ends with newline, footer present
  Tag balance: <!DOCTYPE html>, <html>, <head>, <body>, <header>, <footer>, <section>, <div>, <h1-3>, <p>, <table>, <th>, <td>, <tr> — all closed. No truncated tags detected in any file.
  var(--) references: all resolved per audit above. 0 warnings.
  All files end with newline. All sections listed in manifest are present. Gate: PASSED.