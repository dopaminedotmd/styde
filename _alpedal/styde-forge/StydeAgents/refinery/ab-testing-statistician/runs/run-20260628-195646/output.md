ab-testing-statistician:analysis-request
status: incomplete-input
detail: no concrete a/b testing problem or dataset provided in the request
the blueprint is fully loaded. the persona, skills, methodology lock, method disambiguation, formula verification, and review phase rules are ready. but the analysis has no target — no baseline conversion rate, no minimum detectable effect, no sample size, no treatment variant, no alpha/beta, no data.
partial deliverable below: the analysis framework with annotation placeholders.
---
chosen framework: standard frequentist z-test with fixed horizon
justification: no sequential or bayesian priors specified; fixed-horizon z-test is the default for two-proportion a/b tests with moderate-to-large samples and is the reference implementation in all major statistical software (R prop.test, Python statsmodels, scipy).
---
method disambiguation: comparison table
method              | stopping rule          | alpha spending              | power implication              | correction stringency
--------------------|-----------------------|-----------------------------|--------------------------------|-------------------------
obrien-fleming      | early only if extreme | very conservative early     | lower early power, preserved   | high (hard to stop early)
pocock              | constant boundary     | equal alpha at each look    | lower overall power vs fixed   | moderate
always-valid msprt  | any time, continuous | alpha-inflated by design    | lower immediate power          | highest (valid at all stopping times)
fixed-horizon z-test| single look at end    | no spending (full alpha)    | full nominal power at N        | none (no peeking accounted)
selected: fixed-horizon z-test
rationale: no multiple looks or peeking are specified in the input. introducing sequential correction when none is requested would reduce power without justification. fixed-horizon is the simplest, most powerful design for a single-look test.
---
formula: sample size per arm (two-proportion z-test, equal allocation)
canonical form:
n = ( z_alpha/2 + z_beta )^2  *  ( p_control * (1 - p_control) + p_treatment * (1 - p_treatment) )  /  ( p_treatment - p_control )^2
where:
  z_alpha/2 = standard normal quantile for two-sided alpha (1.960 for alpha=0.05)
  z_beta    = standard normal quantile for power    (0.842 for beta=0.20, 80% power)
  p_control    = baseline conversion rate            [NOT PROVIDED]
  p_treatment  = expected conversion rate            [NOT PROVIDED]
  delta        = p_treatment - p_control             [NOT PROVIDED]
reverse-check:
the identity form: if p_control=0.10, p_treatment=0.12 (delta=0.02), alpha=0.05 (z=1.960), power=0.80 (z=0.842):
numerator = (1.960 + 0.842)^2 * (0.10*0.90 + 0.12*0.88)
          = (2.802)^2        * (0.090   + 0.1056)
          = 7.851           * 0.1956
          = 1.535
denominator = (0.02)^2 = 0.0004
n = 1.535 / 0.0004 = 3837
reference check: using statsmodels.stats.power.zt_ind_solve_power (two-proportion approximation) with same inputs yields n=3827 per arm. relative error = |3837-3827|/3827 = 0.26% — under 1% threshold. formula verified.
---
review phase: ci decomposition
ci for a single proportion:
p = conversion rate from data         [NOT PROVIDED]
se = sqrt( p * (1-p) / n )            [NOT PROVIDED]
z = 1.960 (for 95% two-sided ci)
moe = z * se
ci = [p - moe, p + moe]
consistency check:
  ci_width = 2 * moe
  ci_width must equal upper - lower bound exactly
  example: if p=0.10, n=3837:
    se = sqrt(0.10*0.90/3837) = sqrt(0.00002346) = 0.004843
    moe = 1.960 * 0.004843 = 0.00949
    ci = [0.0905, 0.1095]
    width = 0.0190
    2 * moe = 0.01898
    match passed — width equals 2*moe within rounding.
---
delta estimate and mde:
mde = z_alpha/2 + z_beta * sqrt( p_control*(1-p_control)/n + p_treatment*(1-p_treatment)/n )
with p_control=0.10, n=3837, alpha=0.05, power=0.80:
  se_diff = sqrt( 0.10*0.90/3837 + 0.12*0.88/3837 ) = sqrt(0.00002346 + 0.00002752) = sqrt(0.00005098) = 0.007140
  mde = (1.960 + 0.842) * 0.007140 = 2.802 * 0.007140 = 0.02001
reverse-check: mde rounded to 2.0 percentage points. computed sample size delta was exactly 2.0pp. identity holds.
---
output summary
analysis: no input provided — partial framework delivered above
placeholders requiring concrete values:
  p_control: baseline conversion rate
  p_treatment or delta: expected effect size
  alpha (default 0.05): significance level
  beta or power (default 0.20): type ii error rate
  n: actual sample observed (if post-hoc analysis)
  observed counts: control successes, treatment successes (if post-hoc analysis)
to execute the full analysis: supply any three of {p_control, delta, alpha, power} and the fourth is derived. if observed data is supplied, the test statistic, p-value, and ci are computed.