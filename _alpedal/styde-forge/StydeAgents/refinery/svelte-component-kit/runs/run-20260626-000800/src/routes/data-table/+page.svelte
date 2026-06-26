<script lang="ts">
	/**
	 * DataTable — SvelteKit Page Example
	 * ====================================
	 * Demonstrates the DataTable component with sorting, pagination,
	 * selection, and custom cell rendering.
	 */

	import DataTable from '$lib/components/DataTable.svelte';
	import type { ColumnDef } from '$lib/types';

	// ─── Sample data ────────────────────────────────────────────────
	interface User {
		id: number;
		name: string;
		email: string;
		role: string;
		status: 'active' | 'inactive' | 'pending';
		joined: string;
	}

	const users: User[] = [
		{ id: 1, name: 'Alice Johnson', email: 'alice@example.com', role: 'Admin', status: 'active', joined: '2024-01-15' },
		{ id: 2, name: 'Bob Smith', email: 'bob@example.com', role: 'Editor', status: 'active', joined: '2024-03-10' },
		{ id: 3, name: 'Carol White', email: 'carol@example.com', role: 'Viewer', status: 'inactive', joined: '2024-05-22' },
		{ id: 4, name: 'Dave Brown', email: 'dave@example.com', role: 'Editor', status: 'pending', joined: '2024-06-01' },
		{ id: 5, name: 'Eve Davis', email: 'eve@example.com', role: 'Admin', status: 'active', joined: '2024-02-18' },
		{ id: 6, name: 'Frank Miller', email: 'frank@example.com', role: 'Viewer', status: 'active', joined: '2024-07-04' },
		{ id: 7, name: 'Grace Wilson', email: 'grace@example.com', role: 'Editor', status: 'inactive', joined: '2024-04-30' },
		{ id: 8, name: 'Hank Taylor', email: 'hank@example.com', role: 'Viewer', status: 'pending', joined: '2024-08-12' },
		{ id: 9, name: 'Ivy Anderson', email: 'ivy@example.com', role: 'Admin', status: 'active', joined: '2023-12-01' },
		{ id: 10, name: 'Jack Thomas', email: 'jack@example.com', role: 'Editor', status: 'active', joined: '2024-01-20' },
		{ id: 11, name: 'Kate Martinez', email: 'kate@example.com', role: 'Viewer', status: 'inactive', joined: '2024-09-05' },
		{ id: 12, name: 'Leo Robinson', email: 'leo@example.com', role: 'Editor', status: 'active', joined: '2024-03-25' },
	];

	// ─── Column definitions ─────────────────────────────────────────
	const columns: ColumnDef<User>[] = [
		{
			key: 'name',
			label: 'Name',
			render: (value, row) => `<strong>${value}</strong>`,
		},
		{
			key: 'email',
			label: 'Email',
		},
		{
			key: 'role',
			label: 'Role',
		},
		{
			key: 'status',
			label: 'Status',
			render: (value) => {
				const status = value as string;
				const colors: Record<string, string> = {
					active: '#22c55e',
					inactive: '#94a3b8',
					pending: '#f59e0b',
				};
				return `<span style="color:${colors[status]}; font-weight:600;">● ${status}</span>`;
			},
		},
		{
			key: 'joined',
			label: 'Joined',
			sortable: true,
		},
	];

	let selectedRows = $state<number[]>([]);
	let pageSize = $state(5);
</script>

<svelte:head>
	<title>DataTable Example — Svelte 5 Component Kit</title>
</svelte:head>

<div class="page">
	<h1>DataTable Component</h1>
	<p class="subtitle">
		A sortable, paginated data table with row selection and custom cell rendering.
		Built with Svelte 5 runes (<code>$state</code>, <code>$derived</code>, <code>$effect</code>).
	</p>

	<div class="controls">
		<label>
			Page size:
			<select bind:value={pageSize}>
				<option value={3}>3</option>
				<option value={5}>5</option>
				<option value={10}>10</option>
			</select>
		</label>
		{#if selectedRows.length > 0}
			<span class="selection-info">{selectedRows.length} row(s) selected</span>
		{/if}
	</div>

	<DataTable
		{columns}
		data={users}
		{pageSize}
		selectable
		multiSelect
		bind:selected={selectedRows}
	/>

	<div class="notes">
		<h2>Features Demonstrated</h2>
		<ul>
			<li>Click column headers to sort (asc → desc → none)</li>
			<li>Custom <code>render()</code> for Name and Status columns</li>
			<li>Multi-select with checkboxes</li>
			<li>Pagination with configurable page size</li>
			<li>Keyboard accessible (Tab/Enter/Space)</li>
		</ul>
	</div>
</div>

<style>
	.page {
		max-width: 960px;
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

	.controls {
		display: flex;
		align-items: center;
		gap: 16px;
		margin-bottom: 16px;
		font-size: 0.9rem;
		color: #475569;
	}

	.controls select {
		margin-left: 6px;
		padding: 4px 8px;
		border: 1px solid #d1d5db;
		border-radius: 4px;
		font-size: 0.9rem;
	}

	.selection-info {
		font-weight: 600;
		color: #6366f1;
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

	.notes code {
		background: #e2e8f0;
		padding: 1px 4px;
		border-radius: 3px;
		font-size: 0.85em;
	}
</style>
