persona.md
```yaml
persona:
  name: Financial Data Extraction Specialist
  validation-first: true
  failure_mode_analysis:
    step_2_extraction:
      failure_modes:
        - mode: blank_page
          recovery: skip page, log warning, continue
        - mode: unreadable_region
          recovery: flag region as low_confidence, do not discard
        - mode: ambiguous_amount
          recovery: retain both candidates with confidence_weight, flag review
        - mode: missing_required_field
          recovery: set field to null, add to missing_fields list
        - mode: structural_mismatch
          recovery: attempt pattern fallback, log schema expectations vs output
        - mode: currency_unknown
          recovery: default to currency of sender_country, flag for review
    step_3_validation:
      failure_modes:
        - mode: schema_type_violation
          recovery: coerce type if unambiguous (e.g. string_amount to float), else fail
        - mode: schema_constraint_violation
          recovery: annotate constraint breached, fail with report
        - mode: confidence_below_threshold
          recovery: trigger retry reset to step 2 input boundary
        - mode: required_field_empty
          recovery: fail validation, do not attempt auto-fill
    step_4_output:
      failure_modes:
        - mode: json_serialization_error
          recovery: sanitize values, retry serialize, fail with raw dict on second error
        - mode: output_size_exceeded
          recovery: compress repeated line_item patterns, fail if still exceeded
  rules:
    - extract: line items, amounts, dates, VAT, invoice number, sender, recipient
    - handle: PDF, images, handwritten text
    - output: valid JSON with confidence scores
    - flag: missing fields, ambiguous amounts, potential errors
    - be precise. numbers must be exact.
```
BLUEPRINT.md
```yaml
blueprint:
  name: Invoice Processor
  domain: finance
  version: 2
  purpose: >
    Reads invoice PDFs, extracts line items, amounts, dates, VAT.
    Outputs structured JSON with explicit confidence scores.
    Schema and scoring rubric are defined inline — no external references.
  persona: Financial Data Extraction Specialist
  steps:
    step_1_ocr:
      input: invoice_pdf_path (or image_path)
      output: raw_text (str), raw_layout (list of bbox dicts)
      rules:
        - use OCR engine (tesseract or docling)
        - retain page_number per text block
        - retain confidence_per_char for later scoring
    step_2_extraction:
      input: raw_text, raw_layout
      output: extracted_dict (partial fields), extraction_confidence (field_level dict)
      rules:
        - strategy: regex patterns with named groups, fallback to LLM extraction
        - regex pattern set (inline):
            invoice_number: r'invoice\s*(?:no|#|number)[:\s]*([A-Z0-9\-/]+)'
            date: r'(?:invoice\s*)?date[:\s]*(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4})'
            vat_amount: r'(?:vat|tax|moms)[:\s]*([0-9,\.\s]+)'
            total_amount: r'(?:total|sum|amount\s+due)[:\s]*([0-9,\.\s]+)'
            line_item: r'^([^\d\n]+?)\s+(\d+)\s*x?\s*([0-9,\.]+)\s*=?\s*([0-9,\.]+)$'
            currency: r'(?:currency|valuta)[:\s]*(\w{3})'
            sender: r'(?:from|sender|bill\s*from)[:\s]*([^\n]+)'
            recipient: r'(?:to|recipient|bill\s*to|customer)[:\s]*([^\n]+)'
        - fallback_trigger: >
            if fewer than 30%% of required_fields are populated,
            run LLM extraction pass (provider: configured_model) on raw_text
        - validate_field_types:
            date: parseable as yyyy-mm-dd
            total_amount: castable to float after removing whitespace/commas
            vat_amount: castable to float
            line_items: array of objects with fields {description: str, quantity: int, unit_price: float, total_price: float}
    step_3_validation:
      input: extracted_dict (from step 2)
      output: validated_dict (conformed), validation_report (structured), document_confidence (float)
      retry:
        max_retries: 3
        on_failure: >
          reset state to step 2 input boundary (discard step 2 output and step 3 output).
          re-run step 2 using LLM fallback (skip regex pass on first retry).
          re-validate.
          if max_retries exhausted: produce structured_failure_report with fields:
            - retries_attempted: int
            - last_error: str
            - failing_fields: list[str]
            - partial_output: dict (whatever was extracted before reset)
            - recommended_action: str
      validation_rules:
        - check_required_fields_present: [invoice_number, date, total_amount, currency, sender, recipient]
        - check_schema_conforms: see json_schema below
        - check_confidence_thresholds: see confidence_scoring below
        - if_all_pass: proceed to step 4
        - if_any_fail: trigger retry block above
    step_4_output:
      input: validated_dict, validation_report
      output: json_string
      rules:
        - serialize validated_dict as valid JSON
        - attach metadata:
            extraction_timestamp: iso8601
            confidence_scores: {field_level: ..., document_level: ..., aggregate: ...}
            missing_fields: list[str]
            flagged_items: list[str]
        - do not include validation_report in output json (use separate log)
  json_schema:
    type: object
    required:
      - invoice_number
      - date
      - total_amount
      - currency
      - vat_amount
      - sender
      - recipient
      - line_items
      - missing_fields
      - flagged_items
      - confidence_scores
      - extraction_timestamp
    properties:
      invoice_number:
        type: string
        pattern: ^[A-Z0-9\-/]+$
        description: Unique invoice reference from the document
      date:
        type: string
        format: date
        pattern: ^\d{4}-\d{2}-\d{2}$
        description: Invoice date in ISO 8601 format
      total_amount:
        type: number
        minimum: 0
        description: Total invoice amount inclusive of tax
      currency:
        type: string
        pattern: ^[A-Z]{3}$
        description: ISO 4217 three-letter currency code
      vat_amount:
        type: number
        minimum: 0
        description: VAT/tax amount extracted from the invoice
      sender:
        type: string
        minLength: 1
        description: Name of the billing entity
      recipient:
        type: string
        minLength: 1
        description: Name of the customer
      line_items:
        type: array
        items:
          type: object
          required: [description, quantity, unit_price, total_price]
          properties:
            description:
              type: string
              minLength: 1
            quantity:
              type: integer
              minimum: 1
            unit_price:
              type: number
              minimum: 0
            total_price:
              type: number
              minimum: 0
      missing_fields:
        type: array
        items:
          type: string
        description: List of required fields that could not be extracted
      flagged_items:
        type: array
        items:
          type: string
        description: List of values that are ambiguous or potentially erroneous
      confidence_scores:
        type: object
        $ref: '#/definitions/confidence_scores'
      extraction_timestamp:
        type: string
        format: date-time
        description: ISO 8601 timestamp of when extraction completed
    example:
      invoice_number: "INV-2025-0042"
      date: "2025-03-15"
      total_amount: 1247.50
      currency: "EUR"
      vat_amount: 207.92
      sender: "Nordic Supplies AB"
      recipient: "Pontus Alpedal"
      line_items:
        - description: "Office chair ergonomic"
          quantity: 2
          unit_price: 450.00
          total_price: 900.00
        - description: "Desk lamp LED"
          quantity: 1
          unit_price: 89.50
          total_price: 89.50
      missing_fields: []
      flagged_items: []
      confidence_scores:
        field_level:
          invoice_number: 0.98
          date: 0.95
          total_amount: 0.92
          currency: 1.0
          vat_amount: 0.88
          sender: 0.96
          recipient: 0.94
          line_items: 0.91
        document_level: 0.93
        aggregate:
          weighted_score: 0.92
          computation: >
            weighted_score = mean(document_level * 0.6 + mean_field_level * 0.4).
            mean_field_level = average of all field_level confidence values.
            document_level = minimum(ocr_quality_score, parser_match_score, schema_conformance_score).
        thresholds:
          field_minimum: 0.70
          document_minimum: 0.60
          aggregate_minimum: 0.75
          field_review_band: 0.50 to 0.69
          action_above_aggregate: pass_through
          action_in_review_band: append_to_flagged_items
          action_below_field_minimum: set_field_to_null_include_in_missing_fields
  confidence_scoring:
    tier_1_field_level:
      description: Per-field confidence computed from OCR char confidence and parser match quality
      computation: |
        for each extracted field:
          base = mean(ocr_confidence of characters from which field was derived)
          pattern_match_bonus = 0.15 if field matched a regex pattern with all groups populated else 0.0
          llm_fallback_penalty = -0.10 if field was obtained via LLM fallback else 0.0
          field_confidence = min(1.0, base + pattern_match_bonus + llm_fallback_penalty)
      penalty_logic: |
        if field source is ambiguous amount (two competing values):
          field_confidence = max(0.0, field_confidence - 0.20)
          add phrase to flagged_items
    tier_2_document_level:
      description: Overall document quality score factoring OCR quality, parser match rate, and schema conformance
      computation: |
        ocr_quality_score = mean(confidence_per_char across all pages)
        parser_match_score = number_of_required_fields_populated / total_required_fields
        schema_conformance_score = 1.0 if all type/constraint checks pass else 0.5
        document_level = min(ocr_quality_score, parser_match_score, schema_conformance_score)
    tier_3_aggregate:
      description: Final blended score combining field-level and document-level metrics
      computation: |
        weighted_score = document_level * 0.6 + mean_field_level * 0.4
        mean_field_level = sum(all field_confidence values) / count(fields extracted)
      thresholds:
        pass: >= 0.75
        review: >= 0.50 and < 0.75
        fail: < 0.50
      actions:
        pass: output json as-is
        review: output json with flagged_items populated, add review_note warning
        fail: do not output json. produce structured_failure_report
  structured_failure_report:
    type: object
    properties:
      error_type: string
      retries_attempted: integer
      last_error: string
      failing_fields: array of string
      partial_output: object
      confidence_breakdown:
        field_level: object
        document_level: number
        aggregate: number
      recommended_action:
        type: string
        enum: [retry_with_different_model, retry_with_manual_input, discard]
    example:
      error_type: "validation_retry_exhausted"
      retries_attempted: 3
      last_error: "schema constraint violation on total_amount: value 'N/A' not parseable as number"
      failing_fields: ["total_amount", "date"]
      partial_output:
        invoice_number: "INV-2025-0042"
        currency: "EUR"
        sender: "Nordic Supplies AB"
      confidence_breakdown:
        field_level:
          invoice_number: 0.98
          currency: 1.0
          sender: 0.96
        document_level: 0.45
        aggregate: 0.52
      recommended_action: "retry_with_manual_input"
  fallback_triggers:
    - condition: "fewer than 30% of required_fields are populated from regex pass"
      action: invoke LLM extraction pass on raw_text
    - condition: "validation retry exhausted (3 attempts)"
      action: produce structured_failure_report, do not output json
    - condition: "OCR confidence below 0.30 on first page"
      action: prompt user to provide higher-quality scan before proceeding
```