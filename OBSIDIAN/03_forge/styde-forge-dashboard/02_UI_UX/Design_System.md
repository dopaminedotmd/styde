# Design System

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Design Philosophy

**"Terminal chic"** — dark, compact, functional. Nothing unnecessary.

Inspiration:
- VS Code (dark theme, panel layout)
- Linear (clean typography, subtle animations)
- htop/btm (compact data display)
- Cyberpunk 2077 UI (neon accents, glowing elements)

---

## 2. Color Palette

### 2.1 Primary Palette

| Name | Hex | Usage |
|------|-----|-------|
| **Background** | `#0d0d1a` | App background, main color |
| **Surface** | `#1a1a2e` | Panel background, cards |
| **Surface 2** | `#16213e` | Hover, alternating rows |
| **Border** | `#2a2a4a` | Panel borders, input borders |
| **Text Primary** | `#e0e0e0` | Main text |
| **Text Secondary** | `#8892b0` | Secondary text, labels |
| **Text Muted** | `#4a5568` | Placeholder, inactive text |

### 2.2 Accent Colors

| Name | Hex | Usage |
|------|-----|-------|
| **Primary** | `#6366f1` | Buttons, links, active tab |
| **Primary Hover** | `#818cf8` | Hover on primary elements |
| **Success** | `#10b981` | Done status, positive values |
| **Warning** | `#f59e0b` | Paused, warnings |
| **Danger** | `#ef4444` | Error, stopped, critical |
| **Info** | `#3b82f6` | Information, neutral status |

### 2.3 Status Dots

| Status | Color | Glow |
|--------|-------|------|
| Running | `#10b981` | `box-shadow: 0 0 8px #10b981` |
| Paused | `#f59e0b` | `box-shadow: 0 0 8px #f59e0b` |
| Stopped | `#4a5568` | No glow |
| Error | `#ef4444` | `box-shadow: 0 0 8px #ef4444` (pulsing) |

---

## 3. Typography

### 3.1 Font Stack

```css
font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code',
             'Consolas', 'Monaco', monospace;
```

| Usage | Font | Size | Weight |
|-------|------|------|--------|
| Title bar | JetBrains Mono | 14px | 600 |
| Panel headers | JetBrains Mono | 12px | 600 (uppercase, letter-spacing 1px) |
| Body text | JetBrains Mono | 13px | 400 |
| Code | JetBrains Mono | 12px | 400 |
| Small labels | JetBrains Mono | 11px | 400 |
| Status bar | JetBrains Mono | 11px | 500 |

### 3.2 Text Styles

| Style | CSS |
|-------|-----|
| Heading | `font-weight: 600; color: #e0e0e0;` |
| Body | `font-weight: 400; color: #c0c0d0; line-height: 1.6;` |
| Code | `background: #1a1a2e; border-radius: 4px; padding: 2px 6px;` |
| Link | `color: #6366f1; text-decoration: none; &:hover { text-decoration: underline; }` |

---

## 4. Components (Design Tokens)

### 4.1 Buttons

```css
/* Primary button */
.btn-primary {
  background: #6366f1;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  padding: 6px 16px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}
.btn-primary:hover { background: #818cf8; }
.btn-primary:active { background: #4f46e5; }

/* Secondary button */
.btn-secondary {
  background: transparent;
  color: #c0c0d0;
  border: 1px solid #2a2a4a;
}

/* Danger button */
.btn-danger {
  background: #ef4444;
  color: #ffffff;
}
```

### 4.2 Input Fields

```css
.input {
  background: #0d0d1a;
  border: 1px solid #2a2a4a;
  border-radius: 6px;
  color: #e0e0e0;
  padding: 8px 12px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
}
.input:focus {
  border-color: #6366f1;
  outline: none;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}
```

### 4.3 Scrollbars

```css
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d0d1a; }
::-webkit-scrollbar-thumb {
  background: #2a2a4a;
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: #3a3a5a; }
```

---

## 5. Animations

| Element | Animation | Duration | Easing |
|---------|-----------|----------|--------|
| Panel resize | `width` transition | 150ms | ease-out |
| Panel tab switch | `opacity` fade | 200ms | ease-in-out |
| Button hover | `background` color | 150ms | ease |
| Status dot (running) | `box-shadow` pulse | 2s | infinite ease-in-out |
| New agent in list | Slide-in from right | 300ms | ease-out |
| Notification popup | Slide-in from bottom | 400ms | ease-out |

---

## 6. Icons

Minimal, consistent icon set (Lucide-icons style):

| Icon | Usage |
|------|-------|
| ▶ | Start |
| ⏸ | Pause |
| ⏹ | Stop |
| ⚙ | Settings |
| ● | Status (colored) |
| 📡 | Agent panel |
| 📊 | Benchmark panel |
| 💬 | Chat panel |
| 🔄 | Refresh / update |
| 📌 | Pin panel |
| ✕ | Close panel / remove |
| ⚡ | Speed / tokens per second |
| 💾 | Checkpoint / save |

---

## 7. Dark Mode Only

The Dashboard is **dark theme only** — no light mode. This is a design decision, not a preference:

| Reason |
|--------|
| Terminal aesthetic — belongs in the dark |
| Reduces code complexity (no theme variables) |
| Better for long sessions (less eye strain) |
| Matches the StydeForge Forge terminal appearance |

---

**Status:** Phase 0 — Design
