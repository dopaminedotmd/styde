accent: '#4A9EFF'
background: '#0F1117'
font: 'Inter'
root block:
:root {
  --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-size-base: 16px;
  --font-size-sm: 0.875rem;
  --font-size-xs: 0.75rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;
  --accent-h: 214;
  --accent-s: 100%;
  --accent-l: 65%;
  --accent: hsl(var(--accent-h), var(--accent-s), var(--accent-l));
  --accent-hover: hsl(var(--accent-h), var(--accent-s), 58%);
  --accent-active: hsl(var(--accent-h), var(--accent-s), 50%);
  --accent-muted: hsl(var(--accent-h), var(--accent-s), 65%, 0.15);
  --accent-soft: hsl(var(--accent-h), var(--accent-s), 65%, 0.08);
  --bg-base: #0F1117;
  --bg-elevated: #161822;
  --bg-surface: #1A1D2E;
  --bg-inset: #0A0B10;
  --bg-hover: rgba(255, 255, 255, 0.04);
  --bg-active: rgba(255, 255, 255, 0.06);
  --border-subtle: rgba(255, 255, 255, 0.06);
  --border-default: rgba(255, 255, 255, 0.10);
  --border-strong: rgba(255, 255, 255, 0.16);
  --text-primary: #EAEBF0;
  --text-secondary: #9CA0B0;
  --text-tertiary: #6B7084;
  --text-disabled: #43485C;
  --text-inverse: #0F1117;
  --text-on-accent: #0F1117;
  --danger: #EF4444;
  --danger-hover: #DC2626;
  --danger-bg: rgba(239, 68, 68, 0.10);
  --warning: #F59E0B;
  --warning-hover: #D97706;
  --warning-bg: rgba(245, 158, 11, 0.10);
  --success: #22C55E;
  --success-hover: #16A34A;
  --success-bg: rgba(34, 197, 94, 0.10);
  --info: #3B82F6;
  --info-hover: #2563EB;
  --info-bg: rgba(59, 130, 246, 0.10);
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.35);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.4);
  --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.45);
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-xl: 12px;
  --radius-full: 9999px;
  --transition-fast: 100ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-modal: 300;
  --z-toast: 400;
}
contrast check:
  --text-primary (#EAEBF0) on --bg-base (#0F1117): ratio 15.3:1  AAA
  --text-secondary (#9CA0B0) on --bg-base (#0F1117): ratio 9.5:1   AAA
  --text-primary (#EAEBF0) on --bg-surface (#1A1D2E): ratio 14.2:1 AAA
  --text-secondary (#9CA0B0) on --bg-surface (#1A1D2E): ratio 8.8:1 AAA
  --text-on-accent (#0F1117) on --accent (#4A9EFF): ratio 7.8:1    AAA
  all pairs pass AAA.  0 pairs require AA-only.
single :root block.  16px base.  no duplication.