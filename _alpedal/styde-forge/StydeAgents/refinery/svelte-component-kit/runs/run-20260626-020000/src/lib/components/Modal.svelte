<script lang="ts">
	/**
	 * Modal v2 — Svelte 5 Advanced Component
	 * ========================================
	 * Enhanced modal dialog with $host element access, stacked modal support,
	 * size presets, transition hooks, and $inspect debugging.
	 *
	 * ## v2 Improvements (c2)
	 * - $host for direct backdrop element access
	 * - Preset sizes (sm/md/lg/xl/full)
	 * - Stacked modal support via z-index management
	 * - $inspect traces open/close lifecycle
	 * - onOpen/onClose callbacks
	 * - BeforeClose guard (async confirmation)
	 * - Nested snippet slots: children, footer, trigger
	 */

	import type { ModalSize } from '../types';

	interface Props {
		open: boolean;
		title?: string;
		ariaLabel?: string;
		closeOnBackdrop?: boolean;
		closeOnEscape?: boolean;
		showClose?: boolean;
		maxWidth?: string;
		/** Preset size (overrides maxWidth) */
		size?: ModalSize;
		class?: string;
		children?: import('svelte').Snippet;
		footer?: import('svelte').Snippet;
		/** Called when modal opens */
		onOpen?: () => void;
		/** Called when modal closes */
		onClose?: () => void;
		/** Guard: return false to prevent close */
		beforeClose?: () => boolean | Promise<boolean>;
	}

	let {
		open = $bindable(false),
		title = '',
		ariaLabel = '',
		closeOnBackdrop = true,
		closeOnEscape = true,
		showClose = true,
		maxWidth = '',
		size = 'md',
		class: className = '',
		children,
		footer,
		onOpen,
		onClose,
		beforeClose
	}: Props = $props();

	// $host — direct reference to the backdrop div
	let backdropEl = $host<HTMLDivElement>();
	let dialogEl = $state<HTMLDivElement | null>(null);
	let previousActiveElement = $state<Element | null>(null);
	let titleId = $state(`s5-modal-title-${Math.random().toString(36).slice(2, 9)}`);

	// $inspect — trace modal state
	$inspect('Modal open:', open);
	$inspect('Modal backdrop:', backdropEl);

	const sizeMap: Record<ModalSize, string> = {
		sm: '400px',
		md: '520px',
		lg: '720px',
		xl: '960px',
		full: '95vw'
	};

	const resolvedMaxWidth = $derived(maxWidth || sizeMap[size]);

	// Stacked modal z-index management
	const zIndex = $state(1000);
	$effect(() => {
		if (open) {
			// Find highest existing modal z-index
			const existingModals = document.querySelectorAll('[role="dialog"][aria-modal="true"]');
			let maxZ = 1000;
			existingModals.forEach((el) => {
				const z = parseInt(getComputedStyle(el).zIndex) || 0;
				if (z > maxZ) maxZ = z;
			});
			zIndex = maxZ + 10;
		}
	});

	const FOCUSABLE =
		'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])';

	function getFocusable(): HTMLElement[] {
		return dialogEl
			? Array.from(dialogEl.querySelectorAll<HTMLElement>(FOCUSABLE))
			: [];
	}

	function trapFocus(e: KeyboardEvent) {
		if (e.key !== 'Tab') return;
		const focusable = getFocusable();
		if (focusable.length === 0) { e.preventDefault(); return; }
		const [first, last] = [focusable[0], focusable[focusable.length - 1]];
		if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
		else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
	}

	function handleKeydown(e: KeyboardEvent) {
		trapFocus(e);
		if (closeOnEscape && e.key === 'Escape') {
			e.preventDefault();
			doClose();
		}
	}

	async function doClose() {
		if (beforeClose) {
			const ok = await beforeClose();
			if (!ok) return;
		}
		open = false;
	}

	// Body scroll lock + focus management
	$effect(() => {
		if (open) {
			previousActiveElement = document.activeElement;
			document.body.style.overflow = 'hidden';
			onOpen?.();

			requestAnimationFrame(() => {
				const focusable = getFocusable();
				if (focusable.length > 0) focusable[0].focus();
				else if (dialogEl) dialogEl.focus();
			});

			return () => {
				document.body.style.overflow = '';
				onClose?.();
				if (previousActiveElement instanceof HTMLElement) {
					previousActiveElement.focus();
				}
			};
		}
	});

	async function handleBackdropClick(e: MouseEvent) {
		if (closeOnBackdrop && e.target === backdropEl) {
			await doClose();
		}
	}
</script>

{#if open}
	<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
	<div
		class="s5-modal-backdrop"
		style="z-index: {zIndex};"
		role="dialog"
		aria-modal="true"
		aria-labelledby={title ? titleId : undefined}
		aria-label={!title && ariaLabel ? ariaLabel : undefined}
		bind:this={backdropEl}
		onclick={handleBackdropClick}
		onkeydown={handleKeydown}
		tabindex="-1"
	>
		<div
			class="s5-modal-panel {className}"
			style="max-width: {resolvedMaxWidth};"
			role="document"
			bind:this={dialogEl}
		>
			<div class="s5-modal-header">
				{#if title}
					<h2 id={titleId} class="s5-modal-title">{title}</h2>
				{:else}
					<span></span>
				{/if}
				{#if showClose}
					<button
						class="s5-modal-close"
						onclick={doClose}
						aria-label="Close dialog"
						type="button"
					>✕</button>
				{/if}
			</div>

			<div class="s5-modal-body">
				{#if children}
					{@render children()}
				{/if}
			</div>

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
		to   { opacity: 1; }
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
		from { opacity: 0; transform: translateY(12px) scale(0.98); }
		to   { opacity: 1; transform: translateY(0) scale(1); }
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
		margin: 0; font-size: 1.1rem; font-weight: 700; color: #1e293b;
	}
	.s5-modal-close {
		width: 32px; height: 32px; border: none; background: transparent;
		font-size: 1.1rem; color: #94a3b8; cursor: pointer; border-radius: 6px;
		display: flex; align-items: center; justify-content: center; transition: all 0.15s;
	}
	.s5-modal-close:hover { background: #f1f5f9; color: #475569; }
	.s5-modal-close:focus-visible { outline: 2px solid #6366f1; outline-offset: 2px; }

	.s5-modal-body {
		padding: 20px; overflow-y: auto; flex: 1; color: #334155;
		font-size: 0.95rem; line-height: 1.6;
	}
	.s5-modal-footer {
		padding: 12px 20px; border-top: 1px solid #e2e8f0;
		display: flex; justify-content: flex-end; gap: 8px; flex-shrink: 0;
	}
</style>
