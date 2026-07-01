triage:
  confidence: low
  missingfields: [input_text]
  category: UNKNOWN
  priority: UNABLETODETERMINE
  sentiment: UNKNOWN
  draftresponse: 'Thank you for contacting us. [MISSINGINFO: No customer message provided. Unable to perform triage without input text.] To proceed, please reply with your question or concern and our team will assist you promptly.'
resolution paths:
  - path: 'I can read the customer inquiry from a file. Please provide the file path and I will parse and triage it immediately.'
  - path: 'Paste the raw email or chat text here and I will classify urgency, topic, sentiment, and produce a draft response within seconds.'
  - path: 'If you are unsure what format to use, here is a minimal example I can work from: "I ordered item #4392 five days ago and it still has not shipped. This is unacceptable." I will classify and respond from any message with comparable detail.'