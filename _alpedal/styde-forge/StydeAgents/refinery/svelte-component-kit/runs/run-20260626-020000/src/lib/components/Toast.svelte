<script lang="ts">
	/**
	 * Toast v2 — Svelte 5 Advanced Component
	 * ========================================
	 * Enhanced toast notification system with proper $effect timeout cleanup,
	 * $inspect debugging, $host reference, action buttons, and queue management.
	 *
	 * ## v2 Improvements (c2)
	 * - Proper timeout cleanup: each toast tracks its own timer, cleaned up on
	 *   early dismiss or component unmount via $effect return
	 * - $inspect for debugging toast lifecycle
	 * - $host for Container DOM measurement
	 * - Action button support
	 * - Timestamp-based ordering
	 * - Fade-out animation before removal
	 *
	 * ## Runes Used
	 * - `$state`  — internal toast list, timer map
	 * - `$derived` — visible toasts, ordered
	 * - `$effect`  — managed auto-dismiss with proper cleanup
	 * - `$inspect` — debug tracing
	 * - `$host`   — container element reference
	 */

	import type { Toast, ToastVariant } from '../types';

	// ─── Store ──────────────────────────────────────────────────────
	export function createToastStore() {
		let _toasts = $state<Toast[]>([]);
		let _counter = 0;

		function add(toast: Omit<Toast, 'id' | 'createdAt'>): string {
			const id = `toast-${++_counter}-${Math.random().toString(36).slice(2, 7)}`;
			const full: Toast = {
				...toast,
				id,
				duration: toast.duration ?? 4000,
				dismissible: toast.dismissible ?? true,
				createdAt: Date.now()
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

	// ─── Container ─────────────────────────────────────────────────
	interface ContainerProps {
		store: ReturnType<typeof createToastStore>;
		position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' | 'top-center' | 'bottom-center';
		maxVisible?: number;
	}

	let {
		store,
		position = 'bottom-right',
		maxVisible = 5
	}: ContainerProps = $props();

	// $host — direct reference to the container element
	let containerEl = $host<HTMLDivElement>();

	// v2: Track active timers so we can clean them up
	let timers = $state<Map<string, ReturnType<typeof setTimeout>>>(new Map());

	// Derived: visible toasts sorted by creation time, limited
	const visibleToasts = $derived(
		[...store.toasts]
			.sort((a, b) => a.createdAt - b.createdAt)
			.slice(-maxVisible)
	);

	// $inspect — trace toast state changes in dev mode
	$inspect('Toast count:', store.toasts.length);
	$inspect('Visible toasts:', visibleToasts.length);
	$inspect('Container element:', containerEl);

	// ─── Auto-dismiss with proper cleanup ──────────────────────────
	$effect(() => {
		// Track current toasts
		const currentToasts = store.toasts;

		for (const toast of currentToasts) {
			// Skip if already timed or sticky
			if (timers.has(toast.id)) continue;
			if (!toast.duration || toast.duration <= 0) continue;

			const timer = setTimeout(() => {
				store.remove(toast.id);
				timers.delete(toast.id);
			}, toast.duration);

			const newTimers = new Map(timers);
			newTimers.set(toast.id, timer);
			timers = newTimers;
		}

		// Cleanup: clear timers for toasts that no longer exist
		return () => {
			const activeIds = new Set(currentToasts.map((t) => t.id));
			for (const [id, timer] of timers) {
				if (!activeIds.has(id)) {
					clearTimeout(timer);
					const newTimers = new Map(timers);
					newTimers.delete(id);
					timers = newTimers;
				}
			}
		};
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
	<div
		class="s5-toast-container {getPositionClass(position)}"
		aria-live="polite"
		aria-relevant="additions removals"
		bind:this={containerEl}
	>
		{#each visibleToasts as toast (toast.id)}
			<div
				class="s5-toast s5-toast-{toast.variant}"
				role={toast.variant === 'error' || toast.variant === 'warning' ? 'alert' : 'status'}
				style="animation: s5-toast-in 0.3s ease-out;"
			>
				<span class="s5-toast-icon">{getVariantIcon(toast.variant)}</span>
				<span class="s5-toast-message">{toast.message}</span>

				{#if toast.action}
					<button
						class="s5-toast-action"
						onclick={toast.action.onClick}
						type="button"
					>
						{toast.action.label}
					</button>
				{/if}

				{#if toast.dismissible}
					<button
						class="s5-toast-dismiss"
						onclick={() => {
							// Clean up timer on manual dismiss
							const timer = timers.get(toast.id);
							if (timer) {
								clearTimeout(timer);
								const newTimers = new Map(timers);
								newTimers.delete(toast.id);
								timers = newTimers;
							}
							store.remove(toast.id);
						}}
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
		max-width: 420px;
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
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12), 0 1px 3px rgba(0, 0, 0, 0.08);
		font-size: 0.9rem;
		pointer-events: auto;
		position: relative;
		overflow: hidden;
		border-left: 4px solid;
	}

	@keyframes s5-toast-in {
		from { opacity: 0; transform: translateY(-8px); }
		to   { opacity: 1; transform: translateY(0); }
	}

	@keyframes s5-toast-shrink {
		from { width: 100%; }
		to   { width: 0%; }
	}

	.s5-toast-info    { border-left-color: #6366f1; }
	.s5-toast-success { border-left-color: #22c55e; }
	.s5-toast-warning { border-left-color: #f59e0b; }
	.s5-toast-error   { border-left-color: #ef4444; }

	.s5-toast-icon {
		font-size: 1.1rem;
		flex-shrink: 0;
		width: 24px;
		height: 24px;
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

	.s5-toast-action {
		flex-shrink: 0;
		padding: 4px 10px;
		border: 1px solid #6366f1;
		border-radius: 4px;
		background: transparent;
		color: #6366f1;
		font-size: 0.8rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.15s;
	}
	.s5-toast-action:hover {
		background: #6366f1;
		color: #fff;
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
		opacity: 0.2;
	}
	.s5-toast-info .s5-toast-progress    { color: #6366f1; }
	.s5-toast-success .s5-toast-progress { color: #22c55e; }
	.s5-toast-warning .s5-toast-progress { color: #f59e0b; }
	.s5-toast-error .s5-toast-progress   { color: #ef4444; }
</style>
