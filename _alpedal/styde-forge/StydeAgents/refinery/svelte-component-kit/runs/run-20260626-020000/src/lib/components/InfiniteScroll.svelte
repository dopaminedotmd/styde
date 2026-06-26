<script lang="ts">
	/**
	 * InfiniteScroll — Svelte 5 Advanced Component
	 * ==============================================
	 * Infinite scroll / "load more" container using Svelte 5 runes.
	 * Uses IntersectionObserver via $effect, $host, and snippet slots.
	 *
	 * ## Features
	 * - IntersectionObserver via $effect with proper cleanup
	 * - Loading spinner and "no more" states
	 * - Configurable threshold and root margin
	 * - Reverse scroll (chat-style) support
	 * - $inspect debugging for load state
	 * - $host for sentinel element
	 * - Snippet slots: loading, empty, end states
	 * - $effect cleanup on unmount
	 *
	 * ## Usage
	 * ```svelte
	 * <InfiniteScroll onLoadMore={loadMore} hasMore={hasMore} loading={loading}>
	 *   {#each items as item}<div>{item}</div>{/each}
	 * </InfiniteScroll>
	 * ```
	 */

	import type { InfiniteScrollState } from '../types';

	interface Props {
		/** Called when more items should be loaded */
		onLoadMore: () => void | Promise<void>;
		/** Whether there are more items */
		hasMore: boolean;
		/** Currently loading? */
		loading?: boolean;
		/** Error message if load failed */
		error?: string | null;
		/** IntersectionObserver threshold (0-1) */
		threshold?: number;
		/** IntersectionObserver rootMargin */
		rootMargin?: string;
		/** Reverse direction (new items at top, for chat) */
		reverse?: boolean;
		/** CSS class */
		class?: string;
		/** Snippet: custom loading */
		loadingSnippet?: import('svelte').Snippet;
		/** Snippet: custom end-of-list */
		endSnippet?: import('svelte').Snippet;
		/** Snippet: custom empty state */
		emptySnippet?: import('svelte').Snippet;
		/** Snippet: custom error state */
		errorSnippet?: import('svelte').Snippet;
		children?: import('svelte').Snippet;
	}

	let {
		onLoadMore,
		hasMore,
		loading = false,
		error = null,
		threshold = 0.1,
		rootMargin = '100px',
		reverse = false,
		class: className = '',
		loadingSnippet,
		endSnippet,
		emptySnippet,
		errorSnippet,
		children
	}: Props = $props();

	let sentinelEl = $host<HTMLDivElement>();
	let containerEl = $state<HTMLDivElement | null>(null);
	let hasLoadedOnce = $state(false);

	// $inspect
	$inspect('InfiniteScroll loading:', loading);
	$inspect('InfiniteScroll hasMore:', hasMore);
	$inspect('InfiniteScroll error:', error);

	// IntersectionObserver via $effect with proper cleanup
	$effect(() => {
		if (typeof IntersectionObserver === 'undefined') return;
		if (!sentinelEl) return;

		const observer = new IntersectionObserver(
			(entries) => {
				const entry = entries[0];
				if (entry?.isIntersecting && hasMore && !loading && !error) {
					hasLoadedOnce = true;
					onLoadMore();
				}
			},
			{ threshold, rootMargin }
		);

		observer.observe(sentinelEl);

		return () => {
			observer.disconnect();
		};
	});
</script>

<div class="s5-iscroll-container {className}" class:s5-iscroll-reverse={reverse} bind:this={containerEl}>
	{#if reverse && children}
		<!-- Sentinal at top for reverse scroll -->
		<div class="s5-iscroll-sentinel" bind:this={sentinelEl}></div>
	{/if}

	{#if reverse && loading}
		<div class="s5-iscroll-loading">
			{#if loadingSnippet}{@render loadingSnippet()}
			{:else}<span class="s5-iscroll-spinner"></span> Loading…
			{/if}
		</div>
	{/if}

	{#if error}
		<div class="s5-iscroll-error">
			{#if errorSnippet}{@render errorSnippet()}
			{:else}
				<span class="s5-iscroll-error-icon">⚠</span>
				{error}
				<button class="s5-iscroll-retry-btn" onclick={onLoadMore} type="button">Retry</button>
			{/if}
		</div>
	{/if}

	{#if !hasLoadedOnce && !loading && !error && !hasMore}
		<div class="s5-iscroll-empty">
			{#if emptySnippet}{@render emptySnippet()}
			{:else}No items to display.{/if}
		</div>
	{/if}

	<div class="s5-iscroll-content">
		{#if children}
			{@render children()}
		{/if}
	</div>

	{#if !reverse && loading}
		<div class="s5-iscroll-loading">
			{#if loadingSnippet}{@render loadingSnippet()}
			{:else}<span class="s5-iscroll-spinner"></span> Loading…
			{/if}
		</div>
	{/if}

	{#if !reverse && !hasMore && hasLoadedOnce}
		<div class="s5-iscroll-end">
			{#if endSnippet}{@render endSnippet()}
			{:else}— End of list —{/if}
		</div>
	{/if}

	{#if !reverse}
		<!-- Sentinel at bottom for forward scroll -->
		<div class="s5-iscroll-sentinel" bind:this={sentinelEl}></div>
	{/if}
</div>

<style>
	.s5-iscroll-container {
		overflow-y: auto;
		max-height: 60vh;
	}

	.s5-iscroll-content {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.s5-iscroll-sentinel {
		height: 1px;
	}

	.s5-iscroll-loading {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 8px;
		padding: 16px;
		color: #94a3b8;
		font-size: 0.85rem;
	}

	.s5-iscroll-spinner {
		display: inline-block;
		width: 16px;
		height: 16px;
		border: 2px solid #e2e8f0;
		border-top-color: #6366f1;
		border-radius: 50%;
		animation: s5-iscroll-spin 0.6s linear infinite;
	}
	@keyframes s5-iscroll-spin {
		to { transform: rotate(360deg); }
	}

	.s5-iscroll-end {
		padding: 20px;
		text-align: center;
		color: #cbd5e1;
		font-size: 0.85rem;
	}

	.s5-iscroll-empty {
		padding: 32px;
		text-align: center;
		color: #94a3b8;
		font-size: 0.9rem;
	}

	.s5-iscroll-error {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 8px;
		padding: 12px;
		background: #fef2f2;
		color: #b91c1c;
		border-radius: 6px;
		font-size: 0.85rem;
		margin: 8px;
	}
	.s5-iscroll-error-icon { font-size: 1rem; }
	.s5-iscroll-retry-btn {
		padding: 4px 10px;
		border: 1px solid #b91c1c;
		border-radius: 4px;
		background: transparent;
		color: #b91c1c;
		cursor: pointer;
		font-size: 0.8rem;
		font-weight: 600;
		transition: all 0.15s;
	}
	.s5-iscroll-retry-btn:hover { background: #b91c1c; color: #fff; }
</style>
