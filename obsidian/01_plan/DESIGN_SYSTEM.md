# styde.ai — Design System & Visual Language
**Inspirerad av Clyde-estetiken: Mörkt Prismsken till Artsy Editorial Vit**

Detta dokument spikar den exakta designöversättningen av inspirationsbilden för **styde.ai**. Designen är en kontrastrik tvåstegsupplevelse: en djup, mystisk inloggningsskärm som rullar ned till en ren, luftig och typografiskt sofistikerad dashboard i redaktionell stil.

---

## 1. Den typografiska hierarkin

Designen bygger helt på spänningen mellan en elegant, högkontrastig Serif-font och en minimalistisk sans-serif.

*   **Primär Serif**: **Playfair Display** eller **Cormorant Garamond** (används för logotypen `styde`, stora rubriker och stämningsfulla taglines).
*   **Sekundär Sans-Serif**: **Inter** eller **Geist Sans** (används för brödtext, knappar och funktionsknappar).
*   **Monospace**: **JetBrains Mono** (används för kodblock, loggar och tidsstämplar).

---

## 2. Inloggningsportalen (Login-skärmen)
*Den mörka halvan av inspirationsbilden, roterad och placerad överst.*

```
┌────────────────────────────────────────────────────────┐
│                                                        │
│                      [ s t y d e ]                     │
│                                                        │
│                           ⚡                           │
│                     [ Prism Glow ]                     │
│                           ⚡                           │
│                                                        │
│                    ┌──────────────┐                    │
│                    │  Magic Link  │                    │
│                    │   [ Login ]  │                    │
│                    └──────────────┘                    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Bakgrund & Ljuseffekt (Prism Refraction)
*   **Bakgrund**: Solid, djup kolsvart `#06070B`.
*   **Prismskenet**: En centrerad, vertikal ljuseffekt (Light Leak / Rainbow Prism) som simuleras med en mjuk CSS-gradient (magenta → blå → grön → gul → orange).
*   **CSS-kod för Prismskenet**:
    ```css
    .prism-glow {
      background: linear-gradient(
        to bottom,
        rgba(255, 0, 128, 0.15),
        rgba(0, 128, 255, 0.2),
        rgba(0, 255, 128, 0.15),
        rgba(255, 128, 0, 0.2)
      );
      filter: blur(120px);
      width: 300px;
      height: 100%;
      position: absolute;
      left: 50%;
      transform: translateX(-50%);
      pointer-events: none;
    }
    ```

### Logotyp & Wreath-ikonen
*   **Logotypen `styde`**: Placeras överst i en stor, elegant Cormorant Garamond-stil, i helt vitt.
*   **Ikonen**: Den organiska, cirkulära kransen (Wreath-ikonen) placeras mitt i ljusstrålen. Den är en ren, vit SVG som pulserar mycket långsamt (`animation: breathe 8s infinite ease-in-out`).

---

## 3. Övergången (Smooth Scroll-over)

När användaren klickar på sin Magic Link sker en JS-triggad scrollneddragning som flyttar fokus till dashboarden.
*   Den mörka inloggningsskärmen tonas ut och glider uppåt (`transform: translateY(-100vh)`).
*   Den ljusa dashboarden glider upp från botten.
*   Övergången är mjuk och lyxig: `transition: transform 1.2s cubic-bezier(0.76, 0, 0.24, 1)`.

---

## 4. Den Redaktionella Dashboarden (Dashboard-Delight)
*Den ljusa halvan av inspirationsbilden — artsy, minimalistisk och högkontrastig.*

```
┌──────────────────────────────────────────────────────────┐
│  styde.ai                                    [👤 Partner] │
│                                                          │
│  Move faster with AI                                     │
│  Dina digitala medarbetare                               │
│                                                          │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐           │
│  │ hund │ │faktur│ │sales │ │audit │ │  +   │  AGENTER  │
│  │  ●   │ │  ○   │ │  ○   │ │  ●   │ │      │  (rad)    │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘           │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │                                                    │  │
│  │   🤖 hund                                          │  │
│  │   Agentens svar...                                 │  │
│  │                                                    │  │
│  │                                                    │  │
│  │   ╭──────────────────────────────────────────────╮ │  │
│  │   │  Skriv till hund...                    [↑]   │ │  │
│  │   ╰──────────────────────────────────────────────╯ │  │
│  └────────────────────────────────────────────────────┘  │
│             STOR CHATT-CANVAS (full bredd)               │
└──────────────────────────────────────────────────────────┘
```

### Färgpalett & Layout
*   **Bakgrund**: Ren, pappersliknande vit eller ljust linnefärgad yta (`#FAFAFC` eller `#F4F4F6`).
*   **Border-linjer**: Mycket tunna, diskreta linjer i mörkgrått med låg opacitet (`1px solid rgba(0, 0, 0, 0.08)`) för att dela av sektioner asymmetriskt.
*   **Primär text**: Djupt kolsvart `#111215` (används för Playfair-rubriker och viktiga ord).
*   **Sekundär text**: Skiffergrå `#5F626E` (används för brödtext och detaljer).

### Agent-rad (ovanför chatten)
*   **Placering**: Horisontell rad av agent-kort direkt ovanför chatt-canvas. Inte i sidopanel/drawer.
*   **Kort**: Ett kort per agent med geometrisk SVG-ikon, agentnamn och statuspunkt (`●` aktiv / `○` idle). Ett `+`-kort längst till höger för att lägga till/välja fler agenter.
*   **Interaktion**: Klick på kort → startar (eller återupptar) dedikerad chatttråd med den agenten. Aktiv agent markeras tydligt (t.ex. tjockare kant eller accentfärg).
*   **Wrap/scroll**: Vid 5+ agenter — horisontell scroll, fast enradig layout.

### Chatt-Canvas (Chattgränssnittet)
*   **Chattrutan**: Stor, svävande panel i kritvitt (`#FFFFFF`) som fyller **hela bredden** under agent-raden. Mycket generösa runda hörn (`border-radius: 24px`) och mjuk skugga (`box-shadow: 0 10px 40px rgba(0, 0, 0, 0.02)`).
*   **Agenternas svar**: Visas med stora, vackra serif-rubriker för agentens namn (t.ex. *🤖 `hund`* eller *`Faktura-agenten`*) följt av den genererade texten.
*   **Inputfältet**: Ett helt rundat (pill-shaped) inputfält som svävar i botten av den vita chattrutan.

### Gråskalebilder (flyttad till login)
*   Den stämningsfulla **gråskalebilden** (storstadslandskap/arkitektur) finns inte längre i dashboarden — den tog plats från chatten.
*   Bilden används istället som stämningssättare på **inloggningsskärmen** (se §2), där den förstärker det mogna, sofistikerade intrycket utan att konkurrera med arbetsytan.

---

## 5. Hur vi sätter upp detta i Tailwind CSS

Vi lägger till följande teman i vår `tailwind.config.js` eller i Tailwind v4-konfigurationen:

```javascript
theme: {
  extend: {
    fontFamily: {
      serif: ['"Playfair Display"', '"Cormorant Garamond"', 'serif'],
      sans: ['"Inter"', '"Geist Sans"', 'sans-serif'],
      mono: ['"JetBrains Mono"', 'monospace'],
    },
    colors: {
      styde: {
        darkBg: '#06070B',
        lightBg: '#FAFAFC',
        accent: '#C65D26',
        accentHover: '#D97742',
        textDark: '#111215',
        textMuted: '#5F626E',
      }
    },
    boxShadow: {
      'glass-light': '0 8px 32px 0 rgba(31, 38, 135, 0.03)',
      'glass-dark': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
    }
  }
}
```
