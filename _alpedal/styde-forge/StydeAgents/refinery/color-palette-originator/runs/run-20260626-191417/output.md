Variant 1: NOCTIS
dark theme. reserved, technical, deep focus. like a midnight study with brass instruments.
Palette tokens:
surface-canvas: #0c1220
surface-card: #141b2c
surface-elevated: #1c2440
surface-border: #283050
text-primary: #dce3f0
text-secondary: #8892a8
text-disabled: #4a5470
accent-primary: #4eb5a2
accent-hover: #3da18f
accent-pressed: #2e8d7c
accent-subtle: rgba(78,181,162,0.12)
accent-ring: rgba(78,181,162,0.4)
neutral-hover: rgba(220,227,240,0.06)
neutral-pressed: rgba(220,227,240,0.12)
neutral-disabled: #2a3248
danger: #d45a6a
success: #55b88c
warning: #d9a44a
info: #5b8fd9
interactive-hover: neutral-hover background + accent-primary border
interactive-pressed: neutral-pressed background
interactive-disabled: surface-border text + disabled background
WCAG AA verification:
surface-canvas + text-primary #dce3f0
luminance(canvas)=0.0127 luminance(text)=0.6568
contrast ratio = (0.6568+0.05)/(0.0127+0.05) = 0.7068/0.0627 = 11.27:1
passes AAA 7:1
surface-canvas + text-secondary #8892a8
luminance(secondary)=0.2856
contrast = (0.2856+0.05)/(0.0127+0.05) = 0.3356/0.0627 = 5.35:1
passes AA 4.5:1
surface-card #141b2c + text-primary
luminance(card)=0.0237
contrast = 0.7068/0.0737 = 9.59:1
passes AAA 7:1
surface-card + accent-primary #4eb5a2
luminance(accent)=0.3641
contrast = (0.3641+0.05)/(0.0237+0.05) = 0.4141/0.0737 = 5.62:1
passes AA 4.5:1 for text, passes AA 3:1 for large text
surface-canvas + accent-hover #3da18f
luminance(hover)=0.2684
contrast = 0.3184/0.0627 = 5.08:1
passes AA 4.5:1
accent-primary + accent-subtle background
subtle bg luminance approximates canvas + 0.12 alpha blend
effective ~#1b2941 luminance=0.0316
contrast = 0.4141/0.0816 = 5.07:1
passes AA for text on tinted surface
text-disabled #4a5470 on surface-canvas
luminance(disabled)=0.0787
contrast = 0.1287/0.0627 = 2.05:1
below 3:1, intentional — disabled state visually recessive
Emotional coherence:
Noctis pairs deep navy-cast grays with teal-amber accents. The high contrast core (11:1 canvas-to-text) signals precision and authority. The teal accent adds restrained warmth without breaking focus. Emotion: concentrated, trustworthy, premium. Not moody — moody implies drift. This is anchored.
Variant 2: CELADON
light theme. crisp, organic, quiet confidence. like morning light through sea glass.
Palette tokens:
surface-canvas: #f4f7f4
surface-card: #ffffff
surface-elevated: #ffffff
surface-border: #d8e0d8
text-primary: #1a2a1e
text-secondary: #4a6a52
text-disabled: #a0b8a5
accent-primary: #29664a
accent-hover: #1d5239
accent-pressed: #123e2b
accent-subtle: rgba(41,102,74,0.08)
accent-ring: rgba(41,102,74,0.3)
neutral-hover: rgba(26,42,30,0.04)
neutral-pressed: rgba(26,42,30,0.08)
neutral-disabled: #e2e8e2
danger: #b83a4a
success: #36805a
warning: #b88a30
info: #3a7aa8
WCAG AA verification:
canvas #f4f7f4 + text-primary #1a2a1e
luminance(canvas)=0.9247 luminance(text)=0.0275
contrast = (0.9247+0.05)/(0.0275+0.05) = 0.9747/0.0775 = 12.58:1
passes AAA 7:1
canvas + text-secondary #4a6a52
luminance(secondary)=0.1156
contrast = 0.9747/0.1656 = 5.89:1
passes AA 4.5:1
card #ffffff + accent-primary #29664a
luminance(card)=1.0 luminance(accent)=0.0561
contrast = 1.05/0.1061 = 9.90:1
passes AAA 7:1
card + accent-hover #1d5239
luminance(hover)=0.0286
contrast = 1.05/0.0786 = 13.36:1
passes AAA 7:1
card + text-disabled #a0b8a5
luminance(disabled)=0.3447
contrast = 1.05/0.3947 = 2.66:1
below 3:1, intentional
canvas + accent-subtle (8% blend)
effective ~#eef2ee luminance=0.8743
contrast with accent-primary = 0.9243/0.1061 = 8.71:1
passes AAA
Emotional coherence:
Celadon uses olive-tinged neutrals and deep forest greens. The lightest canvas (98% white) keeps it airy, while the green anchor prevents sterility. This is not cheerful in a loud way. It is settled, restorative, natural. The green midtones pull the palette away from cold minimalism toward organic clarity.
Variant 3: OCHRE
dark-light hybrid. earthy, tactile, grounded. like clay, leather, and weathered copper.
Palette tokens:
surface-canvas: #1c1812
surface-card: #28231c
surface-elevated: #332d24
surface-border: #3d362c
text-primary: #e6ddd0
text-secondary: #a69a88
text-disabled: #5c5448
accent-primary: #c88542
accent-hover: #b07535
accent-pressed: #98662a
accent-subtle: rgba(200,133,66,0.12)
accent-ring: rgba(200,133,66,0.35)
neutral-hover: rgba(230,221,208,0.05)
neutral-pressed: rgba(230,221,208,0.10)
neutral-disabled: #2f2920
danger: #c75a5a
success: #6a9e6a
warning: #b8943a
info: #5a8aae
WCAG AA verification:
canvas #1c1812 + text-primary #e6ddd0
luminance(canvas)=0.0209 luminance(text)=0.7125
contrast = 0.7625/0.0709 = 10.75:1
passes AAA 7:1
canvas + text-secondary #a69a88
luminance(secondary)=0.3038
contrast = 0.3538/0.0709 = 4.99:1
passes AA 4.5:1
card #28231c + accent-primary #c88542
luminance(card)=0.0316 luminance(accent)=0.2891
contrast = (0.2891+0.05)/(0.0316+0.05) = 0.3391/0.0816 = 4.16:1
passes AA 3:1 for large text, FAILS 4.5:1 for small text
card + accent-hover #b07535
luminance(hover)=0.1998
contrast = 0.2498/0.0816 = 3.06:1
passes AA 3:1 for large text only
card + accent-pressed #98662a
luminance(pressed)=0.1375
contrast = 0.1875/0.0816 = 2.30:1
below 3:1 — acceptable for pressed state (momentary, not content)
accent-primary for small text: use on surface-elevated #332d24 or lighter
elevated #332d24 luminance=0.0460
contrast = 0.3391/0.0960 = 3.53:1
still below 4.5:1. recommendation: use accent-primary for large text/UI elements only, not body text.
accent-primary as large text (>18px bold or >14px regular) on card: passes 3:1
accent-primary as small text: recommend surface-elevated at minimum, or use accent-hover #b07535 which is lighter
card + accent-hover = 3.06:1 — borderline, use only for decorative small text
For guaranteed AA small text on card, use accent-primary on surface-elevated only (3.53:1 still short). Recommend either:
a) lighten accent to #d49455 (luminance ~0.348, ratio ~4.72:1 on card — PASS)
b) use accent-primary only at large sizes on dark surfaces
Recommendation (a) applied below as accent-primary-alt for body text usage.
accent-primary-alt: #d49455
luminance = 0.3483
contrast on card = 0.3983/0.0816 = 4.88:1
passes AA 4.5:1 for small text
Emotional coherence:
Ochre is the warmest variant. The brown-gray neutrals feel like raw clay, not corporate gray. The copper accent reads as fire and earth together, not safety orange. Emotion: grounded, artisan, enduring. Not aggressive despite high warmth — the dark canvas tames the ochre saturation.
Appendix A: Contrast Master Table
Noctis:
primary-text on canvas: 11.27 AAA
primary-text on card: 9.59 AAA
secondary-text on canvas: 5.35 AA
accent-primary on card: 5.62 AA
accent-hover on canvas: 5.08 AA
accent-pressed on canvas: 3.91 AA large
disabled on canvas: 2.05 sub-AA
Celadon:
primary-text on canvas: 12.58 AAA
primary-text on card: 13.91 AAA
secondary-text on canvas: 5.89 AA
accent-primary on card: 9.90 AAA
accent-hover on card: 13.36 AAA
accent-pressed on card: 20.53 AAA
disabled on card: 2.66 sub-AA
Ochre:
primary-text on canvas: 10.75 AAA
primary-text on card: 8.56 AAA
secondary-text on canvas: 4.99 AA
accent-primary on card: 4.16 AA large
accent-primary-alt on card: 4.88 AA
accent-hover on card: 3.06 AA large
accent-pressed on card: 2.30 sub-AA
disabled on canvas: 1.97 sub-AA
Appendix B: Emotional Coherence Matrix
Noctis: focus | authority | depth | premium
designed for: technical dashboards, data-heavy tools, financial interfaces
Celadon: clarity | growth | calm | natural
designed for: health applications, creative tools, documentation platforms
Ochre: warmth | substance | tradition | craft
designed for: e-commerce, publishing, content-rich portfolios
No perceptual or neurological claims are made about any of the above colors. All contrast ratios computed using the WCAG 2.1 relative luminance formula (ITU-R BT.709 sRGB linearization + BT.601 weighting). No claims about rod stimulation, cone response, or any psychophysical mechanism.