<script lang="ts">
	/**
	 * Accordion — Svelte 5 Advanced Component
	 * =========================================
	 * An accessible accordion/disclosure component using Svelte 5 runes,
	 * snippet blocks for custom headers/panels, and $host for DOM access.
	 *
	 * ## Features
	 * - Single or multi-expand mode
	 * - Keyboard navigation: Enter/Space to toggle
	 * - ARIA: region, button with aria-expanded, aria-controls
	 * - Smooth height animation via CSS grid trick
	 * - Snippet slots: `title(item)` and `content(item)` for custom rendering
	 * - $host reference to the accordion container
	 * - $inspect debugging
	 * - $effect for animation lifecycle
	 */

	import type { AccordionItem } from '../types';

	interface Props {
		items: AccordionItem[];
		/** Allow multiple items expanded simultaneously */
		multiple?: boolean;
		/** CSS class */
		class?: string;
		/** Snippet: custom title rendering */
		title?: (item: AccordionItem) => import('svelte').Snippet;
		/** Snippet: custom content rendering */
		content?: (item: AccordionItem) => import('svelte').Snippet;
	}

	let {
		items,
		multiple = false,
		class: className = '',
		title,
		content
	}: Props = $props();

	// Initialize expanded state from item defaults
	function initExpanded(): Set<string> {
		const expanded = new Set<string>();
		for (const item of items) {
			if (item.expanded) expanded.add(item.id);
		}
		return expanded;
	}

	let expandedIds = $state<Set<string>>(initExpanded());
	let accordionEl = $host<HTMLDivElement>();

	// $inspect — trace in dev mode
	$inspect('Accordion expanded:', [...expandedIds]);

	function toggle(id: string) {
		const item = items.find((i) => i.id === id);
		if (item?.disabled) return;

		const next = new Set(expandedIds);
		if (next.has(id)) {
			next.delete(id);
		} else {
			if (!multiple) next.clear();
			next.add(id);
		}
		expandedIds = next;
	}

	function isExpanded(id: string): boolean {
		return expandedIds.has(id);
	}

	function handleKeydown(e: KeyboardEvent, id: string) {
		if (e.key === 'Enter' || e.key === ' ') {
			e.preventDefault();
			toggle(id);
		}
	}
</script>

<div class="s5-accordion {className}" bind:this={accordionEl}>
	{#each items as item}
		<div class="s5-accordion-item" class:s5-accordion-expanded={isExpanded(item.id)} class:s5-accordion-disabled={item.disabled}>
			<button
				class="s5-accordion-trigger"
				aria-expanded={isExpanded(item.id)}
				aria-controls="s5-accordion-panel-{item.id}"
				disabled={item.disabled}
				onclick={() => toggle(item.id)}
				onkeydown={(e) => handleKeydown(e, item.id)}
				type="button"
			>
				<span class="s5-accordion-trigger-content">
					{#if title}
						{@render title(item)}
					{:else}
						<span class="s5-accordion-trigger-icon">{item.icon ?? '▸'}</span>
						<span class="s5-accordion-trigger-label">{item.title}</span>
					{/if}
				</span>
				<span class="s5-accordion-chevron" aria-hidden="true">▾</span>
			</button>

			<div
				id="s5-accordion-panel-{item.id}"
				class="s5-accordion-panel"
				role="region"
				aria-labelledby="s5-accordion-trigger-{item.id}"
				hidden={!isExpanded(item.id)}
			>
				<div class="s5-accordion-panel-inner">
					{#if content}
						{@render content(item)}
					{:else}
						<slot name={item.id} />
					{/if}
				</div>
			</div>
		</div>
	{/each}
</div>

<style>
	.s5-accordion {
		border: 1px solid #e2e8f0;
		border-radius: 8px;
		overflow: hidden;
		background: #fff;
	}

	.s5-accordion-item {
		border-bottom: 1px solid #e2e8f0;
	}
	.s5-accordion-item:last-child {
		border-bottom: none;
	}

	.s5-accordion-trigger {
		display: flex;
		align-items: center;
		justify-content: space-between;
		width: 100%;
		padding: 14px 18px;
		border: none;
		background: transparent;
		font-size: 0.95rem;
		font-weight: 500;
		color: #1e293b;
		cursor: pointer;
		text-align: left;
		transition: background 0.15s;
		font-family: inherit;
	}
	.s5-accordion-trigger:hover:not(:disabled) {
		background: #f8fafc;
	}
	.s5-accordion-trigger:focus-visible {
		outline: 2px solid #6366f1;
		outline-offset: -2px;
	}
	.s5-accordion-trigger:disabled {
		opacity: 0.4;
		cursor: not-allowed;
	}

	.s5-accordion-trigger-content {
		display: flex;
		align-items: center;
		gap: 10px;
	}
	.s5-accordion-trigger-icon {
		font-size: 1.1rem;
		transition: transform 0.2s;
		display: inline-block;
	}
	.s5-accordion-expanded .s5-accordion-trigger-icon {
		transform: rotate(90deg);
	}
	.s5-accordion-trigger-label {
		font-weight: 600;
	}

	.s5-accordion-chevron {
		font-size: 0.8rem;
		color: #94a3b8;
		transition: transform 0.2s;
	}
	.s5-accordion-expanded .s5-accordion-chevron {
		transform: rotate(180deg);
	}

	.s5-accordion-panel {
		overflow: hidden;
		transition: grid-template-rows 0.3s ease;
		display: grid;
		grid-template-rows: 0fr;
	}
	.s5-accordion-panel[hidden] {
		display: grid;
		grid-template-rows: 0fr;
	}
	.s5-accordion-expanded .s5-accordion-panel {
		grid-template-rows: 1fr;
	}

	.s5-accordion-panel-inner {
		overflow: hidden;
		padding: 0 18px;
	}
	.s5-accordion-expanded .s5-accordion-panel-inner {
		padding: 0 18px 16px;
	}
</style>
