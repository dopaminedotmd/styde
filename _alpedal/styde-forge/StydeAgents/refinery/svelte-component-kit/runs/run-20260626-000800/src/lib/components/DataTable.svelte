<script lang="ts">
	/**
	 * DataTable — Svelte 5 Component
	 * ===============================
	 * A sortable, accessible data table built with Svelte 5 runes.
	 *
	 * ## Features
	 * - Multi-column sorting via header clicks
	 * - Custom sort comparators per column
	 * - Custom cell rendering
	 * - Row selection (single or multi)
	 * - Pagination with configurable page size
	 * - Accessible: proper ARIA roles, keyboard navigation
	 *
	 * ## Usage
	 * ```svelte
	 * <DataTable {columns} {data} pageSize={10} on:sort={handleSort} />
	 * ```
	 *
	 * ## Runes Used
	 * - `$state`  — currentSort, currentPage, selectedRows
	 * - `$derived` — sortedData, paginatedData, totalPages
	 * - `$effect`  — reset page to 1 when sort or data changes
	 */

	import type { ColumnDef, SortState } from '../types';

	// ─── Props ──────────────────────────────────────────────────────
	interface Props<T = Record<string, unknown>> {
		columns: ColumnDef<T>[];
		data: T[];
		pageSize?: number;
		/** Allow row selection? */
		selectable?: boolean;
		/** Multi-select mode (checkboxes instead of radio) */
		multiSelect?: boolean;
		/** Currently selected row indices (two-way bind) */
		selected?: number[];
		/** CSS class for the wrapper */
		class?: string;
	}

	let {
		columns,
		data = [],
		pageSize = 10,
		selectable = false,
		multiSelect = false,
		selected = $bindable([]),
		class: className = ''
	}: Props = $props();

	// ─── State (Svelte 5 runes) ─────────────────────────────────────
	let currentSort = $state<SortState>({ key: '', direction: null });
	let currentPage = $state(1);

	// ─── Derived ────────────────────────────────────────────────────
	const sortedData = $derived.by(() => {
		if (!currentSort.key || !currentSort.direction) return data;

		const col = columns.find((c) => c.key === currentSort.key);
		const dir = currentSort.direction === 'asc' ? 1 : -1;

		return [...data].sort((a, b) => {
			if (col?.sort) return col.sort(a, b) * dir;

			const aVal = (a as Record<string, unknown>)[currentSort.key];
			const bVal = (b as Record<string, unknown>)[currentSort.key];

			// Natural comparison
			if (typeof aVal === 'string' && typeof bVal === 'string') {
				return aVal.localeCompare(bVal) * dir;
			}
			if (aVal == null && bVal == null) return 0;
			if (aVal == null) return 1 * dir;
			if (bVal == null) return -1 * dir;

			if (aVal < bVal) return -1 * dir;
			if (aVal > bVal) return 1 * dir;
			return 0;
		});
	});

	const totalPages = $derived(Math.max(1, Math.ceil(sortedData.length / pageSize)));

	const paginatedData = $derived.by(() => {
		const start = (currentPage - 1) * pageSize;
		return sortedData.slice(start, start + pageSize);
	});

	// ─── Effects ────────────────────────────────────────────────────
	$effect(() => {
		// Reset page when sort or data changes
		void sortedData.length;
		if (currentPage > totalPages) {
			currentPage = totalPages;
		}
	});

	// ─── Handlers ───────────────────────────────────────────────────
	function handleSort(colKey: string) {
		const col = columns.find((c) => c.key === colKey);
		if (col?.sortable === false) return;

		if (currentSort.key === colKey) {
			// Cycle: asc → desc → none
			if (currentSort.direction === 'asc') {
				currentSort = { key: colKey, direction: 'desc' };
			} else if (currentSort.direction === 'desc') {
				currentSort = { key: '', direction: null };
			} else {
				currentSort = { key: colKey, direction: 'asc' };
			}
		} else {
			currentSort = { key: colKey, direction: 'asc' };
		}
		currentPage = 1;
	}

	function handleRowClick(idx: number) {
		if (!selectable) return;

		if (multiSelect) {
			const exists = selected.includes(idx);
			selected = exists ? selected.filter((i) => i !== idx) : [...selected, idx];
		} else {
			selected = selected.includes(idx) ? [] : [idx];
		}
	}

	function goToPage(page: number) {
		currentPage = Math.max(1, Math.min(page, totalPages));
	}

	// ─── Helpers ────────────────────────────────────────────────────
	function getSortIndicator(colKey: string): string {
		if (currentSort.key !== colKey || !currentSort.direction) return '↕';
		return currentSort.direction === 'asc' ? '↑' : '↓';
	}

	function getCellValue(row: Record<string, unknown>, col: ColumnDef): unknown {
		return row[col.key];
	}

	const visiblePages = $derived.by(() => {
		const pages: (number | '...')[] = [];
		const tp = totalPages;
		const cp = currentPage;

		if (tp <= 7) {
			for (let i = 1; i <= tp; i++) pages.push(i);
		} else {
			pages.push(1);
			if (cp > 3) pages.push('...');
			for (let i = Math.max(2, cp - 1); i <= Math.min(tp - 1, cp + 1); i++) {
				pages.push(i);
			}
			if (cp < tp - 2) pages.push('...');
			pages.push(tp);
		}
		return pages;
	});
</script>

<div class="s5-datatable-wrapper {className}">
	<table class="s5-datatable" role="grid" aria-label="Data table">
		<thead>
			<tr role="row">
				{#if selectable}
					<th class="s5-dt-col-select" role="columnheader" scope="col">
						{#if multiSelect}
							<input
								type="checkbox"
								aria-label="Select all"
								checked={selected.length === paginatedData.length && paginatedData.length > 0}
								onchange={() => {
									// Toggle select all on current page
									if (selected.length === paginatedData.length) {
										selected = [];
									} else {
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
						role="columnheader"
						scope="col"
						aria-sort={
							currentSort.key === col.key
								? currentSort.direction === 'asc'
									? 'ascending'
									: 'descending'
								: 'none'
						}
						tabindex={col.sortable !== false ? 0 : undefined}
						onclick={() => handleSort(col.key)}
						onkeydown={(e) => {
							if (e.key === 'Enter' || e.key === ' ') {
								e.preventDefault();
								handleSort(col.key);
							}
						}}
					>
						<span class="s5-dt-header-label">{col.label}</span>
						{#if col.sortable !== false}
							<span class="s5-dt-sort-indicator" aria-hidden="true">
								{getSortIndicator(col.key)}
							</span>
						{/if}
					</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#if paginatedData.length === 0}
				<tr>
					<td
						colspan={selectable ? columns.length + 1 : columns.length}
						class="s5-dt-empty"
					>
						No data available.
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
							<td class="s5-dt-col-select">
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
							<td class="s5-dt-cell {col.cellClass ?? ''}">
								{#if col.render}
									{@html col.render(getCellValue(row as Record<string, unknown>, col), row)}
								{:else}
									{String(getCellValue(row as Record<string, unknown>, col) ?? '')}
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
			<button
				class="s5-dt-page-btn"
				disabled={currentPage === 1}
				onclick={() => goToPage(currentPage - 1)}
				aria-label="Previous page"
			>
				← Prev
			</button>

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
					>
						{page}
					</button>
				{/if}
			{/each}

			<button
				class="s5-dt-page-btn"
				disabled={currentPage === totalPages}
				onclick={() => goToPage(currentPage + 1)}
				aria-label="Next page"
			>
				Next →
			</button>

			<span class="s5-dt-page-info">
				Page {currentPage} of {totalPages} ({sortedData.length} rows)
			</span>
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

	.s5-dt-header.sortable {
		cursor: pointer;
		transition: background 0.15s;
	}
	.s5-dt-header.sortable:hover {
		background: #f1f5f9;
	}
	.s5-dt-header.sortable:focus-visible {
		outline: 2px solid #6366f1;
		outline-offset: -2px;
	}

	.s5-dt-header.sorted {
		color: #6366f1;
	}

	.s5-dt-header-label {
		margin-right: 4px;
	}

	.s5-dt-sort-indicator {
		font-size: 0.75rem;
		opacity: 0.6;
	}

	.s5-dt-cell {
		padding: 10px 14px;
		border-bottom: 1px solid #f1f5f9;
		color: #334155;
	}

	.s5-dt-col-select {
		width: 40px;
		padding: 10px 8px;
		text-align: center;
	}

	.s5-dt-empty {
		padding: 32px;
		text-align: center;
		color: #94a3b8;
		font-style: italic;
	}

	tr.selectable-row {
		cursor: pointer;
		transition: background 0.15s;
	}
	tr.selectable-row:hover {
		background: #f8fafc;
	}
	tr.selectable-row:focus-visible {
		outline: 2px solid #6366f1;
		outline-offset: -2px;
	}

	tr.selected {
		background: #eef2ff !important;
	}

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
	.s5-dt-page-btn:hover:not(:disabled) {
		background: #6366f1;
		color: #fff;
		border-color: #6366f1;
	}
	.s5-dt-page-btn:disabled {
		opacity: 0.4;
		cursor: not-allowed;
	}
	.s5-dt-page-btn.active {
		background: #6366f1;
		color: #fff;
		border-color: #6366f1;
		font-weight: 600;
	}

	.s5-dt-ellipsis {
		padding: 5px 4px;
		color: #94a3b8;
	}

	.s5-dt-page-info {
		margin-left: auto;
		font-size: 0.8rem;
		color: #94a3b8;
	}
</style>
