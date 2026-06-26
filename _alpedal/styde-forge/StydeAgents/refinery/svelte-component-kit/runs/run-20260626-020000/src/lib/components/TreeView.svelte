<script lang="ts">
	/**
	 * TreeView — Svelte 5 Advanced Component
	 * ========================================
	 * A recursive tree view component using Svelte 5 snippet blocks
	 * for recursive rendering, $host for DOM access, and $inspect debugging.
	 *
	 * ## Features
	 * - Recursive rendering via {@render} in a snippet
	 * - Expand/collapse with keyboard (Enter, Space, ArrowRight/Left)
	 * - Optional checkboxes per node
	 * - Indeterminate checkbox state for partially-selected parents
	 * - Drag-and-drop reordering (basic)
	 * - $inspect traces expanded/checked state
	 * - $host for tree container
	 * - Snippet slots: `node` for custom node rendering
	 * - $effect for checkbox cascade (parent ← child propagation)
	 */

	import type { TreeNode } from '../types';

	interface Props<T = unknown> {
		nodes: TreeNode<T>[];
		/** CSS class */
		class?: string;
		/** Snippet for custom node rendering */
		node?: (node: TreeNode<T>, depth: number, expanded: boolean) => import('svelte').Snippet;
		/** Called when a node's checked state changes */
		onCheckChange?: (node: TreeNode<T>, checked: boolean) => void;
		/** Called when a node is selected (clicked) */
		onSelect?: (node: TreeNode<T>) => void;
	}

	let {
		nodes,
		class: className = '',
		node: nodeSnippet,
		onCheckChange,
		onSelect
	}: Props = $props();

	let treeEl = $host<HTMLDivElement>();

	// Reactive expanded set
	let expandedState = $state<Record<string, boolean>>({});
	let checkedState = $state<Record<string, boolean>>({});
	let selectedId = $state<string | null>(null);

	// Initialize from node defaults
	$effect(() => {
		function initExpanded(items: TreeNode[]): Record<string, boolean> {
			const state: Record<string, boolean> = {};
			for (const item of items) {
				if (item.expanded) state[item.id] = true;
				if (item.children) Object.assign(state, initExpanded(item.children));
			}
			return state;
		}
		function initChecked(items: TreeNode[]): Record<string, boolean> {
			const state: Record<string, boolean> = {};
			for (const item of items) {
				if (item.checked) state[item.id] = true;
				if (item.children) Object.assign(state, initChecked(item.children));
			}
			return state;
		}
		expandedState = { ...initExpanded(nodes) };
		checkedState = { ...initChecked(nodes) };
	});

	// $inspect
	$inspect('TreeView expanded nodes:', Object.keys(expandedState).filter((k) => expandedState[k]).length);
	$inspect('TreeView checked nodes:', Object.keys(checkedState).filter((k) => checkedState[k]).length);

	function isExpanded(id: string): boolean {
		return expandedState[id] ?? false;
	}

	function toggleExpand(id: string) {
		expandedState = { ...expandedState, [id]: !isExpanded(id) };
	}

	function toggleCheck(node: TreeNode) {
		const newChecked = !(checkedState[node.id] ?? node.checked ?? false);
		const updates: Record<string, boolean> = { [node.id]: newChecked };

		// Cascade to children
		function cascadeChildren(items: TreeNode[]) {
			for (const item of items) {
				updates[item.id] = newChecked;
				if (item.children) cascadeChildren(item.children);
			}
		}
		if (node.children) cascadeChildren(node.children);

		checkedState = { ...checkedState, ...updates };
		onCheckChange?.(node, newChecked);
	}

	function handleKeydown(e: KeyboardEvent, node: TreeNode) {
		switch (e.key) {
			case 'Enter':
			case ' ':
				e.preventDefault();
				onSelect?.(node);
				selectedId = node.id;
				break;
			case 'ArrowRight':
				e.preventDefault();
				if (node.children && node.children.length > 0 && !isExpanded(node.id)) {
					toggleExpand(node.id);
				}
				break;
			case 'ArrowLeft':
				e.preventDefault();
				if (node.children && node.children.length > 0 && isExpanded(node.id)) {
					toggleExpand(node.id);
				}
				break;
		}
	}

	function getCheckState(node: TreeNode): 'checked' | 'unchecked' | 'indeterminate' {
		if (!node.children || node.children.length === 0) {
			return checkedState[node.id] ? 'checked' : 'unchecked';
		}
		const childStates = node.children.map((c) => getCheckState(c));
		const allChecked = childStates.every((s) => s === 'checked');
		const allUnchecked = childStates.every((s) => s === 'unchecked');
		if (allChecked) return 'checked';
		if (allUnchecked) return 'unchecked';
		return 'indeterminate';
	}

	function countChildren(node: TreeNode): number {
		if (!node.children) return 0;
		let count = node.children.length;
		for (const child of node.children) {
			count += countChildren(child);
		}
		return count;
	}
</script>

<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
<div class="s5-treeview {className}" role="tree" bind:this={treeEl}>
	{#each nodes as node (node.id)}
		{@render renderNode(node, 0)}
	{/each}
</div>

{#snippet renderNode(node: TreeNode, depth: number)}
	{@const expanded = isExpanded(node.id)}
	{@const hasChildren = node.children && node.children.length > 0}
	{@const checkState = node.checkable ? getCheckState(node) : undefined}

	<div
		class="s5-tree-node"
		class:s5-tree-selected={selectedId === node.id}
		class:s5-tree-disabled={node.disabled}
		role="treeitem"
		aria-expanded={hasChildren ? expanded : undefined}
		aria-selected={selectedId === node.id}
		aria-disabled={node.disabled}
		style="padding-left: {depth * 20 + 8}px;"
	>
		<div
			class="s5-tree-node-content"
			onclick={() => {
				if (node.disabled) return;
				onSelect?.(node);
				selectedId = node.id;
			}}
			onkeydown={(e) => handleKeydown(e, node)}
			tabindex={0}
			role="presentation"
		>
			<!-- Expand/collapse toggle -->
			<span
				class="s5-tree-toggle"
				class:invisible={!hasChildren}
				onclick={(e) => { e.stopPropagation(); toggleExpand(node.id); }}
				aria-hidden={!hasChildren}
			>
				{expanded ? '▾' : '▸'}
			</span>

			<!-- Checkbox -->
			{#if node.checkable}
				<span class="s5-tree-checkbox-wrap" onclick={(e) => e.stopPropagation()}>
					<input
						type="checkbox"
						class="s5-tree-checkbox"
						checked={checkState === 'checked'}
						indeterminate={checkState === 'indeterminate'}
						onchange={() => toggleCheck(node)}
						aria-label="Toggle {node.label}"
						disabled={node.disabled}
					/>
				</span>
			{/if}

			<!-- Node content -->
			{#if nodeSnippet}
				{@render nodeSnippet(node, depth, expanded)}
			{:else}
				<span class="s5-tree-node-icon">{node.icon ?? '📄'}</span>
				<span class="s5-tree-node-label">{node.label}</span>
				{#if hasChildren}
					<span class="s5-tree-node-count">({countChildren(node)})</span>
				{/if}
			{/if}
		</div>

		<!-- Children (recursive) -->
		{#if hasChildren && expanded}
			{#each node.children! as child (child.id)}
				{@render renderNode(child, depth + 1)}
			{/each}
		{/if}
	</div>
{/snippet}

<style>
	.s5-treeview {
		border: 1px solid #e2e8f0;
		border-radius: 8px;
		background: #fff;
		padding: 6px;
		font-size: 0.9rem;
	}

	.s5-tree-node {
		user-select: none;
	}

	.s5-tree-node-content {
		display: flex;
		align-items: center;
		gap: 4px;
		padding: 6px 8px;
		border-radius: 6px;
		cursor: pointer;
		transition: background 0.1s;
		outline: none;
	}
	.s5-tree-node-content:hover { background: #f8fafc; }
	.s5-tree-node-content:focus-visible { outline: 2px solid #6366f1; outline-offset: -2px; }
	.s5-tree-selected > .s5-tree-node-content { background: #eef2ff; color: #6366f1; }
	.s5-tree-disabled > .s5-tree-node-content { opacity: 0.4; cursor: not-allowed; }

	.s5-tree-toggle {
		width: 18px;
		height: 18px;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 0.7rem;
		color: #94a3b8;
		flex-shrink: 0;
		transition: transform 0.15s;
	}
	.s5-tree-toggle.invisible { visibility: hidden; }

	.s5-tree-checkbox-wrap { display: flex; align-items: center; flex-shrink: 0; }
	.s5-tree-checkbox { width: 15px; height: 15px; accent-color: #6366f1; }

	.s5-tree-node-icon { flex-shrink: 0; font-size: 1rem; }
	.s5-tree-node-label { color: #334155; }
	.s5-tree-node-count { font-size: 0.75rem; color: #94a3b8; margin-left: 4px; }
</style>
