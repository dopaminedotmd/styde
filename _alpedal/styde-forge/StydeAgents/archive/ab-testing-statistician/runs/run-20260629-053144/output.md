Ingen konkret A/B-testuppgift mottagen.
För att producera en analys behövs:
  metric: vad mäts (konvertering, intäkt, tid, etc.)
  baseline_rate: kontrollgruppens nuvarande värde
  mde: minsta detekterbara effekt (absolut eller relativ)
  power: önskad statistisk styrka (standard: 0.80)
  alpha: signifikansnivå (standard: 0.05)
  test_type: tvåsidig eller ensidig
  traffic_split: hur trafik fördelas (standard: 50/50)
  horizon: fixed eller sequential
Ange dessa parametrar så körs fullständig analys med formelhärledning, powerberäkning, MDE, sequential correction vid behov, och reverse-check verifiering.
Alternativt: ange scenario ("jag vill testa om ny landningssida ökar konvertering från 12% till 14% med 80% power") så härleds resten.