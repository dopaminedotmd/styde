<script lang="ts">
	import CommandPalette from '$lib/components/CommandPalette.svelte';
	import type { CommandGroup } from '$lib/types';

	const commands: CommandGroup[] = [
		{
			label: 'Navigation',
			items: [
				{ id: 'home', label: 'Go Home', icon: '🏠', shortcut: 'Ctrl+H', action: () => alert('Home') },
				{ id: 'search', label: 'Search Files', icon: '🔍', shortcut: 'Ctrl+P', action: () => alert('Search') },
				{ id: 'settings', label: 'Open Settings', icon: '⚙️', shortcut: 'Ctrl+,', action: () => alert('Settings') },
			]
		},
		{
			label: 'Actions',
			items: [
				{ id: 'new', label: 'New Document', icon: '📄', shortcut: 'Ctrl+N', action: () => alert('New') },
				{ id: 'save', label: 'Save', icon: '💾', shortcut: 'Ctrl+S', action: () => alert('Saved') },
				{ id: 'delete', label: 'Delete Item', icon: '🗑️', shortcut: 'Del', action: () => alert('Deleted') },
				{ id: 'disabled', label: 'Disabled Action', icon: '🚫', action: () => {}, disabled: true },
			]
		}
	];

	let open = $state(false);
</script>

<div class="page">
	<h1>⌘ Command Palette</h1>
	<p class="subtitle">New c2: Keyboard-first (Ctrl+K), fuzzy search, grouped commands, $inspect, $host.</p>
	<p>Press <kbd>Ctrl+K</kbd> or <kbd>⌘+K</kbd> to open, or click below:</p>
	<button class="open-btn" onclick={() => open = true}>Open Command Palette ⌘K</button>
	<p class="hint">Use ↑↓ to navigate, ↵ to select, Esc to dismiss.</p>

	<CommandPalette {commands} bind:open />
</div>

<style>
	.page { padding: 24px 32px; max-width: 600px; }
	h1 { font-size: 1.5rem; margin: 0 0 4px; }
	.subtitle { color: #64748b; margin: 0 0 20px; font-size: 0.9rem; }
	.open-btn {
		padding: 12px 24px; background: #6366f1; color: #fff; border: none;
		border-radius: 8px; font-size: 1rem; cursor: pointer; font-weight: 600;
	}
	.open-btn:hover { background: #4f46e5; }
	kbd {
		padding: 2px 6px; background: #f1f5f9; border: 1px solid #d1d5db;
		border-radius: 3px; font-size: 0.8rem; font-family: monospace;
	}
	.hint { color: #94a3b8; font-size: 0.85rem; margin-top: 12px; }
</style>
