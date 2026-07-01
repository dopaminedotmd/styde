--- minimal design system (no input provided — all [ASSUMED]) ---
:root
  color-primary: #2563eb
  color-primary-hover: #1d4ed8
  color-bg: #ffffff
  color-bg-alt: #f8fafc
  color-text: #1e293b
  color-text-muted: #64748b
  color-border: #e2e8f0
  radius-sm: 4px
  radius-md: 8px
  radius-lg: 12px
  spacing-xs: 4px
  spacing-sm: 8px
  spacing-md: 16px
  spacing-lg: 24px
  spacing-xl: 32px
  font-sans: 'Inter', system-ui, -apple-system, sans-serif
  font-mono: 'JetBrains Mono', 'Fira Code', monospace
  shadow-sm: 0 1px 2px rgba(0,0,0,0.05)
  shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1)
  transition-fast: 150ms ease
  transition-base: 250ms ease
[ASSUMED] modern minimal palette — blue primary, neutral grays, Inter font
.btn
  display: inline-flex
  align-items: center
  gap: var(--spacing-sm)
  padding: 0.5rem 1rem
  border: 1px solid var(--color-border)
  border-radius: var(--radius-md)
  background: var(--color-bg)
  color: var(--color-text)
  font-family: var(--font-sans)
  font-size: 0.875rem
  font-weight: 500
  line-height: 1.25rem
  cursor: pointer
  transition: all var(--transition-fast)
.btn:hover
  box-shadow: var(--shadow-sm)
  border-color: var(--color-primary)
.btn--primary
  background: var(--color-primary)
  color: white
  border-color: var(--color-primary)
.btn--primary:hover
  background: var(--color-primary-hover)
.card
  display: flex
  flex-direction: column
  gap: var(--spacing-md)
  padding: var(--spacing-lg)
  border: 1px solid var(--color-border)
  border-radius: var(--radius-lg)
  background: var(--color-bg)
  box-shadow: var(--shadow-sm)
  transition: box-shadow var(--transition-base)
.card:hover
  box-shadow: var(--shadow-md)
.container
  display: grid
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr))
  gap: var(--spacing-lg)
  padding: var(--spacing-xl)
[ASSUMED] three generic components: button, card, responsive grid container. Refine by providing: component spec, brand colors, breakpoints, animation requirements.