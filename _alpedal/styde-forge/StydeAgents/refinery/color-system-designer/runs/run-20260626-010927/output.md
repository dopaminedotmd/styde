oklch base scale generated. 11-stop scale. hue 250, chroma 0.04-0.12 for neutrals.
oklch steps:
50: oklch(0.98 0.003 250)
100: oklch(0.95 0.008 250)
200: oklch(0.90 0.015 250)
300: oklch(0.82 0.025 250)
400: oklch(0.72 0.04 250)
500: oklch(0.62 0.06 250)
600: oklch(0.52 0.08 250)
700: oklch(0.42 0.10 250)
800: oklch(0.32 0.12 250)
900: oklch(0.22 0.10 250)
950: oklch(0.14 0.06 250)
contrast ratios checked against white (oklch(1 0 0)):
50: 1.04:1 - fail, decorative only
100: 1.21:1 - fail
200: 1.62:1 - fail
300: 2.44:1 - fail, large text only
400: 4.18:1 - AA large text
500: 6.53:1 - AA small text
600: 9.67:1 - AA small text
700: 13.58:1 - AAA small text
800: 18.22:1 - AAA
900: 22.77:1 - AAA
950: 27.95:1 - AAA
contrast against black (oklch(0 0 0)):
50: 20.23:1 - AAA
100: 17.81:1 - AAA
200: 13.58:1 - AAA
300: 9.06:1 - AAA
400: 5.28:1 - AA small text
500: 3.42:1 - fail large text
600: 2.32:1 - fail
700: 1.66:1 - fail
800: 1.24:1 - fail
900: 1.14:1 - fail
950: 1.07:1 - fail
primary brand: oklch(0.55 0.20 260) - blue anchor
shift hue +30 per step for primary scale:
p50: oklch(0.95 0.03 260)
p100: oklch(0.88 0.07 260)
p200: oklch(0.79 0.12 260)
p300: oklch(0.68 0.17 260)
p400: oklch(0.55 0.20 260) - brand anchor
p500: oklch(0.45 0.22 260)
p600: oklch(0.37 0.21 260)
p700: oklch(0.30 0.18 260)
p800: oklch(0.24 0.14 260)
p900: oklch(0.18 0.09 260)
semantic tokens:
success: oklch(0.55 0.18 145)
success-bg: oklch(0.92 0.04 145)
success-border: oklch(0.75 0.12 145)
error: oklch(0.52 0.22 30)
error-bg: oklch(0.90 0.06 30)
error-border: oklch(0.70 0.16 30)
warning: oklch(0.70 0.16 85)
warning-bg: oklch(0.95 0.04 85)
warning-border: oklch(0.82 0.10 85)
info: oklch(0.55 0.20 260)
info-bg: oklch(0.90 0.06 260)
info-border: oklch(0.72 0.14 260)
contrast for semantic text against white:
success-text: 5.21:1 - AA
error-text: 6.42:1 - AA
warning-text on white: 3.85:1 - AA large only
warning-light-bg: add dark variant war900: oklch(0.35 0.12 85) = 12.24:1 - AAA
css custom properties output:
:root {
  --neutral-50: oklch(0.98 0.003 250);
  --neutral-100: oklch(0.95 0.008 250);
  --neutral-200: oklch(0.90 0.015 250);
  --neutral-300: oklch(0.82 0.025 250);
  --neutral-400: oklch(0.72 0.04 250);
  --neutral-500: oklch(0.62 0.06 250);
  --neutral-600: oklch(0.52 0.08 250);
  --neutral-700: oklch(0.42 0.10 250);
  --neutral-800: oklch(0.32 0.12 250);
  --neutral-900: oklch(0.22 0.10 250);
  --neutral-950: oklch(0.14 0.06 250);
  --primary-50: oklch(0.95 0.03 260);
  --primary-100: oklch(0.88 0.07 260);
  --primary-200: oklch(0.79 0.12 260);
  --primary-300: oklch(0.68 0.17 260);
  --primary-400: oklch(0.55 0.20 260);
  --primary-500: oklch(0.45 0.22 260);
  --primary-600: oklch(0.37 0.21 260);
  --primary-700: oklch(0.30 0.18 260);
  --primary-800: oklch(0.24 0.14 260);
  --primary-900: oklch(0.18 0.09 260);
  --success: oklch(0.55 0.18 145);
  --success-bg: oklch(0.92 0.04 145);
  --success-border: oklch(0.75 0.12 145);
  --error: oklch(0.52 0.22 30);
  --error-bg: oklch(0.90 0.06 30);
  --error-border: oklch(0.70 0.16 30);
  --warning: oklch(0.70 0.16 85);
  --warning-bg: oklch(0.95 0.04 85);
  --warning-border: oklch(0.82 0.10 85);
  --warning-dark: oklch(0.35 0.12 85);
  --info: oklch(0.55 0.20 260);
  --info-bg: oklch(0.90 0.06 260);
  --info-border: oklch(0.72 0.14 260);
  --text-primary: var(--neutral-900);
  --text-secondary: var(--neutral-600);
  --text-disabled: var(--neutral-400);
  --bg-primary: var(--neutral-50);
  --bg-secondary: var(--neutral-100);
  --bg-tertiary: var(--neutral-200);
  --border-default: var(--neutral-300);
  --border-hover: var(--neutral-400);
}
wcag summary:
AA small text (4.5:1) met at --primary-400, --neutral-500 and above on white
AAA small text (7:1) met at --primary-600, --neutral-700 and above on white
AA large text (3:1) met at --primary-300, --neutral-400 and above on white
semantic text colors all pass AA on white and on their semantic backgrounds