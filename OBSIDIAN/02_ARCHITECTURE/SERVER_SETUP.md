---
title: "SERVER SETUP — Konfiguration av utvecklings- och produktionsserver"
date: 2026-06-25
author: hermes
tags: [area/ARKITEKTUR, status/APPROVED, author/HERMES, type/SPEC]
status: approved
---

# SERVER SETUP

> Beskrivning av den gemensamma fysiska utvecklings- och produktionsservern för styde.ai. Båda grundarna ansluter och utvecklar direkt på denna maskin.

---

## 1. Topologi och Åtkomst

```
┌─────────────────────────────────────────────────┐
│              SHARED SERVER (fysisk dator)        │
│              (tillgänglig via SSH)               │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │  styde.ai PLATFORM                      │   │
│  │                                          │   │
│  │  Next.js App (kund + admin-vyer)         │   │
│  │  Express API (agent runtime, auth)       │   │
│  │  PostgreSQL (kunder, loggar, agenter)    │   │
│  │  Forge Engine (utvärdering, RAG)         │   │
│  │  (driftsätts i fas 3)                    │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │  ANSLUTNINGAR                            │   │
│  │                                          │   │
│  │  William  ──→ SSH + VS Code Remote       │   │
│  │  Alpedal  ──→ SSH + VS Code Remote       │   │
│  │  Kunder   ──→ HTTPS (via Caddy +         │   │
│  │               Cloudflare Tunnel)         │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  OS: Ubuntu Server 24.04 LTS                    │
│  Databas: PostgreSQL 16                         │
│  Omvänd proxy: Caddy                            │
└─────────────────────────────────────────────────┘
```

---

## 2. Servermiljö och Beroenden

### Operativsystem & Verktyg
- **OS:** Ubuntu Server 24.04 LTS (eller senare stabil LTS).
- **SSH:** OpenSSH-server installerad med avstängd lösenordsinloggning (endast SSH-nycklar tillåtna).
- **Brandvägg:** UFW aktiv, tillåt endast SSH (port 22), HTTP (port 80) och HTTPS (port 443).

### Utvecklingsmiljö
- **Git:** Installerat, repo klonat i `/var/www/styde.ai/` eller i hemkatalogen.
- **Node.js:** v20 LTS installerad via `nvm`.
- **Python:** v3.12 installerad via systemet eller `pyenv` för exekvering av agenter och audits.
- **PostgreSQL 16:** Lokal databas för användarroller, agent-metadata, loggar och tillstånd.

---

## 3. SSH-Konfiguration (Utvecklingsåtkomst)

Både William och Alpedal ska kunna logga in utan lösenord med sina publika SSH-nycklar.

1. Lägg till SSH-nycklar i `~/.ssh/authorized_keys` för respektive användare.
2. Inaktivera lösenordsinloggning i `/etc/ssh/sshd_config`:
   ```bash
   PasswordAuthentication no
   PubkeyAuthentication yes
   ```
3. Starta om SSH-tjänsten:
   ```bash
   sudo systemctl restart sshd
   ```

---

## 4. Databaskonfiguration

Skapa PostgreSQL-databas och användare för applikationen:

```sql
CREATE DATABASE styde;
CREATE USER styde_user WITH PASSWORD 'valfritt_sakert_losenord';
GRANT ALL PRIVILEGES ON DATABASE styde TO styde_user;
```

---

## 5. Caddy Omvänd Proxy (För framtida HTTPS)

När kundportalen ska göras publik använder vi **Caddy** för automatisk hantering av SSL/TLS, kombinerat med **Cloudflare Tunnel** för att exponera servern säkert utan att öppna portar i routern.

Exempel på `Caddyfile`:
```
styde.ai {
    reverse_proxy localhost:3000
}
```

---

## Comments
- 2026-06-25 | hermes: Skapad i enlighet med serverarkitekturen godkänd i total reboot.
