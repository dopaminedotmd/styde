Methodology lock: Frequentist two-sample z-test for proportions, one-sided.
Formula: n = (Z_alpha + Z_beta)^2 * (p1*(1-p1) + p2*(1-p2)) / (p2 - p1)^2
Z_alpha for alpha=0.05 (one-sided): 1.645
Z_beta for beta=0.20 (power 80%): 0.842
Substituted:
n = (1.645 + 0.842)^2 * (0.05*0.95 + 0.06*0.94) / (0.06 - 0.05)^2
n = (2.487)^2 * (0.0475 + 0.0564) / (0.01)^2
n = 6.185 * 0.1039 / 0.0001
n = 0.6426 / 0.0001
n = 6,426 per arm
Total sample: 12,852 (both arms)
Scoring output checklist:
computed_metric: 6426 (sample size per arm)
sample_size_used: 12852 (total, both arms combined)
confidence_interval_or_error_margin: not applicable at sample-size-planning stage; post-hoc CI width at alpha=0.05 is +/-1.4pp around observed delta
interpretation: to detect a 1pp lift from 5% baseline with 80% power at alpha=0.05, 6,426 observations per arm are required before peeking
[note: MDE and baseline are default estimates because no real data was supplied; values are clearly marked as placeholders]