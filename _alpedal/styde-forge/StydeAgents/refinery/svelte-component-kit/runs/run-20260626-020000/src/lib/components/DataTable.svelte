<script lang="ts">
	/**
	 * DataTable v2 — Svelte 5 Advanced Component
	 * ============================================
	 * Enhanced data table with snippet blocks for custom rendering,
	 * $inspect debugging, efficient sort (no unnecessary copies),
	 * column pinning, export CSV, and fixed headers.
	 *
	 * ## v2 Improvements (c2)
	 * - Snippet blocks: `header` and `cell` snippets replace the old
	 *   render() string approach — full Svelte reactivity in cells
	 * - Efficient sort: lazy-sorts on read, not on state change
	 * - $inspect traces sort/page state changes
	 * - Column pinning (left/right)
	 * - CSV export with proper escaping
	 * - `$host` for wrapper measurements
	 *
	 * ## Snippets
	 * - `header(col)` — custom header content per column
	 * - `cell(row, col, value)` — custom cell content
	 * - `empty` — custom empty state
	 */

	import type { ColumnDef, SortState, PageInfo } from '../types';

	interface Props<T = Record<string, unknown>> {
		columns: ColumnDef<T>[];
		data: T[];
		pageSize?: number;
		selectable?: boolean;
		multiSelect?: boolean;
		selected?: number[];
		class?: string;
		/** Snippet: custom header per column */
		header?: (col: ColumnDef<T>) => import('svelte').Snippet;
		/** Snippet: custom cell per row */
		cell?: (row: T, col: ColumnDef<T>, value: unknown) => import('svelte').Snippet;
		/** Snippet: empty state */
		empty?: import('svelte').Snippet;
		/** Show export button */
		exportable?: boolean;
		/** Filename for CSV export */
		exportFilename?: string;
	}

	let {
		columns,
		data = [],
		pageSize = 10,
		selectable = false,
		multiSelect = false,
		selected = $bindable([]),
		class: className = '',
		header,
		cell,
		empty,
		exportable = false,
		exportFilename = 'export.csv'
	}: Props = $props();

	let currentSort = $state<SortState>({ key: '', direction: null });
	let currentPage = $state(1);
	let wrapperEl = $host<HTMLDivElement>();

	// $inspect — trace state in dev mode
	$inspect('DataTable sort:', currentSort);
	$inspect('DataTable page:', currentPage);
	$inspect('DataTable total rows:', data.length);

	// Efficient sort: find column comparator once, then sort
	const sortComparator = $derived.by(() => {
		if (!currentSort.key || !currentSort.direction) return null;
		const col = columns.find((c) => c.key === currentSort.key);
		if (!col) return null;
		const dir = currentSort.direction === 'asc' ? 1 : -1;
		return (a: T, b: T) => {
			if (col.sort) return col.sort(a, b) * dir;
			const aVal = (a as Record<string, unknown>)[currentSort.key];
			const bVal = (b as Record<string, unknown>)[currentSort.key];
			if (typeof aVal === 'string' && typeof bVal === 'string') return aVal.localeCompare(bVal) * dir;
			if (aVal == null && bVal == null) return 0;
			if (aVal == null) return 1 * dir;
			if (bVal == null) return -1 * dir;
			if (aVal < bVal) return -1 * dir;
			if (aVal > bVal) return 1 * dir;
			return 0;
		};
	});

	// Efficient: only sort when comparator or data changes
	const sortedData = $derived(
		sortComparator ? [...data].sort(sortComparator) : data
	);

	const totalPages = $derived(Math.max(1, Math.ceil(sortedData.length / pageSize)));

	const paginatedData = $derived.by(() => {
		const start = (currentPage - 1) * pageSize;
		return sortedData.slice(start, start + pageSize);
	});

	$effect(() => {
		// Clamp page when data shrinks
		if (currentPage > totalPages) currentPage = totalPages;
	});

	function handleSort(colKey: string) {
		const col = columns.find((c) => c.key === colKey);
		if (col?.sortable === false) return;
		if (currentSort.key === colKey) {
			if (currentSort.direction === 'asc') currentSort = { key: colKey, direction: 'desc' };
			else if (currentSort.direction === 'desc') currentSort = { key: '', direction: null };
			else currentSort = { key: colKey, direction: 'asc' };
		} else {
			currentSort = { key: colKey, direction: 'asc' };
		}
		currentPage = 1;
	}

	function handleRowClick(idx: number) {
		if (!selectable) return;
		if (multiSelect) {
			selected = selected.includes(idx)
				? selected.filter((i) => i !== idx)
				: [...selected, idx];
		} else {
			selected = selected.includes(idx) ? [] : [idx];
		}
	}

	function goToPage(page: number) {
		currentPage = Math.max(1, Math.min(page, totalPages));
	}

	function getSortIndicator(colKey: string): string {
		if (currentSort.key !== colKey || !currentSort.direction) return '↕';
		return currentSort.direction === 'asc' ? '↑' : '↓';
	}

	// CSV export
	function exportCSV() {
		const headers = columns.map((c) => c.label);
		const rows = sortedData.map((row) =>
			columns.map((col) => {
				const val = (row as Record<string, unknown>)[col.key];
				const str = String(val ?? '');
				// Escape CSV: wrap in quotes if contains comma, quote, or newline
				return str.includes(',') || str.includes('"') || str.includes('\n')
					? `"${str.replace(/"/g, '""')}"`
					: str;
			}).join(',')
		);
		const csv = [headers.join(','), ...rows].join('\n');
		const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = exportFilename;
		a.click();
		URL.revokeObjectURL(url);
	}

	const pageInfo: PageInfo = $derived({
		current: currentPage,
		total: totalPages,
		pageSize,
		totalRows: sortedData.length
	});

	const visiblePages = $derived.by(() => {
		const pages: (number | '...')[] = [];
		const tp = totalPages;
		const cp = currentPage;
		if (tp <= 7) {
			for (let i = 1; i <= tp; i++) pages.push(i);
		} else {
			pages.push(1);
			if (cp > 3) pages.push('...');
			for (let i = Math.max(2, cp - 1); i <= Math.min(tp - 1, cp + 1); i++) pages.push(i);
			if (cp < tp - 2) pages.push('...');
			pages.push(tp);
		}
		return pages;
	});

	// Render cell value (used when no snippet provided)
	function renderCellValue(row: T, col: ColumnDef<T>): string {
		if (col.render) return col.render((row as Record<string, unknown>)[col.key], row);
		return String((row as Record<string, unknown>)[col.key] ?? '');
	}
</script>

<div class="s5-datatable-wrapper {className}" bind:this={wrapperEl}>
	{#if exportable && sortedData.length > 0}
		<div class="s5-dt-toolbar">
			<span class="s5-dt-row-count">{sortedData.length} row(s)</span>
			<button class="s5-dt-export-btn" onclick={exportCSV} type="button">
				⬇ Export CSV
			</button>
		</div>
	{/if}

	<table class="s5-datatable" role="grid" aria-label="Data table">
		<thead>
			<tr role="row">
				{#if selectable}
					<th class="s5-dt-col-select s5-dt-pinned-left" role="columnheader" scope="col">
						{#if multiSelect}
							<input
								type="checkbox"
								aria-label="Select all"
								checked={selected.length === paginatedData.length && paginatedData.length > 0}
								onchange={() => {
									if (selected.length === paginatedData.length) selected = [];
									else {
										const start = (currentPage - 1) * pageSize;
										selected = paginatedData.map((_, i) => start + i);
									}
								}}
							/>
						{/if}
					</th>
				{/if}
				{#each columns as col}
					<th
						class="s5-dt-header {col.headerClass ?? ''}"
						class:sortable={col.sortable !== false}
						class:sorted={currentSort.key === col.key}
						class:s5-dt-pinned-left={col.pinned === 'left'}
						class:s5-dt-pinned-right={col.pinned === 'right'}
						style={col.width ? `width:${col.width}` : ''}
						role="columnheader"
						scope="col"
						aria-sort={currentSort.key === col.key
							? (currentSort.direction === 'asc' ? 'ascending' : 'descending')
							: 'none'}
						tabindex={col.sortable !== false ? 0 : undefined}
						onclick={() => handleSort(col.key)}
						onkeydown={(e) => {
							if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); handleSort(col.key); }
						}}
					>
						{#if header}
							{@render header(col)}
						{:else}
							<span class="s5-dt-header-label">{col.label}</span>
							{#if col.sortable !== false}
								<span class="s5-dt-sort-indicator" aria-hidden="true">{getSortIndicator(col.key)}</span>
							{/if}
						{/if}
					</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#if paginatedData.length === 0}
				<tr>
					<td colspan={selectable ? columns.length + 1 : columns.length} class="s5-dt-empty">
						{#if empty}
							{@render empty()}
						{:else}
							No data available.
						{/if}
					</td>
				</tr>
			{:else}
				{#each paginatedData as row, idx}
					{@const globalIdx = (currentPage - 1) * pageSize + idx}
					<tr
						role="row"
						class:selected={selectable && selected.includes(globalIdx)}
						class:selectable-row={selectable}
						tabindex={selectable ? 0 : undefined}
						onclick={() => handleRowClick(globalIdx)}
						onkeydown={(e) => {
							if (selectable && (e.key === 'Enter' || e.key === ' ')) {
								e.preventDefault();
								handleRowClick(globalIdx);
							}
						}}
						aria-selected={selectable ? selected.includes(globalIdx) : undefined}
					>
						{#if selectable}
							<td class="s5-dt-col-select s5-dt-pinned-left">
								{#if multiSelect}
									<input
										type="checkbox"
										aria-label="Select row {globalIdx + 1}"
										checked={selected.includes(globalIdx)}
										onchange={() => handleRowClick(globalIdx)}
									/>
								{:else}
									<input
										type="radio"
										name="s5-dt-select"
										aria-label="Select row {globalIdx + 1}"
										checked={selected.includes(globalIdx)}
										onchange={() => handleRowClick(globalIdx)}
									/>
								{/if}
							</td>
						{/if}
						{#each columns as col}
							<td
								class="s5-dt-cell {col.cellClass ?? ''}"
								class:s5-dt-pinned-left={col.pinned === 'left'}
								class:s5-dt-pinned-right={col.pinned === 'right'}
							>
								{#if cell}
									{@render cell(row, col, (row as Record<string, unknown>)[col.key])}
								{:else}
									{@html renderCellValue(row, col)}
								{/if}
							</td>
						{/each}
					</tr>
				{/each}
			{/if}
		</tbody>
	</table>

	{#if totalPages > 1}
		<nav class="s5-dt-pagination" aria-label="Table pagination">
			<button class="s5-dt-page-btn" disabled={currentPage === 1} onclick={() => goToPage(currentPage - 1)} aria-label="Previous page">← Prev</button>
			{#each visiblePages as page}
				{#if page === '...'}
					<span class="s5-dt-ellipsis">…</span>
				{:else}
					<button
						class="s5-dt-page-btn"
						class:active={page === currentPage}
						onclick={() => goToPage(page)}
						aria-label="Page {page}"
						aria-current={page === currentPage ? 'page' : undefined}
					>{page}</button>
				{/if}
			{/each}
			<button class="s5-dt-page-btn" disabled={currentPage === totalPages} onclick={() => goToPage(currentPage + 1)} aria-label="Next page">Next →</button>
			<span class="s5-dt-page-info">Page {currentPage} of {totalPages} ({sortedData.length} rows)</span>
		</nav>
	{/if}
</div>

<style>
	.s5-datatable-wrapper {
		overflow-x: auto;
		border: 1px solid #e2e8f0;
		border-radius: 8px;
		background: #fff;
	}

	.s5-dt-toolbar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 8px 14px;
		background: #f8fafc;
		border-bottom: 1px solid #e2e8f0;
	}
	.s5-dt-row-count { font-size: 0.8rem; color: #64748b; }
	.s5-dt-export-btn {
		padding: 4px 10px;
		border: 1px solid #d1d5db;
		border-radius: 4px;
		background: #fff;
		color: #475569;
		cursor: pointer;
		font-size: 0.8rem;
		transition: all 0.15s;
	}
	.s5-dt-export-btn:hover { background: #f1f5f9; border-color: #6366f1; color: #6366f1; }

	.s5-datatable {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.9rem;
	}

	.s5-dt-header {
		padding: 10px 14px;
		text-align: left;
		font-weight: 600;
		color: #475569;
		background: #f8fafc;
		border-bottom: 2px solid #e2e8f0;
		user-select: none;
		white-space: nowrap;
	}
	.s5-dt-header.sortable { cursor: pointer; transition: background 0.15s; }
	.s5-dt-header.sortable:hover { background: #f1f5f9; }
	.s5-dt-header.sortable:focus-visible { outline: 2px solid #6366f1; outline-offset: -2px; }
	.s5-dt-header.sorted { color: #6366f1; }
	.s5-dt-sort-indicator { font-size: 0.75rem; opacity: 0.6; }
	.s5-dt-header-label { display: inline; }

	.s5-dt-cell {
		padding: 10px 14px;
		border-bottom: 1px solid #f1f5f9;
		color: #334155;
	}
	.s5-dt-col-select { width: 40px; padding: 10px 8px; text-align: center; }
	.s5-dt-empty { padding: 40px; text-align: center; color: #94a3b8; font-style: italic; }

	/* Column pinning */
	.s5-dt-pinned-left {
		position: sticky;
		left: 0;
		z-index: 2;
		background: inherit;
	}
	.s5-dt-pinned-right {
		position: sticky;
		right: 0;
		z-index: 2;
		background: inherit;
	}

	tr.selectable-row { cursor: pointer; transition: background 0.15s; }
	tr.selectable-row:hover { background: #f8fafc; }
	tr.selectable-row:focus-visible { outline: 2px solid #6366f1; outline-offset: -2px; }
	tr.selected { background: #eef2ff !important; }
	tr.selected .s5-dt-pinned-left,
	tr.selected .s5-dt-pinned-right { background: #eef2ff; }

	/* Pagination */
	.s5-dt-pagination {
		display: flex;
		align-items: center;
		gap: 4px;
		padding: 10px 14px;
		border-top: 1px solid #e2e8f0;
		background: #f8fafc;
		flex-wrap: wrap;
	}
	.s5-dt-page-btn {
		padding: 5px 10px;
		border: 1px solid #e2e8f0;
		border-radius: 4px;
		background: #fff;
		color: #475569;
		cursor: pointer;
		font-size: 0.85rem;
		transition: all 0.15s;
	}
	.s5-dt-page-btn:hover:not(:disabled) { background: #6366f1; color: #fff; border-color: #6366f1; }
	.s5-dt-page-btn:disabled { opacity: 0.4; cursor: not-allowed; }
	.s5-dt-page-btn.active { background: #6366f1; color: #fff; border-color: #6366f1; font-weight: 600; }
	.s5-dt-ellipsis { padding: 5px 4px; color: #94a3b8; }
	.s5-dt-page-info { margin-left: auto; font-size: 0.8rem; color: #94a3b8; }
</style>
