api_conventions:
  version: v1
  base_path: /api/v1
  http_verbs:
    allowed:
      - GET      # Read/query resources
      - POST     # Create resources or trigger actions
      - PUT      # Full replacement of resources
      - PATCH    # Partial update of resources
      - DELETE   # Remove resources
    forbidden:
      - HEAD     # Use GET with limit=0 equivalent
      - OPTIONS  # Handled by framework CORS middleware
  path_templates:
    collection:  /{resource}
    document:    /{resource}/{id}
    sub_collection:  /{resource}/{id}/{sub_resource}
    sub_document:    /{resource}/{id}/{sub_resource}/{sub_id}
    action:      /{resource}/{id}/{action_name}
  error_envelope:
    format:
      error:
        code: string           # machine-readable, e.g. "validation_error"
        message: string        # human-readable summary
        details: array         # per-field or per-item errors
          - field: string      # dotted path, e.g. "user.email"
            message: string    # specific message
            code: string       # optional sub-code
        request_id: string     # correlation ID from X-Request-Id
        timestamp: string      # ISO 8601
    status_mapping:
      400: bad_request
      401: unauthorized
      403: forbidden
      404: not_found
      409: conflict
      422: validation_error      # PRIMARY error shape — used even for 400/404/409
      429: rate_limited
      500: internal_error
      503: service_unavailable
    rule: envelope format is identical across ALL status codes — never change shape per status
    rule: in degraded mode (503), omit details array to reduce serialization cost
  edge_case_checklist:
    concurrent_modification:
      - accept ETag/If-Match on PUT/PATCH/DELETE
      - return 412 Precondition Failed on mismatch
      - return 409 Conflict when version field in body differs
    empty_results:
      - return empty array [] not null
      - status 200 not 404 for empty collection
      - total_count: 0 in paginated response
    degraded_state:
      - return 503 with retry-after header
      - omit optional enrichment fields
      - log degraded path at WARN level
      - never cascade write failures into read paths
    partial_failure:
      - batch endpoints return per-item status array
      - top-level status is 200 unless ALL items failed (then 500)
    idempotency:
      - POST to action endpoints accept Idempotency-Key header
      - return cached 200/201 on replay within 24h window
      - return 422 on key collision (same key, different request body)
efficiency_guardrails:
  max_output_per_deliverable:
    schema: 200 lines
    endpoint_definition: 80 lines
    code_example: 60 lines
    total_per_response: 400 lines
  target_completion_steps:
    simple_endpoint: 5 reasoning steps max
    complex_crud: 10 reasoning steps max
    full_resource_group: 15 reasoning steps max
  stop_condition_checklist:
    - does the output satisfy the requirement without extra decoration?
      yes: stop. no: proceed
    - is every line necessary for the core deliverable?
      yes: stop. no: strip one unnecessary line, re-check
    - would a junior engineer understand this without explanation?
      yes: proceed to next. no: add one comment line, re-check
    - is there a path template or error shape i can reuse instead of inventing?
      yes: reuse it. no: add to conventions first
    - have i handled the edge cases from the checklist?
      yes: stop. no: add edge case handling
    - total usable value / total verbosity > 0.8?
      yes: stop. no: compress further
  anti_patterns:
    - "Documentation-bloat": writing a docstring longer than the code
    - "Example-proliferation": more than one example per endpoint shape
    - "Over-validation": validating the same constraint in middleware + body + db
    - "Defensive-speculation": handling error cases that can't occur in the current stack
    - "Status-code-sprawl": using more than 4 distinct codes per resource group