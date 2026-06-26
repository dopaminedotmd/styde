// Barrel export for all components, stores, and types — Svelte 5 Component Kit v2 (c2)

// ─── Components ───────────────────────────────────────────────────
export { default as DataTable } from './components/DataTable.svelte';
export { default as Form } from './components/Form.svelte';
export { default as Modal } from './components/Modal.svelte';
export { default as Tabs } from './components/Tabs.svelte';
export { default as ToastContainer, createToastStore } from './components/Toast.svelte';
export { default as Accordion } from './components/Accordion.svelte';
export { default as CommandPalette } from './components/CommandPalette.svelte';
export { default as TreeView } from './components/TreeView.svelte';
export { default as InfiniteScroll } from './components/InfiniteScroll.svelte';

// ─── Universal Reactive Stores (.svelte.ts) ───────────────────────
export {
	createUndoRedoStore,
	createLocalStore,
	createMediaQueryStore,
	createThemeStore,
	createDebounceStore,
	createCounterStore
} from './stores/reactive.svelte.ts';

// ─── Types ────────────────────────────────────────────────────────
export type * from './types';
