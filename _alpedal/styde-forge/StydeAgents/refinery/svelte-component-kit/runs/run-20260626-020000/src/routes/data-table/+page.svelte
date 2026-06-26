<script lang="ts">
	import DataTable from '$lib/components/DataTable.svelte';
	import type { ColumnDef } from '$lib/types';

	interface User {
		id: number; name: string; email: string; role: string;
		status: 'active' | 'inactive' | 'pending'; joined: string;
	}

	const users: User[] = [
		{ id: 1, name: 'Alice Johnson', email: 'alice@example.com', role: 'Admin', status: 'active', joined: '2024-01-15' },
		{ id: 2, name: 'Bob Smith', email: 'bob@example.com', role: 'Editor', status: 'active', joined: '2024-02-20' },
		{ id: 3, name: 'Carol White', email: 'carol@example.com', role: 'Viewer', status: 'inactive', joined: '2024-03-10' },
		{ id: 4, name: 'Dan Brown', email: 'dan@example.com', role: 'Admin', status: 'pending', joined: '2024-04-05' },
		{ id: 5, name: 'Eve Davis', email: 'eve@example.com', role: 'Editor', status: 'active', joined: '2024-05-12' },
		{ id: 6, name: 'Frank Miller', email: 'frank@example.com', role: 'Viewer', status: 'active', joined: '2024-06-01' },
		{ id: 7, name: 'Grace Lee', email: 'grace@example.com', role: 'Editor', status: 'inactive', joined: '2024-06-15' },
		{ id: 8, name: 'Henry Wilson', email: 'henry@example.com', role: 'Viewer', status: 'pending', joined: '2024-07-01' },
		{ id: 9, name: 'Iris Chen', email: 'iris@example.com', role: 'Admin', status: 'active', joined: '2024-07-10' },
		{ id: 10, name: 'Jack Taylor', email: 'jack@example.com', role: 'Viewer', status: 'active', joined: '2024-08-01' },
		{ id: 11, name: 'Kate Moore', email: 'kate@example.com', role: 'Editor', status: 'active', joined: '2024-08-15' },
		{ id: 12, name: 'Leo Anderson', email: 'leo@example.com', role: 'Viewer', status: 'inactive', joined: '2024-09-01' },
	];

	const columns: ColumnDef<User>[] = [
		{
			key: 'name', label: 'Name',
			render: (value) => `<strong>${value}</strong>`,
		},
		{ key: 'email', label: 'Email', width: '200px' },
		{ key: 'role', label: 'Role' },
		{
			key: 'status', label: 'Status',
			render: (value) => {
				const colors: Record<string, string> = {
					active: '#22c55e', inactive: '#94a3b8', pending: '#f59e0b'
				};
				return `<span style="color:${colors[value as string]}; font-weight:600;">● ${value}</span>`;
			}
		},
		{ key: 'joined', label: 'Joined' },
	];

	let selectedRows = $state<number[]>([]);
	let pageSize = $state(5);
</script>

<div class="page">
	<h1>📊 DataTable Component</h1>
	<p class="subtitle">v2: Enhanced with snippet slots, CSV export, column pinning, $inspect, and efficient sort.</p>
	<div class="controls">
		<label>Page size:
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
	<DataTable {columns} data={users} {pageSize} selectable multiSelect bind:selected={selectedRows} exportable exportFilename="users.csv" />
</div>

<style>
	.page { padding: 24px 32px; max-width: 960px; }
	h1 { font-size: 1.5rem; margin: 0 0 4px; }
	.subtitle { color: #64748b; margin: 0 0 20px; font-size: 0.9rem; }
	.controls { display: flex; gap: 16px; align-items: center; margin-bottom: 16px; font-size: 0.85rem; }
	.controls select { padding: 4px 8px; border: 1px solid #d1d5db; border-radius: 4px; }
	.selection-info { color: #6366f1; font-weight: 600; }
</style>
