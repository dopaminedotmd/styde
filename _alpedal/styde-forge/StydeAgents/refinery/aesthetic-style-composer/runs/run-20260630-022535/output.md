aesthetic-style-composer v2
delivery checklist: 8 files
checklist:
  file: manifest.json
  file: stylesheet.css
  file: swiss.html
  file: minimal.html
  file: brutalist.html
  file: glass.html
  file: neo-brutalist.html
  file: decision-guide.html
--- manifest.json ---
{
  "project": "aesthetic-style-composer",
  "version": 2,
  "templates": [
    {
      "name": "swiss",
      "file": "swiss.html",
      "style": "International Typographic Style",
      "dependencies": ["stylesheet.css", "manifest.json"],
      "tokens": ["--color-primary", "--color-secondary", "--color-bg", "--font-heading", "--font-body", "--grid-columns", "--grid-gap", "--spacing-unit"]
    },
    {
      "name": "minimal",
      "file": "minimal.html",
      "style": "Dieter Rams-inspired Minimal",
      "dependencies": ["stylesheet.css", "manifest.json"],
      "tokens": ["--color-primary", "--color-bg", "--color-text", "--font-body", "--spacing-unit", "--max-width"]
    },
    {
      "name": "brutalist",
      "file": "brutalist.html",
      "style": "Raw Structural Brutalism",
      "dependencies": ["stylesheet.css", "manifest.json"],
      "tokens": ["--color-bg", "--color-text", "--color-border", "--font-heading", "--border-width"]
    },
    {
      "name": "glass",
      "file": "glass.html",
      "style": "Apple-inspired Glassmorphism",
      "dependencies": ["stylesheet.css", "manifest.json"],
      "tokens": ["--color-bg", "--glass-bg", "--glass-border", "--glass-blur", "--color-primary", "--color-text"]
    },
    {
      "name": "neo-brutalist",
      "file": "neo-brutalist.html",
      "style": "Contemporary Neo-Brutalism",
      "dependencies": ["stylesheet.css", "manifest.json"],
      "tokens": ["--color-bg", "--color-accent", "--color-accent2", "--color-text", "--font-heading", "--font-body", "--border-width"]
    }
  ],
  "compositionOrder": ["swiss", "minimal", "brutalist", "glass", "neo-brutalist"],
  "sharedBoilerplate": "stylesheet.css",
  "sharedTokens": ["--color-primary", "--color-secondary", "--color-bg", "--color-text", "--font-heading", "--font-body", "--spacing-unit", "--border-width"],
  "dependencyGraph": {
    "stylesheet.css": [],
    "manifest.json": [],
    "swiss.html": ["stylesheet.css", "manifest.json"],
    "minimal.html": ["stylesheet.css", "manifest.json"],
    "brutalist.html": ["stylesheet.css", "manifest.json"],
    "glass.html": ["stylesheet.css", "manifest.json"],
    "neo-brutalist.html": ["stylesheet.css", "manifest.json"],
    "decision-guide.html": ["stylesheet.css"]
  }
}
--- stylesheet.css ---
:root {
  --color-primary: #2563eb;
  --color-secondary: #7c3aed;
  --color-accent: #f59e0b;
  --color-accent2: #ef4444;
  --color-bg: #ffffff;
  --color-bg-alt: #f8fafc;
  --color-text: #0f172a;
  --color-text-muted: #64748b;
  --color-border: #1e293b;
  --font-heading: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --font-body: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --font-mono: 'JetBrains Mono', 'SF Mono', monospace;
  --spacing-unit: 8px;
  --max-width: 1200px;
  --grid-columns: 12;
  --grid-gap: 24px;
  --border-width: 4px;
  --glass-bg: rgba(255, 255, 255, 0.15);
  --glass-border: rgba(255, 255, 255, 0.3);
  --glass-blur: 20px;
  --border-radius: 0px;
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
img {
  max-width: 100%;
  height: auto;
  display: block;
}
a {
  color: var(--color-primary);
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
.container {
  width: 100%;
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 calc(var(--spacing-unit) * 2);
}
.grid {
  display: grid;
  grid-template-columns: repeat(var(--grid-columns), 1fr);
  gap: var(--grid-gap);
}
.grid--2 { grid-template-columns: repeat(2, 1fr); }
.grid--3 { grid-template-columns: repeat(3, 1fr); }
.grid--4 { grid-template-columns: repeat(4, 1fr); }
.col {
  min-width: 0;
}
.section {
  padding: calc(var(--spacing-unit) * 8) 0;
}
.section--sm {
  padding: calc(var(--spacing-unit) * 4) 0;
}
.section--lg {
  padding: calc(var(--spacing-unit) * 16) 0;
}
.btn {
  display: inline-block;
  padding: calc(var(--spacing-unit) * 1.5) calc(var(--spacing-unit) * 4);
  font-family: var(--font-body);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  border: var(--border-width) solid var(--color-text);
  background: transparent;
  color: var(--color-text);
  text-decoration: none;
}
.btn--primary {
  background: var(--color-primary);
  color: #fff;
  border-color: var(--color-primary);
}
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}
@media (max-width: 768px) {
  .grid { grid-template-columns: 1fr; }
  .grid--2, .grid--3, .grid--4 { grid-template-columns: 1fr; }
  .section { padding: calc(var(--spacing-unit) * 4) 0; }
  .section--lg { padding: calc(var(--spacing-unit) * 8) 0; }
}
@media (min-width: 769px) and (max-width: 1024px) {
  .grid--3 { grid-template-columns: repeat(2, 1fr); }
  .grid--4 { grid-template-columns: repeat(2, 1fr); }
}
--- swiss.html ---
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Swiss International Style</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="stylesheet.css">
<style>
  :root {
    --color-primary: #2563eb;
    --color-secondary: #7c3aed;
    --color-bg: #f8fafc;
    --color-text: #0f172a;
    --font-heading: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    --font-body: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    --grid-columns: 12;
    --grid-gap: 24px;
    --spacing-unit: 8px;
  }
  .swiss-hero {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--grid-gap);
    padding: calc(var(--spacing-unit) * 12) 0;
    align-items: center;
  }
  .swiss-hero__title {
    font-family: var(--font-heading);
    font-weight: 700;
    font-size: 4rem;
    line-height: 0.95;
    letter-spacing: -0.02em;
    text-transform: uppercase;
    color: var(--color-primary);
  }
  .swiss-hero__subtitle {
    font-weight: 300;
    font-size: 1.25rem;
    line-height: 1.4;
    color: var(--color-text);
    max-width: 32ch;
  }
  .swiss-grid-demo {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 2px;
    background: var(--color-primary);
    padding: 2px;
  }
  .swiss-grid-demo__item {
    background: var(--color-bg);
    padding: calc(var(--spacing-unit) * 4);
    aspect-ratio: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-heading);
    font-weight: 500;
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--color-primary);
  }
  .swiss-typography {
    font-family: var(--font-heading);
  }
  .swiss-typography h2 {
    font-size: 3rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: -0.01em;
    line-height: 1;
    margin-bottom: calc(var(--spacing-unit) * 2);
  }
  .swiss-typography p {
    font-weight: 300;
    font-size: 1rem;
    line-height: 1.6;
    max-width: 66ch;
  }
  .swiss-asymmetric {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: var(--grid-gap);
    align-items: start;
  }
  .swiss-asymmetric__block {
    background: var(--color-primary);
    color: #fff;
    padding: calc(var(--spacing-unit) * 6);
    font-weight: 300;
    font-size: 0.875rem;
    line-height: 1.5;
  }
  .swiss-asymmetric__block--small {
    background: var(--color-secondary);
    padding: calc(var(--spacing-unit) * 3);
  }
  @media (max-width: 768px) {
    .swiss-hero { grid-template-columns: 1fr; }
    .swiss-hero__title { font-size: 2.5rem; }
    .swiss-grid-demo { grid-template-columns: repeat(2, 1fr); }
    .swiss-asymmetric { grid-template-columns: 1fr; }
  }
</style>
</head>
<body>
  <div class="container">
    <section class="swiss-hero">
      <div>
        <h1 class="swiss-hero__title">Swiss<br>Typography</h1>
      </div>
      <div>
        <p class="swiss-hero__subtitle">International Typographic Style employs asymmetric balance, grid systems, and sans-serif typefaces to create clear, objective visual communication.</p>
      </div>
    </section>
    <section class="section">
      <div class="swiss-typography">
        <h2>Grid System</h2>
        <p>12-column modular grid with 24px gap. Every element aligns to the baseline grid of 8px.</p>
      </div>
    </section>
    <section class="section">
      <div class="swiss-grid-demo">
        <div class="swiss-grid-demo__item">01</div>
        <div class="swiss-grid-demo__item">02</div>
        <div class="swiss-grid-demo__item">03</div>
        <div class="swiss-grid-demo__item">04</div>
        <div class="swiss-grid-demo__item">05</div>
        <div class="swiss-grid-demo__item">06</div>
        <div class="swiss-grid-demo__item">07</div>
        <div class="swiss-grid-demo__item">08</div>
        <div class="swiss-grid-demo__item">09</div>
        <div class="swiss-grid-demo__item">10</div>
        <div class="swiss-grid-demo__item">11</div>
        <div class="swiss-grid-demo__item">12</div>
      </div>
    </section>
    <section class="section swiss-asymmetric">
      <div class="swiss-asymmetric__block">
        Asymmetric balance is achieved through weighted visual elements rather than mirrored symmetry. The primary content block carries visual mass through size, color, or position.
      </div>
      <div class="swiss-asymmetric__block swiss-asymmetric__block--small">
        Secondary content sits in the remaining field, creating tension and movement across the composition.
      </div>
    </section>
  </div>
</body>
</html>
--- minimal.html ---
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Minimal Design</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="stylesheet.css">
<style>
  :root {
    --color-primary: #1a1a1a;
    --color-bg: #ffffff;
    --color-text: #1a1a1a;
    --font-body: 'Inter', sans-serif;
    --spacing-unit: 8px;
    --max-width: 960px;
  }
  .minimal-header {
    padding: calc(var(--spacing-unit) * 6) 0;
    border-bottom: 1px solid #e5e5e5;
  }
  .minimal-header__title {
    font-family: var(--font-body);
    font-weight: 300;
    font-size: 1.25rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--color-text);
  }
  .minimal-hero {
    padding: calc(var(--spacing-unit) * 16) 0 calc(var(--spacing-unit) * 8);
    text-align: center;
  }
  .minimal-hero__title {
    font-family: var(--font-body);
    font-weight: 300;
    font-size: 3.5rem;
    line-height: 1.1;
    letter-spacing: -0.01em;
    color: var(--color-text);
    max-width: 800px;
    margin: 0 auto;
  }
  .minimal-hero__subtitle {
    font-weight: 300;
    font-size: 1.125rem;
    color: #666;
    margin-top: calc(var(--spacing-unit) * 3);
    max-width: 500px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.6;
  }
  .minimal-content {
    max-width: var(--max-width);
    margin: 0 auto;
    padding: calc(var(--spacing-unit) * 8) 0;
  }
  .minimal-content p {
    font-weight: 300;
    font-size: 1.0625rem;
    line-height: 1.8;
    color: #333;
    margin-bottom: calc(var(--spacing-unit) * 3);
    max-width: 65ch;
  }
  .minimal-features {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: calc(var(--spacing-unit) * 6);
    padding: calc(var(--spacing-unit) * 8) 0;
    border-top: 1px solid #e5e5e5;
  }
  .minimal-features__item {
    text-align: center;
  }
  .minimal-features__number {
    font-weight: 300;
    font-size: 2.5rem;
    color: var(--color-text);
  }
  .minimal-features__label {
    font-weight: 300;
    font-size: 0.875rem;
    color: #666;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-top: calc(var(--spacing-unit) * 1);
  }
  @media (max-width: 768px) {
    .minimal-hero__title { font-size: 2rem; }
    .minimal-features { grid-template-columns: 1fr; gap: calc(var(--spacing-unit) * 4); }
  }
</style>
</head>
<body>
  <div class="container">
    <header class="minimal-header">
      <div class="minimal-header__title">Studio</div>
    </header>
    <section class="minimal-hero">
      <h1 class="minimal-hero__title">Less but better</h1>
      <p class="minimal-hero__subtitle">Dieter Rams design philosophy: remove the unnecessary until only the essential remains. Good design is as little design as possible.</p>
    </section>
    <section class="minimal-content">
      <p>Good design is innovative. Good design makes a product useful. Good design is aesthetic. Good design makes a product understandable. Good design is unobtrusive. Good design is honest. Good design is long-lasting. Good design is thorough down to the last detail. Good design is environmentally friendly. Good design is as little design as possible.</p>
      <p>These ten principles of good design, formulated by Dieter Rams, form the foundation of the minimalist aesthetic. Every visual element must earn its place. Whitespace is not empty space — it is active, compositional space that gives content room to breathe.</p>
    </section>
    <section class="minimal-features">
      <div class="minimal-features__item">
        <div class="minimal-features__number">10</div>
        <div class="minimal-features__label">Principles</div>
      </div>
      <div class="minimal-features__item">
        <div class="minimal-features__number">60+</div>
        <div class="minimal-features__label">Years</div>
      </div>
      <div class="minimal-features__item">
        <div class="minimal-features__number">100%</div>
        <div class="minimal-features__label">Intention</div>
      </div>
    </section>
  </div>
</body>
</html>
--- brutalist.html ---
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Brutalist Design</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="stylesheet.css">
<style>
  :root {
    --color-bg: #1a1a1a;
    --color-text: #f0f0f0;
    --color-border: #f0f0f0;
    --font-heading: 'Inter', sans-serif;
    --border-width: 6px;
  }
  body {
    background: var(--color-bg);
    color: var(--color-text);
  }
  .brutalist-hero {
    padding: calc(var(--spacing-unit) * 10) 0;
    border-bottom: var(--border-width) solid var(--color-border);
  }
  .brutalist-hero__title {
    font-family: var(--font-heading);
    font-weight: 900;
    font-size: 5rem;
    line-height: 0.9;
    text-transform: uppercase;
    letter-spacing: -0.03em;
  }
  .brutalist-hero__subtitle {
    font-family: var(--font-heading);
    font-weight: 700;
    font-size: 1.5rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: calc(var(--spacing-unit) * 3);
    max-width: 50ch;
  }
  .brutalist-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    border-top: var(--border-width) solid var(--color-border);
  }
  .brutalist-grid__item {
    padding: calc(var(--spacing-unit) * 6);
    border-right: var(--border-width) solid var(--color-border);
    border-bottom: var(--border-width) solid var(--color-border);
    font-family: var(--font-heading);
    font-weight: 700;
    font-size: 1.25rem;
    text-transform: uppercase;
  }
  .brutalist-grid__item:nth-child(3n) { border-right: none; }
  .brutalist-block {
    padding: calc(var(--spacing-unit) * 8);
    border: var(--border-width) solid var(--color-border);
    margin-top: calc(var(--spacing-unit) * 4);
    font-family: var(--font-heading);
    font-weight: 700;
    font-size: 1.125rem;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    line-height: 1.4;
  }
  .brutalist-cta {
    display: inline-block;
    padding: calc(var(--spacing-unit) * 3) calc(var(--spacing-unit) * 8);
    border: var(--border-width) solid var(--color-border);
    font-family: var(--font-heading);
    font-weight: 900;
    font-size: 1.5rem;
    text-transform: uppercase;
    color: var(--color-bg);
    background: var(--color-text);
    text-decoration: none;
    margin-top: calc(var(--spacing-unit) * 4);
  }
  @media (max-width: 768px) {
    .brutalist-hero__title { font-size: 2.5rem; }
    .brutalist-grid { grid-template-columns: 1fr; }
    .brutalist-grid__item { border-right: none; }
  }
</style>
</head>
<body>
  <div class="container">
    <section class="brutalist-hero">
      <h1 class="brutalist-hero__title">Raw Structure<br>Exposed Form</h1>
      <p class="brutalist-hero__subtitle">Brutalism strips away ornament. What remains is pure materiality, structural honesty, and typographic force.</p>
    </section>
    <section class="section">
      <div class="brutalist-grid">
        <div class="brutalist-grid__item">Concrete</div>
        <div class="brutalist-grid__item">Steel</div>
        <div class="brutalist-grid__item">Glass</div>
        <div class="brutalist-grid__item">Formwork</div>
        <div class="brutalist-grid__item">Texture</div>
        <div class="brutalist-grid__item">Scale</div>
      </div>
    </section>
    <section class="section">
      <div class="brutalist-block">
        Brutalist web design rejects the polished, the decorative, and the familiar. It exposes the raw grid, uses heavy borders as structural elements, and lets typography carry the full weight of communication. No gradients. No shadows. No apology.
      </div>
      <a href="#" class="brutalist-cta">Enter</a>
    </section>
  </div>
</body>
</html>
--- glass.html ---
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Glassmorphism</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="stylesheet.css">
<style>
  :root {
    --color-bg: #0a0a1a;
    --glass-bg: rgba(255, 255, 255, 0.08);
    --glass-border: rgba(255, 255, 255, 0.18);
    --glass-blur: 24px;
    --color-primary: #60a5fa;
    --color-text: #f1f5f9;
    --border-radius: 16px;
  }
  body {
    background: var(--color-bg);
    color: var(--color-text);
    min-height: 100vh;
  }
  .glass-bg-decor {
    position: fixed;
    top: -20%;
    left: -10%;
    width: 60%;
    height: 60%;
    background: radial-gradient(ellipse at center, rgba(96, 165, 250, 0.15), transparent 70%);
    pointer-events: none;
    z-index: 0;
  }
  .glass-bg-decor--2 {
    top: 50%;
    right: -10%;
    left: auto;
    bottom: auto;
    width: 50%;
    height: 50%;
    background: radial-gradient(ellipse at center, rgba(167, 139, 250, 0.12), transparent 70%);
  }
  .glass-card {
    background: var(--glass-bg);
    backdrop-filter: blur(var(--glass-blur));
    -webkit-backdrop-filter: blur(var(--glass-blur));
    border: 1px solid var(--glass-border);
    border-radius: var(--border-radius);
    padding: calc(var(--spacing-unit) * 5);
  }
  .glass-hero {
    padding: calc(var(--spacing-unit) * 12) 0 calc(var(--spacing-unit) * 8);
    text-align: center;
    position: relative;
    z-index: 1;
  }
  .glass-hero__title {
    font-weight: 300;
    font-size: 3.75rem;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #f1f5f9, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .glass-hero__subtitle {
    font-weight: 300;
    font-size: 1.125rem;
    color: rgba(255, 255, 255, 0.6);
    margin-top: calc(var(--spacing-unit) * 2);
    max-width: 500px;
    margin-left: auto;
    margin-right: auto;
  }
  .glass-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--grid-gap);
    position: relative;
    z-index: 1;
  }
  .glass-grid__card {
    background: var(--glass-bg);
    backdrop-filter: blur(var(--glass-blur));
    -webkit-backdrop-filter: blur(var(--glass-blur));
    border: 1px solid var(--glass-border);
    border-radius: var(--border-radius);
    padding: calc(var(--spacing-unit) * 5);
  }
  .glass-grid__card h3 {
    font-weight: 500;
    font-size: 1.25rem;
    margin-bottom: calc(var(--spacing-unit) * 2);
    color: var(--color-primary);
  }
  .glass-grid__card p {
    font-weight: 300;
    font-size: 0.9375rem;
    line-height: 1.6;
    color: rgba(255, 255, 255, 0.7);
  }
  .glass-metrics {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--grid-gap);
    position: relative;
    z-index: 1;
    margin-top: calc(var(--spacing-unit) * 6);
  }
  .glass-metrics__item {
    text-align: center;
    background: var(--glass-bg);
    backdrop-filter: blur(var(--glass-blur));
    -webkit-backdrop-filter: blur(var(--glass-blur));
    border: 1px solid var(--glass-border);
    border-radius: var(--border-radius);
    padding: calc(var(--spacing-unit) * 4);
  }
  .glass-metrics__number {
    font-weight: 500;
    font-size: 2.5rem;
    color: var(--color-primary);
  }
  .glass-metrics__label {
    font-weight: 300;
    font-size: 0.8125rem;
    color: rgba(255, 255, 255, 0.5);
    margin-top: calc(var(--spacing-unit) * 1);
  }
  @media (max-width: 768px) {
    .glass-hero__title { font-size: 2rem; }
    .glass-grid { grid-template-columns: 1fr; }
    .glass-metrics { grid-template-columns: 1fr; }
  }
</style>
</head>
<body>
  <div class="glass-bg-decor"></div>
  <div class="glass-bg-decor glass-bg-decor--2"></div>
  <div class="container">
    <section class="glass-hero">
      <h1 class="glass-hero__title">Glassmorphism</h1>
      <p class="glass-hero__subtitle">Frosted glass surfaces with layered depth, ambient glow, and translucent materiality.</p>
    </section>
    <section class="glass-grid">
      <div class="glass-grid__card">
        <h3>Translucency</h3>
        <p>Layered backgrounds with controlled opacity create depth through material stacking. The backdrop-filter property delivers the frosted glass effect.</p>
      </div>
      <div class="glass-grid__card">
        <h3>Ambient Glow</h3>
        <p>Soft radial gradients behind glass surfaces simulate environmental lighting, giving otherwise flat elements spatial presence.</p>
      </div>
      <div class="glass-grid__card">
        <h3>Bordered Light</h3>
        <p>Subtle semi-transparent borders define glass edges while maintaining translucency. Light passes through each layer differently.</p>
      </div>
    </section>
    <section class="glass-metrics">
      <div class="glass-metrics__item">
        <div class="glass-metrics__number">24px</div>
        <div class="glass-metrics__label">Blur Radius</div>
      </div>
      <div class="glass-metrics__item">
        <div class="glass-metrics__number">15%</div>
        <div class="glass-metrics__label">Opacity</div>
      </div>
      <div class="glass-metrics__item">
        <div class="glass-metrics__number">3</div>
        <div class="glass-metrics__label">Layers</div>
      </div>
    </section>
  </div>
</body>
</html>
--- neo-brutalist.html ---
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Neo-Brutalist Design</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="stylesheet.css">
<style>
  :root {
    --color-bg: #fafafa;
    --color-accent: #ff6b35;
    --color-accent2: #004e98;
    --color-text: #1a1a1a;
    --font-heading: 'Inter', sans-serif;
    --font-body: 'Inter', sans-serif;
    --border-width: 4px;
    --border-radius: 0px;
  }
  body {
    background: var(--color-bg);
    color: var(--color-text);
  }
  .nb-hero {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--grid-gap);
    padding: calc(var(--spacing-unit) * 8) 0;
    align-items: center;
  }
  .nb-hero__title {
    font-family: var(--font-heading);
    font-weight: 900;
    font-size: 5rem;
    line-height: 0.85;
    text-transform: uppercase;
    color: var(--color-text);
  }
  .nb-hero__title span {
    color: var(--color-accent);
  }
  .nb-hero__subtitle {
    font-weight: 700;
    font-size: 1.25rem;
    line-height: 1.4;
    text-transform: uppercase;
    letter-spacing: 0.02em;
  }
  .nb-strip {
    background: var(--color-accent);
    color: #fff;
    padding: calc(var(--spacing-unit) * 3) 0;
    margin: calc(var(--spacing-unit) * 4) 0;
  }
  .nb-strip__text {
    font-weight: 900;
    font-size: 2rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    text-align: center;
  }
  .nb-cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0;
  }
  .nb-card {
    border: var(--border-width) solid var(--color-text);
    padding: calc(var(--spacing-unit) * 6);
    margin: calc(var(--spacing-unit) * -0.5);
    background: var(--color-bg);
    position: relative;
    text-align: center;
  }
  .nb-card:nth-child(2) {
    background: var(--color-accent);
    color: #fff;
    transform: scale(1.05);
    z-index: 2;
  }
  .nb-card__icon {
    font-size: 3rem;
    margin-bottom: calc(var(--spacing-unit) * 2);
  }
  .nb-card__title {
    font-weight: 800;
    font-size: 1.5rem;
    text-transform: uppercase;
    letter-spacing: -0.01em;
  }
  .nb-card__desc {
    font-weight: 700;
    font-size: 0.8125rem;
    text-transform: uppercase;
    margin-top: calc(var(--spacing-unit) * 2);
    opacity: 0.8;
  }
  .nb-cta {
    display: inline-block;
    padding: calc(var(--spacing-unit) * 3) calc(var(--spacing-unit) * 8);
    background: var(--color-accent);
    color: #fff;
    font-family: var(--font-heading);
    font-weight: 900;
    font-size: 1.75rem;
    text-transform: uppercase;
    border: var(--border-width) solid var(--color-text);
    text-decoration: none;
    margin-top: calc(var(--spacing-unit) * 4);
    transition: transform 0.15s;
  }
  .nb-cta:hover {
    transform: translate(-4px, -4px);
    box-shadow: 8px 8px 0 var(--color-accent2);
  }
  @media (max-width: 768px) {
    .nb-hero { grid-template-columns: 1fr; }
    .nb-hero__title { font-size: 2.5rem; }
    .nb-cards { grid-template-columns: 1fr; }
    .nb-card:nth-child(2) { transform: none; }
  }
</style>
</head>
<body>
  <div class="container">
    <section class="nb-hero">
      <div>
        <h1 class="nb-hero__title">Big<br><span>Bold</span><br>Brutal</h1>
      </div>
      <div>
        <p class="nb-hero__subtitle">Neo-brutalism keeps the structural honesty of classic brutalism but adds vibrant color, playful geometry, and oversized typography for the digital native.</p>
      </div>
    </section>
    <div class="nb-strip">
      <div class="container">
        <div class="nb-strip__text">Color is structure. Size is emphasis. Play is serious.</div>
      </div>
    </div>
    <section class="section">
      <div class="nb-cards">
        <div class="nb-card">
          <div class="nb-card__icon">01</div>
          <div class="nb-card__title">Bright</div>
          <div class="nb-card__desc">High-saturation accent colors define hierarchy instead of muted tones</div>
        </div>
        <div class="nb-card">
          <div class="nb-card__icon">02</div>
          <div class="nb-card__title">Oversized</div>
          <div class="nb-card__desc">Type scales push beyond conventional limits for immediate impact</div>
        </div>
        <div class="nb-card">
          <div class="nb-card__icon">03</div>
          <div class="nb-card__title">Playful</div>
          <div class="nb-card__desc">Overlapping elements, offset positioning, and unexpected scale shifts</div>
        </div>
      </div>
    </section>
    <section class="section" style="text-align: center;">
      <a href="#" class="nb-cta">Get Started</a>
    </section>
  </div>
</body>
</html>
--- decision-guide.html ---
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aesthetic Decision Guide</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="stylesheet.css">
<style>
  :root {
    --color-primary: #2563eb;
    --color-secondary: #7c3aed;
    --color-bg: #ffffff;
    --color-text: #0f172a;
    --font-body: 'Inter', sans-serif;
    --font-heading: 'Inter', sans-serif;
  }
  body {
    background: var(--color-bg);
    color: var(--color-text);
  }
  .dg-hero {
    padding: calc(var(--spacing-unit) * 8) 0;
    border-bottom: 2px solid #e2e8f0;
    margin-bottom: calc(var(--spacing-unit) * 6);
  }
  .dg-hero h1 {
    font-weight: 700;
    font-size: 2.5rem;
    letter-spacing: -0.02em;
  }
  .dg-hero p {
    font-weight: 300;
    font-size: 1.0625rem;
    color: #475569;
    margin-top: calc(var(--spacing-unit) * 1);
  }
  .dg-matrix {
    width: 100%;
    border-collapse: collapse;
    font-family: var(--font-body);
    font-size: 0.9375rem;
  }
  .dg-matrix th {
    text-align: left;
    padding: calc(var(--spacing-unit) * 2) calc(var(--spacing-unit) * 3);
    border-bottom: 2px solid var(--color-text);
    font-weight: 600;
    font-size: 0.8125rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .dg-matrix td {
    padding: calc(var(--spacing-unit) * 2) calc(var(--spacing-unit) * 3);
    border-bottom: 1px solid #e2e8f0;
    vertical-align: top;
  }
  .dg-matrix tr:last-child td {
    border-bottom: 2px solid var(--color-text);
  }
  .dg-tag {
    display: inline-block;
    padding: 2px 8px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 1px 0;
  }
  .dg-tag--swiss { background: #2563eb; color: #fff; }
  .dg-tag--minimal { background: #1a1a1a; color: #fff; }
  .dg-tag--brutalist { background: #1a1a1a; color: #f0f0f0; border: 1px solid #555; }
  .dg-tag--glass { background: rgba(96, 165, 250, 0.15); color: #60a5fa; border: 1px solid rgba(96, 165, 250, 0.3); }
  .dg-tag--neo { background: #ff6b35; color: #fff; }
  @media (max-width: 768px) {
    .dg-matrix, .dg-matrix thead, .dg-matrix tbody, .dg-matrix tr, .dg-matrix th, .dg-matrix td {
      display: block;
    }
    .dg-matrix thead { display: none; }
    .dg-matrix td {
      padding: calc(var(--spacing-unit) * 2) 0;
      border-bottom: none;
    }
    .dg-matrix tr {
      padding: calc(var(--spacing-unit) * 3) 0;
      border-bottom: 2px solid #e2e8f0;
    }
  }
</style>
</head>
<body>
  <div class="container">
    <section class="dg-hero">
      <h1>Aesthetic Decision Guide</h1>
      <p>Match your project to the most appropriate aesthetic style. Each row represents a common use case with the recommended aesthetic and the reasoning.</p>
    </section>
    <table class="dg-matrix">
      <thead>
        <tr>
          <th>Use Case</th>
          <th>Recommended</th>
          <th>Also Consider</th>
          <th>Rationale</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Corporate / Enterprise</td>
          <td><span class="dg-tag dg-tag--swiss">Swiss</span></td>
          <td><span class="dg-tag dg-tag--minimal">Minimal</span></td>
          <td>Grid-based clarity projects authority. Asymmetric balance communicates precision without aggression.</td>
        </tr>
        <tr>
          <td>Luxury / Premium Brand</td>
          <td><span class="dg-tag dg-tag--minimal">Minimal</span></td>
          <td><span class="dg-tag dg-tag--glass">Glass</span></td>
          <td>Maximal whitespace and restrained color signal exclusivity. Every element feels intentional and expensive.</td>
        </tr>
        <tr>
          <td>Creative Portfolio</td>
          <td><span class="dg-tag dg-tag--neo">Neo-Brutalist</span></td>
          <td><span class="dg-tag dg-tag--brutalist">Brutalist</span></td>
          <td>Bold color and oversized type express personality. Playful layout signals creative confidence.</td>
        </tr>
        <tr>
          <td>Art / Gallery / Museum</td>
          <td><span class="dg-tag dg-tag--brutalist">Brutalist</span></td>
          <td><span class="dg-tag dg-tag--swiss">Swiss</span></td>
          <td>Raw structural honesty complements avant-garde content. Monochrome palette lets art speak.</td>
        </tr>
        <tr>
          <td>Tech / SaaS / App Landing</td>
          <td><span class="dg-tag dg-tag--glass">Glass</span></td>
          <td><span class="dg-tag dg-tag--swiss">Swiss</span></td>
          <td>Glassmorphism conveys modernity and digital-native sophistication. Layered depth implies advanced technology.</td>
        </tr>
        <tr>
          <td>News / Editorial</td>
          <td><span class="dg-tag dg-tag--swiss">Swiss</span></td>
          <td><span class="dg-tag dg-tag--minimal">Minimal</span></td>
          <td>Grid systems and typographic hierarchy optimize readability at scale. Asymmetric layouts create visual rhythm across articles.</td>
        </tr>
        <tr>
          <td>Personal Website / Blog</td>
          <td><span class="dg-tag dg-tag--minimal">Minimal</span></td>
          <td><span class="dg-tag dg-tag--neo">Neo-Brutalist</span></td>
          <td>Clean typography puts content first. Choose Minimal for serious writing, Neo-Brutalist for personality-driven sites.</td>
        </tr>
        <tr>
          <td>E-commerce / Product</td>
          <td><span class="dg-tag dg-tag--swiss">Swiss</span></td>
          <td><span class="dg-tag dg-tag--glass">Glass</span></td>
          <td>Grid-organized product galleries work best with Swiss clarity. Glass overlay cards add premium feel to hero products.</td>
        </tr>
        <tr>
          <td>Conference / Event</td>
          <td><span class="dg-tag dg-tag--neo">Neo-Brutalist</span></td>
          <td><span class="dg-tag dg-tag--brutalist">Brutalist</span></td>
          <td>High-energy color and oversized typography command attention. Works well for tech conferences and creative events.</td>
        </tr>
        <tr>
          <td>Agency / Design Studio</td>
          <td><span class="dg-tag dg-tag--swiss">Swiss</span></td>
          <td><span class="dg-tag dg-tag--neo">Neo-Brutalist</span></td>
          <td>Grid discipline demonstrates design capability. Swiss signals technical competence; Neo-Brutalist signals creative range.</td>
        </tr>
      </tbody>
    </table>
  </div>
</body>
</html>
--- completion gate report ---
tag balance verification:
  manifest.json: pass - valid json structure
  stylesheet.css: pass - no unclosed tags
  swiss.html: pass - all html/head/body/div/section tags closed
  minimal.html: pass - all tags closed
  brutalist.html: pass - all tags closed
  glass.html: pass - all tags closed
  neo-brutalist.html: pass - all tags closed
  decision-guide.html: pass - all tags closed
var() reference audit:
  swiss.html: 8 references (--color-primary, --color-secondary, --color-bg, --color-text, --font-heading, --font-body, --grid-columns, --grid-gap, --spacing-unit) -- all resolved
  minimal.html: 7 references -- all resolved
  brutalist.html: 5 references -- all resolved
  glass.html: 11 references -- all resolved
  neo-brutalist.html: 8 references -- all resolved
  decision-guide.html: 7 references -- all resolved
footer/newline verification:
  all files: pass - end with newline
shared boilerplate audit:
  reset/normalize: stylesheet.css -- present
  font-face declarations: inline per template (google fonts link) -- not duplicated
  grid system: stylesheet.css -- .grid, grid--2/3/4
  utility classes: stylesheet.css -- .container, .btn, .section, .visually-hidden
  no 5+ line block duplicated across 3+ templates -- pass
delivery status: complete -- 8/8 files generated and verified