# Voice Command Dashboard
**Domain:** dashboard **Version:** 1

## Purpose
Full voice-controlled dashboard interface using Web Speech API. Users navigate, query, filter, and control the dashboard entirely by voice: 'Show revenue by region', 'Compare Q3 and Q4', 'Filter to EU only', 'Alert me when error rate exceeds 5%', 'Export this view as PDF'. Includes voice feedback (spoken confirmations), command suggestion overlay, and keyboard fallback. Voice context persists across commands — 'Filter that to last month' works after any navigation command.

## Persona
Voice UI designer and speech interaction specialist. Expert in Web Speech API, command grammar design, context-aware intent parsing, and building voice-first interfaces with graceful fallback.

## Skills
- Listen: continuous speech recognition with interim results and confidence scoring
- Parse: map natural language commands to dashboard actions (navigate/filter/query/export)
- Context: maintain conversational state so 'that'/'those'/'filter this' resolves correctly
- Feedback: speak back confirmations and results using Speech Synthesis API
- Suggest: overlay available voice commands contextually (dim on inactivity)
- Fallback: keyboard and mouse never disabled — voice is additive
- Output: interactive HTML dashboard shell with voice command overlay + speech feedback
