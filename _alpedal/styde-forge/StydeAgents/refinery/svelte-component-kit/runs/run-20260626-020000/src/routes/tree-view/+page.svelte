<script lang="ts">
	import TreeView from '$lib/components/TreeView.svelte';
	import type { TreeNode } from '$lib/types';

	const nodes: TreeNode[] = [
		{
			id: 'src', label: 'src', icon: '📁', expanded: true, children: [
				{ id: 'lib', label: 'lib', icon: '📁', expanded: true, children: [
					{ id: 'components', label: 'components', icon: '📁', children: [
						{ id: 'datatable', label: 'DataTable.svelte', icon: '📄', checkable: true, checked: true },
						{ id: 'form', label: 'Form.svelte', icon: '📄', checkable: true, checked: true },
						{ id: 'modal', label: 'Modal.svelte', icon: '📄', checkable: true },
						{ id: 'toast', label: 'Toast.svelte', icon: '📄', checkable: true, checked: true },
					]},
					{ id: 'stores', label: 'stores', icon: '📁', children: [
						{ id: 'reactive', label: 'reactive.svelte.ts', icon: '📄', checkable: true },
					]},
					{ id: 'types', label: 'types.ts', icon: '📄', checkable: true, checked: true },
					{ id: 'index', label: 'index.ts', icon: '📄', checkable: true, checked: true },
				]},
				{ id: 'routes', label: 'routes', icon: '📁', children: [
					{ id: 'layout', label: '+layout.svelte', icon: '📄' },
					{ id: 'page', label: '+page.svelte', icon: '📄' },
				]},
			]
		},
		{ id: 'package', label: 'package.json', icon: '📦' },
		{ id: 'svelteconfig', label: 'svelte.config.js', icon: '⚙️' },
		{ id: 'tsconfig', label: 'tsconfig.json', icon: '⚙️' },
	];

	let selectedId = $state<string | null>(null);
</script>

<div class="page">
	<h1>🌳 TreeView Component</h1>
	<p class="subtitle">New c2: Recursive snippet blocks, checkboxes with cascade, $inspect, $host.</p>
	<TreeView {nodes} onSelect={(n) => selectedId = n.id} />
	{#if selectedId}
		<p class="selected-info">Selected: <strong>{nodes.find((n) => n.id === selectedId)?.label ?? selectedId}</strong></p>
	{/if}
</div>

<style>
	.page { padding: 24px 32px; max-width: 400px; }
	h1 { font-size: 1.5rem; margin: 0 0 4px; }
	.subtitle { color: #64748b; margin: 0 0 20px; font-size: 0.9rem; }
	.selected-info { margin-top: 12px; font-size: 0.85rem; color: #6366f1; }
</style>
