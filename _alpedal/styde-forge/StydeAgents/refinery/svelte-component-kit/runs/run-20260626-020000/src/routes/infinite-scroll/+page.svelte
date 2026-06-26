<script lang="ts">
	import InfiniteScroll from '$lib/components/InfiniteScroll.svelte';

	let items = $state<{ id: number; text: string }[]>([]);
	let loading = $state(false);
	let hasMore = $state(true);
	let page = $state(0);
	let error = $state<string | null>(null);

	function generateItems(p: number) {
		const start = p * 20;
		return Array.from({ length: 20 }, (_, i) => ({
			id: start + i + 1,
			text: `Item #${start + i + 1}: ${Math.random().toString(36).slice(2, 8)}`
		}));
	}

	async function loadMore() {
		loading = true;
		error = null;
		try {
			await new Promise((r) => setTimeout(r, 800));
			items = [...items, ...generateItems(page)];
			page++;
			if (page >= 5) hasMore = false;
		} catch (e) {
			error = 'Failed to load items.';
		} finally {
			loading = false;
		}
	}
</script>

<div class="page">
	<h1>∞ Infinite Scroll</h1>
	<p class="subtitle">New c2: IntersectionObserver via $effect, snippet slots, $host, $inspect.</p>
	<p class="info">Scroll down to load more items. Uses IntersectionObserver with 100px root margin.</p>

	<InfiniteScroll onLoadMore={loadMore} {hasMore} {loading} {error}>
		{#each items as item (item.id)}
			<div class="item">{item.text}</div>
		{/each}
	</InfiniteScroll>

	{#if items.length > 0}
		<p class="count">{items.length} items loaded</p>
	{/if}
</div>

<style>
	.page { padding: 24px 32px; max-width: 500px; }
	h1 { font-size: 1.5rem; margin: 0 0 4px; }
	.subtitle { color: #64748b; margin: 0 0 12px; font-size: 0.9rem; }
	.info { color: #94a3b8; font-size: 0.85rem; margin-bottom: 16px; }
	.item {
		padding: 12px 16px; border: 1px solid #e2e8f0; border-radius: 6px;
		background: #fff; font-size: 0.9rem; color: #334155;
	}
	.count { text-align: center; color: #94a3b8; font-size: 0.8rem; margin-top: 12px; }
</style>
