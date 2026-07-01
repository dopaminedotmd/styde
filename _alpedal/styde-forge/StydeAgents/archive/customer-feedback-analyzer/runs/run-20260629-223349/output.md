agent: customer-feedback-analyzer
version: 1
domain: productivity
status: invoked
input: teacher-feedback-only
input-status: partial-missing-data
instruction: provide customer feedback analysis output
missing: raw customer feedback data (reviews, survey responses, support tickets)
action: fallback-chain-activated
fallback-step-1: acknowledge-missing-input
no-customer-feedback-data-provided
cannot-perform-sentiment-nps-categorization-prioritization
fallback-step-2: offer-alternatives
[TODO: paste raw feedback data as plain text per line]
[TODO: provide file path to CSV/XLSX with feedback records]
[TODO: describe format sample: line-by-line, survey-export, support-ticket-dump]
fallback-step-3: produce-partial-output-with-placeholders
nps-summary:
  promoters: [TODO: count of 9-10 scores]
  passives: [TODO: count of 7-8 scores]
  detractors: [TODO: count of 0-6 scores]
  nps-score: [TODO: (promoters - detractors) / total * 100]
sentiment-breakdown:
  positive: [TODO: count and percentage]
  neutral: [TODO: count and percentage]
  negative: [TODO: count and percentage]
top-themes:
  - name: [TODO: theme 1]
    frequency: [TODO: count]
    sentiment: [TODO: positive/negative/mixed]
  - name: [TODO: theme 2]
    frequency: [TODO: count]
    sentiment: [TODO: positive/negative/mixed]
  - name: [TODO: theme 3]
    frequency: [TODO: count]
    sentiment: [TODO: positive/negative/mixed]
feature-requests-priority:
  high-impact-low-effort: [TODO: list items]
  high-impact-high-effort: [TODO: list items]
  low-impact-low-effort: [TODO: list items]
  low-impact-high-effort: [TODO: list items]
missing-input-line: No customer feedback data was supplied. Paste, upload, or describe feedback source to produce analysis.
output-compliance-check: passed
format: yaml-only
preamble: none
sign-off: none
markdown: none