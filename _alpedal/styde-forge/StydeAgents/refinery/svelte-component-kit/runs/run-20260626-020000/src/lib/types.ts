// ─── Shared TypeScript Types for Svelte 5 Component Kit v2 (c2) ───

// ═══════════════════════════════════════════════════════════════════
// DataTable Types
// ═══════════════════════════════════════════════════════════════════

/** Sort direction for DataTable */
export type SortDirection = 'asc' | 'desc' | null;

/** Sort state for a DataTable column */
export interface SortState {
	key: string;
	direction: SortDirection;
}

/** Column definition for DataTable */
export interface ColumnDef<T = Record<string, unknown>> {
	key: string;
	label: string;
	sortable?: boolean;
	/** Custom render returning HTML string */
	render?: (value: unknown, row: T) => string;
	/** Custom sort comparator */
	sort?: (a: T, b: T) => number;
	headerClass?: string;
	cellClass?: string;
	/** Column width (CSS value, e.g. '120px' or '1fr') */
	width?: string;
	/** Pin column to left or right */
	pinned?: 'left' | 'right';
}

/** Page info for pagination */
export interface PageInfo {
	current: number;
	total: number;
	pageSize: number;
	totalRows: number;
}

// ═══════════════════════════════════════════════════════════════════
// Form Types
// ═══════════════════════════════════════════════════════════════════

/** Validation rule for a form field */
export interface ValidationRule {
	name: string;
	validate: (value: unknown, allValues: Record<string, unknown>) => true | string;
}

/** Async validation rule */
export interface AsyncValidationRule {
	name: string;
	validate: (value: unknown, allValues: Record<string, unknown>) => Promise<true | string>;
}

/** A single field definition */
export interface FormField {
	name: string;
	label: string;
	type: 'text' | 'email' | 'password' | 'number' | 'textarea' | 'select' | 'checkbox' | 'date' | 'tel' | 'url';
	placeholder?: string;
	defaultValue?: unknown;
	rules?: ValidationRule[];
	asyncRules?: AsyncValidationRule[];
	options?: { value: string | number; label: string }[];
	required?: boolean;
	/** Depend on another field's value — re-validate when it changes */
	dependsOn?: string;
	/** Help text below field */
	helpText?: string;
	/** Hide field conditionally */
	visible?: (values: Record<string, unknown>) => boolean;
}

/** Multi-step form step */
export interface FormStep {
	id: string;
	title: string;
	fields: string[]; // field names for this step
	description?: string;
}

// ═══════════════════════════════════════════════════════════════════
// Toast Types
// ═══════════════════════════════════════════════════════════════════

export type ToastVariant = 'info' | 'success' | 'warning' | 'error';

export interface Toast {
	id: string;
	message: string;
	variant: ToastVariant;
	duration?: number;
	dismissible?: boolean;
	/** Action button */
	action?: { label: string; onClick: () => void };
	createdAt: number;
}

export interface ToastStore {
	toasts: Toast[];
	add: (toast: Omit<Toast, 'id' | 'createdAt'>) => string;
	remove: (id: string) => void;
	clear: () => void;
}

// ═══════════════════════════════════════════════════════════════════
// Tabs Types
// ═══════════════════════════════════════════════════════════════════

export interface TabItem {
	id: string;
	label: string;
	disabled?: boolean;
	badge?: number;
	/** Icon (emoji or character) */
	icon?: string;
}

// ═══════════════════════════════════════════════════════════════════
// Modal Types
// ═══════════════════════════════════════════════════════════════════

export type ModalSize = 'sm' | 'md' | 'lg' | 'xl' | 'full';

// ═══════════════════════════════════════════════════════════════════
// Accordion Types
// ═══════════════════════════════════════════════════════════════════

export interface AccordionItem {
	id: string;
	title: string;
	disabled?: boolean;
	/** Initially expanded */
	expanded?: boolean;
	/** Icon override */
	icon?: string;
}

// ═══════════════════════════════════════════════════════════════════
// Command Palette Types
// ═══════════════════════════════════════════════════════════════════

export interface CommandItem {
	id: string;
	label: string;
	/** Category grouping */
	category?: string;
	/** Keyboard shortcut hint */
	shortcut?: string;
	/** Icon */
	icon?: string;
	/** Action to execute */
	action: () => void;
	/** Whether item is active/enabled */
	disabled?: boolean;
}

export interface CommandGroup {
	label: string;
	items: CommandItem[];
}

// ═══════════════════════════════════════════════════════════════════
// TreeView Types
// ═══════════════════════════════════════════════════════════════════

export interface TreeNode<T = unknown> {
	id: string;
	label: string;
	children?: TreeNode<T>[];
	/** Custom data payload */
	data?: T;
	/** Initially expanded */
	expanded?: boolean;
	disabled?: boolean;
	/** Show checkbox */
	checkable?: boolean;
	checked?: boolean;
	/** Icon */
	icon?: string;
}

// ═══════════════════════════════════════════════════════════════════
// Infinite Scroll Types
// ═══════════════════════════════════════════════════════════════════

export interface InfiniteScrollState {
	loading: boolean;
	hasMore: boolean;
	page: number;
	error: string | null;
}

// ═══════════════════════════════════════════════════════════════════
// Universal Reactive Store Types (outside components)
// ═══════════════════════════════════════════════════════════════════

/** Theme mode */
export type ThemeMode = 'light' | 'dark' | 'system';

/** Undo/Redo state */
export interface UndoRedoState<T> {
	past: T[];
	present: T;
	future: T[];
}

/** Media query breakpoint */
export interface MediaBreakpoint {
	name: string;
	query: string;
}

/** LocalStorage sync options */
export interface LocalStoreOptions<T> {
	key: string;
	defaultValue: T;
	serialize?: (value: T) => string;
	deserialize?: (raw: string) => T;
}
