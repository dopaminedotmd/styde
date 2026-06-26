--
# Typographic Rhythm Engine — CSS System
--
## Modular Scale — 6 Ratios with CSS clamp()
Scale base: 16px    Ratio options:
- Minor Second: 1.067   (tight, dense UI)
- Major Second: 1.125   (compact, technical)
- Minor Third:  1.200   (standard, versatile)
- Major Third:  1.250   (editorial, spacious)
- Perfect Fourth: 1.333 (dramatic, luxury)
- Golden Ratio:  1.618  (expressive, creative)
Selected: Perfect Fourth (1.333) for general use, Major Third (1.250) for body system
Step   Ratio     Min(320px)     Mid(768px)     Max(1440px)     CSS clamp()
-caption  0.563   9px            10px           11px            clamp(0.563rem, 0.523rem + 0.237vw, 0.688rem)
-caption2 0.667   11px           12px           14px            clamp(0.688rem, 0.638rem + 0.296vw, 0.875rem)
body      1.000   16px           17px           18px            clamp(1.000rem, 0.931rem + 0.413vw, 1.125rem)
h6        1.125   18px           20px           22px            clamp(1.125rem, 1.043rem + 0.493vw, 1.375rem)
h5        1.250   20px           23px           27px            clamp(1.250rem, 1.148rem + 0.612vw, 1.688rem)
h4        1.333   21px           25px           30px            clamp(1.313rem, 1.189rem + 0.739vw, 1.875rem)
h3        1.500   24px           29px           36px            clamp(1.500rem, 1.338rem + 0.966vw, 2.250rem)
h2        1.777   28px           36px           48px            clamp(1.750rem, 1.503rem + 1.480vw, 3.000rem)
h1        2.369   28px           44px           64px            clamp(1.750rem, 1.324rem + 2.549vw, 4.000rem)
display   3.157   32px           56px           96px            clamp(2.000rem, 1.221rem + 4.671vw, 6.000rem)
Formula used:
  size = base * ratio^step
  clamp(min, preferred, max)
  preferred = min + (max - min) * ((100vw - 320px) / (1440px - 320px))
  stored as: clamp([min]rem, [slope]rem + [vw]vw, [max]rem)
-- Variable Font Axis Integration
axis   property        tag  range     usage
wght   font-weight     wght 100-900  heading: 700-900, body: 350-450
wdth   font-stretch    wdth 75-125   display: 100-110 condensed, editorial: 95-105
slnt   font-style      slnt 0-12     captions: 0, quotes: 3-7 slant
opsz   font-optical-sizing opsz 6-144 UI: 10-14, body: 14-18, display: 72-144
ital   font-style      ital 0-1      emphasis: 1, body: 0
CSS variable font config:
@font-face {
  font-family: 'Inter VF';
  src: url('Inter-Variable.woff2') format('woff2') tech('variations');
  font-weight: 100 900;
  font-stretch: 75% 125%;
  font-optical-sizing: auto;
}
@font-face {
  font-family: 'Literata VF';
  src: url('Literata-Variable.woff2') format('woff2') tech('variations');
  font-weight: 300 900;
  font-optical-sizing: auto;
  font-style: oblique 0deg 12deg;
}
@font-face {
  font-family: 'Geist Mono VF';
  src: url('GeistMono-Variable.woff2') format('woff2') tech('variations');
  font-weight: 100 900;
}
Usage pattern per context:
display-text {
  font-family: 'Inter VF', system-ui;
  font-variation-settings: 'wght' 800, 'wdth' 100, 'opsz' 72;
}
body-text {
  font-family: 'Literata VF', Georgia, serif;
  font-variation-settings: 'wght' 380, 'opsz' 16;
}
code-text {
  font-family: 'Geist Mono VF', 'Cascadia Code', monospace;
  font-variation-settings: 'wght' 450;
}
-- Baseline Grid Rhythm
Grid unit: 4px     Base leading: 24px (1.5 ratio at 16px body)
CSS custom properties for rhythm:
:root {
  --rhythm-base: 1.5rem;            /* 24px baseline grid unit */
  --rhythm-micro: 0.25rem;          /* 4px — smallest adjustment */
  --rhythm-tight: 1.25rem;          /* 20px */
  --rhythm-comfort: 1.75rem;        /* 28px */
  --rhythm-double: 3rem;            /* 48px */
  --rhythm-section: 4.5rem;         /* 72px — 3 grid steps */
  /* Line heights aligned to 4px grid */
  --lh-display: 1.1;     /* 72@96px -> 1.1 = 105.6, round to 108 = 3 units */
  --lh-h1:      1.15;    /* 64@64px -> 73.6, round to 72 = 18 units */
  --lh-h2:      1.2;     /* 48@48px -> 57.6, round to 60 = 15 units */
  --lh-h3:      1.25;    /* 36@36px -> 45, round to 48 = 12 units */
  --lh-h4:      1.333;   /* 30@30px -> 40, round to 40 = 10 units */
  --lh-h5:      1.4;     /* 27@27px -> 37.8, round to 40 = 10 units */
  --lh-h6:      1.5;     /* 22@22px -> 33, round to 36 = 9 units */
  --lh-body:    1.6;     /* 18@18px -> 28.8, round to 28 = 7 units */
  --lh-caption: 1.5;     /* 14@14px -> 21, round to 20 = 5 units */
  --lh-label:   1.3;     /* 12@12px -> 15.6, round to 16 = 4 units */
}
Computed line-heights (actual pixel values snapped to 4px grid):
display:  96px/108px  (1.125)
h1:       64px/72px   (1.125)
h2:       48px/60px   (1.25)
h3:       36px/48px   (1.333)
h4:       30px/40px   (1.333)
h5:       27px/40px   (1.481)
h6:       22px/36px   (1.636)
body:     18px/28px   (1.555)
caption:  14px/20px   (1.428)
label:    12px/16px   (1.333)
Vertical rhythm spacing tokens:
--space-stack:    var(--rhythm-base);          /* between siblings */
--space-inset:    calc(var(--rhythm-base) / 2); /* padding inside blocks */
--space-section:  var(--rhythm-section);        /* between major sections */
--space-group:    var(--rhythm-double);         /* between component groups */
--space-paragraph: var(--rhythm-base);          /* between paragraphs */
p + p, li + li, .text-block > * + * {
  margin-block-start: var(--space-stack);
}
h1, h2, h3, h4, h5, h6 {
  margin-block-end: calc(var(--rhythm-base) / 2);
}
-- Fluid Measure (Optimal Line Length)
Measure: 45-75 characters per line
Applies to: body text, article text, long-form reading
Max widths per breakpoint for optimal measure:
:root {
  --measure-xs: 25ch;   /* mobile — tight, 30-45 chars */
  --measure-sm: 35ch;   /* small tablet */
  --measure-md: 45ch;   /* tablet — ideal narrow */
  --measure-lg: 60ch;   /* desktop — sweet spot */
  --measure-xl: 70ch;   /* wide desktop — max comfortable */
  --measure-max: 75ch;  /* ultra-wide — absolute ceiling */
}
@media (width >= 640px) { --measure-current: var(--measure-md); }
@media (width >= 1024px) { --measure-current: var(--measure-lg); }
@media (width >= 1440px) { --measure-current: var(--measure-xl); }
.reading-block {
  max-inline-size: var(--measure-current, var(--measure-lg));
  margin-inline: auto;
}
.measure-loose { max-inline-size: var(--measure-xl); }
.measure-tight { max-inline-size: var(--measure-md); }
.measure-none { max-inline-size: none; }
-- Type Hierarchy — Contrast Ratio Analysis
context    font-family    weight  size    line-h   contrast*  letter-spacing
display    Inter VF      800     96px    108px    1:16.0    -0.03em
h1         Inter VF      700     64px    72px     1:12.0    -0.025em
h2         Inter VF      650     48px    60px     1:8.0     -0.02em
h3         Inter VF      600     36px    48px     1:5.33    -0.015em
h4         Literata VF   650     30px    40px     1:4.0     -0.005em
h5         Literata VF   600     27px    40px     1:3.0     0em
h6         Literata VF   550     22px    36px     1:2.0     0.005em
body       Literata VF   380     18px    28px     1:1.0     0.01em
small      Literata VF   370     15px    24px     1:0.83    0.015em
caption    Inter VF      400     14px    20px     1:0.77    0.02em
label      Inter VF      500     12px    16px     1:0.66    0.05em
code       Geist Mono VF 400     15px    24px     1:0.83    0em
quote      Literata VF   350     22px    36px     1:1.22    0.01em
*contrast = ratio of this size to body size (18px)
Color contrast for readability:
:root {
  --text-display: hsl(0, 0%, 8%);
  --text-heading: hsl(0, 0%, 12%);
  --text-body: hsl(0, 0%, 18%);
  --text-muted: hsl(0, 0%, 45%);
  --text-caption: hsl(0, 0%, 50%);
  --text-label: hsl(0, 0%, 40%);
  --text-link: hsl(220, 80%, 45%);
  --text-inverse: hsl(0, 0%, 95%);
}
-- Font Pairings — 20+ Contexts
editorial:
  heading: Source Serif 4 (700) / Literata VF (650)
  body: Source Serif 4 (400) / Literata VF (380)
  accent: Inter (500)
  reasoning: serif body signals authority and readability, sans-serif accent for structure
tech:
  heading: Inter (700) / SF Pro Display (700)
  body: Inter (400) / SF Pro Text (400)
  mono: JetBrains Mono (450) / Geist Mono VF (450)
  reasoning: clean sans for UI, mono for code, tight spacing for density
luxury:
  heading: Playfair Display (700) / Cormorant Garamond (600)
  body: Lora (400) / EB Garamond (400)
  accent: Montserrat (300, uppercase)
  reasoning: high-contrast serifs, generous tracking, light weights for elegance
creative:
  heading: Fraunces VF (800, soft) / Bangers (regular)
  body: DM Sans (400) / Archivo (400)
  accent: Space Grotesk (500)
  reasoning: expressive variable font, playful display, contemporary sans
docs:
  heading: IBM Plex Sans (600) / Work Sans (600)
  body: IBM Plex Serif (400) / Atkinson Hyperlegible (400)
  mono: IBM Plex Mono (450) / Fira Code (450)
  reasoning: maximum legibility, clear hierarchy, accessible at all sizes
news:
  heading: Publico Text (700) / Benton Sans (800)
  body: Publico Text (400) / Tiempos Text (400)
  accent: Benton Sans (600)
  reasoning: newspaper-proven pairings, high readability, neutral tone
ecommerce:
  heading: DIN Pro (700) / Montserrat (700)
  body: Open Sans (400) / Lato (400)
  accent: DIN Pro (500 condensed)
  reasoning: bold, scannable headings, clean body, narrow accents for pricing
finance:
  heading: Avenir Next (700) / Proxima Nova (700)
  body: Source Sans 3 (400) / Graphik (400)
  mono: Roboto Mono (450) / DM Mono (450)
  reasoning: serious, trustworthy, numbers legible in mono
health:
  heading: Lato (700) / Nunito (700)
  body: Merriweather (400) / Literata (400)
  accent: Lato (500)
  reasoning: warm rounded sans for calm, serif for authoritative health information
education:
  heading: Lexend (700) / Fredoka (600)
  body: Atkinson Hyperlegible (400) / Lexend (400)
  accent: Fredoka (500)
  reasoning: designed for dyslexia and learning accessibility, clear letterforms
gaming:
  heading: Bebas Neue (700) / Rajdhani (700)
  body: Exo 2 (400) / Orbitron (400)
  accent: Exo 2 (600)
  reasoning: futuristic geometry, condensed display, energetic rhythm
food/cooking:
  heading: Abril Fatface (400) / DM Serif Display (400)
  body: Source Serif 4 (400) / Literata (380)
  accent: Barlow (500)
  reasoning: warm, appetizing serif display, approachable body
fashion:
  heading: Didot (700) / Bodoni Moda (700)
  body: Montserrat (300) / Jost (300)
  accent: Didot (400 italic)
  reasoning: high-contrast didone, thin weights for elegance, editorial spacing
travel:
  heading: Barlow Condensed (700) / Oswald (600)
  body: Barlow (400) / Nunito (400)
  accent: Barlow (500 italic)
  reasoning: condensed for hero imagery, rounded body for friendly tone
legal:
  heading: Charter (700) / STFangSong (700)
  body: Source Serif 4 (400) / Charter (400)
  mono: IBM Plex Mono (450)
  reasoning: traditional serif for authority, generous measure, numbered lists
music:
  heading: Bebas Neue (700) / Montserrat Alternates (700)
  body: Inter (400) / Archivo (400)
  accent: Space Grotesk (500)
  reasoning: bold for album titles, clean for track lists, modern feel
podcast/blog:
  heading: Fraunces VF (700, soft) / Outfit (700)
  body: DM Sans (400) / Sora (400)
  accent: Fraunces VF (500 italic)
  reasoning: warm variable face for personality, clean sans for readability
scientific:
  heading: IBM Plex Sans (600) / Roboto (600)
  body: Noto Serif (400) / Source Serif 4 (400)
  mono: JetBrains Mono (450)
  reasoning: neutral, precise, multi-script support, dense data display
minimalist:
  heading: Helvetica Neue (300) / Inter (300)
  body: Helvetica Neue (300) / Inter (300)
  accent: Helvetica Neue (500)
  reasoning: single-family system, extreme weight contrast, airy spacing
brutalist:
  heading: Antonio (700) / Syne Mono (700)
  body: Space Grotesk (400) / DM Sans (400)
  accent: Mono Lisa (700)
  reasoning: heavy, forceful, monospace-inspired, raw aesthetic
-- Example Typesetting
[Display / Hero]
<h1 class="display-hero">The Quick Brown Fox Jumps Over the Lazy Dog</h1>
[Article Body]
<article class="reading-block">
  <p>A typographic system is the foundation of visual communication. It establishes rhythm, hierarchy, and readability across every surface where text appears. The baseline grid ensures that regardless of font size or weight, all text aligns to an invisible scaffold of horizontal lines. This creates visual order even in dense layouts.</p>
  <p>Variable font technology deepens this system by exposing design axes that traditional fonts lock away. Weight, width, slant, and optical size become dynamic properties that shift with context. A headline can compress at narrow viewports, then expand to fill wide screens. Body text can adjust optical size to remain crisp at any scale.</p>
  <blockquote>Typography is the craft of endowing human language with a durable visual form. It is a craft that requires both technical precision and artistic judgment.</blockquote>
  <p>The modular scale provides mathematical consistency between type sizes. Each step relates to every other step by a constant ratio, ensuring that h1 through caption form a coherent family rather than arbitrary sizes chosen by eye. Combined with fluid clamp() values, this scale survives any viewport without breaking.</p>
</article>
[Card Component]
<article class="card">
  <span class="label">CATEGORY</span>
  <h3 class="card-title">Modular Scale Generation</h3>
  <p class="card-body">Generate type scales with 6 ratios using Pure Harmonic Intervals or custom steps. Output as CSS clamp() fluid values for responsive typography.</p>
  <span class="caption">Updated 4 hours ago</span>
</article>
[Form / UI]
<fieldset>
  <label class="label">Email Address</label>
  <input type="email" class="input" placeholder="user@example.com" />
  <span class="caption">We'll never share your email with third parties</span>
</fieldset>
[Code Block]
<pre><code class="code-block">:root {
  --scale-ratio: 1.333;
  --base-size: 1rem;
}
h1 {
  font-size: clamp(1.75rem, 1.324rem + 2.549vw, 4rem);
  line-height: var(--lh-h1);
  font-variation-settings: 'wght' 700, 'opsz' 48;
}</code></pre>
-- CSS Typography System — Complete
:root {
  /* — Scale — */
  --scale-ratio: 1.333;
  --fs-caption: clamp(0.563rem, 0.523rem + 0.237vw, 0.688rem);
  --fs-caption2: clamp(0.688rem, 0.638rem + 0.296vw, 0.875rem);
  --fs-body: clamp(1rem, 0.931rem + 0.413vw, 1.125rem);
  --fs-h6: clamp(1.125rem, 1.043rem + 0.493vw, 1.375rem);
  --fs-h5: clamp(1.25rem, 1.148rem + 0.612vw, 1.688rem);
  --fs-h4: clamp(1.313rem, 1.189rem + 0.739vw, 1.875rem);
  --fs-h3: clamp(1.5rem, 1.338rem + 0.966vw, 2.25rem);
  --fs-h2: clamp(1.75rem, 1.503rem + 1.48vw, 3rem);
  --fs-h1: clamp(1.75rem, 1.324rem + 2.549vw, 4rem);
  --fs-display: clamp(2rem, 1.221rem + 4.671vw, 6rem);
  /* — Line Height — */
  --lh-display: 1.125;
  --lh-h1: 1.125;
  --lh-h2: 1.25;
  --lh-h3: 1.333;
  --lh-h4: 1.333;
  --lh-h5: 1.481;
  --lh-h6: 1.636;
  --lh-body: 1.555;
  --lh-caption: 1.428;
  --lh-label: 1.333;
  --lh-code: 1.6;
  --lh-quote: 1.636;
  /* — Rhythm — */
  --rhythm-base: 1.5rem;
  --rhythm-micro: 0.25rem;
  --rhythm-tight: 1.25rem;
  --rhythm-comfort: 1.75rem;
  --rhythm-double: 3rem;
  --rhythm-section: 4.5rem;
  --space-stack: var(--rhythm-base);
  --space-inset: calc(var(--rhythm-base) / 2);
  --space-section: var(--rhythm-section);
  --space-group: var(--rhythm-double);
  --space-paragraph: var(--rhythm-base);
  /* — Measure — */
  --measure-xs: 25ch;
  --measure-sm: 35ch;
  --measure-md: 45ch;
  --measure-lg: 60ch;
  --measure-xl: 70ch;
  --measure-max: 75ch;
  /* — Color — */
  --text-display: hsl(0, 0%, 8%);
  --text-heading: hsl(0, 0%, 12%);
  --text-body: hsl(0, 0%, 18%);
  --text-muted: hsl(0, 0%, 45%);
  --text-caption: hsl(0, 0%, 50%);
  --text-label: hsl(0, 0%, 40%);
  --text-link: hsl(220, 80%, 45%);
  --text-inverse: hsl(0, 0%, 95%);
}
@media (width >= 640px) { :root { --measure-current: var(--measure-md); } }
@media (width >= 1024px) { :root { --measure-current: var(--measure-lg); } }
@media (width >= 1440px) { :root { --measure-current: var(--measure-xl); } }
h1, h2, h3, h4, h5, h6 { font-weight: unset; }
.display { font-size: var(--fs-display); line-height: var(--lh-display); font-weight: 800; letter-spacing: -0.03em; font-variation-settings: 'wght' 800, 'wdth' 100, 'opsz' 72; color: var(--text-display); }
h1 { font-size: var(--fs-h1); line-height: var(--lh-h1); font-weight: 700; letter-spacing: -0.025em; font-variation-settings: 'wght' 700, 'opsz' 48; color: var(--text-heading); }
h2 { font-size: var(--fs-h2); line-height: var(--lh-h2); font-weight: 650; letter-spacing: -0.02em; font-variation-settings: 'wght' 650, 'opsz' 36; color: var(--text-heading); }
h3 { font-size: var(--fs-h3); line-height: var(--lh-h3); font-weight: 600; letter-spacing: -0.015em; font-variation-settings: 'wght' 600, 'opsz' 24; color: var(--text-heading); }
h4 { font-size: var(--fs-h4); line-height: var(--lh-h4); font-weight: 650; letter-spacing: -0.005em; font-variation-settings: 'wght' 650, 'opsz' 18; }
h5 { font-size: var(--fs-h5); line-height: var(--lh-h5); font-weight: 600; font-variation-settings: 'wght' 600; }
h6 { font-size: var(--fs-h6); line-height: var(--lh-h6); font-weight: 550; letter-spacing: 0.005em; font-variation-settings: 'wght' 550; }
body, p { font-size: var(--fs-body); line-height: var(--lh-body); font-weight: 380; font-variation-settings: 'wght' 380, 'opsz' 16; color: var(--text-body); }
small, .small { font-size: 0.833em; line-height: var(--lh-body); font-variation-settings: 'opsz' 12; }
.caption { font-size: var(--fs-caption2); line-height: var(--lh-caption); letter-spacing: 0.02em; color: var(--text-caption); font-variation-settings: 'wght' 400; }
.label { font-size: var(--fs-caption); line-height: var(--lh-label); letter-spacing: 0.05em; text-transform: uppercase; font-weight: 500; color: var(--text-label); font-variation-settings: 'wght' 500; }
code, pre { font-size: 0.833em; line-height: var(--lh-code); font-family: 'Geist Mono VF', 'JetBrains Mono', monospace; font-variation-settings: 'wght' 450; }
blockquote { font-size: 1.222em; line-height: var(--lh-quote); font-style: oblique 5deg; font-variation-settings: 'wght' 350, 'slnt' 5; color: var(--text-muted); padding-inline-start: 1.5rem; border-inline-start: 3px solid; }
.reading-block { max-inline-size: var(--measure-current, var(--measure-lg)); margin-inline: auto; }
p + p, li + li, .text-block > * + * { margin-block-start: var(--space-stack); }
h1, h2, h3, h4, h5, h6 { margin-block-end: var(--space-inset); }
h1 { margin-block-start: var(--rhythm-double); }
h2 { margin-block-start: var(--rhythm-double); }
h3 { margin-block-start: var(--rhythm-comfort); }
:is(h1, h2, h3, h4):first-child { margin-block-start: 0; }
section + section { margin-block-start: var(--space-section); }
a { color: var(--text-link); text-decoration-color: currentColor; text-underline-offset: 0.15em; }
a:hover { text-decoration-thickness: 2px; }