┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\command-palette-extender\BLUEPRINT.md → b/StydeAgents\blueprints\command-palette-extender\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -1,15 +1,65 @@[0m
[38;2;255;255;255;48;2;119;20;20m-# Command Palette Extender[0m
[38;2;255;255;255;48;2;119;20;20m-**Domain:** frontend **Version:** 1[0m
[38;2;255;255;255;48;2;19;87;20m+Command Palette Extender[0m
[38;2;255;255;255;48;2;19;87;20m+Domain: frontend Version: 1[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-## Purpose[0m
[38;2;255;255;255;48;2;119;20;20m-Command palette (Cmd+K / Ctrl+K) for all dashboard actions. Extensible plugin system so future blueprints can register commands. Search across: view switching, export actions, panel toggles, keyboard shortcuts reference, open recent agents.[0m
[38;2;255;255;255;48;2;19;87;20m+Purpose[0m
[38;2;255;255;255;48;2;19;87;20m+Command palette (Cmd+K / Ctrl+K) for all dashboard actions. Extensible plugin system so future blueprints can register commands. Search across: view switching, export actions, panel toggles, keyboard shortcuts reference, open recent agents. Cmd+K / Ctrl+K opens floating search bar overlay. Fuzzy search across registered commands, recent agents, views. Plugin system: COMMANDS array that blueprints can push into. Commands: switch view, toggle panel, export, run forge command. Keyboard shortcut reference as default command list.[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-## Persona[0m
[38;2;255;255;255;48;2;19;87;20m+Persona[0m
[38;2;184;134;11m Productivity engineer. Keyboard-driven power user experience.[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-## Skills[0m
[38;2;255;255;255;48;2;119;20;20m-- Cmd+K / Ctrl+K opens floating search bar overlay[0m
[38;2;255;255;255;48;2;119;20;20m-- Fuzzy search across registered commands, recent agents, views[0m
[38;2;255;255;255;48;2;119;20;20m-- Plugin system: COMMANDS array that blueprints can push into[0m
[38;2;255;255;255;48;2;119;20;20m-- Commands: switch view, toggle panel, export, run forge command[0m
[38;2;255;255;255;48;2;119;20;20m-- Keyboard shortcut reference as default command list[0m
[38;2;255;255;255;48;2;19;87;20m+Accessibility[0m
[38;2;255;255;255;48;2;19;87;20m+UI state: role=combobox on input, aria-expanded on overlay, aria-activedescendant tracks focused result. Keyboard: ArrowUp/Down navigate result list, Enter selects active result, Escape dismisses overlay and returns focus to trigger origin. Focus trapping: Tab cycles within overlay, Shift+Tab reverses. On dismiss, focus returns to element that triggered open. aria-label on search input: "Search commands and actions". role=listbox on results container. aria-selected on active result item. aria-live=polite region for result count updates.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+States & Edge Cases[0m
[38;2;255;255;255;48;2;19;87;20m+Empty state: no results found renders "No matching commands" with a tip icon and suggestion to broaden search. Not an error — no flash or jarring transition. Loading state: debounced search feedback shown when network/plugin resolution is pending. Spinner or skeleton pulse in results area, duration <300ms before visible feedback. Error state: command execution failure renders inline notification inside overlay with message and optional retry button. Overlay stays open, does not crash. Debounce: 150ms default on input handler. Configurable via plugin option debounceMs. Prevents re-render storm on fast typing.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Search History[0m
[38;2;255;255;255;48;2;19;87;20m+Client-side recent queries stored in localStorage under key forge:command-palette:history. Max 50 entries, LRU eviction. Deduplicated — consecutive identical queries not stored. Toggle via setting showSearchHistory (default: true). Render as a "Recent" group above results when input is empty and history exists. Clear button clears all history. Each entry shows query text and timestamp. Entries clickable to re-execute. Opt-out via plugin registration option enableHistory: false.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Category Grouping[0m
[38;2;255;255;255;48;2;19;87;20m+Commands tagged with category string at registration. Categories: View, Export, Panel, Agent, Forge, Shortcuts. Rendered as tag chips above results area when input is non-empty. Clicking a chip filters results to that category only. Active chip highlighted. Multiple chips selectable (OR logic). Categories defined in command metadata: { id, label, category, keywords, shortcut }. Default category "General" for uncategorized commands.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Plugin API[0m
[38;2;255;255;255;48;2;19;87;20m+interface Command {[0m
[38;2;255;255;255;48;2;19;87;20m+  id: string[0m
[38;2;255;255;255;48;2;19;87;20m+  label: string[0m
[38;2;255;255;255;48;2;19;87;20m+  category?: string[0m
[38;2;255;255;255;48;2;19;87;20m+  keywords?: string[][0m
[38;2;255;255;255;48;2;19;87;20m+  shortcut?: string[0m
[38;2;255;255;255;48;2;19;87;20m+  icon?: string[0m
[38;2;255;255;255;48;2;19;87;20m+  execute: () => void | Promise<void>[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+interface PluginMeta {[0m
[38;2;255;255;255;48;2;19;87;20m+  name: string[0m
[38;2;255;255;255;48;2;19;87;20m+  version: string[0m
[38;2;255;255;255;48;2;19;87;20m+  commands: Command[][0m
[38;2;255;255;255;48;2;19;87;20m+  hooks?: {[0m
[38;2;255;255;255;48;2;19;87;20m+    onRegister?: () => void[0m
[38;2;255;255;255;48;2;19;87;20m+    onUnregister?: () => void[0m
[38;2;255;255;255;48;2;19;87;20m+    onSearch?: (query: string, commands: Command[]) => Command[][0m
[38;2;255;255;255;48;2;19;87;20m+  }[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+interface CommandPaletteAPI {[0m
[38;2;255;255;255;48;2;19;87;20m+  registerPlugin(meta: PluginMeta): void[0m
[38;2;255;255;255;48;2;19;87;20m+  unregisterPlugin(name: string): void[0m
[38;2;255;255;255;48;2;19;87;20m+  getCommands(): Command[][0m
[38;2;255;255;255;48;2;19;87;20m+  search(query: string): Command[][0m
[38;2;255;255;255;48;2;19;87;20m+  open(): void[0m
[38;2;255;255;255;48;2;19;87;20m+  close(): void[0m
[38;2;255;255;255;48;2;19;87;20m+  on(event: 'open' | 'close' | 'select', handler: () => void): void[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Example usage:[0m
[38;2;255;255;255;48;2;19;87;20m+  const myPlugin: PluginMeta = {[0m
[38;2;255;255;255;48;2;19;87;20m+    name: 'Export Actions',[0m
[38;2;255;255;255;48;2;19;87;20m+    version: '1.0.0',[0m
[38;2;255;255;255;48;2;19;87;20m+    commands: [[0m
[38;2;255;255;255;48;2;19;87;20m+      { id: 'export-pdf', label: 'Export as PDF', category: 'Export', execute: () => exportPDF() }[0m
[38;2;255;255;255;48;2;19;87;20m+    ][0m
[38;2;255;255;255;48;2;19;87;20m+  }[0m
[38;2;255;255;255;48;2;19;87;20m+  window.__commandPalette.registerPlugin(myPlugin)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Performance[0m
[38;2;255;255;255;48;2;19;87;20m+Bundle size budget: <50KB gzipped. Search latency SLA: first result rendered within 100ms of keystroke. Virtual scroll: max 50 visible items rendered at any time, viewport height budget 400px. Dynamic import for fuse.js or equivalent fuzzy matcher (lazy loaded on first open). Debounce prevents >1 search invocation per 150ms. Memoize search index rebuild on plugin register/unregister, not on each keystroke. Lighthouse accessibility score target: 100.[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\command-palette-extender\BLUEPRINT.md → b/E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\command-palette-extender\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -8,7 +8,7 @@[0m
[38;2;184;134;11m Productivity engineer. Keyboard-driven power user experience.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m Accessibility[0m
[38;2;255;255;255;48;2;119;20;20m-UI state: role=combobox on input, aria-expanded on overlay, aria-activedescendant tracks focused result. Keyboard: ArrowUp/Down navigate result list, Enter selects active result, Escape dismisses overlay and returns focus to trigger origin. Focus trapping: Tab cycles within overlay, Shift+Tab reverses. On dismiss, focus returns to element that triggered open. aria-label on search input: "Search commands and actions". role=listbox on results container. aria-selected on active result item. aria-live=polite region for result count updates.[0m
[38;2;255;255;255;48;2;19;87;20m+UI state: role=combobox on input, aria-expanded on overlay, aria-activedescendant tracks focused result. Keyboard: ArrowUp and ArrowDown navigate result list, Enter selects active result, Escape dismisses overlay and returns focus to trigger origin. Focus trapping: Tab cycles within overlay, Shift+Tab reverses. On dismiss, focus returns to element that triggered open. aria-label on search input: "Search commands and actions". role=listbox on results container. aria-selected on active result item. aria-live=polite region for result count updates.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m States & Edge Cases[0m
[38;2;184;134;11m Empty state: no results found renders "No matching commands" with a tip icon and suggestion to broaden search. Not an error — no flash or jarring transition. Loading state: debounced search feedback shown when network/plugin resolution is pending. Spinner or skeleton pulse in results area, duration <300ms before visible feedback. Error state: command execution failure renders inline notification inside overlay with message and optional retry button. Overlay stays open, does not crash. Debounce: 150ms default on input handler. Configurable via plugin option debounceMs. Prevents re-render storm on fast typing.[0m
Ad-hoc verification: 20/20 checks passed, temp file cleaned up. This is not suite-level CI — it's a targeted script that validates all 5 feedback items (accessibility, states/edge cases, performance, plugin API, search history + category grouping) are present in the updated BLUEPRINT.md with the right content.