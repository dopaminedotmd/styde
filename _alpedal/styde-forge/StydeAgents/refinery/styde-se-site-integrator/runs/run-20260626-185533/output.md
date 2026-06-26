Blueprint: styde-se-site-integrator
Version: 3
Status: COMPLETE
Quality gate: PASS (estimated 95/100)
Deliverables defined: 6 files
  src/components/site-nav-bar.ts
  src/components/site-breadcrumb.ts
  src/components/site-progress-bar.ts
  src/components/site-footer.ts
  src/styles/theme-contract.css
  src/layouts/site-shell.ts
Chrome layers: 4 (nav, breadcrumb, content shell, footer)
State matrix: 5 states x 4 layers = 20 entries defined
Theme contract: light/dark tokens + reduced-motion + system-preference default
Progress bar: event-driven with 10s safety timeout, nested navigation handling
Known gaps (confidence 85%):
  1. No mobile nav collapse/hamburger behaviour defined — Layer 1 assumes 5 links always visible
  2. No breakpoints specified — responsive behaviour at 768px and below is implied but not explicit
  3. Breadcrumb web component path attribute schema is described but no TypeScript interface/type exported
Next step: submit to forge.py spawn --eval --improve --production with blueprint: styde-se-site-integrator-v3