<script lang="ts">
	/**
	 * CommandPalette — Svelte 5 Advanced Component
	 * ==============================================
	 * A keyboard-first command palette (like ⌘K) built with Svelte 5 runes.
	 * Uses snippet blocks, $host, $inspect, and advanced reactivity.
	 *
	 * ## Features
	 * - Keyboard-first: Ctrl/Cmd+K to open, arrows to navigate, Enter to select
	 * - Fuzzy search with highlighted matches
	 * - Grouped commands with category headers
	 * - Shortcut display
	 * - $inspect debugging for search/filter state
	 * - $host for portal positioning
	 * - Snippet slots: empty state, custom item rendering
	 * - $effect for scroll-into-view on keyboard nav
	 */

	import type { CommandGroup, CommandItem } from '../types';

	interface Props {
		/** Flat list or grouped commands */
		commands: CommandItem[] | CommandGroup[];
		/** Open state (two-way bind) */
		open?: boolean;
		/** Placeholder text */
		placeholder?: string;
		/** Empty state snippet */
		empty?: import('svelte').Snippet;
		/** Custom item render snippet */
		item?: (cmd: CommandItem, active: boolean) => import('svelte').Snippet;
		/** Called on close */
		onClose?: () => void;
	}

	let {
		commands,
		open = $bindable(false),
		placeholder = 'Type a command or search…',
		empty,
		item,
		onClose
	}: Props = $props();

	let search = $state('');
	let activeIndex = $state(0);
	let inputEl = $state<HTMLInputElement | null>(null);
	let listEl = $state<HTMLDivElement | null>(null);
	let paletteEl = $host<HTMLDivElement>();

	// $inspect — trace in dev mode
	$inspect('CommandPalette open:', open);
	$inspect('CommandPalette search:', search);

	// Normalize commands to flat list with group info
	interface FlatCommand extends CommandItem {
		groupLabel?: string;
	}

	const flatCommands = $derived.by((): FlatCommand[] => {
		if (Array.isArray(commands) && commands.length > 0 && 'items' in commands[0]) {
			// Grouped commands
			const result: FlatCommand[] = [];
			for (const group of commands as CommandGroup[]) {
				for (const cmd of group.items) {
					result.push({ ...cmd, groupLabel: group.label });
				}
			}
			return result;
		}
		return (commands as CommandItem[]).map((c) => ({ ...c }));
	});

	// Fuzzy filter
	const filteredCommands = $derived.by(() => {
		if (!search.trim()) return flatCommands;
		const query = search.toLowerCase();
		return flatCommands.filter((cmd) => {
			const text = `${cmd.label} ${cmd.category ?? ''} ${cmd.groupLabel ?? ''}`.toLowerCase();
			return text.includes(query);
		});
	});

	// Clamp active index
	$effect(() => {
		if (activeIndex >= filteredCommands.length) {
			activeIndex = Math.max(0, filteredCommands.length - 1);
		}
	});

	// Scroll active item into view
	$effect(() => {
		if (listEl) {
			const activeEl = listEl.querySelector('[aria-selected="true"]');
			activeEl?.scrollIntoView({ block: 'nearest' });
		}
	});

	function handleOpen() {
		search = '';
		activeIndex = 0;
		open = true;
	}

	function handleClose() {
		open = false;
		search = '';
		onClose?.();
	}

	function handleKeydown(e: KeyboardEvent) {
		switch (e.key) {
			case 'ArrowDown':
				e.preventDefault();
				activeIndex = (activeIndex + 1) % Math.max(1, filteredCommands.length);
				break;
			case 'ArrowUp':
				e.preventDefault();
				activeIndex = (activeIndex - 1 + filteredCommands.length) % Math.max(1, filteredCommands.length);
				break;
			case 'Enter':
				e.preventDefault();
				if (filteredCommands[activeIndex]?.disabled) return;
				filteredCommands[activeIndex]?.action();
				handleClose();
				break;
			case 'Escape':
				e.preventDefault();
				handleClose();
				break;
		}
	}

	function executeCommand(cmd: FlatCommand) {
		if (cmd.disabled) return;
		cmd.action();
		handleClose();
	}

	// Global keyboard listener
	$effect(() => {
		function handler(e: KeyboardEvent) {
			if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
				e.preventDefault();
				if (open) handleClose();
				else handleOpen();
			}
		}
		window.addEventListener('keydown', handler);
		return () => window.removeEventListener('keydown', handler);
	});

	// Focus input on open
	$effect(() => {
		if (open) {
			requestAnimationFrame(() => inputEl?.focus());
		}
	});

	// Highlight matching text
	function highlightMatch(text: string, query: string): string {
		if (!query) return text;
		const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
		return text.replace(regex, '<mark class="s5-cmd-highlight">$1</mark>');
	}
</script>

{#if open}
	<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
	<div class="s5-cmd-overlay" onclick={handleClose} onkeydown={(e) => { if (e.key === 'Escape') handleClose(); }}>
		<div
			class="s5-cmd-palette"
			role="combobox"
			aria-expanded="true"
			aria-haspopup="listbox"
			aria-label="Command palette"
			bind:this={paletteEl}
			onclick={(e) => e.stopPropagation()}
		>
			<div class="s5-cmd-input-wrap">
				<span class="s5-cmd-search-icon" aria-hidden="true">⌘</span>
				<input
					bind:this={inputEl}
					class="s5-cmd-input"
					type="text"
					bind:value={search}
					{placeholder}
					onkeydown={handleKeydown}
					aria-autocomplete="list"
					aria-controls="s5-cmd-list"
					aria-activedescendant={filteredCommands[activeIndex] ? 's5-cmd-' + filteredCommands[activeIndex].id : undefined}
				/>
			</div>

			<div id="s5-cmd-list" class="s5-cmd-list" role="listbox" bind:this={listEl}>
				{#if filteredCommands.length === 0}
					<div class="s5-cmd-empty">
						{#if empty}
							{@render empty()}
						{:else}
							No commands found.
						{/if}
					</div>
				{:else}
					{#each filteredCommands as cmd, idx}
						{@const showGroupLabel = cmd.groupLabel && (idx === 0 || filteredCommands[idx - 1].groupLabel !== cmd.groupLabel)}
						{#if showGroupLabel}
							<div class="s5-cmd-group-label">{cmd.groupLabel}</div>
						{/if}
						<button
							id="s5-cmd-{cmd.id}"
							class="s5-cmd-item"
							class:active={idx === activeIndex}
							class:disabled={cmd.disabled}
							role="option"
							aria-selected={idx === activeIndex}
							aria-disabled={cmd.disabled}
							disabled={cmd.disabled}
							onclick={() => executeCommand(cmd)}
							onmouseenter={() => activeIndex = idx}
							type="button"
						>
							{#if item}
								{@render item(cmd, idx === activeIndex)}
							{:else}
								{#if cmd.icon}
									<span class="s5-cmd-item-icon">{cmd.icon}</span>
								{/if}
								<span class="s5-cmd-item-label">
									{@html highlightMatch(cmd.label, search)}
								</span>
								{#if cmd.category}
									<span class="s5-cmd-item-category">{cmd.category}</span>
								{/if}
								<span class="s5-cmd-item-spacer"></span>
								{#if cmd.shortcut}
									<span class="s5-cmd-item-shortcut">{cmd.shortcut}</span>
								{/if}
							{/if}
						</button>
					{/each}
				{/if}
			</div>

			<div class="s5-cmd-footer">
				<span>↑↓ Navigate</span>
				<span>↵ Select</span>
				<span>Esc Dismiss</span>
			</div>
		</div>
	</div>
{/if}

<style>
	.s5-cmd-overlay {
		position: fixed;
		inset: 0;
		z-index: 2000;
		display: flex;
		align-items: flex-start;
		justify-content: center;
		padding-top: 15vh;
		background: rgba(0, 0, 0, 0.4);
		backdrop-filter: blur(2px);
		animation: s5-cmd-fade-in 0.15s ease-out;
	}
	@keyframes s5-cmd-fade-in {
		from { opacity: 0; }
		to   { opacity: 1; }
	}

	.s5-cmd-palette {
		width: 100%;
		max-width: 560px;
		background: #fff;
		border-radius: 12px;
		box-shadow: 0 16px 48px rgba(0, 0, 0, 0.18);
		overflow: hidden;
		animation: s5-cmd-slide 0.15s ease-out;
	}
	@keyframes s5-cmd-slide {
		from { opacity: 0; transform: translateY(-8px) scale(0.98); }
		to   { opacity: 1; transform: translateY(0) scale(1); }
	}

	.s5-cmd-input-wrap {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 12px 16px;
		border-bottom: 1px solid #e2e8f0;
	}
	.s5-cmd-search-icon {
		font-size: 1.1rem;
		color: #94a3b8;
		flex-shrink: 0;
	}
	.s5-cmd-input {
		flex: 1;
		border: none;
		outline: none;
		font-size: 1rem;
		color: #1e293b;
		background: transparent;
		font-family: inherit;
	}
	.s5-cmd-input::placeholder { color: #94a3b8; }

	.s5-cmd-list {
		max-height: 320px;
		overflow-y: auto;
		padding: 6px;
	}

	.s5-cmd-group-label {
		padding: 8px 12px 2px;
		font-size: 0.72rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: #94a3b8;
	}

	.s5-cmd-item {
		display: flex;
		align-items: center;
		gap: 10px;
		width: 100%;
		padding: 10px 12px;
		border: none;
		background: transparent;
		border-radius: 6px;
		font-size: 0.9rem;
		color: #334155;
		cursor: pointer;
		text-align: left;
		transition: background 0.1s;
		font-family: inherit;
	}
	.s5-cmd-item.active {
		background: #eef2ff;
		color: #6366f1;
	}
	.s5-cmd-item.disabled {
		opacity: 0.4;
		cursor: not-allowed;
	}

	.s5-cmd-item-icon { font-size: 1.1rem; flex-shrink: 0; }
	.s5-cmd-item-label { flex-shrink: 0; }
	.s5-cmd-item-category {
		font-size: 0.75rem;
		color: #94a3b8;
	}
	.s5-cmd-item-spacer { flex: 1; }
	.s5-cmd-item-shortcut {
		font-size: 0.72rem;
		color: #94a3b8;
		background: #f1f5f9;
		padding: 2px 6px;
		border-radius: 3px;
		font-family: monospace;
	}
	.s5-cmd-item.active .s5-cmd-item-shortcut {
		background: #ddd6fe;
		color: #6366f1;
	}

	.s5-cmd-highlight {
		background: #fef08a;
		color: #1e293b;
		border-radius: 2px;
		padding: 0 1px;
	}
	.s5-cmd-item.active .s5-cmd-highlight {
		background: #fde68a;
	}

	.s5-cmd-empty {
		padding: 24px;
		text-align: center;
		color: #94a3b8;
		font-size: 0.9rem;
	}

	.s5-cmd-footer {
		display: flex;
		gap: 12px;
		padding: 8px 16px;
		border-top: 1px solid #e2e8f0;
		font-size: 0.7rem;
		color: #94a3b8;
	}
</style>
