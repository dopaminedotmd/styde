<script lang="ts">
	/**
	 * Tabs — SvelteKit Page Example
	 * ==============================
	 * Demonstrates the Tabs component with keyboard navigation,
	 * multiple variants, badges, and named snippets.
	 */

	import Tabs from '$lib/components/Tabs.svelte';
	import type { TabItem } from '$lib/types';

	const items: TabItem[] = [
		{ id: 'overview', label: 'Overview' },
		{ id: 'details', label: 'Details', badge: 3 },
		{ id: 'settings', label: 'Settings' },
		{ id: 'billing', label: 'Billing' },
		{ id: 'disabled', label: 'Disabled', disabled: true },
	];

	const pillItems: TabItem[] = [
		{ id: 'all', label: 'All', badge: 42 },
		{ id: 'active', label: 'Active' },
		{ id: 'archived', label: 'Archived' },
	];

	let activeTab = $state('overview');
	let pillTab = $state('all');
	let underlineTab = $state('tab1');

	// Track tab changes
	function handleTabChange(id: string) {
		console.log('Tab changed to:', id);
	}
</script>

<svelte:head>
	<title>Tabs Example — Svelte 5 Component Kit</title>
</svelte:head>

<div class="page">
	<h1>Tabs Component</h1>
	<p class="subtitle">
		An accessible tab panel with keyboard navigation using Svelte 5 runes
		(<code>$state</code>, <code>$derived</code>, <code>$effect</code>).
	</p>

	<!-- Default variant -->
	<section class="demo-section">
		<h2>Default Variant</h2>
		<p>Classic tabbed interface with bottom border highlight.</p>

		<Tabs items={items} bind:active={activeTab} onChange={handleTabChange}>
			{#snippet children('overview')}
				<p>Welcome to the project dashboard! Here's a quick summary:</p>
				<ul>
					<li><strong>42</strong> total tasks</li>
					<li><strong>15</strong> in progress</li>
					<li><strong>8</strong> overdue</li>
				</ul>
			{/snippet}

			{#snippet children('details')}
				<p>Detailed information about the selected item.</p>
				<table class="info-table">
					<tr><td>Created</td><td>June 1, 2026</td></tr>
					<tr><td>Last modified</td><td>June 24, 2026</td></tr>
					<tr><td>Owner</td><td>Alice Johnson</td></tr>
					<tr><td>Status</td><td><span class="badge-active">Active</span></td></tr>
				</table>
			{/snippet}

			{#snippet children('settings')}
				<p>Configure your preferences here. This tab demonstrates that content
				is preserved in the DOM but hidden with <code>[hidden]</code> when inactive.</p>
			{/snippet}

			{#snippet children('billing')}
				<p>Billing and subscription management.</p>
				<div class="billing-card">
					<p><strong>Current Plan:</strong> Pro</p>
					<p><strong>Next Billing:</strong> July 15, 2026</p>
					<p><strong>Amount:</strong> $29.00/month</p>
				</div>
			{/snippet}

			{#snippet children('disabled')}
				<p>This tab is disabled — you shouldn't be able to reach this content via keyboard or click.</p>
			{/snippet}
		</Tabs>
	</section>

	<!-- Pills variant -->
	<section class="demo-section">
		<h2>Pills Variant</h2>
		<p>Pill-style tabs with a filled background on the active tab.</p>

		<Tabs items={pillItems} bind:active={pillTab} variant="pills">
			{#snippet children('all')}
				<p>Showing all 42 items. Use the tabs to filter.</p>
			{/snippet}
			{#snippet children('active')}
				<p>Showing active items only.</p>
			{/snippet}
			{#snippet children('archived')}
				<p>Showing archived items only.</p>
			{/snippet}
		</Tabs>
	</section>

	<!-- Underline variant -->
	<section class="demo-section">
		<h2>Underline Variant</h2>
		<p>Tabs with an animated underline indicator that slides between tabs.</p>

		<Tabs
			items={[
				{ id: 'tab1', label: 'General' },
				{ id: 'tab2', label: 'Security' },
				{ id: 'tab3', label: 'Notifications' },
			]}
			bind:active={underlineTab}
			variant="underline"
		>
			{#snippet children('tab1')}
				<p>General account settings.</p>
			{/snippet}
			{#snippet children('tab2')}
				<p>Security and password settings.</p>
			{/snippet}
			{#snippet children('tab3')}
				<p>Notification preferences.</p>
			{/snippet}
		</Tabs>
	</section>

	<div class="notes">
		<h2>Features Demonstrated</h2>
		<ul>
			<li>Keyboard navigation: <kbd>←</kbd> <kbd>→</kbd> <kbd>Home</kbd> <kbd>End</kbd></li>
			<li>Three variants: default, pills, underline</li>
			<li>Animated underline indicator (CSS transition)</li>
			<li>Badge counts on tab labels</li>
			<li>Disabled tabs</li>
			<li>Svelte 5 named snippets for tab content</li>
			<li>ARIA: <code>role="tablist"</code>, <code>role="tab"</code>, <code>role="tabpanel"</code></li>
		</ul>
	</div>
</div>

<style>
	.page {
		max-width: 720px;
		margin: 0 auto;
		padding: 32px 20px;
	}

	h1 {
		font-size: 1.8rem;
		color: #1e293b;
		margin-bottom: 6px;
	}

	.subtitle {
		color: #64748b;
		margin-bottom: 32px;
		line-height: 1.6;
	}

	.subtitle code {
		background: #f1f5f9;
		padding: 1px 5px;
		border-radius: 3px;
		font-size: 0.85em;
	}

	.demo-section {
		margin-bottom: 36px;
	}
	.demo-section h2 {
		font-size: 1.2rem;
		color: #1e293b;
		margin-bottom: 4px;
	}
	.demo-section > p {
		color: #64748b;
		font-size: 0.9rem;
		margin-bottom: 12px;
	}

	.info-table {
		width: 100%;
		border-collapse: collapse;
		margin-top: 8px;
	}
	.info-table td {
		padding: 8px 12px;
		border-bottom: 1px solid #f1f5f9;
		font-size: 0.9rem;
	}
	.info-table td:first-child {
		font-weight: 600;
		color: #64748b;
		width: 140px;
	}

	.badge-active {
		background: #dcfce7;
		color: #15803d;
		padding: 2px 8px;
		border-radius: 10px;
		font-size: 0.8rem;
		font-weight: 600;
	}

	.billing-card {
		background: #f8fafc;
		border: 1px solid #e2e8f0;
		border-radius: 8px;
		padding: 14px 18px;
		margin-top: 8px;
	}
	.billing-card p {
		margin: 4px 0;
		font-size: 0.9rem;
	}

	.notes {
		margin-top: 32px;
		padding: 16px 20px;
		background: #f8fafc;
		border-radius: 8px;
		border: 1px solid #e2e8f0;
	}

	.notes h2 {
		font-size: 1.1rem;
		margin-bottom: 10px;
		color: #334155;
	}

	.notes ul {
		padding-left: 20px;
		color: #475569;
		font-size: 0.9rem;
		line-height: 1.8;
	}

	.notes code, kbd {
		background: #e2e8f0;
		padding: 1px 5px;
		border-radius: 3px;
		font-size: 0.85em;
	}
</style>
