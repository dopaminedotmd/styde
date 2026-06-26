<script lang="ts">
	/**
	 * Form v2 — Svelte 5 Advanced Component
	 * =======================================
	 * Enhanced form builder with async validation, dependent fields,
	 * $inspect debugging, $host element reference, and multi-step support.
	 *
	 * ## v2 Improvements (c2)
	 * - Async validation rules with loading indicators
	 * - Dependent field re-validation (dependsOn)
	 * - $inspect traces validation and submission state
	 * - $host for form element direct access
	 * - Multi-step form support via steps prop
	 * - Conditional field visibility
	 * - Help text per field
	 * - Date, tel, url input types
	 * - Snippet slots for custom submit area
	 */

	import type { FormField, FormStep } from '../types';

	interface Props {
		fields: FormField[];
		validateOn?: 'change' | 'blur' | 'submit';
		onSubmit?: (values: Record<string, unknown>) => Promise<void> | void;
		initialValues?: Record<string, unknown>;
		class?: string;
		submitLabel?: string;
		showReset?: boolean;
		/** Multi-step form steps */
		steps?: FormStep[];
		/** Snippet for custom actions area */
		actions?: import('svelte').Snippet;
	}

	let {
		fields,
		validateOn = 'submit',
		onSubmit,
		initialValues = {},
		class: className = '',
		submitLabel = 'Submit',
		showReset = false,
		steps,
		actions
	}: Props = $props();

	// $host — direct reference to the <form> element
	let formEl = $host<HTMLFormElement>();

	function initValues(): Record<string, unknown> {
		const vals: Record<string, unknown> = {};
		for (const f of fields) {
			vals[f.name] = initialValues[f.name] ?? f.defaultValue ?? '';
		}
		return vals;
	}

	let formValues = $state<Record<string, unknown>>(initValues());
	let errors = $state<Record<string, string>>({});
	let asyncErrors = $state<Record<string, string>>({});
	let touched = $state<Record<string, boolean>>({});
	let isSubmitting = $state(false);
	let isAsyncValidating = $state<Record<string, boolean>>({});
	let submitError = $state<string | null>(null);
	let submitSuccess = $state(false);
	let currentStep = $state(0);

	// $inspect — trace key state in dev mode
	$inspect('Form values:', Object.keys(formValues).length);
	$inspect('Form errors:', Object.keys(errors).length);
	$inspect('Form valid:', !Object.keys(errors).length && !Object.keys(asyncErrors).length);
	$inspect('Form element:', formEl);

	const isValid = $derived.by(() => {
		if (Object.keys(errors).length > 0) return false;
		if (Object.keys(asyncErrors).length > 0) return false;
		for (const f of fields) {
			if (f.required && !formValues[f.name]) return false;
		}
		return true;
	});

	const hasFieldErrors = $derived(Object.keys(errors).length > 0 || Object.keys(asyncErrors).length > 0);

	// Current step's fields
	const currentStepFields = $derived(
		steps && steps[currentStep]
			? fields.filter((f) => steps![currentStep].fields.includes(f.name))
			: fields
	);

	const stepCount = $derived(steps ? steps.length : 1);

	// ─── Validation ─────────────────────────────────────────────────
	function validateField(name: string): string | null {
		const field = fields.find((f) => f.name === name);
		if (!field) return null;
		const value = formValues[name];

		if (field.required) {
			if (value === '' || value === null || value === undefined) return `${field.label} is required.`;
			if (Array.isArray(value) && value.length === 0) return `${field.label} is required.`;
		}

		if (field.rules) {
			for (const rule of field.rules) {
				const result = rule.validate(value, formValues);
				if (result !== true) return result;
			}
		}

		// HTML5 type checks
		if (field.type === 'email' && typeof value === 'string' && value) {
			if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return 'Please enter a valid email address.';
		}

		return null;
	}

	async function validateFieldAsync(name: string): Promise<string | null> {
		const field = fields.find((f) => f.name === name);
		if (!field || !field.asyncRules) return null;
		const value = formValues[name];

		for (const rule of field.asyncRules) {
			const result = await rule.validate(value, formValues);
			if (result !== true) return result;
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
	async function handleChange(name: string, value: unknown) {
		formValues = { ...formValues, [name]: value };

		if (validateOn === 'change') {
			const err = validateField(name);
			const newErrors = { ...errors };
			if (err) newErrors[name] = err;
			else delete newErrors[name];
			errors = newErrors;
		}

		// Re-validate dependent fields
		for (const f of fields) {
			if (f.dependsOn === name && touched[f.name]) {
				const err = validateField(f.name);
				const newErrors = { ...errors };
				if (err) newErrors[f.name] = err;
				else delete newErrors[f.name];
				errors = newErrors;
			}
		}

		submitError = null;
		submitSuccess = false;
	}

	async function handleBlur(name: string) {
		touched = { ...touched, [name]: true };

		if (validateOn === 'blur' || validateOn === 'change') {
			const err = validateField(name);
			const newErrors = { ...errors };
			if (err) newErrors[name] = err;
			else delete newErrors[name];
			errors = newErrors;
		}

		// Async validation on blur
		const field = fields.find((f) => f.name === name);
		if (field?.asyncRules && formValues[name]) {
			isAsyncValidating = { ...isAsyncValidating, [name]: true };
			const err = await validateFieldAsync(name);
			const newAsyncErrors = { ...asyncErrors };
			if (err) newAsyncErrors[name] = err;
			else delete newAsyncErrors[name];
			asyncErrors = newAsyncErrors;
			isAsyncValidating = { ...isAsyncValidating, [name]: false };
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

		// Run async validations
		for (const f of fields) {
			if (f.asyncRules) {
				isAsyncValidating = { ...isAsyncValidating, [f.name]: true };
				const err = await validateFieldAsync(f.name);
				const newAsyncErrors = { ...asyncErrors };
				if (err) newAsyncErrors[f.name] = err;
				else delete newAsyncErrors[f.name];
				asyncErrors = newAsyncErrors;
				isAsyncValidating = { ...isAsyncValidating, [f.name]: false };
			}
		}

		if (Object.keys(asyncErrors).length > 0) return;
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
		asyncErrors = {};
		touched = {};
		isAsyncValidating = {};
		submitError = null;
		submitSuccess = false;
		currentStep = 0;
	}

	function getFieldError(name: string): string | undefined {
		return errors[name] || asyncErrors[name] || undefined;
	}

	function isFieldVisible(field: FormField): boolean {
		if (!field.visible) return true;
		return field.visible(formValues);
	}

	// Step validation
	function validateStep(): boolean {
		const stepFields = currentStepFields;
		const newErrors: Record<string, string> = {};
		for (const f of stepFields) {
			const err = validateField(f.name);
			if (err) newErrors[f.name] = err;
			touched[f.name] = true;
		}
		errors = { ...errors, ...newErrors };
		// Clear errors for fields validated in this step
		for (const f of stepFields) {
			if (!newErrors[f.name]) {
				const e = { ...errors };
				delete e[f.name];
				errors = e;
			}
		}
		return Object.keys(newErrors).length === 0;
	}

	function nextStep() {
		if (validateStep() && currentStep < stepCount - 1) currentStep++;
	}

	function prevStep() {
		if (currentStep > 0) currentStep--;
	}

	const liveErrors = $derived(
		[...Object.values(errors), ...Object.values(asyncErrors)]
			.filter(Boolean)
			.join('. ')
	);

	$effect(() => { void liveErrors; });
</script>

<form class="s5-form {className}" onsubmit={handleSubmit} onreset={handleReset} novalidate bind:this={formEl}>
	{#if submitError}
		<div class="s5-form-alert s5-form-alert-error" role="alert">{submitError}</div>
	{/if}
	{#if submitSuccess}
		<div class="s5-form-alert s5-form-alert-success" role="status">✓ Form submitted successfully!</div>
	{/if}

	{#if steps && steps.length > 1}
		<div class="s5-form-stepper">
			{#each steps as step, i}
				<button
					type="button"
					class="s5-form-step-indicator"
					class:active={i === currentStep}
					class:completed={i < currentStep}
					onclick={() => { if (i < currentStep) currentStep = i; }}
					aria-label="Step {i + 1}: {step.title}"
				>
					<span class="s5-form-step-num">{i + 1}</span>
					<span class="s5-form-step-label">{step.title}</span>
				</button>
			{/each}
		</div>
		{#if steps[currentStep]?.description}
			<p class="s5-form-step-desc">{steps[currentStep].description}</p>
		{/if}
	{/if}

	{#each currentStepFields as field}
		{#if isFieldVisible(field)}
			<div class="s5-form-field">
				<label class="s5-form-label" for="s5-f-{field.name}">
					{field.label}
					{#if field.required}<span class="s5-form-required" aria-hidden="true">*</span>{/if}
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

				{#if field.helpText}
					<span class="s5-form-help">{field.helpText}</span>
				{/if}

				{#if isAsyncValidating[field.name]}
					<span class="s5-form-validating">Checking…</span>
				{/if}

				{#if getFieldError(field.name) && touched[field.name]}
					<span id="s5-err-{field.name}" class="s5-form-error" role="alert">
						{getFieldError(field.name)}
					</span>
				{/if}
			</div>
		{/if}
	{/each}

	<div class="sr-only" aria-live="assertive" aria-atomic="true">
		{#if liveErrors}{liveErrors}{/if}
	</div>

	<div class="s5-form-actions">
		{#if steps && steps.length > 1}
			<button type="button" class="s5-form-reset" disabled={currentStep === 0} onclick={prevStep}>← Back</button>
			{#if currentStep < stepCount - 1}
				<button type="button" class="s5-form-submit" onclick={nextStep}>Next →</button>
			{:else}
				<button type="submit" class="s5-form-submit" disabled={isSubmitting || (validateOn === 'change' && hasFieldErrors)}>
					{#if isSubmitting}<span class="s5-spinner" aria-hidden="true"></span>Submitting…{:else}{submitLabel}{/if}
				</button>
			{/if}
		{:else if actions}
			{@render actions()}
		{:else}
			<button type="submit" class="s5-form-submit" disabled={isSubmitting || (validateOn === 'change' && hasFieldErrors)}>
				{#if isSubmitting}<span class="s5-spinner" aria-hidden="true"></span>Submitting…{:else}{submitLabel}{/if}
			</button>
			{#if showReset}<button type="reset" class="s5-form-reset" disabled={isSubmitting}>Reset</button>{/if}
		{/if}
	</div>
</form>

<style>
	.s5-form { max-width: 560px; display: flex; flex-direction: column; gap: 16px; }

	.s5-form-alert { padding: 10px 14px; border-radius: 6px; font-size: 0.9rem; }
	.s5-form-alert-error { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
	.s5-form-alert-success { background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }

	/* Stepper */
	.s5-form-stepper { display: flex; gap: 4px; }
	.s5-form-step-indicator {
		display: flex; align-items: center; gap: 6px; padding: 6px 12px;
		border: 1px solid #e2e8f0; border-radius: 6px; background: #fff;
		font-size: 0.8rem; cursor: pointer; transition: all 0.15s;
	}
	.s5-form-step-indicator.active { border-color: #6366f1; background: #eef2ff; color: #6366f1; }
	.s5-form-step-indicator.completed { border-color: #22c55e; background: #f0fdf4; color: #22c55e; }
	.s5-form-step-num { width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-weight: 700; font-size: 0.75rem; background: #e2e8f0; color: #64748b; }
	.s5-form-step-indicator.active .s5-form-step-num { background: #6366f1; color: #fff; }
	.s5-form-step-indicator.completed .s5-form-step-num { background: #22c55e; color: #fff; }
	.s5-form-step-desc { font-size: 0.85rem; color: #64748b; margin: 0; }

	.s5-form-field { display: flex; flex-direction: column; gap: 4px; }
	.s5-form-label { font-size: 0.85rem; font-weight: 600; color: #374151; }
	.s5-form-required { color: #ef4444; margin-left: 2px; }

	.s5-form-input {
		padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px;
		font-size: 0.9rem; transition: border-color 0.15s, box-shadow 0.15s;
		outline: none; font-family: inherit;
	}
	.s5-form-input:focus { border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,0.15); }
	.s5-form-input.has-error { border-color: #ef4444; }
	.s5-form-input.has-error:focus { box-shadow: 0 0 0 3px rgba(239,68,68,0.15); }
	.s5-form-textarea { min-height: 80px; resize: vertical; }
	.s5-form-select { appearance: none; background: #fff url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'><path fill='%236b7280' d='M6 8L1 3h10z'/></svg>") no-repeat right 10px center; padding-right: 30px; }

	.s5-form-checkbox-wrap { display: flex; align-items: center; gap: 8px; }
	.s5-form-checkbox { width: 18px; height: 18px; accent-color: #6366f1; }
	.s5-form-checkbox-label { font-size: 0.9rem; color: #374151; }

	.s5-form-help { font-size: 0.78rem; color: #94a3b8; }
	.s5-form-validating { font-size: 0.78rem; color: #6366f1; font-style: italic; }
	.s5-form-error { font-size: 0.8rem; color: #ef4444; margin-top: 2px; }

	.s5-form-actions { display: flex; gap: 10px; padding-top: 4px; }
	.s5-form-submit {
		padding: 10px 22px; background: #6366f1; color: #fff; border: none;
		border-radius: 6px; font-weight: 600; font-size: 0.9rem; cursor: pointer;
		display: flex; align-items: center; gap: 6px; transition: background 0.15s;
	}
	.s5-form-submit:hover:not(:disabled) { background: #4f46e5; }
	.s5-form-submit:disabled { opacity: 0.6; cursor: not-allowed; }

	.s5-form-reset {
		padding: 10px 18px; background: #fff; color: #6b7280;
		border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.9rem;
		cursor: pointer; transition: all 0.15s;
	}
	.s5-form-reset:hover:not(:disabled) { background: #f9fafb; }
	.s5-form-reset:disabled { opacity: 0.6; cursor: not-allowed; }

	.s5-spinner { display: inline-block; width: 14px; height: 14px; border: 2px solid rgba(255,255,255,0.3); border-top-color: #fff; border-radius: 50%; animation: s5-spin 0.6s linear infinite; }
	@keyframes s5-spin { to { transform: rotate(360deg); } }

	.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }
</style>
