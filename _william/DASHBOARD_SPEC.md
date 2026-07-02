# styde.ai Dashboard — Spec v2.0

> "Resan in i automationen." Login som en filmisk upplevelse. Chatten som kommandocentralen.

---

## 1. Vibe & Design Language

### Koncept

*Meridian möter Hermes. Lyxig reseupplevelse möter ren AI-kommandocentral.*

**Kärnidé:** Att logga in på styde.ai ska kännas som att kliva in i något viktigt. Inte en SaaS-dashboard — en kontrollcentral för din digitala personal. Som att öppna dörren till en hemlig operationsbas i ett berg.

Bakgrundsbilden är inte dekorativ — den är **portalen**. Den berättar: "Du är på väg någonstans."

### Färgpalett

| Roll | Färg | Hex |
|------|------|-----|
| Bakgrund login | Mörkt blå/svart gradient | `#0B0D15` → `#000000` |
| Bakgrund dashboard | Djup skiffer | `#0E1017` |
| Yta (cards) | Mörk grå | `#1A1D27` |
| Border | Subtil vit | `rgba(255,255,255,0.06)` |
| **Accent — Rust Orange** | Varm, jordnära | **`#C65D26`** |
| Accent hover | Ljusare orange | `#D97742` |
| Text primär | Vit/cream | `#F0EDE8` |
| Text sekundär | Dämpad | `#8B8F9B` |
| Vertikal text | Ljus, diskret | `#6B7280` |
| Glass-bakgrund | Frostat glas | `rgba(255,255,255,0.03)` |

**Accentfärgen (#C65D26) är kritisk.** Den är den "mänskliga" punkten i den kalla digitala miljön. Värme i mörkret. Som lampan i fönstret.

### Typografi

| Element | Font | Info |
|---------|------|------|
| Hero-headline (login) | **Playfair Display** | Serif, kursiv, 3-4rem |
| Rubriker (dashboard) | Playfair Display | Serif, 1.5-2rem |
| Brödtext | **Inter** | Sans, 14-15px, regular |
| Knappar / UI | Inter | Sans, 500-600 weight |
| Monospace (kod/data) | JetBrains Mono | 13px |
| Vertikal text | Inter | Uppercase, tight tracking |

**Playfair Display** är hjärtat i identiteten. Den ger tyngd och berättelse. Använd den sparsamt — bara för hero och sektionsrubriker.

### Designprinciper

1. **Asymmetri** — text vänster, CTA höger/nere. Inget symmetriskt centrerat.
2. **Lager** — bilden är lagret längst bak, glass-kort ovanpå, text överst.
3. **Rörelse** — scroll är en berättelse, inte ett mekaniskt flöde.
4. **Vertikal text** — vänster marginalen är "ryggraden". Alltid något vertikalt där.
5. **Orange som kraft** — accent används bara för CTA och aktiva element. Inget slumpmässigt orange.
6. **Mörkt men inte mörkt** — tillräckligt ljus text för läsbarhet, tillräckligt mörk bakgrund för djup.

---

## 2. Loginscreen — Upplevelsen

### Visuell layout

```
┌──────────────────────────────────────────────────────────┐
│ [HOW IT WORKS]                        [styde.ai] [● ● ●] │
│                                                            │
│                                                            │
│                                                            │
│   SYSTEM // ACCESS                                         │
│                     ┌──────────────────────────┐            │
│                     │                          │            │
│                     │   Välkommen tillbaka     │            │
│                     │                          │            │
│                     │   "Your work.            │            │
│                     │    Amplified by          │            │
│                     │    intelligence."        │            │
│                     │                          │            │
│                     │   ┌──────────────────┐   │            │
│                     │   │ name@company.se  │   │            │
│                     │   │  [↓ Magic Link]   │   │            │
│                     │   └──────────────────┘   │            │
│                     │                          │            │
│                     │   [🔄 Ny hit? Skapa konto]│            │
│                     │                          │            │
│                     └──────────────────────────┘            │
│                                                            │
│                        SCROLL                              │
│                        │                                   │
└──────────────────────────────────────────────────────────┘
```

### Bakgrundsbild

Full-bleed background image. Högupplöst, atmosfärisk, fångad i golden hour.

**Tema:** Resan. Vägen framåt. Landskap som känns stort och betydelsefullt.

Krav på bilden:
- Mörk förgrund (ovanpå texts)
- Ljus himmel/långt bort (djup)
- Varma toner (orange, bärnsten, guld)
- Känsla av rörelse framåt (väg, stig, horisont)
- Ingenting "AI" eller "tech" i bilden — den är mänsklig

**Över bilden:** Subtil mörk gradient botten-till-topp för läsbarhet. ca 15% opacity overlay.

### Komponenter

| Element | Placering | Detaljer |
|---------|-----------|----------|
| "HOW IT WORKS" | Top left, pill | Liten, `#C65D26` bg, vit text. Länkar till `/how-it-works` |
| "styde.ai · DIGITAL COLLABORATORS" | Top right | Uppercase, small, tight tracking, sekundär text |
| Status dots | Top right | 3 små dots ("system status"), animeras subtilt |
| Vertikal text | Far left edge | `"SYSTEM // ACCESS"` roterad -90°, uppercase, tracking 0.2em |
| Login card | Center | Glassmorphism-kort. `rgba(255,255,255,0.03)` bg, blur(16px), border 1px `rgba(255,255,255,0.08)`, border-radius 20px |
| Välkomsttext | Inuti kort | Liten sans, uppercase, sekundär färg |
| Hero-headline | Inuti kort | Playfair Display, kursiv, 2.5rem, `#F0EDE8` |
| Email input | Inuti kort | Rent inputfält, border bottom, placeholder "name@company.se" |
| Magic Link CTA | Inuti kort | Pill-knapp, `#C65D26` bg. "Send Magic Link" |
| "Ny hit?" | Inuti kort | Liten länk under CTA |
| SCROLL | Bottom center | Liten uppercase text + vertikal linje (animeras upp/ner) |

### Login flow

1. Användaren landar på login-sidan. Helbildsscenen. Inget annat syns.
2. Skriver sin e-post.
3. Klickar "Send Magic Link".
4. Får e-post med länk.
5. Klickar länken → loggas in → **scroll-animationen startar automatiskt.**

### Vad som INTE syns på login

- Inget "Powered by" badge
- Inga cookie-banners (GDPR löses separat)
- Inga login-formulär med lösenord — bara magic link
- Inga social login-knappar

---

## 3. Scroll-overgången — Magin

När användaren loggar in sker detta i en mjuk animation:

### Steg-för-steg

```
[Steg 1]  Login-screen syns. Bakgrundsbilden full.
[Steg 2]  Användaren klickar magic link → laddar dashboard-sidan
[Steg 3]  Dashboard-sidan visas → automatiskt scroll nedåt (JS-animerat)
[Steg 4]  Bakgrundsbilden "scrollar uppåt" och fade:ar ut
[Steg 5]  Chat-dashboarden glider in från botten
[Steg 6]  Användaren är nu i chat-vyn. Bakgrunden är mörk solid #0E1017
```

### Animationsteknik

- `window.scrollTo({ top: window.innerHeight, behavior: 'smooth' })` eller
- CSS `scroll-behavior: smooth` + en trigger efter auth
- Bakgrunden är en `position: fixed` hero-sektion som fade:ar ut vid scroll
- Dashboard-sektionen har `position: relative` och tar över när hero är borta

### Visuell effekt

```
Scroll 0%:  ┌──────────────────┐  ← Hero full synlig
            │   BILD           │
            │   Login card     │

Scroll 50%: ┌──────────────────┐
            │   BILD (fade)    │  ← Bilden fade:ar, chatten skymtas
            │   ═══════════    │
            │   Chat (coming)  │

Scroll 100%:┌──────────────────┐  ← Chatten i full vy
            │   CHAT-VY        │
            │   Agent-kort     │
```

---

## 4. Chat Dashboard — Efter scrollen

### Layout

```
┌──────────────────────────────────────────────────────────┐
│ [☰]  styde.ai              [🟢 🟡 ⚪] 3 agents  [👤] │
│ ┌─────┬────────────────────────────────────────────┐     │
│ │     │                                            │     │
│ │     │  💬 **Chat**                               │     │
│ │     │                                            │     │
│ │     │  Hej! Jag är din centrala AI-assistent.    │     │
│ │     │  Jag pratar med alla dina agenter.         │     │
│ │     │                                            │     │
│ │     │  --- Igår ---                              │     │
│ │     │                                            │     │
│ │     │  Du: Kör en audit på vår hemsida           │     │
│ │     │                                            │     │
│ │     │  Agent: ✅ Klar!                           │     │
│ │     │  3 automationer funna                      │     │
│ │     │  [📄 Öppna rapport]                        │     │
│ │     │                                            │     │
│ │     │  ┌──────────────────────────────┐          │     │
│ │     │  │ Skriv till dina agenter... │  ✨       │     │
│ │     │  └──────────────────────────────┘          │     │
│ │     │                                            │     │
│ │     └────────────────────────────────────────────┘     │
│ │                                    ┌──────────┐        │
│ │  🟢 Faktura-agenten               │ Aktiv     │        │
│ │  142 fakturor hanterade idag      │           │        │
│ │                                    └──────────┘        │
│ │  🟡 Kund-support                  │ Väntar    │        │
│ │  Koppla Slack för att aktivera    │ Koppla →  │        │
│ │                                    └──────────┘        │
│ │  ⚪ Mejlsorteraren                │ Inaktiv   │        │
│ │  Kräver IMAP-koppling             │ Setup →   │        │
│ │                                    └──────────┘        │
│ │                                                        │
│ │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │  │ 📊 Ny    │ │ 🔌 Koppla│ │ 📋 Rapp- │ │ ⚙️ Instäl│ │
│ │  │ audit    │ │  verktyg │ │  orter   │ │ -ningar  │ │
│ │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
└──────────────────────────────────────────────────────────────┘
```

### Vänster sidebar

| Element | Funktion |
|---------|----------|
| Toggle hamburger | Öppna/stäng sidebar |
| Logo | `styde.ai` — länk till `/` |
| Agent-indikatorer | 🟢🟡⚪ summering av agentstatus |
| User menu | Avatar/dropdown — settings, logout |

När sidebar är öppen: agentlista med namn, senaste meddelande, tid.

### Chat — Main content

Chatten är hjärtat. Samma koncept som v1 men med Meridian-design.

**Chat-input:**
- Låda med rundade hörn (12px)
- Placeholder: "Fråga dina agenter vad som helst..."
- Enter skickar, Shift+Enter ny rad
- Liten skicka-knapp (→) i orange #C65D26
- Auto-resize textarea

**Chat-meddelanden:**
- Egna meddelanden: högerjusterade, mörk bubbla (#1A1D27)
- Agent-svar: vänsterjusterade, med avatar/ikon för agenten
- Streaming: texten fade:ar in med en blinkande cursor
- Kodblock: monospace, mörk bakgrund (#13151E)
- Actions: knappar under meddelandet (öppna rapport, ladda ner, etc.)

**Agent-attribution:**
Varje agentsvar har en badge:
```
[🤖 Faktura-agenten] 🟢 Aktiv · 2 min sedan
```
Badgen är liten, rundad, i sekundär text.

### Höger panel — Agent-status

En smal panel (300px) som visar alla agenter med status.

| Agent | Status | Action |
|-------|--------|--------|
| Faktura-agenten | 🟢 Aktiv — 142 fakturor idag | — |
| Kund-support | 🟡 Väntar — kräver Slack | [🔗 Koppla] |
| Mejlsorteraren | ⚪ Inaktiv — kräver IMAP | [→ Setup] |
| Webb-analytikern | 🟢 Aktiv — övervakar | [📄 Rapport] |
| Lead-generatorn | 🔴 Fel — API-nyckel ogiltig | [⚙️ Fixa] |

**Status dots:**
- 🟢 Aktiv — pulserande grön glow (#22C55E med box-shadow)
- 🟡 Väntar — statisk gul (#EAB308)
- ⚪ Inaktiv — grå (#6B7280)
- 🔴 Error — statisk röd (#EF4444)

### Quick action buttons

Under agent-status, fyra knappar i rad:

| Knapp | Ikon | Funktion |
|-------|------|----------|
| Ny audit | 📊 | Fyller chat-input med prompten för audit |
| Koppla verktyg | 🔌 | Navigerar till integrationsvyn |
| Rapporter | 📋 | Navigerar till rapportarkivet |
| Inställningar | ⚙️ | Navigerar till settings |

---

## 5. Övriga sidor — Design language

Alla undersidor använder samma design language som chatten:
- Mörk bakgrund (#0E1017)
- Playfair Display för sektionsrubriker
- Orange accent (#C65D26) för CTA
- Glassmorphism-kort för cards
- Vertikal text på vänster marginal

### Agents (`/agents`)

```
┌──────────────────────────────────────────────────────────────┐
│  AGENTS // ÖVERSIKT                                         │
│                                                              │
│  Dina digitala medarbetare                                   │
│  "Agents that work while you sleep."                         │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  🤖 Faktura-agenten              🟢 Aktiv              │  │
│  │  Hanterar 142 fakturor idag                            │  │
│  │  Senast aktiv: 2 min sedan                             │  │
│  │  [💬 Chatta]  [📄 Se arbete]  [⚙️]                   │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  🤖 Kund-support               🟡 Väntar              │  │
│  │  Koppla Slack för att aktivera                         │  │
│  │  [💬 Chatta]  [🔗 Koppla Slack]  [⚙️]                │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

### Integrations (`/integrations`)

```
┌──────────────────────────────────────────────────────────────┐
│  INTEGRATIONS // VERKTYG                                    │
│                                                              │
│  "Connect the tools you already use."                        │
│                                                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │  🔌 Slack    │ │  ✉️ E-post  │ │  📊 Fortnox  │        │
│  │  🟢 Ansluten │ │  ⚪ Anslut  │ │  ⚪ Anslut  │        │
│  │  [⚙️]        │ │  [🔗]       │ │  [🔗]       │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
└──────────────────────────────────────────────────────────────────┘
```

### Rapporter (`/reports`)

Listvy med kort. Varje kort har:
- Titel (Playfair, kursiv)
- Datum (Inter, sekundär)
- Agent som skapade den
- Actions: [📄 Öppna] [📥 PDF] [📧 Skicka]

---

## 6. Knappar & Interaktioner — Design

### Knappstilar

| Typ | Utseende | Användning |
|-----|----------|------------|
| **Primär CTA** | `#C65D26` bg, vit text, pill (border-radius: 50px), padding: 10px 28px, font-weight 600 | Magic link, Ny audit, Planera |
| **Sekundär** | Transparent, vit border 1px, pill | Se arbete, Avbryt |
| **Ghost** | Bara text, ingen bg, orange hover | Länkar, "Ny hit?" |
| **Ikon** | Cirkel, `#C65D26` outline eller fylld | Pil, stäng, menu |

### Hover-effekter

Alla interaktiva element har:
- `transition: all 0.2s ease`
- Ljusare orange på hover (`#D97742`)
- Subtilt scale(1.02) på primära CTA
- Opacity change på sekundära element

### Loading states

- Skeleton screens för data som laddas (gråa pulserande rektanglar)
- Spinner: en tunn cirkel som roterar, orange
- Streaming: blinkande cursor (`|`) i slutet av texten medan agenten skriver

---

## 7. Teknisk stack (oförändrad)

| Lager | Val |
|-------|-----|
| Ramverk | Next.js 14+ (App Router) |
| Styling | Tailwind CSS v4 |
| UI-komponenter | shadcn/ui (bas) + custom chat |
| Databas | PostgreSQL |
| ORM | Drizzle |
| Auth | NextAuth.js — magic link |
| Deploy | Caddy → Next.js standalone på Ubuntu |
| Docker | dockerode (via API routes) |
| Realtid | Server-Sent Events (chat streaming) |

---

## 8. Mappstruktur

```
apps/dashboard/
├── app/
│   ├── login/
│   │   └── page.tsx              # Login screen — full hero bild
│   ├── (dashboard)/
│   │   ├── layout.tsx            # Dashboard layout (sidebar + content)
│   │   ├── page.tsx              # Chat — command center
│   │   ├── agents/
│   │   │   ├── page.tsx
│   │   │   └── [id]/page.tsx
│   │   ├── integrations/
│   │   │   └── page.tsx
│   │   ├── reports/
│   │   │   ├── page.tsx
│   │   │   └── [id]/page.tsx
│   │   ├── settings/
│   │   │   └── page.tsx
│   │   └── admin/
│   │       └── page.tsx
├── components/
│   ├── login/
│   │   ├── hero-image.tsx
│   │   ├── login-card.tsx
│   │   └── scroll-indicator.tsx
│   ├── dashboard/
│   │   ├── shell.tsx             # Dashboard wrapper
│   │   ├── sidebar.tsx
│   │   └── topbar.tsx
│   ├── chat/
│   │   ├── chat-input.tsx
│   │   ├── chat-message.tsx
│   │   ├── chat-stream.tsx
│   │   └── suggested-prompts.tsx
│   ├── agents/
│   │   ├── agent-card.tsx
│   │   ├── agent-status-dot.tsx
│   │   └── agent-panel.tsx
│   ├── integrations/
│   │   └── integration-card.tsx
│   ├── reports/
│   │   ├── report-card.tsx
│   │   └── report-viewer.tsx
│   └── ui/                       # shadcn/ui + custom
│       ├── button.tsx
│       ├── card.tsx
│       └── input.tsx
│   ├── styles/
│   │   ├── globals.css           # Tailwind + typography + theme
│   │   └── fonts.ts
│   └── lib/
│       ├── db.ts
│       ├── docker.ts
│       └── agents.ts
```

---

## 9. Alla features — Checklista v2.0

### Sidor (8 st)
- [ ] `/login` — Full-bleed hero, login-kort, scroll-indikator
- [ ] `/` — Chat command center (efter scroll-animation)
- [ ] `/agents` — Agent-översikt med statuskort
- [ ] `/agents/:id` — Agent-detalj (chat + output + config)
- [ ] `/integrations` — Koppla verktyg (grid av kort)
- [ ] `/reports` — Rapportarkiv
- [ ] `/reports/:id` — Rapportdetalj
- [ ] `/settings` — Kontoinställningar
- [ ] `/admin` — Admin (William only)

### Upplevelse
- [ ] Full-bleed hero background på login
- [ ] Glassmorphism login-kort (blur, transparent bg)
- [ ] Magic link auth (inget lösenord)
- [ ] Automatisk scroll-animation login → dashboard
- [ ] Vertikal text på vänster marginal
- [ ] "SCROLL"-indikator med pulserande linje
- [ ] Dark mode only — inget light mode
- [ ] Smooth transitions overall

### Chat
- [ ] Chat-input med auto-resize
- [ ] Real-tids streaming (SSE)
- [ ] Agent-attribution per svar
- [ ] Suggested prompts / quick actions
- [ ] Actions-knappar i chatt (öppna rapport, ladda ner)
- [ ] Historik sparad i databasen
- [ ] Full markdown-rendering i svar
- [ ] Kodblock med syntax highlighting
- [ ] Blinkande cursor under streaming

### Agent-status
- [ ] Live status dots (🟢🟡⚪🔴) med glow
- [ ] Agent-panel på höger sida
- [ ] Quick actions per agent
- [ ] "Koppla"-CTA för agenter som väntar på integration

### Integrationer
- [ ] Slack (OAuth)
- [ ] E-post (IMAP)
- [ ] Fortnox
- [ ] Google Workspace
- [ ] Webhooks

### Rapporter
- [ ] Lista med kort (titel, datum, agent, actions)
- [ ] Rapport-viewer (markdown/YAML)
- [ ] Export PDF
- [ ] Skicka till e-post

### Admin (William)
- [ ] Kundlista med status
- [ ] Alla agenter på alla kunder
- [ ] Docker-status
- [ ] Systemloggar

---

## 10. Inte i v2.0

- ❌ Mobil app (native)
- ❌ Multi-lingual
- ❌ White label
- ❌ Team-medlemmar
- ❌ Agent marketplace
- ❌ Public API
- ❌ Lösenordslogin (bara magic link)
- ❌ Light mode — aldrig
