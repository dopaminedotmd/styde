triage:
  confidence: low
  missingfields:
    - message_content
    - customer_id
    - channel
  category: UNKNOWN
  priority: UNABLETODETERMINE
  sentiment: UNKNOWN
  urgency: UNKNOWN
  topic: UNKNOWN
escalation:
  level: 0
  reason: No input message provided. Cannot classify without source material.
  suggestedowner: system
response:
  notice: No input message received for triage.
  suggestion: Provide a customer message via one of these methods:
    method1: paste the message text directly into this input
    method2: provide a file path to a text file containing the message
  draftresponse: null
  drafttemplate: '[MISSINGINFO] We received your inquiry and are looking into it. [MISSINGINFO_DETAILS]'
To triage: paste a customer message, include a file path, or describe the issue. Any of those works.