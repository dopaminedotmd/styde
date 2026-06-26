<script lang="ts">
	import Tabs from '$lib/components/Tabs.svelte';
	import type { TabItem } from '$lib/types';

	const items: TabItem[] = [
		{ id: 'overview', label: 'Overview', icon: '📋' },
		{ id: 'details', label: 'Details', badge: 4, icon: '📄' },
		{ id: 'settings', label: 'Settings', icon: '⚙️', disabled: false },
		{ id: 'security', label: 'Security', icon: '🔒' },
	];

	let active = $state('overview');
	let variant = $state<'default'|'pills'|'underline'>('underline');
</script>

<div class="page">
	<h1>📑 Tabs Component</h1>
	<p class="subtitle">v2: Icons, vertical layout, lazy panels, $inspect, and $host.</p>
	<div class="controls">
		<label>Variant:
			<select bind:value={variant}>
				<option value="default">Default</option>
				<option value="pills">Pills</option>
				<option value="underline">Underline</option>
			</select>
		</label>
	</div>
	<Tabs {items} bind:active {variant}>
		<slot name="overview"><p>Welcome to the overview tab!</p></slot>
		<slot name="details"><p>Details: you have 4 unread notifications.</p></slot>
		<slot name="settings"><p>Configure your preferences here.</p></slot>
		<slot name="security"><p>2FA is enabled. Last login: today.</p></slot>
	</Tabs>
</div>

<style>
	.page { padding: 24px 32px; max-width: 600px; }
	h1 { font-size: 1.5rem; margin: 0 0 4px; }
	.subtitle { color: #64748b; margin: 0 0 20px; font-size: 0.9rem; }
	.controls { margin-bottom: 16px; }
	.controls select { padding: 4px 8px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 0.85rem; }
</style>
