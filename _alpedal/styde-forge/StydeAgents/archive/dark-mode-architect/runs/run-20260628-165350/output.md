Confidence: 40% — no task body, design specs, or target files provided
Detect:
  missing: task body, design details, CSS/scss files to theme, component list, brand colors
  present: blueprint persona and skills, teacher feedback on r-coverage and efficiency
Propose three alternatives:
1. Paste full task input now — e.g. "Create dark theme tokens for a React dashboard with primary=#2563eb"
2. Point to a file or directory — e.g. "Read src/styles/variables.css and src/components/ for theming"
3. Format example — valid task input for this blueprint looks like:
```
task: Add dark mode to existing component library
files:
  - src/styles/tokens.css
  - src/components/Button/
  - src/components/Card/
spec:
  brand_primary: '#2563eb'
  brand_secondary: '#7c3aed'
  surface_levels: 3
  contrast_ratio_min: 4.5:1
  prefers_color_scheme: true
  manual_toggle: true
```
Prompt me with one of the three above and I will produce:
- CSS custom property token sets (light + dark)
- Contrast-validated palette output with WCAG AA/AAA ratings
- r-coverage YAML summary (standardized per teacher feedback)