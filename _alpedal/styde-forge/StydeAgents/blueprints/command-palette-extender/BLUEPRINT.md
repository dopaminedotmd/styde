# Command Palette Extender
**Domain:** frontend **Version:** 1

## Purpose
Command palette (Cmd+K / Ctrl+K) for all dashboard actions. Extensible plugin system so future blueprints can register commands. Search across: view switching, export actions, panel toggles, keyboard shortcuts reference, open recent agents.

## Persona
Productivity engineer. Keyboard-driven power user experience.

## Skills
- Cmd+K / Ctrl+K opens floating search bar overlay
- Fuzzy search across registered commands, recent agents, views
- Plugin system: COMMANDS array that blueprints can push into
- Commands: switch view, toggle panel, export, run forge command
- Keyboard shortcut reference as default command list
