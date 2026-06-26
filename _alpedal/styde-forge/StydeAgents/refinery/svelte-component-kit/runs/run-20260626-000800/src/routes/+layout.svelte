<script lang="ts">
	import ToastContainer, { createToastStore } from '$lib/components/Toast.svelte';

	// Global toast store — shared across all pages
	const toasts = createToastStore();

	// Expose globally for demo purposes
	// In production, export from $lib/stores/toasts.ts instead
	if (typeof window !== 'undefined') {
		(window as unknown as Record<string, unknown>).__toasts = toasts;
	}
</script>

<nav class="demo-nav">
	<a href="/data-table">📊 DataTable</a>
	<a href="/form">📝 Form</a>
	<a href="/modal">🪟 Modal</a>
	<a href="/toast">🔔 Toast</a>
	<a href="/tabs">📑 Tabs</a>
</nav>

<main>
	{@render children?.()}
</main>

<ToastContainer store={toasts} position="bottom-right" maxVisible={5} />

<style>
	:global(body) {
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
		background: #fff;
		color: #1e293b;
		margin: 0;
	}

	.demo-nav {
		display: flex;
		gap: 4px;
		padding: 10px 20px;
		background: #f8fafc;
		border-bottom: 1px solid #e2e8f0;
		flex-wrap: wrap;
	}

	.demo-nav a {
		padding: 7px 14px;
		border-radius: 6px;
		text-decoration: none;
		color: #475569;
		font-size: 0.9rem;
		font-weight: 500;
		transition: all 0.15s;
	}
	.demo-nav a:hover {
		background: #eef2ff;
		color: #6366f1;
	}

	main {
		min-height: calc(100vh - 52px);
	}
</style>
