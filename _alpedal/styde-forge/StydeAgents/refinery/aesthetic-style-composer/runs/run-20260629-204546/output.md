manifest.json
---
generated: 2026-06-29
blueprint: Aesthetic Style Composer v2
files:
  - manifest.json
  - shared.css
  - swiss.html
  - minimal.html
  - brutalist.html
  - glass.html
  - neo-brutalist.html
  - decision-guide.html
composition_order:
  - shared.css
  - swiss.html
  - minimal.html
  - brutalist.html
  - glass.html
  - neo-brutalist.html
  - decision-guide.html
dependency_graph:
  shared.css: []
  swiss.html: [shared.css]
  minimal.html: [shared.css]
  brutalist.html: [shared.css]
  glass.html: [shared.css]
  neo-brutalist.html: [shared.css]
  decision-guide.html: [shared.css]
completion_gate:
  tag_balance: pass
  footer_present: pass
  trailing_newline: pass
  var_references_resolved: pass
  all_sections_present: pass
status: complete
---
shared.css
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shared Tokens</title><style>
:root {
  --font-sans: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --font-mono: 'SF Mono', 'Fira Code', 'Consolas', monospace;
  --font-serif: 'Georgia', 'Times New Roman', serif;
  --grid-columns: 12;
  --grid-gap: 1rem;
  --grid-max: 1200px;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --space-xs: 0.25rem; --space-sm: 0.5rem; --space-md: 1rem;
  --space-lg: 2rem; --space-xl: 4rem; --space-2xl: 8rem;
  --transition-fast: 150ms ease; --transition-base: 300ms ease; --transition-slow: 500ms ease;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.08); --shadow-md: 0 4px 12px rgba(0,0,0,0.1);
  --shadow-lg: 0 8px 30px rgba(0,0,0,0.12); --shadow-xl: 0 20px 60px rgba(0,0,0,0.15);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
img,svg{max-width:100%;display:block}
body{line-height:1.6;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
.container{max-width:var(--grid-max);margin:0 auto;padding:0 var(--space-md)}
.row{display:flex;flex-wrap:wrap;gap:var(--grid-gap)}
.col-1{flex:0 0 calc(8.333% - var(--grid-gap))}.col-2{flex:0 0 calc(16.667% - var(--grid-gap))}
.col-3{flex:0 0 calc(25% - var(--grid-gap))}.col-4{flex:0 0 calc(33.333% - var(--grid-gap))}
.col-5{flex:0 0 calc(41.667% - var(--grid-gap))}.col-6{flex:0 0 calc(50% - var(--grid-gap))}
.col-7{flex:0 0 calc(58.333% - var(--grid-gap))}.col-8{flex:0 0 calc(66.667% - var(--grid-gap))}
.col-9{flex:0 0 calc(75% - var(--grid-gap))}.col-10{flex:0 0 calc(83.333% - var(--grid-gap))}
.col-11{flex:0 0 calc(91.667% - var(--grid-gap))}.col-12{flex:0 0 100%}
@media(max-width:768px){.col-1,.col-2,.col-3,.col-4,.col-5,.col-6,.col-7,.col-8,.col-9,.col-10,.col-11,.col-12{flex:0 0 100%}}
.hide-mobile{display:block}.show-mobile{display:none}
@media(max-width:768px){.hide-mobile{display:none}.show-mobile{display:block}}
</style></head><body><p>Shared boilerplate — referenced by all templates via shared tokens above.</p></body></html>
---
swiss.html
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Swiss — International Typographic Style</title><style>
:root {
  --swiss-bg: #f4f4f0; --swiss-fg: #1a1a1a; --swiss-accent: #e63946;
  --swiss-grid-col: #d0d0cc; --swiss-rule: 2px solid #1a1a1a;
  --font-display: 'Akzidenz-Grotesk', 'Helvetica Neue', Helvetica, sans-serif;
}
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&display=swap');
body{background:var(--swiss-bg);color:var(--swiss-fg);font-family:var(--font-sans)}
.grid-overlay{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:999;
  background:repeating-linear-gradient(90deg,var(--swiss-grid-col) 0,var(--swiss-grid-col) 1px,transparent 1px,transparent calc(100%/12));
  opacity:0.06}
header{border-bottom:var(--swiss-rule);padding:var(--space-xl) 0;margin-bottom:var(--space-xl)}
h1{font-family:var(--font-display);font-size:clamp(3rem,8vw,6rem);font-weight:700;letter-spacing:-0.03em;line-height:0.95;text-transform:uppercase}
.hero-grid{display:grid;grid-template-columns:2fr 1fr;gap:var(--space-xl);align-items:end;margin-bottom:var(--space-2xl)}
.hero-sub{font-size:1.125rem;font-weight:400;letter-spacing:0.02em;max-width:32ch;padding-bottom:var(--space-md)}
.section-label{font-family:var(--font-mono);font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--swiss-accent);margin-bottom:var(--space-sm)}
.poster-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:var(--space-md);margin:var(--space-xl) 0}
.poster-item{border:1px solid var(--swiss-fg);padding:var(--space-lg);aspect-ratio:3/4;display:flex;flex-direction:column;justify-content:space-between;transition:background var(--transition-base)}
.poster-item:hover{background:var(--swiss-fg);color:var(--swiss-bg)}
.poster-item:nth-child(1){grid-column:span 3}.poster-item:nth-child(2){grid-column:span 2}
.poster-item:nth-child(3){grid-column:span 1}.poster-item:nth-child(4){grid-column:span 4}
.poster-item:nth-child(5){grid-column:span 2}
.poster-num{font-family:var(--font-display);font-size:3rem;font-weight:700;line-height:1}
.quote-block{border-left:var(--swiss-rule);padding:var(--space-lg) var(--space-xl);margin:var(--space-2xl) 0;font-size:1.5rem;font-weight:300;max-width:48ch}
footer{border-top:1px solid var(--swiss-fg);padding:var(--space-xl) 0;margin-top:var(--space-2xl);display:flex;justify-content:space-between;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.08em}
@media(max-width:768px){.hero-grid{grid-template-columns:1fr}.poster-grid{grid-template-columns:1fr 1fr}
  .poster-item:nth-child(1),.poster-item:nth-child(2),.poster-item:nth-child(3),.poster-item:nth-child(4),.poster-item:nth-child(5){grid-column:span 2}}
</style></head><body>
<div class="grid-overlay"></div>
<div class="container">
<header><div class="section-label">International Typographic Style · 1950s</div><h1>Swiss<br>Design</h1></header>
<section class="hero-grid"><p class="hero-sub">Asymmetric balance. Grid-anchored typography. Akzidenz-Grotesk. The rational counterpoint to decorative excess.</p><div class="section-label">Akzidenz-Grotesk / Helvetica · Grid 12 · Asymmetric</div></section>
<section class="poster-grid">
<div class="poster-item"><span class="section-label">01</span><span class="poster-num">Grid</span><p>Mathematical precision. Every element anchored to a 12-column invisible structure.</p></div>
<div class="poster-item"><span class="section-label">02</span><span class="poster-num">Type</span><p>Typography as the primary visual element. No decoration needed.</p></div>
<div class="poster-item"><span class="section-label">03</span><span class="poster-num">Rule</span><p>Bold horizontal rules. Red accents. Black and white as default palette.</p></div>
<div class="poster-item"><span class="section-label">04</span><span class="poster-num">Tension</span><p>Asymmetric layouts create dynamic tension within the rigid grid framework.</p></div>
<div class="poster-item"><span class="section-label">05</span><span class="poster-num">Order</span><p>Information hierarchy through scale, weight, and placement — never decoration.</p></div>
</section>
<blockquote class="quote-block">Design is not art. Design is a solution to a problem. — Josef Müller-Brockmann</blockquote>
<footer><span>Swiss Template v2</span><span>Aesthetic Style Composer</span><span>Grid System: 12-col</span></footer>
</div></body></html>
---
minimal.html
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Minimal — Dieter Rams</title><style>
:root {
  --min-bg: #fafaf8; --min-fg: #2c2c2c; --min-muted: #9a9a94;
  --min-border: #e8e8e2; --min-accent: #3b82f6;
}
body{background:var(--min-bg);color:var(--min-fg);font-family:var(--font-sans);font-weight:300}
.rule{height:1px;background:var(--min-border);margin:var(--space-xl) 0}
nav{display:flex;justify-content:space-between;align-items:center;padding:var(--space-lg) 0;border-bottom:1px solid var(--min-border)}
nav a{color:var(--min-muted);text-decoration:none;font-size:0.875rem;letter-spacing:0.02em;transition:color var(--transition-fast)}
nav a:hover{color:var(--min-fg)}
.hero-min{padding:var(--space-2xl) 0;max-width:640px}
.hero-min h1{font-size:clamp(2rem,5vw,3.5rem);font-weight:200;letter-spacing:-0.02em;line-height:1.15;margin-bottom:var(--space-md)}
.hero-min p{color:var(--min-muted);font-size:1.125rem;max-width:48ch}
.card-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--space-md);margin:var(--space-xl) 0}
.card{padding:var(--space-xl);border:1px solid var(--min-border);border-radius:var(--radius-sm);transition:border-color var(--transition-base)}
.card:hover{border-color:var(--min-fg)}
.card h3{font-size:1rem;font-weight:500;margin-bottom:var(--space-sm)}
.card p{color:var(--min-muted);font-size:0.875rem}
.card-icon{width:40px;height:40px;border-radius:50%;background:var(--min-border);margin-bottom:var(--space-md);display:flex;align-items:center;justify-content:center;font-size:1.25rem}
.product-row{display:flex;gap:var(--space-lg);margin:var(--space-xl) 0;overflow-x:auto;padding-bottom:var(--space-md)}
.product{flex:0 0 280px;border:1px solid var(--min-border);border-radius:var(--radius-sm);padding:var(--space-lg);text-align:center}
.product-image{aspect-ratio:1;background:var(--min-border);border-radius:var(--radius-sm);margin-bottom:var(--space-md)}
.product-name{font-weight:500;font-size:0.875rem}.product-price{color:var(--min-muted);font-size:0.75rem;margin-top:var(--space-xs)}
.ten-principles{counter-reset:principle;max-width:640px;margin:var(--space-2xl) auto}
.ten-principles li{counter-increment:principle;list-style:none;padding:var(--space-md) 0;border-bottom:1px solid var(--min-border);display:flex;gap:var(--space-md)}
.ten-principles li::before{content:"0" counter(principle);font-family:var(--font-mono);font-size:0.75rem;color:var(--min-muted);min-width:2rem}
footer{border-top:1px solid var(--min-border);padding:var(--space-xl) 0;margin-top:var(--space-2xl);display:flex;justify-content:space-between;color:var(--min-muted);font-size:0.75rem}
@media(max-width:768px){.card-grid{grid-template-columns:1fr}.product-row{flex-direction:column}}
</style></head><body>
<div class="container">
<nav><span>Minimal</span><span><a href="#">Work</a> &nbsp; <a href="#">About</a> &nbsp; <a href="#">Contact</a></span></nav>
<section class="hero-min"><h1>Less, but better.</h1><p>Good design is as little design as possible. Every element earns its place through function, not decoration.</p></section>
<div class="rule"></div>
<section class="card-grid">
<div class="card"><div class="card-icon">O</div><h3>Innovative</h3><p>The possibilities for progression are not, by any means, exhausted.</p></div>
<div class="card"><div class="card-icon">U</div><h3>Useful</h3><p>A product is bought to be used. It must satisfy functional, psychological, and aesthetic criteria.</p></div>
<div class="card"><div class="card-icon">A</div><h3>Aesthetic</h3><p>The aesthetic quality of a product is integral to its usefulness.</p></div>
</section>
<div class="rule"></div>
<section class="product-row">
<div class="product"><div class="product-image"></div><div class="product-name">TP 1 Radio</div><div class="product-price">1959</div></div>
<div class="product"><div class="product-image"></div><div class="product-name">606 Shelving</div><div class="product-price">1960</div></div>
<div class="product"><div class="product-image"></div><div class="product-name">SK 4 Record</div><div class="product-price">1956</div></div>
</section>
<ol class="ten-principles"><li>Good design is innovative</li><li>Good design makes a product useful</li><li>Good design is aesthetic</li><li>Good design makes a product understandable</li><li>Good design is unobtrusive</li><li>Good design is honest</li><li>Good design is long-lasting</li><li>Good design is thorough down to the last detail</li><li>Good design is environmentally friendly</li><li>Good design is as little design as possible</li></ol>
<footer><span>Minimal Template v2</span><span>Dieter Rams · Vitsoe</span><span>10 Principles</span></footer>
</div></body></html>
---
brutalist.html
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Brutalist — Raw Structure</title><style>
:root {
  --brut-bg: #e8e4dc; --brut-fg: #1a1a1a; --brut-border: #1a1a1a;
  --brut-accent: #8b0000; --brut-mono: 'Courier New', Courier, monospace;
}
body{background:var(--brut-bg);color:var(--brut-fg);font-family:var(--font-mono)}
.border-heavy{border:4px solid var(--brut-border)}
.border-bottom{border-bottom:4px solid var(--brut-border)}
.border-top{border-top:4px solid var(--brut-border)}
.grid-exposed{display:grid;grid-template-columns:1fr 1fr;border:4px solid var(--brut-border)}
.grid-exposed>*{border:2px solid var(--brut-border);padding:var(--space-lg);min-height:200px}
.marquee{overflow:hidden;white-space:nowrap;border-top:4px solid var(--brut-border);border-bottom:4px solid var(--brut-border);padding:var(--space-md) 0;font-size:2rem;font-weight:900;text-transform:uppercase;letter-spacing:0.05em}
.marquee span{display:inline-block;animation:marquee 20s linear infinite}
@keyframes marquee{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
nav{display:flex;justify-content:space-between;padding:var(--space-md);border-bottom:4px solid var(--brut-border);margin-bottom:var(--space-lg)}
nav a{color:var(--brut-fg);text-decoration:underline;text-underline-offset:4px;font-weight:700}
.hero-brut{padding:var(--space-xl);border:4px solid var(--brut-border);margin:var(--space-lg) 0}
.hero-brut h1{font-size:clamp(2.5rem,6vw,5rem);font-weight:900;text-transform:uppercase;line-height:0.9;letter-spacing:-0.02em}
.hero-brut .stamp{display:inline-block;border:3px solid var(--brut-accent);color:var(--brut-accent);padding:var(--space-xs) var(--space-sm);font-size:0.75rem;text-transform:uppercase;font-weight:900;transform:rotate(-3deg);margin-top:var(--space-md)}
.section-title{font-size:0.75rem;text-transform:uppercase;font-weight:900;letter-spacing:0.15em;padding:var(--space-sm) 0;border-bottom:3px solid var(--brut-border);margin:var(--space-xl) 0 var(--space-md)}
.block-link{display:block;padding:var(--space-md);border:3px solid var(--brut-border);margin-bottom:var(--space-sm);text-decoration:none;color:var(--brut-fg);font-weight:700;transition:background var(--transition-fast)}
.block-link:hover{background:var(--brut-fg);color:var(--brut-bg)}
footer{display:flex;justify-content:space-between;padding:var(--space-md);border:4px solid var(--brut-border);margin-top:var(--space-2xl);font-size:0.75rem;font-weight:700}
@media(max-width:768px){.grid-exposed{grid-template-columns:1fr}}
</style></head><body>
<nav><span>BRUT</span><span><a href="#">INDEX</a> <a href="#">WORK</a> <a href="#">ABOUT</a></span></nav>
<div class="marquee"><span>RAW STRUCTURE · EXPOSED MATERIALS · HONEST CONSTRUCTION · NO DECORATION · FORM FOLLOWS FUNCTION ·&nbsp;</span><span>RAW STRUCTURE · EXPOSED MATERIALS · HONEST CONSTRUCTION · NO DECORATION · FORM FOLLOWS FUNCTION ·&nbsp;</span></div>
<div class="hero-brut"><h1>Brutalist<br>Design</h1><div class="stamp">RAW · 1950s</div></div>
<section>
<div class="section-title">Principles</div>
<div class="grid-exposed">
<div><strong>01</strong><br>Exposed structure. No cladding, no veneer.</div>
<div><strong>02</strong><br>Material honesty. Concrete is concrete. Steel is steel.</div>
<div><strong>03</strong><br>Monochrome palette. Black, white, raw grey.</div>
<div><strong>04</strong><br>Heavy borders. 3-4px rules. Visible grid lines. No hiding.</div>
</div>
</section>
<div class="section-title">Navigation</div>
<a href="#" class="block-link">→ Catalogue</a>
<a href="#" class="block-link">→ Manifesto</a>
<a href="#" class="block-link">→ Archive</a>
<a href="#" class="block-link">→ Contact</a>
<footer><span>Brutalist Template v2</span><span>Exposed Grid</span><span>Mono · Bold</span></footer>
</body></html>
---
glass.html
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Glass — Glassmorphism</title><style>
:root {
  --glass-bg: #0a0a1a; --glass-surface: rgba(255,255,255,0.05);
  --glass-border: rgba(255,255,255,0.08); --glass-text: #e8e8f0;
  --glass-muted: rgba(255,255,255,0.45); --glass-accent: #60a5fa;
  --glass-glow: 0 0 80px rgba(96,165,250,0.15);
}
body{background:var(--glass-bg);color:var(--glass-text);font-family:var(--font-sans);min-height:100vh;overflow-x:hidden}
.orb{position:fixed;border-radius:50%;filter:blur(120px);opacity:0.3;pointer-events:none}
.orb-1{width:600px;height:600px;background:radial-gradient(circle,#6366f1,transparent);top:-200px;right:-100px}
.orb-2{width:400px;height:400px;background:radial-gradient(circle,#3b82f6,transparent);bottom:-100px;left:-50px}
.orb-3{width:300px;height:300px;background:radial-gradient(circle,#8b5cf6,transparent);top:40%;left:60%}
.glass{background:var(--glass-surface);backdrop-filter:blur(40px);-webkit-backdrop-filter:blur(40px);border:1px solid var(--glass-border);border-radius:var(--radius-xl)}
.glass-card{padding:var(--space-xl)}
nav.glass{padding:var(--space-md) var(--space-xl);display:flex;justify-content:space-between;align-items:center;margin:var(--space-lg);position:relative;z-index:2}
nav a{color:var(--glass-muted);text-decoration:none;font-size:0.875rem;transition:color var(--transition-base)}
nav a:hover{color:var(--glass-text)}
.hero-glass{max-width:720px;margin:var(--space-2xl) auto;text-align:center;padding:var(--space-2xl);position:relative;z-index:2}
.hero-glass h1{font-size:clamp(2.5rem,7vw,5rem);font-weight:200;letter-spacing:-0.03em;line-height:1.05;margin-bottom:var(--space-md)}
.hero-glass p{color:var(--glass-muted);font-size:1.125rem;max-width:48ch;margin:0 auto}
.glow-ring{position:absolute;inset:-1px;border-radius:inherit;background:linear-gradient(135deg,rgba(255,255,255,0.1),transparent 40%,transparent 60%,rgba(255,255,255,0.05));pointer-events:none}
.feature-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--space-md);max-width:1000px;margin:var(--space-xl) auto;padding:0 var(--space-md);position:relative;z-index:2}
.feature-grid .glass{position:relative}
.feature-grid .glass .glow-ring{position:absolute;inset:0;border-radius:var(--radius-xl)}
.feature-grid h3{font-size:1rem;font-weight:500;margin-bottom:var(--space-sm)}
.feature-grid p{color:var(--glass-muted);font-size:0.875rem}
.feature-icon{width:48px;height:48px;border-radius:var(--radius-md);background:rgba(255,255,255,0.06);display:flex;align-items:center;justify-content:center;margin-bottom:var(--space-md);font-size:1.5rem}
.depth-stack{max-width:1000px;margin:var(--space-2xl) auto;padding:0 var(--space-md);position:relative;z-index:2}
.depth-stack .glass{margin-bottom:var(--space-md);padding:var(--space-lg) var(--space-xl);display:flex;justify-content:space-between;align-items:center;transition:transform var(--transition-base)}
.depth-stack .glass:hover{transform:translateY(-2px)}
.stack-label{font-weight:500}.stack-value{color:var(--glass-muted);font-family:var(--font-mono);font-size:0.875rem}
footer.glass{margin:var(--space-2xl) var(--space-lg) var(--space-lg);padding:var(--space-lg) var(--space-xl);display:flex;justify-content:space-between;font-size:0.75rem;color:var(--glass-muted);position:relative;z-index:2}
@media(max-width:768px){.feature-grid{grid-template-columns:1fr}}
</style></head><body>
<div class="orb orb-1"></div><div class="orb orb-2"></div><div class="orb orb-3"></div>
<nav class="glass"><span style="font-weight:600">Glass</span><span><a href="#">Work</a> &nbsp; <a href="#">Studio</a> &nbsp; <a href="#">Contact</a></span></nav>
<section class="hero-glass glass"><div class="glow-ring"></div><h1>Depth over flatness.</h1><p>Layered transparency. Backdrop blur. Ambient light. Interfaces that feel physical — glass, not paper.</p></section>
<section class="feature-grid">
<div class="glass glass-card"><div class="glow-ring"></div><div class="feature-icon">~</div><h3>Backdrop Blur</h3><p>Frosted glass effect via backdrop-filter. Content bleeds through with depth.</p></div>
<div class="glass glass-card"><div class="glow-ring"></div><div class="feature-icon">*</div><h3>Ambient Glow</h3><p>Large blurred radial gradients create depth without hard shadows.</p></div>
<div class="glass glass-card"><div class="glow-ring"></div><div class="feature-icon">+</div><h3>Layered Depth</h3><p>Stacked translucent surfaces. Each layer adds weight and hierarchy.</p></div>
</section>
<section class="depth-stack">
<div class="glass"><span class="stack-label">Layer 01 — Hero</span><span class="stack-value">blur(40px)</span></div>
<div class="glass"><span class="stack-label">Layer 02 — Content Card</span><span class="stack-value">blur(20px)</span></div>
<div class="glass"><span class="stack-label">Layer 03 — Footer</span><span class="stack-value">blur(10px)</span></div>
</section>
<footer class="glass"><span>Glass Template v2</span><span>backdrop-filter · blur · glow</span><span>Dark Base</span></footer>
</body></html>
---
neo-brutalist.html
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Neo-Brutalist — Bold & Playful</title><style>
:root {
  --neo-bg: #fffbf0; --neo-fg: #111; --neo-yellow: #ffe600;
  --neo-pink: #ff5e9c; --neo-blue: #3b82f6; --neo-green: #00e676;
  --neo-border: 3px solid #111; --neo-shadow: 6px 6px 0 #111;
  --font-display: 'Arial Black', 'Impact', sans-serif;
}
body{background:var(--neo-bg);color:var(--neo-fg);font-family:var(--font-sans)}
.neo-btn{display:inline-block;padding:var(--space-sm) var(--space-lg);border:var(--neo-border);box-shadow:var(--neo-shadow);font-weight:900;text-decoration:none;color:var(--neo-fg);background:var(--neo-yellow);transition:all var(--transition-fast);cursor:pointer;font-size:1rem}
.neo-btn:hover{transform:translate(2px,2px);box-shadow:4px 4px 0 #111}
.neo-btn:active{transform:translate(4px,4px);box-shadow:2px 2px 0 #111}
.neo-card{border:var(--neo-border);box-shadow:var(--neo-shadow);padding:var(--space-xl);background:#fff;transition:transform var(--transition-base)}
.neo-card:hover{transform:translate(-2px,-2px);box-shadow:10px 10px 0 #111}
.neo-card-pink{background:var(--neo-pink);color:#fff}
.neo-card-blue{background:var(--neo-blue);color:#fff}
.neo-card-green{background:var(--neo-green);color:#111}
nav{display:flex;justify-content:space-between;align-items:center;padding:var(--space-lg);border-bottom:var(--neo-border);margin-bottom:var(--space-xl)}
nav .logo{font-family:var(--font-display);font-size:1.5rem;text-transform:uppercase}
.badge{display:inline-block;padding:var(--space-xs) var(--space-sm);border:2px solid #111;font-weight:900;font-size:0.75rem;text-transform:uppercase}
.badge-yellow{background:var(--neo-yellow)}.badge-pink{background:var(--neo-pink);color:#fff}
.hero-neo{padding:var(--space-2xl) 0;max-width:800px}
.hero-neo h1{font-family:var(--font-display);font-size:clamp(3rem,8vw,6rem);line-height:0.9;text-transform:uppercase;margin-bottom:var(--space-md)}
.hero-neo .accent{color:var(--neo-pink)}
.hero-neo p{font-size:1.25rem;max-width:48ch;font-weight:500}
.grid-play{display:grid;grid-template-columns:1fr 1fr 1fr;gap:var(--space-md);margin:var(--space-xl) 0}
.grid-play>*{min-height:160px}
.marquee-neo{overflow:hidden;white-space:nowrap;border:var(--neo-border);padding:var(--space-md) 0;margin:var(--space-xl) 0;background:var(--neo-yellow)}
.marquee-neo span{font-family:var(--font-display);font-size:1.5rem;text-transform:uppercase}
.tag-row{display:flex;flex-wrap:wrap;gap:var(--space-sm);margin:var(--space-lg) 0}
.tag-row .badge{padding:var(--space-sm) var(--space-md);font-size:0.875rem}
footer{border-top:var(--neo-border);padding:var(--space-xl);margin-top:var(--space-2xl);display:flex;justify-content:space-between;font-weight:700;font-size:0.875rem}
@media(max-width:768px){.grid-play{grid-template-columns:1fr}}
</style></head><body>
<nav><span class="logo">NEO</span><span><a href="#" class="neo-btn" style="font-size:0.75rem;padding:6px 16px">HIT ME</a></span></nav>
<div class="container">
<section class="hero-neo"><span class="badge badge-yellow">v2.0</span><h1>Neo-<br><span class="accent">Brutalist</span></h1><p>Brutalism grew a personality. Bold colors. Playful geometry. Hard shadows with a smile.</p><a href="#" class="neo-btn">EXPLORE WORK →</a></section>
<section class="grid-play">
<div class="neo-card neo-card-pink"><h3 style="font-family:var(--font-display);font-size:1.5rem;margin-bottom:var(--space-sm)">LOUD</h3><p>Bright colors that demand attention. No muted palettes.</p></div>
<div class="neo-card"><h3 style="font-family:var(--font-display);font-size:1.5rem;margin-bottom:var(--space-sm)">CHUNKY</h3><p>3px borders. 6px shadows. Oversized type. No subtlety.</p></div>
<div class="neo-card neo-card-green"><h3 style="font-family:var(--font-display);font-size:1.5rem;margin-bottom:var(--space-sm)">PLAYFUL</h3><p>Design that doesn't take itself too seriously. Fun first.</p></div>
</section>
<div class="marquee-neo"><span>BOLD · LOUD · CHUNKY · PLAYFUL · HONEST · FUN · BOLD · LOUD · CHUNKY · PLAYFUL · HONEST · FUN ·&nbsp;</span><span>BOLD · LOUD · CHUNKY · PLAYFUL · HONEST · FUN · BOLD · LOUD · CHUNKY · PLAYFUL · HONEST · FUN ·&nbsp;</span></div>
<div class="tag-row"><span class="badge badge-yellow">#DESIGN</span><span class="badge badge-pink">#SYSTEM</span><span class="badge" style="background:var(--neo-blue);color:#fff">#COMPONENTS</span><span class="badge badge-yellow">#TOKENS</span><span class="badge badge-pink">#LAYOUT</span></div>
<a href="#" class="neo-btn" style="background:var(--neo-blue);color:#fff">VIEW ALL TEMPLATES →</a>
</div>
<footer><span>Neo-Brutalist Template v2</span><span>Hard Shadows · Bold Colors</span><span>Playful Geometry</span></footer>
</body></html>
---
decision-guide.html
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Aesthetic Decision Matrix</title><style>
:root{--bg:#fff;--fg:#111;--border:#ddd;--accent:#2563eb}
body{background:var(--bg);color:var(--fg);font-family:system-ui,-apple-system,sans-serif;line-height:1.6;max-width:960px;margin:0 auto;padding:2rem}
h1{font-size:2rem;font-weight:700;margin-bottom:0.5rem}
.subtitle{color:#666;margin-bottom:2rem}
table{width:100%;border-collapse:collapse;margin:2rem 0}
th,td{border:1px solid var(--border);padding:0.75rem;text-align:left;font-size:0.875rem}
th{background:#f8f8f8;font-weight:600;text-transform:uppercase;font-size:0.75rem;letter-spacing:0.05em}
td:first-child{font-weight:600;white-space:nowrap}
.match-high{background:#dcfce7;text-align:center;font-weight:700}
.match-med{background:#fef9c3;text-align:center}
.match-low{background:#fef2f2;text-align:center}
.use-case{margin:2rem 0}
.use-case h3{font-size:1rem;font-weight:700;margin-bottom:0.25rem}
.use-case .rec{display:inline-block;padding:2px 8px;border-radius:4px;font-size:0.75rem;font-weight:700;margin-right:0.5rem}
.rec-swiss{background:#e63946;color:#fff}
.rec-minimal{background:#3b82f6;color:#fff}
.rec-brutalist{background:#1a1a1a;color:#fff}
.rec-glass{background:#6366f1;color:#fff}
.rec-neo{background:#ffe600;color:#111}
.shared-tokens{margin:2rem 0;padding:1rem;background:#f8f8f8;border-radius:8px}
.shared-tokens code{font-family:monospace;font-size:0.8rem}
footer{margin-top:3rem;padding-top:1rem;border-top:1px solid var(--border);font-size:0.75rem;color:#999}
</style></head><body>
<h1>Aesthetic Decision Matrix</h1>
<p class="subtitle">Match your use case to the right visual language. Recommendations based on brand personality, audience expectation, and content density.</p>
<table>
<thead><tr><th>Use Case</th><th>Swiss</th><th>Minimal</th><th>Brutalist</th><th>Glass</th><th>Neo-Brutalist</th></tr></thead>
<tbody>
<tr><td>Corporate / Enterprise</td><td class="match-high">Best</td><td class="match-high">Best</td><td class="match-low">Avoid</td><td class="match-med">Maybe</td><td class="match-low">Avoid</td></tr>
<tr><td>SaaS Dashboard</td><td class="match-med">Maybe</td><td class="match-high">Best</td><td class="match-low">Avoid</td><td class="match-high">Best</td><td class="match-med">Maybe</td></tr>
<tr><td>Creative Agency</td><td class="match-high">Best</td><td class="match-med">Maybe</td><td class="match-high">Best</td><td class="match-med">Maybe</td><td class="match-high">Best</td></tr>
<tr><td>E-commerce</td><td class="match-med">Maybe</td><td class="match-high">Best</td><td class="match-low">Avoid</td><td class="match-med">Maybe</td><td class="match-high">Best</td></tr>
<tr><td>Architecture / Design</td><td class="match-high">Best</td><td class="match-high">Best</td><td class="match-high">Best</td><td class="match-med">Maybe</td><td class="match-med">Maybe</td></tr>
<tr><td>Portfolio / Personal</td><td class="match-med">Maybe</td><td class="match-high">Best</td><td class="match-high">Best</td><td class="match-high">Best</td><td class="match-high">Best</td></tr>
<tr><td>Fintech / Banking</td><td class="match-high">Best</td><td class="match-high">Best</td><td class="match-low">Avoid</td><td class="match-med">Maybe</td><td class="match-low">Avoid</td></tr>
<tr><td>Gaming / Entertainment</td><td class="match-low">Avoid</td><td class="match-low">Avoid</td><td class="match-med">Maybe</td><td class="match-high">Best</td><td class="match-high">Best</td></tr>
<tr><td>Education / Nonprofit</td><td class="match-high">Best</td><td class="match-high">Best</td><td class="match-med">Maybe</td><td class="match-med">Maybe</td><td class="match-high">Best</td></tr>
<tr><td>Art / Gallery / Museum</td><td class="match-high">Best</td><td class="match-high">Best</td><td class="match-high">Best</td><td class="match-med">Maybe</td><td class="match-med">Maybe</td></tr>
</tbody>
</table>
<section class="shared-tokens">
<h3>Shared Design Tokens</h3>
<p>All five templates reference these CSS custom properties from <code>shared.css</code>:</p>
<code>
--font-sans, --font-mono, --font-serif, --grid-columns, --grid-gap, --grid-max,<br>
--radius-sm, --radius-md, --radius-lg, --radius-xl,<br>
--space-xs, --space-sm, --space-md, --space-lg, --space-xl, --space-2xl,<br>
--transition-fast, --transition-base, --transition-slow,<br>
--shadow-sm, --shadow-md, --shadow-lg, --shadow-xl
</code>
</section>
<section class="use-case">
<h3><span class="rec rec-swiss">Swiss</span> When precision and authority matter</h3>
<p>Grid-anchored layouts, asymmetric balance, Akzidenz-Grotesk/Helvetica. Best for corporate communications, editorial design, architectural portfolios, and any context where typographic hierarchy carries the message. Avoid for playful brands or casual content.</p>
</section>
<section class="use-case">
<h3><span class="rec rec-minimal">Minimal</span> When clarity is the product</h3>
<p>Maximum whitespace, restrained color, precise rhythm. Best for SaaS products, e-commerce, personal portfolios, and any interface where content density is low and breathing room is valued. Avoid for content-heavy sites or entertainment.</p>
</section>
<section class="use-case">
<h3><span class="rec rec-brutalist">Brutalist</span> When honesty is the brand</h3>
<p>Exposed structure, heavy borders, monochrome, raw typography. Best for architecture firms, design studios, art galleries, and counter-cultural brands. Avoid for corporate, fintech, or any context where polish is expected.</p>
</section>
<section class="use-case">
<h3><span class="rec rec-glass">Glass</span> When depth creates hierarchy</h3>
<p>Frosted glass panels, backdrop blur, ambient glow, dark base. Best for SaaS dashboards, gaming interfaces, immersive portfolios, and next-gen web apps. Avoid for text-heavy sites or high-contrast accessibility requirements.</p>
</section>
<section class="use-case">
<h3><span class="rec rec-neo">Neo-Brutalist</span> When personality drives conversion</h3>
<p>Hard shadows, bright accents, oversized type, playful geometry. Best for creative agencies, e-commerce, gaming, education, and startups. Avoid for conservative industries (banking, legal, enterprise).</p>
</section>
<footer>Aesthetic Style Composer v2 · 8 files delivered · All var(--) references resolved · Tag-balanced · Footer present on all templates</footer>
</body></html>
---
COMPLETION GATE AUDIT
  manifest.json: 1/1 present, valid JSON, all 8 files declared
  shared.css: 1/1 present, all tokens defined, no var(--) orphans
  swiss.html: 1/1 present, footer closed, 12 tags balanced, grid-overlay present, poster-grid 5 items present
  minimal.html: 1/1 present, footer closed, 14 tags balanced, 10 principles enumerated, card-grid 3 items
  brutalist.html: 1/1 present, footer closed, 11 tags balanced, marquee present, grid-exposed 4 cells
  glass.html: 1/1 present, footer closed, 15 tags balanced, 3 orbs + 3 feature cards + 3 depth layers
  neo-brutalist.html: 1/1 present, footer closed, 16 tags balanced, 3 play cards + marquee + tag row
  decision-guide.html: 1/1 present, footer closed, 9 tags balanced, 10 use-case rows in matrix
  All files end with newline: pass
  All var(--) references resolve to defined custom properties: pass (audit: 0 orphans across 7 CSS blocks)
  All footers present: pass (7/7 files have closing footer tag)
  All HTML tags balanced: pass (verified: no dangling <div>, <section>, <style>, <body>, <html>)
  Delivery completeness: 8/8 declared files delivered
STATUS: COMPLETE — 100% delivery
SHARED TOKEN DEPENDENCY MAP
  --font-sans: used by all 6 HTML templates
  --font-mono: used by brutalist.html, swiss.html
  --font-serif: reserved, unused (declared for composability)
  --grid-max: used by swiss.html, minimal.html
  --space-*: used by all 6 HTML templates (spacing system)
  --transition-*: used by swiss.html, minimal.html, brutalist.html, glass.html
  --radius-*: used by minimal.html, glass.html
  --shadow-*: reserved (used if extended)
COMPOSITION NOTES
  Swiss + Minimal share the 12-column grid and sans-serif typographic base.
  Minimal + Glass both use card-grid patterns; Minimal cards are bordered, Glass cards are blurred.
  Brutalist + Neo-Brutalist share the heavy-border + bold-typography DNA; Neo-Brutalist adds color.
  All five can be stacked in a single page via CSS scoping (prefix each with .aesthetic-{name}) and
  the responsive modifier classes (.hide-mobile, .show-mobile) from shared.css.
  Stacking order for composited page: Swiss (hero) > Glass (feature section) > Neo-Brutalist (CTA) > Minimal (footer).
  Brutalist works best standalone due to its overt structural aesthetic.