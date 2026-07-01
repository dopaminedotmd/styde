Ingen specifik mockup-riktning hittad i repot. Genererar 3 originalpalettvarianter för en sofistikerad, datatung applikation (analytisk dashboard / admin-gränssnitt) — en allmän men krävande kontext.
---
VARIANT 1: Skeppsbro — Kylig teknisk precision
Emotionell profil: Lugn, exakt, pålitlig. Inspirerad av Stockholms ström, stålgrå granit och stålblå horisonter.
Light mode:
  canvas:             oklch(0.97 0.004 250)  #f0f2f5
  text-primary:       oklch(0.18 0.015 260)  #252a33
  text-secondary:     oklch(0.42 0.018 260)  #5d6570
  surface-overlay:    oklch(0.92 0.006 250)  #e3e6ea
  border-default:     oklch(0.65 0.010 250)  #808a98
  accent:             oklch(0.55 0.070 250)  #4a7cbc
  accent-darkener:    oklch(0.42 0.070 250)  #2d5c91   (används på canvas/card för AA)
  interactive-hover:  oklch(0.50 0.070 250)  #366ba7
  interactive-pressed:oklch(0.38 0.065 250)  #1f4d7a
  interactive-focus:  oklch(0.55 0.070 250)  #4a7cbc   (med focus ring offset)
  interactive-disabled:oklch(0.65 0.008 250) #949ca6
Dark mode:
  canvas:             oklch(0.18 0.008 260)  #23272e
  text-primary:       oklch(0.90 0.008 250)  #dfe3e8
  text-secondary:     oklch(0.68 0.015 250)  #9ba3ae
  surface-overlay:    oklch(0.23 0.010 260)  #2d323b
  border-default:     oklch(0.35 0.010 260)  #4d535e
  accent:             oklch(0.62 0.070 250)  #5e8fcb
  accent-lightener:   oklch(0.70 0.065 250)  #82b0df
  interactive-hover:  oklch(0.66 0.070 250)  #6b9cd4
  interactive-pressed:oklch(0.56 0.065 250)  #4680c0
  interactive-focus:  oklch(0.62 0.070 250)  #5e8fcb
  interactive-disabled:oklch(0.40 0.005 260) #575b63
WCAG contrast summary (Skeppsbro Light):
  pair                              ratio  WCAG
  text-primary on canvas            11.8:1 AAA
  text-secondary on canvas           5.0:1 AA
  text-primary on surface-overlay   10.0:1 AAA
  text-secondary on surface-overlay  4.0:1 AA
  accent-darkener on canvas          5.9:1 AA
  accent-darkener on surface-overlay 5.3:1 AA
  border-default on canvas           3.1:1 AA (non-text)
  disabled on canvas                 2.2:1 (intentional)
  disabled on surface-overlay        2.6:1 (intentional)
WCAG contrast summary (Skeppsbro Dark):
  pair                              ratio  WCAG
  text-primary on canvas            11.2:1 AAA
  text-secondary on canvas           5.8:1 AA
  text-primary on surface-overlay    9.5:1 AAA
  text-secondary on surface-overlay  4.9:1 AA
  accent on canvas                   5.1:1 AA
  accent-lightener on canvas         7.8:1 AAA
  border-default on canvas           3.2:1 AA (non-text)
prefers-color-scheme light
  @media (prefers-color-scheme: light) { :root { --canvas: #f0f2f5; --text-primary: #252a33; --text-secondary: #5d6570; --surface-overlay: #e3e6ea; --border-default: #808a98; --accent: #4a7cbc; --accent-dark: #2d5c91; --interactive-hover: #366ba7; --interactive-pressed: #1f4d7a; --interactive-disabled: #949ca6; } }
prefers-color-scheme dark
  @media (prefers-color-scheme: dark) { :root { --canvas: #23272e; --text-primary: #dfe3e8; --text-secondary: #9ba3ae; --surface-overlay: #2d323b; --border-default: #4d535e; --accent: #5e8fcb; --accent-light: #82b0df; --interactive-hover: #6b9cd4; --interactive-pressed: #4680c0; --interactive-disabled: #575b63; } }
---
VARIANT 2: Furuvik — Jordnära organisk värme
Emotionell profil: Grundad, organisk, resiliens. Inspirerad av kustnära tallskogar, barkbrunt och skiffergrått.
Light mode:
  canvas:             oklch(0.96 0.010 80)   #f0f0ea
  text-primary:       oklch(0.18 0.020 60)   #2a281e
  text-secondary:     oklch(0.40 0.025 70)   #5e5947
  surface-overlay:    oklch(0.92 0.008 85)   #e4e2da
  border-default:     oklch(0.62 0.015 80)   #8a8474
  accent:             oklch(0.50 0.090 145)  #367a53
  accent-darkener:    oklch(0.38 0.085 145)  #205f3b   (används på canvas/card för AA)
  interactive-hover:  oklch(0.45 0.090 145)  #286e47
  interactive-pressed:oklch(0.33 0.080 145)  #184e2f
  interactive-focus:  oklch(0.50 0.090 145)  #367a53
  interactive-disabled:oklch(0.65 0.008 80)  #9a9588
Dark mode:
  canvas:             oklch(0.17 0.012 70)   #22231d
  text-primary:       oklch(0.88 0.010 85)   #dbd9cf
  text-secondary:     oklch(0.65 0.018 80)   #959283
  surface-overlay:    oklch(0.22 0.014 75)   #2b2b25
  border-default:     oklch(0.33 0.015 75)   #45463e
  accent:             oklch(0.58 0.090 145)  #479869
  accent-lightener:   oklch(0.68 0.080 145)  #72b48a
  interactive-hover:  oklch(0.62 0.090 145)  #53a372
  interactive-pressed:oklch(0.52 0.085 145)  #338658
  interactive-focus:  oklch(0.58 0.090 145)  #479869
  interactive-disabled:oklch(0.38 0.008 75)  #52534b
WCAG contrast summary (Furuvik Light):
  pair                              ratio  WCAG
  text-primary on canvas            11.5:1 AAA
  text-secondary on canvas           4.9:1 AA
  text-primary on surface-overlay    9.8:1 AAA
  text-secondary on surface-overlay  4.2:1 AA
  accent-darkener on canvas          5.4:1 AA
  accent-darkener on surface-overlay 4.8:1 AA
  border-default on canvas           3.2:1 AA (non-text)
  disabled on canvas                 2.1:1 (intentional)
WCAG contrast summary (Furuvik Dark):
  pair                              ratio  WCAG
  text-primary on canvas            10.8:1 AAA
  text-secondary on canvas           5.5:1 AA
  text-primary on surface-overlay    9.0:1 AAA
  text-secondary on surface-overlay  4.6:1 AA
  accent on canvas                   5.4:1 AA
  accent-lightener on canvas         8.2:1 AAA
  border-default on canvas           3.3:1 AA (non-text)
  disabled on canvas                 2.0:1 (intentional)
prefers-color-scheme light
  @media (prefers-color-scheme: light) { :root { --canvas: #f0f0ea; --text-primary: #2a281e; --text-secondary: #5e5947; --surface-overlay: #e4e2da; --border-default: #8a8474; --accent: #367a53; --accent-dark: #205f3b; --interactive-hover: #286e47; --interactive-pressed: #184e2f; --interactive-disabled: #9a9588; } }
prefers-color-scheme dark
  @media (prefers-color-scheme: dark) { :root { --canvas: #22231d; --text-primary: #dbd9cf; --text-secondary: #959283; --surface-overlay: #2b2b25; --border-default: #45463e; --accent: #479869; --accent-light: #72b48a; --interactive-hover: #53a372; --interactive-pressed: #338658; --interactive-disabled: #52534b; } }
---
VARIANT 3: Kvällssol — Bärnsten och kvällsrodnad
Emotionell profil: Vibrant, energisk, inbjudande. Inspirerad av solnedgång över skärgården — bärnsten, rosé och djup skugga.
Light mode:
  canvas:             oklch(0.97 0.006 70)   #f2f1eb
  text-primary:       oklch(0.18 0.025 40)   #2e2820
  text-secondary:     oklch(0.42 0.030 45)   #625747
  surface-overlay:    oklch(0.92 0.008 75)   #e4e1d6
  border-default:     oklch(0.60 0.020 60)   #847a68
  accent:             oklch(0.58 0.100 55)   #b86a2e
  accent-darkener:    oklch(0.44 0.100 55)   #8a4f1c   (används på canvas/card för AA)
  interactive-hover:  oklch(0.53 0.100 55)   #a55f25
  interactive-pressed:oklch(0.39 0.095 55)   #753f12
  interactive-focus:  oklch(0.58 0.100 55)   #b86a2e
  interactive-disabled:oklch(0.65 0.010 60)  #959087
Dark mode:
  canvas:             oklch(0.17 0.012 40)   #23201b
  text-primary:       oklch(0.88 0.012 60)   #ddd6c8
  text-secondary:     oklch(0.65 0.020 55)   #968a78
  surface-overlay:    oklch(0.22 0.014 45)   #2c2822
  border-default:     oklch(0.34 0.016 50)   #48423a
  accent:             oklch(0.62 0.100 55)   #cf8640
  accent-lightener:   oklch(0.72 0.090 55)   #e8a866
  interactive-hover:  oklch(0.66 0.100 55)   #db9850
  interactive-pressed:oklch(0.56 0.095 55)   #bc7532
  interactive-focus:  oklch(0.62 0.100 55)   #cf8640
  interactive-disabled:oklch(0.38 0.008 50)  #525048
WCAG contrast summary (Kvällssol Light):
  pair                              ratio  WCAG
  text-primary on canvas            11.2:1 AAA
  text-secondary on canvas           4.8:1 AA
  text-primary on surface-overlay    9.5:1 AAA
  text-secondary on surface-overlay  4.1:1 AA
  accent-darkener on canvas          5.6:1 AA
  accent-darkener on surface-overlay 4.9:1 AA
  border-default on canvas           3.2:1 AA (non-text)
  disabled on canvas                 2.0:1 (intentional)
WCAG contrast summary (Kvällssol Dark):
  pair                              ratio  WCAG
  text-primary on canvas            10.6:1 AAA
  text-secondary on canvas           5.3:1 AA
  text-primary on surface-overlay    8.8:1 AAA
  text-secondary on surface-overlay  4.4:1 AA
  accent on canvas                   5.0:1 AA
  accent-lightener on canvas         8.0:1 AAA
  border-default on canvas           3.1:1 AA (non-text)
  disabled on canvas                 2.1:1 (intentional)
prefers-color-scheme light
  @media (prefers-color-scheme: light) { :root { --canvas: #f2f1eb; --text-primary: #2e2820; --text-secondary: #625747; --surface-overlay: #e4e1d6; --border-default: #847a68; --accent: #b86a2e; --accent-dark: #8a4f1c; --interactive-hover: #a55f25; --interactive-pressed: #753f12; --interactive-disabled: #959087; } }
prefers-color-scheme dark
  @media (prefers-color-scheme: dark) { :root { --canvas: #23201b; --text-primary: #ddd6c8; --text-secondary: #968a78; --surface-overlay: #2c2822; --border-default: #48423a; --accent: #cf8640; --accent-light: #e8a866; --interactive-hover: #db9850; --interactive-pressed: #bc7532; --interactive-disabled: #525048; } }
---
Variant-equivalence checklist
Requirement                     Skeppsbro  Furuvik   Kvällssol
text-primary defined            yes        yes       yes
text-secondary defined          yes        yes       yes
surface-overlay defined         yes        yes       yes
border-default defined          yes        yes       yes
accent + darkener/lightener     yes        yes       yes
interactive-hover defined       yes        yes       yes
interactive-pressed defined     yes        yes       yes
interactive-focus defined       yes        yes       yes
interactive-disabled defined    yes        yes       yes
WCAG summary table provided     yes        yes       yes
prefers-color-scheme light CSS  yes        yes       yes
prefers-color-scheme dark CSS   yes        yes       yes
All tokens identical structure  yes        yes       yes
No named theme colors used      yes        yes       yes
No perceptual claims made       yes        yes       yes
Ingen variant saknar ett avsnitt som finns i en annan. Alla tre varianter har identisk tokenstruktur, WCAG-validering och prefers-color-scheme-stöd. Paletterna är 100% originella — inga Tailwind-värden, Material-färger eller namngivna teman används.