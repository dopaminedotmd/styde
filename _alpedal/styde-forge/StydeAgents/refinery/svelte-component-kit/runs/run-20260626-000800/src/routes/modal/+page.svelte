<script lang="ts">
	/**
	 * Modal — SvelteKit Page Example
	 * =================================
	 * Demonstrates the Modal component with focus trapping,
	 * keyboard handling, and different configurations.
	 */

	import Modal from '$lib/components/Modal.svelte';

	let basicOpen = $state(false);
	let formOpen = $state(false);
	let noBackdropClose = $state(false);
	let largeOpen = $state(false);

	let formName = $state('');
	let formEmail = $state('');
	let formMessage = $state('');

	function submitForm() {
		alert(`Submitted: ${formName} (${formEmail})`);
		formOpen = false;
	}
</script>

<svelte:head>
	<title>Modal Example — Svelte 5 Component Kit</title>
</svelte:head>

<div class="page">
	<h1>Modal Component</h1>
	<p class="subtitle">
		An accessible modal dialog with focus trapping using Svelte 5 runes
		(<code>$state</code>, <code>$effect</code>).
	</p>

	<!-- Demo triggers -->
	<div class="demo-grid">
		<button class="demo-btn" onclick={() => (basicOpen = true)}>
			Basic Modal
		</button>
		<button class="demo-btn" onclick={() => (formOpen = true)}>
			Form Modal
		</button>
		<button class="demo-btn" onclick={() => (noBackdropClose = true)}>
			No Backdrop Close
		</button>
		<button class="demo-btn" onclick={() => (largeOpen = true)}>
			Large Modal
		</button>
	</div>

	<!-- Basic Modal -->
	<Modal bind:open={basicOpen} title="Welcome!">
		{#snippet children()}
			<p>This is a basic modal dialog built with Svelte 5.</p>
			<ul>
				<li>Press <kbd>Esc</kbd> to close</li>
				<li>Click the backdrop to close</li>
				<li><kbd>Tab</kbd> cycles through modal elements only</li>
				<li>Focus is restored to the trigger when closed</li>
			</ul>
		{/snippet}
	</Modal>

	<!-- Form Modal -->
	<Modal bind:open={formOpen} title="Contact Us">
		{#snippet children()}
			<form class="modal-form" onsubmit={(e) => { e.preventDefault(); submitForm(); }}>
				<label>
					Name
					<input type="text" bind:value={formName} placeholder="Your name" />
				</label>
				<label>
					Email
					<input type="email" bind:value={formEmail} placeholder="you@example.com" />
				</label>
				<label>
					Message
					<textarea bind:value={formMessage} placeholder="Your message…" rows="3"></textarea>
				</label>
			</form>
		{/snippet}
		{#snippet footer()}
			<button class="btn-secondary" onclick={() => (formOpen = false)}>Cancel</button>
			<button class="btn-primary" onclick={submitForm}>Send</button>
		{/snippet}
	</Modal>

	<!-- No Backdrop Close -->
	<Modal bind:open={noBackdropClose} title="Important Action" closeOnBackdrop={false}>
		{#snippet children()}
			<p>This modal cannot be closed by clicking the backdrop.</p>
			<p>You must use the close button or press <kbd>Esc</kbd>.</p>
		{/snippet}
	</Modal>

	<!-- Large Modal -->
	<Modal bind:open={largeOpen} title="Terms of Service" maxWidth="720px">
		{#snippet children()}
			<div class="large-content">
				<h3>1. Acceptance of Terms</h3>
				<p>By accessing this service, you agree to these terms and conditions…</p>
				<h3>2. User Responsibilities</h3>
				<p>You are responsible for maintaining the confidentiality of your account…</p>
				<h3>3. Content Guidelines</h3>
				<p>All content uploaded must comply with our community standards…</p>
				<h3>4. Termination</h3>
				<p>We reserve the right to terminate accounts that violate our policies…</p>
				<h3>5. Limitation of Liability</h3>
				<p>The service is provided "as is" without warranties of any kind…</p>
			</div>
		{/snippet}
		{#snippet footer()}
			<button class="btn-primary" onclick={() => (largeOpen = false)}>I Agree</button>
		{/snippet}
	</Modal>

	<div class="notes">
		<h2>Features Demonstrated</h2>
		<ul>
			<li>Focus trap — <kbd>Tab</kbd> and <kbd>Shift+Tab</kbd> cycle within the modal</li>
			<li>Close on <kbd>Escape</kbd> key</li>
			<li>Close on backdrop click (can be disabled)</li>
			<li>Body scroll lock while open</li>
			<li>Focus restoration to trigger element on close</li>
			<li>Named snippets (<code>children</code>, <code>footer</code>)</li>
			<li>ARIA attributes (<code>role="dialog"</code>, <code>aria-modal</code>, <code>aria-labelledby</code>)</li>
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
		margin-bottom: 24px;
		line-height: 1.6;
	}

	.subtitle code {
		background: #f1f5f9;
		padding: 1px 5px;
		border-radius: 3px;
		font-size: 0.85em;
	}

	.demo-grid {
		display: flex;
		gap: 10px;
		flex-wrap: wrap;
		margin-bottom: 32px;
	}

	.demo-btn {
		padding: 10px 20px;
		background: #6366f1;
		color: #fff;
		border: none;
		border-radius: 6px;
		font-size: 0.9rem;
		font-weight: 600;
		cursor: pointer;
		transition: background 0.15s;
		font-family: inherit;
	}
	.demo-btn:hover {
		background: #4f46e5;
	}

	.modal-form {
		display: flex;
		flex-direction: column;
		gap: 14px;
	}
	.modal-form label {
		display: flex;
		flex-direction: column;
		gap: 4px;
		font-size: 0.85rem;
		font-weight: 600;
		color: #374151;
	}
	.modal-form input,
	.modal-form textarea {
		padding: 8px 12px;
		border: 1px solid #d1d5db;
		border-radius: 6px;
		font-size: 0.9rem;
		outline: none;
		font-family: inherit;
	}
	.modal-form input:focus,
	.modal-form textarea:focus {
		border-color: #6366f1;
		box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
	}

	.btn-primary {
		padding: 8px 18px;
		background: #6366f1;
		color: #fff;
		border: none;
		border-radius: 6px;
		font-weight: 600;
		cursor: pointer;
		font-size: 0.9rem;
	}
	.btn-primary:hover {
		background: #4f46e5;
	}

	.btn-secondary {
		padding: 8px 18px;
		background: #fff;
		color: #475569;
		border: 1px solid #d1d5db;
		border-radius: 6px;
		cursor: pointer;
		font-size: 0.9rem;
	}
	.btn-secondary:hover {
		background: #f9fafb;
	}

	.large-content h3 {
		font-size: 1rem;
		color: #1e293b;
		margin-top: 16px;
		margin-bottom: 4px;
	}
	.large-content h3:first-child {
		margin-top: 0;
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
