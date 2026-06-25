---
name: ca-offert-writer
description: Skapar formella offerter i obsidian/04_clients/_active/ utifrån OFFERT_TEMPLATE.md. Följer prissättningsregler för Audit, Build och Operate (SLA-nivåer) baserat på audit-rapporter.
version: 1.1.0
owner: william
last-updated: 2026-06-25
---

# ca-offert-writer

## Purpose

Write formal and structured quotes based on audit results and the pricing rules established in [[MASTER_PLAN_FINAL]] and [[PRICING_MODEL]].

## Quote Writing Instructions

1. **Read the template:** Use the content of `obsidian/04_clients/templates/OFFERT_TEMPLATE.md` as the base template.
2. **Define frontmatter:**
   - Title: `Quote — {Customer Name}`
   - Tags: `[area/CLIENT, status/REVIEW, author/WILLIAM, type/REPORT]`
   - Status: `review`
3. **Pricing Rules (MASTER_PLAN_FINAL §4):**
   - **Audit:** Fixed price 19,900 SEK.
   - **Build (Package 2):** From 99,000 SEK up to 300,000 SEK (quoted based on number of agents and complexity).
     - *Deduction Clause (Mandatory):* When purchasing Build (Package 2) within 30 days, the cost of Audit (19,900 SEK) is deducted from the total Build amount.
   - **Operate (Package 3):** Ongoing monthly cost based on support level (SLA):
     - **Basic:** 4,900 SEK/month (Email support, 24h response time weekdays).
     - **Pro:** 9,900 SEK/month (Email + phone, 8h response time weekdays).
     - **Enterprise:** 19,900 SEK/month (Priority support, 2h response time all days).
4. **Write to file:**
   - Save the quote to: `obsidian/04_clients/_active/{customer_name}_OFFERT.md`.
5. **Format:**
   - Use standardized Obsidian syntax and wikilinks.
   - Add a wikilink to the completed report (`{customer_name}_AUDIT.md`).

## Comments

- 2026-06-25 | hermes: Updated description to Swedish, bumped version to 1.1.0 and added comments section.
- 2026-06-25 | hermes: Translated body prose from Swedish to English. Added translation note.

---
**Translation note:** This file was translated from Swedish to English on 2026-06-25. All frontmatter YAML fields remain unchanged.
