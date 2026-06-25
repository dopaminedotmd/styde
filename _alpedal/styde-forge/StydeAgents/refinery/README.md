# Agent Blueprints

Denna katalog innehåller specifikationer och konfigurationer för styde.ai-agenter (blueprints).

## Blueprint-format
Varje blueprint ligger i en egen underkatalog och består av följande filer:

1. **`blueprint.yaml`**: Metadata, kostnad, beräknad tidsbesparing, krav och inställningar.
2. **`persona.md`**: Agentens personlighet, tonläge, rollbeskrivning och beteende.
3. **`prompt_template.md`**: Systemprompt för agenten med plats för variabler (t.ex. `{{variabel}}`).
4. **`tools.yaml`**: Beskrivning av de externa verktyg och API:er som agenten har tillgång till.
5. **`tests/`** (valfritt): `input.json` och `expected.json` för automatiserad utvärdering.

Se referensdokumentation under `obsidian/03_forge/styde-forge/01_Vision/Blueprint_Catalog.md` för inspiration.
