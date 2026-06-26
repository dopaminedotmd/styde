// ─── Shared TypeScript Types for Svelte 5 Component Kit ───

/** Sort direction for DataTable */
export type SortDirection = 'asc' | 'desc' | null;

/** Sort state for a DataTable column */
export interface SortState {
	key: string;
	direction: SortDirection;
}

/** Column definition for DataTable */
export interface ColumnDef<T = Record<string, unknown>> {
	/** Unique key matching a property in the data row */
	key: string;
	/** Display label for the column header */
	label: string;
	/** Is this column sortable? Default: true */
	sortable?: boolean;
	/** Custom render function. Receives the row value and the full row. */
	render?: (value: unknown, row: T) => string;
	/** Custom sort comparator. Receives two rows, returns a number. */
	sort?: (a: T, b: T) => number;
	/** Optional CSS class for the column header */
	headerClass?: string;
	/** Optional CSS class for each cell in this column */
	cellClass?: string;
}

/** Validation rule for a form field */
export interface ValidationRule {
	/** Unique name for the rule (used in error messages) */
	name: string;
	/** Validation function. Return true if valid, or a string error message. */
	validate: (value: unknown, allValues: Record<string, unknown>) => true | string;
}

/** A single field definition in a Form */
export interface FormField {
	/** Field name (key in form data) */
	name: string;
	/** Display label */
	label: string;
	/** Input type: text, email, password, number, textarea, select, checkbox */
	type: 'text' | 'email' | 'password' | 'number' | 'textarea' | 'select' | 'checkbox';
	/** Placeholder text */
	placeholder?: string;
	/** Default value */
	defaultValue?: unknown;
	/** Validation rules applied in order */
	rules?: ValidationRule[];
	/** For select fields: array of { value, label } options */
	options?: { value: string | number; label: string }[];
	/** Is this field required? */
	required?: boolean;
}

/** Toast notification variant */
export type ToastVariant = 'info' | 'success' | 'warning' | 'error';

/** A single toast notification */
export interface Toast {
	id: string;
	message: string;
	variant: ToastVariant;
	duration?: number; // ms, 0 = sticky
	dismissible?: boolean;
}

/** Toast store returned by createToastStore */
export interface ToastStore {
	toasts: Toast[];
	add: (toast: Omit<Toast, 'id'>) => string;
	remove: (id: string) => void;
	clear: () => void;
}

/** Tab item definition */
export interface TabItem {
	id: string;
	label: string;
	disabled?: boolean;
	/** Optional badge count */
	badge?: number;
}
