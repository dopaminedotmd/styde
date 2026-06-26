/**
 * Enterprise Theming Engine — theme-engine.js
 * Styde Forge Cycle 2 · dark-mode-architect
 *
 * Features:
 *   - Runtime theme switching via data-theme attribute
 *   - localStorage persistence with migration
 *   - System preference detection (prefers-color-scheme)
 *   - Smooth transitions with reduced-motion respect
 *   - Event-driven architecture for theme-aware components
 *   - Data visualization color resolution
 *   - Print-aware (no override during print)
 */

const ThemeEngine = (() => {
  /* -----------------------------------------------------------------------
   * Constants
   * --------------------------------------------------------------------- */
  const STORAGE_KEY = 'styde-theme-preference';
  const THEME_ATTR = 'data-theme';
  const TRANSITION_ATTR = 'data-theme-transitioning';
  const VALID_THEMES = new Set(['light', 'dark', 'oled', 'forest']);
  const DEFAULT_THEME = 'light';
  const TRANSITION_DURATION_MS = 300;

  /* -----------------------------------------------------------------------
   * State
   * --------------------------------------------------------------------- */
  let activeTheme = null;
  let transitionTimer = null;
  const listeners = new Map(); // event → Set<callback>
  let printMediaQuery = null;

  /* -----------------------------------------------------------------------
   * Event System
   * --------------------------------------------------------------------- */
  function emit(eventName, detail = {}) {
    const cbs = listeners.get(eventName);
    if (!cbs) return;
    const payload = { theme: detail.theme || activeTheme, previousTheme: detail.previousTheme, ...detail };
    cbs.forEach(fn => {
      try { fn(payload); } catch (e) { console.error('[ThemeEngine] listener error:', e); }
    });
  }

  function on(eventName, callback) {
    if (!listeners.has(eventName)) listeners.set(eventName, new Set());
    listeners.get(eventName).add(callback);
    return () => listeners.get(eventName).delete(callback);
  }

  /* -----------------------------------------------------------------------
   * Persistence
   * --------------------------------------------------------------------- */
  function loadStoredPreference() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      // Support both legacy string and modern {theme, version} object
      let theme;
      try {
        const parsed = JSON.parse(raw);
        theme = parsed.theme || parsed;
      } catch {
        theme = raw; // legacy flat string
      }
      return VALID_THEMES.has(theme) ? theme : null;
    } catch {
      return null;
    }
  }

  function persistPreference(theme) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        theme,
        version: 2,
        updatedAt: Date.now()
      }));
    } catch (e) {
      console.warn('[ThemeEngine] localStorage unavailable:', e.message);
    }
  }

  /* -----------------------------------------------------------------------
   * System Preference Detection
   * --------------------------------------------------------------------- */
  function getSystemPreference() {
    if (!window.matchMedia) return null;
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) return 'dark';
    if (window.matchMedia('(prefers-color-scheme: light)').matches) return 'light';
    return null;
  }

  function listenToSystemChanges() {
    if (!window.matchMedia) return;
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    const handler = (e) => {
      // Only auto-switch if user hasn't explicitly set a preference
      if (!loadStoredPreference()) {
        setTheme(e.matches ? 'dark' : 'light', { source: 'system' });
      }
    };
    // Use modern addEventListener if available
    if (mq.addEventListener) {
      mq.addEventListener('change', handler);
    } else {
      mq.addListener(handler);
    }
  }

  /* -----------------------------------------------------------------------
   * Print Awareness
   * --------------------------------------------------------------------- */
  function setupPrintDetection() {
    if (!window.matchMedia) return;
    printMediaQuery = window.matchMedia('print');
    const handler = (e) => {
      emit(e.matches ? 'print-start' : 'print-end');
    };
    if (printMediaQuery.addEventListener) {
      printMediaQuery.addEventListener('change', handler);
    } else {
      printMediaQuery.addListener(handler);
    }
  }

  /* -----------------------------------------------------------------------
   * Data Visualization Helpers
   * --------------------------------------------------------------------- */
  function getDataVizColors(count = 12) {
    const cs = getComputedStyle(document.documentElement);
    const colors = [];
    for (let i = 1; i <= Math.min(count, 12); i++) {
      colors.push(cs.getPropertyValue(`--dv-cat-${String(i).padStart(2, '0')}`).trim());
    }
    return colors;
  }

  function getDataVizCSSVar(index) {
    const i = ((index - 1) % 12) + 1;
    return `var(--dv-cat-${String(i).padStart(2, '0')})`;
  }

  function resolveCSSVar(varName) {
    return getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
  }

  /* -----------------------------------------------------------------------
   * Theme Setting
   * --------------------------------------------------------------------- */
  function setTheme(theme, opts = {}) {
    const { source = 'api', animate = true } = opts;

    if (!VALID_THEMES.has(theme)) {
      console.warn(`[ThemeEngine] Invalid theme "${theme}". Valid: ${[...VALID_THEMES].join(', ')}`);
      return false;
    }

    if (theme === activeTheme) return true;

    const previousTheme = activeTheme;

    // Add transition class before changing attribute
    if (animate && previousTheme !== null) {
      document.documentElement.setAttribute(TRANSITION_ATTR, '');
      clearTimeout(transitionTimer);
      transitionTimer = setTimeout(() => {
        document.documentElement.removeAttribute(TRANSITION_ATTR);
      }, TRANSITION_DURATION_MS);
    }

    // Apply theme
    document.documentElement.setAttribute(THEME_ATTR, theme);
    activeTheme = theme;

    // Persist (but not for system-triggered auto-switching)
    if (source !== 'system') {
      persistPreference(theme);
    }

    // Notify listeners
    emit('theme-change', { theme, previousTheme, source });

    return true;
  }

  function getTheme() {
    return activeTheme || loadStoredPreference() || getSystemPreference() || DEFAULT_THEME;
  }

  function getAvailableThemes() {
    return [...VALID_THEMES];
  }

  function cycleTheme() {
    const themes = [...VALID_THEMES];
    const idx = themes.indexOf(activeTheme);
    const next = themes[(idx + 1) % themes.length];
    return setTheme(next, { source: 'cycle' });
  }

  /* -----------------------------------------------------------------------
   * Initialization
   * --------------------------------------------------------------------- */
  function init() {
    if (activeTheme !== null) return; // already initialized

    // Determine initial theme: stored > system > default
    const stored = loadStoredPreference();
    const system = stored ? null : getSystemPreference();
    const initial = stored || system || DEFAULT_THEME;

    // Apply without animation on first load
    document.documentElement.setAttribute(THEME_ATTR, initial);
    activeTheme = initial;

    // Watch for system changes
    listenToSystemChanges();

    // Set up print detection
    setupPrintDetection();

    // Emit initial theme event so components can bootstrap
    emit('theme-init', { theme: initial, source: stored ? 'storage' : system ? 'system' : 'default' });

    return initial;
  }

  /* -----------------------------------------------------------------------
   * Public API
   * --------------------------------------------------------------------- */
  return {
    init,
    setTheme,
    getTheme,
    getAvailableThemes,
    cycleTheme,
    getDataVizColors,
    getDataVizCSSVar,
    resolveCSSVar,
    on,
    get VALID_THEMES() { return VALID_THEMES; },
    get DEFAULT_THEME() { return DEFAULT_THEME; }
  };
})();

/* -----------------------------------------------------------------------
 * Auto-bootstrap (safe for both <head> and <body> placement)
 * --------------------------------------------------------------------- */
if (typeof window !== 'undefined' && typeof document !== 'undefined') {
  // Block render flash: apply theme attribute before paint
  // This runs synchronously so it's the earliest possible moment
  (function preventFOUC() {
    const STORAGE_KEY = 'styde-theme-preference';
    const VALID_THEMES = new Set(['light', 'dark', 'oled', 'forest']);
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      let theme = 'light';
      if (raw) {
        try {
          const parsed = JSON.parse(raw);
          theme = parsed.theme || parsed;
        } catch {
          theme = raw;
        }
        if (!VALID_THEMES.has(theme)) theme = 'light';
      }
      document.documentElement.setAttribute('data-theme', theme);
    } catch {
      document.documentElement.setAttribute('data-theme', 'light');
    }
  })();

  // Full init after DOM is interactive
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => ThemeEngine.init());
  } else {
    ThemeEngine.init();
  }
}

/* -----------------------------------------------------------------------
 * Module export (ESM / UMD compatible)
 * --------------------------------------------------------------------- */
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ThemeEngine;
}
if (typeof define === 'function' && define.amd) {
  define([], () => ThemeEngine);
}
if (typeof window !== 'undefined') {
  window.ThemeEngine = ThemeEngine;
}
