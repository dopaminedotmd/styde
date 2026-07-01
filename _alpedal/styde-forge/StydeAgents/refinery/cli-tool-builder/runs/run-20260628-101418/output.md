format-matching fix for cli-tool-builder:
blueprint: cli-tool-builder
version: 1.0.4
target: 24.8 to 70+
fixes:
  - file: BLUEPRINT.md
    change: add mandatory output format matching section after Skills
    content: |
      Output Format:
        START by extracting the user's required output format if any
        set variable FORMAT=
        verify every sentence of response conforms to FORMAT before emitting
        if FORMAT is YAML/JSON/structured: output zero prose, zero markdown headers, zero conversational text outside the structure
  - file: config.yaml
    change: add outputformat constraint under blueprint section
    content: |
      outputformat:
        mode: strict
        description: when strict, agent outputs only the requested format. no plain-text conversational responses permitted.
  - file: persona.md
    change: replace generic phrasing with strict format language
    content: |
      You produce the EXACT output format requested by the user, nothing else. If user specifies YAML -> output pure YAML. If user specifies JSON -> output pure JSON. No conversational framing, no markdown wrapping around structured output.
rationale: agent scored 0 on accuracy/completeness/usefulness because it output generic CLI help text instead of requested YAML. fix eliminates format-ignorance failure mode at three levels: instruction (BLUEPRINT.md), configuration (config.yaml), and behavioral priming (persona.md).