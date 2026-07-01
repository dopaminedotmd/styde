INSUFFICIENTDATA: No customer feedback text provided for analysis. No NPS survey data provided. No feature request descriptions provided.
Assumptions used for this partial output: Default empty corpus analysis. All metrics reported as zero/null. Categorization buckets shown as empty templates.
YAML
analysis:
  total_feedback_count: 0
  source: UNKNOWN
  status: PARTIAL
  gaps:
    - missing_feedback_texts: true
    - missing_nps_responses: true
    - missing_feature_requests: true
sentiment:
  positive: 0
  neutral: 0
  negative: 0
  average_sentiment_score: null
nps:
  promoters: 0
  passives: 0
  detractors: 0
  total_responses: 0
  nps_score: null
  calculation: 'INSUFFICIENTDATA - numerator undefined'
categories:
  none: []
feature_priorities:
  none: []
fallback_options:
  - option: paste feedback texts inline
    result: complete analysis with sentiment scores
  - option: read feedback from file
    expected_format: CSV with columns [id, text, nps_score, category]
    path: default to ./feedback.csv if unspecified
  - option: assume defaults and proceed
    note: generates synthetic placeholder analysis with zero counts only