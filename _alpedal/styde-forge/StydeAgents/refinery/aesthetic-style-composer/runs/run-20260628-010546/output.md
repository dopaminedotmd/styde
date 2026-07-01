Aesthetic Style Composer - Template Pack v1
=============================================
*** TEMPLATE 1: SWISS (International Typographic Style) ***
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Swiss Grid · International Typographic Style</title>
<style>
:root {
  --red: #E63946;
  --blue: #1D3557;
  --yellow: #F1FAEE;
  --black: #1A1A1A;
  --white: #F5F5F5;
  --gray: #8D99AE;
  --grid-gap: 24px;
  --col-count: 12;
  --font-display: 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif;
  --font-body: 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif;
  --baseline: 8px;
  --measure: 66ch;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html { font-size: 16px; }
body {
  font-family: var(--font-body);
  font-weight: 400;
  line-height: 1.5;
  color: var(--black);
  background: var(--white);
  padding: calc(var(--baseline) * 6);
}
.grid {
  display: grid;
  grid-template-columns: repeat(var(--col-count), 1fr);
  gap: var(--grid-gap);
  max-width: 1200px;
  margin: 0 auto;
}
.grid__item {
  grid-column: span 4;
}
.grid__item--wide {
  grid-column: span 8;
}
.grid__item--full {
  grid-column: 1 / -1;
}
h1 {
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 5vw, 4.5rem);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  line-height: 0.95;
  color: var(--red);
  margin-bottom: calc(var(--baseline) * 2);
}
h2 {
  font-family: var(--font-display);
  font-size: clamp(1.5rem, 3vw, 2.25rem);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--blue);
  margin-bottom: calc(var(--baseline) * 2);
}
h3 {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--gray);
  margin-bottom: var(--baseline);
}
p {
  font-size: 1rem;
  line-height: 1.625;
  max-width: var(--measure);
  margin-bottom: calc(var(--baseline) * 2);
  color: var(--black);
}
.small {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--gray);
}
.block {
  background: var(--black);
  color: var(--white);
  padding: calc(var(--baseline) * 4);
  margin-bottom: calc(var(--baseline) * 3);
}
.block--accent {
  background: var(--red);
}
.block--secondary {
  background: var(--blue);
}
.asymmetric {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--grid-gap);
  margin-bottom: calc(var(--baseline) * 4);
}
.rule {
  height: 4px;
  background: var(--red);
  width: 60px;
  margin-bottom: calc(var(--baseline) * 3);
}
.rule--blue {
  background: var(--blue);
  width: 120px;
}
.grid-diagram {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 4px;
  margin: calc(var(--baseline) * 3) 0;
}
.grid-diagram span {
  height: 24px;
  background: var(--gray);
  opacity: 0.3;
}
.grid-diagram span:nth-child(4n+1) { background: var(--red); opacity: 0.5; }
@media (max-width: 768px) {
  body { padding: calc(var(--baseline) * 2); }
  .asymmetric { grid-template-columns: 1fr; }
  .grid__item { grid-column: 1 / -1; }
  .grid__item--wide { grid-column: 1 / -1; }
}
@media (min-width: 769px) and (max-width: 1024px) {
  .grid { grid-template-columns: repeat(8, 1fr); }
}
</style>
</head>
<body>
<div class=grid>
  <div class=grid__item--full>
    <div class=rule></div>
    <h1>International<br>Typographic<br>Style</h1>
    <p class=small>Grid system · Asymmetric balance · Swiss design</p>
  </div>
</div>
<div class=asymmetric>
  <div>
    <h3>Modular Grid</h3>
    <p>The 12-column grid system provides mathematical precision and flexible layout structures. Each module follows the 8px baseline rhythm for vertical consistency across all typographic elements.</p>
    <div class=grid-diagram>
      <span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span>
    </div>
  </div>
  <div>
    <h3>Akzidenz-Grotesk</h3>
    <p>Neue Haas Grotesk (Helvetica) and Akzidenz-Grotesk form the typographic backbone. Sans-serif, neutral, highly legible. Asymmetric compositions create dynamic tension while maintaining strict grid alignment.</p>
  </div>
</div>
<div class=grid>
  <div class=grid__item>
    <div class=block><h2 style=color:var(--white)>01</h2><p style=color:var(--white);font-size:0.875rem>Primary palette anchored by signal red</p></div>
  </div>
  <div class=grid__item>
    <div class="block block--accent"><h2 style=color:var(--white)>02</h2><p style=color:var(--white);font-size:0.875rem>Structural blue for depth</p></div>
  </div>
  <div class=grid__item>
    <div class="block block--secondary"><h2 style=color:var(--white)>03</h2><p style=color:var(--white);font-size:0.875rem>Pure geometry, no decoration</p></div>
  </div>
</div>
<div class=grid>
  <div class=grid__item--wide>
    <div class=rule--blue></div>
    <h3>Design Tokens</h3>
    <p style=font-size:0.875rem>Type: Helvetica Neue / Akzidenz-Grotesk · Grid: 12-col, 24px gap · Scale: 1.25 modular · Baseline: 8px · Max measure: 66ch · Color: signal red #E63946, navy #1D3557, off-white #F1FAEE</p>
  </div>
  <div class=grid__item>
    <h3>Use Case</h3>
    <p style=font-size:0.875rem>Editorial layouts, institutional branding, posters, wayfinding systems, data-heavy dashboards requiring clarity</p>
  </div>
</div>
</body>
</html>
*** TEMPLATE 2: MINIMAL (Dieter Rams) ***
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Minimal · Less But Better</title>
<style>
:root {
  --bg: #FAFAF8;
  --text: #222222;
  --text-secondary: #888888;
  --accent: #2B2B2B;
  --border: #E0E0E0;
  --white: #FFFFFF;
  --spacing-unit: 8px;
  --max-width: 960px;
  --font-sans: -apple-system, 'Helvetica Neue', sans-serif;
  --font-mono: 'SF Mono', 'Menlo', monospace;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html { font-size: 16px; -webkit-font-smoothing: antialiased; }
body {
  font-family: var(--font-sans);
  font-weight: 400;
  line-height: 1.6;
  color: var(--text);
  background: var(--bg);
  padding: calc(var(--spacing-unit) * 12);
  min-height: 100vh;
}
.container {
  max-width: var(--max-width);
  margin: 0 auto;
}
header {
  margin-bottom: calc(var(--spacing-unit) * 16);
  border-bottom: 1px solid var(--border);
  padding-bottom: calc(var(--spacing-unit) * 4);
}
h1 {
  font-size: clamp(1.25rem, 2vw, 1.5rem);
  font-weight: 500;
  letter-spacing: 0.04em;
  color: var(--text);
  margin-bottom: var(--spacing-unit);
}
h2 {
  font-size: clamp(2rem, 4vw, 3.5rem);
  font-weight: 300;
  line-height: 1.15;
  color: var(--accent);
  margin-bottom: calc(var(--spacing-unit) * 3);
  max-width: 18ch;
}
h3 {
  font-size: 1rem;
  font-weight: 500;
  color: var(--text);
  margin-bottom: var(--spacing-unit);
}
p {
  font-size: 1rem;
  line-height: 1.7;
  color: var(--text-secondary);
  margin-bottom: calc(var(--spacing-unit) * 4);
  max-width: 42em;
}
.p-small {
  font-size: 0.8125rem;
  color: var(--text-secondary);
  letter-spacing: 0.02em;
}
.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: calc(var(--spacing-unit) * 6);
  margin-bottom: calc(var(--spacing-unit) * 10);
}
.grid-3 {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: calc(var(--spacing-unit) * 5);
  margin-bottom: calc(var(--spacing-unit) * 10);
}
.card {
  background: var(--white);
  border: 1px solid var(--border);
  padding: calc(var(--spacing-unit) * 5);
  transition: all 0.2s ease;
}
.card:hover {
  border-color: var(--accent);
}
.card h3 {
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-secondary);
  margin-bottom: calc(var(--spacing-unit) * 2);
}
.card p {
  font-size: 0.9375rem;
  margin-bottom: 0;
}
.rule {
  width: 32px;
  height: 2px;
  background: var(--accent);
  margin-bottom: calc(var(--spacing-unit) * 4);
}
.space-block {
  height: calc(var(--spacing-unit) * 8);
}
.number {
  font-size: 3.5rem;
  font-weight: 200;
  color: var(--border);
  line-height: 1;
  margin-bottom: calc(var(--spacing-unit) * 2);
}
.principle {
  margin-bottom: calc(var(--spacing-unit) * 10);
}
.principle p {
  margin-bottom: 0;
}
footer {
  border-top: 1px solid var(--border);
  padding-top: calc(var(--spacing-unit) * 4);
  margin-top: calc(var(--spacing-unit) * 16);
  display: flex;
  justify-content: space-between;
  font-size: 0.8125rem;
  color: var(--text-secondary);
}
@media (max-width: 768px) {
  body { padding: calc(var(--spacing-unit) * 4); }
  .grid-2, .grid-3 { grid-template-columns: 1fr; }
  h2 { font-size: 1.75rem; }
}
</style>
</head>
<body>
<div class=container>
<header>
  <h1>Dieter Rams · 10 Principles</h1>
</header>
<div>
  <h2>Less but better.<br>Weniger aber besser.</h2>
  <div class=rule></div>
  <p>Good design is as little design as possible. Back to purity, back to simplicity. Every element has purpose. Nothing ornamental, nothing superfluous.</p>
</div>
<div class=space-block></div>
<div class=grid-3>
  <div class=card>
    <div class=number>01</div>
    <h3>Innovative</h3>
    <p>Good design makes a product useful. It optimises utility while discarding everything that detracts from function.</p>
  </div>
  <div class=card>
    <div class=number>02</div>
    <h3>Honest</h3>
    <p>It does not make a product more innovative, powerful or valuable than it really is. No manipulation.</p>
  </div>
  <div class=card>
    <div class=number>03</div>
    <h3>Unobtrusive</h3>
    <p>Products fulfilling a purpose are like tools. They are neither decorative objects nor works of art.</p>
  </div>
</div>
<div class=grid-2>
  <div class=principle>
    <h3>Design System Tokens</h3>
    <p class=p-small>Spacing: 8px modular scale · Type: system sans-serif, SF Mono · Color: off-white #FAFAF8, charcoal #2B2B2B, warm gray #888 · Grid: implicit, trust the whitespace · Max measure: 42em · Border: 1px solid #E0E0E0</p>
  </div>
  <div class=principle>
    <h3>When To Use</h3>
    <p class=p-small>Product interfaces, documentation sites, premium brand landing pages, editorial systems where content is the hero. Avoid for playful, youthful, or entertainment contexts.</p>
  </div>
</div>
<footer>
  <span>Weniger aber besser</span>
  <span>Braun · 1955–1995</span>
</footer>
</div>
</body>
</html>
*** TEMPLATE 3: BRUTALIST ***
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>BRUTALIST · RAW STRUCTURE</title>
<style>
:root {
  --black: #0A0A0A;
  --white: #F0F0F0;
  --gray-1: #2A2A2A;
  --gray-2: #555555;
  --gray-3: #999999;
  --accent: #CC0000;
  --border-w: 4px;
  --font-display: 'Impact', 'Arial Black', sans-serif;
  --font-body: 'Courier New', 'Courier', monospace;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html { font-size: 16px; }
body {
  font-family: var(--font-body);
  background: var(--white);
  color: var(--black);
  line-height: 1.4;
}
.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0;
}
.border-box {
  border: var(--border-w) solid var(--black);
  padding: 24px;
  margin-bottom: 12px;
}
header.border-box {
  background: var(--black);
  color: var(--white);
  margin-top: 12px;
}
h1 {
  font-family: var(--font-display);
  font-size: clamp(3rem, 8vw, 7rem);
  text-transform: uppercase;
  letter-spacing: -0.02em;
  line-height: 0.9;
  color: var(--white);
}
h2 {
  font-family: var(--font-display);
  font-size: clamp(1.5rem, 4vw, 3rem);
  text-transform: uppercase;
  letter-spacing: 0.02em;
  line-height: 1;
  margin-bottom: 12px;
  color: var(--black);
}
h3 {
  font-family: var(--font-body);
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  font-weight: 700;
  border-bottom: var(--border-w) solid var(--black);
  padding-bottom: 8px;
  margin-bottom: 16px;
}
p {
  font-size: 1rem;
  line-height: 1.5;
  margin-bottom: 16px;
}
.exposed-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}
.exposed-grid > div {
  border: var(--border-w) solid var(--black);
  padding: 16px;
  background: var(--white);
}
.exposed-grid > div:nth-child(1) { background: var(--black); color: var(--white); }
.block-heavy {
  border: 8px solid var(--black);
  padding: 32px;
  background: var(--accent);
  color: var(--white);
  margin-bottom: 12px;
}
.block-heavy h2 { color: var(--white); }
.block-heavy p { color: var(--white); font-weight: 700; }
.rule-heavy {
  height: 8px;
  background: var(--black);
  width: 100%;
  margin: 12px 0;
}
.rule-heavy--accent {
  height: 4px;
  background: var(--accent);
  width: 40%;
}
.invert {
  background: var(--black);
  color: var(--white);
  border-color: var(--white);
}
.mono-stripe {
  display: flex;
  gap: 0;
  margin: 12px 0;
}
.mono-stripe span {
  flex: 1;
  height: 24px;
}
.mono-stripe span:nth-child(odd) { background: var(--black); }
.mono-stripe span:nth-child(even) { background: var(--white); border: 2px solid var(--black); }
.label {
  font-family: var(--font-body);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--gray-2);
  border: var(--border-w) solid var(--gray-3);
  display: inline-block;
  padding: 4px 12px;
  margin-bottom: 12px;
}
.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.two-col > div {
  border: var(--border-w) solid var(--black);
  padding: 24px;
}
footer {
  border-top: 8px solid var(--black);
  padding: 24px 0;
  margin-top: 12px;
  text-align: center;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.2em;
}
@media (max-width: 768px) {
  .exposed-grid { grid-template-columns: 1fr 1fr; }
  .two-col { grid-template-columns: 1fr; }
  .border-box { padding: 16px; border-width: 3px; }
}
</style>
</head>
<body>
<div class=container>
<header class=border-box>
  <h1>BRUTALIST</h1>
  <p style=color:var(--gray-3);font-size:0.75rem;text-transform:uppercase;letter-spacing:0.2em>> EXPOSED STRUCTURE · NO APOLOGIES · RAW CONCRETE <</p>
  <div class=mono-stripe><span></span><span></span><span></span><span></span><span></span><span></span></div>
</header>
<div class=border-box style=border-top:0>
  <span class=label>MANIFESTO</span>
  <p style=font-size:1.125rem;font-weight:700>Architecture is what columns and beams do. Decoration is a crime. The grid is not a tool it is the truth. Every border every gap every weight is exposed.</p>
  <div class=rule-heavy--accent></div>
</div>
<div class=block-heavy>
  <h2>RAW MATERIAL</h2>
  <p>Concrete · Steel · Glass. No paint. No veneer. No hiding. The structure is the aesthetic. The system is the decoration.</p>
</div>
<div class=exposed-grid>
  <div style=font-family:var(--font-display);font-size:2rem;line-height:1>01</div>
  <div><h3 style=border:0;margin:0;padding:0>Honest</h3><p style=font-size:0.875rem;margin:0>Materials exposed</p></div>
  <div><h3 style=border:0;margin:0;padding:0>Heavy</h3><p style=font-size:0.875rem;margin:0>Borders 4–8px</p></div>
  <div><h3 style=border:0;margin:0;padding:0>Raw</h3><p style=font-size:0.875rem;margin:0>Monochrome base</p></div>
</div>
<div class=two-col>
  <div>
    <h3>Design Tokens</h3>
    <p style=font-size:0.8125rem>Type: Impact / Arial Black for display, Courier New for body · Grid: 4-column exposed · Borders: 4px minimum · Palette: #0A0A0A #F0F0F0 #CC0000 · Stripe pattern as ornament</p>
  </div>
  <div>
    <h3>When To Use</h3>
    <p style=font-size:0.8125rem>Architecture portfolios, art galleries, underground culture, developer docs, anything that demands attention through raw honesty. Avoid for luxury, healthcare, children.</p>
  </div>
</div>
<footer>
  BRUTALISM · 1950s–1970s · REVIVAL · 2020s
</footer>
</div>
</body>
</html>
*** TEMPLATE 4: GLASS (Apple-inspired Glassmorphism) ***
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Glass · Depth & Frost</title>
<style>
:root {
  --glass-bg: rgba(255, 255, 255, 0.18);
  --glass-border: rgba(255, 255, 255, 0.30);
  --glass-shadow: rgba(0, 0, 0, 0.06);
  --glass-blur: 24px;
  --text-primary: #1C1C1E;
  --text-secondary: #636366;
  --accent: #007AFF;
  --accent-glow: rgba(0, 122, 255, 0.25);
  --gradient-start: #667EEA;
  --gradient-mid: #764BA2;
  --gradient-end: #F093FB;
  --bg-dark: #0A0A0F;
  --spacing: 20px;
  --radius: 20px;
  --font: -apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html { font-size: 16px; }
body {
  font-family: var(--font);
  background: linear-gradient(135deg, var(--gradient-start), var(--gradient-mid), var(--gradient-end));
  background-attachment: fixed;
  min-height: 100vh;
  padding: calc(var(--spacing) * 2);
  display: flex;
  flex-direction: column;
  align-items: center;
  -webkit-font-smoothing: antialiased;
}
.container {
  max-width: 1100px;
  width: 100%;
}
.glass {
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
  border-radius: var(--radius);
  box-shadow: 0 8px 32px var(--glass-shadow);
  padding: calc(var(--spacing) * 2);
  margin-bottom: var(--spacing);
}
h1 {
  font-size: clamp(2rem, 5vw, 4rem);
  font-weight: 700;
  letter-spacing: -0.03em;
  color: var(--white, #FFFFFF);
  text-shadow: 0 2px 20px rgba(0,0,0,0.1);
  margin-bottom: 8px;
  line-height: 1.1;
}
h2 {
  font-size: clamp(1.25rem, 3vw, 2rem);
  font-weight: 600;
  letter-spacing: -0.02em;
  color: var(--white, #FFFFFF);
  margin-bottom: 12px;
}
h3 {
  font-size: 0.8125rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: rgba(255,255,255,0.6);
  margin-bottom: 16px;
}
p {
  font-size: 1rem;
  line-height: 1.6;
  color: rgba(255,255,255,0.8);
  margin-bottom: 16px;
}
.glass-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing);
  margin-bottom: var(--spacing);
}
.glass-card {
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
  border-radius: var(--radius);
  padding: calc(var(--spacing) * 1.5);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.glass-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.12);
}
.glass-card .icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: rgba(255,255,255,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin-bottom: 16px;
  backdrop-filter: blur(8px);
}
.glass-card h4 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #FFFFFF;
  margin-bottom: 8px;
}
.glass-card p {
  font-size: 0.9375rem;
  margin-bottom: 0;
}
.hero-glass {
  background: var(--glass-bg);
  backdrop-filter: blur(40px);
  -webkit-backdrop-filter: blur(40px);
  border: 1px solid var(--glass-border);
  border-radius: calc(var(--radius) * 2);
  padding: calc(var(--spacing) * 3);
  margin-bottom: var(--spacing);
  text-align: center;
}
.hero-glass p {
  max-width: 36em;
  margin: 0 auto 24px auto;
}
.badge {
  display: inline-block;
  background: rgba(255,255,255,0.12);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.20);
  border-radius: 100px;
  padding: 6px 16px;
  font-size: 0.75rem;
  color: rgba(255,255,255,0.8);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 16px;
}
.glow-button {
  display: inline-block;
  padding: 14px 40px;
  border-radius: 100px;
  background: var(--accent);
  color: #FFFFFF;
  font-weight: 600;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  box-shadow: 0 0 30px var(--accent-glow);
  transition: all 0.2s ease;
}
.glow-button:hover {
  transform: scale(1.02);
  box-shadow: 0 0 50px var(--accent-glow);
}
.metrics {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing);
  margin-bottom: var(--spacing);
}
.metric-item {
  background: var(--glass-bg);
  backdrop-filter: blur(16px);
  border-radius: var(--radius);
  padding: calc(var(--spacing) * 1.5);
  text-align: center;
  border: 1px solid rgba(255,255,255,0.12);
}
.metric-item .value {
  font-size: 2rem;
  font-weight: 700;
  color: #FFFFFF;
  line-height: 1.2;
}
.metric-item .label {
  font-size: 0.75rem;
  color: rgba(255,255,255,0.5);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
@media (max-width: 768px) {
  body { padding: var(--spacing); }
  .glass-grid { grid-template-columns: 1fr; }
  .metrics { grid-template-columns: 1fr 1fr; }
  .hero-glass { padding: var(--spacing); }
}
</style>
</head>
<body>
<div class=container>
<div class=hero-glass>
  <span class=badge>Glassmorphism · iOS 18 inspired</span>
  <h1>Layered Depth</h1>
  <p>Frosted surfaces with dynamic backdrop blur create visual hierarchy through translucency and ambient glow. Every layer breathes.</p>
  <button class=glow-button>Experience the Glass</button>
</div>
<div class=glass-grid>
  <div class=glass-card>
    <div class=icon>🌀</div>
    <h4>Backdrop Blur</h4>
    <p>Multiple blur layers (24px–40px) create genuine depth perception through translucency.</p>
  </div>
  <div class=glass-card>
    <div class=icon>✨</div>
    <h4>Ambient Glow</h4>
    <p>Soft box-shadows and accent glows produce a luminous halo effect around interactive elements.</p>
  </div>
  <div class=glass-card>
    <div class=icon>🔮</div>
    <h4>Frosted Borders</h4>
    <p>Semi-transparent borders at rgba(255,255,255,0.30) create the signature frosted-glass edge.</p>
  </div>
</div>
<div class=metrics>
  <div class=metric-item>
    <div class=value>24px</div>
    <div class=label>Base Blur</div>
  </div>
  <div class=metric-item>
    <div class=value>40px</div>
    <div class=label>Hero Blur</div>
  </div>
  <div class=metric-item>
    <div class=value>20px</div>
    <div class=label>Border Radius</div>
  </div>
  <div class=metric-item>
    <div class=value>0.18</div>
    <div class=label>Opacity</div>
  </div>
</div>
<div class=glass style=display:grid;grid-template-columns:1fr 1fr;gap:var(--spacing)>
  <div>
    <h3>Design Tokens</h3>
    <p style=font-size:0.875rem>Glass bg: rgba(255,255,255,0.18) · Border: rgba(255,255,255,0.30) · Blur: 24px/40px · Accent: #007AFF · Gradient: #667EEA → #764BA2 → #F093FB · Radius: 20px · Shadow: rgba(0,0,0,0.06)</p>
  </div>
  <div>
    <h3>When To Use</h3>
    <p style=font-size:0.875rem>Product showcases, music/entertainment apps, portfolio sites, modern SaaS landing pages, iOS/macOS interfaces. Avoid for text-heavy editorial, data dashboards, accessibility-critical contexts.</p>
  </div>
</div>
</div>
</body>
</html>
*** TEMPLATE 5: NEO-BRUTALIST ***
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Neo-Brutalist · Playful Heavy</title>
<style>
:root {
  --hot-pink: #FF2A6D;
  --cyber-lime: #05FFA1;
  --deep-purple: #7000FF;
  --sun-yellow: #FFE600;
  --black: #0D0D0D;
  --off-white: #F5F0EB;
  --border-w: 3px;
  --radius: 0px;
  --font-display: 'Helvetica Now', 'Helvetica Neue', sans-serif;
  --font-body: 'Helvetica Neue', 'Arial', sans-serif;
  --shadow-heavy: 8px 8px 0px var(--black);
  --shadow-color: 8px 8px 0px var(--hot-pink);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html { font-size: 16px; }
body {
  font-family: var(--font-body);
  background: var(--off-white);
  color: var(--black);
  line-height: 1.4;
  padding: 20px;
}
.container {
  max-width: 1100px;
  margin: 0 auto;
}
.section {
  margin-bottom: 40px;
}
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: var(--border-w) solid var(--black);
  padding: 20px 24px;
  background: var(--sun-yellow);
  box-shadow: var(--shadow-heavy);
  margin-bottom: 40px;
}
.logo {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: -0.03em;
}
nav {
  display: flex;
  gap: 24px;
}
nav a {
  font-size: 0.875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--black);
  text-decoration: none;
  border-bottom: 3px solid transparent;
  padding-bottom: 4px;
}
nav a:hover {
  border-bottom-color: var(--hot-pink);
}
h1 {
  font-family: var(--font-display);
  font-size: clamp(3rem, 8vw, 7rem);
  font-weight: 900;
  line-height: 0.85;
  letter-spacing: -0.04em;
  text-transform: uppercase;
  margin-bottom: 16px;
}
h2 {
  font-family: var(--font-display);
  font-size: clamp(1.75rem, 4vw, 3rem);
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: -0.02em;
  line-height: 1;
  margin-bottom: 16px;
}
h3 {
  font-family: var(--font-display);
  font-size: 0.8125rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 12px;
  opacity: 0.6;
}
p {
  font-size: 1rem;
  line-height: 1.5;
  margin-bottom: 16px;
  max-width: 42em;
}
.hero {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 24px;
  margin-bottom: 40px;
}
.hero-text {
  border: var(--border-w) solid var(--black);
  padding: 32px;
  background: var(--off-white);
  box-shadow: var(--shadow-heavy);
}
.hero-visual {
  border: var(--border-w) solid var(--black);
  padding: 32px;
  background: var(--cyber-lime);
  box-shadow: var(--shadow-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 5rem;
  font-weight: 900;
  color: var(--black);
}
.playground {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
.play-card {
  border: var(--border-w) solid var(--black);
  padding: 28px;
  transition: transform 0.15s ease;
  cursor: default;
}
.play-card:nth-child(1) { background: var(--hot-pink); box-shadow: var(--shadow-heavy); }
.play-card:nth-child(2) { background: var(--deep-purple); box-shadow: var(--shadow-color); color: var(--off-white); }
.play-card:nth-child(3) { background: var(--sun-yellow); box-shadow: var(--shadow-heavy); }
.play-card:hover {
  transform: translate(-4px, -4px);
  box-shadow: 12px 12px 0px var(--black);
}
.play-card h4 {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 800;
  text-transform: uppercase;
  margin-bottom: 12px;
}
.play-card p {
  font-size: 0.9375rem;
  margin-bottom: 0;
}
.badge-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}
.badge {
  display: inline-block;
  border: var(--border-w) solid var(--black);
  padding: 6px 18px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  background: var(--off-white);
}
.badge--pink { background: var(--hot-pink); color: var(--off-white); }
.badge--green { background: var(--cyber-lime); color: var(--black); }
.badge--purple { background: var(--deep-purple); color: var(--off-white); }
.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.two-col > div {
  border: var(--border-w) solid var(--black);
  padding: 24px;
}
footer {
  border-top: var(--border-w) solid var(--black);
  padding: 24px 0;
  margin-top: 40px;
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
@media (max-width: 768px) {
  .hero { grid-template-columns: 1fr; }
  .playground { grid-template-columns: 1fr; }
  .two-col { grid-template-columns: 1fr; }
  header { flex-direction: column; gap: 16px; }
  nav { flex-wrap: wrap; justify-content: center; }
}
</style>
</head>
<body>
<div class=container>
<header>
  <div class=logo>NEO BRUTAL</div>
  <nav>
    <a href>Work</a>
    <a href>Play</a>
    <a href>About</a>
  </nav>
</header>
<div class=hero>
  <div class=hero-text>
    <div class=badge-row>
      <span class=badge>Bold</span>
      <span class="badge badge--pink">Loud</span>
      <span class="badge badge--green">Playful</span>
    </div>
    <h1>Playful<br>Heavy</h1>
    <p>Neo-brutalism takes the raw honesty of 1950s brutalist architecture and injects it with contemporary energy: bright colour, oversized type, and geometric play.</p>
  </div>
  <div class=hero-visual>
    NEO
  </div>
</div>
<div class=playground>
  <div class=play-card>
    <h4 style=color:var(--off-white)>Hot Pink</h4>
    <p style=color:var(--off-white)>Primary accent. Demands attention. Pairs with black for maximum contrast.</p>
  </div>
  <div class=play-card>
    <h4>Cyber Lime</h4>
    <p>Secondary accent. Digital energy. Works as background or highlight.</p>
  </div>
  <div class=play-card>
    <h4>Sun Yellow</h4>
    <p>Tertiary accent. Optimism and warmth. Used for headers and banners.</p>
  </div>
</div>
<div class=two-col>
  <div>
    <h3>Design Tokens</h3>
    <p style=font-size:0.875rem>Type: Helvetica Now/Neue, 900 weight for display · Colors: hot pink #FF2A6D, lime #05FFA1, purple #7000FF, yellow #FFE600 · Shadows: 8px 8px 0px black · Borders: 3px solid · Radius: 0px · Transforms: translate(-4px,-4px) on hover</p>
  </div>
  <div>
    <h3>When To Use</h3>
    <p style=font-size:0.875rem>Creative agencies, music festivals, e-commerce hype drops, portfolio sites, gaming, youth brands. Avoid for corporate, legal, medical, elderly-focused, or luxury contexts.</p>
  </div>
</div>
<footer>
  <span>Neo-Brutalism · 2020s revival</span>
  <span>Play is not decoration · Play is structure</span>
</footer>
</div>
</body>
</html>
=============================================
AESTHETIC DECISION MATRIX
=============================================
use-case: Editorial / Long-form Content
swiss: 9
minimal: 8
brutalist: 4
glass: 3
neo-brutalist: 2
recommendation: Swiss (International Typographic Style) — grid systems, asymmetric balance, disciplined typography enhance readability and visual hierarchy at scale.
use-case: Corporate / Enterprise SaaS
swiss: 7
minimal: 9
brutalist: 3
glass: 8
neo-brutalist: 2
recommendation: Minimal (Dieter Rams) — restrained color, maximal whitespace, functional precision communicates trust and clarity.
use-case: Creative Agency / Portfolio
swiss: 8
minimal: 5
brutalist: 7
glass: 6
neo-brutalist: 9
recommendation: Neo-Brutalist — bright accent colors, oversized typography, playful geometry signals creative confidence and contemporary taste.
use-case: Music / Entertainment / Festival
swiss: 4
minimal: 2
brutalist: 6
glass: 7
neo-brutalist: 9
recommendation: Neo-Brutalist — high-energy palette, bold forms, playful interactions match the emotional register of entertainment spaces.
use-case: Architecture / Art Gallery
swiss: 7
minimal: 6
brutalist: 9
glass: 5
neo-brutalist: 6
recommendation: Brutalist — raw materials, exposed grids, monochrome palette, heavy borders reflect architectural honesty and structural integrity.
use-case: Mobile App / iOS Interface
swiss: 5
minimal: 7
brutalist: 1
glass: 9
neo-brutalist: 3
recommendation: Glass (Apple-inspired Glassmorphism) — backdrop blur, layered depth, ambient glow align with native iOS design language and Human Interface Guidelines.
use-case: Developer Docs / API Reference
swiss: 8
minimal: 6
brutalist: 7
glass: 3
neo-brutalist: 4
recommendation: Swiss (International Typographic Style) — grid precision, clear hierarchy, sans-serif clarity. Brutalist is a secondary option for tooling that wants to convey rawness.
use-case: Luxury / Premium Brand
swiss: 6
minimal: 9
brutalist: 2
glass: 8
neo-brutalist: 1
recommendation: Minimal (Dieter Rams) — restraint signals quality. Glass works for premium digital products where luminosity and depth convey sophistication.
use-case: E-commerce / Product Showcase
swiss: 7
minimal: 8
brutalist: 3
glass: 6
neo-brutalist: 5
recommendation: Minimal — functional, product-first layout with generous whitespace and unobtrusive framing. Swiss for editorial-heavy product catalogues.
use-case: Youth / Streetwear / Hype Culture
swiss: 3
minimal: 2
brutalist: 5
glass: 4
neo-brutalist: 9
recommendation: Neo-Brutalist — oversized type, bold color blocks, heavy shadows, playful animation potential matches the visual language of street culture and hype drops.
=============================================
COMPOSITE COLOR PALETTES
=============================================
swiss:
  primary: '#E63946' (signal red)
  secondary: '#1D3557' (navy)
  accent: '#F1FAEE' (off-white)
  neutral: '#8D99AE' (gray)
  base: '#1A1A1A' (near-black)
  surface: '#F5F5F5' (white)
minimal:
  primary: '#2B2B2B' (charcoal)
  secondary: '#888888' (warm gray)
  accent: '#222222' (text)
  neutral: '#E0E0E0' (border)
  base: '#222222' (text)
  surface: '#FAFAF8' (off-white)
brutalist:
  primary: '#0A0A0A' (black)
  secondary: '#CC0000' (accent red)
  accent: '#F0F0F0' (white)
  neutral: '#555555' (mid gray)
  base: '#0A0A0A' (black)
  surface: '#F0F0F0' (white)
glass:
  primary: '#007AFF' (apple blue)
  secondary: '#764BA2' (gradient purple)
  accent: 'rgba(255,255,255,0.18)' (glass)
  neutral: 'rgba(255,255,255,0.30)' (border)
  base: '#1C1C1E' (text)
  surface: 'gradient(#667EEA, #764BA2, #F093FB)'
neo-brutalist:
  primary: '#FF2A6D' (hot pink)
  secondary: '#05FFA1' (cyber lime)
  accent: '#7000FF' (deep purple)
  neutral: '#FFE600' (sun yellow)
  base: '#0D0D0D' (black)
  surface: '#F5F0EB' (off-white)