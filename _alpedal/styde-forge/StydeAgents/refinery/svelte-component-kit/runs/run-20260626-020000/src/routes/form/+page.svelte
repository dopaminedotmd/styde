<script lang="ts">
	import Form from '$lib/components/Form.svelte';
	import type { FormField, FormStep, ValidationRule } from '$lib/types';

	const passwordMin: ValidationRule = {
		name: 'minLength',
		validate: (value) => typeof value === 'string' && value.length >= 8 ? true : 'Minimum 8 characters required.',
	};

	const fields: FormField[] = [
		{ name: 'fullName', label: 'Full Name', type: 'text', required: true, helpText: 'Your legal full name.' },
		{ name: 'email', label: 'Email', type: 'email', required: true },
		{ name: 'password', label: 'Password', type: 'password', required: true, rules: [passwordMin] },
		{ name: 'bio', label: 'Bio', type: 'textarea', placeholder: 'Tell us about yourself…' },
		{ name: 'birthdate', label: 'Birth Date', type: 'date' },
		{ name: 'agreedToTerms', label: 'I agree to the terms', type: 'checkbox', required: true },
	];

	const steps: FormStep[] = [
		{ id: 'account', title: 'Account', description: 'Create your account details.', fields: ['fullName', 'email', 'password'] },
		{ id: 'profile', title: 'Profile', description: 'Tell us about yourself.', fields: ['bio', 'birthdate'] },
		{ id: 'confirm', title: 'Confirm', description: 'Review and agree.', fields: ['agreedToTerms'] },
	];

	async function handleSubmit(values: Record<string, unknown>) {
		console.log('Submitting:', values);
		await new Promise((r) => setTimeout(r, 1500));
	}
</script>

<div class="page">
	<h1>📝 Form Component</h1>
	<p class="subtitle">v2: Multi-step wizard with async validation, dependent fields, $inspect, and $host.</p>
	<Form {fields} {steps} validateOn="blur" onSubmit={handleSubmit} submitLabel="Create Account" showReset />
</div>

<style>
	.page { padding: 24px 32px; max-width: 600px; }
	h1 { font-size: 1.5rem; margin: 0 0 4px; }
	.subtitle { color: #64748b; margin: 0 0 20px; font-size: 0.9rem; }
</style>
