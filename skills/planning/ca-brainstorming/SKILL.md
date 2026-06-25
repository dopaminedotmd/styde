---
name: ca-brainstorming
description: Måste användas före all form av kodning, projekt-scaffolding eller implementation. Tvingar fram design-first och mini-spec som ska godkännas av William innan kod skrivs. Använd alltid denna skill när en ny uppgift eller ändring ska påbörjas.
version: 2.1.0
owner: william
last-updated: 2026-06-25
---

# ca-brainstorming — Design före kod (v2.0)

> Uppgraderad från obra/superpowers brainstorming (S-rank). Se `.agents/skills/brainstorming/SKILL.md` för original.

Tvingar fram design-first före implementation. Varje projekt, oavsett storlek, går igenom denna process.

<HARD-GATE>
Skriv INTE kod, scaffolda INGET projekt, anropa INGEN implementations-skill förrän en design är presenterad och godkänd av William. Detta gäller ALLT arbete oavsett hur enkelt det verkar.
</HARD-GATE>

## Anti-Pattern: "Det här är för enkelt för att behöva design"

Allt går igenom denna process. En todo-lista, en env-fil, en config-ändring — allt. "Enkla" saker är där otestade antaganden orsakar mest slöseri. Designen kan vara kort (några meningar), men du MÅSTE presentera den och få godkännande.

## Arbetsflöde (9 steg)

Utför i ordning. Skapa en task per steg.

1. **Utforska projektkontext** — läs filer, docs, senaste commits
2. **Erbjud visual companion just-in-time** — först när en fråga VERKLIGEN skulle bli tydligare visuellt. Inte upfront.
3. **Ställ klargörande frågor** — en i taget. Förstå syfte, begränsningar, successkriterier
4. **Föreslå 2-3 angreppssätt** — med trade-offs och din rekommendation
5. **Presentera design** — i sektioner, få godkännande efter varje sektion
6. **Skriv design-dokument** — spara till `OBSIDIAN/01_PLAN/{YYYY-MM-DD}-{topic}-design.md`
7. **Spec self-review** — kolla placeholders, motsägelser, tvetydighet, scope
8. **William granskar spec** — be William läsa specen innan implementation
9. **Övergå till implementation** — anropa `ca-plan-creator` för att skapa implementationsplan

## Nyckelprinciper

- **En fråga i taget** — överväldiga aldrig med flera frågor samtidigt
- **Föreslå alternativ** — alltid 2-3 angreppssätt
- **YAGNI** — ta bort onödiga features från alla designer
- **Inkrementell validering** — presentera, få godkännande, gå vidare
- **Var flexibel** — gå tillbaka och förtydliga när något inte är vettigt

## Spec Self-Review (efter skriven spec)

1. **Placeholder-scan:** Finns "TBD", "TODO", ofullständiga sektioner? Fixa.
2. **Intern konsistens:** Motsäger sektioner varandra? Matchar arkitektur feature-beskrivningarna?
3. **Scope-koll:** Fokuserad nog för en implementationsplan, eller behövs nedbrytning?
4. **Tvetydighetskoll:** Kan något krav tolkas på två sätt? Välj ett och gör det explicit.

Fixa inline. Ingen ny granskning behövs.

## Design för isolering och tydlighet

- Bryt systemet i mindre enheter med ett tydligt syfte var
- Varje enhet ska kunna förstås och testas oberoende
- Kan någon förstå vad en enhet gör utan att läsa dess interna kod? Kan du ändra implementationen utan att bryta användare? Om inte — gränserna är fel.

## Efter design

William granskar specen → godkänner → `ca-plan-creator` skapar implementationsplanen.

## Kommentarer

- 2026-06-25 | hermes: Uppdaterade beskrivningen till mer proaktiv svenska, bumpade version till 2.1.0 och lade till kommentarssektion.
