font-face configuration with all strategies combined:
@font-face {
  font-family: 'Inter V';
  src: url('/fonts/inter-var.woff2') format('woff2');
  font-display: swap;
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
  font-weight: 100 900;
  font-stretch: 75% 125%;
}
@font-face {
  font-family: 'Inter Fallback';
  src: local('Arial'), local('Helvetica');
  size-adjust: 107%;
  ascent-override: 90%;
  descent-override: 22%;
  line-gap-override: 0%;
}
body {
  font-family: 'Inter Fallback', 'Inter V', system-ui, sans-serif;
}
Preload in <head>:
<link rel="preload" href="/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
Subset command (glyphhanger via pyftsubset):
pyftsubset Inter-Variable.woff2 --unicodes="U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD" --layout-features="kern,liga,clig" --flavor=woff2 --output-file=inter-var-latin.woff2
Or with glyphhanger CLI:
glyphhanger https://example.com --subset=Inter-Variable.woff2 --formats=woff2
Variable font advantages: single file covers all weights (100-900), no per-weight HTTP requests. Size ~30KB gzipped vs 200KB+ for 10 static woff2 files.
Fallback metrics via CSS size-adjust calculation tool:
https://www.industrialempathy.com/perfect-ish-font-fallback/?font=Inter
Swap vs optional: swap for above-fold text, optional for body text. Optional gives 100ms block + 100ms swap then invisible fallback - better UX when network is slow and font is non-critical.
Implementation priority:
1. Variable font + subset + preload = fast first paint
2. Fallback with size-adjust = zero CLS
3. font-display: swap for above-fold, optional for below = no FOIT, minimal FOUT
4. unicode-range subsetting cuts payload to 30% of original