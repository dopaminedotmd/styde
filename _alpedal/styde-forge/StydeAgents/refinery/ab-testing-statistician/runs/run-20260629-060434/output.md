Ingen parametrar angivna. Visar ramverksberedskap med formel.
framework: Standard frequentist z-test, fixed horizon, two-sided
källa: Chow, Shao & Wang (2008), Sample Size Calculations in Clinical Research, 2nd ed, kap 3
Grundformel:
n_per_arm = (Z_alpha/2 + Z_beta)^2 * 2 * sigma^2 / delta^2
Termdefinitioner:
  Z_alpha/2: kritiskt z-värde för tvåsidigt test vid signifikansnivå alpha
  Z_beta: z-värde för önskad power (1 - beta)
  sigma: populationens standardavvikelse (eller poolad SD)
  delta: minsta detekterbara effekt (MDE), absolut skillnad mellan grupper
Alla fyra parametrar saknas. Formeln är redo för insättning.
Exempel vid alpha=0.05, power=0.80, sigma=1, delta=0.2:
  Z_alpha/2 = Z_0.025 = 1.96
  Z_beta = Z_0.20 = 0.8416
  n = (1.96 + 0.8416)^2 * 2 * 1^2 / 0.2^2
    = (2.8016)^2 * 2 * 1 / 0.04
    = 7.8490 * 2 / 0.04
    = 15.698 / 0.04
    = 392.45
  n_per_arm = 393 (avrundat uppåt)
Reverse-check:
  SE = sigma * sqrt(2/n) = 1 * sqrt(2/393) = 1 * sqrt(0.005089) = 0.07134
  MoE = Z_alpha/2 * SE = 1.96 * 0.07134 = 0.1398
  CI-halvbredd vid n=393 täcker 0.1398, vilket ger power för delta=0.2:
  Z_obs = delta/SE = 0.2/0.07134 = 2.8035
  Power = P(Z > Z_alpha/2 - Z_obs) + P(Z < -Z_alpha/2 - Z_obs)
        = P(Z > 1.96 - 2.8035) = P(Z > -0.8435) = 0.8005
  0.8005 ≈ 0.80. Identitet håller inom 0.1%. Verifierad.
Leverera alpha, power, sigma, delta för numerisk output.