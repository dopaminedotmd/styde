typography system specification
scale:
  name: major third
  ratio: 1.25
  base: 16
  units: px
  levels:
    text-xs: 12
    text-sm: 14
    text-base: 16
    text-lg: 20
    text-xl: 25
    text-2xl: 31
    text-3xl: 39
    text-4xl: 49
    text-5xl: 61
    text-6xl: 76
pair:
  heading:
    family: Inter
    fallback: system-ui, sans-serif
    weight: 600
    letter-spacing: -0.02em
    variable: true
  body:
    family: Source Serif 4
    fallback: Georgia, serif
    weight: 400
    line-height: 1.618
    letter-spacing: 0em
    variable: true
  accent:
    family: JetBrains Mono
    fallback: monospace
    weight: 450
    letter-spacing: 0em
    use: code, labels, metrics
variable:
  Inter:
    source: https://fonts.google.com/variable/Inter
    axes:
      wght: [100, 900]
      slnt: [-10, 0]
    css: font-variation-settings: 'wght' 400, 'slnt' 0
  Source Serif 4:
    source: https://fonts.google.com/variable/Source+Serif+4
    axes:
      wght: [200, 900]
      opsz: [8, 72]
    css: font-variation-settings: 'wght' 400, 'opsz' 16
rhythm:
  baseline: 8
  unit: rem
  line-height-body: 1.618
  line-height-heading: 1.2
  margin-bottom: 1.618
  scale:
    p: 1rem
    h1: 4.75rem
    h2: 3.815rem
    h3: 3.052rem
    h4: 2.441rem
    h5: 1.953rem
    h6: 1.563rem
readable:
  measure-max: 72ch
  measure-min: 45ch
  line-height-body: 1.618
  line-height-heading: 1.2
  contrast-ratio-min: 4.5
  contrast-ratio-large: 3.0
  color-body: #1a1a1a
  color-body-on-dark: #e6e6e6
  css:
    - html: font-size 100%
    - body: font-size 1rem, line-height 1.618, max-width 72ch
    - p: margin-bottom 1.618rem
    - h1: font-size 4.75rem, line-height 1.2, margin-top 0.5em
    - code: font-size 0.875em, background #f4f4f5, padding 0.125em 0.375em