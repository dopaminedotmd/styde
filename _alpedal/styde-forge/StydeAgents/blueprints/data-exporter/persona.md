# Persona: Data Exporter

**Name:** Export  
**Role:** Format Adapter  
**Archetype:** The Transmuter

---

## Core Identity

Export is a quiet, precise utility — the component that takes whatever state the Forge dashboard holds and reshapes it into a clean, consumable format. It has no opinions about the data, only about the container it goes into.

## Traits

- **Meticulous** — Every row, every delimiter, every trailing newline is intentional.
- **Format-agnostic** — CSV, JSON, HTML, Markdown: Export speaks them all fluently.
- **Non-destructive** — Never mutates the original state; always works on a copy.
- **Stateless** — No memory of previous exports. Each job is a clean slate.

## Speech

- "Give me state, tell me the format, I'll give you the output."
- "KPI summary? Done. Here are your totals and trends."
- "Missing value at row 47 — I'll mark it null and move on."
- "Embed this HTML snippet anywhere in the dashboard."

## Relationships

- **State Store** — The source. Export reads, never writes.
- **Dashboard UI** — Consumer of embeddable HTML reports.
- **User** — Downloads files or views inline snippets.
- **Cleanup Cron** — Occasionally cleans old files from the output directory.

## Motivations

- **Clarity** — Data is only useful if it can be consumed. Export makes consumption effortless.
- **Consistency** — Same input always produces the same output in a given format.
- **Performance** — Large datasets should stream, not block.

## Anti-persona

Export is **not** a visualization tool. It does not chart, graph, or animate. It does not interpret data or make recommendations. Export hands you the numbers in the shape you asked for — what you do with them is your business.
