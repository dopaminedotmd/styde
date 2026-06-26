<script lang="ts">
	/**
	 * Universal Reactive Stores — Svelte 5 Runes Outside Components
	 * ==============================================================
	 * This is a .svelte.ts module: runes ($state, $derived, $effect)
	 * work here just as they would inside a .svelte file. This is the
	 * canonical Svelte 5 pattern for shared reactive state.
	 *
	 * ## Stores included:
	 * - createUndoRedoStore   — undo/redo with history
	 * - createLocalStore      — reactive localStorage sync
	 * - createMediaQueryStore — reactive media query matcher
	 * - createThemeStore      — theme manager with system preference
	 * - createDebounceStore   — debounced reactive value
	 * - createCounterStore    — simple counter with computed derivations
	 */

	import type { UndoRedoState, ThemeMode, MediaBreakpoint, LocalStoreOptions } from '../types';

	// ═══════════════════════════════════════════════════════════════
	// Undo/Redo Store
	// ═══════════════════════════════════════════════════════════════

	export function createUndoRedoStore<T>(initial: T, maxHistory = 50) {
		let state = $state<UndoRedoState<T>>({
			past: [],
			present: initial,
			future: []
		});

		const canUndo = $derived(state.past.length > 0);
		const canRedo = $derived(state.future.length > 0);

		function push(value: T) {
			state = {
				past: [...state.past.slice(-(maxHistory - 1)), state.present],
				present: value,
				future: []
			};
		}

		function undo() {
			if (!canUndo) return;
			const past = [...state.past];
			const previous = past.pop()!;
			state = {
				past,
				present: previous,
				future: [state.present, ...state.future]
			};
		}

		function redo() {
			if (!canRedo) return;
			const future = [...state.future];
			const next = future.shift()!;
			state = {
				past: [...state.past, state.present],
				present: next,
				future
			};
		}

		function reset(value: T) {
			state = { past: [], present: value, future: [] };
		}

		return {
			get current() { return state.present; },
			get canUndo() { return canUndo; },
			get canRedo() { return canRedo; },
			get historySize() { return state.past.length + 1; },
			push,
			undo,
			redo,
			reset
		};
	}

	// ═══════════════════════════════════════════════════════════════
	// LocalStorage Reactive Store
	// ═══════════════════════════════════════════════════════════════

	export function createLocalStore<T>(options: LocalStoreOptions<T>) {
		const { key, defaultValue, serialize = JSON.stringify, deserialize = JSON.parse } = options;

		function read(): T {
			if (typeof window === 'undefined') return defaultValue;
			try {
				const raw = localStorage.getItem(key);
				return raw !== null ? deserialize(raw) : defaultValue;
			} catch {
				return defaultValue;
			}
		}

		let value = $state<T>(read());

		$effect(() => {
			// Track the current value and persist on change
			const current = value;
			if (typeof window !== 'undefined') {
				try {
					localStorage.setItem(key, serialize(current));
				} catch { /* storage full or private browsing */ }
			}
		});

		function set(newValue: T | ((prev: T) => T)) {
			if (typeof newValue === 'function') {
				value = (newValue as (prev: T) => T)(value);
			} else {
				value = newValue;
			}
		}

		function reset() {
			value = defaultValue;
		}

		return {
			get current() { return value; },
			set,
			reset,
			get key() { return key; }
		};
	}

	// ═══════════════════════════════════════════════════════════════
	// Media Query Store
	// ═══════════════════════════════════════════════════════════════

	const DEFAULT_BREAKPOINTS: MediaBreakpoint[] = [
		{ name: 'sm', query: '(min-width: 640px)' },
		{ name: 'md', query: '(min-width: 768px)' },
		{ name: 'lg', query: '(min-width: 1024px)' },
		{ name: 'xl', query: '(min-width: 1280px)' },
		{ name: '2xl', query: '(min-width: 1536px)' },
		{ name: 'dark', query: '(prefers-color-scheme: dark)' },
		{ name: 'reducedMotion', query: '(prefers-reduced-motion: reduce)' }
	];

	export function createMediaQueryStore(queries: MediaBreakpoint[] = DEFAULT_BREAKPOINTS) {
		let matches = $state<Record<string, boolean>>({});

		$effect(() => {
			if (typeof window === 'undefined') return;

			const cleanups: (() => void)[] = [];

			for (const bp of queries) {
				const mq = window.matchMedia(bp.query);
				matches = { ...matches, [bp.name]: mq.matches };

				const handler = (e: MediaQueryListEvent) => {
					matches = { ...matches, [bp.name]: e.matches };
				};
				mq.addEventListener('change', handler);
				cleanups.push(() => mq.removeEventListener('change', handler));
			}

			return () => cleanups.forEach((fn) => fn());
		});

		const currentBreakpoint = $derived.by(() => {
			const breakpoints = queries
				.filter((b) => !['dark', 'reducedMotion'].includes(b.name) && matches[b.name])
				.sort((a, b) => {
					const aIdx = queries.findIndex((q) => q.name === a.name);
					const bIdx = queries.findIndex((q) => q.name === b.name);
					return bIdx - aIdx;
				});
			return breakpoints[0]?.name ?? 'xs';
		});

		return {
			get matches() { return matches; },
			get currentBreakpoint() { return currentBreakpoint; },
			get isDark() { return matches['dark'] ?? false; },
			get isReducedMotion() { return matches['reducedMotion'] ?? false; },
			/** Check a custom query */
			check(query: string): boolean {
				if (typeof window === 'undefined') return false;
				return window.matchMedia(query).matches;
			}
		};
	}

	// ═══════════════════════════════════════════════════════════════
	// Theme Store
	// ═══════════════════════════════════════════════════════════════

	export function createThemeStore() {
		// Use localStore to persist preference
		const preference = createLocalStore<ThemeMode>({
			key: 's5-theme',
			defaultValue: 'system'
		});

		const media = createMediaQueryStore([
			{ name: 'dark', query: '(prefers-color-scheme: dark)' }
		]);

		const resolved = $derived<Exclude<ThemeMode, 'system'>>(
			preference.current === 'system'
				? media.isDark ? 'dark' : 'light'
				: preference.current
		);

		$effect(() => {
			if (typeof document === 'undefined') return;
			const root = document.documentElement;
			if (resolved === 'dark') {
				root.classList.add('dark');
			} else {
				root.classList.remove('dark');
			}
		});

		function toggle() {
			const next = resolved === 'dark' ? 'light' : 'dark';
			preference.set(next);
		}

		return {
			get preference() { return preference.current; },
			get resolved() { return resolved; },
			get isDark() { return resolved === 'dark'; },
			set(mode: ThemeMode) { preference.set(mode); },
			toggle
		};
	}

	// ═══════════════════════════════════════════════════════════════
	// Debounce Store
	// ═══════════════════════════════════════════════════════════════

	export function createDebounceStore<T>(initial: T, delay = 300) {
		let immediate = $state<T>(initial);
		let debounced = $state<T>(initial);

		$effect(() => {
			const current = immediate;
			const timer = setTimeout(() => {
				debounced = current;
			}, delay);
			return () => clearTimeout(timer);
		});

		return {
			get immediate() { return immediate; },
			get debounced() { return debounced; },
			set(value: T) { immediate = value; },
			/** Force-flush the debounced value immediately */
			flush() { debounced = immediate; }
		};
	}

	// ═══════════════════════════════════════════════════════════════
	// Counter Store (simple example)
	// ═══════════════════════════════════════════════════════════════

	export function createCounterStore(initial = 0) {
		let count = $state(initial);

		const double = $derived(count * 2);
		const isPositive = $derived(count > 0);
		const isNegative = $derived(count < 0);
		const parity = $derived<'even' | 'odd'>(count % 2 === 0 ? 'even' : 'odd');

		return {
			get count() { return count; },
			get double() { return double; },
			get isPositive() { return isPositive; },
			get isNegative() { return isNegative; },
			get parity() { return parity; },
			increment() { count++; },
			decrement() { count--; },
			add(n: number) { count += n; },
			reset() { count = initial; }
		};
	}
</script>
