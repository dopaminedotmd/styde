---
title: "Designspecifikation — Konsult-agent v0.1"
date: 2026-06-25
author: hermes
tags: [area/PLAN, status/DRAFT, author/HERMES, type/SPEC]
status: draft
---

# Designspecifikation — Konsult-agent v0.1

> Specifikation för implementering av det första CLI-verktyget för automatiserad kundaudit.

---

## 1. Syfte och omfattning

Verktyget ska ta en företagswebbadress (URL) som indata, crawla startsidan och upp till 5 relevanta interna undersidor, extrahera texten, samt använda OpenAI API för att analysera informationen. Resultatet sparas som en YAML-fil och skrivs ut i terminalen.

---

## 2. Arkitektur och komponenter

### 2.1 Crawler-modul (Requests + BeautifulSoup)
- Indata: Start-URL.
- Hämtar HTML för startsidan.
- Extraherar interna länkar (t.ex. `/om-oss`, `/tjanster`, `/kontakt`).
- Filtrerar och väljer ut max 5 unika undersidor.
- Hämtar HTML för undersidorna synkront.
- Rensar HTML-taggar, scripts och styles för att erhålla ren text.

### 2.2 Analys-modul (OpenAI API)
- Använder OpenAI-klienten i Python.
- Läser API-nyckel från en lokal `.env`-fil eller miljövariabeln `OPENAI_API_KEY`.
- Modell: `gpt-4o-mini`.
- Systemprompt instruerar modellen att utföra analysen och svara strikt i JSON/YAML-format.

### 2.3 Output-modul
- Konverterar LLM-resultatet till YAML-struktur.
- Sparar rapporten till en lokal fil (standard: `report.yaml`).
- Presenterar YAML-strukturen på standard output.

---

## 3. Gränssnitt och Dataformat

### 3.1 CLI-kommando
```bash
python konsult.py https://[foretag].se -o min_rapport.yaml
```

### 3.2 Output YAML-schema
```yaml
test_audit:
  company: "Företagsnamn AB"
  url: "https://foretag.se"
  industry: "bransch"
  estimated_size: "10-20 anställda"
  tech_stack:
    - "System 1"
    - "System 2"
  automation_potential:
    - process: "Processnamn"
      signal: "Observation på webbplatsen som tyder på manuellt arbete"
      priority: 1
      time_savings_hours_per_week: 8
```

---

## 4. Verifieringsplan

### 4.1 Manuella tester
- Provkör mot 3-5 kända svenska webbplatser (t.ex. lokala redovisningsbyråer eller hantverkare).
- Verifiera att ingen känslig information sparas i Git-repot (kontrollera `.gitignore`).
- Kontrollera att utskriften på terminalen matchar det definierade YAML-schemat.

---

## Comments

- 2026-06-25 | hermes: Första specifikationen skapad efter godkänd metod A.
