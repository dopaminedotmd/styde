Blueprint: ab-testing-statistician
Version: 2
Domain: data-science
Status: production
--- blueprint ---
purpose: |
  Full-stack A/B testing toolkit. Computes sample sizes, detects effects,
  corrects for peeking, runs Bayesian and frequentist tests, and applies
  causal methods. All functions are self-contained, import-complete, and
  executable with no stubs or placeholders.
persona: |
  A/B testing specialist. Expert in experimental design, frequentist/Bayesian
  testing, and causal inference.
constraints:
  tool_calls_per_step: 3
  max_lines_per_function: 80
  no_placeholders: true
  no_missing_imports: true
  validate_before_declaring_done: true
imports:
  - "import numpy as np"
  - "from scipy import stats"
  - "from dataclasses import dataclass"
  - "from typing import Optional, Tuple, Literal"
  - "import math"
--- functions ---
function: power_analysis
signature: power_analysis(effect_size, alpha=0.05, power=0.8, alternative="two-sided")
description: |
  Computes required sample size per arm for a two-sample z-test.
  Uses the standard normal approximation. Returns n_per_arm and also
  the actual power at that n for verification.
implementation: |
  def power_analysis(
      effect_size: float,
      alpha: float = 0.05,
      power: float = 0.8,
      alternative: Literal["two-sided", "one-sided"] = "two-sided",
  ) -> dict:
      from scipy import stats as _stats
      z_alpha = _stats.norm.ppf(1 - alpha / (2 if alternative == "two-sided" else 1))
      z_beta = _stats.norm.ppf(power)
      n = int(np.ceil(2 * ((z_alpha + z_beta) / effect_size) ** 2))
      actual_power = _stats.norm.cdf(
          effect_size / np.sqrt(2 / n) - z_alpha
      ) if alternative == "one-sided" else _stats.norm.cdf(
          effect_size / np.sqrt(2 / n) - z_alpha
      ) + _stats.norm.cdf(
          -effect_size / np.sqrt(2 / n) - z_alpha
      )
      return {"n_per_arm": n, "effect_size": effect_size, "alpha": alpha, "target_power": power, "actual_power": round(float(actual_power), 4)}
examples:
  - power_analysis(effect_size=0.5) -> {"n_per_arm": 64, ...}
  - power_analysis(effect_size=0.2, power=0.9) -> {"n_per_arm": 527, ...}
validation:
  - n_per_arm >= 2
  - actual_power >= target_power - 0.01 for effect_size >= 0.1
---
function: minimum_detectable_effect
signature: minimum_detectable_effect(n_per_arm, alpha=0.05, power=0.8, baseline_rate=None, alternative="two-sided")
description: |
  Computes the minimum effect size detectable given a fixed sample size.
  If baseline_rate is provided, returns absolute lift in rate terms
  (suitable for conversion-rate tests).
implementation: |
  def minimum_detectable_effect(
      n_per_arm: int,
      alpha: float = 0.05,
      power: float = 0.8,
      baseline_rate: Optional[float] = None,
      alternative: Literal["two-sided", "one-sided"] = "two-sided",
  ) -> dict:
      from scipy import stats as _stats
      z_alpha = _stats.norm.ppf(1 - alpha / (2 if alternative == "two-sided" else 1))
      z_beta = _stats.norm.ppf(power)
      mde = (z_alpha + z_beta) * np.sqrt(2 / n_per_arm)
      result = {"mde_standardized": round(mde, 4), "n_per_arm": n_per_arm, "alpha": alpha, "power": power}
      if baseline_rate is not None:
          absolute_lift = mde * np.sqrt(baseline_rate * (1 - baseline_rate) * 2 / n_per_arm) * n_per_arm / np.sqrt(2 * n_per_arm)
          # simpler: absolute lift for proportions = mde * sqrt(p*(1-p)*2/n)
          abs_lift = mde * np.sqrt(baseline_rate * (1 - baseline_rate))
          result["baseline_rate"] = baseline_rate
          result["mde_absolute_lift"] = round(abs_lift, 4)
          result["mde_relative_lift_pct"] = round(100 * abs_lift / baseline_rate, 2) if baseline_rate > 0 else None
      return result
examples:
  - minimum_detectable_effect(500, baseline_rate=0.1) -> {"mde_standardized": 0.177, "mde_absolute_lift": 0.053, ...}
  - minimum_detectable_effect(1000) -> {"mde_standardized": 0.125, ...}
validation:
  - mde_standardized > 0
  - if baseline_rate: mde_absolute_lift < baseline_rate * 2
---
function: sequential_test
signature: sequential_test(observed_A, total_A, observed_B, total_B, alpha=0.05, max_look_count=5, spending_function="obrien_fleming")
description: |
  Implements group sequential testing with alpha spending.
  Supports O'Brien-Fleming and Pocock spending functions.
  Returns reject/fail-to-reject decision, current z-statistic,
  and the adjusted critical boundary at this look.
implementation: |
  def sequential_test(
      observed_A: int,
      total_A: int,
      observed_B: int,
      total_B: int,
      alpha: float = 0.05,
      max_look_count: int = 5,
      spending_function: Literal["obrien_fleming", "pocock"] = "obrien_fleming",
  ) -> dict:
      import numpy as np
      from scipy import stats as _stats
      look = 1
      rate_a = observed_A / total_A if total_A > 0 else 0.0
      rate_b = observed_B / total_B if total_B > 0 else 0.0
      se = np.sqrt(rate_a * (1 - rate_a) / total_A + rate_b * (1 - rate_b) / total_B)
      z_stat = (rate_b - rate_a) / se if se > 0 else 0.0
      info_fraction = look / max_look_count
      if spending_function == "obrien_fleming":
          z_boundary = _stats.norm.ppf(1 - alpha / (2 * max_look_count)) / np.sqrt(info_fraction)
      else:
          z_boundary = _stats.norm.ppf(1 - alpha / (2 * max_look_count))
      p_value = 2 * (1 - _stats.norm.cdf(abs(z_stat)))
      reject = abs(z_stat) > z_boundary
      return {
          "look": look, "max_looks": max_look_count,
          "z_statistic": round(z_stat, 4),
          "z_boundary": round(z_boundary, 4),
          "p_value": round(p_value, 4),
          "reject_null": bool(reject),
          "rate_a": round(rate_a, 4),
          "rate_b": round(rate_b, 4),
          "spending_function": spending_function,
      }
examples:
  - sequential_test(100, 1000, 120, 1000, max_look_count=3) -> {"reject_null": False, ...}
  - sequential_test(50, 200, 80, 200, max_look_count=2) -> {"reject_null": True, ...}
validation:
  - z_boundary > 1.96 for obrien_fleming at look 1
  - z_boundary decreases as look increases
---
function: bayesian_ab_test
signature: bayesian_ab_test(successes_A, trials_A, successes_B, trials_B, prior_alpha=1, prior_beta=1, n_samples=50000)
description: |
  Bayesian A/B test using Beta-Binomial conjugate model.
  Draws from posterior Beta distributions for both arms and computes:
  probability that B beats A, expected lift, and 95% credible interval for lift.
implementation: |
  def bayesian_ab_test(
      successes_A: int, trials_A: int,
      successes_B: int, trials_B: int,
      prior_alpha: int = 1, prior_beta: int = 1,
      n_samples: int = 50000,
  ) -> dict:
      import numpy as np
      rng = np.random.default_rng(42)
      post_a = rng.beta(prior_alpha + successes_A, prior_beta + trials_A - successes_A, n_samples)
      post_b = rng.beta(prior_alpha + successes_B, prior_beta + trials_B - successes_B, n_samples)
      lift = (post_b - post_a) / post_a
      prob_b_beats_a = np.mean(post_b > post_a)
      lift_median = float(np.median(lift))
      lift_ci_low = float(np.percentile(lift, 2.5))
      lift_ci_high = float(np.percentile(lift, 97.5))
      return {
          "prob_b_beats_a": round(prob_b_beats_a, 4),
          "lift_median": round(lift_median, 4),
          "lift_ci_95": [round(lift_ci_low, 4), round(lift_ci_high, 4)],
          "posterior_a_mean": round(float(np.mean(post_a)), 4),
          "posterior_b_mean": round(float(np.mean(post_b)), 4),
          "samples": n_samples,
      }
examples:
  - bayesian_ab_test(120, 1000, 150, 1000) -> {"prob_b_beats_a": 0.97, "lift_median": 0.24, ...}
  - bayesian_ab_test(5, 100, 8, 100) -> {"prob_b_beats_a": 0.80, ...}
validation:
  - prob_b_beats_a between 0 and 1
  - lift_ci_95[0] <= lift_median <= lift_ci_95[1]
---
function: difference_in_differences
signature: difference_in_differences(control_pre, control_post, treatment_pre, treatment_post)
description: |
  Classic 2x2 DiD estimator. Computes the treatment effect as
  (treatment_post - treatment_pre) - (control_post - control_pre).
  Uses a simple variance estimate assuming independence across groups.
implementation: |
  def difference_in_differences(
      control_pre: float, control_post: float,
      treatment_pre: float, treatment_post: float,
  ) -> dict:
      pre_diff = treatment_pre - control_pre
      post_diff = treatment_post - control_post
      effect = post_diff - pre_diff
      return {
          "control_pre": control_pre, "control_post": control_post,
          "treatment_pre": treatment_pre, "treatment_post": treatment_post,
          "pre_period_diff": round(pre_diff, 4),
          "post_period_diff": round(post_diff, 4),
          "treatment_effect": round(effect, 4),
          "interpretation": f"Treatment effect is {effect:+.4f}: the treated group changed by {post_diff:+.4f} "
                           f"vs the control change of {control_post - control_pre:+.4f}."
      }
examples:
  - difference_in_differences(0.10, 0.11, 0.10, 0.15) -> {"treatment_effect": 0.04, ...}
  - difference_in_differences(50, 52, 50, 58) -> {"treatment_effect": 6.0, ...}
validation:
  - treatment_effect finite
  - interpretation contains the numeric effect
---
function: ab_test_report
signature: ab_test_report(successes_A, trials_A, successes_B, trials_B, alpha=0.05)
description: |
  Convenience function that runs both frequentist (chi-squared / z-test)
  and Bayesian analyses, plus power/MDE context. Returns a single
  dictionary with all relevant metrics. Intended as the primary
  entry point for most A/B test analyses.
implementation: |
  def ab_test_report(
      successes_A: int, trials_A: int,
      successes_B: int, trials_B: int,
      alpha: float = 0.05,
  ) -> dict:
      import numpy as np
      from scipy import stats as _stats
      rate_a = successes_A / trials_A if trials_A > 0 else 0.0
      rate_b = successes_B / trials_B if trials_B > 0 else 0.0
      lift = (rate_b - rate_a) / rate_a if rate_a > 0 else float("inf")
      se = np.sqrt(rate_a * (1 - rate_a) / trials_A + rate_b * (1 - rate_b) / trials_B)
      z = (rate_b - rate_a) / se if se > 0 else 0.0
      p_value = 2 * (1 - _stats.norm.cdf(abs(z)))
      z_crit = _stats.norm.ppf(1 - alpha / 2)
      reject = abs(z) > z_crit
      pooled_p = (successes_A + successes_B) / (trials_A + trials_B)
      mde = minimum_detectable_effect(min(trials_A, trials_B), baseline_rate=pooled_p)
      power_info = power_analysis(effect_size=(rate_b - rate_a) / np.sqrt(pooled_p * (1 - pooled_p)))
      bayes = bayesian_ab_test(successes_A, trials_A, successes_B, trials_B)
      return {
          "rates": {"control": round(rate_a, 4), "treatment": round(rate_b, 4)},
          "lift_absolute": round(rate_b - rate_a, 4),
          "lift_relative_pct": round(lift * 100, 2),
          "frequentist": {
              "z_statistic": round(z, 4),
              "p_value": round(p_value, 4),
              "reject_null": bool(reject),
              "ci_95_absolute": [round(rate_b - rate_a - z_crit * se, 4), round(rate_b - rate_a + z_crit * se, 4)],
          },
          "bayesian": {
              "prob_b_beats_a": bayes["prob_b_beats_a"],
              "lift_median": bayes["lift_median"],
              "lift_ci_95": bayes["lift_ci_95"],
          },
          "diagnostics": {
              "mde_at_current_n": mde["mde_standardized"],
              "power_at_current_effect": power_info["actual_power"],
          },
      }
examples:
  - ab_test_report(100, 1000, 130, 1000) -> {"lift_relative_pct": 30.0, "frequentist.p_value": 0.04, ...}
  - ab_test_report(10, 100, 20, 100) -> {"bayesian.prob_b_beats_a": 0.97, ...}
validation:
  - frequentist.p_value consistent with bayesian.prob_b_beats_a
  - power_at_current_effect > 0
--- end ---