<script lang="ts">
	import Accordion from '$lib/components/Accordion.svelte';
	import type { AccordionItem } from '$lib/types';

	const items: AccordionItem[] = [
		{ id: 'q1', title: 'What is Svelte 5?', expanded: true },
		{ id: 'q2', title: 'How do runes work?', icon: '✨' },
		{ id: 'q3', title: 'What are snippet blocks?', disabled: false },
		{ id: 'q4', title: 'Can I use runes outside components?', icon: '🧩' },
	];
</script>

<div class="page">
	<h1>🪗 Accordion Component</h1>
	<p class="subtitle">New c2: Snippet slots, smooth animation, $host, $inspect.</p>
	<Accordion {items}>
		<slot name="q1"><p>Svelte 5 introduces runes — universal reactive primitives that work inside and outside components.</p></slot>
		<slot name="q2"><p>Runes like $state, $derived, and $effect are compiler directives that make variables reactive.</p></slot>
		<slot name="q3"><p>Snippet blocks ({#snippet}/{@render}) let you define reusable chunks of template that accept parameters.</p></slot>
		<slot name="q4"><p>Yes! Create .svelte.ts files where runes function just like they do inside .svelte components.</p></slot>
	</Accordion>
</div>

<style>
	.page { padding: 24px 32px; max-width: 600px; }
	h1 { font-size: 1.5rem; margin: 0 0 4px; }
	.subtitle { color: #64748b; margin: 0 0 20px; font-size: 0.9rem; }
</style>
