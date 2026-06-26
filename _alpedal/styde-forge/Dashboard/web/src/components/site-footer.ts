import { LitElement, html, css } from 'lit';
import { property } from 'lit/decorators.js';

interface FooterLink {
  label: string;
  href: string;
}

interface FooterData {
  copyright: string;
  links: FooterLink[];
  social: { platform: string; href: string; icon: string }[];
}

const DEFAULT_LINKS: FooterLink[] = [
  { label: 'About', href: '/about' },
  { label: 'Contact', href: '/contact' },
  { label: 'Privacy', href: '/privacy' },
  { label: 'Terms', href: '/terms' },
  { label: 'Status', href: '/status' },
];

const FALLBACK_DATA: FooterData = {
  copyright: '\u00a9 styde.se',
  links: [],
  social: [],
};

export class SiteFooter extends LitElement {
  static styles = css`
    :host {
      display: block;
      min-height: var(--footer-min-height, 48px);
      background: var(--surface-2, #f5f5f7);
      border-top: 1px solid var(--border, #d2d2d7);
      padding: 16px 24px;
      box-sizing: border-box;
    }

    .footer-inner {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      max-width: 1200px;
      margin: 0 auto;
      font-size: 13px;
      color: var(--text-secondary, #6e6e73);
    }

    .footer-copyright {
      color: var(--text-muted, #aeaeb2);
      font-size: 12px;
    }

    .footer-links {
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
    }

    .footer-link {
      color: var(--text-secondary, #6e6e73);
      text-decoration: none;
      transition: color 0.15s ease;
    }

    .footer-link:hover {
      color: var(--accent, #0071e3);
    }

    .footer-link:focus-visible {
      outline: 2px solid var(--accent, #0071e3);
      outline-offset: 2px;
      border-radius: 2px;
    }

    .footer-social {
      display: flex;
      gap: 12px;
    }

    .footer-social-link {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 28px;
      height: 28px;
      border-radius: 50%;
      background: var(--surface-3, #e8e8ed);
      color: var(--text-secondary, #6e6e73);
      text-decoration: none;
      font-size: 14px;
      transition: background 0.15s ease, color 0.15s ease;
    }

    .footer-social-link:hover {
      background: var(--accent, #0071e3);
      color: white;
    }

    .back-to-top {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      color: var(--text-muted, #aeaeb2);
      text-decoration: none;
      font-size: 12px;
      cursor: pointer;
      background: none;
      border: none;
      padding: 4px 8px;
      border-radius: var(--radius-sm, 4px);
      transition: color 0.15s ease, background 0.15s ease;
    }

    .back-to-top:hover {
      color: var(--accent, #0071e3);
      background: var(--surface-3, #e8e8ed);
    }

    .back-to-top:focus-visible {
      outline: 2px solid var(--accent, #0071e3);
      outline-offset: 2px;
    }

    /* Skeleton loading */
    .skeleton {
      display: flex;
      flex-direction: column;
      gap: 8px;
      max-width: 1200px;
      margin: 0 auto;
    }

    .skeleton-row {
      display: flex;
      gap: 12px;
    }

    .skeleton-pill {
      height: 12px;
      border-radius: 999px;
      background: var(--surface-3, #e8e8ed);
      animation: pulse 1.5s ease-in-out infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 0.4; }
      50% { opacity: 0.8; }
    }

    @media (max-width: 640px) {
      .footer-inner {
        flex-direction: column;
        align-items: flex-start;
      }
    }

    @media (prefers-reduced-motion: reduce) {
      .skeleton-pill {
        animation: none;
        opacity: 0.5;
      }
    }
  `;

  @property({ type: Object })
  data: FooterData | null = null;

  @property({ type: Boolean, reflect: true })
  loading = false;

  @property({ type: Boolean, reflect: true })
  error = false;

  private _onBackToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  render() {
    if (this.loading) {
      return html`
        <div class="skeleton">
          <div class="skeleton-row">
            <div class="skeleton-pill" style="width: 120px"></div>
            <div class="skeleton-pill" style="width: 60px"></div>
            <div class="skeleton-pill" style="width: 80px"></div>
          </div>
          <div class="skeleton-row">
            <div class="skeleton-pill" style="width: 40px; height: 28px; border-radius: 50%"></div>
            <div class="skeleton-pill" style="width: 40px; height: 28px; border-radius: 50%"></div>
          </div>
        </div>
      `;
    }

    const resolvedData = this.data || FALLBACK_DATA;
    const links = resolvedData.links.length > 0 ? resolvedData.links : DEFAULT_LINKS;

    // Error/empty: minimal render with just copyright
    if (this.error || resolvedData.links.length === 0) {
      return html`
        <div class="footer-inner">
          <span class="footer-copyright">\u00a9 styde.se</span>
          <button class="back-to-top" @click=${this._onBackToTop}>
            Back to top
          </button>
        </div>
      `;
    }

    return html`
      <div class="footer-inner">
        <div class="footer-links">
          ${links.map(
            (link) => html`
              <a class="footer-link" href="${link.href}">${link.label}</a>
            `
          )}
        </div>

        <div class="footer-copyright">${resolvedData.copyright}</div>

        <div style="display: flex; align-items: center; gap: 12px;">
          ${resolvedData.social.length > 0
            ? html`
                <div class="footer-social">
                  ${resolvedData.social.map(
                    (s) => html`
                      <a
                        class="footer-social-link"
                        href="${s.href}"
                        aria-label="${s.platform}"
                      >
                        ${s.icon}
                      </a>
                    `
                  )}
                </div>
              `
            : ''}
          <button class="back-to-top" @click=${this._onBackToTop}>
            Back to top
          </button>
        </div>
      </div>
    `;
  }
}

customElements.define('site-footer', SiteFooter);
