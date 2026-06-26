import { LitElement, html, css } from 'lit';
import { state } from 'lit/decorators.js';

/**
 * SiteShell — single integration point between Forge SPA page content
 * and the broader styde.se chrome.
 *
 * Composes nav-bar, breadcrumb, main content slot, and footer.
 * Handles scroll listeners, wires progress bar to router events.
 *
 * Framework-agnostic web component accepted by both Lit SPA and Astro pages.
 */
export class SiteShell extends LitElement {
  static styles = css`
    :host {
      display: flex;
      flex-direction: column;
      min-height: 100vh;
    }

    .chrome-slot {
      display: block;
    }

    .content-wrapper {
      flex: 1;
      display: flex;
      flex-direction: column;
      padding-top: var(--nav-height, 56px);
      position: relative;
    }

    .content-area {
      flex: 1;
      display: flex;
      flex-direction: column;
      min-height: calc(100vh - var(--nav-height, 56px) - var(--breadcrumb-height, 32px) - var(--footer-min-height, 48px));
    }

    .content-area.no-breadcrumb {
      min-height: calc(100vh - var(--nav-height, 56px) - var(--footer-min-height, 48px));
    }

    slot[name='content']::slotted(*) {
      flex: 1;
    }

    .sidebar-layout {
      display: flex;
      flex: 1;
      width: 100%;
    }

    slot[name='sidebar']::slotted(*) {
      width: 240px;
      flex-shrink: 0;
      border-right: 1px solid var(--border, #d2d2d7);
      background: var(--surface-2, #f5f5f7);
    }

    slot[name='content']::slotted(*) {
      flex: 1;
      min-width: 0;
    }

    @media (max-width: 768px) {
      .sidebar-layout {
        flex-direction: column;
      }
      slot[name='sidebar']::slotted(*) {
        width: 100%;
        border-right: none;
        border-bottom: 1px solid var(--border, #d2d2d7);
      }
    }
  `;

  @state()
  private _breadcrumbVisible = true;

  @state()
  private _hasSidebar = false;

  private _boundProgressStart: (e: Event) => void;
  private _boundProgressComplete: (e: Event) => void;

  constructor() {
    super();
    this._boundProgressStart = () =>
      document.dispatchEvent(new CustomEvent('progress:start'));
    this._boundProgressComplete = () =>
      document.dispatchEvent(new CustomEvent('progress:complete'));
  }

  connectedCallback() {
    super.connectedCallback();
    // Listen for route changes on document to fire progress events
    // Compatible with both Lit Router and Astro view transitions
    document.addEventListener('router:navigate', this._boundProgressStart);
    document.addEventListener('router:ready', this._boundProgressComplete);
    // Astro view transition events
    document.addEventListener('astro:before-swap', this._boundProgressStart);
    document.addEventListener('astro:after-swap', this._boundProgressComplete);
  }

  disconnectedCallback() {
    super.disconnectedCallback();
    document.removeEventListener('router:navigate', this._boundProgressStart);
    document.removeEventListener('router:ready', this._boundProgressComplete);
    document.removeEventListener('astro:before-swap', this._boundProgressStart);
    document.removeEventListener('astro:after-swap', this._boundProgressComplete);
  }

  private _onSlotChange(e: Event) {
    const slot = e.target as HTMLSlotElement;
    if (slot.name === 'sidebar') {
      const nodes = slot.assignedNodes({ flatten: true });
      this._hasSidebar = nodes.length > 0;
    }
  }

  render() {
    const contentStyles = this._breadcrumbVisible ? '' : 'no-breadcrumb';

    return html`
      <site-progress-bar></site-progress-bar>

      <site-nav-bar></site-nav-bar>

      <div class="content-wrapper">
        <site-breadcrumb
          .loading=${false}
          .error=${false}
          style=${this._breadcrumbVisible ? 'display: block;' : 'display: none;'}
        ></site-breadcrumb>

        <div class="content-area ${contentStyles}">
          <div class="sidebar-layout">
            <slot name="sidebar" @slotchange=${this._onSlotChange}></slot>
            <slot name="content"></slot>
          </div>
        </div>
      </div>

      <site-footer></site-footer>
    `;
  }
}

customElements.define('site-shell', SiteShell);
