AESTHETIC STYLE COMPOSER v1
DESIGN TOKENS — SHARED VOCABULARY
scale:
  xs: 0.25rem
  sm: 0.5rem
  md: 1rem
  lg: 2rem
  xl: 4rem
  xxl: 8rem
grid:
  columns: 12
  gutter: 1.5rem
  max_width: 1200px
breakpoints:
  mobile: 480px
  tablet: 768px
  desktop: 1024px
  wide: 1440px
type_scale:
  body: 1rem/1.5
  h6: 0.875rem/1.3
  h5: 1rem/1.3
  h4: 1.25rem/1.25
  h3: 1.5rem/1.2
  h2: 2rem/1.15
  h1: 3rem/1.1
  display: 4.5rem/1.05
transition: 200ms ease
==============================================
AESTHETIC 1: SWISS (International Typographic Style)
tokens:
  fonts:
    primary: Helvetica Neue, Helvetica, Arial, sans-serif
    mono: SF Mono, Menlo, monospace
  colors:
    background: '#F5F5F5'
    surface: '#FFFFFF'
    text_primary: '#1A1A1A'
    text_secondary: '#666666'
    accent: '#E30613'
    rule: '#CCCCCC'
  spacing: 8px grid
  alignment: asymmetric, flush left, ragged right
  rhythm: 4:3 module ratio
layout: asymmetric two-column grid, generous margins, content offset from center, floated figures with captions set in italic, horizontal rules as section dividers, no borders or boxes — space is the separator
mood: clarity, authority, objectivity, precision
Swiss template — single-file HTML:
<html lang=en>
<meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Swiss — International Typographic Style</title>
<style>
:root{--font-sans:'Helvetica Neue',Helvetica,Arial,sans-serif;--font-mono:SF Mono,Menlo,monospace;--bg:#F5F5F5;--surface:#FFF;--text:#1A1A1A;--text2:#666;--accent:#E30613;--rule:#CCC;--space:8px;--max-w:1200px}
*{margin:0;padding:0;box-sizing:border-box}
html{background:var(--bg);color:var(--text);font-family:var(--font-sans);font-weight:400;font-size:16px;line-height:1.5;-webkit-font-smoothing:antialiased}
body{padding:calc(var(--space)*12) calc(var(--space)*6);max-width:var(--max-w);margin:0 auto}
.grid{display:grid;grid-template-columns:repeat(12,1fr);gap:var(--space)*3}
.col-4{grid-column:span 4}.col-6{grid-column:span 6}.col-8{grid-column:span 8}.col-10{grid-column:span 10;grid-column-start:3}
h1{font-size:3rem;font-weight:300;line-height:1.1;letter-spacing:-0.02em;margin-bottom:calc(var(--space)*6)}
h2{font-size:1.5rem;font-weight:500;line-height:1.2;margin-bottom:calc(var(--space)*3);padding-top:calc(var(--space)*6);border-top:1px solid var(--rule)}
h3{font-size:1rem;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:var(--space)}
p{margin-bottom:calc(var(--space)*3);max-width:72ch}
p+.meta{margin-top:calc(var(--space)*-2);margin-bottom:calc(var(--space)*4);color:var(--text2);font-size:0.825rem}
hr{margin:calc(var(--space)*6) 0;border:0;border-top:1px solid var(--rule)}
figure{margin:calc(var(--space)*4) 0;padding:calc(var(--space)*4);background:var(--surface);border-left:4px solid var(--accent)}
figure img{width:100%;display:block}
figcaption{font-style:italic;font-size:0.875rem;color:var(--text2);margin-top:var(--space)}
blockquote{margin:calc(var(--space)*4) 0;padding-left:calc(var(--space)*4);border-left:3px solid var(--accent);font-size:1.25rem;font-weight:300;font-style:italic;color:var(--text2)}
.grid-2{columns:2;column-gap:calc(var(--space)*4)}
@media(max-width:768px){body{padding:calc(var(--space)*4) var(--space)*2}.col-8,.col-10,.col-6{grid-column:span 12}.grid-2{columns:1}h1{font-size:2rem}}
</style>
<div class=grid>
<header class=col-10>
<h1>Swiss Design<br>International Typographic Style</h1>
<p class=meta>Grid systems & asymmetrical balance &middot; 1950s&ndash;present</p>
</header>
</div>
<div class=grid>
<section class=col-8>
<h2>Grid & Rhythm</h2>
<p>The modular grid is the skeleton. Every element aligns to the 8px baseline. Content sits flush left, ragged right. Asymmetry creates tension — the reader's eye moves across the page, never sits still.</p>
<hr>
<h2>Typography</h2>
<p>Helvetica Neue in three weights: light for display, regular for body, medium for subheads. All caps for labels. No hyphens. No justification. The type itself is the ornament.</p>
</section>
<aside class=col-4 style="margin-top:3rem">
<p class=meta><strong>Key principles</strong></p>
<p>Clarity over decoration<br>Function over flourish<br>Space as separator<br>Grid as guide, not cage</p>
</aside>
</div>
<hr>
<div class=grid>
<figure class=col-6>
<div style="height:200px;background:var(--text);opacity:0.1;display:flex;align-items:center;justify-content:center;color:var(--text);font-size:0.825rem">FIGURE — PLACEHOLDER</div>
<figcaption>Asymmetric image placement with caption offset below the baseline grid</figcaption>
</figure>
<div class=col-4>
<h3>Asymmetric Balance</h3>
<p>A large figure on the left balances smaller text on the right. Not symmetrical — equivalent visual weight at different positions. The golden ratio guides proportions.</p>
</div>
</div>
<hr>
<blockquote>The typographer must obey the principle of clarity and order. This is the essential discipline of the International Style. — Emil Ruder</blockquote>
==============================================
AESTHETIC 2: MINIMAL (Dieter Rams)
tokens:
  fonts:
    primary: Inter, system-ui, sans-serif
    ui: SF Pro Text, system-ui
  colors:
    background: '#FAFAFA'
    surface: '#FFFFFF'
    text_primary: '#222222'
    text_secondary: '#888888'
    accent: '#3366FF'
    rule: '#EEEEEE'
    muted: '#F0F0F0'
  spacing: 16px grid (single unit, never combine)
  alignment: strict left, vertical baseline grid
  rhythm: exact multiples of 16px — no fractional margins
layout: single-column or two-column with massive whitespace, content centered in the upper third, all elements share one spacing unit, precise vertical rhythm, no decoration — only essential elements, every element justifies its existence
mood: calm, honest, reduced, intentional, quiet
Minimal template — single-file HTML:
<html lang=en>
<meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Minimal — Dieter Rams</title>
<style>
:root{--sans:Inter,system-ui,sans-serif;--ui:'SF Pro Text',system-ui;--bg:#FAFAFA;--surface:#FFF;--text:#222;--text2:#888;--accent:#36F;--rule:#EEE;--muted:#F0F0F0;--unit:16px}
*{margin:0;padding:0;box-sizing:border-box}
html{background:var(--bg);color:var(--text);font-family:var(--sans);font-weight:400;font-size:16px;line-height:1.5;-webkit-font-smoothing:antialiased}
body{padding:calc(var(--unit)*6);max-width:720px;margin:0 auto}
h1{font-size:2rem;font-weight:500;line-height:1.2;letter-spacing:-0.01em;margin-bottom:var(--unit)}
h2{font-size:1.25rem;font-weight:500;line-height:1.3;margin-top:calc(var(--unit)*4);margin-bottom:var(--unit);padding-top:calc(var(--unit)*2);border-top:1px solid var(--rule)}
h3{font-size:0.875rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:var(--text2);margin-bottom:var(--unit)}
p{margin-bottom:calc(var(--unit)*2);max-width:65ch;color:var(--text)}
p.meta{color:var(--text2);font-size:0.75rem;letter-spacing:0.02em}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
hr{border:0;border-top:1px solid var(--rule);margin:calc(var(--unit)*3) 0}
.card{background:var(--surface);padding:calc(var(--unit)*2);border-radius:0;margin-bottom:calc(var(--unit)*2)}
.card p:last-child{margin-bottom:0}
.tag{display:inline-block;font-size:0.75rem;padding:2px 8px;background:var(--muted);color:var(--text2);margin-right:4px;margin-bottom:4px;letter-spacing:0.02em}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:calc(var(--unit)*2)}
@media(max-width:600px){body{padding:calc(var(--unit)*3)}.grid-2{grid-template-columns:1fr}h1{font-size:1.5rem}}
</style>
<header>
<h1>Less but Better</h1>
<p class=meta>Dieter Rams &middot; 10 principles of good design</p>
</header>
<hr>
<section>
<h3>01 / Innovative</h3>
<p>Good design makes a product useful. It has to satisfy certain criteria, not only functional but also psychological and aesthetic. Good design emphasises the usefulness of a product whilst disregarding anything that could possibly detract from it.</p>
<h3>02 / Aesthetic</h3>
<p>The aesthetic quality of a product is integral to its usefulness because products are used every day and have an effect on people and their well-being. Only well-executed objects can be beautiful.</p>
<h3>03 / Understandable</h3>
<p>It clarifies the product's structure. Better still, it can make the product clearly express its function by making use of the user's intuition. At best, it is self-explanatory.</p>
<h3>04 / Unobtrusive</h3>
<p>Products fulfilling a purpose are like tools. They are neither decorative objects nor works of art. Their design should therefore be neutral and restrained, to leave room for the user's self-expression.</p>
</section>
<hr>
<div class=grid-2>
<div class=card>
<p class=meta style=margin-bottom:8px>Honest</p>
<p>It does not make a product more innovative, powerful or valuable than it really is.</p>
</div>
<div class=card>
<p class=meta style=margin-bottom:8px>Long-lasting</p>
<p>It avoids being fashionable and therefore never appears antiquated.</p>
</div>
<div class=card>
<p class=meta style=margin-bottom:8px>Thorough</p>
<p>Nothing must be arbitrary or left to chance. Care and accuracy in the design process show respect towards the user.</p>
</div>
<div class=card>
<p class=meta style=margin-bottom:8px>Minimal</p>
<p>Less, but better — because it concentrates on the essential aspects.</p>
</div>
</div>
==============================================
AESTHETIC 3: BRUTALIST
tokens:
  fonts:
    primary: 'Space Mono', 'Courier New', monospace
    heading: 'Righteous', 'Arial Black', impact
  colors:
    background: '#FFFFFF'
    surface: '#F0F0F0'
    text_primary: '#000000'
    text_secondary: '#444444'
    accent: '#000000'
    rule: '#000000'
    highlight: '#FFFF00'
  borders: thick solid black (4px minimum)
  spacing: aggressive — large gaps, no padding on containers
layout: exposed structural grid with visible column gutters, content explodes to edges, heavy horizontal rules as structural elements, raw black on white, no rounded corners, no shadows, no gradients, content bleeds off edges intentionally, elements collide
mood: raw, honest, powerful, confrontational, anti-aesthetic
Brutalist template — single-file HTML:
<html lang=en>
<meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Brutalist — Raw Structure</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Righteous&display=swap');
:root{--mono:'Space Mono','Courier New',monospace;--head:'Righteous','Arial Black',impact,sans-serif;--bg:#FFF;--text:#000;--text2:#444;--accent:#000;--hl:#FF0;--border:4px solid #000}
*{margin:0;padding:0;box-sizing:border-box}
html{background:var(--bg);color:var(--text);font-family:var(--mono);font-weight:400;font-size:14px;line-height:1.4}
body{max-width:1400px;margin:0 auto}
header{border-bottom:var(--border);padding:2rem;text-align:center}
h1{font-family:var(--head);font-size:4.5rem;line-height:1;text-transform:uppercase;letter-spacing:-0.03em;word-break:break-all}
h2{font-family:var(--head);font-size:2rem;text-transform:uppercase;line-height:1;margin-bottom:1rem}
h3{font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem}
p{margin-bottom:1rem;max-width:none}
.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:0}
.grid-3>*{border-right:var(--border);border-bottom:var(--border);padding:1.5rem}
.grid-3>*:nth-child(3n){border-right:0}
.block{border:var(--border);padding:2rem;margin:2rem;background:var(--bg)}
.block.highlight{background:var(--hl);color:#000}
.mono{font-family:var(--mono)}
hr{border:0;border-top:var(--border);margin:0}
.big{font-size:3rem;font-family:var(--head);text-transform:uppercase;line-height:0.9;border:0;padding:2rem;border-bottom:var(--border)}
figure{border:var(--border);padding:3rem 2rem;text-align:center;margin:2rem;background:var(--bg);font-size:0.75rem;text-transform:uppercase;letter-spacing:0.15em}
@media(max-width:768px){.grid-3{grid-template-columns:1fr}.grid-3>*{border-right:0}h1{font-size:2.5rem}.block,.figure{margin:1rem}}
</style>
<header>
<h1>BRUTAL</h1>
<p style=font-size:0.75rem;letter-spacing:0.2em;text-transform:uppercase;margin-top:0.5rem>structure &gt; decoration &middot; content &gt; chrome</p>
</header>
<section class=grid-3>
<div>
<h3>01 / RAW MATERIALS</h3>
<p>Concrete. Steel. Glass. Exposed. Unpainted. The structure is the facade. The grid is the ornament. Brutalism rejects the superficial.</p>
</div>
<div>
<h3>02 / SCALE</h3>
<p>Oversized. Monumental. Typography at display sizes. Margins that swallow content. Brutalism demands attention through scale alone.</p>
</div>
<div>
<h3>03 / HONESTY</h3>
<p>No rounded corners. No shadows. No gradients. Every pixel is declared. The designer's hand is visible in every structural decision.</p>
</div>
<div>
<h3>04 / TENSION</h3>
<p>Elements collide. Borders overlap. Content bleeds off edges. The page is a construction site — the scaffolding is part of the design.</p>
</div>
<div>
<h3>05 / MONOCHROME</h3>
<p>Black. White. Maybe yellow for emphasis. Color is a decision, not a default. Most of the time, you don't need it.</p>
</div>
<div>
<h3>06 / GRID</h3>
<p>The grid is visible. Column gutters are gaps, not whitespace. The underlying structure is the subject. Layout is infrastructure.</p>
</div>
</section>
<div class=big>BRUTALISM IS NOT A STYLE<br>IT IS AN ATTITUDE</div>
<figure>
[ FIGURE — 4PX BORDER, NO FRILLS ]
<figcaption style=margin-top:1rem;font-size:0.625rem;letter-spacing:0.15em>Every element earns its border</figcaption>
</figure>
<section class=grid-3>
<div><p>08<br><big style=font-size:2rem;font-family:var(--head)>Corbusier</big><br>Raw concrete. Beton brut. The origin.</p></div>
<div><p>09<br><big style=font-size:2rem;font-family:var(--head)>Kahn</big><br>Monumental geometry. Light as material.</p></div>
<div><p>10<br><big style=font-size:2rem;font-family:var(--head)>Smithson</big><br>New Brutalism. Ethics over aesthetics.</p></div>
</section>
==============================================
AESTHETIC 4: GLASS (Glassmorphism)
tokens:
  fonts:
    primary: 'SF Pro Display', system-ui, sans-serif
    display: 'SF Pro Rounded', system-ui
  colors:
    background_gradient_start: '#667eea'
    background_gradient_end: '#764ba2'
    glass_bg: 'rgba(255,255,255,0.15)'
    glass_border: 'rgba(255,255,255,0.25)'
    glass_shadow: 'rgba(0,0,0,0.1)'
    text_primary: '#FFFFFF'
    text_secondary: 'rgba(255,255,255,0.7)'
    accent: '#FFFFFF'
    highlight: 'rgba(255,255,255,0.3)'
  glass: backdrop-blur(20px), border-radius: 16px, semi-transparent border, layered shadow
layout: full-bleed gradient or video background, floating glass cards with depth stacking, content panels at varying z-index creating parallax-like depth, circular and organic elements breaking grid rigidity, frosted overlays on images, glowing accent borders
mood: futuristic, ethereal, premium, depthful, immersive, dreamlike
Glass template — single-file HTML:
<html lang=en>
<meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Glass — Depth & Translucency</title>
<style>
:root{--sans:'SF Pro Display',system-ui,sans-serif;--rounded:'SF Pro Rounded',system-ui;--bg1:#667eea;--bg2:#764ba2;--glass:rgba(255,255,255,0.12);--border:rgba(255,255,255,0.2);--shadow:rgba(0,0,0,0.08);--text:#FFF;--text2:rgba(255,255,255,0.7);--hl:rgba(255,255,255,0.25);--radius:16px}
*{margin:0;padding:0;box-sizing:border-box}
html{background:linear-gradient(135deg,var(--bg1),var(--bg2));min-height:100vh;color:var(--text);font-family:var(--sans);-webkit-font-smoothing:antialiased}
body{padding:3rem;max-width:1200px;margin:0 auto;position:relative;z-index:1}
body::before{content:'';position:fixed;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle at 30% 20%,rgba(255,255,255,0.08) 0%,transparent 50%),radial-gradient(circle at 70% 80%,rgba(255,255,255,0.05) 0%,transparent 40%);pointer-events:none;z-index:0}
.glass{background:var(--glass);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border:1px solid var(--border);border-radius:var(--radius);box-shadow:0 8px 32px var(--shadow);padding:2.5rem;margin-bottom:2rem;position:relative;z-index:2}
.glass:hover{border-color:rgba(255,255,255,0.35);box-shadow:0 12px 48px rgba(0,0,0,0.12)}
h1{font-size:3.5rem;font-weight:600;line-height:1.1;letter-spacing:-0.03em;margin-bottom:1rem;background:linear-gradient(135deg,#FFF 60%,rgba(255,255,255,0.5));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
h2{font-size:1.5rem;font-weight:500;margin-bottom:1.5rem;color:var(--text2)}
h3{font-size:0.875rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:var(--text2);margin-bottom:0.75rem}
p{color:var(--text2);line-height:1.6;margin-bottom:1rem;max-width:65ch}
p strong{color:var(--text)}
.pill{display:inline-block;background:var(--hl);backdrop-filter:blur(4px);padding:4px 14px;border-radius:999px;font-size:0.75rem;letter-spacing:0.02em;margin-right:6px;margin-bottom:6px;border:1px solid rgba(255,255,255,0.1)}
.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem}
.float{position:relative;z-index:3;margin-top:-2rem}
.orb{width:300px;height:300px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,0.12),transparent 70%);position:fixed;top:-100px;right:-100px;pointer-events:none;z-index:0}
.orb2{width:200px;height:200px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,0.08),transparent 70%);position:fixed;bottom:10%;left:-50px;pointer-events:none;z-index:0}
@media(max-width:768px){body{padding:1.5rem}.grid-3,.grid-2{grid-template-columns:1fr}h1{font-size:2.5rem}}
</style>
<div class=orb></div>
<div class=orb2></div>
<header class=glass>
<h1>Glassmorphism</h1>
<h2>Depth through translucency & layered light</h2>
<p style=font-size:1.125rem>A design language built on frosted surfaces, ambient glow, and stacked depth. Every layer is a pane of glass — the background breathes through it.</p>
<div style=margin-top:1.5rem>
<span class=pill>backdrop-filter</span>
<span class=pill>frosted glass</span>
<span class=pill>depth stacking</span>
<span class=pill>ambient glow</span>
</div>
</header>
<section class=grid-3 style=margin-top:-0.5rem>
<div class=glass>
<h3>Translucency</h3>
<p>Surfaces are never opaque. Light passes through, revealing the layers beneath. The background gradient bleeds through every pane.</p>
</div>
<div class=glass>
<h3>Depth</h3>
<p>Cards float at different z-levels. Shadows are not drops — they are ambient occlusion between layers. Each pane occupies its own plane.</p>
</div>
<div class=glass>
<h3>Light</h3>
<p>Glow originates from within. Radial gradients simulate backlight. Borders catch virtual light sources. The interface feels alive.</p>
</div>
</section>
<section class=grid-2>
<div class=glass style=padding:3rem>
<h3>Platform Aesthetic</h3>
<p>Apple popularized this language. macOS Big Sur introduced frosted titlebars. iOS blurred everything beneath. Design moved from flat planes to volumetric light.</p>
<p style=font-size:0.875rem;color:var(--text2);margin-top:auto>White text on dark glass. Maximum contrast through minimum opacity.</p>
</div>
<div class=glass style=padding:3rem;text-align:center>
<big style=font-size:4rem;font-weight:200;line-height:1;display:block>∅</big>
<p style=margin-top:1rem;font-size:0.875rem>The void beneath every surface. Background is not background — it is atmosphere.</p>
</div>
</section>
==============================================
AESTHETIC 5: NEO-BRUTALIST
tokens:
  fonts:
    primary: 'Host Grotesk', system-ui, sans-serif
    display: 'Clash Display', system-ui, sans-serif
  colors:
    background: '#FFFDF7'
    surface: '#FFFFFF'
    text_primary: '#1A1A1A'
    text_secondary: '#666'
    accent_pink: '#FF3B7D'
    accent_yellow: '#FFD700'
    accent_lime: '#00E676'
    accent_blue: '#2979FF'
    rule: '#1A1A1A'
  borders: 3px solid black
  offset: '4px offset shadow (brutal flat shadow)'
layout: asymmetric overlapping sections, oversized type breaking grid, tilted/rotated elements, bright color blocks as structural dividers, hand-drawn vibe through precise geometry, playful scale shifts, sticky elements that overlap, decorative oversized numerals
mood: playful, confident, contemporary, electric, irreverent, bold
Neo-Brutalist template — single-file HTML:
<html lang=en>
<meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Neo-Brutalist — Playful Monolith</title>
<style>
:root{--body:'Host Grotesk',system-ui,sans-serif;--display:'Clash Display','Arial Black',impact,sans-serif;--bg:#FFFDF7;--surface:#FFF;--text:#1A1A1A;--text2:#666;--pink:#FF3B7D;--yellow:#FFD700;--lime:#00E676;--blue:#2979FF;--black:#1A1A1A;--border:3px solid var(--black);--offset:4px 4px 0px 0px var(--black)}
@import url('https://api.fontshare.com/v2/css?f[]=clash-display@400,600,700&f[]=host-grotesk@400,500&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
html{background:var(--bg);color:var(--text);font-family:var(--body);font-size:16px;line-height:1.5}
body{max-width:1200px;margin:0 auto;padding:0 2rem 4rem}
h1{font-family:var(--display);font-size:6rem;font-weight:700;line-height:0.85;letter-spacing:-0.04em;margin-bottom:0.5rem}
h2{font-family:var(--display);font-size:3rem;font-weight:600;line-height:1;margin-bottom:1.5rem}
h3{font-size:0.75rem;font-weight:500;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem}
p{margin-bottom:1rem;max-width:70ch}
.tag{display:inline-block;border:var(--border);padding:4px 12px;background:var(--surface);box-shadow:var(--offset);font-size:0.75rem;font-weight:500;text-transform:uppercase;margin-right:8px;margin-bottom:8px}
.tag:hover{transform:translate(-1px,-1px);box-shadow:6px 6px 0px 0px var(--black)}
.btn{display:inline-block;border:var(--border);padding:12px 28px;background:var(--pink);color:#FFF;font-family:var(--body);font-weight:600;text-transform:uppercase;font-size:0.875rem;letter-spacing:0.05em;box-shadow:var(--offset);cursor:default;margin-right:12px;margin-bottom:12px}
.btn.yellow{background:var(--yellow);color:var(--text)}.btn.lime{background:var(--lime);color:var(--text)}.btn.blue{background:var(--blue);color:#FFF}
.giant-num{font-family:var(--display);font-size:12rem;font-weight:700;line-height:0.8;color:var(--pink);position:relative;z-index:0;opacity:0.15;pointer-events:none;user-select:none}
.overlap{position:relative;margin-top:-4rem;z-index:2}
.bordered{border:var(--border);padding:2rem;background:var(--surface);box-shadow:var(--offset);margin-bottom:2rem}
.split{display:grid;grid-template-columns:1fr 1fr;gap:0;margin:3rem 0}
.split>*{border:var(--border);padding:2.5rem;background:var(--surface)}.split>*:first-child{border-right:0}
.marquee{overflow:hidden;white-space:nowrap;border-top:var(--border);border-bottom:var(--border);padding:0.75rem 0;font-family:var(--display);font-size:2rem;font-weight:600;text-transform:uppercase;letter-spacing:-0.02em;margin:3rem 0;background:var(--yellow);color:var(--text)}
@media(max-width:768px){h1{font-size:3rem}h2{font-size:2rem}.split{grid-template-columns:1fr}.split>*:first-child{border-right:var(--border);border-bottom:0}.giant-num{font-size:6rem}}
</style>
<header style="position:relative;padding-top:4rem">
<span class=giant-num style=position:absolute;top:-2rem;left:-1rem>01</span>
<h1>Neo-<br>Brutalist</h1>
<p style=font-size:1.25rem;font-weight:500;max-width:50ch>Contemporary brutality. Bright colors. Big type. Playful geometry. Zero fear.</p>
<div style=margin-top:2rem>
<span class=tag>big type</span>
<span class=tag>bright color</span>
<span class=tag>offset shadow</span>
<span class=tag>overlap</span>
<span class=tag>raw grid</span>
</div>
</header>
<div style=margin:3rem 0>
<span class=btn>Pink</span>
<span class=btn yellow>Yellow</span>
<span class=btn lime>Lime</span>
<span class=btn blue>Blue</span>
</div>
<section class=split>
<div>
<h3>The philosophy</h3>
<p>Neo-Brutalism takes the raw honesty of 1950s brutalism and injects color, humor, and digital-native playfulness. The grid is still exposed. The borders are still thick. But now they dance.</p>
<p>Color is structural. Yellow is not decoration — it is a section divider. Pink is not an accent — it is an action. The palette becomes part of the layout system.</p>
</div>
<div>
<h3>The rules</h3>
<p><strong>1.</strong> No rounded corners.</p>
<p><strong>2.</strong> Every element has a border or it does not exist.</p>
<p><strong>3.</strong> Offset shadow is not optional — it is the material.</p>
<p><strong>4.</strong> Scale until it breaks. Then scale more.</p>
<p><strong>5.</strong> Color is a structural element, not a decorative one.</p>
</div>
</section>
<div class=marquee>PLAYFUL GEOMETRY &bull; BOLD TYPOGRAPHY &bull; RAW STRUCTURE &bull; COLOR AS MATERIAL &bull;</div>
<section class=bordered>
<div style=display:flex;gap:3rem;flex-wrap:wrap;align-items:center>
<div style=flex:1>
<h2>Build with attitude</h2>
<p>Neo-Brutalism is the design language of the current web renaissance. It is unapologetic. It is memorable. It looks like someone cared enough to break the rules properly.</p>
</div>
<div style="flex:0 0 200px;text-align:center;font-family:var(--display);font-size:4rem;font-weight:700;line-height:1;color:var(--pink)">→</div>
</div>
</section>
<div class=overlap style=text-align:center;margin-bottom:-2rem>
<span class=giant-num style=font-size:8rem;opacity:0.1>05</span>
</div>
==============================================
DECISION MATRIX — Aesthetic Selection Guide
use_case: Landing page / SaaS hero
  recommended: Glass
  why: Depth and translucency create premium first impression. Gradient backgrounds feel energetic. Glass cards communicate modernity and polish.
  also_works: Neo-Brutalist (for edgy/YC-era startups)
  avoid: Brutalist (too confrontational for conversion)
use_case: Portfolio / Creative agency
  recommended: Swiss
  why: Grid precision and typographic hierarchy showcase work without competing. Asymmetric layouts feel curated. Red accent reads as design confidence.
  also_works: Minimal
  avoid: Glass (competes with content)
use_case: Editorial / Long-form reading
  recommended: Minimal
  why: Zero distraction. Maximal whitespace reduces cognitive load. Single-column with generous margins is proven for reading endurance.
  also_works: Swiss
  avoid: Neo-Brutalist (too loud for sustained reading)
use_case: Developer docs / API reference
  recommended: Brutalist
  why: Raw structure communicates engineering honesty. Monochrome reduces visual noise. Exposed grid mirrors code structure. High information density.
  also_works: Minimal
  avoid: Glass (reduced readability at high information density)
use_case: Personal site / Artist portfolio
  recommended: Neo-Brutalist
  why: Personality demands attention. Color and scale express individuality. Playful overlap signals creative confidence. Memorable.
  also_works: Brutalist (for fine art/photography)
  avoid: Minimal (risks feeling generic)
use_case: E-commerce / Product showcase
  recommended: Glass
  why: Glass cards on dark gradient make products glow. Depth stacking creates hierarchy. Premium feel supports higher price perception.
  also_works: Swiss (for luxury/minimal brands)
  avoid: Brutalist (negative association with cheap/aggressive)
use_case: Dashboard / Data visualization
  recommended: Minimal
  why: Information is the decoration. Restrained color palette keeps data legible. Cardinals spacing ensures consistent rhythm across charts.
  also_works: Brutalist (for internal tools)
  avoid: Neo-Brutalist (color competes with data encoding)
use_case: Agency / Design studio site
  recommended: Swiss
  why: Demonstrates design literacy. Grid precision signals mastery. Red accent is a recognizable design reference. Speaks to other designers.
  also_works: Neo-Brutalist (for younger/edgier studios)
  avoid: Minimal (risks looking unfinished/undesigned)
use_case: Mobile app UI
  recommended: Glass
  why: Native OS conventions (iOS). backdropped translucency feels native. Light layers map to OS behaviors. Consistent with platform expectations.
  also_works: Minimal
  avoid: Brutalist (fat borders waste screen real estate)
use_case: Blog / Newsletter
  recommended: Minimal
  why: Content is king. Readability is the only metric. Type scale and baseline grid serve the text. Nothing else matters.
  also_works: Swiss
  avoid: Glass (gradient backgrounds reduce text legibility long-term)
==============================================
LAYER COMPATIBILITY — When to break the rules
rule_break: Use glass cards on a brutalist layout
  verdict: Works. The transparency softens the raw borders. Creates a high/low tension. Best for hero sections.
rule_break: Use neo-brutalist color blocks inside a swiss grid
  verdict: Works. The grid disciplines the color. Color becomes accent within structure. Common in contemporary Swiss-adjacent studios.
rule_break: Use minimalist whitespace with brutalist borders
  verdict: Risky. The borders contradict the quiet. Best done with hairline (1px) borders instead of 4px. Read: "quiet brutality."
rule_break: Use brutalism type scale (4rem+) with glass backgrounds
  verdict: Works for hero headings. The massive type anchors the floating glass. Creates ground in the dream.
rule_break: Mix neo-brutalist and glass in same layout
  verdict: Risky without clear z-index hierarchy. Glass in background layer, neo-brutalist elements in foreground. Overlap works if the glass is the backdrop space.
==============================================
FIVE TEMPLATES DELIVERED. Each is a complete self-contained HTML document. Copy any template block, save as .html, open in browser. Design tokens are declared as CSS custom properties at the root of each file — override colors, type scale, spacing at :root to generate variants within the same aesthetic family. Decision matrix covers 10 common use cases with explicit recommendations, alternatives, and anti-patterns.