import { LitElement, html, css } from 'lit';
import { state } from 'lit/decorators.js';

export class SiteProgressBar extends LitElement {
  static styles = css`
    :host {
      display: block;
      position: fixed;
      top: calc(var(--nav-height, 56px) - 3px);
      left: 0;
      right: 0;
      z-index: var(--z-progress, 1001);
      height: 3px;
      pointer-events: none;
    }

    .track {
      width: 100%;
      height: 100%;
      background: var(--progress-track, #e8e8ed);
      position: relative;
      overflow: hidden;
      opacity: 0;
      transition: opacity var(--progress-fade-duration, 0.2s) ease-out;
    }

    .track.active {
      opacity: 1;
    }

    .fill {
      height: 100%;
      background: var(--progress-fill, #0071e3);
      width: 0%;
      transition: width var(--progress-duration, 0.4s) ease-out;
    }

    @media (prefers-reduced-motion: reduce) {
      .fill {
        transition: none;
      }
    }
  `;

  @state()
  private _active = false;

  @state()
  private _width = 0;

  private _safetyTimer: ReturnType<typeof setTimeout> | null = null;
  private _boundStart: (e: Event) => void;
  private _boundComplete: (e: Event) => void;

  constructor() {
    super();
    this._boundStart = this._onProgressStart.bind(this);
    this._boundComplete = this._onProgressComplete.bind(this);
  }

  connectedCallback() {
    super.connectedCallback();
    document.addEventListener('progress:start', this._boundStart);
    document.addEventListener('progress:complete', this._boundComplete);
  }

  disconnectedCallback() {
    super.disconnectedCallback();
    document.removeEventListener('progress:start', this._boundStart);
    document.removeEventListener('progress:complete', this._boundComplete);
    this._clearSafety();
  }

  private _onProgressStart() {
    this._clearSafety();
    this._active = true;
    this._width = 0;
    // Force reflow then animate
    requestAnimationFrame(() => {
      this._width = 30;
      this._safetyTimer = setTimeout(() => {
        this._width = 90;
        setTimeout(() => {
          this._active = false;
          this._width = 0;
        }, 600);
      }, 10000);
    });
  }

  private _onProgressComplete() {
    this._clearSafety();
    this._width = 100;
    setTimeout(() => {
      this._active = false;
      this._width = 0;
    }, 400);
  }

  private _clearSafety() {
    if (this._safetyTimer !== null) {
      clearTimeout(this._safetyTimer);
      this._safetyTimer = null;
    }
  }

  render() {
    return html`
      <div class="track ${this._active ? 'active' : ''}">
        <div class="fill" style="width: ${this._width}%"></div>
      </div>
    `;
  }
}

customElements.define('site-progress-bar', SiteProgressBar);
