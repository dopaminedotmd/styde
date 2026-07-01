MANIFEST (index.html)
---
templates:
  - id: swiss
    file: swiss.html
    dependencies: [stylesheet.css]
    tokens: [--color-primary, --color-secondary, --font-heading, --font-body, --grid-columns, --spacing-unit]
  - id: minimal
    file: minimal.html
    dependencies: [stylesheet.css]
    tokens: [--color-primary, --color-bg, --font-body, --spacing-unit, --rhythm-base]
  - id: brutalist
    file: brutalist.html
    dependencies: [stylesheet.css]
    tokens: [--color-bg, --color-text, --border-weight, --font-mono, --spacing-unit]
  - id: glass
    file: glass.html
    dependencies: [stylesheet.css]
    tokens: [--glass-bg, --glass-border, --glass-blur, --color-accent, --font-body, --spacing-unit]
  - id: neo-brutalist
    file: neo-brutalist.html
    dependencies: [stylesheet.css]
    tokens: [--nb-accent, --nb-secondary, --font-display, --font-body, --border-weight, --spacing-unit]
shared_dependencies:
  stylesheet.css:
    - reset rules
    - font-face declarations (Inter, JetBrains Mono, Akzidenz-Grotesk fallback)
    - grid system (.container, .row, .col-*)
    - common utilities (.sr-only, .text-center, .mt-*, .mb-*)
dependency_graph:
  swiss: [stylesheet.css]
  minimal: [stylesheet.css]
  brutalist: [stylesheet.css]
  glass: [stylesheet.css]
  neo-brutalist: [stylesheet.css]
composition_order: [stylesheet.css, swiss.html, minimal.html, brutalist.html, glass.html, neo-brutalist.html, decision-guide.html]
---
STYLESHEET.CSS
/* Aesthetic Style Composer - Shared Stylesheet */
/* Do not modify --color-* tokens per-template; define overrides in template :root blocks */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; scroll-behavior: smooth; }
img { max-width: 100%; display: block; }
a { color: inherit; text-decoration: none; }
:root {
  --spacing-unit: 1rem;
  --grid-columns: 12;
  --container-max: 1200px;
  --font-sans: 'Inter', 'Akzidenz-Grotesk', 'Helvetica Neue', Arial, sans-serif;
  --font-mono: 'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;
  --border-radius-sm: 4px;
  --border-radius-md: 8px;
  --transition-fast: 150ms ease;
  --transition-base: 250ms ease;
}
.container { width: 100%; max-width: var(--container-max); margin: 0 auto; padding: 0 calc(var(--spacing-unit) * 2); }
.row { display: flex; flex-wrap: wrap; margin: 0 calc(-1 * var(--spacing-unit)); }
.col { flex: 1 0 0%; padding: 0 var(--spacing-unit); }
.col-4 { flex: 0 0 33.333%; max-width: 33.333%; padding: 0 var(--spacing-unit); }
.col-6 { flex: 0 0 50%; max-width: 50%; padding: 0 var(--spacing-unit); }
.col-8 { flex: 0 0 66.667%; max-width: 66.667%; padding: 0 var(--spacing-unit); }
.col-12 { flex: 0 0 100%; max-width: 100%; padding: 0 var(--spacing-unit); }
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); border: 0; }
.text-center { text-align: center; }
.mt-1 { margin-top: var(--spacing-unit); }
.mt-2 { margin-top: calc(var(--spacing-unit) * 2); }
.mt-4 { margin-top: calc(var(--spacing-unit) * 4); }
.mb-1 { margin-bottom: var(--spacing-unit); }
.mb-2 { margin-bottom: calc(var(--spacing-unit) * 2); }
.mb-4 { margin-bottom: calc(var(--spacing-unit) * 4); }
.py-2 { padding-top: calc(var(--spacing-unit) * 2); padding-bottom: calc(var(--spacing-unit) * 2); }
.py-4 { padding-top: calc(var(--spacing-unit) * 4); padding-bottom: calc(var(--spacing-unit) * 4); }
@media (max-width: 768px) { .col-4, .col-6, .col-8 { flex: 0 0 100%; max-width: 100%; } }
/* END stylesheet.css */
SWISS.HTML
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Swiss International - Aesthetic Style Composer</title>
<link rel="stylesheet" href="stylesheet.css">
<style>
:root {
  --sw-bg: #f8f8f8;
  --sw-text: #1a1a1a;
  --sw-accent: #c0392b;
  --sw-muted: #7f8c8d;
  --sw-grid-color: rgba(192, 57, 43, 0.08);
  --sw-font-heading: 'Akzidenz-Grotesk', 'Helvetica Neue', Arial, sans-serif;
  --sw-font-body: 'Helvetica Neue', Arial, sans-serif;
  --sw-leading: 1.618;
}
.swiss-page { font-family: var(--sw-font-body); color: var(--sw-text); background: var(--sw-bg); line-height: var(--sw-leading); }
.swiss-page h1, .swiss-page h2, .swiss-page h3 { font-family: var(--sw-font-heading); font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
.swiss-page h1 { font-size: 3rem; margin-bottom: var(--spacing-unit); }
.swiss-page h2 { font-size: 1.5rem; margin-bottom: var(--spacing-unit); border-top: 3px solid var(--sw-accent); padding-top: var(--spacing-unit); }
.swiss-header { padding: calc(var(--spacing-unit) * 4) 0; border-bottom: 2px solid var(--sw-accent); margin-bottom: calc(var(--spacing-unit) * 3); }
.swiss-grid-demo { background: repeating-linear-gradient(90deg, var(--sw-grid-color) 0px, var(--sw-grid-color) 1px, transparent 1px, transparent calc(100% / 12)); min-height: 200px; }
.swiss-card { background: #fff; padding: calc(var(--spacing-unit) * 2); border: 1px solid #ddd; }
.swiss-card h3 { color: var(--sw-accent); margin-bottom: var(--spacing-unit); }
.swiss-footer { margin-top: calc(var(--spacing-unit) * 4); padding: calc(var(--spacing-unit) * 2) 0; border-top: 1px solid #ddd; font-size: 0.875rem; color: var(--sw-muted); text-align: center; }
</style>
</head>
<body class="swiss-page">
<div class="swiss-header"><div class="container"><h1>International Typographic Style</h1><p class="mt-1">Asymmetric balance &middot; Grid systems &middot; Grotesk typography</p></div></div>
<div class="container"><div class="row mb-4"><div class="col-8"><h2>Grid Manifesto</h2><p>The grid defines content hierarchy. Asymmetric columns create tension. White space is structural, not decorative.</p></div><div class="col-4"><div class="swiss-card"><h3>Principles</h3><p>Akzidenz-Grotesk &middot; flush left/ragged right &middot; mathematical proportions &middot; objective photography</p></div></div></div>
<div class="row mb-4"><div class="col-6"><div class="swiss-card"><h3>Typography</h3><p>Akzidenz-Grotesk for display, Helvetica for body. Strict leading ratio 1:1.618. No hyphenation.</p></div></div><div class="col-6"><div class="swiss-card"><h3>Color</h3><p>Monochromatic with a single accent (red). Black text on off-white. Color = information hierarchy.</p></div></div></div>
<div class="swiss-grid-demo row"></div></div>
<div class="swiss-footer"><div class="container">&copy; 2026 Aesthetic Style Composer &mdash; Swiss</div></div>
</body>
</html>
MINIMAL.HTML
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Minimal - Aesthetic Style Composer</title>
<link rel="stylesheet" href="stylesheet.css">
<style>
:root {
  --mn-bg: #ffffff;
  --mn-text: #2c2c2c;
  --mn-muted: #b0b0b0;
  --mn-accent: #4a4a4a;
  --mn-font: 'Inter', 'Helvetica Neue', sans-serif;
  --mn-leading: 1.75;
  --mn-rhythm: 2rem;
}
.minimal-page { font-family: var(--mn-font); color: var(--mn-text); background: var(--mn-bg); line-height: var(--mn-leading); }
.minimal-page h1 { font-size: 2.5rem; font-weight: 300; letter-spacing: -0.02em; margin-bottom: var(--mn-rhythm); }
.minimal-page h2 { font-size: 1.25rem; font-weight: 400; text-transform: uppercase; letter-spacing: 0.15em; color: var(--mn-muted); margin-bottom: var(--mn-rhythm); }
.minimal-page h3 { font-size: 1rem; font-weight: 500; margin-bottom: var(--spacing-unit); }
.minimal-page p { margin-bottom: var(--mn-rhythm); max-width: 640px; }
.minimal-header { padding: calc(var(--spacing-unit) * 6) 0 var(--mn-rhythm) 0; border-bottom: 1px solid #eee; margin-bottom: calc(var(--mn-rhythm) * 2); }
.minimal-card { padding: calc(var(--spacing-unit) * 3); border: none; }
.minimal-card h3 { color: var(--mn-accent); }
.minimal-divider { width: 48px; height: 2px; background: var(--mn-accent); margin: calc(var(--mn-rhythm) * 2) 0; }
.minimal-footer { margin-top: calc(var(--mn-rhythm) * 3); padding: calc(var(--mn-rhythm)) 0; border-top: 1px solid #eee; font-size: 0.75rem; color: var(--mn-muted); text-transform: uppercase; letter-spacing: 0.1em; }
</style>
</head>
<body class="minimal-page">
<div class="minimal-header"><div class="container"><h1>Less but better</h1><h2>Dieter Rams &middot; 10 principles</h2></div></div>
<div class="container"><div class="row mb-4"><div class="col-6"><div class="minimal-card"><h3>Innovative</h3><p>Good design is innovative. It develops alongside technology while remaining invisible to the user.</p><div class="minimal-divider"></div></div></div><div class="col-6"><div class="minimal-card"><h3>Useful</h3><p>Good design makes a product useful. It serves its purpose through clarity and precision.</p><div class="minimal-divider"></div></div></div></div>
<div class="row"><div class="col-6"><div class="minimal-card"><h3>Aesthetic</h3><p>Good design is aesthetic. Beauty emerges from restraint, proportion, and material honesty.</p><div class="minimal-divider"></div></div></div><div class="col-6"><div class="minimal-card"><h3>Honest</h3><p>Good design is honest. It does not promise what it cannot deliver nor manipulate through decoration.</p><div class="minimal-divider"></div></div></div></div></div>
<div class="minimal-footer"><div class="container">&copy; 2026 Aesthetic Style Composer &mdash; Minimal</div></div>
</body>
</html>
BRUTALIST.HTML
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Brutalist - Aesthetic Style Composer</title>
<link rel="stylesheet" href="stylesheet.css">
<style>
:root {
  --br-bg: #1a1a1a;
  --br-text: #f0f0f0;
  --br-accent: #ff4444;
  --br-border: #f0f0f0;
  --br-border-w: 4px;
  --br-font: 'JetBrains Mono', 'SF Mono', monospace;
  --br-leading: 1.2;
}
.brutalist-page { font-family: var(--br-font); color: var(--br-text); background: var(--br-bg); line-height: var(--br-leading); }
.brutalist-page h1 { font-size: 4rem; font-weight: 700; text-transform: uppercase; margin-bottom: var(--spacing-unit); }
.brutalist-page h2 { font-size: 1.5rem; font-weight: 400; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: var(--spacing-unit); border-left: var(--br-border-w) solid var(--br-accent); padding-left: var(--spacing-unit); }
.brutalist-page h3 { font-size: 1rem; text-transform: uppercase; margin-bottom: var(--spacing-unit); }
.brutalist-header { padding: calc(var(--spacing-unit) * 3) 0; border-bottom: var(--br-border-w) solid var(--br-border); margin-bottom: calc(var(--spacing-unit) * 3); }
.brutalist-card { border: var(--br-border-w) solid var(--br-border); padding: calc(var(--spacing-unit) * 2); margin-bottom: var(--spacing-unit); background: #222; }
.brutalist-card h3 { color: var(--br-accent); }
.brutalist-btn { display: inline-block; background: var(--br-accent); color: var(--br-bg); padding: var(--spacing-unit) calc(var(--spacing-unit) * 2); font-family: var(--br-font); text-transform: uppercase; font-weight: 700; border: none; cursor: pointer; }
.brutalist-btn:hover { background: var(--br-text); color: var(--br-bg); }
.brutalist-footer { margin-top: calc(var(--spacing-unit) * 4); padding: calc(var(--spacing-unit) * 2) 0; border-top: var(--br-border-w) solid var(--br-border); font-size: 0.75rem; text-transform: uppercase; }
</style>
</head>
<body class="brutalist-page">
<div class="brutalist-header"><div class="container"><h1>RAW STRUCTURE</h1><p>Brutalism reveals the material truth of the web. No chrome, no gloss, no apology.</p></div></div>
<div class="container"><div class="row mb-4"><div class="col-4"><div class="brutalist-card"><h3>Concrete Typography</h3><p>Monospace throughout. Weight is meaning. Size is hierarchy.</p></div></div><div class="col-4"><div class="brutalist-card"><h3>Heavy Borders</h3><p>4px minimum. Structure is ornament. Every box is declared.</p></div></div><div class="col-4"><div class="brutalist-card"><h3>Monochrome + Red</h3><p>Black ground, white text, red for action. No gradients.</p></div></div></div>
<div class="row"><div class="col-12 text-center"><span class="brutalist-btn">Enter the structure</span></div></div></div>
<div class="brutalist-footer"><div class="container">&copy; 2026 Aesthetic Style Composer &mdash; Brutalist</div></div>
</body>
</html>
GLASS.HTML
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Glassmorphism - Aesthetic Style Composer</title>
<link rel="stylesheet" href="stylesheet.css">
<style>
:root {
  --gl-bg-start: #0f0c29;
  --gl-bg-mid: #302b63;
  --gl-bg-end: #24243e;
  --gl-glass-bg: rgba(255, 255, 255, 0.08);
  --gl-glass-border: rgba(255, 255, 255, 0.18);
  --gl-glass-blur: 16px;
  --gl-accent: #6c63ff;
  --gl-text: #ffffff;
  --gl-text-muted: rgba(255, 255, 255, 0.6);
  --gl-font: 'Inter', 'Helvetica Neue', sans-serif;
}
.glass-page { font-family: var(--gl-font); color: var(--gl-text); background: linear-gradient(135deg, var(--gl-bg-start), var(--gl-bg-mid), var(--gl-bg-end)); min-height: 100vh; }
.glass-page h1 { font-size: 2.5rem; font-weight: 300; letter-spacing: -0.02em; margin-bottom: var(--spacing-unit); }
.glass-page h2 { font-size: 1.25rem; font-weight: 400; color: var(--gl-text-muted); margin-bottom: calc(var(--spacing-unit) * 2); }
.glass-header { padding: calc(var(--spacing-unit) * 4) 0; text-align: center; }
.glass-card {
  background: var(--gl-glass-bg);
  -webkit-backdrop-filter: blur(var(--gl-glass-blur));
  -moz-backdrop-filter: blur(var(--gl-glass-blur));
  -ms-backdrop-filter: blur(var(--gl-glass-blur));
  backdrop-filter: blur(var(--gl-glass-blur));
  border: 1px solid var(--gl-glass-border);
  border-radius: var(--border-radius-md);
  padding: calc(var(--spacing-unit) * 3);
  transition: transform var(--transition-base), box-shadow var(--transition-base);
}
.glass-card:hover { transform: translateY(-4px); box-shadow: 0 8px 32px rgba(108, 99, 255, 0.2); }
.glass-card h3 { color: var(--gl-accent); margin-bottom: var(--spacing-unit); }
.glass-accent { color: var(--gl-accent); }
.glass-footer { margin-top: calc(var(--spacing-unit) * 4); padding: calc(var(--spacing-unit) * 2) 0; text-align: center; color: var(--gl-text-muted); font-size: 0.875rem; }
</style>
</head>
<body class="glass-page">
<div class="glass-header"><div class="container"><h1>Ambient Depth</h1><h2>Frosted surfaces &middot; Layered light &middot; Immersive space</h2></div></div>
<div class="container"><div class="row mb-4"><div class="col-4"><div class="glass-card"><h3>Glass</h3><p>Backdrop blur creates depth through translucency. Content floats above gradient backgrounds.</p></div></div><div class="col-4"><div class="glass-card"><h3>Light</h3><p>Ambient glow from accent color. Surfaces catch and scatter virtual light.</p></div></div><div class="col-4"><div class="glass-card"><h3>Layers</h3><p>Multiple frosted panes stacked at different depths with subtle shadows.</p></div></div></div>
<div class="row"><div class="col-12 text-center"><p class="glass-accent">Glassmorphism &middot; Apple design language &middot; macOS inspired</p></div></div></div>
<div class="glass-footer"><div class="container">&copy; 2026 Aesthetic Style Composer &mdash; Glass</div></div>
</body>
</html>
NEO-BRUTALIST.HTML
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Neo-Brutalist - Aesthetic Style Composer</title>
<link rel="stylesheet" href="stylesheet.css">
<style>
:root {
  --nb-bg: #f5f0eb;
  --nb-text: #1a1a2e;
  --nb-accent: #ff6b6b;
  --nb-secondary: #4ecdc4;
  --nb-warning: #ffe66d;
  --nb-font-display: 'Inter', 'Helvetica Neue', sans-serif;
  --nb-font-body: 'Inter', sans-serif;
  --nb-border-w: 3px;
  --nb-shadow: 8px 8px 0 rgba(26, 26, 46, 0.15);
}
.neo-page { font-family: var(--nb-font-body); color: var(--nb-text); background: var(--nb-bg); }
.neo-page h1 { font-family: var(--nb-font-display); font-size: 3.5rem; font-weight: 800; letter-spacing: -0.03em; margin-bottom: var(--spacing-unit); }
.neo-page h2 { font-size: 1.5rem; font-weight: 700; margin-bottom: var(--spacing-unit); }
.neo-page h3 { font-size: 1.125rem; font-weight: 700; margin-bottom: var(--spacing-unit); }
.neo-header { padding: calc(var(--spacing-unit) * 3) 0; border-bottom: var(--nb-border-w) solid var(--nb-text); margin-bottom: calc(var(--spacing-unit) * 3); }
.neo-card {
  background: #fff;
  border: var(--nb-border-w) solid var(--nb-text);
  border-radius: 0;
  padding: calc(var(--spacing-unit) * 2);
  box-shadow: var(--nb-shadow);
  transition: transform var(--transition-fast);
}
.neo-card:hover { transform: translate(-2px, -2px); box-shadow: 10px 10px 0 rgba(26, 26, 46, 0.2); }
.neo-card h3 { color: var(--nb-accent); }
.neo-card.-secondary h3 { color: var(--nb-secondary); }
.neo-card.-warning h3 { color: #d4a017; }
.neo-tag { display: inline-block; background: var(--nb-accent); color: #fff; padding: 4px 12px; font-weight: 700; font-size: 0.75rem; border: 2px solid var(--nb-text); margin-bottom: var(--spacing-unit); }
.neo-footer { margin-top: calc(var(--spacing-unit) * 4); padding: calc(var(--spacing-unit) * 2) 0; border-top: var(--nb-border-w) solid var(--nb-text); font-weight: 700; font-size: 0.875rem; }
</style>
</head>
<body class="neo-page">
<div class="neo-header"><div class="container"><h1>Playful Structure</h1><span class="neo-tag">Neo-Brutalist v2</span><p>Bold color &middot; Oversized type &middot; Playful geometry &middot; Raw but refined</p></div></div>
<div class="container"><div class="row mb-4"><div class="col-4"><div class="neo-card"><h3>Hot accent</h3><p>Coral red for action. Teal for contrast. Yellow for attention. No muted tones.</p></div></div><div class="col-4"><div class="neo-card -secondary"><h3>Big type</h3><p>3.5rem headings. 800 weight. Tight tracking. Type leads, layout follows.</p></div></div><div class="col-4"><div class="neo-card -warning"><h3>Hard shadows</h3><p>8px offset. No blur. Shadow = depth, not diffusion. Boxes cast crisp blocks.</p></div></div></div>
<div class="row"><div class="col-12 text-center"><p style="font-size: 1.25rem; font-weight: 700;">Neo-Brutalism is Brutalism after color theory class</p></div></div></div>
<div class="neo-footer"><div class="container">&copy; 2026 Aesthetic Style Composer &mdash; Neo-Brutalist</div></div>
</body>
</html>
DECISION-GUIDE.HTML
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aesthetic Decision Guide - Aesthetic Style Composer</title>
<link rel="stylesheet" href="stylesheet.css">
<style>
:root {
  --dg-bg: #fafafa;
  --dg-text: #1a1a1a;
  --dg-border: #ddd;
  --dg-font: 'Inter', 'Helvetica Neue', sans-serif;
  --dg-swiss: #c0392b;
  --dg-minimal: #4a4a4a;
  --dg-brutalist: #ff4444;
  --dg-glass: #6c63ff;
  --dg-neo: #ff6b6b;
}
.dg-page { font-family: var(--dg-font); color: var(--dg-text); background: var(--dg-bg); padding: calc(var(--spacing-unit) * 3) 0; }
.dg-page h1 { font-size: 2rem; font-weight: 700; margin-bottom: calc(var(--spacing-unit) * 2); }
.dg-page h2 { font-size: 1rem; font-weight: 600; margin-bottom: var(--spacing-unit); }
.dg-table { width: 100%; border-collapse: collapse; margin-bottom: calc(var(--spacing-unit) * 3); }
.dg-table th, .dg-table td { border: 1px solid var(--dg-border); padding: var(--spacing-unit); text-align: left; font-size: 0.875rem; vertical-align: top; }
.dg-table th { font-weight: 600; background: #f0f0f0; }
.dg-tag { display: inline-block; padding: 2px 8px; border-radius: 3px; font-size: 0.75rem; font-weight: 600; color: #fff; }
.dg-tag.-swiss { background: var(--dg-swiss); }
.dg-tag.-minimal { background: var(--dg-minimal); }
.dg-tag.-brutalist { background: var(--dg-brutalist); }
.dg-tag.-glass { background: var(--dg-glass); }
.dg-tag.-neo { background: var(--dg-neo); }
</style>
</head>
<body class="dg-page">
<div class="container"><h1>Aesthetic Decision Matrix</h1>
<table class="dg-table">
<thead><tr><th>Use Case</th><th>Recommended</th><th>Why</th></tr></thead>
<tbody>
<tr><td>Editorial / Magazine</td><td><span class="dg-tag -swiss">Swiss</span></td><td>Grid systems, asymmetric balance, Grotesk typography ideal for text-heavy layouts with structured hierarchy</td></tr>
<tr><td>Landing Page / SaaS</td><td><span class="dg-tag -minimal">Minimal</span></td><td>Max whitespace, restrained color, clear CTA rhythm. Users focus on content, not decoration</td></tr>
<tr><td>Portfolio / Agency</td><td><span class="dg-tag -minimal">Minimal</span> or <span class="dg-tag -glass">Glass</span></td><td>Minimal for classic elegance, Glass for modern immersive showcase with depth</td></tr>
<tr><td>Documentation / API</td><td><span class="dg-tag -brutalist">Brutalist</span></td><td>Monospace, heavy structure, no ambiguity. Content hierarchy through weight and borders</td></tr>
<tr><td>Creative / Art / Music</td><td><span class="dg-tag -neo">Neo-Brutalist</span></td><td>Bold colors, oversized type, playful geometry. Maximum personality and visual impact</td></tr>
<tr><td>Product / E-commerce</td><td><span class="dg-tag -glass">Glass</span></td><td>Frosted surfaces create premium feel. Layered depth suits product hero imagery</td></tr>
<tr><td>Dashboard / Admin</td><td><span class="dg-tag -swiss">Swiss</span></td><td>Grid discipline, clear data hierarchy, restrained accent color for data viz</td></tr>
<tr><td>Mobile App Landing</td><td><span class="dg-tag -glass">Glass</span> or <span class="dg-tag -neo">Neo-Brutalist</span></td><td>Glass for premium apps, Neo-Brutalist for bold consumer apps targeting younger users</td></tr>
<tr><td>News / Blog</td><td><span class="dg-tag -swiss">Swiss</span> or <span class="dg-tag -minimal">Minimal</span></td><td>Swiss for dense information, Minimal for long-form reading with clean typography</td></tr>
<tr><td>Corporate / B2B</td><td><span class="dg-tag -minimal">Minimal</span></td><td>Trust through restraint. No decorative excess. Precision and clarity signal professionalism</td></tr>
</tbody>
</table>
<h2>Composition Notes</h2>
<p><b>Swiss + Minimal:</b> Both use clean typography and generous whitespace. Swiss adds grid discipline and asymmetric tension; Minimal strips to essential content rhythm. Compose Swiss grid structure with Minimal color palette for editorial-landing hybrids.</p>
<p><b>Brutalist + Neo-Brutalist:</b> Same structural DNA. Neo-Brutalist inherits heavy borders and exposed grids from Brutalist, adds color and playfulness. Use Brutalist for serious/systems, Neo-Brutalist for creative/personality.</p>
<p><b>Glass overlay on any:</b> Glass cards can be layered over any other aesthetic as hero sections or feature panels. The frosted surface creates depth against Swiss grids, Minimal whitespace, or Brutalist concrete.</p>
<p><b>Responsive stacking:</b> All templates use the shared .col-* grid system from stylesheet.css. At 768px breakpoint, columns stack vertically. Show/hide modifiers can be added via shared .sr-only or custom data-attributes per template.</p>
</div>
</body>
</html>