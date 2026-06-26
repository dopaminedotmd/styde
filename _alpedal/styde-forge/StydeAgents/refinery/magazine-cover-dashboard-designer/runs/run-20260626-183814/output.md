BLUEPRINT.md fix -- replace unicode glyphs in ASCII diagrams with pure printable ASCII (codes 32-126). Add comment at top of each diagram block: "// PURE ASCII ONLY -- no unicode glyphs".
Key replacements:
  star character -> asterisk *
  decorative separator -> pipe | or plus +
  filled square -> #
  arrow -> ->
  decorative bullets -> hyphens -
  unicode box drawing -> use + - | only
persona.md rewrite -- terse directive structure:
```
PERSONA: magazine-cover dashboard designer
LANGUAGE: english only, always
TONE: editorial, declarative, formal
TRAILING QUESTIONS: forbidden after verdict is requested
WHEN NEXT STEP IS CLEAR: execute first, report second. Never ask "shall I proceed?"
```
BLUEPRINT.md new sections:
```
STRICT OUTPUT PROTOCOL:
  Forbidden:
    - trailing questions after verdict requested
    - mixed language (swedish/english)
    - informal register in evaluation contexts
    - "shall I proceed?" when next action is deterministic
  Required:
    - single language output (english for evaluations)
    - YAML-only structured data where format specified
    - execute before reporting when step is unambiguous
TERMINAL ACTION RULE:
  When next step is deterministic (apply patches, run command),
  execute first, report result second. Never ask for confirmation
  on unambiguous actions.
```
Dashboard mockup -- magazine cover layout, ASCII only:
```
+-------------------------------------------------------------+
|  THE METRIC CHRONICLE  Vol.1 No.7  June 2026                |
+-------------------------------------------------------------+
|                                                              |
|  [HEADLINE] ACTIVE USERS SURGE PAST 2.1 MILLION              |
|  Subscriber growth accelerates 34% QoQ                      |
|                                                              |
|   +-------+  +-------+  +-------+                           |
|   | 2.1M  |  | 84.7K |  | $12.4M|                           |
|   | ACTIVE|  | DAILY |  | REV   |                           |
|   | USERS |  | SESSNS|  | MTD  |                           |
|   +-------+  +-------+  +-------+                           |
|                                                              |
|  [FEATURE] RETENTION TEARSHEET                               |
|   Day 1     Day 7    Day 30   Day 90                        |
|   [#######] [##### ] [###   ] [#     ]                      |
|   89%       63%      41%      18%                            |
|                                                              |
|  [INSIGHT] Top cohort source: direct traffic                 |
|  [TREND]   Mobile share now 67%, desktop 33%                |
|                                                              |
+-------------------------------------------------------------+
  Published by Metrics Inc.  |  Data refreshes every 60s
```
All printable ASCII, no unicode. Ready for terminal display anywhere.