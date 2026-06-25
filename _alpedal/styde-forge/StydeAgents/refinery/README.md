# Agent Blueprints (Pre-Existing — styde.ai Format)

Denna katalog innehåller specifikationer och konfigurationer för styde.ai-agenter (blueprints).

## Blueprint-format
Varje blueprint ligger i en egen underkatalog och består av följande filer:

1. **`blueprint.yaml`**: Metadata, kostnad, beräknad tidsbesparing, krav och inställningar.
2. **`persona.md`**: Agentens personlighet, tonläge, rollbeskrivning och beteende.
3. **`prompt_template.md`**: Systemprompt för agenten med plats för variabler (t.ex. `{{variabel}}`).
4. **`tools.yaml`**: Beskrivning av de externa verktyg och API:er som agenten har tillgång till.
5. **`tests/`** (valfritt): `input.json` och `expected.json` för automatiserad utvärdering.

Se referensdokumentation under `obsidian/03_forge/styde-forge/01_Vision/Blueprint_Catalog.md` för inspiration.

---

> **⚠️ NOTICE:** Dessa blueprints är i **gamla formatet** (från styde.ai, Williams projekt).
> **Styde Forge** (Pontus) använder ett nytt blueprint-format som anges i
> `Planing/v1.0_Phase1/02_Forge_Spawn/Blueprint_Loading_System.md`.
>
> Skillnader:
> | Aspekt | Old (styde.ai) | New (Forge) |
> |--------|---------------|-------------|
> | Config | `blueprint.yaml` + `tools.yaml` | `config.yaml` (allt i ett) |
> | Prompt | `prompt_template.md` | `BLUEPRINT.md` (purpose) + `persona.md` (personality) |
> | Skills | Ingen separat mapp | `skills/` katalog med SKILL.md |
> | Språk | Svenska | Engelska |
>
> De gamla blueprints finns kvar som referens och kommer att konverteras vid Phase 1.
