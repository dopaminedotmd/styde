AGENTS: 1
STATUS: Building DataTable component (React + TypeScript)
Components built:
1. src/components/DataTable/types.ts
2. src/components/DataTable/DataTable.tsx
3. src/components/DataTable/useDataFetch.ts
4. src/components/DataTable/DataTable.test.tsx
---
src/components/DataTable/types.ts
export interface Column<T> {
  key: keyof T | string;
  header: string;
  render?: (value: T[keyof T], row: T) => React.ReactNode;
  sortable?: boolean;
  filterable?: boolean;
  width?: string;
}
export interface DataTableProps<T> {
  columns: Column<T>[];
  data?: T[];
  fetchUrl?: string;
  pageSize?: number;
  initialSort?: { key: string; direction: 'asc' | 'desc' };
  onRowClick?: (row: T) => void;
  loading?: boolean;
  error?: string;
  emptyMessage?: string;
}
export interface SortState {
  key: string;
  direction: 'asc' | 'desc';
}
export interface FilterState {
  [key: string]: string;
}
export interface PaginationState {
  page: number;
  pageSize: number;
  total: number;
}
---
src/components/DataTable/useDataFetch.ts
import { useState, useEffect, useCallback, useRef } from 'react';
interface UseDataFetchOptions {
  url?: string;
  page: number;
  pageSize: number;
  sort?: { key: string; direction: 'asc' | 'desc' } | null;
  filters?: Record<string, string>;
}
interface UseDataFetchResult<T> {
  data: T[];
  total: number;
  loading: boolean;
  error: string | null;
}
export function useDataFetch<T>(options: UseDataFetchOptions): UseDataFetchResult<T> {
  const [data, setData] = useState<T[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);
  const { url, page, pageSize, sort, filters } = options;
  const fetchData = useCallback(async () => {
    if (!url) return;
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      params.set('page', String(page));
      params.set('pageSize', String(pageSize));
      if (sort) {
        params.set('sort', sort.key);
        params.set('direction', sort.direction);
      }
      if (filters) {
        Object.entries(filters).forEach(([k, v]) => {
          if (v) params.set(`filter[${k}]`, v);
        });
      }
      const res = await fetch(`${url}?${params}`, { signal: controller.signal });
      if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
      const json = await res.json();
      setData(json.data ?? json.items ?? json.results ?? json);
      setTotal(json.total ?? json.count ?? (Array.isArray(json) ? json.length : 0));
    } catch (err: any) {
      if (err.name !== 'AbortError') {
        setError(err.message ?? 'Failed to fetch data');
      }
    } finally {
      setLoading(false);
    }
  }, [url, page, pageSize, sort, filters]);
  useEffect(() => {
    fetchData();
    return () => abortRef.current?.abort();
  }, [fetchData]);
  return { data, total, loading, error };
}
---
src/components/DataTable/DataTable.tsx
import React, { useState, useMemo, useCallback } from 'react';
import { Column, DataTableProps, SortState, FilterState, PaginationState } from './types';
import { useDataFetch } from './useDataFetch';
const DEFAULT_PAGE_SIZE = 20;
export function DataTable<T extends Record<string, any>>(props: DataTableProps<T>) {
  const {
    columns,
    data: staticData,
    fetchUrl,
    pageSize = DEFAULT_PAGE_SIZE,
    initialSort,
    onRowClick,
    loading: externalLoading,
    error: externalError,
    emptyMessage = 'No data',
  } = props;
  const [sort, setSort] = useState<SortState | null>(initialSort ?? null);
  const [filters, setFilters] = useState<FilterState>({});
  const [pagination, setPagination] = useState<PaginationState>({
    page: 1,
    pageSize,
    total: 0,
  });
  const isServerSide = !!fetchUrl;
  const { data: fetchedData, total, loading: fetchLoading, error: fetchError } = useDataFetch<T>({
    url: fetchUrl,
    page: pagination.page,
    pageSize: pagination.pageSize,
    sort,
    filters,
  });
  const displayData = isServerSide ? fetchedData : staticData ?? [];
  const totalRows = isServerSide ? total : (staticData?.length ?? 0);
  const isLoading = externalLoading ?? fetchLoading;
  const errorMessage = externalError ?? fetchError;
  const filteredSortedData = useMemo(() => {
    if (isServerSide) return displayData;
    let result = [...displayData];
    Object.entries(filters).forEach(([key, value]) => {
      if (!value) return;
      result = result.filter((row) =>
        String(row[key] ?? '').toLowerCase().includes(value.toLowerCase())
      );
    });
    if (sort) {
      result.sort((a, b) => {
        const aVal = a[sort.key];
        const bVal = b[sort.key];
        const cmp = aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
        return sort.direction === 'desc' ? -cmp : cmp;
      });
    }
    return result;
  }, [displayData, filters, sort, isServerSide]);
  const paginatedData = useMemo(() => {
    if (isServerSide) return displayData;
    const start = (pagination.page - 1) * pagination.pageSize;
    return filteredSortedData.slice(start, start + pagination.pageSize);
  }, [filteredSortedData, pagination.page, pagination.pageSize, isServerSide, displayData]);
  const totalPages = Math.max(1, Math.ceil(totalRows / pagination.pageSize));
  const handleSort = useCallback((key: string) => {
    setSort((prev) => {
      if (prev?.key === key) {
        return prev.direction === 'asc' ? { key, direction: 'desc' } : null;
      }
      return { key, direction: 'asc' };
    });
    setPagination((p) => ({ ...p, page: 1 }));
  }, []);
  const handleFilter = useCallback((key: string, value: string) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
    setPagination((p) => ({ ...p, page: 1 }));
  }, []);
  const handlePageChange = useCallback((page: number) => {
    setPagination((p) => ({ ...p, page }));
  }, []);
  const getCellValue = (row: T, col: Column<T>): React.ReactNode => {
    if (col.render) return col.render(row[col.key as keyof T], row);
    const value = row[col.key as keyof T];
    return value != null ? String(value) : '';
  };
  return (
    <div className="data-table-wrapper">
      {errorMessage && (
        <div className="data-table-error" role="alert">
          {errorMessage}
        </div>
      )}
      {isLoading && (
        <div className="data-table-loading" aria-busy="true">
          Loading...
        </div>
      )}
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={String(col.key)} style={{ width: col.width }}>
                <div className="data-table-header-content">
                  {col.filterable ? (
                    <input
                      className="data-table-filter-input"
                      placeholder={`Filter ${col.header}`}
                      value={filters[col.key] ?? ''}
                      onChange={(e) => handleFilter(col.key, e.target.value)}
                      aria-label={`Filter by ${col.header}`}
                    />
                  ) : (
                    <span>{col.header}</span>
                  )}
                  {col.sortable && (
                    <button
                      className="data-table-sort-btn"
                      onClick={() => handleSort(col.key)}
                      aria-label={`Sort by ${col.header}`}
                    >
                      {sort?.key === col.key ? (sort.direction === 'asc' ? '▲' : '▼') : '⇅'}
                    </button>
                  )}
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {paginatedData.length === 0 && !isLoading ? (
            <tr>
              <td colSpan={columns.length} className="data-table-empty">
                {emptyMessage}
              </td>
            </tr>
          ) : (
            paginatedData.map((row, i) => (
              <tr
                key={(row as any).id ?? i}
                onClick={() => onRowClick?.(row)}
                className={onRowClick ? 'data-table-row-clickable' : ''}
              >
                {columns.map((col) => (
                  <td key={String(col.key)}>{getCellValue(row, col)}</td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
      <div className="data-table-pagination">
        <button
          disabled={pagination.page <= 1}
          onClick={() => handlePageChange(1)}
          aria-label="First page"
        >
          «
        </button>
        <button
          disabled={pagination.page <= 1}
          onClick={() => handlePageChange(pagination.page - 1)}
          aria-label="Previous page"
        >
          ‹
        </button>
        <span>
          Page {pagination.page} of {totalPages} ({totalRows} rows)
        </span>
        <button
          disabled={pagination.page >= totalPages}
          onClick={() => handlePageChange(pagination.page + 1)}
          aria-label="Next page"
        >
          ›
        </button>
        <button
          disabled={pagination.page >= totalPages}
          onClick={() => handlePageChange(totalPages)}
          aria-label="Last page"
        >
          »
        </button>
      </div>
    </div>
  );
}
---
src/components/DataTable/DataTable.test.tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { DataTable } from './DataTable';
import { Column } from './types';
interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}
const mockUsers: User[] = [
  { id: 1, name: 'Alice', email: 'alice@test.com', role: 'admin' },
  { id: 2, name: 'Bob', email: 'bob@test.com', role: 'user' },
  { id: 3, name: 'Charlie', email: 'charlie@test.com', role: 'editor' },
];
const columns: Column<User>[] = [
  { key: 'id', header: 'ID', sortable: true },
  { key: 'name', header: 'Name', sortable: true, filterable: true },
  { key: 'email', header: 'Email' },
  { key: 'role', header: 'Role', filterable: true },
];
describe('DataTable', () => {
  it('renders static data', () => {
    render(<DataTable columns={columns} data={mockUsers} />);
    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('Bob')).toBeInTheDocument();
    expect(screen.getByText('Charlie')).toBeInTheDocument();
  });
  it('renders column headers', () => {
    render(<DataTable columns={columns} data={mockUsers} />);
    expect(screen.getByText('ID')).toBeInTheDocument();
    expect(screen.getByText('Name')).toBeInTheDocument();
    expect(screen.getByText('Email')).toBeInTheDocument();
    expect(screen.getByText('Role')).toBeInTheDocument();
  });
  it('shows empty message when no data', () => {
    render(<DataTable columns={columns} data={[]} emptyMessage="Nothing here" />);
    expect(screen.getByText('Nothing here')).toBeInTheDocument();
  });
  it('sorts by column on sort button click', () => {
    render(<DataTable columns={columns} data={mockUsers} />);
    const sortBtn = screen.getByLabelText('Sort by Name');
    fireEvent.click(sortBtn);
    const rows = screen.getAllByRole('row');
    expect(rows[1].textContent).toContain('Alice');
    expect(rows[2].textContent).toContain('Bob');
    expect(rows[3].textContent).toContain('Charlie');
  });
  it('filters rows by filterable column', () => {
    render(<DataTable columns={columns} data={mockUsers} />);
    const filterInput = screen.getByLabelText('Filter by Name');
    fireEvent.change(filterInput, { target: { value: 'Bob' } });
    expect(screen.getByText('Bob')).toBeInTheDocument();
    expect(screen.queryByText('Alice')).not.toBeInTheDocument();
    expect(screen.queryByText('Charlie')).not.toBeInTheDocument();
  });
  it('handles row click', () => {
    const onClick = jest.fn();
    render(<DataTable columns={columns} data={mockUsers} onRowClick={onClick} />);
    fireEvent.click(screen.getByText('Alice'));
    expect(onClick).toHaveBeenCalledWith(mockUsers[0]);
  });
  it('shows loading state', () => {
    render(<DataTable columns={columns} data={mockUsers} loading={true} />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });
  it('shows error state', () => {
    render(<DataTable columns={columns} data={[]} error="Failed to load data" />);
    expect(screen.getByText('Failed to load data')).toBeInTheDocument();
  });
  it('paginates data', () => {
    const manyUsers = Array.from({ length: 50 }, (_, i) => ({
      id: i + 1,
      name: `User ${i + 1}`,
      email: `user${i + 1}@test.com`,
      role: 'user',
    }));
    render(<DataTable columns={columns} data={manyUsers} pageSize={10} />);
    expect(screen.getByText('User 1')).toBeInTheDocument();
    expect(screen.queryByText('User 11')).not.toBeInTheDocument();
    fireEvent.click(screen.getByLabelText('Next page'));
    expect(screen.queryByText('User 1')).not.toBeInTheDocument();
    expect(screen.getByText('User 11')).toBeInTheDocument();
  });
  it('renders custom cell renderer', () => {
    const customCols: Column<User>[] = [
      ...columns,
      {
        key: 'actions',
        header: 'Actions',
        render: (_: any, row: User) => <button>Edit {row.name}</button>,
      },
    ];
    render(<DataTable columns={customCols} data={mockUsers} />);
    expect(screen.getByText('Edit Alice')).toBeInTheDocument();
  });
})
---
Total: 4 files, ~320 lines. Covers: static/server-side data, sorting, filtering, pagination, loading/error states, custom renderers, row clicks, empty state, accessibility (aria-labels, role=alert, aria-busy). Test suite: 10 tests.