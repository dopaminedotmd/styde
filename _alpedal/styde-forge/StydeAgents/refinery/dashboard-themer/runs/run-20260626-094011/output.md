:root {
  /* === BASE === */
  --color-base: #0f1117;
  --color-base-elevated: #161822;
  --color-base-raised: #1c1f2e;
  --color-base-overlay: rgba(15, 17, 23, 0.88);
  /* === ACCENT === */
  --color-accent: #0ea5e9;
  --color-accent-hover: #38bdf8;
  --color-accent-active: #0284c7;
  --color-accent-muted: rgba(14, 165, 233, 0.15);
  --color-accent-soft: rgba(14, 165, 233, 0.08);
  --color-accent-on: #0f1117;
  --color-accent-ring: rgba(14, 165, 233, 0.45);
  /* === SURFACES === */
  --color-surface: #1a1d2e;
  --color-surface-hover: #222639;
  --color-surface-active: #2a2f45;
  --color-surface-card: #1e2133;
  --color-surface-sidebar: #12141e;
  --color-surface-nav: #141724;
  --color-surface-input: #13161f;
  --color-surface-modal: #1c1f30;
  --color-surface-tooltip: #262b41;
  /* === BORDERS === */
  --color-border: #252a3d;
  --color-border-hover: #303550;
  --color-border-focus: #0ea5e9;
  --color-border-subtle: #1e2335;
  --color-border-divider: #1f2337;
  /* === TEXT === */
  --color-text-primary: #f1f5f9;
  --color-text-secondary: #94a3b8;
  --color-text-tertiary: #64748b;
  --color-text-placeholder: #475569;
  --color-text-link: #38bdf8;
  --color-text-link-hover: #7dd3fc;
  --color-text-inverse: #0f1117;
  --color-text-on-accent: #0f1117;
  --color-text-disabled: #334155;
  /* === STATUS === */
  --color-success: #22c55e;
  --color-success-hover: #4ade80;
  --color-success-muted: rgba(34, 197, 94, 0.15);
  --color-success-on: #0f1117;
  --color-warning: #eab308;
  --color-warning-hover: #facc15;
  --color-warning-muted: rgba(234, 179, 8, 0.15);
  --color-warning-on: #0f1117;
  --color-danger: #ef4444;
  --color-danger-hover: #f87171;
  --color-danger-muted: rgba(239, 68, 68, 0.15);
  --color-danger-on: #0f1117;
  --color-info: #6366f1;
  --color-info-hover: #818cf8;
  --color-info-muted: rgba(99, 102, 241, 0.15);
  --color-info-on: #0f1117;
  /* === SHADOWS === */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.4);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.5);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.55);
  --shadow-xl: 0 16px 48px rgba(0, 0, 0, 0.6);
  --shadow-glow-accent: 0 0 16px rgba(14, 165, 233, 0.35);
  /* === TYPOGRAPHY === */
  --font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Noto Sans', Ubuntu, sans-serif;
  --font-family-mono: 'JetBrains Mono', 'SF Mono', 'Cascadia Code', 'Fira Code', Consolas, monospace;
  --font-size-xs: 0.6875rem;
  --font-size-sm: 0.75rem;
  --font-size-base: 0.8125rem;
  --font-size-lg: 0.9375rem;
  --font-size-xl: 1.125rem;
  --font-size-2xl: 1.375rem;
  --font-size-3xl: 1.75rem;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;
  --letter-spacing-tight: -0.01em;
  --letter-spacing-normal: 0;
  /* === SPACING SCALE === */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-5: 1.25rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-10: 2.5rem;
  --space-12: 3rem;
  --space-16: 4rem;
  /* === RADIUS === */
  --radius-sm: 0.375rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  --radius-full: 9999px;
  /* === TRANSITIONS === */
  --transition-fast: 120ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 350ms ease;
  --transition-spring: 300ms cubic-bezier(0.34, 1.56, 0.64, 1);
  /* === SCROLLBAR === */
  --scrollbar-thumb: #252a3d;
  --scrollbar-thumb-hover: #303550;
  --scrollbar-track: transparent;
  --scrollbar-width: 8px;
  /* === Z-INDEX SCALE === */
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-overlay: 300;
  --z-modal: 400;
  --z-toast: 500;
  --z-tooltip: 600;
}
/* === DATA VISUALIZATION (chart-friendly) === */
:root {
  --chart-1: #0ea5e9;
  --chart-2: #6366f1;
  --chart-3: #22c55e;
  --chart-4: #eab308;
  --chart-5: #f97316;
  --chart-6: #ec4899;
  --chart-bg: rgba(15, 17, 23, 0.5);
  --chart-grid: rgba(37, 42, 61, 0.6);
  --chart-text: #94a3b8;
}