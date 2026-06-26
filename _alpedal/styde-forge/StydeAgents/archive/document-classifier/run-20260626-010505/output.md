document_classifier blueprint v1
type: document classification & routing
confidence: 95%
handlers:
  invoice: accounting@company.com or AP system
  contract: legal@company.com or CLM platform
  report: analyst@company.com or BI dashboard
  CV: hr@company.com or ATS
  letter: correspondence@company.com or mail system
  form: processing@company.com or forms engine
  receipt: expense@company.com or ERP
  manual: support@company.com or knowledge base
  policy: compliance@company.com or policy portal
  presentation: comms@company.com or slide library
fallback: general-inbox@company.com | confidence < 70% -> human review
multi-page: concatenate pages, extract dominant type from page-level votes
scanned: OCR via tesseract or document-ai, preserve layout signals
mixed: page-by-page classification, route each section to respective handler