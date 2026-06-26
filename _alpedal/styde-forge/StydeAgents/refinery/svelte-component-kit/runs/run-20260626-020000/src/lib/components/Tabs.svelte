<script lang="ts">
	/**
	 * Tabs v2 — Svelte 5 Advanced Component
	 * =======================================
	 * Enhanced tab panel with $inspect debugging, $host reference,
	 * icon support, and lazy panel rendering option.
	 *
	 * ## v2 Improvements (c2)
	 * - $inspect traces active tab and indicator position
	 * - $host for tab list element
	 * - Icon support per tab item
	 * - Lazy panel rendering (optional: only render when active)
	 * - Improved indicator animation via $effect tracking
	 * - Vertical variant support
	 */

	import type { TabItem } from '../types';

	interface Props {
		items: TabItem[];
		active?: string;
		onChange?: (id: string) => void;
		variant?: 'default' | 'pills' | 'underline';
		/** Vertical layout */
		vertical?: boolean;
		/** Only render panel content when tab is active */
		lazy?: boolean;
		class?: string;
		children?: Record<string, import('svelte').Snippet>;
	}

	let {
		items,
		active = $bindable(items[0]?.id ?? ''),
		onChange,
		variant = 'default',
		vertical = false,
		lazy = false,
		class: className = '',
		children = {}
	}: Props = $props();

	let tabButtons = $state<HTMLElement[]>([]);
	let indicatorStyle = $state('');
	let tabListEl = $host<HTMLDivElement>();

	const activeIndex = $derived(items.findIndex((t) => t.id === active));

	// $inspect — trace in dev mode
	$inspect('Tabs active:', active);
	$inspect('Tabs activeIndex:', activeIndex);
	$inspect('Tabs variant:', variant);

	$effect(() => {
		const idx = activeIndex;
		if (idx >= 0 && tabButtons[idx] && variant === 'underline') {
			const btn = tabButtons[idx];
			if (vertical) {
				indicatorStyle = `top: ${btn.offsetTop}px; height: ${btn.offsetHeight}px;`;
			} else {
				indicatorStyle = `left: ${btn.offsetLeft}px; width: ${btn.offsetWidth}px;`;
			}
		}
	});

	function setActive(id: string) {
		if (items.find((t) => t.id === id)?.disabled) return;
		active = id;
		onChange?.(id);
	}

	function handleKeydown(e: KeyboardEvent, currentIdx: number) {
		let newIdx = currentIdx;
		const enabled = items
			.map((t, i) => (t.disabled ? -1 : i))
			.filter((i) => i >= 0);

		const nextKey = vertical ? 'ArrowDown' : 'ArrowRight';
		const prevKey = vertical ? 'ArrowUp' : 'ArrowLeft';

		switch (e.key) {
			case nextKey:
			case 'ArrowDown':
				e.preventDefault();
				newIdx = enabled[(enabled.indexOf(currentIdx) + 1) % enabled.length];
				break;
			case prevKey:
			case 'ArrowUp':
				e.preventDefault();
				newIdx = enabled[
					(enabled.indexOf(currentIdx) - 1 + enabled.length) % enabled.length
				];
				break;
			case 'Home':
				e.preventDefault();
				newIdx = enabled[0];
				break;
			case 'End':
				e.preventDefault();
				newIdx = enabled[enabled.length - 1];
				break;
			default:
				return;
		}

		setActive(items[newIdx].id);
		tabButtons[newIdx]?.focus();
	}

	function variantClass(): string {
		switch (variant) {
			case 'pills': return 's5-tabs-pills';
			case 'underline': return 's5-tabs-underline';
			default: return 's5-tabs-default';
		}
	}
</script>

<div
	class="s5-tabs {variantClass()} {className}"
	class:s5-tabs-vertical={vertical}
>
	<div
		class="s5-tabs-list"
		role="tablist"
		aria-orientation={vertical ? 'vertical' : 'horizontal'}
		bind:this={tabListEl}
	>
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
				{#if tab.icon}
					<span class="s5-tab-icon" aria-hidden="true">{tab.icon}</span>
				{/if}
				{tab.label}
				{#if tab.badge !== undefined}
					<span class="s5-tab-badge">{tab.badge}</span>
				{/if}
			</button>
		{/each}

		{#if variant === 'underline'}
			<div class="s5-tabs-indicator" class:s5-tabs-indicator-vertical={vertical} style={indicatorStyle}></div>
		{/if}
	</div>

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
			{#if lazy}
				{#if active === tab.id && snippet}
					{@render snippet()}
				{/if}
			{:else if snippet}
				<div style={active === tab.id ? '' : 'display: none;'}>
					{@render snippet()}
				</div>
			{/if}
		</div>
	{/each}
</div>

<style>
	.s5-tabs { display: flex; flex-direction: column; }
	.s5-tabs-vertical { flex-direction: row; gap: 16px; }

	.s5-tabs-list {
		display: flex;
		gap: 2px;
		position: relative;
		border-bottom: 1px solid #e2e8f0;
	}
	.s5-tabs-vertical .s5-tabs-list {
		flex-direction: column;
		border-bottom: none;
		border-right: 1px solid #e2e8f0;
		min-width: 160px;
	}

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
	.s5-tabs-vertical .s5-tab-btn {
		border-radius: 6px 0 0 6px;
		justify-content: flex-start;
	}
	.s5-tab-btn:hover:not(.disabled) { color: #334155; background: #f8fafc; }
	.s5-tab-btn:focus-visible { outline: 2px solid #6366f1; outline-offset: -2px; }
	.s5-tab-btn.active { color: #6366f1; font-weight: 600; }
	.s5-tab-btn.disabled { opacity: 0.4; cursor: not-allowed; }

	.s5-tab-icon { font-size: 1.1rem; line-height: 1; }
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
	.s5-tab-btn.active .s5-tab-badge { background: #eef2ff; color: #6366f1; }

	/* Default variant */
	.s5-tabs-default .s5-tab-btn.active {
		background: #fff;
		border: 1px solid #e2e8f0;
		border-bottom-color: #fff;
		margin-bottom: -1px;
	}
	.s5-tabs-vertical.s5-tabs-default .s5-tab-btn.active {
		border-bottom-color: #e2e8f0;
		border-right-color: #fff;
		margin-bottom: 0;
		margin-right: -1px;
	}

	/* Pills variant */
	.s5-tabs-pills .s5-tabs-list { border-bottom: none; gap: 4px; padding-bottom: 8px; }
	.s5-tabs-vertical.s5-tabs-pills .s5-tabs-list { border-right: none; padding-bottom: 0; padding-right: 8px; }
	.s5-tabs-pills .s5-tab-btn { border-radius: 8px; }
	.s5-tabs-pills .s5-tab-btn.active { background: #eef2ff; color: #4f46e5; }

	/* Underline variant */
	.s5-tabs-underline .s5-tabs-list { border-bottom: 2px solid #e2e8f0; }
	.s5-tabs-vertical.s5-tabs-underline .s5-tabs-list { border-bottom: none; border-right: 2px solid #e2e8f0; }
	.s5-tabs-underline .s5-tab-btn { border-radius: 0; padding: 12px 20px; }
	.s5-tabs-underline .s5-tab-btn.active { color: #6366f1; background: transparent; }

	.s5-tabs-indicator {
		position: absolute;
		bottom: -2px;
		left: 0;
		height: 2px;
		background: #6366f1;
		transition: left 0.2s ease, width 0.2s ease;
	}
	.s5-tabs-indicator-vertical {
		bottom: auto;
		left: auto;
		top: 0;
		right: -2px;
		width: 2px;
		height: 0;
		transition: top 0.2s ease, height 0.2s ease;
	}

	.s5-tab-panel {
		padding: 16px 0;
		color: #334155;
		font-size: 0.95rem;
		line-height: 1.6;
		flex: 1;
	}
	.s5-tab-panel[hidden] { display: none; }
	.s5-tab-panel:focus-visible { outline: 2px solid #6366f1; outline-offset: 2px; border-radius: 4px; }
</style>
