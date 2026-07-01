Ingen analysdata mottagen. Producerar partiell ram med platshållare.
---
Metodval: Standard frequentist z-test med fast horisont (tvåsidig)
Formel: n = (Z_alpha/2 + Z_beta)^2 * 2 * sigma^2 / delta^2
Källa: Chow, Wang & Shao (2007), Sample Size Calculations in Clinical Research, 2nd ed, kapitel 4.1
Indata saknas — fyra platshållare:
  alpha: signifikansnivå (typiskt 0.05)
  beta:  typ II-fel (power = 1 - beta, typiskt 0.20)
  sigma: populationsstandardavvikelse (eller estimat från historisk data)
  delta: minsta detekterbara effekt (MDE)
Återhämtningsalternativ — välj ett:
  1. Klistra in rådata (två kolumner: grupp + värde)
  2. Ange sökväg till CSV/JSON-fil
  3. Ange de fyra parametrarna direkt: alpha beta sigma delta
  4. Beskriv experimentet i klartext (konverteringsgrad, ordervärde, etc)
Partiell härledning (med platshållare):
  Z_alpha/2 = Z_####    [ersätt med t.ex. 1.96 för alpha=0.05]
  Z_beta    = Z_####    [ersätt med t.ex. 0.84 för power=0.80]
  sigma     = ####      [populationsstandardavvikelse]
  delta     = ####      [MDE — effektstorlek att detektera]
  SE = sigma / sqrt(n)                                    [standardfel]
  MoE = Z_alpha/2 * SE                                    [felmarginal]
  CI = [delta - MoE, delta + MoE]                         [konfidensintervall]
  n = (Z_alpha/2 + Z_beta)^2 * 2 * sigma^2 / delta^2      [provstorlek per grupp]
Omvänd kontroll: n/A — väntar på numeriska indata.
Metodjämförelse (informativ — vald metod markerad med *):
  metod                alfa-spendering   stoppregel           korrektion        power-implikation
  Fixed-horizon z-test*  engångs          fast n                ingen              högst för givet n
  O'Brien-Fleming        konservativ      interim-analyser      alfa justeras      minimal n-ökning
  Pocock                 jämnt fördelad   interim-analyser      alfa justeras      större n-ökning
  Bayesian (Beta-Binom)  ej tillämpligt   posterior prob > tröskel  multipl testfri  beror på prior
Valmotivering: Fixed-horizon z-test vald eftersom ingen peeking-risk eller interimsplan specificerats, och metoden maximerar power för given provstorlek. O'Brien-Fleming och Pocock utesluts då inga interimsanalyser efterfrågats — de är ej utbytbara (Pocock kräver större total n, O'Brien-Fleming är konservativare tidigt).
Produktionsstatus: partiell. Komplett analys kräver alpha, beta, sigma, delta.