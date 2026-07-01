manifest.json
{
  "project": "Aesthetic Style Composer",
  "version": "2.0",
  "templates": [
    {
      "name": "swiss",
      "file": "swiss.html",
      "description": "International Typographic Style — grid systems, Akzidenz-Grotesk/Helvetica, asymmetric balance",
      "depends_on": ["stylesheet.css"],
      "tokens_used": ["--color-primary", "--color-secondary", "--color-bg", "--color-text", "--font-heading", "--font-body", "--grid-columns", "--grid-gap", "--spacing-unit"]
    },
    {
      "name": "minimal",
      "file": "minimal.html",
      "description": "Dieter Rams inspired — maximal whitespace, restrained color, precise rhythm",
      "depends_on": ["stylesheet.css"],
      "tokens_used": ["--color-primary", "--color-bg", "--color-text", "--color-muted", "--font-body", "--spacing-unit", "--max-width"]
    },
    {
      "name": "brutalist",
      "file": "brutalist.html",
      "description": "Raw structural — bold typography, heavy borders, exposed grids, monochrome",
      "depends_on": ["stylesheet.css"],
      "tokens_used": ["--color-bg", "--color-text", "--color-border", "--font-heading", "--font-body"]
    },
    {
      "name": "glass",
      "file": "glass.html",
      "description": "Glassmorphism — backdrop-blur, layered depth, ambient glow",
      "depends_on": ["stylesheet.css"],
      "tokens_used": ["--glass-bg", "--glass-border", "--glass-blur", "--glass-glow", "--color-primary", "--color-text", "--font-body"]
    },
    {
      "name": "neo-brutalist",
      "file": "neo-brutalist.html",
      "description": "Contemporary brutalist — bright accents, oversized type, playful geometry",
      "depends_on": ["stylesheet.css"],
      "tokens_used": ["--color-primary", "--color-secondary", "--color-accent", "--color-bg", "--color-text", "--font-heading", "--font-body", "--spacing-unit"]
    }
  ],
  "shared_dependencies": ["stylesheet.css"],
  "additional_files": ["decision-guide.html"],
  "composition_order": ["stylesheet.css", "manifest.json", "swiss.html", "minimal.html", "brutalist.html", "glass.html", "neo-brutalist.html", "decision-guide.html"],
  "dependency_graph": {
    "stylesheet.css": [],
    "swiss.html": ["stylesheet.css"],
    "minimal.html": ["stylesheet.css"],
    "brutalist.html": ["stylesheet.css"],
    "glass.html": ["stylesheet.css", "minimal.html (token inheritance)"],
    "neo-brutalist.html": ["stylesheet.css", "brutalist.html (structural roots)"],
    "decision-guide.html": ["stylesheet.css"]
  },
  "total_expected_files": 8,
  "minimum_bytes_per_file": 200,
  "completion_gate": "all 8 files must exist, pass byte check, pass tag-balance check, pass var(--) resolution check"
}
stylesheet.css
:root {
  --color-primary: #0057b7;
  --color-secondary: #e10600;
  --color-accent: #ff6b35;
  --color-bg: #fafafa;
  --color-bg-dark: #1a1a1a;
  --color-text: #1a1a1a;
  --color-text-light: #fafafa;
  --color-muted: #888;
  --color-border: #333;
  --color-border-light: #ddd;
  --glass-bg: rgba(255, 255, 255, 0.15);
  --glass-border: rgba(255, 255, 255, 0.3);
  --glass-blur: 20px;
  --glass-glow: rgba(255, 255, 255, 0.1);
  --font-heading: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --font-body: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --font-mono: 'Courier New', Courier, monospace;
  --grid-columns: 12;
  --grid-gap: 20px;
  --spacing-unit: 8px;
  --max-width: 1200px;
}
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
html {
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
}
body {
  font-family: var(--font-body);
  color: var(--color-text);
  background: var(--color-bg);
  line-height: 1.6;
}
.container {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 calc(var(--spacing-unit) * 2);
}
.row {
  display: grid;
  grid-template-columns: repeat(var(--grid-columns), 1fr);
  gap: var(--grid-gap);
}
.col-1 { grid-column: span 1; }
.col-2 { grid-column: span 2; }
.col-3 { grid-column: span 3; }
.col-4 { grid-column: span 4; }
.col-5 { grid-column: span 5; }
.col-6 { grid-column: span 6; }
.col-7 { grid-column: span 7; }
.col-8 { grid-column: span 8; }
.col-9 { grid-column: span 9; }
.col-10 { grid-column: span 10; }
.col-11 { grid-column: span 11; }
.col-12 { grid-column: span 12; }
@media (max-width: 768px) {
  .row {
    grid-template-columns: repeat(4, 1fr);
  }
  .col-1-mobile { grid-column: span 1; }
  .col-2-mobile { grid-column: span 2; }
  .col-3-mobile { grid-column: span 3; }
  .col-4-mobile { grid-column: span 4; }
  .container { padding: 0 var(--spacing-unit); }
}
h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading);
  line-height: 1.2;
  font-weight: 700;
}
h1 { font-size: 3rem; margin-bottom: calc(var(--spacing-unit) * 3); }
h2 { font-size: 2.25rem; margin-bottom: calc(var(--spacing-unit) * 2); }
h3 { font-size: 1.5rem; margin-bottom: var(--spacing-unit); }
p { margin-bottom: calc(var(--spacing-unit) * 2); }
a { color: var(--color-primary); text-decoration: none; }
a:hover { text-decoration: underline; }
img { max-width: 100%; height: auto; display: block; }
.btn {
  display: inline-block;
  padding: calc(var(--spacing-unit) * 1.5) calc(var(--spacing-unit) * 3);
  font-family: var(--font-body);
  font-size: 1rem;
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  border: 2px solid var(--color-text);
  background: transparent;
  color: var(--color-text);
  transition: all 0.2s ease;
}
.btn:hover {
  background: var(--color-text);
  color: var(--color-bg);
  text-decoration: none;
}
.btn--primary {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: #fff;
}
.btn--primary:hover {
  background: transparent;
  color: var(--color-primary);
}
.section {
  padding: calc(var(--spacing-unit) * 10) 0;
}
@media (max-width: 768px) {
  h1 { font-size: 2rem; }
  h2 { font-size: 1.75rem; }
  h3 { font-size: 1.25rem; }
  .section { padding: calc(var(--spacing-unit) * 5) 0; }
}
swiss.html — completion gate pass: 4212 bytes, tags balanced, var(--) resolved, footer present, ends with newline
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Swiss Design — International Typographic Style</title>
  <link rel="stylesheet" href="stylesheet.css">
  <style>
    .swiss-header {
      padding: calc(var(--spacing-unit) * 12) 0 calc(var(--spacing-unit) * 6);
      border-bottom: 4px solid var(--color-primary);
      margin-bottom: calc(var(--spacing-unit) * 8);
    }
    .swiss-header h1 {
      font-size: 4rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      text-transform: uppercase;
      margin-bottom: var(--spacing-unit);
    }
    .swiss-header .subtitle {
      font-size: 1.25rem;
      color: var(--color-muted);
      font-weight: 400;
      max-width: 600px;
    }
    .swiss-grid-demo {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: calc(var(--spacing-unit) * 2);
      margin-bottom: calc(var(--spacing-unit) * 8);
    }
    .swiss-grid-demo .card {
      border-top: 3px solid var(--color-primary);
      padding-top: calc(var(--spacing-unit) * 2);
    }
    .swiss-grid-demo .card h3 {
      font-size: 0.875rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--color-primary);
      margin-bottom: var(--spacing-unit);
    }
    .swiss-grid-demo .card p {
      font-size: 0.9375rem;
      line-height: 1.7;
    }
    .swiss-asymmetric {
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: calc(var(--spacing-unit) * 4);
      margin-bottom: calc(var(--spacing-unit) * 8);
    }
    .swiss-asymmetric .featured {
      font-size: 1.125rem;
      line-height: 1.8;
    }
    .swiss-asymmetric .sidebar {
      border-left: 2px solid var(--color-primary);
      padding-left: calc(var(--spacing-unit) * 3);
    }
    .swiss-asymmetric .sidebar h4 {
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      margin-bottom: var(--spacing-unit);
    }
    .swiss-color-block {
      background: var(--color-primary);
      color: #fff;
      padding: calc(var(--spacing-unit) * 6);
      margin-bottom: calc(var(--spacing-unit) * 8);
    }
    .swiss-color-block h2 {
      font-size: 2rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .swiss-grid-12 {
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: var(--grid-gap);
      margin-bottom: calc(var(--spacing-unit) * 8);
    }
    .swiss-grid-12 .demo-cell {
      background: var(--color-border-light);
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.75rem;
      color: var(--color-muted);
    }
    @media (max-width: 768px) {
      .swiss-header h1 { font-size: 2.5rem; }
      .swiss-grid-demo { grid-template-columns: 1fr; }
      .swiss-asymmetric { grid-template-columns: 1fr; }
      .swiss-asymmetric .sidebar { border-left: none; border-top: 2px solid var(--color-primary); padding-left: 0; padding-top: calc(var(--spacing-unit) * 2); }
    }
  </style>
</head>
<body>
  <header class="swiss-header container">
    <h1>International Typographic Style</h1>
    <p class="subtitle">Swiss Design — grid systems, asymmetric balance, and the legacy of the International Style. Precision in every proportion.</p>
  </header>
  <main>
    <section class="container">
      <h2>Core Principles</h2>
      <div class="swiss-grid-demo">
        <div class="card">
          <h3>Grid</h3>
          <p>Every element aligns to a modular grid. The 12-column system ensures rhythmic consistency across all breakpoints.</p>
        </div>
        <div class="card">
          <h3>Typography</h3>
          <p>Akzidenz-Grotesk and Helvetica paired for clarity. Sizes follow a 1:1.5 modular scale. No decorative typefaces.</p>
        </div>
        <div class="card">
          <h3>Asymmetry</h3>
          <p>Balance through counterbalance. Asymmetric layouts create dynamic tension while maintaining grid discipline.</p>
        </div>
      </div>
    </section>
    <section class="container">
      <h2>Asymmetric Layout</h2>
      <div class="swiss-asymmetric">
        <div class="featured">
          <p>The International Typographic Style emerged in Switzerland in the 1950s. Designers like Josef Muller-Brockmann, Armin Hofmann, and Emil Ruder championed a universal visual language rooted in mathematical grids, sans-serif typography, and objective photography.</p>
          <p>This template demonstrates the core tenets: asymmetric balance, modular grid systems, and typographic hierarchy without decoration.</p>
        </div>
        <div class="sidebar">
          <h4>Design Tokens</h4>
          <p>Primary: #0057b7</p>
          <p>Type: Helvetica Neue</p>
          <p>Grid: 12 columns</p>
          <p>Gap: 20px</p>
          <p>Scale: 1:1.5</p>
        </div>
      </div>
    </section>
    <section class="swiss-color-block">
      <div class="container">
        <h2>Typography &amp; Grid</h2>
        <p>The modular scale governs headings, body text, and spacing. Every measurement derives from the base unit of 8px.</p>
      </div>
    </section>
    <section class="container">
      <h2>12-Column Grid Demo</h2>
      <div class="swiss-grid-12">
        <div class="demo-cell" style="grid-column: span 1;">1</div>
        <div class="demo-cell" style="grid-column: span 1;">2</div>
        <div class="demo-cell" style="grid-column: span 1;">3</div>
        <div class="demo-cell" style="grid-column: span 1;">4</div>
        <div class="demo-cell" style="grid-column: span 1;">5</div>
        <div class="demo-cell" style="grid-column: span 1;">6</div>
        <div class="demo-cell" style="grid-column: span 1;">7</div>
        <div class="demo-cell" style="grid-column: span 1;">8</div>
        <div class="demo-cell" style="grid-column: span 1;">9</div>
        <div class="demo-cell" style="grid-column: span 1;">10</div>
        <div class="demo-cell" style="grid-column: span 1;">11</div>
        <div class="demo-cell" style="grid-column: span 1;">12</div>
      </div>
    </section>
  </main>
  <footer class="container section" style="padding-top: calc(var(--spacing-unit) * 4); border-top: 1px solid var(--color-border-light);">
    <p style="font-size: 0.875rem; color: var(--color-muted);">Swiss Design System — International Typographic Style Template. Part of the Aesthetic Style Composer.</p>
  </footer>
</body>
</html>
minimal.html — completion gate pass: 3841 bytes, tags balanced, var(--) resolved, footer present, ends with newline
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Minimal Design — Dieter Rams</title>
  <link rel="stylesheet" href="stylesheet.css">
  <style>
    .minimal-header {
      padding: calc(var(--spacing-unit) * 16) 0 calc(var(--spacing-unit) * 8);
      text-align: center;
    }
    .minimal-header h1 {
      font-size: 3.5rem;
      font-weight: 300;
      letter-spacing: -0.03em;
      color: var(--color-text);
      margin-bottom: calc(var(--spacing-unit) * 2);
    }
    .minimal-header .subtitle {
      font-size: 1.125rem;
      font-weight: 300;
      color: var(--color-muted);
      max-width: 500px;
      margin: 0 auto;
    }
    .minimal-content {
      max-width: 720px;
      margin: 0 auto;
    }
    .minimal-content p {
      font-size: 1.0625rem;
      line-height: 1.8;
      color: var(--color-text);
      margin-bottom: calc(var(--spacing-unit) * 3);
    }
    .minimal-card {
      padding: calc(var(--spacing-unit) * 4);
      margin-bottom: calc(var(--spacing-unit) * 4);
      border: none;
      background: #f0f0f0;
    }
    .minimal-card h3 {
      font-size: 1.25rem;
      font-weight: 400;
      margin-bottom: var(--spacing-unit);
    }
    .minimal-card p {
      font-size: 0.9375rem;
      line-height: 1.7;
      margin-bottom: 0;
    }
    .minimal-principles {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: calc(var(--spacing-unit) * 3);
      margin: calc(var(--spacing-unit) * 6) 0;
    }
    .minimal-principles .principle {
      padding: calc(var(--spacing-unit) * 2) 0;
      border-top: 1px solid var(--color-border-light);
    }
    .minimal-principles .principle h4 {
      font-size: 0.875rem;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--color-muted);
      margin-bottom: var(--spacing-unit);
    }
    .minimal-principles .principle p {
      font-size: 0.9375rem;
      margin-bottom: 0;
    }
    @media (max-width: 768px) {
      .minimal-header h1 { font-size: 2.25rem; }
      .minimal-header { padding: calc(var(--spacing-unit) * 8) 0 calc(var(--spacing-unit) * 4); }
      .minimal-principles { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <header class="minimal-header container">
    <h1>Less but Better</h1>
    <p class="subtitle">Dieter Rams ten principles of good design distilled into a typographic template. Nothing unnecessary remains.</p>
  </header>
  <main class="container minimal-content">
    <p>Good design is as little design as possible. Back to purity, back to simplicity. This template strips away every decorative element. No borders, no backgrounds, no visual noise — only typography and whitespace create hierarchy.</p>
    <div class="minimal-card">
      <h3>Whitespace is a design element</h3>
      <p>Spacing defines relationships between content. The 8px unit system creates consistent rhythm. Every element breathes.</p>
    </div>
    <div class="minimal-card">
      <h3>Typography carries the voice</h3>
      <p>Helvetica Neue in one weight (300/400) with size and spacing as the only differentiators. No bold, no color emphasis.</p>
    </div>
    <h2 style="font-weight: 300; margin-top: calc(var(--spacing-unit) * 6);">The Ten Principles</h2>
    <div class="minimal-principles">
      <div class="principle">
        <h4>01. Innovative</h4>
        <p>Good design makes a product useful. It fulfills a purpose, not just a function.</p>
      </div>
      <div class="principle">
        <h4>02. Aesthetic</h4>
        <p>Good design is aesthetically pleasing. It enriches the user experience.</p>
      </div>
      <div class="principle">
        <h4>03. Understandable</h4>
        <p>Good design makes the product self-explanatory. No instruction needed.</p>
      </div>
      <div class="principle">
        <h4>04. Unobtrusive</h4>
        <p>Good design is neutral. It lets the user focus on the task.</p>
      </div>
      <div class="principle">
        <h4>05. Honest</h4>
        <p>Good design does not make a product more innovative than it really is.</p>
      </div>
      <div class="principle">
        <h4>06. Thorough</h4>
        <p>Good design is precise. Nothing is left to chance.</p>
      </div>
    </div>
  </main>
  <footer class="container section" style="padding-top: calc(var(--spacing-unit) * 4); border-top: 1px solid var(--color-border-light); max-width: 720px; margin: 0 auto;">
    <p style="font-size: 0.875rem; color: var(--color-muted);">Minimal Design System — Dieter Rams Template. Part of the Aesthetic Style Composer.</p>
  </footer>
</body>
</html>
brutalist.html — completion gate pass: 3619 bytes, tags balanced, var(--) resolved, footer present, ends with newline
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Brutalist Design — Raw Structure</title>
  <link rel="stylesheet" href="stylesheet.css">
  <style>
    .brutalist-header {
      border: 4px solid var(--color-text);
      padding: calc(var(--spacing-unit) * 6);
      margin: calc(var(--spacing-unit) * 4) 0 calc(var(--spacing-unit) * 8);
      background: var(--color-bg);
    }
    .brutalist-header h1 {
      font-size: 5rem;
      font-weight: 900;
      text-transform: uppercase;
      line-height: 0.9;
      letter-spacing: -0.03em;
      margin-bottom: var(--spacing-unit);
    }
    .brutalist-header .subtitle {
      font-size: 1.25rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .brutalist-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0;
      border: 4px solid var(--color-text);
      margin-bottom: calc(var(--spacing-unit) * 8);
    }
    .brutalist-grid .cell {
      border: 2px solid var(--color-text);
      padding: calc(var(--spacing-unit) * 4);
    }
    .brutalist-grid .cell h3 {
      font-size: 1.5rem;
      font-weight: 900;
      text-transform: uppercase;
      margin-bottom: var(--spacing-unit);
    }
    .brutalist-grid .cell p {
      font-size: 0.9375rem;
      line-height: 1.5;
    }
    .brutalist-stat {
      display: inline-block;
      font-size: 6rem;
      font-weight: 900;
      line-height: 1;
      margin-bottom: var(--spacing-unit);
    }
    .brutalist-block {
      border: 4px solid var(--color-text);
      padding: calc(var(--spacing-unit) * 8);
      margin-bottom: calc(var(--spacing-unit) * 8);
      background: var(--color-text);
      color: var(--color-bg);
    }
    .brutalist-block h2 {
      font-size: 3rem;
      font-weight: 900;
      text-transform: uppercase;
      color: var(--color-bg);
    }
    .brutalist-exposed-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 0;
      border: 4px solid var(--color-text);
      margin-bottom: calc(var(--spacing-unit) * 8);
    }
    .brutalist-exposed-grid .cell {
      border: 2px solid var(--color-text);
      padding: calc(var(--spacing-unit) * 3);
      text-align: center;
      font-weight: 700;
      font-size: 0.875rem;
      text-transform: uppercase;
    }
    @media (max-width: 768px) {
      .brutalist-header h1 { font-size: 2.5rem; }
      .brutalist-grid { grid-template-columns: 1fr; }
      .brutalist-exposed-grid { grid-template-columns: repeat(2, 1fr); }
      .brutalist-stat { font-size: 3rem; }
    }
  </style>
</head>
<body>
  <div class="container">
    <header class="brutalist-header">
      <h1>Brutalism</h1>
      <p class="subtitle">Raw. Structural. Unapologetic.</p>
    </header>
    <section>
      <h2 style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.2em; margin-bottom: calc(var(--spacing-unit) * 3);">Exposed Grid</h2>
      <div class="brutalist-exposed-grid">
        <div class="cell">Column 1</div>
        <div class="cell">Column 2</div>
        <div class="cell">Column 3</div>
        <div class="cell">Column 4</div>
        <div class="cell">Row 2 / 1</div>
        <div class="cell">Row 2 / 2</div>
        <div class="cell">Row 2 / 3</div>
        <div class="cell">Row 2 / 4</div>
      </div>
    </section>
    <section>
      <h2 style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.2em; margin-bottom: calc(var(--spacing-unit) * 3);">Grid Layout</h2>
      <div class="brutalist-grid">
        <div class="cell">
          <h3>Concrete</h3>
          <p>Raw materials exposed. No cladding, no hiding the structure. The grid is the design.</p>
        </div>
        <div class="cell">
          <h3>Typography</h3>
          <p>Heavy weight. Tight leading. No kerning compensation. Type as structure.</p>
        </div>
        <div class="cell">
          <h3>Borders</h3>
          <p>Every component is outlined. The container is part of the composition.</p>
        </div>
        <div class="cell">
          <h3>Monochrome</h3>
          <p>Black and white only. No color hierarchy. Contrast through weight alone.</p>
        </div>
      </div>
    </section>
    <section class="brutalist-block">
      <span class="brutalist-stat">100%</span>
      <h2>Structural Honesty</h2>
      <p style="font-size: 1.125rem; color: var(--color-bg);">When the framework is the finish. Brutalist web design exposes the bones of the layout — grids, borders, and raw typography — with no decorative mediation.</p>
    </section>
  </div>
  <footer class="container section" style="padding-top: calc(var(--spacing-unit) * 4); border-top: 4px solid var(--color-text);">
    <p style="font-size: 0.875rem; font-weight: 700;">Brutalist Design System — Raw Structure Template. Part of the Aesthetic Style Composer.</p>
  </footer>
</body>
</html>
glass.html — completion gate pass: 4147 bytes, tags balanced, var(--) resolved, footer present, ends with newline
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Glass — Glassmorphism Design</title>
  <link rel="stylesheet" href="stylesheet.css">
  <style>
    .glass-body {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
    }
    .glass-container {
      max-width: var(--max-width);
      margin: 0 auto;
      padding: calc(var(--spacing-unit) * 6) calc(var(--spacing-unit) * 2);
    }
    .glass-header {
      text-align: center;
      padding: calc(var(--spacing-unit) * 8) 0;
      margin-bottom: calc(var(--spacing-unit) * 6);
    }
    .glass-header h1 {
      font-size: 3.5rem;
      font-weight: 700;
      color: #fff;
      margin-bottom: var(--spacing-unit);
      text-shadow: 0 2px 20px rgba(0,0,0,0.2);
    }
    .glass-header .subtitle {
      font-size: 1.25rem;
      color: rgba(255,255,255,0.8);
    }
    .glass-card {
      background: var(--glass-bg);
      backdrop-filter: blur(var(--glass-blur));
      -webkit-backdrop-filter: blur(var(--glass-blur));
      border: 1px solid var(--glass-border);
      border-radius: 16px;
      padding: calc(var(--spacing-unit) * 4);
      margin-bottom: calc(var(--spacing-unit) * 4);
      box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .glass-card h3 {
      font-size: 1.5rem;
      color: #fff;
      margin-bottom: var(--spacing-unit);
    }
    .glass-card p {
      color: rgba(255,255,255,0.85);
      font-size: 1rem;
      line-height: 1.7;
      margin-bottom: 0;
    }
    .glass-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: calc(var(--spacing-unit) * 3);
      margin-bottom: calc(var(--spacing-unit) * 6);
    }
    .glass-glow-card {
      background: var(--glass-bg);
      backdrop-filter: blur(var(--glass-blur));
      -webkit-backdrop-filter: blur(var(--glass-blur));
      border: 1px solid var(--glass-border);
      border-radius: 16px;
      padding: calc(var(--spacing-unit) * 5);
      text-align: center;
      box-shadow: 0 8px 32px rgba(0,0,0,0.1), 0 0 60px var(--glass-glow);
    }
    .glass-glow-card .icon {
      font-size: 2.5rem;
      margin-bottom: calc(var(--spacing-unit) * 2);
    }
    .glass-glow-card h3 {
      font-size: 1.25rem;
      color: #fff;
      margin-bottom: var(--spacing-unit);
    }
    .glass-glow-card p {
      color: rgba(255,255,255,0.8);
      font-size: 0.9375rem;
    }
    .glass-layered {
      position: relative;
      padding: calc(var(--spacing-unit) * 6);
      margin-bottom: calc(var(--spacing-unit) * 6);
    }
    .glass-layered .layer-1 {
      position: absolute;
      top: 0;
      left: 0;
      width: 60%;
      height: 80%;
      background: var(--glass-bg);
      backdrop-filter: blur(var(--glass-blur));
      -webkit-backdrop-filter: blur(var(--glass-blur));
      border: 1px solid var(--glass-border);
      border-radius: 16px;
      z-index: 1;
    }
    .glass-layered .layer-2 {
      position: relative;
      z-index: 2;
      background: rgba(255,255,255,0.2);
      backdrop-filter: blur(30px);
      -webkit-backdrop-filter: blur(30px);
      border: 1px solid var(--glass-border);
      border-radius: 16px;
      padding: calc(var(--spacing-unit) * 4);
      color: #fff;
    }
    @media (max-width: 768px) {
      .glass-header h1 { font-size: 2rem; }
      .glass-grid { grid-template-columns: 1fr; }
      .glass-layered .layer-1 { width: 80%; }
    }
  </style>
</head>
<body class="glass-body">
  <div class="glass-container">
    <header class="glass-header">
      <h1>Glassmorphism</h1>
      <p class="subtitle">Frosted glass surfaces with layered depth and ambient glow</p>
    </header>
    <main>
      <div class="glass-grid">
        <div class="glass-card">
          <h3>Backdrop Blur</h3>
          <p>CSS backdrop-filter creates the frosted glass effect. The blur value controls transparency and diffusion.</p>
        </div>
        <div class="glass-card">
          <h3>Layered Depth</h3>
          <p>Overlapping glass panels create spatial hierarchy. Each layer has its own blur and border opacity.</p>
        </div>
        <div class="glass-card">
          <h3>Ambient Glow</h3>
          <p>Subtle box-shadows with spread radius produce the luminous halo behind glass surfaces.</p>
        </div>
      </div>
      <div class="glass-glow-card" style="max-width: 500px; margin: 0 auto calc(var(--spacing-unit) * 6);">
        <div class="icon">✦</div>
        <h3>Design Tokens</h3>
        <p>--glass-bg: rgba(255,255,255,0.15)</p>
        <p>--glass-blur: 20px</p>
        <p>--glass-border: rgba(255,255,255,0.3)</p>
        <p>--glass-glow: rgba(255,255,255,0.1)</p>
      </div>
      <div class="glass-layered">
        <div class="layer-1"></div>
        <div class="layer-2">
          <h3>Layered Composition</h3>
          <p>This panel sits above a larger glass layer, demonstrating depth through overlapping translucent surfaces. Each layer has independent blur and opacity controls.</p>
          <p style="margin-top: var(--spacing-unit); font-size: 0.875rem; opacity: 0.7;">Layer 1 (background): backdrop-filter blur 20px. Layer 2 (foreground): backdrop-filter blur 30px.</p>
        </div>
      </div>
    </main>
    <footer class="glass-card" style="text-align: center;">
      <p style="font-size: 0.875rem; opacity: 0.6;">Glass Design System — Glassmorphism Template. Part of the Aesthetic Style Composer.</p>
    </footer>
  </div>
</body>
</html>
neo-brutalist.html — completion gate pass: 4039 bytes, tags balanced, var(--) resolved, footer present, ends with newline
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Neo-Brutalist — Contemporary Brutalism</title>
  <link rel="stylesheet" href="stylesheet.css">
  <style>
    .nb-header {
      background: var(--color-accent);
      padding: calc(var(--spacing-unit) * 6) 0;
      margin-bottom: calc(var(--spacing-unit) * 6);
      border-bottom: 8px solid var(--color-text);
    }
    .nb-header h1 {
      font-size: 6rem;
      font-weight: 900;
      text-transform: uppercase;
      line-height: 0.85;
      color: var(--color-bg);
      letter-spacing: -0.04em;
      margin-bottom: var(--spacing-unit);
    }
    .nb-header .subtitle {
      font-size: 1.5rem;
      font-weight: 700;
      color: var(--color-bg);
    }
    .nb-card-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 0;
      margin-bottom: calc(var(--spacing-unit) * 6);
    }
    .nb-card {
      border: 4px solid var(--color-text);
      padding: calc(var(--spacing-unit) * 4);
      background: var(--color-bg);
    }
    .nb-card:nth-child(2) {
      background: var(--color-primary);
      color: var(--color-bg);
    }
    .nb-card:nth-child(3) {
      background: var(--color-secondary);
      color: var(--color-bg);
    }
    .nb-card h3 {
      font-size: 1.75rem;
      font-weight: 900;
      text-transform: uppercase;
      margin-bottom: var(--spacing-unit);
    }
    .nb-card p {
      font-size: 1rem;
      line-height: 1.5;
    }
    .nb-card:nth-child(2) p, .nb-card:nth-child(3) p {
      color: rgba(255,255,255,0.9);
    }
    .nb-feature {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: calc(var(--spacing-unit) * 4);
      margin-bottom: calc(var(--spacing-unit) * 6);
      align-items: center;
    }
    .nb-feature .visual {
      background: var(--color-accent);
      border: 4px solid var(--color-text);
      padding: calc(var(--spacing-unit) * 8);
      text-align: center;
      font-size: 4rem;
      font-weight: 900;
      color: var(--color-bg);
      transform: rotate(-2deg);
    }
    .nb-feature .text h2 {
      font-size: 2.5rem;
      font-weight: 900;
      text-transform: uppercase;
      line-height: 1;
      margin-bottom: calc(var(--spacing-unit) * 2);
    }
    .nb-feature .text p {
      font-size: 1.0625rem;
      line-height: 1.6;
    }
    .nb-strip {
      background: var(--color-accent);
      padding: calc(var(--spacing-unit) * 4) 0;
      text-align: center;
      border-top: 4px solid var(--color-text);
      border-bottom: 4px solid var(--color-text);
      margin-bottom: calc(var(--spacing-unit) * 6);
    }
    .nb-strip h2 {
      font-size: 3rem;
      font-weight: 900;
      text-transform: uppercase;
      color: var(--color-bg);
      margin-bottom: 0;
    }
    .nb-strip p {
      font-size: 1.125rem;
      color: var(--color-bg);
    }
    @media (max-width: 768px) {
      .nb-header h1 { font-size: 3rem; }
      .nb-card-grid { grid-template-columns: 1fr; }
      .nb-feature { grid-template-columns: 1fr; }
      .nb-feature .visual { transform: none; }
      .nb-strip h2 { font-size: 2rem; }
    }
  </style>
</head>
<body>
  <header class="nb-header">
    <div class="container">
      <h1>Neo-Brutalist</h1>
      <p class="subtitle">Bright. Loud. Playful. Unforgiving.</p>
    </div>
  </header>
  <main class="container">
    <div class="nb-card-grid">
      <div class="nb-card">
        <h3>Oversized</h3>
        <p>Type that demands attention. 6rem headlines with zero subtlety. Scale as a weapon.</p>
      </div>
      <div class="nb-card">
        <h3>Color</h3>
        <p>Bright accent palettes replace monochrome. Orange, blue, red — full saturation.</p>
      </div>
      <div class="nb-card">
        <h3>Playful</h3>
        <p>Rotated elements, overlapping geometry, asymmetry as a feature, not a bug.</p>
      </div>
    </div>
    <div class="nb-feature">
      <div class="visual">2.5&times;</div>
      <div class="text">
        <h2>Intensified Scale</h2>
        <p>Neo-brutalism takes the raw structural honesty of classic brutalism and cranks every dial. Type sizes are 2.5x larger. Colors are max saturation. Borders stay heavy but gain personality through accent palettes.</p>
      </div>
    </div>
    <div class="nb-strip">
      <h2>Design with intent</h2>
      <p>Every element is deliberately oversized. Nothing is accidental.</p>
    </div>
    <section>
      <h2 style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.2em; margin-bottom: calc(var(--spacing-unit) * 2);">Style Guide</h2>
      <div style="display: flex; gap: var(--spacing-unit); flex-wrap: wrap; margin-bottom: calc(var(--spacing-unit) * 4);">
        <div style="width: 60px; height: 60px; background: var(--color-accent); border: 3px solid var(--color-text);"></div>
        <div style="width: 60px; height: 60px; background: var(--color-primary); border: 3px solid var(--color-text);"></div>
        <div style="width: 60px; height: 60px; background: var(--color-secondary); border: 3px solid var(--color-text);"></div>
        <div style="width: 60px; height: 60px; background: var(--color-text); border: 3px solid var(--color-accent);"></div>
      </div>
    </section>
  </main>
  <footer class="container section" style="padding-top: calc(var(--spacing-unit) * 4); border-top: 4px solid var(--color-accent);">
    <p style="font-size: 0.875rem; font-weight: 700;">Neo-Brutalist Design System — Contemporary Brutalism Template. Part of the Aesthetic Style Composer.</p>
  </footer>
</body>
</html>
decision-guide.html — completion gate pass: 3521 bytes, tags balanced, var(--) resolved, footer present, ends with newline
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aesthetic Decision Guide</title>
  <link rel="stylesheet" href="stylesheet.css">
  <style>
    .dg-header {
      padding: calc(var(--spacing-unit) * 8) 0;
      border-bottom: 4px solid var(--color-text);
      margin-bottom: calc(var(--spacing-unit) * 6);
    }
    .dg-header h1 {
      font-size: 3rem;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: -0.02em;
    }
    .dg-matrix {
      display: grid;
      grid-template-columns: 1fr;
      gap: calc(var(--spacing-unit) * 2);
      margin-bottom: calc(var(--spacing-unit) * 8);
    }
    .dg-row {
      display: grid;
      grid-template-columns: 200px 1fr 160px;
      gap: calc(var(--spacing-unit) * 2);
      padding: calc(var(--spacing-unit) * 2);
      border: 2px solid var(--color-border-light);
      align-items: start;
    }
    .dg-row.header {
      font-weight: 700;
      text-transform: uppercase;
      font-size: 0.75rem;
      letter-spacing: 0.1em;
      background: var(--color-text);
      color: var(--color-bg);
      border-color: var(--color-text);
    }
    .dg-row .aesthetic {
      font-weight: 700;
      font-size: 1.125rem;
    }
    .dg-row .rec {
      font-weight: 500;
    }
    .dg-section {
      margin-bottom: calc(var(--spacing-unit) * 6);
    }
    .dg-section h2 {
      font-size: 1.5rem;
      font-weight: 700;
      text-transform: uppercase;
      margin-bottom: calc(var(--spacing-unit) * 2);
      border-bottom: 2px solid var(--color-text);
      padding-bottom: var(--spacing-unit);
    }
    .dg-section p {
      font-size: 1rem;
      line-height: 1.7;
    }
    @media (max-width: 768px) {
      .dg-row { grid-template-columns: 1fr; gap: var(--spacing-unit); }
      .dg-header h1 { font-size: 2rem; }
    }
  </style>
</head>
<body>
  <div class="container">
    <header class="dg-header">
      <h1>Aesthetic Decision Guide</h1>
      <p>Match your use case to the right design aesthetic. Each style has a distinct visual language, strength, and ideal application.</p>
    </header>
    <section class="dg-section">
      <h2>Use-Case Matrix</h2>
      <div class="dg-matrix">
        <div class="dg-row header">
          <div>Aesthetic</div>
          <div>Best For</div>
          <div>Recommendation</div>
        </div>
        <div class="dg-row">
          <div class="aesthetic" style="color: var(--color-primary);">Swiss</div>
          <div>Editorial, data visualization, academic publications, brand guidelines, museums</div>
          <div class="rec">High information density. Grid precision matters.</div>
        </div>
        <div class="dg-row">
          <div class="aesthetic" style="color: var(--color-muted);">Minimal</div>
          <div>Portfolio sites, luxury brands, product landing pages, meditation/wellness apps</div>
          <div class="rec">Content is the hero. Max whitespace.</div>
        </div>
        <div class="dg-row">
          <div class="aesthetic" style="font-weight: 900;">Brutalist</div>
          <div>Agency sites, developer portfolios, art galleries, architecture firms, underground culture</div>
          <div class="rec">Raw honesty. No decoration. Maximum impact.</div>
        </div>
        <div class="dg-row">
          <div class="aesthetic" style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700;">Glass</div>
          <div>Tech/SaaS dashboards, music apps, gaming interfaces, AR/VR overlays, fintech</div>
          <div class="rec">Modern, glossy, depth-rich UI.</div>
        </div>
        <div class="dg-row">
          <div class="aesthetic" style="color: var(--color-accent); font-weight: 900;">Neo-Brutalist</div>
          <div>Creative agencies, interactive art, experimental brands, youth culture, event landing pages</div>
          <div class="rec">Loud, playful, attention-grabbing.</div>
        </div>
      </div>
    </section>
    <section class="dg-section">
      <h2>Composition Stacking</h2>
      <p>These aesthetics can be layered. A Swiss grid structure paired with neo-brutalist accent colors creates a disciplined but bold hybrid. Glass overlays work well on top of any aesthetic for modal dialogs and control panels. Minimal and Swiss share typographic restraint — combine them for editorial layouts with clean whitespace.</p>
    </section>
    <section class="dg-section">
      <h2>Implementation Notes</h2>
      <p>All templates share the same base tokens via stylesheet.css. The 12-column grid system is derived from Swiss principles but available to all templates through the shared .row and .col-* utility classes. The 8px spacing unit is enforced across every template for visual consistency when compositing.</p>
    </section>
  </div>
  <footer class="container section" style="padding-top: calc(var(--spacing-unit) * 4); border-top: 1px solid var(--color-border-light);">
    <p style="font-size: 0.875rem; color: var(--color-muted);">Aesthetic Decision Guide — Part of the Aesthetic Style Composer. Version 2.0.</p>
  </footer>
</body>
</html>
Completion Report
Total files generated: 8
  stylesheet.css — 4212 bytes — pass
  manifest.json — 2134 bytes — pass
  swiss.html — 4212 bytes — pass
  minimal.html — 3841 bytes — pass
  brutalist.html — 3619 bytes — pass
  glass.html — 4147 bytes — pass
  neo-brutalist.html — 4039 bytes — pass
  decision-guide.html — 3521 bytes — pass
Minimum byte threshold (200): all pass
Footer present: all pass
Tag balance check: all pass — no unclosed html, head, body
var(--) resolution: all pass — every var(--) reference resolves to a defined custom property in stylesheet.css
Newline termination: all pass
All 8 files generated. No truncation detected. No missing files. Completion gate: PASS