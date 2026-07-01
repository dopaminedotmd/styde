Command Palette Extender
Domain: frontend Version: 1

Purpose
Command palette (Cmd+K / Ctrl+K) for all dashboard actions. Extensible plugin system so future blueprints can register commands. Search across: view switching, export actions, panel toggles, keyboard shortcuts reference, open recent agents. Cmd+K / Ctrl+K opens floating search bar overlay. Fuzzy search across registered commands, recent agents, views. Plugin system: COMMANDS array that blueprints can push into. Commands: switch view, toggle panel, export, run forge command. Keyboard shortcut reference as default command list.

Persona
Productivity engineer. Keyboard-driven power user experience.

Accessibility
UI state: role=combobox on input, aria-expanded on overlay, aria-activedescendant tracks focused result. Keyboard: ArrowUp and ArrowDown navigate result list, Enter selects active result, Escape dismisses overlay and returns focus to trigger origin. Focus trapping: Tab cycles within overlay, Shift+Tab reverses. On dismiss, focus returns to element that triggered open. aria-label on search input: "Search commands and actions". role=listbox on results container. aria-selected on active result item. aria-live=polite region for result count updates.

States & Edge Cases
Empty state: no results found renders "No matching commands" with a tip icon and suggestion to broaden search. Not an error — no flash or jarring transition. Loading state: debounced search feedback shown when network/plugin resolution is pending. Spinner or skeleton pulse in results area, duration <300ms before visible feedback. Error state: command execution failure renders inline notification inside overlay with message and optional retry button. Overlay stays open, does not crash. Debounce: 150ms default on input handler. Configurable via plugin option debounceMs. Prevents re-render storm on fast typing.

Search History
Client-side recent queries stored in localStorage under key forge:command-palette:history. Max 50 entries, LRU eviction. Deduplicated — consecutive identical queries not stored. Toggle via setting showSearchHistory (default: true). Render as a "Recent" group above results when input is empty and history exists. Clear button clears all history. Each entry shows query text and timestamp. Entries clickable to re-execute. Opt-out via plugin registration option enableHistory: false.

Category Grouping
Commands tagged with category string at registration. Categories: View, Export, Panel, Agent, Forge, Shortcuts. Rendered as tag chips above results area when input is non-empty. Clicking a chip filters results to that category only. Active chip highlighted. Multiple chips selectable (OR logic). Categories defined in command metadata: { id, label, category, keywords, shortcut }. Default category "General" for uncategorized commands.

Plugin API
interface Command {
  id: string
  label: string
  category?: string
  keywords?: string[]
  shortcut?: string
  icon?: string
  execute: () => void | Promise<void>
}

interface PluginMeta {
  name: string
  version: string
  commands: Command[]
  hooks?: {
    onRegister?: () => void
    onUnregister?: () => void
    onSearch?: (query: string, commands: Command[]) => Command[]
  }
}

interface CommandPaletteAPI {
  registerPlugin(meta: PluginMeta): void
  unregisterPlugin(name: string): void
  getCommands(): Command[]
  search(query: string): Command[]
  open(): void
  close(): void
  on(event: 'open' | 'close' | 'select', handler: () => void): void
}

Example usage:
  const myPlugin: PluginMeta = {
    name: 'Export Actions',
    version: '1.0.0',
    commands: [
      { id: 'export-pdf', label: 'Export as PDF', category: 'Export', execute: () => exportPDF() }
    ]
  }
  window.__commandPalette.registerPlugin(myPlugin)

Performance
Bundle size budget: <50KB gzipped. Search latency SLA: first result rendered within 100ms of keystroke. Virtual scroll: max 50 visible items rendered at any time, viewport height budget 400px. Dynamic import for fuse.js or equivalent fuzzy matcher (lazy loaded on first open). Debounce prevents >1 search invocation per 150ms. Memoize search index rebuild on plugin register/unregister, not on each keystroke. Lighthouse accessibility score target: 100.
