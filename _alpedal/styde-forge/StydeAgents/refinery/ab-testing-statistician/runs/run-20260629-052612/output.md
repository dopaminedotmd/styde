Ingen specifik uppgift tillhandahållen. Demonstrerar med standardscenario: jämförelse av två konversionsrater, fixed-horizon frequentist z-test.
STATISTICAL FRAMEWORK
  method: Standard frequentist two-proportion pooled z-test, fixed-horizon design
  rationale: Two-proportion test är standard för binära utfall med oberoende grupper. Fixed-horizon vald eftersom ingen peeking-plan angavs — enklast, ger lägst N för given power.
  citation: Fleiss, J.L., Levin, B., & Paik, M.C. (2003). Statistical Methods for Rates and Proportions, 3rd ed. Wiley. Formula 3.14.
INPUT PARAMETRAR (demo defaults)
  alpha: 0.05
  power: 0.80
  baseline_conversion_p1: 0.10
  minimum_detectable_effect_absolute: 0.02
  p2: 0.12
  tail: two-sided
DERIVATION — SAMPLE SIZE PER ARM
Canonical formula (Fleiss 3.14, two-proportion, equal allocation):
n = ( Zα/2 * sqrt(2*p_bar*(1-p_bar)) + Zβ * sqrt(p1*(1-p1) + p2*(1-p2)) )^2 / (p2 - p1)^2
where p_bar = (p1 + p2) / 2
Step 1: Z-values from standard normal
  Zα/2 = Z_0.025 = 1.95996
  Zβ = Z_0.20 = 0.84162
  source: standard normal quantile table
Step 2: p_bar
  p_bar = (0.10 + 0.12) / 2 = 0.22 / 2 = 0.11
Step 3: pooled variance term
  2 * p_bar * (1 - p_bar) = 2 * 0.11 * 0.89 = 2 * 0.0979 = 0.1958
  sqrt(0.1958) = 0.44249
  Zα/2 * sqrt(2 * p_bar * (1 - p_bar)) = 1.95996 * 0.44249 = 0.86728
Step 4: alternative variance term
  p1 * (1 - p1) = 0.10 * 0.90 = 0.09
  p2 * (1 - p2) = 0.12 * 0.88 = 0.1056
  sum = 0.09 + 0.1056 = 0.1956
  sqrt(0.1956) = 0.44227
  Zβ * sqrt(p1*(1-p1) + p2*(1-p2)) = 0.84162 * 0.44227 = 0.37221
Step 5: numerator
  (0.86728 + 0.37221)^2 = (1.23949)^2 = 1.53634
Step 6: denominator
  (p2 - p1)^2 = (0.12 - 0.10)^2 = 0.02^2 = 0.0004
Step 7: n per arm
  n = 1.53634 / 0.0004 = 3840.85
  ceiling: 3841 per arm
Total sample: 2 * 3841 = 7682
REVERSE-CHECK: POWER VERIFICATION
Compute power at n=3841 per arm to verify identity holds:
H0 pooled proportion under null: p_pooled = 0.11
  SE_null = sqrt(p_pooled * (1-p_pooled) * (1/n1 + 1/n2))
  SE_null = sqrt(0.11 * 0.89 * (1/3841 + 1/3841))
  SE_null = sqrt(0.0979 * (2/3841))
  SE_null = sqrt(0.0979 * 0.00052070)
  SE_null = sqrt(0.000050977)
  SE_null = 0.007140
HA standard error (no pooling):
  SE_alt = sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
  SE_alt = sqrt(0.09/3841 + 0.1056/3841)
  SE_alt = sqrt(0.000023432 + 0.000027493)
  SE_alt = sqrt(0.000050925)
  SE_alt = 0.007136
Non-centrality parameter approach:
  Z_power = (p2 - p1) / SE_alt - Zα/2 * (SE_null / SE_alt)
  Z_power = 0.02 / 0.007136 - 1.95996 * (0.007140 / 0.007136)
  Z_power = 2.80269 - 1.95996 * 1.00056
  Z_power = 2.80269 - 1.96106
  Z_power = 0.84163
Power = Φ(Z_power) = Φ(0.84163) = 0.8000
Target: 0.80 — match within 0.01%. Reverse-check PASS.
CONFIDENCE INTERVAL DECOMPOSITION (scenario: observed p_hat1=0.10, p_hat2=0.12)
Point estimate:
  delta_hat = 0.12 - 0.10 = 0.02
Standard error of difference:
  SE_diff = sqrt(p_hat1*(1-p_hat1)/n1 + p_hat2*(1-p_hat2)/n2)
  SE_diff = sqrt(0.10*0.90/3841 + 0.12*0.88/3841)
  SE_diff = sqrt(0.09/3841 + 0.1056/3841)
  SE_diff = sqrt(0.000023432 + 0.000027493)
  SE_diff = sqrt(0.000050925)
  SE_diff = 0.007136
Z-critical:
  Z_0.025 = 1.95996
Margin of error:
  MoE = Z_0.025 * SE_diff = 1.95996 * 0.007136 = 0.013987
Confidence interval bounds:
  lower: 0.02 - 0.013987 = 0.006013
  upper: 0.02 + 0.013987 = 0.033987
95% CI: [0.0060, 0.0340]
CI width check:
  2 * MoE = 2 * 0.013987 = 0.027974
  observed width = 0.033987 - 0.006013 = 0.027974 — match.
METHOD DISAMBIGUATION TABLE
framework            stopping_rule         alpha_spending    power_implication    peeking_correction
fixed-horizon z      one analysis at end   N/A (single look)  optimal (lowest N)   none possible — no interim
O'Brien-Fleming      up to K interim       very conservative  +3-5% sample size    stringent early, relaxed late
                      looks allowed         early, total ~α    vs fixed-horizon
Pocock               up to K interim       constant at each   +10-15% sample       uniform boundary — easier
                      looks allowed         look, total ~α     size vs fixed        to implement
Wang-Tsiatis Delta   up to K interim       tunable via Δ       between OBF and      adjustable stringency
                      looks allowed         parameter           Pocock
Selection: fixed-horizon z-test selected. Ingen peeking-plan specificerad, inga interim-analyser efterfrågade, ingen sequential-korrektion motiverad. Vid avsaknad av peeking-krav är fixed-horizon optimalt — ger lägst total N.
RESULTAT
sample_size_per_arm: 3841
total_sample_size: 7682
alpha: 0.05
power: 0.80
baseline_rate_p1: 0.10
treatment_rate_p2: 0.12
mde_absolute: 0.02
mde_relative: 20.0%
expected_ci_half_width_at_n: 0.01399
expected_ci: [0.0060, 0.0340]
CAVEAT: Detta är en demonstration med standardvärden. För faktisk analys, specificera: baseline-konverteringsrat, minsta detekterbara effekt (absolut eller relativ), önskad power, alfa-nivå, och eventuell sequential/peeking-design. Alla mellansteg, substitutioner och reverse-check redovisade ovan — inga dolda beräkningar.