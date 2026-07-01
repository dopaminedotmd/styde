manifest.json
{
  "project": "Aesthetic Style Composer",
  "version": "2.0",
  "templates": [
    "swiss.html",
    "minimal.html",
    "brutalist.html",
    "glass.html",
    "neo-brutalist.html"
  ],
  "composition_order": ["swiss", "minimal", "brutalist", "glass", "neo-brutalist"],
  "shared_dependencies": {
    "stylesheet.css": ["reset/normalize", "font-face", "grid-system", "utility-classes"],
    "design_tokens": ["--color-primary", "--color-secondary", "--color-bg", "--font-sans", "--font-mono", "--spacing-unit"]
  },
  "dependency_graph": {
    "swiss": ["--color-primary", "--font-sans", "grid-system"],
    "minimal": ["--color-primary", "--color-bg", "--spacing-unit", "grid-system"],
    "brutalist": ["--color-secondary", "--font-mono", "--spacing-unit"],
    "glass": ["--color-primary", "--color-secondary", "--color-bg", "--font-sans", "grid-system"],
    "neo-brutalist": ["--color-primary", "--color-secondary", "--font-mono", "--font-sans", "grid-system"]
  },
  "completion_checklist": [
    "manifest.json",
    "stylesheet.css",
    "swiss.html",
    "minimal.html",
    "brutalist.html",
    "glass.html",
    "neo-brutalist.html",
    "decision-guide.html"
  ]
}
stylesheet.css
:root {
  --color-primary: #2563eb;
  --color-secondary: #7c3aed;
  --color-accent: #f59e0b;
  --color-bg: #fafafa;
  --color-bg-alt: #f0f0f0;
  --color-text: #1a1a2e;
  --color-text-light: #6b7280;
  --color-border: #d1d5db;
  --font-sans: 'Helvetica Neue', 'Inter', -apple-system, sans-serif;
  --font-mono: 'SF Mono', 'JetBrains Mono', 'Fira Code', monospace;
  --spacing-unit: 8px;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.07);
  --shadow-lg: 0 10px 25px rgba(0,0,0,0.1);
  --grid-columns: 12;
  --grid-gap: 24px;
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; scroll-behavior: smooth; }
body { font-family: var(--font-sans); color: var(--color-text); background: var(--color-bg); line-height: 1.6; -webkit-font-smoothing: antialiased; }
img { max-width: 100%; height: auto; display: block; }
a { color: var(--color-primary); text-decoration: none; }
a:hover { text-decoration: underline; }
.container { width: 100%; max-width: 1200px; margin: 0 auto; padding: 0 var(--spacing-unit); }
.row { display: flex; flex-wrap: wrap; gap: var(--grid-gap); }
.col { flex: 1; min-width: 0; }
.col-4 { flex: 0 0 calc(33.333% - var(--grid-gap)); }
.col-6 { flex: 0 0 calc(50% - var(--grid-gap)); }
.col-8 { flex: 0 0 calc(66.667% - var(--grid-gap)); }
.col-12 { flex: 0 0 100%; }
@media (max-width: 768px) { .col-4, .col-6, .col-8 { flex: 0 0 100%; } }
.text-center { text-align: center; }
.text-right { text-align: right; }
.mt-1 { margin-top: calc(var(--spacing-unit) * 1); }
.mt-2 { margin-top: calc(var(--spacing-unit) * 2); }
.mt-4 { margin-top: calc(var(--spacing-unit) * 4); }
.mt-8 { margin-top: calc(var(--spacing-unit) * 8); }
.mb-1 { margin-bottom: calc(var(--spacing-unit) * 1); }
.mb-2 { margin-bottom: calc(var(--spacing-unit) * 2); }
.mb-4 { margin-bottom: calc(var(--spacing-unit) * 4); }
.p-1 { padding: calc(var(--spacing-unit) * 1); }
.p-2 { padding: calc(var(--spacing-unit) * 2); }
.p-4 { padding: calc(var(--spacing-unit) * 4); }
.sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; }
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
  --swiss-red: #da291c;
  --swiss-blue: #005eb8;
  --swiss-black: #1a1a1a;
  --swiss-grid-size: 8px;
}
.swiss-page { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background: #fff; color: var(--swiss-black); max-width: 1000px; margin: 0 auto; padding: 48px; display: grid; grid-template-columns: repeat(12, 1fr); gap: var(--swiss-grid-size); }
.swiss-page .swiss-header { grid-column: 1 / -1; border-bottom: 4px solid var(--swiss-red); padding-bottom: 16px; margin-bottom: 32px; }
.swiss-page h1 { font-size: 48px; font-weight: 700; letter-spacing: -1px; text-transform: uppercase; line-height: 1; margin: 0; }
.swiss-page h2 { font-size: 24px; font-weight: 400; text-transform: uppercase; letter-spacing: 2px; color: var(--swiss-red); margin-top: 32px; grid-column: 1 / -1; border-top: 1px solid #ccc; padding-top: 16px; }
.swiss-page .swiss-content { grid-column: 1 / 9; font-size: 14px; line-height: 1.7; }
.swiss-page .swiss-sidebar { grid-column: 9 / -1; font-size: 12px; line-height: 1.6; border-left: 1px solid #ccc; padding-left: 16px; }
.swiss-page .swiss-grid-demo { grid-column: 1 / -1; display: grid; grid-template-columns: repeat(12, 1fr); gap: 2px; margin-top: 24px; }
.swiss-page .swiss-grid-demo div { background: var(--swiss-red); color: #fff; font-size: 10px; padding: 8px 4px; text-align: center; font-family: 'Helvetica Neue', sans-serif; }
.swiss-page .swiss-footer { grid-column: 1 / -1; margin-top: 48px; border-top: 1px solid #ccc; padding-top: 16px; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; color: #999; text-align: right; }
</style>
</head>
<body>
<div class="swiss-page">
  <header class="swiss-header"><h1>Swiss International Style</h1></header>
  <h2>Typography & Grid</h2>
  <div class="swiss-content">
    <p>The International Typographic Style emerged in Switzerland in the 1950s. It emphasizes clarity, objectivity, and systematic grid structures. Asymmetric layouts, sans-serif typefaces, and photography presented with stark clarity define the movement.</p>
    <p>Grid systems provide the structural backbone. Content aligns to an underlying modular grid of 8px units. Ragged-right text setting preferred over justified alignment.</p>
  </div>
  <div class="swiss-sidebar">
    <p>Akzidenz-Grotesk / Helvetica pairings</p>
    <p>Asymmetric balance</p>
    <p>Photography full-bleed</p>
    <p>Minimal color: red accent on black-white</p>
  </div>
  <div class="swiss-grid-demo">
    <div>1</div><div>2</div><div>3</div><div>4</div><div>5</div><div>6</div><div>7</div><div>8</div><div>9</div><div>10</div><div>11</div><div>12</div>
  </div>
  <footer class="swiss-footer">International Typographic Style &mdash; 1950s Switzerland</footer>
</div>
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
.minimal-page { max-width: 800px; margin: 0 auto; padding: 80px 64px; background: #fff; color: #333; }
.minimal-page h1 { font-size: 32px; font-weight: 300; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 64px; color: #111; }
.minimal-page h2 { font-size: 20px; font-weight: 300; letter-spacing: 2px; color: #555; margin-top: 48px; margin-bottom: 16px; }
.minimal-page p { font-size: 15px; line-height: 2; color: #666; margin-bottom: 24px; max-width: 600px; }
.minimal-page .minimal-card { border: 1px solid #eee; padding: 48px; margin: 32px 0; transition: all 0.3s ease; }
.minimal-page .minimal-card:hover { border-color: #aaa; box-shadow: 0 0 0 1px #aaa; }
.minimal-page .minimal-card h3 { font-size: 14px; font-weight: 400; text-transform: uppercase; letter-spacing: 3px; color: #999; margin-bottom: 16px; }
.minimal-page .minimal-card p { font-size: 14px; line-height: 1.8; color: #777; }
.minimal-page .minimal-divider { height: 1px; background: #e8e8e8; margin: 64px 0; }
.minimal-footer { font-size: 11px; color: #bbb; text-transform: uppercase; letter-spacing: 2px; margin-top: 80px; }
</style>
</head>
<body>
<div class="minimal-page">
  <h1>Dieter Rams &mdash; Weniger aber besser</h1>
  <p>Good design is as little design as possible. Less is more &mdash; but more precise. Each element serves a purpose. Every line earns its place.</p>
  <div class="minimal-card">
    <h3>1. Innovative</h3>
    <p>Good design is innovative. Technological progress constantly offers new opportunities for innovative design, but it should always be human-centered.</p>
  </div>
  <div class="minimal-card">
    <h3>2. Useful</h3>
    <p>Good design makes a product useful. It has to satisfy certain criteria, not only functional but also psychological and aesthetic.</p>
  </div>
  <div class="minimal-card">
    <h3>3. Aesthetic</h3>
    <p>Good design is aesthetic. The aesthetic quality of a product is integral to its usefulness because products are used every day and have an effect on people.</p>
  </div>
  <div class="minimal-divider"></div>
  <h2>Design Principles</h2>
  <p>Maximal whitespace creates breathing room. Restrained color palette elevates what matters. Precise rhythm through consistent vertical spacing. No decoration without purpose.</p>
  <div class="minimal-footer">10 Principles of Good Design &mdash; Dieter Rams</div>
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
.brutal-page { background: #fff; color: #000; max-width: 900px; margin: 0 auto; font-family: 'Courier New', 'SF Mono', monospace; }
.brutal-page .brutal-header { border: 4px solid #000; padding: 24px; margin: 16px; text-align: center; }
.brutal-page .brutal-header h1 { font-size: 48px; font-weight: 900; text-transform: uppercase; letter-spacing: -2px; line-height: 1; margin: 0; }
.brutal-page .brutal-header p { font-size: 14px; margin-top: 8px; color: #555; }
.brutal-page .brutal-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px; }
.brutal-page .brutal-block { border: 3px solid #000; padding: 24px; background: #fff; }
.brutal-page .brutal-block h2 { font-size: 24px; text-transform: uppercase; margin-bottom: 12px; border-bottom: 2px solid #000; padding-bottom: 8px; }
.brutal-page .brutal-block p { font-size: 13px; line-height: 1.6; }
.brutal-page .brutal-block .brutal-label { display: inline-block; background: #000; color: #fff; padding: 4px 12px; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
.brutal-page .brutal-full { grid-column: 1 / -1; }
.brutal-page .brutal-stats { border: 3px solid #000; padding: 32px; margin: 16px; display: flex; gap: 32px; justify-content: center; }
.brutal-page .brutal-stat { text-align: center; }
.brutal-page .brutal-stat .number { font-size: 48px; font-weight: 900; line-height: 1; }
.brutal-page .brutal-stat .label { font-size: 10px; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }
.brutal-page .brutal-footer { border-top: 4px solid #000; margin: 16px; padding: 16px 0; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; text-align: center; }
</style>
</head>
<body>
<div class="brutal-page">
  <div class="brutal-header"><h1>Brutalist Web</h1><p>Raw. Unpolished. Structural.</p></div>
  <div class="brutal-grid">
    <div class="brutal-block">
      <span class="brutal-label">Core</span>
      <h2>Structure</h2>
      <p>Exposed grids, heavy borders, monochrome palettes. The frame is the design. No ornament, no surface smoothing. Content declares its place.</p>
    </div>
    <div class="brutal-block">
      <span class="brutal-label">Type</span>
      <h2>Typography</h2>
      <p>Bold oversized type. Monospace by default. Large contrast ratios. Text as structural element, breaking out of containers.</p>
    </div>
    <div class="brutal-block brutal-full">
      <span class="brutal-label">Ethos</span>
      <h2>Honesty in Materials</h2>
      <p>Brutalism in architecture exposed concrete structure. In web, it exposes the HTML skeleton. Raw grids, unstyled elements as design choice. The browser's default styles become part of the aesthetic vocabulary.</p>
    </div>
  </div>
  <div class="brutal-stats">
    <div class="brutal-stat"><div class="number">100%</div><div class="label">Monochrome</div></div>
    <div class="brutal-stat"><div class="number">4px</div><div class="label">Min Border</div></div>
    <div class="brutal-stat"><div class="number">12</div><div class="label">Grid Columns</div></div>
  </div>
  <div class="brutal-footer">Brutalist Web Design &mdash; Raw Aesthetic Movement</div>
</div>
</body>
</html>
glass.html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Glassmorphism Design</title>
<link rel="stylesheet" href="stylesheet.css">
<style>
.glass-page { min-height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; padding: 40px; position: relative; overflow: hidden; }
.glass-page::before { content: ''; position: absolute; width: 300px; height: 300px; background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%); top: -50px; right: -50px; border-radius: 50%; }
.glass-page::after { content: ''; position: absolute; width: 200px; height: 200px; background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%); bottom: -30px; left: -30px; border-radius: 50%; }
.glass-card { position: relative; z-index: 1; max-width: 600px; width: 100%; padding: 48px; border-radius: 16px; background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); }
.glass-card h1 { font-size: 28px; color: #fff; font-weight: 600; margin-bottom: 8px; letter-spacing: -0.5px; }
.glass-card .glass-subtitle { font-size: 14px; color: rgba(255,255,255,0.7); margin-bottom: 32px; }
.glass-card .glass-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.glass-card .glass-item { background: rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.15); backdrop-filter: blur(10px); transition: transform 0.3s ease; }
.glass-card .glass-item:hover { transform: translateY(-4px); background: rgba(255, 255, 255, 0.18); }
.glass-card .glass-item h3 { font-size: 14px; color: #fff; font-weight: 500; margin-bottom: 4px; }
.glass-card .glass-item p { font-size: 12px; color: rgba(255,255,255,0.6); line-height: 1.5; }
.glass-card .glass-footer { margin-top: 32px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.15); font-size: 11px; color: rgba(255,255,255,0.5); text-align: center; }
</style>
</head>
<body>
<div class="glass-page">
  <div class="glass-card">
    <h1>Glassmorphism</h1>
    <div class="glass-subtitle">Frosted glass aesthetic for modern interfaces</div>
    <div class="glass-grid">
      <div class="glass-item"><h3>Backdrop Blur</h3><p>Creates depth through frosted transparency, revealing content beneath with soft focus.</p></div>
      <div class="glass-item"><h3>Layered Depth</h3><p>Multiple translucent layers stack to create a sense of physical depth and hierarchy.</p></div>
      <div class="glass-item"><h3>Ambient Glow</h3><p>Soft gradient backgrounds and radial light sources create atmospheric illumination.</p></div>
      <div class="glass-item"><h3>Light Borders</h3><p>Subtle semi-transparent borders define edges while maintaining the glass effect.</p></div>
    </div>
    <div class="glass-footer">Apple-inspired glassmorphism &mdash; iOS design language</div>
  </div>
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
.neobrutal-page { background: #fff; max-width: 960px; margin: 0 auto; padding: 24px; font-family: 'Inter', 'Helvetica Neue', sans-serif; }
.neobrutal-header { background: #ff6b35; border: 4px solid #000; padding: 24px 32px; margin-bottom: 24px; box-shadow: 8px 8px 0 #000; transform: rotate(-0.5deg); }
.neobrutal-header h1 { font-size: 48px; font-weight: 900; color: #fff; text-transform: uppercase; letter-spacing: -2px; line-height: 1; margin: 0; text-shadow: 2px 2px 0 rgba(0,0,0,0.3); }
.neobrutal-header p { font-size: 16px; color: rgba(255,255,255,0.9); margin-top: 8px; font-weight: 500; }
.neobrutal-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 24px; }
.neobrutal-card { border: 4px solid #000; padding: 24px; background: #fff; box-shadow: 6px 6px 0 #000; transition: all 0.15s ease; }
.neobrutal-card:nth-child(1) { border-color: #000; background: #f7f7f7; }
.neobrutal-card:nth-child(2) { border-color: #000; background: #e8f5e9; }
.neobrutal-card:nth-child(3) { border-color: #000; background: #fff3e0; }
.neobrutal-card:hover { transform: translate(-3px, -3px); box-shadow: 9px 9px 0 #000; }
.neobrutal-card h2 { font-size: 20px; font-weight: 800; margin-bottom: 8px; text-transform: uppercase; letter-spacing: -0.5px; }
.neobrutal-card p { font-size: 13px; line-height: 1.6; color: #333; }
.neobrutal-card .tag { display: inline-block; background: #000; color: #fff; padding: 2px 10px; font-size: 10px; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; }
.neobrutal-cta { border: 4px solid #000; padding: 32px; text-align: center; background: #4ecdc4; box-shadow: 8px 8px 0 #000; margin-bottom: 24px; }
.neobrutal-cta h2 { font-size: 28px; font-weight: 900; color: #000; text-transform: uppercase; }
.neobrutal-cta p { font-size: 14px; color: #000; margin-top: 8px; font-weight: 500; }
.neobrutal-footer { text-align: center; padding: 16px; font-size: 12px; font-weight: 700; color: #999; text-transform: uppercase; letter-spacing: 2px; }
</style>
</head>
<body>
<div class="neobrutal-page">
  <div class="neobrutal-header"><h1>Neo-Brutalism</h1><p>Contemporary edge meets raw structure</p></div>
  <div class="neobrutal-grid">
    <div class="neobrutal-card"><span class="tag">Color</span><h2>Bright Accents</h2><p>Vibrant color blocks against monochrome structure. Orange, teal, yellow &mdash; high saturation, high contrast.</p></div>
    <div class="neobrutal-card"><span class="tag">Type</span><h2>Oversized Type</h2><p>Bold headlines dominate. Heavy weight, tight tracking. Text as graphic element.</p></div>
    <div class="neobrutal-card"><span class="tag">Shape</span><h2>Playful Geometry</h2><p>Rotated elements, offset shadows, layered boxes. Structured chaos with intentional collision.</p></div>
  </div>
  <div class="neobrutal-cta"><h2>Build Something Bold</h2><p>Bright colors. Heavy borders. Zero subtlety.</p></div>
  <div class="neobrutal-footer">Neo-Brutalist Design &mdash; 2020s Aesthetic Movement</div>
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
.decision-page { max-width: 900px; margin: 40px auto; padding: 32px; font-family: var(--font-sans); color: var(--color-text); }
.decision-page h1 { font-size: 28px; font-weight: 700; margin-bottom: 8px; }
.decision-page .subtitle { font-size: 14px; color: var(--color-text-light); margin-bottom: 32px; }
.decision-page table { width: 100%; border-collapse: collapse; margin-bottom: 32px; }
.decision-page th { background: var(--color-text); color: #fff; padding: 12px 16px; text-align: left; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }
.decision-page td { padding: 12px 16px; border-bottom: 1px solid var(--color-border); font-size: 13px; line-height: 1.5; }
.decision-page tr:nth-child(even) td { background: var(--color-bg-alt); }
.decision-page .score { display: inline-block; padding: 2px 10px; border-radius: 99px; font-size: 11px; font-weight: 700; }
.decision-page .score-high { background: #d4edda; color: #155724; }
.decision-page .score-mid { background: #fff3cd; color: #856404; }
.decision-page .score-low { background: #f8d7da; color: #721c24; }
.decision-page h2 { font-size: 18px; font-weight: 600; margin-top: 32px; margin-bottom: 12px; }
.decision-page .rec-card { border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 20px; margin-bottom: 16px; }
.decision-page .rec-card h3 { font-size: 15px; font-weight: 600; margin-bottom: 6px; }
.decision-page .rec-card p { font-size: 13px; color: var(--color-text-light); line-height: 1.6; }
</style>
</head>
<body>
<div class="decision-page">
  <h1>Aesthetic Decision Matrix</h1>
  <div class="subtitle">Match use-cases to recommended visual styles</div>
  <table>
    <tr><th>Use Case</th><th>Swiss</th><th>Minimal</th><th>Brutalist</th><th>Glass</th><th>Neo-Brutal</th></tr>
    <tr><td>Corporate / Enterprise</td><td><span class="score score-high">Best</span></td><td><span class="score score-mid">Good</span></td><td><span class="score score-low">Poor</span></td><td><span class="score score-mid">Good</span></td><td><span class="score score-low">Poor</span></td></tr>
    <tr><td>Portfolio / Creative</td><td><span class="score score-mid">Good</span></td><td><span class="score score-high">Best</span></td><td><span class="score score-mid">Good</span></td><td><span class="score score-high">Best</span></td><td><span class="score score-mid">Good</span></td></tr>
    <tr><td>Blog / Editorial</td><td><span class="score score-high">Best</span></td><td><span class="score score-high">Best</span></td><td><span class="score score-low">Poor</span></td><td><span class="score score-low">Poor</span></td><td><span class="score score-low">Poor</span></td></tr>
    <tr><td>SaaS / Dashboard</td><td><span class="score score-mid">Good</span></td><td><span class="score score-mid">Good</span></td><td><span class="score score-low">Poor</span></td><td><span class="score score-high">Best</span></td><td><span class="score score-low">Poor</span></td></tr>
    <tr><td>Agency / Landing</td><td><span class="score score-mid">Good</span></td><td><span class="score score-mid">Good</span></td><td><span class="score score-mid">Good</span></td><td><span class="score score-mid">Good</span></td><td><span class="score score-high">Best</span></td></tr>
    <tr><td>Art / Avant-garde</td><td><span class="score score-mid">Good</span></td><td><span class="score score-low">Poor</span></td><td><span class="score score-high">Best</span></td><td><span class="score score-mid">Good</span></td><td><span class="score score-high">Best</span></td></tr>
    <tr><td>E-Commerce / Retail</td><td><span class="score score-mid">Good</span></td><td><span class="score score-high">Best</span></td><td><span class="score score-low">Poor</span></td><td><span class="score score-mid">Good</span></td><td><span class="score score-low">Poor</span></td></tr>
  </table>
  <h2>Composition Notes</h2>
  <div class="rec-card"><h3>Token Sharing</h3><p>Swiss, Minimal, and Glass styles all share --color-primary (blue) and --font-sans. Neo-Brutalist and Brutalist use --font-mono and bold --color-secondary. All reference the shared grid system from stylesheet.css.</p></div>
  <div class="rec-card"><h3>Grid Relationships</h3><p>Swiss uses 12-column modular grid. Minimal uses single-column centered layout. Brutalist uses 2-column asymmetric. Glass uses 2-column card grid. Neo-Brutalist uses 3-column with offset shadow.</p></div>
  <div class="rec-card"><h3>Responsive Behavior</h3><p>All templates collapse to single-column below 768px. The .container/.row/.col system from stylesheet.css handles breakpoints. Glass and Neo-Brutalist add hover transitions for interaction feedback.</p></div>
  <div class="rec-card"><h3>Compositing</h3><p>Swiss header can house Minimal content body. Glass card can overlay Brutalist background. Neo-Brutalist CTA sections can embed Swiss grid demos. Token compatibility ensures visual coherence.</p></div>
</div>
</body>
</html>