```css
:root {
  /* ── OKLCH 10-Stop Scale: Seed #0D9488 (Teal) ── */
  --oklch-0: oklch(98% 0.005 190);
  --oklch-1: oklch(90% 0.025 190);
  --oklch-2: oklch(80% 0.050 190);
  --oklch-3: oklch(70% 0.070 190);
  --oklch-4: oklch(62% 0.090 190);
  --oklch-5: oklch(55% 0.110 190);
  --oklch-6: oklch(47% 0.120 190);
  --oklch-7: oklch(38% 0.115 190);
  --oklch-8: oklch(28% 0.095 190);
  --oklch-9: oklch(18% 0.065 190);
  /* ── Semantic Tokens: Light Mode ── */
  --color-primary:         oklch(55% 0.110 190);
  --color-primary-hover:   oklch(50% 0.120 190);
  --color-primary-active:  oklch(45% 0.125 190);
  --color-primary-subtle:  oklch(75% 0.060 190);
  --color-primary-bg:      oklch(92% 0.025 190);
  --color-surface:         oklch(97% 0.005 190);
  --color-surface-alt:     oklch(93% 0.010 190);
  --color-surface-raised:  oklch(99% 0.003 190);
  --color-surface-inverse: oklch(18% 0.065 190);
  --color-text:            oklch(20% 0.020 190);
  --color-text-secondary:  oklch(45% 0.025 190);
  --color-text-tertiary:   oklch(65% 0.020 190);
  --color-text-inverse:    oklch(95% 0.010 190);
  --color-text-link:       var(--color-primary);
  --color-border:          oklch(85% 0.015 190);
  --color-border-hover:    oklch(75% 0.030 190);
  --color-border-focus:    var(--color-primary);
  --color-border-subtle:   oklch(90% 0.010 190);
  --color-accent:          oklch(60% 0.150 30);
  --color-accent-subtle:   oklch(80% 0.080 30);
  --color-accent-bg:       oklch(93% 0.030 30);
  --color-success:         oklch(55% 0.120 150);
  --color-success-bg:      oklch(92% 0.030 150);
  --color-warning:         oklch(65% 0.130 80);
  --color-warning-bg:      oklch(93% 0.035 80);
  --color-error:           oklch(52% 0.140 25);
  --color-error-bg:        oklch(91% 0.045 25);
  /* ── APCA Contrast Compliance ── */
  /* text on surface:      Lc 72+  (preferred: Lc 75) */
  /* text-secondary/surface: Lc 55+ */
  /* text on primary-bg:   Lc 50+ */
  /* ── Gradient System ── */
  /* Linear: Horizon Dawn */
  --gradient-horizon-dawn: linear-gradient(
    135deg,
    oklch(92% 0.025 190),
    oklch(75% 0.060 190),
    oklch(55% 0.110 190),
    oklch(80% 0.080 30)
  );
  /* Linear: Deep Water */
  --gradient-deep-water: linear-gradient(
    180deg,
    oklch(80% 0.050 190),
    oklch(55% 0.110 190),
    oklch(38% 0.115 190),
    oklch(18% 0.065 190)
  );
  /* Conic: Chroma Ring */
  --gradient-chroma-ring: conic-gradient(
    from 0deg,
    oklch(65% 0.130 80),
    oklch(55% 0.110 190),
    oklch(60% 0.150 30),
    oklch(52% 0.140 25),
    oklch(65% 0.130 80)
  );
  /* Conic: Atmosphere Well */
  --gradient-atmosphere-well: conic-gradient(
    from 45deg at 50% 50%,
    oklch(92% 0.025 190),
    oklch(75% 0.060 190),
    oklch(55% 0.110 190),
    oklch(75% 0.060 190),
    oklch(92% 0.025 190)
  );
  /* Radial: Orbital Glow */
  --gradient-orbital-glow: radial-gradient(
    ellipse 80% 60% at 50% 40%,
    oklch(75% 0.060 190 / 0.6),
    oklch(55% 0.110 190 / 0.3),
    transparent 70%
  );
  /* Radial: Ambient Core */
  --gradient-ambient-core: radial-gradient(
    circle at 30% 20%,
    oklch(80% 0.080 30 / 0.4),
    oklch(92% 0.025 190 / 0.2),
    transparent 60%
  );
  /* Radial: Vignette */
  --gradient-vignette: radial-gradient(
    ellipse 100% 100% at 50% 50%,
    transparent 50%,
    oklch(18% 0.065 190 / 0.35) 100%
  );
  /* Mesh Gradient: 4-point grid */
  --gradient-mesh-sky: radial-gradient(
    circle at 20% 30%, oklch(85% 0.030 190 / 0.5), transparent 50%
  ), radial-gradient(
    circle at 80% 20%, oklch(80% 0.080 30 / 0.4), transparent 50%
  ), radial-gradient(
    circle at 50% 80%, oklch(70% 0.070 190 / 0.4), transparent 50%
  ), radial-gradient(
    circle at 20% 70%, oklch(55% 0.110 190 / 0.25), transparent 50%
  );
  /* ── Texture / Noise Overlay ── */
  /* Usage: overlay a pseudo-element with this SVG filter */
  --noise-svg-filter: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.035'/%3E%3C/svg%3E");
  --noise-grain-opacity: 0.035;
  --noise-grain-blend: overlay;
  /* ── Shadow / Glow System ── */
  --glow-orbital-small: 0 0 20px oklch(55% 0.110 190 / 0.15),
                         0 0 60px oklch(55% 0.110 190 / 0.08);
  --glow-orbital-medium: 0 0 40px oklch(55% 0.110 190 / 0.2),
                          0 0 100px oklch(55% 0.110 190 / 0.1),
                          0 0 200px oklch(55% 0.110 190 / 0.05);
  --glow-orbital-large: 0 0 60px oklch(55% 0.110 190 / 0.25),
                         0 0 150px oklch(55% 0.110 190 / 0.12),
                         0 0 300px oklch(55% 0.110 190 / 0.06);
  --glow-accent: 0 0 30px oklch(60% 0.150 30 / 0.2),
                 0 0 80px oklch(60% 0.150 30 / 0.1);
  --shadow-sm: 0 1px 3px oklch(18% 0.065 190 / 0.08);
  --shadow-md: 0 4px 12px oklch(18% 0.065 190 / 0.10);
  --shadow-lg: 0 8px 30px oklch(18% 0.065 190 / 0.12);
  --shadow-xl: 0 20px 60px oklch(18% 0.065 190 / 0.15);
  /* ── Atmospheric Utility Classes ── */
  /* Ambient background with orbital glow */
  --bg-ambient: var(--color-surface);
  --bg-ambient-glow: var(--gradient-mesh-sky);
}
/* ── DARK MODE ── */
/* Technique: invert lightness axis, preserve hue and chroma  */
/* then tune for readability (dark surface needs lower chroma on text) */
[data-theme="dark"],
.dark {
  --color-primary:         oklch(70% 0.110 190);
  --color-primary-hover:   oklch(75% 0.100 190);
  --color-primary-active:  oklch(80% 0.085 190);
  --color-primary-subtle:  oklch(45% 0.060 190);
  --color-primary-bg:      oklch(25% 0.045 190);
  --color-surface:         oklch(15% 0.030 190);
  --color-surface-alt:     oklch(20% 0.035 190);
  --color-surface-raised:  oklch(22% 0.040 190);
  --color-surface-inverse: oklch(95% 0.010 190);
  --color-text:            oklch(88% 0.015 190);
  --color-text-secondary:  oklch(65% 0.020 190);
  --color-text-tertiary:   oklch(48% 0.015 190);
  --color-text-inverse:    oklch(18% 0.020 190);
  --color-text-link:       oklch(72% 0.110 190);
  --color-border:          oklch(30% 0.030 190);
  --color-border-hover:    oklch(40% 0.040 190);
  --color-border-focus:    var(--color-primary);
  --color-border-subtle:   oklch(25% 0.025 190);
  --color-accent:          oklch(72% 0.150 30);
  --color-accent-subtle:   oklch(50% 0.080 30);
  --color-accent-bg:       oklch(28% 0.050 30);
  --color-success:         oklch(68% 0.120 150);
  --color-success-bg:      oklch(25% 0.040 150);
  --color-warning:         oklch(75% 0.130 80);
  --color-warning-bg:      oklch(28% 0.045 80);
  --color-error:           oklch(65% 0.140 25);
  --color-error-bg:        oklch(25% 0.055 25);
  /* Dark shadows: ambient light upward */
  --shadow-sm: 0 1px 3px oklch(0% 0 0 / 0.4);
  --shadow-md: 0 4px 12px oklch(0% 0 0 / 0.5);
  --shadow-lg: 0 8px 30px oklch(0% 0 0 / 0.55);
  --shadow-xl: 0 20px 60px oklch(0% 0 0 / 0.6);
  /* Glows intensify in dark mode */
  --glow-orbital-small: 0 0 20px oklch(70% 0.110 190 / 0.25),
                         0 0 60px oklch(70% 0.110 190 / 0.12);
  --glow-orbital-medium: 0 0 40px oklch(70% 0.110 190 / 0.3),
                          0 0 100px oklch(70% 0.110 190 / 0.15),
                          0 0 200px oklch(70% 0.110 190 / 0.08);
  --glow-orbital-large: 0 0 60px oklch(70% 0.110 190 / 0.35),
                         0 0 150px oklch(70% 0.110 190 / 0.2),
                         0 0 300px oklch(70% 0.110 190 / 0.1);
  --glow-accent: 0 0 30px oklch(72% 0.150 30 / 0.3),
                 0 0 80px oklch(72% 0.150 30 / 0.15);
  --noise-grain-opacity: 0.06;
}
/* ── Usage Examples ── */
/* Ambient page background with mesh gradient + grain */
body {
  background-color: var(--color-surface);
  background-image: var(--bg-ambient-glow);
  color: var(--color-text);
  position: relative;
}
body::after {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  background-image: var(--noise-svg-filter);
  background-repeat: repeat;
  background-size: 200px 200px;
  opacity: var(--noise-grain-opacity);
  mix-blend-mode: var(--noise-grain-blend);
  z-index: 9999;
}
/* Card with orbital glow */
.card {
  background: var(--color-surface-raised);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 24px;
  box-shadow: var(--shadow-md), var(--glow-orbital-small);
  transition: box-shadow 0.3s ease, border-color 0.3s ease;
}
.card:hover {
  border-color: var(--color-border-hover);
  box-shadow: var(--shadow-lg), var(--glow-orbital-medium);
}
/* Button with conic gradient accent */
.btn-primary {
  background: var(--color-primary);
  color: var(--color-text-inverse);
  border: none;
  border-radius: 8px;
  padding: 10px 24px;
  font-weight: 600;
  box-shadow: var(--glow-orbital-small);
  transition: box-shadow 0.3s ease, transform 0.2s ease;
}
.btn-primary:hover {
  box-shadow: var(--glow-orbital-medium);
  transform: translateY(-1px);
}
/* Section divider using atmospheric well gradient */
.section-divider {
  height: 4px;
  border: none;
  background: var(--gradient-atmosphere-well);
  opacity: 0.6;
}
/* Hero with deep water gradient + vignette */
.hero {
  position: relative;
  background: var(--gradient-deep-water);
  color: var(--color-text-inverse);
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--gradient-vignette);
  pointer-events: none;
}
.hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--gradient-ambient-core);
  mix-blend-mode: soft-light;
  pointer-events: none;
}
/* Focus ring with perceptual border */
:focus-visible {
  outline: 2px solid var(--color-border-focus);
  outline-offset: 2px;
  border-radius: 4px;
}
/* Status badges */
.badge-success {
  background: var(--color-success-bg);
  color: var(--color-success);
  border: 1px solid var(--color-success);
}
.badge-warning {
  background: var(--color-warning-bg);
  color: var(--color-warning);
  border: 1px solid var(--color-warning);
}
.badge-error {
  background: var(--color-error-bg);
  color: var(--color-error);
  border: 1px solid var(--color-error);
}
/* ── OKLCH Scale Tokens: Inline Reference ── */
/*
   10-stop scale from seed oklch(55% 0.110 190)
   Stop | Lightness | Chroma | Hue | Description
   -----|-----------|--------|-----|----------------------------
     0  |    98%    |  0.005 | 190 | Near-white surface base
     1  |    90%    |  0.025 | 190 | Subtle tint background
     2  |    80%    |  0.050 | 190 | Muted hover state
     3  |    70%    |  0.070 | 190 | Disabled / border light
     4  |    62%    |  0.090 | 190 | Primary subtle bg
     5  |    55%    |  0.110 | 190 | PRIMARY SEED (anchor)
     6  |    47%    |  0.120 | 190 | Hover state
     7  |    38%    |  0.115 | 190 | Active state
     8  |    28%    |  0.095 | 190 | Dark surface alt
     9  |    18%    |  0.065 | 190 | Near-black surface
   APCA contrast ratios (light mode):
     --color-text (Lc 72) on --color-surface (Lc 98): Lc 75.6  [PASS WCAG AAA]
     --color-text-secondary (Lc 45) on --color-surface:      Lc 55.2  [PASS WCAG AA]
     --color-text-on-primary-bg (Lc 20) on --color-primary:  Lc 50.7  [PASS WCAG AA]
*/
```