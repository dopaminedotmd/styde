<script lang="ts">
	import ToastContainer, { createToastStore } from '$lib/components/Toast.svelte';
	import { createThemeStore } from '$lib/stores/reactive.svelte.ts';

	const toasts = createToastStore();
	const theme = createThemeStore();

	if (typeof window !== 'undefined') {
		(window as unknown as Record<string, unknown>).__toasts = toasts;
		(window as unknown as Record<string, unknown>).__theme = theme;
	}
</script>

<nav class="demo-nav">
	<a href="/data-table">📊 DataTable</a>
	<a href="/form">📝 Form</a>
	<a href="/modal">🪟 Modal</a>
	<a href="/toast">🔔 Toast</a>
	<a href="/tabs">📑 Tabs</a>
	<a href="/accordion">🪗 Accordion</a>
	<a href="/command-palette">⌘ CmdPalette</a>
	<a href="/tree-view">🌳 TreeView</a>
	<a href="/infinite-scroll">∞ InfScroll</a>
	<button
		class="demo-theme-btn"
		onclick={() => theme.toggle()}
		aria-label="Toggle theme"
		type="button"
	>
		{theme.isDark ? '☀️' : '🌙'}
	</button>
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
	:global(body.dark) {
		background: #0f172a;
		color: #e2e8f0;
	}

	.demo-nav {
		display: flex;
		gap: 4px;
		padding: 10px 20px;
		background: #f8fafc;
		border-bottom: 1px solid #e2e8f0;
		flex-wrap: wrap;
		align-items: center;
	}
	:global(body.dark) .demo-nav {
		background: #1e293b;
		border-bottom-color: #334155;
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
	.demo-nav a:hover { background: #eef2ff; color: #6366f1; }

	.demo-theme-btn {
		margin-left: auto;
		padding: 6px 10px;
		border: 1px solid #e2e8f0;
		border-radius: 6px;
		background: #fff;
		cursor: pointer;
		font-size: 1.1rem;
		transition: all 0.15s;
	}
	.demo-theme-btn:hover { background: #f1f5f9; }

	main { min-height: calc(100vh - 52px); }
</style>
