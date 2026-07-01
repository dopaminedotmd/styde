Blueprint: command-palette-extender
Version: 1
Domain: frontend
Status: ready
Implementation summary:
  Create CmdPalette.svelte with floating overlay, search input, keyboard trap
  Register Cmd+k / Ctrl+k global listener in Dashboard.svelte or +layout.svelte
  COMMANDS array in a dedicated module: /lib/commands.ts
  Commands shape:
    { id: string, label: string, shortcut?: string, group: string, icon?: string, action: () => void }
  Initial groups: Views, Panels, Export, Forge, Shortcuts
  Default command list maps to the keyboard shortcuts reference group
  Export function: registerCommand(cmd) that pushes into a writable store
  Blueprints push via: import { registerCommand } from '$lib/commands'; registerCommand({...})
  Fuzzy search via simple includes or fzy.js if available
  Overlay closes on Escape, click outside, or command selection
  Focus trap inside overlay when open
  Render in a portal (teleport / body direct) so it overlays all content
Result: A <CmdPalette> component that mounts on Cmd+k, searches filtered commands, and executes on Enter. Blueprints add items through registerCommand(). No markdown, no wrapping. Pure artifact. Ready to wire into any SvelteKit dashboard layout.