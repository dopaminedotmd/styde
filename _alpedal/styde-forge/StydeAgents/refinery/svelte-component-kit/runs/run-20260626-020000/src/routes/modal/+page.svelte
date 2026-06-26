<script lang="ts">
	import Modal from '$lib/components/Modal.svelte';
	let showModal = $state(false);
	let showLarge = $state(false);
	let showConfirm = $state(false);

	async function confirmClose(): Promise<boolean> {
		return confirm('Discard changes?');
	}
</script>

<div class="page">
	<h1>🪟 Modal Component</h1>
	<p class="subtitle">v2: Stacked modals, preset sizes, $host, beforeClose guard, and $inspect.</p>

	<div class="btn-group">
		<button onclick={() => showModal = true}>Open Default</button>
		<button onclick={() => showLarge = true}>Open Large</button>
		<button onclick={() => showConfirm = true}>Open with Guard</button>
	</div>

	<Modal bind:open={showModal} title="Default Modal" size="md">
		{#snippet children()}<p>This is a medium modal using snippet blocks.</p>{/snippet}
		{#snippet footer()}
			<button class="btn-secondary" onclick={() => showModal = false}>Cancel</button>
			<button class="btn-primary" onclick={() => showModal = false}>Confirm</button>
		{/snippet}
	</Modal>

	<Modal bind:open={showLarge} title="Large Modal" size="lg">
		{#snippet children()}<p>A larger modal for more content. Up to 720px wide.</p>{/snippet}
	</Modal>

	<Modal bind:open={showConfirm} title="Confirm Close" beforeClose={confirmClose}>
		{#snippet children()}<p>Try closing — you'll be prompted first!</p>{/snippet}
	</Modal>
</div>

<style>
	.page { padding: 24px 32px; max-width: 600px; }
	h1 { font-size: 1.5rem; margin: 0 0 4px; }
	.subtitle { color: #64748b; margin: 0 0 20px; font-size: 0.9rem; }
	.btn-group { display: flex; gap: 8px; flex-wrap: wrap; }
	.btn-group button {
		padding: 10px 20px; border: 1px solid #d1d5db; border-radius: 6px;
		background: #fff; cursor: pointer; font-size: 0.9rem; transition: all 0.15s;
	}
	.btn-group button:hover { background: #f1f5f9; border-color: #6366f1; color: #6366f1; }
	.btn-primary { background: #6366f1 !important; color: #fff !important; border-color: #6366f1 !important; }
	.btn-secondary { background: #fff; color: #475569; }
</style>
