<script lang="ts">
	/**
	 * Modal — Svelte 5 Component
	 * ===========================
	 * An accessible modal dialog with focus trapping, built with Svelte 5 runes.
	 *
	 * ## Features
	 * - Focus trap: Tab cycles through only modal elements
	 * - Closes on Escape key
	 * - Closes on backdrop click (configurable)
	 * - ARIA dialog role, aria-modal, aria-labelledby
	 * - Restores focus to the trigger element on close
	 * - Animation via CSS transitions
	 * - Locks body scroll while open
	 *
	 * ## Usage
	 * ```svelte
	 * <script>
	 *   let open = $state(false);
	 * </script>
	 * <button onclick={() => open = true}>Open Modal</button>
	 * <Modal bind:open title="My Dialog">
	 *   <p>Modal content here.</p>
	 * </Modal>
	 * ```
	 *
	 * ## Runes Used
	 * - `$state`  — focusableElements
	 * - `$derived` — nothing derived needed
	 * - `$effect`  — focus trap lifecycle, body scroll lock, restore focus
	 */

	// ─── Props ──────────────────────────────────────────────────────
	interface Props {
		/** Controls modal visibility (two-way bind) */
		open: boolean;
		/** Modal title (displayed in header, used for aria-labelledby) */
		title?: string;
		/** ARIA label (if no visible title) */
		ariaLabel?: string;
		/** Close on backdrop click? Default: true */
		closeOnBackdrop?: boolean;
		/** Close on Escape? Default: true */
		closeOnEscape?: boolean;
		/** Show close button in header? Default: true */
		showClose?: boolean;
		/** Max width of the modal */
		maxWidth?: string;
		/** CSS class for the modal panel */
		class?: string;
		/** Children (slot) */
		children?: import('svelte').Snippet;
		/** Footer slot */
		footer?: import('svelte').Snippet;
	}

	let {
		open = $bindable(false),
		title = '',
		ariaLabel = '',
		closeOnBackdrop = true,
		closeOnEscape = true,
		showClose = true,
		maxWidth = '520px',
		class: className = '',
		children,
		footer
	}: Props = $props();

	// ─── State ──────────────────────────────────────────────────────
	let dialogEl = $state<HTMLDialogElement | null>(null);
	let previousActiveElement = $state<Element | null>(null);
	let titleId = $state(`s5-modal-title-${Math.random().toString(36).slice(2, 9)}`);

	// ─── Focus trap ─────────────────────────────────────────────────
	const FOCUSABLE_SELECTOR =
		'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])';

	function getFocusableElements(): HTMLElement[] {
		if (!dialogEl) return [];
		return Array.from(dialogEl.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTOR));
	}

	function trapFocus(e: KeyboardEvent) {
		if (e.key !== 'Tab') return;

		const focusable = getFocusableElements();
		if (focusable.length === 0) {
			e.preventDefault();
			return;
		}

		const first = focusable[0];
		const last = focusable[focusable.length - 1];

		if (e.shiftKey) {
			if (document.activeElement === first) {
				e.preventDefault();
				last.focus();
			}
		} else {
			if (document.activeElement === last) {
				e.preventDefault();
				first.focus();
			}
		}
	}

	function handleKeydown(e: KeyboardEvent) {
		trapFocus(e);

		if (closeOnEscape && e.key === 'Escape') {
			e.preventDefault();
			open = false;
		}
	}

	// ─── Body scroll lock ───────────────────────────────────────────
	$effect(() => {
		if (open) {
			previousActiveElement = document.activeElement;
			document.body.style.overflow = 'hidden';

			// Focus first focusable element or the dialog itself
			requestAnimationFrame(() => {
				const focusable = getFocusableElements();
				if (focusable.length > 0) {
					focusable[0].focus();
				} else if (dialogEl) {
					dialogEl.focus();
				}
			});

			return () => {
				document.body.style.overflow = '';
				// Restore focus
				if (previousActiveElement instanceof HTMLElement) {
					previousActiveElement.focus();
				}
			};
		}
	});

	function handleBackdropClick(e: MouseEvent) {
		if (closeOnBackdrop && e.target === dialogEl) {
			open = false;
		}
	}

	function close() {
		open = false;
	}
</script>

{#if open}
	<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
	<div
		class="s5-modal-backdrop"
		role="dialog"
		aria-modal="true"
		aria-labelledby={title ? titleId : undefined}
		aria-label={!title && ariaLabel ? ariaLabel : undefined}
		bind:this={dialogEl}
		onclick={handleBackdropClick}
		onkeydown={handleKeydown}
		tabindex="-1"
	>
		<div class="s5-modal-panel {className}" style="max-width: {maxWidth};" role="document">
			<!-- Header -->
			<div class="s5-modal-header">
				{#if title}
					<h2 id={titleId} class="s5-modal-title">{title}</h2>
				{:else}
					<span></span>
				{/if}
				{#if showClose}
					<button
						class="s5-modal-close"
						onclick={close}
						aria-label="Close dialog"
						type="button"
					>
						✕
					</button>
				{/if}
			</div>

			<!-- Body -->
			<div class="s5-modal-body">
				{#if children}
					{@render children()}
				{/if}
			</div>

			<!-- Footer -->
			{#if footer}
				<div class="s5-modal-footer">
					{@render footer()}
				</div>
			{/if}
		</div>
	</div>
{/if}

<style>
	.s5-modal-backdrop {
		position: fixed;
		inset: 0;
		z-index: 1000;
		display: flex;
		align-items: center;
		justify-content: center;
		background: rgba(0, 0, 0, 0.45);
		backdrop-filter: blur(3px);
		animation: s5-fade-in 0.2s ease-out;
		padding: 16px;
	}

	@keyframes s5-fade-in {
		from { opacity: 0; }
		to { opacity: 1; }
	}

	.s5-modal-panel {
		background: #fff;
		border-radius: 12px;
		box-shadow: 0 20px 60px rgba(0, 0, 0, 0.18);
		width: 100%;
		max-height: 85vh;
		display: flex;
		flex-direction: column;
		animation: s5-slide-up 0.2s ease-out;
		outline: none;
	}

	@keyframes s5-slide-up {
		from {
			opacity: 0;
			transform: translateY(12px) scale(0.98);
		}
		to {
			opacity: 1;
			transform: translateY(0) scale(1);
		}
	}

	.s5-modal-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 16px 20px;
		border-bottom: 1px solid #e2e8f0;
		flex-shrink: 0;
	}

	.s5-modal-title {
		margin: 0;
		font-size: 1.1rem;
		font-weight: 700;
		color: #1e293b;
	}

	.s5-modal-close {
		width: 32px;
		height: 32px;
		border: none;
		background: transparent;
		font-size: 1.1rem;
		color: #94a3b8;
		cursor: pointer;
		border-radius: 6px;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: all 0.15s;
	}
	.s5-modal-close:hover {
		background: #f1f5f9;
		color: #475569;
	}
	.s5-modal-close:focus-visible {
		outline: 2px solid #6366f1;
		outline-offset: 2px;
	}

	.s5-modal-body {
		padding: 20px;
		overflow-y: auto;
		flex: 1;
		color: #334155;
		font-size: 0.95rem;
		line-height: 1.6;
	}

	.s5-modal-footer {
		padding: 12px 20px;
		border-top: 1px solid #e2e8f0;
		display: flex;
		justify-content: flex-end;
		gap: 8px;
		flex-shrink: 0;
	}
</style>
