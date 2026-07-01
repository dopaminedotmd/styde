**Revision applied. Outputting revised BLUEPRINT.md below.**
Command Palette Extender
Domain: frontend Version: 2
Purpose
Command palette (Cmd+K / Ctrl+K) for all dashboard actions. Extensible plugin system so future blueprints can register commands. Search across: view switching, export actions, panel toggles, keyboard shortcuts reference, open recent agents. Plugin registration at build-time via COMMANDS array; blueprints call registerCommands() to extend.
Persona
Productivity engineer. Keyboard-driven power user experience.
Skills
- Cmd+K / Ctrl+K opens floating search bar overlay
- Fuzzy search across registered commands, recent agents, views
- Plugin system: COMMANDS array that blueprints can push into
- Commands: switch view, toggle panel, export, run forge command
- Keyboard shortcut reference as default command list
Accessibility
- ARIA attributes on overlay root: role='combobox', aria-expanded (true/false), aria-activedescendant (points to currently highlighted result id), aria-label='Command palette'
- ARIA attributes on input: role='searchbox', aria-autocomplete='list', aria-controls='command-results-listbox'
- ARIA attributes on results list: role='listbox', id='command-results-listbox', aria-label='Search results'
- Keyboard navigation: ArrowUp/Down cycle through results with visual highlight (active descendant updates), Enter executes the highlighted command, Escape dismisses overlay and returns focus to trigger element, Tab/Shift+Tab cycles between input and results list only (focus trap within overlay)
- Focus trapping: on open, focus moves to search input. Tab cycle is contained within the overlay boundary. On close, focus returns to the element that triggered Cmd+K/Ctrl+K
- Screen reader announcements: debounced "N results available" update via aria-live='polite' region
- Reduced motion: CSS prefers-reduced-motion disables open/close animations
States & Edge Cases
- Empty state: overlay displays "No results found" with a muted icon. Shows keyboard shortcut hints below (Esc to close, Enter to select visible item). If no commands registered at all, show "No commands available — install a plugin to get started"
- Loading state: after input change, a 150ms debounce triggers before search executes. During debounce window, show a subtle shimmer/spinner in the search bar. If results take >300ms, show skeleton rows (3 dimmed placeholders)
- Error state: if a command execution throws, render inline error toast below the command: "Failed: [command name] — [error message]" with a dismiss button. Toast auto-dismisses after 5 seconds. Execution errors never crash the overlay
- Debounce configuration: input handler uses 150ms default debounce. Exposed as config debounceMs in plugin registration options (range 50-500ms). If user types faster than debounce, only the final value triggers search — intermediate keystrokes are discarded, not queued
- Overflow state: results list has max-height with CSS scroll. If results exceed viewport, list scrolls internally. Virtual scroll for >50 results
- No-op state: pressing Cmd+K when overlay is already open does nothing (no duplicate stack)
- Unregister: plugins can call unregisterCommands(namespace) on teardown. Graceful degredation if namespace not found