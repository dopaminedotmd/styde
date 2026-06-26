Typography system output for a modern web project:
TYPE SCALE (modular scale 1.25 major third):
--text-xs: 0.75rem (12px)
--text-sm: 0.875rem (14px)
--text-base: 1rem (16px)
--text-lg: 1.125rem (18px)
--text-xl: 1.25rem (20px)
--text-2xl: 1.5rem (24px)
--text-3xl: 1.875rem (30px)
--text-4xl: 2.25rem (36px)
--text-5xl: 3rem (48px)
--text-6xl: 3.75rem (60px)
--text-7xl: 4.5rem (72px)
FONT PAIRING:
Headings: Inter Tight (variable, wght 600-800)
Body: Inter (variable, wght 300-500)
Mono: JetBrains Mono (variable, wght 400-700)
Rationale: Inter Tight has tighter letter-spacing for display use. Both Inter families share x-height and skeleton for harmonious pairing. One foundry, consistent metrics.
VARIABLE FONT AXES:
Inter: wght 300-900, opsz 8-36 (optical sizing auto-adjusted)
Inter Tight: wght 500-800
JetBrains Mono: wght 300-700, ital 0-1
CSS: font-weight uses numeric 100-900 values directly. No separate bold files.
Performance: 3 variable font files replace 18 static weights. Pageload reduction ~240KB to ~85KB woff2.
VERTICAL RHYTHM:
Baseline grid: 8px
Line heights computed to snap to 8px increments:
--leading-xs: 1rem (16px, 2 grid units)
--leading-sm: 1.25rem (20px, crosses grid — allowed for small text)
--leading-base: 1.5rem (24px, 3 grid units)
--leading-lg: 1.75rem (28px, 3.5 — used for display only)
--leading-xl: 2rem (32px, 4 grid units)
Margins and padding on block elements always snap to multiples of 8px.
p + p margin-top: 1rem (16px, 2 grid units).
READABILITY:
Line length: 65-75 characters per line. Container max-width 680px for prose, 720px for articles.
Line height body: 1.5 (24px on 16px base) — optimal for Latin scripts.
Line height headings: 1.15-1.25 — tighter for display weight.
Contrast: body text #1a1a1a on #ffffff (ratio 16.2:1). Large text #2a2a2a (10.8:1). Small supplementary text #5a5a5a (6.5:1, AAA compliant at 7:1 threshold for small).
Hyphens: auto on body text for justified gaps. No widows: single-word final lines prevented via text-wrap: pretty on headings.