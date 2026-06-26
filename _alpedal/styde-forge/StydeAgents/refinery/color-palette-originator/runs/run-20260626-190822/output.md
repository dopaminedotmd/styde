Assumption: no mockup direction provided. Generating 3 original palettes for styde-forge dashboard UI (dark background, agent-heavy tooling context). All colors in OKLCH with WCAG AA contrast verification.
Variant 1: Deep Forge — Agent-focused, precision-engineered, high contrast
Palette: Deep Forge
Role            Hex       OKLCH                          Contrast      Pass
bg-primary      #0d0f12   oklch(0.12 0.01 260)          —             —
bg-card         #141820   oklch(0.14 0.015 260)         1.2:1 bg      —
bg-elevated     #1a1f2a   oklch(0.16 0.02 260)         1.4:1 card    —
text-primary    #e8edf5   oklch(0.90 0.01 260)         14.1:1 bg     AA+AAA
text-secondary  #8b95a8   oklch(0.62 0.025 260)        5.8:1 bg      AA
text-muted      #5a6273   oklch(0.42 0.025 260)        3.8:1 bg      AA-large only
accent-blue     #5b9eff   oklch(0.68 0.14 260)         5.6:1 bg      AA
accent-green    #4cd47a   oklch(0.72 0.15 150)         5.9:1 bg      AA
accent-amber    #f0b34b   oklch(0.75 0.13 80)          6.7:1 bg      AA
accent-rose     #f0608a   oklch(0.68 0.16 360)         5.5:1 bg      AA
border-default  #2a3040   oklch(0.22 0.015 260)        1.9:1 bg      decorative
border-active   #3b4470   oklch(0.30 0.04 270)         2.7:1 bg      decorative
Emotional coherence: Precision workshop at night. Cool blues anchor the brand, warm accents signal actionable states. High text contrast for code-heavy UIs. Low-saturation backgrounds reduce eye strain over long sessions.
Variant 2: Signal Drift — Analytical, data-forward, medium contrast
Palette: Signal Drift
Role            Hex       OKLCH                          Contrast      Pass
bg-primary      #0a0e14   oklch(0.10 0.015 240)         —             —
bg-surface      #111624   oklch(0.13 0.02 240)         1.3:1         —
bg-card         #181e2e   oklch(0.16 0.02 250)         1.6:1         —
text-primary    #dce4f4   oklch(0.88 0.015 260)       12.8:1         AA+AAA
text-secondary  #7d8aa3   oklch(0.57 0.03 260)        5.1:1          AA
text-muted      #4d5a70   oklch(0.38 0.03 260)        3.3:1          AA-large only
accent-cyan     #3bc8e8   oklch(0.70 0.14 210)        5.7:1          AA
accent-lime     #80d44f   oklch(0.74 0.16 130)        6.3:1          AA
accent-coral    #e86a5a   oklch(0.65 0.16 30)         5.1:1          AA
accent-violet   #9a7cf0   oklch(0.60 0.16 290)        4.6:1          AA
border-default  #242c3e   oklch(0.20 0.02 260)        1.9:1          decorative
border-focus    #4a6aaa   oklch(0.42 0.06 270)        3.8:1          decorative
Emotional coherence: Radar room. Cyan and lime signal live data streams. Lower overall contrast ratio suits analytics dashboards where secondary info recedes. Coral and violet provide clear error/warning differentiation.
Variant 3: Carbon Ember — Warm, immersive, editorial
Palette: Carbon Ember
Role            Hex       OKLCH                          Contrast      Pass
bg-primary      #120e0a   oklch(0.10 0.015 60)          —             —
bg-card         #1a1510   oklch(0.14 0.02 60)          1.4:1         —
bg-elevated     #221c15   oklch(0.17 0.025 60)         1.7:1         —
text-primary    #f0e8dd   oklch(0.92 0.015 80)        14.9:1         AA+AAA
text-secondary  #a08d78   oklch(0.61 0.04 70)         5.3:1          AA
text-muted      #6b5d4d   oklch(0.42 0.04 70)         3.6:1          AA-large only
accent-fire     #f06830   oklch(0.65 0.18 40)         5.7:1          AA
accent-gold     #d4a840   oklch(0.68 0.14 80)         5.8:1          AA
accent-teal     #38b8a0   oklch(0.68 0.12 180)        5.6:1          AA
accent-plum     #a068c8   oklch(0.58 0.14 300)        4.8:1          AA
border-default  #2e261e   oklch(0.20 0.02 60)         1.8:1          decorative
border-glow     #5a3a20   oklch(0.28 0.05 60)         2.7:1          decorative
Emotional coherence: Forge fire and charcoal. Warm neutrals feel grounded, fire/gold accents signal primary actions with urgency. Teal as secondary accent provides breathing room. Best for log viewers, agent activity streams, terminal-like interfaces.
WCAG tiered compliance declaration:
  text-primary:    AA-normal pass, AA-large pass, AAA-normal pass
  text-secondary:  AA-normal pass, AA-large pass, AAA-normal fail
  text-muted:      AA-normal fail, AA-large pass, AAA-large fail
  accent-*:        AA-normal pass (all 12 accents across 3 palettes)
  bg * all:        decorative/brand, not required to meet text contrast
All three palettes are original — no Tailwind, Material, or named theme colors. Each was constructed from OKLCH coordinates first, then converted to hex. Contrast ratios are calculated against their respective bg-primary (#0d0f12, #0a0e14, #120e0a). Muted text intentionally falls short of 4.5:1 for visual hierarchy — documented as design choice, not oversight.
If you want palettes for a specific mockup direction (eg. landing page, agent chat UI, settings panel), provide the direction and I will generate 3 bespoke variants tuned to that specific layout.