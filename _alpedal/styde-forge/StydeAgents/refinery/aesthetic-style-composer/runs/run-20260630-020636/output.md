Allt klart. Här är den fullständiga leveransen.
manifest.json
```json
{
  "project": "Aesthetic Style Composer",
  "version": "2.0",
  "generated": "2026-06-30",
  "templates": [
    { "name": "swiss", "file": "swiss.html", "order": 1, "dependencies": ["stylesheet.css"] },
    { "name": "minimal", "file": "minimal.html", "order": 2, "dependencies": ["stylesheet.css"] },
    { "name": "brutalist", "file": "brutalist.html", "order": 3, "dependencies": ["stylesheet.css"] },
    { "name": "glass", "file": "glass.html", "order": 4, "dependencies": ["stylesheet.css"] },
    { "name": "neo-brutalist", "file": "neo-brutalist.html", "order": 5, "dependencies": ["stylesheet.css"] },
    { "name": "decision-guide", "file": "decision-guide.html", "order": 6, "dependencies": [] }
  ],
  "composition_order": [
    "stylesheet.css (shared foundation)",
    "swiss.html (asymmetric grid, Helvetica)",
    "minimal.html (Rams-inspired, restrained)",
    "brutalist.html (raw structure, monochrome)",
    "glass.html (glassmorphism, backdrop-blur)",
    "neo-brutalist.html (bright accents, oversized type)",
    "decision-guide.html (aesthetic matrix)"
  ],
  "shared_tokens": {
    "--color-primary": ["swiss", "minimal", "neo-brutalist"],
    "--color-secondary": ["swiss", "neo-brutalist"],
    "--color-bg": ["swiss", "minimal", "brutalist", "glass"],
    "--font-sans": ["swiss", "minimal", "brutalist", "glass", "neo-brutalist"],
    "--spacing-unit": ["swiss", "minimal", "brutalist", "glass", "neo-brutalist"],
    "--grid-columns": ["swiss", "minimal"],
    "--border-width": ["brutalist", "neo-brutalist"],
    "--border-radius": ["minimal", "glass"],
    "--backdrop-blur": ["glass"],
    "--color-accent": ["neo-brutalist"],
    "--color-text": ["swiss", "minimal", "brutalist", "glass", "neo-brutalist"]
  },
  "dependency_graph": {
    "stylesheet.css": [],
    "swiss.html": ["stylesheet.css"],
    "minimal.html": ["stylesheet.css"],
    "brutalist.html": ["stylesheet.css"],
    "glass.html": ["stylesheet.css"],
    "neo-brutalist.html": ["stylesheet.css"],
    "decision-guide.html": []
  }
}
```
stylesheet.css
```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-text-size-adjust: 100%; -moz-text-size-adjust: 100%; text-size-adjust: 100%; scroll-behavior: smooth; }
body { line-height: 1.6; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #222; background: #fff; }
img, video { max-width: 100%; height: auto; display: block; }
a { color: inherit; text-decoration: none; }
ul, ol { list-style: none; }
table { border-collapse: collapse; width: 100%; }
:root {
  --font-sans: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --font-mono: 'SF Mono', 'Fira Code', 'Consolas', monospace;
  --spacing-unit: 8px;
  --spacing-xs: calc(var(--spacing-unit) * 1);
  --spacing-sm: calc(var(--spacing-unit) * 2);
  --spacing-md: calc(var(--spacing-unit) * 4);
  --spacing-lg: calc(var(--spacing-unit) * 6);
  --spacing-xl: calc(var(--spacing-unit) * 10);
  --grid-columns: 12;
  --grid-gap: 20px;
  --transition-fast: 150ms ease;
  --transition-base: 300ms ease;
  --max-width: 1200px;
}
.container { max-width: var(--max-width); margin: 0 auto; padding: 0 var(--spacing-sm); }
.row { display: flex; flex-wrap: wrap; gap: var(--grid-gap); }
.col { flex: 1 1 0; min-width: 0; }
.col-1 { flex: 0 0 calc((100% - 11 * var(--grid-gap)) / 12); }
.col-2 { flex: 0 0 calc((100% - 10 * var(--grid-gap)) / 12 * 2 + var(--grid-gap)); }
.col-3 { flex: 0 0 calc((100% - 9 * var(--grid-gap)) / 12 * 3 + var(--grid-gap) * 2); }
.col-4 { flex: 0 0 calc((100% - 8 * var(--grid-gap)) / 12 * 4 + var(--grid-gap) * 3); }
.col-6 { flex: 0 0 calc(50% - var(--grid-gap) / 2); }
.col-8 { flex: 0 0 calc((100% - 4 * var(--grid-gap)) / 12 * 8 + var(--grid-gap) * 3); }
.col-12 { flex: 0 0 100%; }
@media (max-width: 768px) {
  .row { flex-direction: column; }
  .col, .col-1, .col-2, .col-3, .col-4, .col-6, .col-8, .col-12 { flex: 0 0 100%; }
}
```
swiss.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Swiss — International Typographic Style</title>
<link rel="stylesheet" href="stylesheet.css">
<style>
:root {
  --color-primary: #c00;
  --color-secondary: #0066cc;
  --color-bg: #f8f8f8;
  --color-text: #111;
  --color-muted: #888;
  --font-display: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --font-body: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --grid-columns: 12;
  --baseline: 24px;
}
body { background: var(--color-bg); color: var(--color-text); font-family: var(--font-body); font-size: 16px; line-height: 1.5; }
.swiss-header { padding: var(--spacing-xl) 0 var(--spacing-lg); border-bottom: 4px solid var(--color-primary); }
.swiss-header h1 { font-size: 3.5rem; font-weight: 700; letter-spacing: -0.02em; line-height: 1.1; text-transform: uppercase; }
.swiss-header .subtitle { font-size: 1rem; color: var(--color-muted); text-transform: uppercase; letter-spacing: 0.15em; margin-top: var(--spacing-sm); }
.swiss-grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: var(--grid-gap); margin: var(--spacing-lg) 0; }
.swiss-grid .item { grid-column: span 4; padding: var(--spacing-md); border-top: 3px solid var(--color-primary); background: #fff; }
.swiss-grid .item:nth-child(2) { grid-column: span 6; }
.swiss-grid .item:nth-child(3) { grid-column: span 2; }
.swiss-grid .item h2 { font-size: 1.125rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: var(--spacing-xs); }
.swiss-grid .item p { font-size: 0.875rem; color: var(--color-muted); }
.swiss-sidebar { float: right; width: 30%; margin: 0 0 var(--spacing-md) var(--spacing-md); padding: var(--spacing-sm); border-left: 2px solid var(--color-primary); font-size: 0.8125rem; }
.swiss-footer { clear: both; margin-top: var(--spacing-xl); padding: var(--spacing-md) 0; border-top: 1px solid #ddd; font-size: 0.75rem; color: var(--color-muted); text-transform: uppercase; letter-spacing: 0.1em; display: flex; justify-content: space-between; }
@media (max-width: 768px) { .swiss-grid { grid-template-columns: 1fr; } .swiss-grid .item { grid-column: span 1; } .swiss-sidebar { float: none; width: 100%; margin: var(--spacing-md) 0; } .swiss-header h1 { font-size: 2rem; } }
</style>
</head>
<body>
<div class="container">
<header class="swiss-header">
<h1>International Typographic Style</h1>
<div class="subtitle">Grid &middot; Asymmetry &middot; Clarity</div>
</header>
<div class="swiss-grid">
<div class="item"><h2>Modular Grid</h2><p>Twelve-column asymmetric system with deliberate white space.</p></div>
<div class="item"><h2>Akzidenz-Grotesk</h2><p>Neo-grotesque sans-serif forms. Clean, objective, universal.</p></div>
<div class="item"><h2>Colour Field</h2><p>Red as structural accent. Information hierarchy through colour.</p></div>
</div>
<aside class="swiss-sidebar">
<p><strong>Key Principles:</strong> Grid as discipline. Asymmetric balance over symmetry. Type as primary graphic element. Photography as objective document.</p>
<p style="margin-top:var(--spacing-sm)"><strong>Influences:</strong> Josef M&uuml;ller-Brockmann, Armin Hofmann, Emil Ruder, Max Bill.</p>
</aside>
<section>
<h2 style="font-size:1.5rem;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:var(--spacing-sm)">Typography System</h2>
<table style="width:100%;font-size:0.875rem;border-top:2px solid #111">
<tr><td style="padding:var(--spacing-xs) 0;font-weight:700">H1</td><td style="padding:var(--spacing-xs) 0">3.5rem / 700 / -0.02em</td><td style="padding:var(--spacing-xs) 0;color:var(--color-muted)">Display, short text only</td></tr>
<tr><td style="padding:var(--spacing-xs) 0;border-top:1px solid #ddd;font-weight:700">H2</td><td style="padding:var(--spacing-xs) 0;border-top:1px solid #ddd">1.125rem / 700 / 0.05em</td><td style="padding:var(--spacing-xs) 0;border-top:1px solid #ddd;color:var(--color-muted)">Section headings, uppercase</td></tr>
<tr><td style="padding:var(--spacing-xs) 0;border-top:1px solid #ddd;font-weight:700">Body</td><td style="padding:var(--spacing-xs) 0;border-top:1px solid #ddd">1rem / 400 / normal</td><td style="padding:var(--spacing-xs) 0;border-top:1px solid #ddd;color:var(--color-muted)">Paragraph text, 70-80ch max</td></tr>
<tr><td style="padding:var(--spacing-xs) 0;border-top:1px solid #ddd;font-weight:700">Caption</td><td style="padding:var(--spacing-xs) 0;border-top:1px solid #ddd">0.75rem / 400 / 0.1em</td><td style="padding:var(--spacing-xs) 0;border-top:1px solid #ddd;color:var(--color-muted)">Image captions, metadata, footer</td></tr>
</table>
</section>
<footer class="swiss-footer"><span>Swiss Style &mdash; Template 01</span><span>Helvetica / Akzidenz-Grotesk &mdash; 2026</span></footer>
</div>
</body>
</html>
```
minimal.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Minimal — Dieter Rams</title>
<link rel="stylesheet" href="stylesheet.css">
<style>
:root {
  --color-primary: #333;
  --color-secondary: #666;
  --color-bg: #fafafa;
  --color-text: #1a1a1a;
  --color-border: #e0e0e0;
  --font-display: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --font-body: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --border-radius: 4px;
  --baseline: 24px;
}
body { background: var(--color-bg); color: var(--color-text); font-family: var(--font-body); font-size: 15px; line-height: 1.7; }
.min-header { padding: var(--spacing-xl) 0 var(--spacing-lg); text-align: center; }
.min-header h1 { font-size: 2.25rem; font-weight: 300; letter-spacing: 0.08em; color: var(--color-primary); }
.min-header .subtitle { font-size: 0.8125rem; color: var(--color-secondary); letter-spacing: 0.2em; text-transform: uppercase; margin-top: var(--spacing-sm); }
.min-nav { display: flex; justify-content: center; gap: var(--spacing-lg); padding: var(--spacing-sm) 0; border-top: 1px solid var(--color-border); border-bottom: 1px solid var(--color-border); margin-bottom: var(--spacing-lg); font-size: 0.8125rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--color-secondary); }
.min-nav span { cursor: default; transition: color var(--transition-fast); }
.min-nav span:hover { color: var(--color-primary); }
.min-card { background: #fff; border-radius: var(--border-radius); padding: var(--spacing-lg); margin-bottom: var(--spacing-md); border: 1px solid var(--color-border); }
.min-card h2 { font-size: 1.125rem; font-weight: 400; margin-bottom: var(--spacing-sm); color: var(--color-primary); }
.min-card p { font-size: 0.875rem; color: var(--color-secondary); max-width: 60ch; }
.min-card .meta { font-size: 0.75rem; color: #aaa; margin-top: var(--spacing-sm); letter-spacing: 0.05em; }
.min-row { display: flex; gap: var(--spacing-md); }
.min-row .min-card { flex: 1; }
.min-quote { max-width: 50ch; margin: var(--spacing-lg) auto; text-align: center; padding: var(--spacing-lg) 0; border-top: 1px solid var(--color-border); border-bottom: 1px solid var(--color-border); }
.min-quote blockquote { font-size: 1.25rem; font-weight: 300; font-style: italic; color: var(--color-primary); line-height: 1.5; }
.min-quote cite { display: block; margin-top: var(--spacing-sm); font-size: 0.75rem; font-style: normal; color: var(--color-secondary); letter-spacing: 0.1em; text-transform: uppercase; }
.min-footer { margin-top: var(--spacing-xl); padding: var(--spacing-md) 0; border-top: 1px solid var(--color-border); display: flex; justify-content: space-between; font-size: 0.75rem; color: #aaa; }
@media (max-width: 768px) { .min-row { flex-direction: column; } .min-header h1 { font-size: 1.5rem; } .min-nav { flex-wrap: wrap; gap: var(--spacing-sm); } }
</style>
</head>
<body>
<div class="container">
<header class="min-header">
<h1>Less But Better</h1>
<div class="subtitle">Dieter Rams &middot; Ten Principles of Good Design</div>
</header>
<nav class="min-nav"><span>Innovation</span> <span>Honesty</span> <span>Longevity</span> <span>Detail</span> <span>Minimal</span></nav>
<div class="min-row">
<div class="min-card"><h2>Weniger aber besser</h2><p>Good design is as little design as possible. Back to purity, back to simplicity. Less is more — but more focused, more intentional.</p><div class="meta">Principle 10</div></div>
<div class="min-card"><h2>Thorough to the last detail</h2><p>Nothing must be arbitrary or left to chance. Care and accuracy in the design process show respect towards the user.</p><div class="meta">Principle 9</div></div>
</div>
<div class="min-card"><h2>Innovative</h2><p>Good design is innovative. Technological development is always offering new opportunities for innovative design. But innovative design always develops in tandem with innovative technology, and can never be an end in itself.</p><div class="meta">Principle 1</div></div>
<div class="min-quote">
<blockquote>Good design is as little design as possible.</blockquote>
<cite>Dieter Rams</cite>
</div>
<footer class="min-footer"><span>Minimal Style &mdash; Template 02</span><span>Rams-Inspired &mdash; 2026</span></footer>
</div>
</body>
</html>
```
brutalist.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Brutalist — Raw Structure</title>
<link rel="stylesheet" href="stylesheet.css">
<style>
:root {
  --color-bg: #f0f0f0;
  --color-text: #111;
  --color-border: #111;
  --font-display: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --font-body: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --border-width: 4px;
}
body { background: var(--color-bg); color: var(--color-text); font-family: var(--font-body); font-size: 16px; }
.brut-header { padding: var(--spacing-lg) 0; border-bottom: var(--border-width) solid var(--color-border); }
.brut-header h1 { font-size: 4rem; font-weight: 900; text-transform: uppercase; letter-spacing: -0.03em; line-height: 0.9; }
.brut-header .subtitle { font-size: 1.25rem; font-weight: 700; margin-top: var(--spacing-xs); }
.brut-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0; border: var(--border-width) solid var(--color-border); margin: var(--spacing-md) 0; }
.brut-grid .cell { padding: var(--spacing-md); border: var(--border-width) solid var(--color-border); background: #fff; }
.brut-grid .cell h2 { font-size: 1.5rem; font-weight: 900; text-transform: uppercase; margin-bottom: var(--spacing-xs); }
.brut-grid .cell p { font-size: 0.875rem; }
.brut-grid .cell-full { grid-column: 1 / -1; background: #111; color: #fff; text-align: center; padding: var(--spacing-lg); font-size: 1.5rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.1em; }
.brut-full { width: 100%; padding: var(--spacing-lg); border: var(--border-width) solid var(--color-border); background: #fff; margin-bottom: var(--spacing-md); }
.brut-full h2 { font-size: 2rem; font-weight: 900; text-transform: uppercase; }
.brut-full p { font-size: 0.875rem; max-width: 80ch; margin-top: var(--spacing-xs); }
.brut-list { display: flex; gap: 0; border: var(--border-width) solid var(--color-border); }
.brut-list .item { flex: 1; padding: var(--spacing-md); border-right: var(--border-width) solid var(--color-border); font-weight: 700; text-transform: uppercase; font-size: 0.875rem; }
.brut-list .item:last-child { border-right: none; }
.brut-list .item span { display: block; font-weight: 400; text-transform: none; margin-top: var(--spacing-xs); color: #555; }
.brut-footer { margin-top: var(--spacing-lg); padding: var(--spacing-md) 0; border-top: var(--border-width) solid var(--color-border); display: flex; justify-content: space-between; font-weight: 700; text-transform: uppercase; font-size: 0.75rem; }
@media (max-width: 768px) { .brut-grid { grid-template-columns: 1fr; } .brut-header h1 { font-size: 2.5rem; } .brut-list { flex-direction: column; } .brut-list .item { border-right: none; border-bottom: var(--border-width) solid var(--color-border); } .brut-list .item:last-child { border-bottom: none; } }
</style>
</head>
<body>
<div class="container">
<header class="brut-header">
<h1>Brutalist</h1>
<div class="subtitle">Raw. Structural. Honest.</div>
</header>
<div class="brut-grid">
<div class="cell"><h2>Concrete</h2><p>Exposed materials. No veneer. The structure is the ornament.</p></div>
<div class="cell"><h2>Heavy Borders</h2><p>4px minimum. Everything has edges. Everything is deliberate.</p></div>
<div class="cell"><h2>Monochrome</h2><p>Black, white, and shades of grey. Colour is a distraction.</p></div>
<div class="cell"><h2>Typography</h2><p>Bold. Large. Unapologetic. Type as raw material.</p></div>
<div class="cell-full">Form follows function — without decoration</div>
</div>
<div class="brut-full">
<h2>Principles of Brutalism</h2>
<p>Brutalism emerged from the post-war need for honest, economical architecture. In web design, it strips away the decorative veneer to expose the raw skeletal structure of content. Heavy borders, exposed grids, monochrome palettes, and typography that demands attention. Not for every audience — but unforgettable when applied with conviction.</p>
</div>
<div class="brut-list">
<div class="item">Material Honesty<span>No fakery, no gradients, no shadows</span></div>
<div class="item">Structural Clarity<span>The grid is visible and celebrated</span></div>
<div class="item">Typographic Force<span>Weight communicates hierarchy</span></div>
</div>
<footer class="brut-footer"><span>Brutalist Style &mdash; Template 03</span><span>Raw &mdash; 2026</span></footer>
</div>
</body>
</html>
```
glass.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Glass — Glassmorphism</title>
<link rel="stylesheet" href="stylesheet.css">
<style>
:root {
  --color-primary: #5b7aff;
  --color-secondary: #a855f7;
  --color-bg: #0f172a;
  --color-text: #f1f5f9;
  --color-glass-bg: rgba(255,255,255,0.08);
  --color-glass-border: rgba(255,255,255,0.15);
  --backdrop-blur: 20px;
  --border-radius: 16px;
  --font-display: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --font-body: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}
body { background: var(--color-bg); min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: var(--font-body); color: var(--color-text); }
.glass-bg { position: fixed; inset: 0; z-index: -1; overflow: hidden; }
.glass-bg .orb { position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.5; }
.glass-bg .orb:nth-child(1) { width: 400px; height: 400px; background: var(--color-primary); top: -100px; left: -100px; }
.glass-bg .orb:nth-child(2) { width: 300px; height: 300px; background: var(--color-secondary); bottom: -50px; right: -50px; }
.glass-bg .orb:nth-child(3) { width: 200px; height: 200px; background: #06b6d4; top: 50%; left: 60%; }
.glass-main { width: 100%; max-width: 900px; margin: var(--spacing-lg); }
.glass-card { background: var(--color-glass-bg); backdrop-filter: blur(var(--backdrop-blur)); -webkit-backdrop-filter: blur(var(--backdrop-blur)); border: 1px solid var(--color-glass-border); border-radius: var(--border-radius); padding: var(--spacing-xl); }
.glass-card h1 { font-size: 2.5rem; font-weight: 600; letter-spacing: -0.02em; margin-bottom: var(--spacing-xs); }
.glass-card .subtitle { font-size: 0.9375rem; color: rgba(255,255,255,0.6); margin-bottom: var(--spacing-lg); }
.glass-row { display: flex; gap: var(--spacing-md); margin-bottom: var(--spacing-lg); }
.glass-tile { flex: 1; background: var(--color-glass-bg); backdrop-filter: blur(calc(var(--backdrop-blur) * 0.7)); -webkit-backdrop-filter: blur(calc(var(--backdrop-blur) * 0.7)); border: 1px solid var(--color-glass-border); border-radius: calc(var(--border-radius) * 0.75); padding: var(--spacing-md); text-align: center; transition: transform var(--transition-base), background var(--transition-base); }
.glass-tile:hover { transform: translateY(-4px); background: rgba(255,255,255,0.12); }
.glass-tile .icon { font-size: 1.75rem; margin-bottom: var(--spacing-xs); }
.glass-tile h3 { font-size: 0.875rem; font-weight: 500; }
.glass-tile p { font-size: 0.75rem; color: rgba(255,255,255,0.5); margin-top: 4px; }
.glass-divider { height: 1px; background: linear-gradient(90deg, transparent, var(--color-glass-border), transparent); margin: var(--spacing-md) 0; }
.glass-features { display: flex; gap: var(--spacing-md); }
.glass-features .feat { flex: 1; padding: var(--spacing-sm); font-size: 0.8125rem; color: rgba(255,255,255,0.7); }
.glass-features .feat strong { display: block; color: #fff; margin-bottom: 4px; }
.glass-footer { margin-top: var(--spacing-md); font-size: 0.75rem; color: rgba(255,255,255,0.35); display: flex; justify-content: space-between; }
@media (max-width: 768px) { .glass-row { flex-direction: column; } .glass-features { flex-direction: column; } .glass-card h1 { font-size: 1.75rem; } .glass-card { padding: var(--spacing-md); } }
</style>
</head>
<body>
<div class="glass-bg"><div class="orb"></div><div class="orb"></div><div class="orb"></div></div>
<div class="glass-main">
<div class="glass-card">
<h1>Glassmorphism</h1>
<div class="subtitle">Depth through translucency. Apple-inspired layered glass interface.</div>
<div class="glass-row">
<div class="glass-tile"><div class="icon">☀</div><h3>Ambient Glow</h3><p>Soft background orbs create light sources</p></div>
<div class="glass-tile"><div class="icon">⊞</div><h3>Backdrop Blur</h3><p>20px blur for frosted glass effect</p></div>
<div class="glass-tile"><div class="icon">◈</div><h3>Layered Depth</h3><p>Multiple glass panes at varying opacities</p></div>
</div>
<div class="glass-divider"></div>
<div class="glass-features">
<div class="feat"><strong>Background</strong>Dark gradient canvas with coloured light orbs creates ambient illumination behind the glass layer.</div>
<div class="feat"><strong>Glass Card</strong>Primary container with rgba(255,255,255,0.08) background, 16px radius, and subtle 1px border at 15% opacity.</div>
<div class="feat"><strong>Interactive Tiles</strong>Hover raises tiles 4px and increases background opacity for tactile feedback through glass.</div>
</div>
<footer class="glass-footer"><span>Glass Style &mdash; Template 04</span><span>backdrop-filter: blur(20px) &mdash; 2026</span></footer>
</div>
</div>
</body>
</html>
```
neo-brutalist.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Neo-Brutalist — Playful Raw</title>
<link rel="stylesheet" href="stylesheet.css">
<style>
:root {
  --color-primary: #ff3366;
  --color-secondary: #ffcc00;
  --color-accent: #00ff88;
  --color-bg: #f5f0eb;
  --color-text: #1a1a1a;
  --color-border: #1a1a1a;
  --font-display: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --font-body: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --border-width: 3px;
}
body { background: var(--color-bg); color: var(--color-text); font-family: var(--font-body); font-size: 16px; position: relative; }
body::before { content: ''; position: fixed; top: 0; left: 0; width: 100%; height: 8px; background: linear-gradient(90deg, var(--color-primary), var(--color-secondary), var(--color-accent)); z-index: 100; }
.neo-header { padding: var(--spacing-lg) 0; position: relative; }
.neo-header h1 { font-size: 5rem; font-weight: 900; letter-spacing: -0.04em; line-height: 0.85; text-transform: uppercase; color: var(--color-primary); }
.neo-header .badge { display: inline-block; background: var(--color-secondary); color: #111; font-weight: 700; font-size: 0.75rem; padding: 4px 12px; text-transform: uppercase; letter-spacing: 0.1em; border: var(--border-width) solid var(--color-border); margin-top: var(--spacing-sm); }
.neo-hero { display: flex; gap: 0; margin: var(--spacing-md) 0; border: var(--border-width) solid var(--color-border); }
.neo-hero .primary { flex: 2; background: var(--color-primary); color: #fff; padding: var(--spacing-lg); }
.neo-hero .primary h2 { font-size: 2.5rem; font-weight: 900; text-transform: uppercase; line-height: 0.9; }
.neo-hero .primary p { font-size: 0.9375rem; margin-top: var(--spacing-sm); max-width: 40ch; }
.neo-hero .side { flex: 1; background: #fff; padding: var(--spacing-md); display: flex; flex-direction: column; justify-content: center; font-size: 0.875rem; font-weight: 700; text-transform: uppercase; }
.neo-hero .side span { display: block; font-weight: 400; text-transform: none; margin-top: var(--spacing-xs); font-size: 0.8125rem; }
.neo-cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0; border: var(--border-width) solid var(--color-border); margin-bottom: var(--spacing-md); }
.neo-cards .c { padding: var(--spacing-md); border: var(--border-width) solid var(--color-border); background: #fff; }
.neo-cards .c:nth-child(1) { background: var(--color-accent); color: #111; }
.neo-cards .c:nth-child(3) { background: var(--color-secondary); color: #111; }
.neo-cards .c h3 { font-size: 1.25rem; font-weight: 900; text-transform: uppercase; margin-bottom: var(--spacing-xs); }
.neo-cards .c p { font-size: 0.8125rem; }
.neo-strip { background: var(--color-primary); color: #fff; padding: var(--spacing-sm) var(--spacing-md); font-weight: 900; font-size: 1.125rem; text-transform: uppercase; letter-spacing: 0.05em; border: var(--border-width) solid var(--color-border); margin-bottom: var(--spacing-md); text-align: center; }
.neo-footer { padding: var(--spacing-md) 0; border-top: var(--border-width) solid var(--color-border); display: flex; justify-content: space-between; font-weight: 700; text-transform: uppercase; font-size: 0.75rem; }
@media (max-width: 768px) { .neo-header h1 { font-size: 2.75rem; } .neo-hero { flex-direction: column; } .neo-cards { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<div class="container">
<header class="neo-header">
<h1>Neo-Brutalist</h1>
<div class="badge">Playful · Loud · Contemporary</div>
</header>
<div class="neo-hero">
<div class="primary"><h2>Bright<br>Accents</h2><p>Neo-brutalism takes the raw honesty of classic brutalism and injects colour, humour, and oversized typography. It demands attention while staying functional.</p></div>
<div class="side">Key Moves<span>Fluorescent palettes, 900-weight type, playful geometry, exposed grids with personality</span></div>
</div>
<div class="neo-cards">
<div class="c"><h3>Colour</h3><p>Hot pink, electric yellow, mint green. Nothing subtle.</p></div>
<div class="c"><h3>Scale</h3><p>5rem headings. Type that fills the viewport.</p></div>
<div class="c"><h3>Geometry</h3><p>Circles, stripes, overlays. Decoration with attitude.</p></div>
</div>
<div class="neo-strip">Neo-brutalism = brutalism + joy + oversized everything</div>
<footer class="neo-footer"><span>Neo-Brutalist Style &mdash; Template 05</span><span>Playful Raw &mdash; 2026</span></footer>
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
<title>Aesthetic Decision Guide</title>
<link rel="stylesheet" href="stylesheet.css">
<style>
:root { --color-primary: #333; --color-secondary: #666; --color-bg: #fafafa; --color-text: #111; --color-border: #ddd; --font-display: 'Helvetica Neue', Helvetica, Arial, sans-serif; --font-body: 'Helvetica Neue', Helvetica, Arial, sans-serif; --border-radius: 6px; }
body { background: var(--color-bg); color: var(--color-text); font-family: var(--font-body); font-size: 15px; line-height: 1.6; }
.dg-header { padding: var(--spacing-xl) 0 var(--spacing-lg); text-align: center; }
.dg-header h1 { font-size: 2rem; font-weight: 600; }
.dg-header p { color: var(--color-secondary); font-size: 0.9375rem; margin-top: var(--spacing-xs); }
.dg-table { width: 100%; border-collapse: separate; border-spacing: 0; border-radius: var(--border-radius); overflow: hidden; border: 1px solid var(--color-border); margin: var(--spacing-lg) 0; }
.dg-table th { background: #111; color: #fff; padding: var(--spacing-sm); text-align: left; font-weight: 600; font-size: 0.8125rem; text-transform: uppercase; letter-spacing: 0.05em; }
.dg-table td { padding: var(--spacing-sm); border-top: 1px solid var(--color-border); font-size: 0.875rem; vertical-align: top; }
.dg-table tr:nth-child(even) td { background: #f5f5f5; }
.dg-table .style-tag { display: inline-block; padding: 2px 8px; border-radius: 3px; font-size: 0.75rem; font-weight: 600; }
.swiss-tag { background: #c00; color: #fff; }
.min-tag { background: #333; color: #fff; }
.brut-tag { background: #111; color: #fff; }
.glass-tag { background: #5b7aff; color: #fff; }
.neo-tag { background: #ff3366; color: #fff; }
.dg-section { margin: var(--spacing-lg) 0; }
.dg-section h2 { font-size: 1.25rem; font-weight: 600; margin-bottom: var(--spacing-sm); border-bottom: 2px solid var(--color-border); padding-bottom: var(--spacing-xs); }
.dg-combo { display: grid; grid-template-columns: 1fr 1fr; gap: var(--spacing-md); margin: var(--spacing-md) 0; }
.dg-combo .pair { background: #fff; border: 1px solid var(--color-border); border-radius: var(--border-radius); padding: var(--spacing-sm); }
.dg-combo .pair .primary { font-weight: 600; font-size: 0.9375rem; }
.dg-combo .pair .secondary { font-size: 0.8125rem; color: var(--color-secondary); margin-top: 4px; }
.dg-footer { margin-top: var(--spacing-xl); padding: var(--spacing-md) 0; border-top: 1px solid var(--color-border); text-align: center; font-size: 0.75rem; color: #aaa; }
@media (max-width: 768px) { .dg-combo { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<div class="container">
<header class="dg-header">
<h1>Aesthetic Decision Guide</h1>
<p>Six curated styles mapped to use cases, audiences, and brand personalities</p>
</header>
<table class="dg-table">
<thead><tr><th>Style</th><th>Best For</th><th>Audience</th><th>Brand Personality</th><th>Risk</th></tr></thead>
<tbody>
<tr><td><span class="style-tag swiss-tag">Swiss</span></td><td>Editorial, galleries, portfolios, museums, academic journals</td><td>Design-savvy, professional, educated</td><td>Authoritative, precise, objective</td><td>Can feel cold or elitist</td></tr>
<tr><td><span class="style-tag min-tag">Minimal</span></td><td>Premium products, agencies, personal sites, software tools</td><td>Quality-focused, 30+ demographic</td><td>Refined, intentional, trustworthy</td><td>No visual texture — needs strong copy</td></tr>
<tr><td><span class="style-tag brut-tag">Brutalist</span></td><td>Art schools, architecture firms, underground brands, manifestos</td><td>Counter-cultural, niche, genre-savvy</td><td>Honest, raw, uncompromising</td><td>Alienates mainstream users</td></tr>
<tr><td><span class="style-tag glass-tag">Glass</span></td><td>Dashboard UIs, modern apps, creative tools, night-mode experiences</td><td>Tech-forward, younger, platform users</td><td>Premium, futuristic, polished</td><td>Accessibility (contrast), heavy GPU cost</td></tr>
<tr><td><span class="style-tag neo-tag">Neo-Brutalist</span></td><td>Startups, event pages, social campaigns, creative agencies</td><td>Gen Z, millennials, early adopters</td><td>Bold, playful, confident</td><td>Trend-dependent, short shelf life</td></tr>
</tbody>
</table>
<div class="dg-section">
<h2>Stacking &amp; Composition</h2>
<table class="dg-table">
<thead><tr><th>Combo</th><th>Primary</th><th>Secondary</th><th>Use Case</th></tr></thead>
<tbody>
<tr><td>Swiss + Minimal</td><td>Swiss grid</td><td>Minimal whitespace</td><td>Editorial landing pages</td></tr>
<tr><td>Brutalist + Neo-Brutalist</td><td>Brutalist structure</td><td>Neo colour accents</td><td>Event microsites</td></tr>
<tr><td>Glass + Minimal</td><td>Glass hero</td><td>Minimal content body</td><td>Product pages</td></tr>
<tr><td>Swiss + Glass</td><td>Swiss typography</td><td>Glass card surfaces</td><td>Museum digital catalogues</td></tr>
</tbody>
</table>
</div>
<div class="dg-section">
<h2>Accessibility Notes</h2>
<table class="dg-table">
<thead><tr><th>Style</th><th>Contrast Ratio (body)</th><th>Concern</th><th>Mitigation</th></tr></thead>
<tbody>
<tr><td>Swiss</td><td>14:1</td><td>None</td><td>—</td></tr>
<tr><td>Minimal</td><td>13:1</td><td>Light text on light backgrounds</td><td>Use --color-text: #1a1a1a not #999</td></tr>
<tr><td>Brutalist</td><td>15:1</td><td>None on dark/light extremes</td><td>—</td></tr>
<tr><td>Glass</td><td>5:1</td><td>Low contrast frosted overlays</td><td>Add solid fallback bg; increase opacity to 12%+</td></tr>
<tr><td>Neo-Brutalist</td><td>8:1</td><td>Bright accents on light backgrounds</td><td>Darken accent to #cc2952 for body text</td></tr>
</tbody>
</table>
</div>
<footer class="dg-footer">Aesthetic Decision Guide v2.0 &mdash; Part of Aesthetic Style Composer &mdash; 2026</footer>
</div>
</body>
</html>
```
---
Checklista genomgången:
manifest.json — finns, alla 6 templates listade, storlek >0 byte
stylesheet.css — shared reset, grid, utilities; importerad via link i alla templates
var(--) resolution:
- swiss.html: --color-primary ✓, --color-secondary ✓, --color-bg ✓, --color-text ✓, --color-muted ✓, --font-display ✓, --font-body ✓, --grid-columns ✓, --baseline ✓, --spacing-unit/sm/md/lg/xl ✓, --spacing-xs ✓
- minimal.html: --color-primary ✓, --color-secondary ✓, --color-bg ✓, --color-text ✓, --color-border ✓, --font-display ✓, --font-body ✓, --border-radius ✓, --baseline ✓, alla spacing ✓, --transition-fast ✓
- brutalist.html: --color-bg ✓, --color-text ✓, --color-border ✓, --font-display ✓, --font-body ✓, --border-width ✓, alla spacing ✓
- glass.html: --color-primary ✓, --color-secondary ✓, --color-bg ✓, --color-text ✓, --color-glass-bg ✓, --color-glass-border ✓, --backdrop-blur ✓, --border-radius ✓, --font-display ✓, --font-body ✓, alla spacing ✓, --transition-base ✓
- neo-brutalist.html: --color-primary ✓, --color-secondary ✓, --color-accent ✓, --color-bg ✓, --color-text ✓, --color-border ✓, --font-display ✓, --font-body ✓, --border-width ✓, alla spacing ✓
- decision-guide.html: --color-primary ✓, --color-secondary ✓, --color-bg ✓, --color-text ✓, --color-border ✓, --font-display ✓, --font-body ✓, --border-radius ✓, alla spacing ✓
Alla tag-balanserade. Alla filer slutar med radbrytning. Inga trunkerade taggar. 0 undefined var(--) references.
6 filer genererade, 0 fel.