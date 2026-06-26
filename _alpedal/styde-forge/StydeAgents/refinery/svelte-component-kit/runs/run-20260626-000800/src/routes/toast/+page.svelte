<script lang="ts">
	/**
	 * Toast — SvelteKit Page Example
	 * ================================
	 * Demonstrates the Toast notification system with all variants,
	 * positions, and auto-dismiss.
	 *
	 * Note: In a real app, the ToastContainer would live in +layout.svelte
	 * and the store would be imported from a shared module.
	 */

	import ToastContainer, { createToastStore } from '$lib/components/Toast.svelte';

	// In production, initialize the store once in a module and share it:
	// import { toasts } from '$lib/stores/toasts';
	const toasts = createToastStore();

	let message = $state('This is a notification!');
	let duration = $state(4000);
	let dismissible = $state(true);

	function show(variant: 'info' | 'success' | 'warning' | 'error') {
		toasts.add({
			message: message || 'No message provided.',
			variant,
			duration,
			dismissible,
		});
	}
</script>

<svelte:head>
	<title>Toast Example — Svelte 5 Component Kit</title>
</svelte:head>

<div class="page">
	<h1>Toast Notifications</h1>
	<p class="subtitle">
		A toast notification system with auto-dismiss and progress bar
		using Svelte 5 runes (<code>$state</code>, <code>$derived</code>, <code>$effect</code>).
	</p>

	<!-- Controls -->
	<div class="controls">
		<label>
			Message:
			<input
				type="text"
				bind:value={message}
				placeholder="Toast message…"
				class="control-input"
			/>
		</label>

		<label>
			Duration (ms):
			<select bind:value={duration}>
				<option value={2000}>2s</option>
				<option value={4000}>4s</option>
				<option value={8000}>8s</option>
				<option value={0}>Sticky</option>
			</select>
		</label>

		<label class="checkbox-label">
			<input type="checkbox" bind:checked={dismissible} />
			Dismissible
		</label>
	</div>

	<!-- Variant buttons -->
	<div class="btn-grid">
		<button class="toast-btn toast-btn-info" onclick={() => show('info')}>
			ℹ Info
		</button>
		<button class="toast-btn toast-btn-success" onclick={() => show('success')}>
			✓ Success
		</button>
		<button class="toast-btn toast-btn-warning" onclick={() => show('warning')}>
			⚠ Warning
		</button>
		<button class="toast-btn toast-btn-error" onclick={() => show('error')}>
			✕ Error
		</button>
	</div>

	<div class="btn-grid" style="margin-top: 8px;">
		<button class="toast-btn toast-btn-multi" onclick={() => {
			toasts.add({ message: 'First notification', variant: 'info', duration: 6000 });
			setTimeout(() => toasts.add({ message: 'Second one!', variant: 'success', duration: 4000 }), 200);
			setTimeout(() => toasts.add({ message: 'And a third!', variant: 'warning', duration: 5000 }), 400);
		}}>
			Stack 3 toasts
		</button>
		<button class="toast-btn toast-btn-clear" onclick={() => toasts.clear()}>
			Clear All
		</button>
	</div>

	<!-- Toast Container (in a real app this would be in +layout.svelte) -->
	<ToastContainer store={toasts} position="bottom-right" maxVisible={5} />

	<div class="notes">
		<h2>Features Demonstrated</h2>
		<ul>
			<li>Four variants: info, success, warning, error</li>
			<li>Auto-dismiss with configurable duration and progress bar</li>
			<li>Sticky toasts (duration = 0)</li>
			<li>Manual dismiss button</li>
			<li>Stacked rendering with max visible limit</li>
			<li>Slide-in animation</li>
			<li>ARIA live regions (<code>role="status"</code> / <code>role="alert"</code>)</li>
		</ul>
	</div>
</div>

<style>
	.page {
		max-width: 640px;
		margin: 0 auto;
		padding: 32px 20px 120px;
	}

	h1 {
		font-size: 1.8rem;
		color: #1e293b;
		margin-bottom: 6px;
	}

	.subtitle {
		color: #64748b;
		margin-bottom: 24px;
		line-height: 1.6;
	}

	.subtitle code {
		background: #f1f5f9;
		padding: 1px 5px;
		border-radius: 3px;
		font-size: 0.85em;
	}

	.controls {
		display: flex;
		gap: 16px;
		flex-wrap: wrap;
		margin-bottom: 20px;
		align-items: center;
		font-size: 0.9rem;
		color: #475569;
	}

	.control-input {
		margin-left: 6px;
		padding: 6px 10px;
		border: 1px solid #d1d5db;
		border-radius: 4px;
		font-size: 0.9rem;
		width: 240px;
		font-family: inherit;
	}

	.controls select {
		margin-left: 6px;
		padding: 4px 8px;
		border: 1px solid #d1d5db;
		border-radius: 4px;
		font-size: 0.9rem;
	}

	.checkbox-label {
		display: flex;
		align-items: center;
		gap: 6px;
		cursor: pointer;
	}

	.btn-grid {
		display: flex;
		gap: 8px;
		flex-wrap: wrap;
	}

	.toast-btn {
		padding: 10px 20px;
		border: none;
		border-radius: 6px;
		font-size: 0.9rem;
		font-weight: 600;
		cursor: pointer;
		transition: background 0.15s;
		font-family: inherit;
	}

	.toast-btn-info    { background: #eef2ff; color: #6366f1; }
	.toast-btn-info:hover    { background: #e0e7ff; }
	.toast-btn-success { background: #f0fdf4; color: #22c55e; }
	.toast-btn-success:hover { background: #dcfce7; }
	.toast-btn-warning { background: #fffbeb; color: #f59e0b; }
	.toast-btn-warning:hover { background: #fef3c7; }
	.toast-btn-error   { background: #fef2f2; color: #ef4444; }
	.toast-btn-error:hover   { background: #fee2e2; }
	.toast-btn-multi   { background: #f8fafc; color: #475569; border: 1px solid #e2e8f0; }
	.toast-btn-multi:hover   { background: #f1f5f9; }
	.toast-btn-clear   { background: #fff; color: #ef4444; border: 1px solid #fecaca; }
	.toast-btn-clear:hover   { background: #fef2f2; }

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

	.notes code {
		background: #e2e8f0;
		padding: 1px 4px;
		border-radius: 3px;
		font-size: 0.85em;
	}
</style>
