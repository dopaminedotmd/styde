Svar:
Låt oss lägga till Hermes C i jämförelsen.

Hermes A: Har tillgång till vårt 48 GB USB (280–350 elit-agenter + ~180–250 extraherade, högkvalitativa skills + lineage + teacher logs).
Hermes B: Har bara de vanliga ~85 built-in skills som Hermes Agent kommer med från början.
Hermes C: Har tillgång till alla skills som finns publikt på internet (GitHub, Awesome-lists, community packs, npm/pip-paket, blogginlägg, etc.).

Nu jämför vi de tre agenterna när de får exakt samma prompt:
"Skapa en komplex hemsida/program."
Sammanfattande bedömning
För en komplex och produktionsinriktad applikation blir rangordningen oftast följande:





























PlaceringAgentFörväntad kvalitetKommentar1Hermes AHögstBäst balans mellan kvalitet, relevans och konsekvens2Hermes CBra men ojämnKan vara mycket bra, men också mediokert3Hermes BLägstMest generisk och boilerplate-tung
Skillnaden mellan Hermes A och Hermes C är ofta mindre än mellan Hermes A och Hermes B, men den är fortfarande tydlig på flera viktiga områden.
Detaljerad jämförelse




































































DimensionHermes A (48 GB USB)Hermes C (Allt på internet)Hermes B (Endast base skills)VinnareKodkvalitet & MaintainabilityMycket hög. Använder beprövade, extraherade mönsterVarierande. Kan hitta både extremt bra och dåliga mönsterMedel. Mycket boilerplateAArkitektur & DesignStark. Har tillgång till många validerade arkitekturmönsterKan vara mycket bra (om den hittar rätt saker), men ofta inkonsistentOfta generiskAEdge cases & RobusthetMycket bra. Har sett många tidigare misstag via teacher logsBra potential, men måste själv "upptäcka" problemenSvagareAInnovation & NytänkandeMedel. Tenderar att använda beprövade lösningarHögst. Kan hitta nya, kreativa eller nischade lösningarLägstCKonsekvens & TillförlitlighetHögst. Kunskapen är kuraterad och testadLägst. Mycket brus och ojämn kvalitetMedelAUppdaterad kunskapBra, men inte alltid den allra senasteBäst. Kan hitta de senaste biblioteken och mönstrenSämstCTid till bra resultatSnabbast. Många problem redan löstaMedel. Måste sålla bland mycket informationLångsammastARisk för dåliga valLågHög. Kan välja populära men dåliga bibliotekMedelA
Varför Hermes A oftast vinner över Hermes C
Även om Hermes C har tillgång till mycket mer information än Hermes A, så har den flera nackdelar:

Kvalitetsbrus: På internet finns det extremt många mediokra, föråldrade eller direkt dåliga skills och exempel. Hermes C måste själv sålla.
Brist på kontext: Den vet inte vilka mönster som faktiskt har fungerat bra inom just detta system över tid. Den saknar lineage och teacher logs.
Inkonsekvens: Hermes C kan ge ett fantastiskt resultat ena gången och ett mediokert nästa gång, beroende på vad den hittar.
Överbelastning: För mycket information kan göra att den väljer en "okej" lösning istället för den bästa.

Hermes A har istället en kuraterad kunskapsbas där mycket av sållningsarbetet redan är gjort. De skills och mönster som finns på USB:et har passerat kvalitetsgranskning och visat sig fungera bra i praktiken.
När Hermes C kan vara bättre än Hermes A
Hermes C kan ibland prestera bättre än Hermes A i följande fall:

När uppgiften är mycket nischad eller tekniskt ny (t.ex. ny webbläsar-API, nytt ramverk, specifik prestandaoptimering).
När man vill ha hög kreativitet och oväntade lösningar.
När Hermes A:s kunskap börjar bli lite "gammal" inom ett snabbt föränderligt område.

Slutsats – Tre vägar





























AgentStyrkaSvaghetBäst lämpad förHermes AHög och konsekvent kvalitetKan vara mindre innovativProduktionskod och komplexa systemHermes CHög innovationskraft + breddOjämn kvalitet och brusForskning, experiment och nya teknikerHermes BEnkelhetGenerisk och boilerplate-tungEnkla till medelstora uppgifter
Sammanfattning:
För en komplex hemsida/program är rangordningen oftast:

Hermes A (vårt 48 GB USB) — Bästa totalresultat
Hermes C (Allt på internet) — Kan vara nära A, men mer ojämnt
Hermes B (Endast base skills) — Tydligt sämre
