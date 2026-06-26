<script lang="ts">
	/**
	 * Form — Svelte 5 Component
	 * ==========================
	 * A declarative form builder with real-time validation using Svelte 5 runes.
	 *
	 * ## Features
	 * - Declarative field definitions via props
	 * - Real-time validation as user types (or on blur/submit)
	 * - Custom validation rules with error messages
	 * - Field-level and form-level error display
	 * - Submit handling with loading/disabled states
	 * - Accessible: labels, aria attributes, error announcements
	 *
	 * ## Usage
	 * ```svelte
	 * <Form {fields} {onSubmit} validateOn="blur" />
	 * ```
	 *
	 * ## Runes Used
	 * - `$state`  — formValues, errors, touched, isSubmitting
	 * - `$derived` — isValid, fieldErrors
	 * - `$effect`  — announce validation changes to screen readers
	 */

	import type { FormField, ValidationRule } from '../types';

	// ─── Props ──────────────────────────────────────────────────────
	interface Props {
		fields: FormField[];
		/** Validation trigger: 'change' | 'blur' | 'submit' */
		validateOn?: 'change' | 'blur' | 'submit';
		/**
		 * Submit handler. Receives form values, touched map, and a setErrors callback.
		 * Return void or throw to signal failure.
		 */
		onSubmit?: (values: Record<string, unknown>) => Promise<void> | void;
		/** Initial values (overrides field defaults) */
		initialValues?: Record<string, unknown>;
		/** CSS class for the form element */
		class?: string;
		/** Submit button label */
		submitLabel?: string;
		/** Show a reset button? */
		showReset?: boolean;
	}

	let {
		fields,
		validateOn = 'submit',
		onSubmit,
		initialValues = {},
		class: className = '',
		submitLabel = 'Submit',
		showReset = false
	}: Props = $props();

	// ─── Initialize form values ─────────────────────────────────────
	function initValues(): Record<string, unknown> {
		const vals: Record<string, unknown> = {};
		for (const f of fields) {
			vals[f.name] = initialValues[f.name] ?? f.defaultValue ?? '';
		}
		return vals;
	}

	// ─── State (Svelte 5 runes) ─────────────────────────────────────
	let formValues = $state<Record<string, unknown>>(initValues());
	let errors = $state<Record<string, string>>({});
	let touched = $state<Record<string, boolean>>({});
	let isSubmitting = $state(false);
	let submitError = $state<string | null>(null);
	let submitSuccess = $state(false);

	// ─── Derived ────────────────────────────────────────────────────
	const isValid = $derived.by(() => {
		if (Object.keys(errors).length > 0) return false;
		for (const f of fields) {
			if (f.required && !formValues[f.name]) return false;
		}
		return true;
	});

	const hasFieldErrors = $derived(Object.keys(errors).length > 0);

	// ─── Validation ─────────────────────────────────────────────────
	function validateField(name: string): string | null {
		const field = fields.find((f) => f.name === name);
		if (!field) return null;

		const value = formValues[name];

		// Required check
		if (field.required) {
			if (value === '' || value === null || value === undefined) {
				return `${field.label} is required.`;
			}
			if (Array.isArray(value) && value.length === 0) {
				return `${field.label} is required.`;
			}
		}

		// Run custom rules
		if (field.rules) {
			for (const rule of field.rules) {
				const result = rule.validate(value, formValues);
				if (result !== true) return result;
			}
		}

		// HTML5-type checks
		if (field.type === 'email' && typeof value === 'string' && value) {
			if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
				return 'Please enter a valid email address.';
			}
		}

		return null;
	}

	function validateAll(): boolean {
		const newErrors: Record<string, string> = {};
		for (const f of fields) {
			const err = validateField(f.name);
			if (err) newErrors[f.name] = err;
			touched[f.name] = true;
		}
		errors = newErrors;
		return Object.keys(newErrors).length === 0;
	}

	// ─── Handlers ───────────────────────────────────────────────────
	function handleChange(name: string, value: unknown) {
		formValues = { ...formValues, [name]: value };

		if (validateOn === 'change') {
			const err = validateField(name);
			errors = { ...errors, [name]: err || '' };
			// Remove key if no error
			if (!err) {
				const newErrors = { ...errors };
				delete newErrors[name];
				errors = newErrors;
			}
		}

		submitError = null;
		submitSuccess = false;
	}

	function handleBlur(name: string) {
		touched = { ...touched, [name]: true };

		if (validateOn === 'blur') {
			const err = validateField(name);
			if (err) {
				errors = { ...errors, [name]: err };
			} else {
				const newErrors = { ...errors };
				delete newErrors[name];
				errors = newErrors;
			}
		}
	}

	async function handleSubmit(e: Event) {
		e.preventDefault();
		submitError = null;
		submitSuccess = false;

		// Mark all touched
		const allTouched: Record<string, boolean> = {};
		for (const f of fields) allTouched[f.name] = true;
		touched = allTouched;

		if (!validateAll()) return;

		if (!onSubmit) return;

		isSubmitting = true;
		try {
			await onSubmit({ ...formValues });
			submitSuccess = true;
		} catch (err) {
			submitError = err instanceof Error ? err.message : 'Submission failed.';
		} finally {
			isSubmitting = false;
		}
	}

	function handleReset() {
		formValues = initValues();
		errors = {};
		touched = {};
		submitError = null;
		submitSuccess = false;
	}

	function getFieldError(name: string): string | undefined {
		return errors[name] || undefined;
	}

	// ─── Derived field errors list for screen readers ───────────────
	const liveErrors = $derived(
		Object.values(errors).filter(Boolean).join('. ')
	);

	$effect(() => {
		// ARIA live region picks up error changes
		void liveErrors;
	});
</script>

<form class="s5-form {className}" onsubmit={handleSubmit} onreset={handleReset} novalidate>
	{#if submitError}
		<div class="s5-form-alert s5-form-alert-error" role="alert">
			{submitError}
		</div>
	{/if}

	{#if submitSuccess}
		<div class="s5-form-alert s5-form-alert-success" role="status">
			✓ Form submitted successfully!
		</div>
	{/if}

	{#each fields as field}
		<div class="s5-form-field">
			<label class="s5-form-label" for="s5-f-{field.name}">
				{field.label}
				{#if field.required}
					<span class="s5-form-required" aria-hidden="true">*</span>
				{/if}
			</label>

			{#if field.type === 'textarea'}
				<textarea
					id="s5-f-{field.name}"
					class="s5-form-input s5-form-textarea"
					class:has-error={!!getFieldError(field.name) && touched[field.name]}
					placeholder={field.placeholder ?? ''}
					value={String(formValues[field.name] ?? '')}
					oninput={(e) => handleChange(field.name, e.currentTarget.value)}
					onblur={() => handleBlur(field.name)}
					aria-invalid={!!getFieldError(field.name) && touched[field.name]}
					aria-describedby={getFieldError(field.name) ? 's5-err-' + field.name : undefined}
				></textarea>

			{:else if field.type === 'select'}
				<select
					id="s5-f-{field.name}"
					class="s5-form-input s5-form-select"
					class:has-error={!!getFieldError(field.name) && touched[field.name]}
					value={String(formValues[field.name] ?? '')}
					onchange={(e) => handleChange(field.name, e.currentTarget.value)}
					onblur={() => handleBlur(field.name)}
					aria-invalid={!!getFieldError(field.name) && touched[field.name]}
					aria-describedby={getFieldError(field.name) ? 's5-err-' + field.name : undefined}
				>
					<option value="">-- Select --</option>
					{#each field.options ?? [] as opt}
						<option value={opt.value}>{opt.label}</option>
					{/each}
				</select>

			{:else if field.type === 'checkbox'}
				<div class="s5-form-checkbox-wrap">
					<input
						type="checkbox"
						id="s5-f-{field.name}"
						class="s5-form-checkbox"
						checked={!!formValues[field.name]}
						onchange={(e) => handleChange(field.name, e.currentTarget.checked)}
						onblur={() => handleBlur(field.name)}
						aria-invalid={!!getFieldError(field.name) && touched[field.name]}
						aria-describedby={getFieldError(field.name) ? 's5-err-' + field.name : undefined}
					/>
					<span class="s5-form-checkbox-label">{field.placeholder ?? field.label}</span>
				</div>

			{:else}
				<input
					type={field.type}
					id="s5-f-{field.name}"
					class="s5-form-input"
					class:has-error={!!getFieldError(field.name) && touched[field.name]}
					placeholder={field.placeholder ?? ''}
					value={String(formValues[field.name] ?? '')}
					oninput={(e) => handleChange(field.name, e.currentTarget.value)}
					onblur={() => handleBlur(field.name)}
					aria-invalid={!!getFieldError(field.name) && touched[field.name]}
					aria-describedby={getFieldError(field.name) ? 's5-err-' + field.name : undefined}
				/>
			{/if}

			{#if getFieldError(field.name) && touched[field.name]}
				<span id="s5-err-{field.name}" class="s5-form-error" role="alert">
					{getFieldError(field.name)}
				</span>
			{/if}
		</div>
	{/each}

	<!-- Screen-reader-only live region for error announcements -->
	<div class="sr-only" aria-live="assertive" aria-atomic="true">
		{#if liveErrors}
			{liveErrors}
		{/if}
	</div>

	<div class="s5-form-actions">
		<button
			type="submit"
			class="s5-form-submit"
			disabled={isSubmitting || (validateOn === 'change' && hasFieldErrors)}
		>
			{#if isSubmitting}
				<span class="s5-spinner" aria-hidden="true"></span>
				Submitting…
			{:else}
				{submitLabel}
			{/if}
		</button>

		{#if showReset}
			<button type="reset" class="s5-form-reset" disabled={isSubmitting}>Reset</button>
		{/if}
	</div>
</form>

<style>
	.s5-form {
		max-width: 560px;
		display: flex;
		flex-direction: column;
		gap: 16px;
	}

	.s5-form-alert {
		padding: 10px 14px;
		border-radius: 6px;
		font-size: 0.9rem;
	}
	.s5-form-alert-error {
		background: #fef2f2;
		color: #b91c1c;
		border: 1px solid #fecaca;
	}
	.s5-form-alert-success {
		background: #f0fdf4;
		color: #15803d;
		border: 1px solid #bbf7d0;
	}

	.s5-form-field {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.s5-form-label {
		font-size: 0.85rem;
		font-weight: 600;
		color: #374151;
	}

	.s5-form-required {
		color: #ef4444;
		margin-left: 2px;
	}

	.s5-form-input {
		padding: 8px 12px;
		border: 1px solid #d1d5db;
		border-radius: 6px;
		font-size: 0.9rem;
		transition: border-color 0.15s, box-shadow 0.15s;
		outline: none;
		font-family: inherit;
	}
	.s5-form-input:focus {
		border-color: #6366f1;
		box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
	}
	.s5-form-input.has-error {
		border-color: #ef4444;
	}
	.s5-form-input.has-error:focus {
		box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15);
	}

	.s5-form-textarea {
		min-height: 80px;
		resize: vertical;
	}

	.s5-form-select {
		appearance: none;
		background: #fff url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'><path fill='%236b7280' d='M6 8L1 3h10z'/></svg>") no-repeat right 10px center;
		padding-right: 30px;
	}

	.s5-form-checkbox-wrap {
		display: flex;
		align-items: center;
		gap: 8px;
	}
	.s5-form-checkbox {
		width: 18px;
		height: 18px;
		accent-color: #6366f1;
	}
	.s5-form-checkbox-label {
		font-size: 0.9rem;
		color: #374151;
	}

	.s5-form-error {
		font-size: 0.8rem;
		color: #ef4444;
		margin-top: 2px;
	}

	.s5-form-actions {
		display: flex;
		gap: 10px;
		padding-top: 4px;
	}

	.s5-form-submit {
		padding: 10px 22px;
		background: #6366f1;
		color: #fff;
		border: none;
		border-radius: 6px;
		font-weight: 600;
		font-size: 0.9rem;
		cursor: pointer;
		display: flex;
		align-items: center;
		gap: 6px;
		transition: background 0.15s;
	}
	.s5-form-submit:hover:not(:disabled) {
		background: #4f46e5;
	}
	.s5-form-submit:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.s5-form-reset {
		padding: 10px 18px;
		background: #fff;
		color: #6b7280;
		border: 1px solid #d1d5db;
		border-radius: 6px;
		font-size: 0.9rem;
		cursor: pointer;
		transition: all 0.15s;
	}
	.s5-form-reset:hover:not(:disabled) {
		background: #f9fafb;
	}
	.s5-form-reset:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.s5-spinner {
		display: inline-block;
		width: 14px;
		height: 14px;
		border: 2px solid rgba(255,255,255,0.3);
		border-top-color: #fff;
		border-radius: 50%;
		animation: s5-spin 0.6s linear infinite;
	}

	@keyframes s5-spin {
		to { transform: rotate(360deg); }
	}

	.sr-only {
		position: absolute;
		width: 1px;
		height: 1px;
		padding: 0;
		margin: -1px;
		overflow: hidden;
		clip: rect(0,0,0,0);
		white-space: nowrap;
		border: 0;
	}
</style>
