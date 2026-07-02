---
title: "DASHBOARD SPEC — Specifikation för Next.js-dashboarden"
date: 2026-06-25
author: hermes
tags: [area/ARKITEKTUR, status/APPROVED, author/HERMES, type/SPEC]
status: approved
---

# DASHBOARD SPEC — styde.ai Portal

> Specifikation för styde.ai-portalen. En gemensam Next.js-applikation med rollbaserad behörighet som hanterar både kundernas gränssnitt och vår interna administrationspanel.

---

## 1. Syfte
Att erbjuda ett och samma webbgränssnitt för:
1. **Kundvy (Customer View):** Låter kundernas personal övervaka, starta och hantera sina tilldelade agenter.
2. **Adminvy (Admin View):** Låter styde.ai-teamet (William och Alpedal) övervaka samtliga kunder, lägga till nya agenter, konfigurera systeminställningar samt läsa globala felloggar.

---

## 2. Arkitektur & Säkerhet
- **Teknikstack:** Next.js (App Router), Tailwind CSS (om godkänt, annars Vanilla CSS), Express API (backend-tjänster) och PostgreSQL.
- **Drift:** Körs lokalt på vår delade fysiska server (se [[SERVER_SETUP]]).
- **Autentisering:** E-post och lösenord med JWT-tokens sparade i HTTP-only cookies.
- **Rollbaserad behörighet (RBAC):**
  - `ROLE_ADMIN` (styde-teamet): Full tillgång till alla vyer, kunder och inställningar.
  - `ROLE_CUSTOMER_ADMIN`: Tillgång till den egna organisationens agenter, användarhantering och historik.
  - `ROLE_CUSTOMER_USER`: Kan se egna agenter och starta dem manuellt, men inte ändra inställningar.

---

## 3. Gränssnitt och Skärmar (MVP)

### Skärm 1: Inloggning (`/login`)
- Enkel och ren inloggningsskärm.
- Logotyp, e-postfält, lösenord och "Logga in"-knapp.
- Vid lyckad inloggning omdirigeras användaren baserat på roll: `ROLE_ADMIN` omdirigeras till `/admin`, övriga till `/dashboard`.

---

### Skärm 2: Kund-Dashboard (`/dashboard`)
Visar en översikt av den inloggade kundens aktiva agenter.

```
[Header: styde.ai — Företagsnamn]
[Statusrad: Alla agenter körs normalt ✓]

[Agent-kort 1]          [Agent-kort 2]          [Agent-kort 3]
  Fakturagranskare        Kundtjänst-Triage       E-postsorterare
  Status: OK              Status: OK              Status: PAUSAD
  Senast: Idag 08:30      Senast: Igår 17:15      Senast: Måndag 09:00
  [Kör manuellt]          [Kör manuellt]          [Kör manuellt]
```

Varje agent-kort visar:
- Agentens namn (t.ex. "Fakturagranskare").
- Statusindikator (Aktiv, Pausad, Fel).
- Tidpunkt för senaste körning.
- Knapp: "Kör manuellt" (triggare).
- Klick på kortet → Omdirigering till detaljvy `/dashboard/agents/[id]`.

---

### Skärm 3: Agent-Detaljvy (`/dashboard/agents/[id]`)
Detaljerad historik och inställningar för en specifik agent.
- **Status:** Grön (OK) eller Röd (Fel).
- **Inställningar:** Redigera miljövariabler/konfigurationer för den specifika agenten (endast tillgängligt för `ROLE_CUSTOMER_ADMIN` och `ROLE_ADMIN`).
- **Historiklista:** De senaste 20 körningarna.
  ```
  | Tidpunkt | Status | Resultat / Logg | Åtgärd |
  |----------|--------|-----------------|--------|
  | 2026-06-25 08:30 | OK | Processat 12 fakturor | [Visa logg] |
  | 2026-06-24 08:30 | OK | Processat 8 fakturor | [Visa logg] |
  | 2026-06-23 08:30 | FEL | Anslutningen mot Fortnox misslyckades | [Visa logg] |
  ```

---

### Skärm 4: Admin-Översikt (`/admin`)
*Endast tillgänglig för `ROLE_ADMIN` (William/Alpedal).*
- **Kundlista:** Översikt över samtliga anslutna kunder, deras status och antal installerade agenter.
- **Globala felloggar:** Visar de senaste felen hos alla agenter i realtid.
- **Ny Kund:** Knapp för att lägga till ny kundorganisation i databasen.

```
[Admin Panel — styde.ai]
Kunder:
| Kundnamn | Agenter | Status | Senaste aktivitet |
|----------|---------|--------|-------------------|
| Företag A AB | 3 st | OK | Idag 08:30 |
| Företag B AB | 1 st | FEL | Igår 15:40 |

[Lägg till kund]  [Globala felloggar]  [Inställningar]
```

---

### Skärm 5: Admin Kundredigering (`/admin/customers/[id]`)
*Endast tillgänglig för `ROLE_ADMIN`.*
- **Lägg till Agent:** Välj en blueprint från `agent-blueprints/`, ge den ett kundspecifikt namn, och konfigurera dess API-nycklar och parametrar.
- **Hantera Användare:** Lägg till eller ta bort kundkonton kopplade till denna kund.
- **Driftstatus:** Stäng av eller slå på alla kundens agenter globalt.

---

## 4. Design & Estetik
- **Basfärg:** Benvit (`#E3E3E4` / `#F4F4F6`) som bakgrund för att ge en premiumkänsla och undvika standard-vitt.
- **Typografi:** Outfit eller Inter via Google Fonts.
- **Statusfärger:** Mjuka harmoniska färger istället för skrikiga standardfärger (t.ex. en dämpad smaragdgrön för OK, dämpad korallröd för FEL, varm bärnsten för PAUSAD).
- **Responsivitet:** Portalen ska fungera utmärkt på både mobil (för chefer på språng) och desktop.

---

## Comments
- 2026-06-24 | william: Skapade första utkastet.
- 2026-06-25 | hermes: Sammanslog kund- och admin-dashboard till en enda Next.js-portal med rollbaserad styrning. Översatte till svenska i enlighet med repo-regler.
