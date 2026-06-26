import { LitElement, html, css } from 'lit';
import { property, state } from 'lit/decorators.js';

export interface BreadcrumbSegment {
  label: string;
  href?: string;
}

export class SiteBreadcrumb extends LitElement {
  static styles = css`
    :host {
      display: block;
      height: var(--breadcrumb-height, 32px);
      background: var(--surface-2, #f5f5f7);
      border-bottom: 1px solid var(--border, #d2d2d7);
      position: sticky;
      top: var(--nav-height, 56px);
      z-index: var(--z-breadcrumb, 999);
      transition: background 0.2s ease, opacity 0.2s ease;
      overflow: hidden;
    }

    .breadcrumb-inner {
      display: flex;
      align-items: center;
      height: 100%;
      padding: 0 16px;
      font-size: 12px;
      color: var(--text-secondary, #6e6e73);
      gap: 4px;
      max-width: 100%;
      overflow: hidden;
    }

    .segment {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      white-space: nowrap;
    }

    .segment-link {
      color: var(--text-secondary, #6e6e73);
      text-decoration: none;
      padding: 2px 4px;
      border-radius: var(--radius-sm, 4px);
      transition: color 0.15s ease, background 0.15s ease;
    }

    .segment-link:hover {
      color: var(--accent, #0071e3);
      background: var(--surface-3, #e8e8ed);
    }

    .segment-link:focus-visible {
      outline: 2px solid var(--accent, #0071e3);
      outline-offset: 1px;
    }

    .segment-current {
      color: var(--text-primary, #1d1d1f);
      font-weight: 500;
    }

    .segment-muted {
      color: var(--text-muted, #aeaeb2);
      font-style: italic;
    }

    .separator {
      color: var(--text-muted, #aeaeb2);
      margin: 0 2px;
      user-select: none;
    }

    .skeleton {
      display: flex;
      align-items: center;
      gap: 6px;
      height: 100%;
      padding: 0 16px;
    }

    .skeleton-pill {
      height: 12px;
      width: 40px;
      background: var(--surface-3, #e8e8ed);
      border-radius: 999px;
      animation: pulse 1.5s ease-in-out infinite;
    }

    .skeleton-sep {
      height: 8px;
      width: 8px;
      background: var(--text-muted, #aeaeb2);
      border-radius: 50%;
      opacity: 0.3;
    }

    @keyframes pulse {
      0%, 100% { opacity: 0.4; }
      50% { opacity: 0.8; }
    }

    @media (prefers-reduced-motion: reduce) {
      .skeleton-pill {
        animation: none;
        opacity: 0.5;
      }
    }
  `;

  @property({ type: Array })
  path: BreadcrumbSegment[] = [];

  @property({ type: Boolean, reflect: true })
  loading = false;

  @property({ type: Boolean, reflect: true })
  error = false;

  @state()
  private _scrollOpacity = 1;

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
    const scrollY = window.scrollY;
    if (scrollY > 100) {
      const opacity = Math.max(0.6, 1 - (scrollY - 100) / 200);
      this._scrollOpacity = opacity;
    } else {
      this._scrollOpacity = 1;
    }
  }

  private _onSegmentClick(seg: BreadcrumbSegment, e: MouseEvent) {
    if (!seg.href) return;
    e.preventDefault();
    this.dispatchEvent(
      new CustomEvent('breadcrumb:select', {
        bubbles: true,
        composed: true,
        detail: { label: seg.label, href: seg.href },
      })
    );
  }

  private _renderSegments() {
    if (!this.path || this.path.length === 0) {
      // Empty path fallback
      const fallback = document.title || 'Page';
      return html`
        <span class="segment segment-link" href="/">styde.se</span>
        <span class="separator">></span>
        <span class="segment segment-current">${fallback}</span>
      `;
    }

    return this.path.map((seg, i) => {
      const isLast = i === this.path.length - 1;
      const segments = [];

      if (i > 0) {
        segments.push(html`<span class="separator">></span>`);
      }

      if (isLast) {
        segments.push(
          html`<span class="segment segment-current">${seg.label}</span>`
        );
      } else if (seg.href) {
        segments.push(
          html`<a
            class="segment segment-link"
            href="${seg.href}"
            @click=${(e: MouseEvent) => this._onSegmentClick(seg, e)}
          >
            ${seg.label}
          </a>`
        );
      } else {
        segments.push(
          html`<span class="segment segment-muted">${seg.label}</span>`
        );
      }

      return html`<span class="segment">${segments}</span>`;
    });
  }

  render() {
    if (this.loading) {
      return html`
        <div class="skeleton">
          <div class="skeleton-pill"></div>
          <span class="skeleton-sep"></span>
          <div class="skeleton-pill"></div>
          <span class="skeleton-sep"></span>
          <div class="skeleton-pill" style="width: 60px"></div>
        </div>
      `;
    }

    if (this.error) {
      // Error fallback: derive from URL
      const slug = window.location.pathname.split('/').filter(Boolean).pop() || 'page';
      const fallbackPath: BreadcrumbSegment[] = [
        { label: 'styde.se', href: '/' },
        { label: 'Forge', href: '/forge' },
        { label: slug },
      ];
      return html`
        <div class="breadcrumb-inner" style="opacity: ${this._scrollOpacity}">
          ${fallbackPath.map((seg, i) => {
            const isLast = i === fallbackPath.length - 1;
            return html`
              ${i > 0 ? html`<span class="separator">></span>` : ''}
              ${isLast
                ? html`<span class="segment segment-current">${seg.label}</span>`
                : html`<a class="segment segment-link" href="${seg.href}">${seg.label}</a>`}
            `;
          })}
        </div>
      `;
    }

    return html`
      <div class="breadcrumb-inner" style="opacity: ${this._scrollOpacity}">
        ${this._renderSegments()}
      </div>
    `;
  }
}

customElements.define('site-breadcrumb', SiteBreadcrumb);
