---
name: ca-audit-reporter
description: Skriver strukturerade och handlingskraftiga audit-rapporter i obsidian/04_clients/_active/ utifrån AUDIT_TEMPLATE.md. Används efter att en kundaudit har genomförts med ca-audit-agent.
version: 1.1.0
owner: alpedal
last-updated: 2026-06-25
---

# ca-audit-reporter

## Purpose

Write structured, clear, and actionable audit reports based on the data collected by [[ca-audit-agent]].

## Report Writing Instructions

1. **Read the template:** Use the content of `obsidian/04_clients/templates/AUDIT_TEMPLATE.md` as the base template.
2. **Define frontmatter:**
   - Title: `Audit Report — {Customer Name}`
   - Tags: `[area/CLIENT, status/REVIEW, author/ALPEDAL, type/REPORT]`
   - Status: `review`
3. **Fill in the sections:**
   - **Summary:** Write 2-3 sentences summarizing the customer's challenges, pain points, and automation potential.
   - **Company Info:** Fill in the table with the company's name, industry, number of employees, IT responsible, current systems, and estimated monthly IT cost.
   - **Systems:** List the systems, their purpose, number of users, and whether they are automatable.
   - **Mapped Flows:** Describe each identified flow in detail (trigger, steps, systems, time, pain).
   - **Opportunities:** Fill in the table with priority order, ROI classification, complexity, and estimated build time.
   - **Recommendation:** Clearly describe which 2-3 agents should be built first.
4. **Format:**
   - Use standardized Obsidian syntax (callouts, wikilinks).
   - Add wikilinks to relevant person profiles (e.g., [[william]], [[alpedal]]) and to the upcoming quote (`OFFERT_{CUSTOMER_NAME}.md`).
5. **Output:**
   - Save the completed report to: `obsidian/04_clients/_active/{customer_name}_AUDIT.md`.

## Comments

- 2026-06-25 | hermes: Updated description to Swedish, bumped version to 1.1.0 and added comments section.
- 2026-06-25 | hermes: Translated body prose from Swedish to English. Added translation note.

---
**Translation note:** This file was translated from Swedish to English on 2026-06-25. All frontmatter YAML fields remain unchanged.
