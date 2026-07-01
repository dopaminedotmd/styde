task: build form-associated web component with shadow dom and slots
name: styde-input
kind: form-associated custom element
-- styde-input.js --
class StydeInput extends HTMLElement {
  static formAssociated = true
  static observedAttributes = ['value', 'placeholder', 'label', 'disabled', 'required', 'variant']
  constructor() {
    super()
    this._internals = this.attachInternals()
    this._shadow = this.attachShadow({ mode: 'open', delegatesFocus: true })
    this._value = ''
    this._render()
  }
  // -- lifecycle
  connectedCallback() {
    this._internals.setFormValue(this._value)
    this._input?.addEventListener('input', this)
    this._input?.addEventListener('change', this)
  }
  disconnectedCallback() {
    this._input?.removeEventListener('input', this)
    this._input?.removeEventListener('change', this)
  }
  attributeChangedCallback(name, old, value) {
    if (old === value) return
    if (name === 'value') { this._value = value ?? ''; this._internals.setFormValue(this._value) }
    if (name === 'disabled') this._input?.toggleAttribute('disabled', value !== null)
    if (name === 'placeholder') this._input?.setAttribute('placeholder', value ?? '')
    if (name === 'label') this._labelEl && (this._labelEl.textContent = value ?? '')
    if (name === 'variant') this._applyVariant(value)
  }
  handleEvent(e) {
    if (e.type === 'input') {
      this._value = e.target.value
      this._internals.setFormValue(this._value)
      this.dispatchEvent(new CustomEvent('styde-input', { bubbles: true, composed: true, detail: { value: this._value } }))
    }
  }
  // -- form association api
  get form() { return this._internals.form }
  get value() { return this._value }
  set value(v) { this._value = String(v ?? ''); this._input && (this._input.value = this._value); this._internals.setFormValue(this._value) }
  get disabled() { return this.hasAttribute('disabled') }
  set disabled(v) { v ? this.setAttribute('disabled', '') : this.removeAttribute('disabled') }
  get name() { return this.getAttribute('name') ?? '' }
  get type() { return 'text' }
  get validity() { return this._internals.validity }
  get validationMessage() { return this._internals.validationMessage }
  checkValidity() { return this._internals.checkValidity() }
  reportValidity() { return this._internals.reportValidity() }
  _applyVariant(variant) {
    const root = this._shadow.querySelector('.wrapper')
    if (!root) return
    root.className = 'wrapper'
    if (variant) root.classList.add(variant)
  }
  _render() {
    this._shadow.innerHTML = `
      <style>
        :host { display: inline-block; font-family: system-ui, sans-serif; --label-color: #374151; --border-color: #d1d5db; --focus-color: #3b82f6; --error-color: #ef4444; --bg: #ffffff; --radius: 6px; --pad: 8px 12px; --font-size: 14px; }
        .wrapper { display: flex; flex-direction: column; gap: 4px; }
        .wrapper.error { --border-color: var(--error-color); --label-color: var(--error-color); }
        .wrapper.success { --border-color: #22c55e; }
        label { font-size: 12px; font-weight: 500; color: var(--label-color); cursor: pointer; }
        .input-container { position: relative; display: flex; align-items: center; }
        input { width: 100%; padding: var(--pad); font-size: var(--font-size); border: 1px solid var(--border-color); border-radius: var(--radius); background: var(--bg); outline: none; transition: border-color 0.15s; box-sizing: border-box; }
        input:focus { border-color: var(--focus-color); box-shadow: 0 0 0 2px color-mix(in srgb, var(--focus-color) 20%, transparent); }
        input:disabled { opacity: 0.5; cursor: not-allowed; background: #f9fafb; }
        slot[name=prefix]::slotted(*) { position: absolute; left: 8px; pointer-events: none; }
        slot[name=suffix]::slotted(*) { position: absolute; right: 8px; pointer-events: none; }
        slot[name=hint]::slotted(*) { font-size: 12px; color: #6b7280; }
        slot[name=error]::slotted(*) { font-size: 12px; color: var(--error-color); display: none; }
        :host(:invalid) slot[name=error]::slotted(*) { display: block; }
        :host(:state(user-invalid)) slot[name=error]::slotted(*) { display: block; }
      </style>
      <div class="wrapper" part="wrapper">
        <label part="label" id="label-el"><slot name="label">Input</slot></label>
        <div class="input-container">
          <slot name="prefix"></slot>
          <input part="input" id="native-input" type="text" autocomplete="off">
          <slot name="suffix"></slot>
        </div>
        <slot name="hint"></slot>
        <slot name="error"></slot>
      </div>
    `
    this._input = this._shadow.getElementById('native-input')
    this._labelEl = this._shadow.getElementById('label-el')
    this._input.setAttribute('aria-labelledby', 'label-el')
  }
}
customElements.define('styde-input', StydeInput)
-- usage example --
<form id="demo-form">
  <styde-input
    name="email"
    label="Email address"
    placeholder="you@example.com"
    value=""
    required
  >
    <span slot="prefix">@</span>
    <span slot="hint">We will never share your email</span>
    <span slot="error">Email is required</span>
  </styde-input>
  <styde-input
    name="password"
    label="Password"
    placeholder="min 8 characters"
    variant="success"
  >
    <span slot="suffix">eye-icon</span>
  </styde-input>
  <button type="submit">Submit</button>
</form>
<script type="module" src="styde-input.js"></script>
-- verification --
skills demonstrated:
  CustomEl: lifecycle callbacks (connected, disconnected, attributeChanged, handleEvent), custom element definition
  Shadow: shadow dom mode open delegatesFocus, scoped styles with part and css custom properties
  Slot: named slots for label prefix suffix hint error composition
  Form: attachInternals setFormValue checkValidity reportValidity validity validationMessage formAssociated static
known limitation: Lit not used because the spec requires zero-dependency baseline. if a lit version is needed, a 2nd blueprint variant can be generated. user can request lit + reactive controllers as an optimization step.