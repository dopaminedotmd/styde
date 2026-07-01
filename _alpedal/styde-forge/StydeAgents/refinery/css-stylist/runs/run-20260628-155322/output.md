/* ===== DESIGN TOKENS (CSS Custom Properties) ===== */
:root {
  /* ---- Typography ---- */
  --font-sans: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
  --text-h1-size: clamp(2.25rem, 4vw, 3.5rem);
  --text-h1-weight: 800;
  --text-h1-line-height: 1.1;
  --text-h1-letter-spacing: -0.03em;
  --text-h2-size: clamp(1.75rem, 3vw, 2.5rem);
  --text-h2-weight: 700;
  --text-h2-line-height: 1.2;
  --text-h2-letter-spacing: -0.02em;
  --text-h3-size: clamp(1.375rem, 2.5vw, 1.875rem);
  --text-h3-weight: 600;
  --text-h3-line-height: 1.25;
  --text-h3-letter-spacing: -0.015em;
  --text-h4-size: clamp(1.125rem, 2vw, 1.5rem);
  --text-h4-weight: 600;
  --text-h4-line-height: 1.3;
  --text-h4-letter-spacing: 0;
  --text-h5-size: clamp(1rem, 1.75vw, 1.25rem);
  --text-h5-weight: 600;
  --text-h5-line-height: 1.35;
  --text-h5-letter-spacing: 0;
  --text-h6-size: clamp(0.875rem, 1.5vw, 1rem);
  --text-h6-weight: 600;
  --text-h6-line-height: 1.4;
  --text-h6-letter-spacing: 0.01em;
  --text-body-size: 1rem;
  --text-body-weight: 400;
  --text-body-line-height: 1.6;
  --text-body-letter-spacing: 0;
  --text-small-size: 0.8125rem;
  --text-caption-size: 0.75rem;
  /* ---- Spacing scale ---- */
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
  /* ---- Color tokens (light) ---- */
  --color-surface: #ffffff;
  --color-surface-alt: #f8f9fa;
  --color-surface-raised: #ffffff;
  --color-surface-overlay: rgba(0, 0, 0, 0.45);
  --color-text-primary: #111827;
  --color-text-secondary: #6b7280;
  --color-text-tertiary: #9ca3af;
  --color-text-inverse: #ffffff;
  --color-text-link: #2563eb;
  --color-border: #d1d5db;
  --color-border-light: #e5e7eb;
  --color-border-heavy: #9ca3af;
  --color-brand: #2563eb;
  --color-brand-hover: #1d4ed8;
  --color-brand-active: #1e40af;
  --color-brand-subtle: #eff6ff;
  --color-success: #16a34a;
  --color-success-bg: #f0fdf4;
  --color-warning: #d97706;
  --color-warning-bg: #fffbeb;
  --color-error: #dc2626;
  --color-error-bg: #fef2f2;
  --color-info: #0284c7;
  --color-info-bg: #f0f9ff;
  --color-focus-ring: #2563eb;
  --color-focus-ring-offset: #ffffff;
  /* ---- Form control sizing ---- */
  --input-height: 2.5rem;
  --input-padding-x: 0.75rem;
  --input-padding-y: 0.5rem;
  --input-radius: 0.375rem;
  --input-font-size: 0.9375rem;
  --input-border-width: 1px;
  /* ---- Animation ---- */
  --duration-instant: 0ms;
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 400ms;
  --duration-leisurely: 600ms;
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-in-out: cubic-bezier(0.45, 0, 0.25, 1);
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
  --motion-reduce: 0ms;
}
/* ===== DARK MODE ===== */
@media (prefers-color-scheme: dark) {
  :root {
    --color-surface: #0f172a;
    --color-surface-alt: #1e293b;
    --color-surface-raised: #1e293b;
    --color-surface-overlay: rgba(0, 0, 0, 0.7);
    --color-text-primary: #f1f5f9;
    --color-text-secondary: #94a3b8;
    --color-text-tertiary: #64748b;
    --color-text-inverse: #0f172a;
    --color-text-link: #60a5fa;
    --color-border: #334155;
    --color-border-light: #1e293b;
    --color-border-heavy: #475569;
    --color-brand: #3b82f6;
    --color-brand-hover: #60a5fa;
    --color-brand-active: #93c5fd;
    --color-brand-subtle: rgba(59, 130, 246, 0.12);
    --color-success: #22c55e;
    --color-success-bg: rgba(34, 197, 94, 0.1);
    --color-warning: #f59e0b;
    --color-warning-bg: rgba(245, 158, 11, 0.1);
    --color-error: #ef4444;
    --color-error-bg: rgba(239, 68, 68, 0.1);
    --color-info: #38bdf8;
    --color-info-bg: rgba(56, 189, 248, 0.1);
    --color-focus-ring: #60a5fa;
    --color-focus-ring-offset: #0f172a;
  }
}
/* Explicit class override (for manual toggle) */
.dark {
  --color-surface: #0f172a;
  --color-surface-alt: #1e293b;
  --color-surface-raised: #1e293b;
  --color-surface-overlay: rgba(0, 0, 0, 0.7);
  --color-text-primary: #f1f5f9;
  --color-text-secondary: #94a3b8;
  --color-text-tertiary: #64748b;
  --color-text-inverse: #0f172a;
  --color-text-link: #60a5fa;
  --color-border: #334155;
  --color-border-light: #1e293b;
  --color-border-heavy: #475569;
  --color-brand: #3b82f6;
  --color-brand-hover: #60a5fa;
  --color-brand-active: #93c5fd;
  --color-brand-subtle: rgba(59, 130, 246, 0.12);
  --color-success: #22c55e;
  --color-success-bg: rgba(34, 197, 94, 0.1);
  --color-warning: #f59e0b;
  --color-warning-bg: rgba(245, 158, 11, 0.1);
  --color-error: #ef4444;
  --color-error-bg: rgba(239, 68, 68, 0.1);
  --color-info: #38bdf8;
  --color-info-bg: rgba(56, 189, 248, 0.1);
  --color-focus-ring: #60a5fa;
  --color-focus-ring-offset: #0f172a;
}
/* ===== RESPONSIVE BREAKPOINTS ===== */
/* Mobile-first: min-width approach
   sm: >= 640px   (large phones / phablets)
   md: >= 768px   (tablets portrait)
   lg: >= 1024px  (tablets landscape / small laptops)
   xl: >= 1280px  (desktop)
   2xl: >= 1536px (wide desktop)
   Usage example: @media (--mq-md) { ... }
*/
@custom-media --mq-sm (min-width: 640px);
@custom-media --mq-md (min-width: 768px);
@custom-media --mq-lg (min-width: 1024px);
@custom-media --mq-xl (min-width: 1280px);
@custom-media --mq-2xl (min-width: 1536px);
/* ===== BASE ELEMENTS ===== */
*, *::before, *::after {
  box-sizing: border-box;
}
html {
  font-size: 100%;
  -webkit-text-size-adjust: 100%;
  scroll-behavior: smooth;
}
body {
  font-family: var(--font-sans);
  font-size: var(--text-body-size);
  font-weight: var(--text-body-weight);
  line-height: var(--text-body-line-height);
  letter-spacing: var(--text-body-letter-spacing);
  color: var(--color-text-primary);
  background-color: var(--color-surface);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
/* ---- Typography ---- */
h1, .h1 {
  font-size: var(--text-h1-size);
  font-weight: var(--text-h1-weight);
  line-height: var(--text-h1-line-height);
  letter-spacing: var(--text-h1-letter-spacing);
  margin: 0 0 var(--space-6) 0;
}
h2, .h2 {
  font-size: var(--text-h2-size);
  font-weight: var(--text-h2-weight);
  line-height: var(--text-h2-line-height);
  letter-spacing: var(--text-h2-letter-spacing);
  margin: 0 0 var(--space-5) 0;
}
h3, .h3 {
  font-size: var(--text-h3-size);
  font-weight: var(--text-h3-weight);
  line-height: var(--text-h3-line-height);
  letter-spacing: var(--text-h3-letter-spacing);
  margin: 0 0 var(--space-4) 0;
}
h4, .h4 {
  font-size: var(--text-h4-size);
  font-weight: var(--text-h4-weight);
  line-height: var(--text-h4-line-height);
  letter-spacing: var(--text-h4-letter-spacing);
  margin: 0 0 var(--space-3) 0;
}
h5, .h5 {
  font-size: var(--text-h5-size);
  font-weight: var(--text-h5-weight);
  line-height: var(--text-h5-line-height);
  letter-spacing: var(--text-h5-letter-spacing);
  margin: 0 0 var(--space-2) 0;
}
h6, .h6 {
  font-size: var(--text-h6-size);
  font-weight: var(--text-h6-weight);
  line-height: var(--text-h6-line-height);
  letter-spacing: var(--text-h6-letter-spacing);
  margin: 0 0 var(--space-2) 0;
}
p, .body {
  font-size: var(--text-body-size);
  font-weight: var(--text-body-weight);
  line-height: var(--text-body-line-height);
  margin: 0 0 var(--space-4) 0;
}
small, .small {
  font-size: var(--text-small-size);
}
.caption {
  font-size: var(--text-caption-size);
  color: var(--color-text-secondary);
}
a {
  color: var(--color-text-link);
  text-decoration: underline;
  text-underline-offset: 2px;
  transition: color var(--duration-fast) var(--ease-out);
}
a:hover {
  color: var(--color-brand-hover);
}
a:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
  border-radius: 2px;
}
code {
  font-family: var(--font-mono);
  font-size: 0.875em;
  padding: 0.125em 0.375em;
  background: var(--color-surface-alt);
  border: 1px solid var(--color-border-light);
  border-radius: 4px;
}
/* ===== FORM CONTROLS ===== */
/* ---- Base input styling ---- */
.form-field {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  margin-bottom: var(--space-4);
}
.form-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text-primary);
}
.form-hint {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
}
.form-error {
  font-size: 0.75rem;
  color: var(--color-error);
  display: none;
}
/* Text input, select, textarea */
input[type="text"],
input[type="email"],
input[type="password"],
input[type="search"],
input[type="url"],
input[type="tel"],
input[type="number"],
input[type="date"],
input[type="datetime-local"],
input[type="time"],
input[type="month"],
input[type="week"],
input[type="color"],
select,
textarea {
  font-family: var(--font-sans);
  font-size: var(--input-font-size);
  line-height: 1.4;
  height: var(--input-height);
  padding: var(--input-padding-y) var(--input-padding-x);
  color: var(--color-text-primary);
  background: var(--color-surface);
  border: var(--input-border-width) solid var(--color-border);
  border-radius: var(--input-radius);
  transition:
    border-color var(--duration-fast) var(--ease-out),
    box-shadow var(--duration-fast) var(--ease-out);
  width: 100%;
}
input[type="color"] {
  height: 2.75rem;
  padding: 0.25rem;
}
/* Hover */
input:not(:disabled):hover,
select:not(:disabled):hover,
textarea:not(:disabled):hover {
  border-color: var(--color-border-heavy);
}
/* Focus */
input:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: var(--color-focus-ring);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-focus-ring) 25%, transparent);
}
/* Disabled */
input:disabled,
select:disabled,
textarea:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: var(--color-surface-alt);
}
/* Error state */
.input-error,
input[aria-invalid="true"],
select[aria-invalid="true"],
textarea[aria-invalid="true"] {
  border-color: var(--color-error);
}
.input-error:focus,
input[aria-invalid="true"]:focus,
select[aria-invalid="true"]:focus,
textarea[aria-invalid="true"]:focus {
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-error) 25%, transparent);
}
.input-error ~ .form-error,
[aria-invalid="true"] ~ .form-error {
  display: block;
}
/* Textarea specific */
textarea {
  height: auto;
  min-height: 6rem;
  resize: vertical;
  line-height: 1.6;
}
/* Select with custom arrow */
select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' fill='%236b7280'%3E%3Cpath d='M1.41 0L6 4.58 10.59 0 12 1.41l-6 6-6-6z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  padding-right: 2.25rem;
}
/* ---- Checkbox & Radio ---- */
input[type="checkbox"],
input[type="radio"] {
  appearance: none;
  width: 1.125rem;
  height: 1.125rem;
  margin: 0;
  flex-shrink: 0;
  border: 2px solid var(--color-border);
  background: var(--color-surface);
  cursor: pointer;
  transition:
    border-color var(--duration-fast) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out);
  vertical-align: middle;
}
input[type="checkbox"] {
  border-radius: 4px;
}
input[type="radio"] {
  border-radius: 50%;
}
input[type="checkbox"]:hover,
input[type="radio"]:hover {
  border-color: var(--color-brand);
}
input[type="checkbox"]:focus-visible,
input[type="radio"]:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}
input[type="checkbox"]:checked {
  background: var(--color-brand) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='white'%3E%3Cpath d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z'/%3E%3C/svg%3E") center/80% no-repeat;
  border-color: var(--color-brand);
}
input[type="radio"]:checked {
  background: radial-gradient(circle, var(--color-brand) 40%, transparent 45%);
  border-color: var(--color-brand);
}
input[type="checkbox"]:disabled,
input[type="radio"]:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.checkbox-label,
.radio-label {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  cursor: pointer;
  font-size: 0.9375rem;
  line-height: 1.4;
}
.checkbox-label:has(:disabled),
.radio-label:has(:disabled) {
  opacity: 0.4;
  cursor: not-allowed;
}
/* ---- Toggle Switch ---- */
.toggle {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  cursor: pointer;
  font-size: 0.9375rem;
}
.toggle-track {
  position: relative;
  width: 2.5rem;
  height: 1.375rem;
  background: var(--color-border);
  border-radius: 9999px;
  transition: background-color var(--duration-normal) var(--ease-out);
  flex-shrink: 0;
}
.toggle-track::after {
  content: '';
  position: absolute;
  top: 0.1875rem;
  left: 0.1875rem;
  width: 1rem;
  height: 1rem;
  background: white;
  border-radius: 50%;
  transition: transform var(--duration-normal) var(--ease-out);
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}
.toggle input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}
.toggle input:checked + .toggle-track {
  background: var(--color-brand);
}
.toggle input:checked + .toggle-track::after {
  transform: translateX(1.125rem);
}
.toggle input:focus-visible + .toggle-track {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}
.toggle input:disabled + .toggle-track {
  opacity: 0.4;
}
/* ===== ANIMATION SYSTEM ===== */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
/* Utility classes for animation */
.fade-in {
  animation: anim-fade-in var(--duration-normal) var(--ease-out) forwards;
}
.slide-up {
  animation: anim-slide-up var(--duration-normal) var(--ease-out) forwards;
}
.scale-in {
  animation: anim-scale-in var(--duration-normal) var(--ease-out) forwards;
}
@keyframes anim-fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes anim-slide-up {
  from { opacity: 0; transform: translateY(0.75rem); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes anim-scale-in {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
/* Interactive transitions */
.interactive {
  transition:
    transform var(--duration-fast) var(--ease-out),
    box-shadow var(--duration-fast) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out),
    opacity var(--duration-fast) var(--ease-out);
}
.interactive:hover {
  transform: translateY(-1px);
}
.interactive:active {
  transform: translateY(0);
}
/* ===== BUTTONS ===== */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  font-family: var(--font-sans);
  font-size: 0.9375rem;
  font-weight: 500;
  line-height: 1;
  padding: 0.625rem 1.25rem;
  border: 1px solid transparent;
  border-radius: var(--input-radius);
  cursor: pointer;
  text-decoration: none;
  white-space: nowrap;
  user-select: none;
  transition:
    background-color var(--duration-fast) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out),
    color var(--duration-fast) var(--ease-out),
    transform var(--duration-fast) var(--ease-out),
    box-shadow var(--duration-fast) var(--ease-out);
}
.btn:hover {
  transform: translateY(-1px);
}
.btn:active {
  transform: translateY(0);
}
.btn:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}
.btn-primary {
  background: var(--color-brand);
  color: white;
}
.btn-primary:hover {
  background: var(--color-brand-hover);
}
.btn-secondary {
  background: transparent;
  border-color: var(--color-border);
  color: var(--color-text-primary);
}
.btn-secondary:hover {
  background: var(--color-surface-alt);
  border-color: var(--color-border-heavy);
}
.btn-ghost {
  background: transparent;
  color: var(--color-text-primary);
  border-color: transparent;
}
.btn-ghost:hover {
  background: var(--color-surface-alt);
}
.btn-danger {
  background: var(--color-error);
  color: white;
}
.btn-danger:hover {
  background: #b91c1c;
}
.btn-sm {
  font-size: 0.8125rem;
  padding: 0.375rem 0.75rem;
}
.btn-lg {
  font-size: 1.0625rem;
  padding: 0.75rem 1.75rem;
}
/* ===== NAVIGATION ===== */
/* ---- Nav bar ---- */
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-6);
  height: 3.75rem;
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border-light);
  gap: var(--space-4);
}
.navbar-brand {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--color-text-primary);
  text-decoration: none;
  white-space: nowrap;
}
.navbar-nav {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  list-style: none;
  margin: 0;
  padding: 0;
}
.nav-link {
  display: inline-flex;
  align-items: center;
  padding: var(--space-2) var(--space-3);
  color: var(--color-text-secondary);
  text-decoration: none;
  font-size: 0.9375rem;
  font-weight: 500;
  border-radius: var(--input-radius);
  transition:
    color var(--duration-fast) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out);
}
.nav-link:hover {
  color: var(--color-text-primary);
  background: var(--color-surface-alt);
}
.nav-link.active {
  color: var(--color-brand);
  background: var(--color-brand-subtle);
}
.nav-link:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}
/* ---- Hamburger menu (mobile) ---- */
.hamburger {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 2.25rem;
  height: 2.25rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.375rem;
  border-radius: var(--input-radius);
}
.hamburger span {
  display: block;
  width: 100%;
  height: 2px;
  background: var(--color-text-primary);
  border-radius: 1px;
  transition: transform var(--duration-normal) var(--ease-out);
}
.hamburger:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}
@media (max-width: 767px) {
  .hamburger {
    display: inline-flex;
  }
  .navbar-nav {
    display: none;
    position: absolute;
    top: 3.75rem;
    left: 0;
    right: 0;
    flex-direction: column;
    background: var(--color-surface);
    border-bottom: 1px solid var(--color-border-light);
    padding: var(--space-2);
    box-shadow: 0 8px 24px var(--color-surface-overlay);
  }
  .navbar-nav.open {
    display: flex;
  }
}
/* ---- Sidebar ---- */
.sidebar {
  width: 16rem;
  min-width: 16rem;
  height: 100%;
  background: var(--color-surface);
  border-right: 1px solid var(--color-border-light);
  padding: var(--space-4) 0;
  overflow-y: auto;
}
.sidebar-nav {
  list-style: none;
  margin: 0;
  padding: 0;
}
.sidebar-link {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-4);
  color: var(--color-text-secondary);
  text-decoration: none;
  font-size: 0.9375rem;
  border-left: 3px solid transparent;
  transition:
    color var(--duration-fast) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out);
}
.sidebar-link:hover {
  background: var(--color-surface-alt);
  color: var(--color-text-primary);
}
.sidebar-link.active {
  color: var(--color-brand);
  background: var(--color-brand-subtle);
  border-left-color: var(--color-brand);
}
.sidebar-link:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: -2px;
}
.sidebar-section-title {
  padding: var(--space-3) var(--space-4) var(--space-1);
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-tertiary);
}
/* ---- Tabs ---- */
.tabs {
  display: flex;
  gap: 0;
  border-bottom: 2px solid var(--color-border-light);
  list-style: none;
  margin: 0;
  padding: 0;
}
.tab {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  color: var(--color-text-secondary);
  font-size: 0.9375rem;
  font-weight: 500;
  text-decoration: none;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  cursor: pointer;
  background: none;
  transition:
    color var(--duration-fast) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out);
}
.tab:hover {
  color: var(--color-text-primary);
  border-bottom-color: var(--color-border);
}
.tab.active {
  color: var(--color-brand);
  border-bottom-color: var(--color-brand);
}
.tab:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: -2px;
  border-radius: 2px;
}
/* ---- Breadcrumbs ---- */
.breadcrumbs {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  list-style: none;
  margin: 0;
  padding: 0;
  font-size: 0.875rem;
  flex-wrap: wrap;
}
.breadcrumbs li {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
}
.breadcrumbs li + li::before {
  content: '/';
  color: var(--color-text-tertiary);
  font-size: 0.75rem;
}
.breadcrumb-link {
  color: var(--color-text-secondary);
  text-decoration: none;
}
.breadcrumb-link:hover {
  color: var(--color-text-primary);
  text-decoration: underline;
}
.breadcrumb-current {
  color: var(--color-text-primary);
  font-weight: 500;
}
/* ---- Pagination ---- */
.pagination {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  list-style: none;
  margin: 0;
  padding: 0;
}
.page-item {
  display: inline-flex;
}
.page-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 2.25rem;
  height: 2.25rem;
  padding: 0 var(--space-2);
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
  border: 1px solid transparent;
  border-radius: var(--input-radius);
  transition:
    color var(--duration-fast) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out);
}
.page-link:hover {
  background: var(--color-surface-alt);
  border-color: var(--color-border-light);
  color: var(--color-text-primary);
}
.page-item.active .page-link {
  background: var(--color-brand);
  color: white;
  border-color: var(--color-brand);
}
.page-link:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}
.page-item.disabled .page-link {
  opacity: 0.4;
  pointer-events: none;
}
/* ===== ACCESSIBILITY ===== */
/* Screen-reader-only utility */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
.sr-only-focusable:not(:focus):not(:focus-visible) {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
/* Skip-to-content link (visually hidden until focused) */
.skip-to-content {
  position: absolute;
  top: -100%;
  left: var(--space-4);
  background: var(--color-brand);
  color: white;
  padding: var(--space-2) var(--space-4);
  border-radius: 0 0 var(--input-radius) var(--input-radius);
  z-index: 9999;
  font-weight: 500;
  text-decoration: none;
}
.skip-to-content:focus {
  top: 0;
}
/* Focus-visible for all interactive elements */
:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}
/* Remove focus outline for mouse users (keep for keyboard) */
:focus:not(:focus-visible) {
  outline: none;
}
/* Reduced motion: applied globally via media query above */
/* High contrast mode support */
@media (prefers-contrast: high) {
  :root {
    --color-border: #000000;
    --color-border-light: #555555;
    --color-text-secondary: #444444;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --color-border: #ffffff;
      --color-border-light: #aaaaaa;
      --color-text-secondary: #cccccc;
    }
  }
}