<script lang="ts">
	/**
	 * Tabs — Svelte 5 Component
	 * ==========================
	 * An accessible tab panel component built with Svelte 5 runes.
	 *
	 * ## Features
	 * - Keyboard navigation: arrow keys, Home, End
	 * - Proper ARIA roles: tablist, tab, tabpanel
	 * - Active tab indicator with animation
	 * - Support for disabled tabs
	 * - Optional badge counts
	 * - Two-way binding for active tab
	 *
	 * ## Usage
	 * ```svelte
	 * <script>
	 *   import Tabs from '$lib/components/Tabs.svelte';
	 *   import type { TabItem } from '$lib/types';
	 *
	 *   const items: TabItem[] = [
	 *     { id: 'one', label: 'Overview' },
	 *     { id: 'two', label: 'Details' },
	 *     { id: 'three', label: 'Settings' },
	 *   ];
	 *   let active = $state('one');
	 * </script>
	 *
	 * <Tabs {items} bind:active>
	 *   <svelte:fragment slot="one">Overview content…</svelte:fragment>
	 *   <svelte:fragment slot="two">Details content…</svelte:fragment>
	 * </Tabs>
	 * ```
	 *
	 * ## Runes Used
	 * - `$state`  — activeTab, tabRefs
	 * - `$derived` — activeIndex
	 * - `$effect`  — focus management, indicator position
	 */

	import type { TabItem } from '../types';

	// ─── Props ──────────────────────────────────────────────────────
	interface Props {
		/** Tab definitions */
		items: TabItem[];
		/** Currently active tab id (two-way bind) */
		active?: string;
		/** Called when active tab changes */
		onChange?: (id: string) => void;
		/** Variant: 'default' | 'pills' | 'underline' */
		variant?: 'default' | 'pills' | 'underline';
		/** CSS class */
		class?: string;
		/** Children snippets keyed by tab id */
		children?: Record<string, import('svelte').Snippet>;
	}

	let {
		items,
		active = $bindable(items[0]?.id ?? ''),
		onChange,
		variant = 'default',
		class: className = '',
		children = {}
	}: Props = $props();

	// ─── State ──────────────────────────────────────────────────────
	let tabButtons = $state<HTMLElement[]>([]);
	let indicatorStyle = $state('');

	const activeIndex = $derived(items.findIndex((t) => t.id === active));

	// ─── Effects ────────────────────────────────────────────────────
	$effect(() => {
		// Update indicator position when active tab changes
		const idx = activeIndex;
		if (idx >= 0 && tabButtons[idx]) {
			const btn = tabButtons[idx];
			if (variant === 'underline') {
				indicatorStyle = `left: ${btn.offsetLeft}px; width: ${btn.offsetWidth}px;`;
			}
		}
	});

	function setActive(id: string) {
		if (items.find((t) => t.id === id)?.disabled) return;
		active = id;
		onChange?.(id);
	}

	// ─── Keyboard navigation ───────────────────────────────────────
	function handleKeydown(e: KeyboardEvent, currentIdx: number) {
		let newIdx = currentIdx;
		const enabledIndices = items
			.map((t, i) => (t.disabled ? -1 : i))
			.filter((i) => i >= 0);

		switch (e.key) {
			case 'ArrowRight':
			case 'ArrowDown':
				e.preventDefault();
				newIdx = enabledIndices[(enabledIndices.indexOf(currentIdx) + 1) % enabledIndices.length];
				break;
			case 'ArrowLeft':
			case 'ArrowUp':
				e.preventDefault();
				newIdx =
					enabledIndices[
						(enabledIndices.indexOf(currentIdx) - 1 + enabledIndices.length) %
							enabledIndices.length
					];
				break;
			case 'Home':
				e.preventDefault();
				newIdx = enabledIndices[0];
				break;
			case 'End':
				e.preventDefault();
				newIdx = enabledIndices[enabledIndices.length - 1];
				break;
			default:
				return;
		}

		setActive(items[newIdx].id);
		tabButtons[newIdx]?.focus();
	}

	function getVariantClass(): string {
		switch (variant) {
			case 'pills': return 's5-tabs-pills';
			case 'underline': return 's5-tabs-underline';
			default: return 's5-tabs-default';
		}
	}
</script>

<div class="s5-tabs {getVariantClass()} {className}">
	<!-- Tab List -->
	<div class="s5-tabs-list" role="tablist" aria-orientation="horizontal">
		{#each items as tab, idx}
			<button
				bind:this={tabButtons[idx]}
				role="tab"
				id="s5-tab-{tab.id}"
				aria-selected={active === tab.id}
				aria-controls="s5-panel-{tab.id}"
				tabindex={active === tab.id ? 0 : -1}
				disabled={tab.disabled}
				class="s5-tab-btn"
				class:active={active === tab.id}
				class:disabled={tab.disabled}
				onclick={() => setActive(tab.id)}
				onkeydown={(e) => handleKeydown(e, idx)}
				type="button"
			>
				{tab.label}
				{#if tab.badge !== undefined}
					<span class="s5-tab-badge">{tab.badge}</span>
				{/if}
			</button>
		{/each}

		{#if variant === 'underline'}
			<div class="s5-tabs-indicator" style={indicatorStyle}></div>
		{/if}
	</div>

	<!-- Tab Panels -->
	{#each items as tab}
		{@const snippet = children[tab.id]}
		<div
			role="tabpanel"
			id="s5-panel-{tab.id}"
			aria-labelledby="s5-tab-{tab.id}"
			class="s5-tab-panel"
			hidden={active !== tab.id}
			tabindex={0}
		>
			{#if active === tab.id && snippet}
				{@render snippet()}
			{/if}
		</div>
	{/each}
</div>

<style>
	.s5-tabs {
		display: flex;
		flex-direction: column;
	}

	/* Tab List */
	.s5-tabs-list {
		display: flex;
		gap: 2px;
		position: relative;
		border-bottom: 1px solid #e2e8f0;
	}

	/* Tab Button */
	.s5-tab-btn {
		position: relative;
		padding: 10px 18px;
		border: none;
		background: transparent;
		font-size: 0.9rem;
		font-weight: 500;
		color: #64748b;
		cursor: pointer;
		display: flex;
		align-items: center;
		gap: 6px;
		white-space: nowrap;
		transition: color 0.15s;
		border-radius: 6px 6px 0 0;
		font-family: inherit;
	}
	.s5-tab-btn:hover:not(.disabled) {
		color: #334155;
		background: #f8fafc;
	}
	.s5-tab-btn:focus-visible {
		outline: 2px solid #6366f1;
		outline-offset: -2px;
	}
	.s5-tab-btn.active {
		color: #6366f1;
		font-weight: 600;
	}
	.s5-tab-btn.disabled {
		opacity: 0.4;
		cursor: not-allowed;
	}

	/* Badge */
	.s5-tab-badge {
		font-size: 0.7rem;
		background: #e2e8f0;
		color: #475569;
		padding: 1px 6px;
		border-radius: 10px;
		font-weight: 600;
		min-width: 20px;
		text-align: center;
	}
	.s5-tab-btn.active .s5-tab-badge {
		background: #eef2ff;
		color: #6366f1;
	}

	/* Variant: Default */
	.s5-tabs-default .s5-tab-btn.active {
		background: #fff;
		border: 1px solid #e2e8f0;
		border-bottom-color: #fff;
		margin-bottom: -1px;
	}

	/* Variant: Pills */
	.s5-tabs-pills .s5-tabs-list {
		border-bottom: none;
		gap: 4px;
		padding-bottom: 8px;
	}
	.s5-tabs-pills .s5-tab-btn {
		border-radius: 8px;
	}
	.s5-tabs-pills .s5-tab-btn.active {
		background: #eef2ff;
		color: #4f46e5;
	}

	/* Variant: Underline */
	.s5-tabs-underline .s5-tabs-list {
		border-bottom: 2px solid #e2e8f0;
	}
	.s5-tabs-underline .s5-tab-btn {
		border-radius: 0;
		padding: 12px 20px;
	}
	.s5-tabs-underline .s5-tab-btn.active {
		color: #6366f1;
		background: transparent;
	}

	.s5-tabs-indicator {
		position: absolute;
		bottom: -2px;
		left: 0;
		height: 2px;
		background: #6366f1;
		transition: left 0.2s ease, width 0.2s ease;
	}

	/* Tab Panel */
	.s5-tab-panel {
		padding: 16px 0;
		color: #334155;
		font-size: 0.95rem;
		line-height: 1.6;
	}
	.s5-tab-panel[hidden] {
		display: none;
	}
	.s5-tab-panel:focus-visible {
		outline: 2px solid #6366f1;
		outline-offset: 2px;
		border-radius: 4px;
	}
</style>
