import { LitElement, html, css } from 'lit';
import { property, state } from 'lit/decorators.js';

interface NavLink {
  label: string;
  href: string;
}

const DEFAULT_NAV_LINKS: NavLink[] = [
  { label: 'Forge', href: '/forge' },
  { label: 'Docs', href: '/docs' },
  { label: 'Community', href: '/community' },
  { label: 'Pricing', href: '/pricing' },
  { label: 'Blog', href: '/blog' },
];

export class SiteNavBar extends LitElement {
  static styles = css`
    :host {
      display: block;
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: var(--nav-height, 56px);
      z-index: var(--z-nav, 1000);
      background: var(--surface-1, #ffffff);
      border-bottom: 1px solid var(--border, #d2d2d7);
      box-shadow: 0 1px 3px var(--shadow, rgba(0, 0, 0, 0.08));
      transition: transform var(--nav-transition, 0.3s ease-out), box-shadow var(--nav-transition, 0.3s ease-out);
      will-change: transform;
    }

    :host(.nav-hidden) {
      transform: translateY(calc(-1 * var(--nav-height, 56px)));
      box-shadow: none;
    }

    .nav-inner {
      display: flex;
      align-items: center;
      height: 100%;
      padding: 0 20px;
      max-width: 1200px;
      margin: 0 auto;
      gap: 24px;
    }

    .logo {
      display: flex;
      align-items: center;
      gap: 8px;
      text-decoration: none;
      color: var(--text-primary, #1d1d1f);
      font-weight: 600;
      font-size: 18px;
      flex-shrink: 0;
    }

    .logo svg {
      width: 28px;
      height: 28px;
    }

    .logo:focus-visible {
      outline: 2px solid var(--accent, #0071e3);
      outline-offset: 4px;
      border-radius: 4px;
    }

    .nav-links {
      display: flex;
      gap: 4px;
      flex: 1;
    }

    .nav-link {
      color: var(--text-secondary, #6e6e73);
      text-decoration: none;
      font-size: 14px;
      padding: 6px 12px;
      border-radius: var(--radius-md, 8px);
      transition: color 0.15s ease, background 0.15s ease;
    }

    .nav-link:hover {
      color: var(--text-primary, #1d1d1f);
      background: var(--surface-2, #f5f5f7);
    }

    .nav-link:focus-visible {
      outline: 2px solid var(--accent, #0071e3);
      outline-offset: 2px;
    }

    .nav-link.active {
      color: var(--accent, #0071e3);
      font-weight: 500;
    }

    .user-area {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-shrink: 0;
    }

    .avatar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: var(--surface-3, #e8e8ed);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      border: none;
      padding: 0;
      color: var(--text-secondary, #6e6e73);
      font-size: 14px;
      transition: box-shadow 0.15s ease;
    }

    .avatar:hover {
      box-shadow: 0 0 0 2px var(--accent, #0071e3);
    }

    .avatar:focus-visible {
      outline: 2px solid var(--accent, #0071e3);
    }

    .btn-signin {
      background: none;
      border: 1px solid var(--border, #d2d2d7);
      color: var(--text-primary, #1d1d1f);
      padding: 6px 14px;
      border-radius: var(--radius-md, 8px);
      font-size: 13px;
      cursor: pointer;
      transition: border-color 0.15s ease, background 0.15s ease;
    }

    .btn-signin:hover {
      border-color: var(--accent, #0071e3);
      background: var(--surface-2, #f5f5f7);
    }

    .btn-getstarted {
      background: var(--accent, #0071e3);
      color: white;
      border: none;
      padding: 6px 14px;
      border-radius: var(--radius-md, 8px);
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      transition: background 0.15s ease;
    }

    .btn-getstarted:hover {
      background: var(--accent-hover, #0077ed);
    }

    .btn-signin:focus-visible,
    .btn-getstarted:focus-visible {
      outline: 2px solid var(--accent, #0071e3);
      outline-offset: 2px;
    }

    /* Skeleton loading state */
    .skeleton-bar {
      display: flex;
      align-items: center;
      height: 100%;
      padding: 0 20px;
      max-width: 1200px;
      margin: 0 auto;
      gap: 24px;
    }

    .skeleton-logo {
      width: 100px;
      height: 24px;
      background: var(--surface-3, #e8e8ed);
      border-radius: var(--radius-sm, 6px);
      animation: pulse 1.5s ease-in-out infinite;
    }

    .skeleton-nav {
      display: flex;
      gap: 8px;
      flex: 1;
    }

    .skeleton-pill {
      height: 28px;
      width: 80px;
      background: var(--surface-3, #e8e8ed);
      border-radius: 999px;
      animation: pulse 1.5s ease-in-out infinite;
    }

    .skeleton-avatar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: var(--surface-3, #e8e8ed);
      animation: pulse 1.5s ease-in-out infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 0.4; }
      50% { opacity: 0.8; }
    }

    /* Degraded error state */
    .degraded-msg {
      color: var(--text-muted, #aeaeb2);
      font-size: 13px;
      font-style: italic;
      flex: 1;
    }

    .degraded-avatar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: var(--surface-3, #e8e8ed);
      flex-shrink: 0;
    }

    @media (max-width: 768px) {
      .nav-links {
        display: none;
      }
    }

    @media (prefers-reduced-motion: reduce) {
      :host {
        transition: none;
      }
      .skeleton-pill,
      .skeleton-logo,
      .skeleton-avatar {
        animation: none;
        opacity: 0.5;
      }
    }
  `;

  @property({ type: Array })
  links: NavLink[] = [];

  @property({ type: Boolean, reflect: true })
  loading = false;

  @property({ type: Boolean, reflect: true })
  error = false;

  @property({ type: Boolean, reflect: true })
  loggedIn = false;

  @state()
  private _hidden = false;

  @state()
  private _lastScrollY = 0;

  private _boundScroll: () => void;

  constructor() {
    super();
    this._boundScroll = this._onScroll.bind(this);
  }

  connectedCallback() {
    super.connectedCallback();
    window.addEventListener('scroll', this._boundScroll, { passive: true });
  }

  disconnectedCallback() {
    super.disconnectedCallback();
    window.removeEventListener('scroll', this._boundScroll);
  }

  private _onScroll() {
    const currentY = window.scrollY;
    if (currentY <= 0) {
      this._hidden = false;
      this._lastScrollY = 0;
      return;
    }

    const delta = currentY - this._lastScrollY;
    if (delta > 10) {
      this._hidden = true;
    } else if (delta < -10) {
      this._hidden = false;
    }
    this._lastScrollY = currentY;
  }

  private _fireDegraded() {
    document.dispatchEvent(
      new CustomEvent('nav:degraded', {
        bubbles: true,
        detail: { state: 'error' },
      })
    );
  }

  render() {
    // Loading state
    if (this.loading) {
      return html`
        <div class="skeleton-bar">
          <div class="skeleton-logo"></div>
          <div class="skeleton-nav">
            <div class="skeleton-pill"></div>
            <div class="skeleton-pill"></div>
            <div class="skeleton-pill"></div>
          </div>
          <div class="skeleton-avatar"></div>
        </div>
      `;
    }

    // Error state - degraded
    if (this.error) {
      return html`
        <div class="nav-inner">
          <a class="logo" href="/" aria-label="styde.se home">
            <svg viewBox="0 0 28 28" fill="none">
              <rect width="28" height="28" rx="6" fill="var(--accent, #0071e3)"/>
              <text x="14" y="20" text-anchor="middle" fill="white" font-size="16" font-weight="700">S</text>
            </svg>
          </a>
          <span class="degraded-msg">Navigation unavailable</span>
          <div class="degraded-avatar" @click=${this._fireDegraded}></div>
        </div>
      `;
    }

    // Normal state - use links (with fallback if empty)
    const resolvedLinks = this.links.length > 0 ? this.links : DEFAULT_NAV_LINKS;

    return html`
      <div class="nav-inner">
        <a class="logo" href="/" aria-label="styde.se home">
          <svg viewBox="0 0 28 28" fill="none">
            <rect width="28" height="28" rx="6" fill="var(--accent, #0071e3)"/>
            <text x="14" y="20" text-anchor="middle" fill="white" font-size="16" font-weight="700">S</text>
          </svg>
          styde
        </a>

        <nav class="nav-links">
          ${resolvedLinks.map(
            (link) => html`
              <a
                class="nav-link"
                href="${link.href}"
                ?active=${location.pathname.startsWith(link.href)}
              >
                ${link.label}
              </a>
            `
          )}
        </nav>

        <div class="user-area">
          ${this.loggedIn
            ? html`
                <button class="avatar" aria-label="User menu">
                  <svg width="18" height="18" viewBox="0 0 18 18" fill="currentColor">
                    <circle cx="9" cy="6" r="3"/>
                    <path d="M3 16c0-3.3 2.7-6 6-6s6 2.7 6 6"/>
                  </svg>
                </button>
              `
            : html`
                <button class="btn-signin">Sign In</button>
                <button class="btn-getstarted">Get Started</button>
              `}
        </div>
      </div>
    `;
  }
}

customElements.define('site-nav-bar', SiteNavBar);
