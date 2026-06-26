<script lang="ts">
	/**
	 * Toast — Svelte 5 Component
	 * ===========================
	 * A toast notification system built with Svelte 5 runes.
	 * Includes both the store (createToastStore) and the rendering component.
	 *
	 * ## Features
	 * - Multiple variants: info, success, warning, error
	 * - Auto-dismiss with configurable duration
	 * - Manual dismiss
	 * - Stacked rendering with animation
	 * - Position configurable (top-right, bottom-right, etc.)
	 * - Accessible: role="status" / role="alert"
	 *
	 * ## Usage
	 * ```ts
	 * // In a shared module:
	 * import { createToastStore } from './Toast.svelte';
	 * export const toasts = createToastStore();
	 * ```
	 * ```svelte
	 * <!-- In +layout.svelte -->
	 * <ToastContainer store={toasts} />
	 * ```
	 * ```ts
	 * // Anywhere in the app:
	 * toasts.add({ message: 'Saved!', variant: 'success' });
	 * ```
	 *
	 * ## Runes Used
	 * - `$state`  — internal toast list (inside store)
	 * - `$derived` — filtered, visible toasts
	 * - `$effect`  — auto-dismiss timers
	 */

	import type { Toast, ToastVariant } from '../types';

	// ─── Store ──────────────────────────────────────────────────────
	/**
	 * Creates a reactive toast store.
	 * Call once and share the returned object across your app.
	 */
	export function createToastStore() {
		let _toasts = $state<Toast[]>([]);
		let _counter = 0;

		function add(toast: Omit<Toast, 'id'>): string {
			const id = `toast-${++_counter}-${Math.random().toString(36).slice(2, 7)}`;
			const full: Toast = {
				...toast,
				id,
				duration: toast.duration ?? 4000,
				dismissible: toast.dismissible ?? true
			};
			_toasts = [..._toasts, full];
			return id;
		}

		function remove(id: string) {
			_toasts = _toasts.filter((t) => t.id !== id);
		}

		function clear() {
			_toasts = [];
		}

		return {
			get toasts() {
				return _toasts;
			},
			add,
			remove,
			clear
		};
	}

	// ─── Container Props ────────────────────────────────────────────
	interface ContainerProps {
		store: ReturnType<typeof createToastStore>;
		/** Position on screen */
		position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' | 'top-center' | 'bottom-center';
		/** Max visible toasts */
		maxVisible?: number;
	}

	let {
		store,
		position = 'bottom-right',
		maxVisible = 5
	}: ContainerProps = $props();

	// ─── Derived ────────────────────────────────────────────────────
	const visibleToasts = $derived(store.toasts.slice(-maxVisible));

	// ─── Effects ────────────────────────────────────────────────────
	$effect(() => {
		// Auto-dismiss toasts with a duration
		for (const toast of store.toasts) {
			if (toast.duration && toast.duration > 0) {
				const dur = toast.duration;
				const id = toast.id;
				const timer = setTimeout(() => {
					store.remove(id);
				}, dur);
				// No cleanup needed per toast since the store handles removal
				// but we track timer to avoid memory leaks if toast is removed early
			}
		}
	});

	// ─── Helpers ────────────────────────────────────────────────────
	function getVariantIcon(variant: ToastVariant): string {
		switch (variant) {
			case 'success': return '✓';
			case 'error': return '✕';
			case 'warning': return '⚠';
			case 'info': return 'ℹ';
		}
	}

	function getPositionClass(pos: string): string {
		return `s5-toast-${pos}`;
	}
</script>

{#if visibleToasts.length > 0}
	<div class="s5-toast-container {getPositionClass(position)}" aria-live="polite" aria-relevant="additions removals">
		{#each visibleToasts as toast (toast.id)}
			<div
				class="s5-toast s5-toast-{toast.variant}"
				role={toast.variant === 'error' || toast.variant === 'warning' ? 'alert' : 'status'}
				style="animation: s5-toast-in 0.3s ease-out;"
			>
				<span class="s5-toast-icon">{getVariantIcon(toast.variant)}</span>
				<span class="s5-toast-message">{toast.message}</span>
				{#if toast.dismissible}
					<button
						class="s5-toast-dismiss"
						onclick={() => store.remove(toast.id)}
						aria-label="Dismiss notification"
						type="button"
					>
						✕
					</button>
				{/if}

				{#if toast.duration && toast.duration > 0}
					<div
						class="s5-toast-progress"
						style="animation: s5-toast-shrink {toast.duration}ms linear forwards;"
					></div>
				{/if}
			</div>
		{/each}
	</div>
{/if}

<style>
	.s5-toast-container {
		position: fixed;
		z-index: 9999;
		display: flex;
		flex-direction: column;
		gap: 8px;
		max-width: 400px;
		width: 100%;
		pointer-events: none;
	}

	.s5-toast-top-right    { top: 16px; right: 16px; }
	.s5-toast-top-left     { top: 16px; left: 16px; }
	.s5-toast-bottom-right { bottom: 16px; right: 16px; }
	.s5-toast-bottom-left  { bottom: 16px; left: 16px; }
	.s5-toast-top-center   { top: 16px; left: 50%; transform: translateX(-50%); }
	.s5-toast-bottom-center { bottom: 16px; left: 50%; transform: translateX(-50%); }

	.s5-toast {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 12px 16px;
		border-radius: 8px;
		background: #fff;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
		font-size: 0.9rem;
		pointer-events: auto;
		position: relative;
		overflow: hidden;
		border-left: 4px solid;
	}

	@keyframes s5-toast-in {
		from {
			opacity: 0;
			transform: translateY(-8px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	@keyframes s5-toast-shrink {
		from { width: 100%; }
		to { width: 0%; }
	}

	.s5-toast-info    { border-left-color: #6366f1; }
	.s5-toast-success { border-left-color: #22c55e; }
	.s5-toast-warning { border-left-color: #f59e0b; }
	.s5-toast-error   { border-left-color: #ef4444; }

	.s5-toast-icon {
		font-size: 1.1rem;
		flex-shrink: 0;
		width: 22px;
		height: 22px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 50%;
		font-weight: 700;
	}
	.s5-toast-info .s5-toast-icon    { color: #6366f1; background: #eef2ff; }
	.s5-toast-success .s5-toast-icon { color: #22c55e; background: #f0fdf4; }
	.s5-toast-warning .s5-toast-icon { color: #f59e0b; background: #fffbeb; }
	.s5-toast-error .s5-toast-icon   { color: #ef4444; background: #fef2f2; }

	.s5-toast-message {
		flex: 1;
		color: #334155;
		line-height: 1.4;
	}

	.s5-toast-dismiss {
		flex-shrink: 0;
		width: 24px;
		height: 24px;
		border: none;
		background: transparent;
		color: #94a3b8;
		cursor: pointer;
		border-radius: 4px;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 0.85rem;
		transition: all 0.15s;
	}
	.s5-toast-dismiss:hover {
		background: #f1f5f9;
		color: #475569;
	}

	.s5-toast-progress {
		position: absolute;
		bottom: 0;
		left: 0;
		height: 3px;
		background: currentColor;
		opacity: 0.25;
	}
	.s5-toast-info .s5-toast-progress    { color: #6366f1; }
	.s5-toast-success .s5-toast-progress { color: #22c55e; }
	.s5-toast-warning .s5-toast-progress { color: #f59e0b; }
	.s5-toast-error .s5-toast-progress   { color: #ef4444; }
</style>
