<script lang="ts">
	import ToastContainer, { createToastStore } from '$lib/components/Toast.svelte';
	const toasts = createToastStore();
	if (typeof window !== 'undefined') (window as unknown as Record<string, unknown>).__toasts = toasts;

	function show(variant: 'info'|'success'|'warning'|'error') {
		toasts.add({ message: `${variant.charAt(0).toUpperCase() + variant.slice(1)} notification!`, variant, duration: 4000 });
	}

	function showWithAction() {
		toasts.add({
			message: 'File uploaded successfully!',
			variant: 'success',
			duration: 6000,
			action: { label: 'Undo', onClick: () => toasts.add({ message: 'Upload undone.', variant: 'info' }) }
		});
	}
</script>

<div class="page">
	<h1>🔔 Toast Component</h1>
	<p class="subtitle">v2: Proper timeout cleanup, action buttons, $inspect, and $host.</p>
	<div class="btn-group">
		<button class="btn-info" onclick={() => show('info')}>Info</button>
		<button class="btn-success" onclick={() => show('success')}>Success</button>
		<button class="btn-warning" onclick={() => show('warning')}>Warning</button>
		<button class="btn-error" onclick={() => show('error')}>Error</button>
		<button onclick={showWithAction}>With Action</button>
		<button onclick={() => toasts.clear()}>Clear All</button>
	</div>
	<ToastContainer store={toasts} position="bottom-right" maxVisible={5} />
</div>

<style>
	.page { padding: 24px 32px; max-width: 600px; }
	h1 { font-size: 1.5rem; margin: 0 0 4px; }
	.subtitle { color: #64748b; margin: 0 0 20px; font-size: 0.9rem; }
	.btn-group { display: flex; gap: 8px; flex-wrap: wrap; }
	.btn-group button {
		padding: 10px 20px; border: 1px solid #d1d5db; border-radius: 6px; background: #fff; cursor: pointer; font-size: 0.9rem;
	}
	.btn-info:hover { border-color: #6366f1; color: #6366f1; }
	.btn-success:hover { border-color: #22c55e; color: #22c55e; }
	.btn-warning:hover { border-color: #f59e0b; color: #f59e0b; }
	.btn-error:hover { border-color: #ef4444; color: #ef4444; }
</style>
