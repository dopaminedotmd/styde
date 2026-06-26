:root {
  /* Base - 16px standard */
  --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  --font-size-base: 16px;
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-md: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 2rem;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;
  /* Spacing / Rhythm Scale */
  --space-0: 0;
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
  --space-20: 5rem;
  --space-24: 6rem;
  /* Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;
  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.4), 0 2px 4px -2px rgba(0,0,0,0.3);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.5), 0 4px 6px -4px rgba(0,0,0,0.4);
  --shadow-xl: 0 20px 25px -5px rgba(0,0,0,0.6), 0 8px 10px -6px rgba(0,0,0,0.4);
  /* Transitions / Easing */
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-smooth: cubic-bezier(0.65, 0, 0.35, 1);
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 350ms;
  --duration-slower: 500ms;
  /* Primary / Accent - #6366f1 (indigo) */
  --color-primary-50: #eef2ff;
  --color-primary-100: #e0e7ff;
  --color-primary-200: #c7d2fe;
  --color-primary-300: #a5b4fc;
  --color-primary-400: #818cf8;
  --color-primary-500: #6366f1;
  --color-primary-600: #4f46e5;
  --color-primary-700: #4338ca;
  --color-primary-800: #3730a3;
  --color-primary-900: #312e81;
  --color-primary: var(--color-primary-500);
  /* Surface / Background - #0f1117 */
  --color-surface-50: #f8fafc;
  --color-surface-100: #f1f5f9;
  --color-surface-200: #e2e8f0;
  --color-surface-300: #cbd5e1;
  --color-surface-400: #94a3b8;
  --color-surface-500: #64748b;
  --color-surface-600: #475569;
  --color-surface-700: #334155;
  --color-surface-800: #1e293b;
  --color-surface-900: #0f172a;
  --color-surface-950: #0f1117;
  --color-bg: var(--color-surface-950);
  --color-bg-elevated: var(--color-surface-900);
  --color-bg-card: var(--color-surface-800);
  --color-bg-input: var(--color-surface-900);
  --color-bg-hover: rgba(255,255,255,0.04);
  /* Text - WCAG AAA on #0f1117 (luminance 0.004) */
  --color-text-primary: #f1f5f9;
  --color-text-secondary: #94a3b8;
  --color-text-tertiary: #64748b;
  --color-text-inverse: #0f172a;
  --color-text-link: var(--color-primary-400);
  --color-text-link-hover: var(--color-primary-300);
  --color-text-on-primary: #ffffff;
  /* Border */
  --color-border: rgba(255,255,255,0.08);
  --color-border-hover: rgba(255,255,255,0.14);
  --color-border-focus: var(--color-primary-500);
  --color-border-muted: rgba(255,255,255,0.05);
  /* States */
  --color-hover: rgba(255,255,255,0.06);
  --color-active: rgba(255,255,255,0.10);
  --color-selected: rgba(99,102,241,0.20);
  --color-focus-ring: rgba(99,102,241,0.35);
  --color-error: #ef4444;
  --color-error-bg: rgba(239,68,68,0.10);
  --color-success: #22c55e;
  --color-success-bg: rgba(34,197,94,0.10);
  --color-warning: #eab308;
  --color-warning-bg: rgba(234,179,8,0.10);
  --color-info: #3b82f6;
  --color-info-bg: rgba(59,130,246,0.10);
}
/*
Component token usage examples:
.card {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  box-shadow: var(--shadow-md);
  transition: box-shadow var(--duration-normal) var(--ease-out),
              border-color var(--duration-normal) var(--ease-out);
}
.card:hover {
  border-color: var(--color-border-hover);
  box-shadow: var(--shadow-lg);
}
.button-primary {
  background: var(--color-primary);
  color: var(--color-text-on-primary);
  font-weight: var(--font-weight-semibold);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-md);
  border: none;
  transition: background var(--duration-fast) var(--ease-out),
              transform var(--duration-fast) var(--ease-out);
  cursor: pointer;
}
.button-primary:hover {
  background: var(--color-primary-600);
}
.button-primary:active {
  transform: scale(0.97);
}
.input {
  background: var(--color-bg-input);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-2) var(--space-3);
  color: var(--color-text-primary);
  font-size: var(--font-size-md);
  font-family: var(--font-family);
  transition: border-color var(--duration-fast) var(--ease-out),
              box-shadow var(--duration-fast) var(--ease-out);
}
.input:focus {
  border-color: var(--color-border-focus);
  box-shadow: 0 0 0 3px var(--color-focus-ring);
  outline: none;
}
.input::placeholder {
  color: var(--color-text-tertiary);
}
*/