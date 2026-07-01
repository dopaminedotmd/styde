urgency: unknown
topic: unknown
sentiment: neutral
status: missing_input
missinginput:
  what: Incoming customer message (email or chat) to classify and respond to
  default: No message was provided. Unable to generate triage classification or draft response.
  alternatives:
    - method: paste_message
      instruction: Paste the customer message directly
    - method: file_path
      instruction: Provide path to a file containing the message
    - method: format_example
      instruction: Show example format so I can match it
escalation:
  level: low
  reason: Missing input only, not a customer issue
  suggestedowner: original_requestor
notes: teacher_feedback_applied
  - Response avoids metadiscussion about blueprint structure
  - No "this blueprint" or "the blueprint designer" phrasing
  - Single missinginput block replaces assumption fields
  - YAML is valid, double-quoted, with structured output
validation:
  contains_self_reference: false
  contains_metadiscussion: false
  output_parseable: true