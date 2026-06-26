<script lang="ts">
	/**
	 * Form — SvelteKit Page Example
	 * ==============================
	 * Demonstrates the Form component with declarative field definitions,
	 * custom validation rules, and async submission.
	 */

	import Form from '$lib/components/Form.svelte';
	import type { FormField, ValidationRule } from '$lib/types';

	// ─── Custom validation rules ────────────────────────────────────
	const passwordMinLength: ValidationRule = {
		name: 'minLength',
		validate: (value) => {
			if (typeof value === 'string' && value.length < 8) {
				return 'Password must be at least 8 characters.';
			}
			return true;
		},
	};

	const passwordMatch: ValidationRule = {
		name: 'match',
		validate: (value, allValues) => {
			if (value !== allValues.password) {
				return 'Passwords do not match.';
			}
			return true;
		},
	};

	// ─── Field definitions ──────────────────────────────────────────
	const fields: FormField[] = [
		{
			name: 'fullName',
			label: 'Full Name',
			type: 'text',
			placeholder: 'John Doe',
			required: true,
		},
		{
			name: 'email',
			label: 'Email Address',
			type: 'email',
			placeholder: 'john@example.com',
			required: true,
		},
		{
			name: 'role',
			label: 'Role',
			type: 'select',
			required: true,
			options: [
				{ value: 'admin', label: 'Administrator' },
				{ value: 'editor', label: 'Editor' },
				{ value: 'viewer', label: 'Viewer' },
			],
		},
		{
			name: 'password',
			label: 'Password',
			type: 'password',
			placeholder: 'Min. 8 characters',
			required: true,
			rules: [passwordMinLength],
		},
		{
			name: 'confirmPassword',
			label: 'Confirm Password',
			type: 'password',
			required: true,
			rules: [passwordMatch],
		},
		{
			name: 'bio',
			label: 'Bio',
			type: 'textarea',
			placeholder: 'Tell us about yourself…',
		},
		{
			name: 'newsletter',
			label: 'Subscribe',
			type: 'checkbox',
			placeholder: 'I want to receive the newsletter',
		},
	];

	// ─── Submit handler ─────────────────────────────────────────────
	async function handleSubmit(values: Record<string, unknown>) {
		// Simulate API call
		console.log('Form submitted:', values);
		await new Promise((resolve) => setTimeout(resolve, 1500));
	}

	let validateOn = $state<'change' | 'blur' | 'submit'>('submit');
</script>

<svelte:head>
	<title>Form Example — Svelte 5 Component Kit</title>
</svelte:head>

<div class="page">
	<h1>Form Component</h1>
	<p class="subtitle">
		A declarative form with real-time validation using Svelte 5 runes
		(<code>$state</code>, <code>$derived</code>, <code>$effect</code>).
	</p>

	<div class="validate-control">
		<label>
			Validation mode:
			<select bind:value={validateOn}>
				<option value="submit">On Submit</option>
				<option value="blur">On Blur</option>
				<option value="change">On Change</option>
			</select>
		</label>
	</div>

	<Form
		{fields}
		{validateOn}
		onSubmit={handleSubmit}
		submitLabel="Create Account"
		showReset
		initialValues={{ newsletter: false }}
	/>

	<div class="notes">
		<h2>Features Demonstrated</h2>
		<ul>
			<li>Declarative field definitions (text, email, password, select, textarea, checkbox)</li>
			<li>Custom validation rules (minLength, passwordMatch)</li>
			<li>Three validation modes: submit, blur, change</li>
			<li>Async submission with loading spinner</li>
			<li>Reset button to clear the form</li>
			<li>Screen-reader accessible with ARIA attributes</li>
		</ul>
	</div>
</div>

<style>
	.page {
		max-width: 640px;
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

	.validate-control {
		margin-bottom: 20px;
		font-size: 0.9rem;
		color: #475569;
	}

	.validate-control select {
		margin-left: 6px;
		padding: 4px 8px;
		border: 1px solid #d1d5db;
		border-radius: 4px;
		font-size: 0.9rem;
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
