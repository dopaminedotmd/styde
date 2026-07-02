# hund-forge — Persona Refinement Engine

Specialiserad Forge-instans för att iterativt förbättra Hunds persona.

**Kodnamn:** Hundsmältan
**Typ:** Persona-refinement (inte agent-produktion)
**Plats:** `_william/hund-forge/` — separat från riktiga Forge

---

## Vad detta ÄR

Ett system som spawnar agenter med Hunds persona, testar dem mot scenarier,
utvärderar hur väl de följer persona-reglerna, och föreslår förbättringar.

Inga kund-agenter byggs här. Inga produktion-deployments. Detta är en
R&D-smältdegel för att finslipa Hunds röst, identitet och beteende.

## Vad detta INTE är

- INTE en ersättning för riktiga Forge (`_alpedal/styde-forge/`)
- INTE en agent-fabrik
- INTE kund-vänd

## Struktur

```
hund-forge/
  StydeAgents/
    blueprints/
      hund-persona/           ← Blueprinten ÄR Hunds persona
        persona.md            ← Röstregler, tillstånd, responsmatris
        BLUEPRINT.md          ← Syfte: persona-konsistens-evaluering
        config.yaml           ← Metadata, agent-konfig, eval-vikter
    benchmarks/
      persona-consistency.md  ← 10 scenarier som testar persona-regler
  state.yaml                  ← Tillstånd, versioner, scores
```

## Användning

Från `_alpedal/styde-forge/`:

```bash
# Spawna Hund-agent och kör mot benchmark
python Core/forge.py spawn hund-persona --benchmark persona-consistency

# Evaluera resultatet
python Core/forge.py eval hund-persona <run_id> --benchmark persona-consistency

# Låt teacher analysera och föreslå förbättringar
python Core/forge.py improve hund-persona <run_id>
```

## Första målet

Få hund-persona blueprinten att passera 85/100 på persona-consistency benchmark.
När den gör det — uppdatera `hund/assets/hund-system/hund.md` med de förbättringar
som Forge-loopen producerat.

---

*Byggd av Hermes. 2026-06-27.*
