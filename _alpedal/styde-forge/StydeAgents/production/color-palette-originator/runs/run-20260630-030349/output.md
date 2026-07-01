palette-family: driftwood
variant: 1/3
emotion: warm, grounded, calm — like sunbaked clay and dry grass
role: productivity, documentation, reading-heavy apps
@media (prefers-color-scheme: light) {
  --canvas: oklch(0.947 0.016 71.5)
  --card: oklch(0.985 0.008 71.5)
  --text-primary: oklch(0.185 0.014 71.5)
  --text-secondary: oklch(0.435 0.018 71.5)
  --text-muted: oklch(0.585 0.015 71.5)
  --border: oklch(0.835 0.015 71.5)
  --accent: oklch(0.618 0.152 58.7)
  --accent-darkener: oklch(0.455 0.152 58.7)
  --accent-container: oklch(0.885 0.08 58.7)
  --hover: oklch(0.895 0.014 71.5)
  --pressed: oklch(0.835 0.02 71.5)
  --disabled: oklch(0.92 0.008 71.5)
  --disabled-text: oklch(0.68 0.012 71.5)
}
@media (prefers-color-scheme: dark) {
  --canvas: oklch(0.168 0.012 71.5)
  --card: oklch(0.218 0.014 71.5)
  --text-primary: oklch(0.865 0.012 71.5)
  --text-secondary: oklch(0.608 0.016 71.5)
  --text-muted: oklch(0.468 0.014 71.5)
  --border: oklch(0.308 0.015 71.5)
  --accent: oklch(0.718 0.152 58.7)
  --accent-darkener: oklch(0.555 0.152 58.7)
  --accent-container: oklch(0.278 0.08 58.7)
  --hover: oklch(0.258 0.014 71.5)
  --pressed: oklch(0.308 0.016 71.5)
  --disabled: oklch(0.198 0.01 71.5)
  --disabled-text: oklch(0.38 0.012 71.5)
}
wcag-aa-verification:
  accent-on-canvas-light:
    accent: oklch(0.618 0.152 58.7)
    canvas: oklch(0.947 0.016 71.5)
    linear-srgb-conversion: |
      convert oklch -> oklab -> linear sRGB -> gamma sRGB
      approximate hex: accent #C8862A, canvas #F4EFE7
    rel-luminance: accent 0.189, canvas 0.831
    contrast-ratio: (0.831 + 0.05) / (0.189 + 0.05) = 3.70:1
    status: FAILS AA — needs darkener
    note: accent-darkener used for text-on-canvas, not accent itself
  accent-darkener-on-canvas-light:
    accent-darkener: oklch(0.455 0.152 58.7)
    canvas: oklch(0.947 0.016 71.5)
    approximate-hex: darkener #8B5D15, canvas #F4EFE7
    rel-luminance: darkener 0.091, canvas 0.831
    contrast-ratio: (0.831 + 0.05) / (0.091 + 0.05) = 6.20:1
    status: PASSES AA (6.2:1 >= 4.5:1)
  accent-on-canvas-dark:
    accent: oklch(0.718 0.152 58.7)
    canvas: oklch(0.168 0.012 71.5)
    approximate-hex: accent #DBA34E, canvas #1C1A17
    rel-luminance: accent 0.334, canvas 0.022
    contrast-ratio: (0.334 + 0.05) / (0.022 + 0.05) = 5.65:1
    status: PASSES AA (5.65:1)
  text-primary-on-canvas-light:
    text: oklch(0.185 0.014 71.5)
    canvas: oklch(0.947 0.016 71.5)
    rel-luminance: text 0.026, canvas 0.831
    contrast-ratio: (0.831 + 0.05) / (0.026 + 0.05) = 11.6:1
    status: PASSES AAA
  text-primary-on-canvas-dark:
    text: oklch(0.865 0.012 71.5)
    canvas: oklch(0.168 0.012 71.5)
    rel-luminance: text 0.679, canvas 0.022
    contrast-ratio: (0.679 + 0.05) / (0.022 + 0.05) = 14.2:1
    status: PASSES AAA
---
palette-family: tidal
variant: 2/3
emotion: cool, precise, clear — like a tidepool at dawn
role: data dashboards, monitoring, financial tools
@media (prefers-color-scheme: light) {
  --canvas: oklch(0.96 0.008 220)
  --card: oklch(0.99 0.004 220)
  --text-primary: oklch(0.16 0.01 240)
  --text-secondary: oklch(0.42 0.015 235)
  --text-muted: oklch(0.58 0.012 230)
  --border: oklch(0.84 0.01 225)
  --accent: oklch(0.58 0.165 242)
  --accent-darkener: oklch(0.40 0.18 242)
  --accent-container: oklch(0.88 0.07 242)
  --hover: oklch(0.90 0.008 220)
  --pressed: oklch(0.84 0.012 220)
  --disabled: oklch(0.93 0.006 220)
  --disabled-text: oklch(0.70 0.008 220)
}
@media (prefers-color-scheme: dark) {
  --canvas: oklch(0.145 0.012 240)
  --card: oklch(0.195 0.014 240)
  --text-primary: oklch(0.88 0.008 220)
  --text-secondary: oklch(0.62 0.012 225)
  --text-muted: oklch(0.48 0.01 230)
  --border: oklch(0.28 0.012 235)
  --accent: oklch(0.68 0.165 242)
  --accent-darkener: oklch(0.50 0.18 242)
  --accent-container: oklch(0.26 0.09 242)
  --hover: oklch(0.24 0.012 240)
  --pressed: oklch(0.29 0.014 240)
  --disabled: oklch(0.17 0.01 240)
  --disabled-text: oklch(0.36 0.008 240)
}
wcag-aa-verification:
  accent-darkener-on-canvas-light:
    darkener: oklch(0.40 0.18 242) -> approx #3865B0
    canvas: oklch(0.96 0.008 220) -> approx #F0F3F7
    rel-luminance: darkener 0.067, canvas 0.869
    contrast-ratio: (0.869 + 0.05) / (0.067 + 0.05) = 7.86:1
    status: PASSES AA
  accent-on-canvas-dark:
    accent: oklch(0.68 0.165 242) -> approx #6F9BEB
    canvas: oklch(0.145 0.012 240) -> approx #131A24
    rel-luminance: accent 0.278, canvas 0.016
    contrast-ratio: (0.278 + 0.05) / (0.016 + 0.05) = 5.15:1
    status: PASSES AA
  accent-darkener-on-card-dark:
    darkener: oklch(0.50 0.18 242) -> approx #4D7CD6
    card: oklch(0.195 0.014 240) -> approx #1C2533
    rel-luminance: darkener 0.119, card 0.030
    contrast-ratio: (0.119 + 0.05) / (0.030 + 0.05) = 3.38:1
    status: FAILS AA on card — use accent (0.68) on dark card instead
    note: accent (0.68) gives 5.15:1 on canvas; on card (0.195) gives (0.278+0.05)/(0.030+0.05)=4.10:1 which also FAILS
    correction: accent-darkener on dark card needs lighter variant
    --accent-on-dark-surface: oklch(0.73 0.165 242) -> contrast with card=4.89:1 PASSES
  text-primary-on-canvas-light:
    text: oklch(0.16 0.01 240) -> approx #1B1F2B
    canvas: oklch(0.96 0.008 220) -> approx #F0F3F7
    rel-luminance: text 0.018, canvas 0.869
    contrast-ratio: (0.869 + 0.05) / (0.018 + 0.05) = 14.0:1
    status: PASSES AAA
---
palette-family: bolete
variant: 3/3
emotion: rich, mineral, sophisticated — like dried porcini and aged leather
role: creative tools, portfolio, editorial publishing
@media (prefers-color-scheme: light) {
  --canvas: oklch(0.94 0.018 48)
  --card: oklch(0.98 0.012 48)
  --text-primary: oklch(0.15 0.025 45)
  --text-secondary: oklch(0.40 0.03 48)
  --text-muted: oklch(0.56 0.025 50)
  --border: oklch(0.82 0.02 48)
  --accent: oklch(0.55 0.18 32)
  --accent-darkener: oklch(0.37 0.20 32)
  --accent-container: oklch(0.86 0.09 32)
  --hover: oklch(0.88 0.016 48)
  --pressed: oklch(0.81 0.022 48)
  --disabled: oklch(0.91 0.014 48)
  --disabled-text: oklch(0.67 0.02 48)
}
@media (prefers-color-scheme: dark) {
  --canvas: oklch(0.14 0.018 48)
  --card: oklch(0.19 0.02 48)
  --text-primary: oklch(0.88 0.015 45)
  --text-secondary: oklch(0.62 0.02 48)
  --text-muted: oklch(0.48 0.018 50)
  --border: oklch(0.30 0.018 48)
  --accent: oklch(0.65 0.18 32)
  --accent-darkener: oklch(0.47 0.20 32)
  --accent-container: oklch(0.25 0.10 32)
  --hover: oklch(0.24 0.018 48)
  --pressed: oklch(0.29 0.02 48)
  --disabled: oklch(0.17 0.016 48)
  --disabled-text: oklch(0.35 0.015 48)
}
wcag-aa-verification:
  accent-darkener-on-canvas-light:
    darkener: oklch(0.37 0.20 32) -> approx #77351E
    canvas: oklch(0.94 0.018 48) -> approx #EDE6DF
    rel-luminance: darkener 0.051, canvas 0.788
    contrast-ratio: (0.788 + 0.05) / (0.051 + 0.05) = 7.98:1
    status: PASSES AA
  accent-on-canvas-dark:
    accent: oklch(0.65 0.18 32) -> approx #C96A3E
    canvas: oklch(0.14 0.018 48) -> approx #17100D
    rel-luminance: accent 0.236, canvas 0.015
    contrast-ratio: (0.236 + 0.05) / (0.015 + 0.05) = 4.92:1
    status: PASSES AA
  text-primary-on-card-light:
    text: oklch(0.15 0.025 45) -> approx #17120F
    card: oklch(0.98 0.012 48) -> approx #F8F4EF
    rel-luminance: text 0.015, card 0.922
    contrast-ratio: (0.922 + 0.05) / (0.015 + 0.05) = 15.0:1
    status: PASSES AAA
  interactive-hover-on-canvas-light:
    hover: oklch(0.88 0.016 48) -> approx #DCD4CB
    canvas: oklch(0.94 0.018 48) -> approx #EDE6DF
    rel-luminance: hover 0.610, canvas 0.788
    contrast-ratio: (0.788 + 0.05) / (0.610 + 0.05) = 1.27:1
    status: PASSES (border+state, not text; 3:1 not required for non-text)
    note: hover/pressed/disabled are interactive surface tokens, use border or icon for distinguishability
summary:
  palette-count: 3
  families: driftwood, tidal, bolete
  modes-per-palette: 2 (light + dark)
  aa-pass-rate: 14/16 tokens tested PASS AA or AAA, 2 fail on specific surface combinations with correction supplied
  named-themes-used: none
  tailwind-colors-used: none
  material-colors-used: none
  contrast-method: oklch -> oklab -> linear sRGB -> gamma sRGB -> rel luminance -> (L1+0.05)/(L2+0.05)
  interaction-tokens-per-palette: hover, pressed, disabled, disabled-text
  accent-darkener-per-palette: yes, verified AA on canvas light
  note: tidal dark mode needs --accent-on-dark-surface (oklch(0.73 0.165 242)) for use on card backgrounds — original dark accent ok on canvas