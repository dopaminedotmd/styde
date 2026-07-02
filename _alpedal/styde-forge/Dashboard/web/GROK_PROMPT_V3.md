You are designing the next-generation Mission Control dashboard for StydeForge — a personal AI agent refinery and training pipeline. This is a creative exploration brief. Go wild but stay grounded in the product's purpose.

═══════════════════════════════════════════
CONTEXT: WHAT IS STYDEFORGE?
═══════════════════════════════════════════

StydeForge ("The Crucible") is a portable, local AI agent refinery. It takes raw agent blueprints (LLM personas) and runs them through a continuous evolutionary loop: SPAWN → EVALUATE → IMPROVE → CHECKPOINT → PRODUCTION. Think of it as a forge/smelter for autonomous AI agents. Agents are heated, hammered, tested, and refined until they reach world-class quality (≥85/100 on a multi-judge eval), then promoted to production.

Key domain concepts:
- Agents move through zones: REFINERY (active training) → PRODUCTION (shipped, world-class) → ARCHIVE (retired)
- Dual-model architecture: a fast model spawns agents, a powerful model evaluates and teaches them
- 6-layer evaluation pipeline with Bayesian scoring
- Caveman Ultra mode: hyper-efficient prompts, 70% fewer tokens
- It runs locally on Pontus' dual-GPU rig (RTX 3080 + RTX 3070 Ti)
- The entire loop is autonomous — zero manual steps once started

The dashboard IS the control room for this factory. It should feel like a fusion of:
- An Apple design studio (frosted glass, spatial depth, SF typography, breathing whitespace)
- An industrial control room (live metrics, pipeline monitoring, thermal signatures)
- A sci-fi forge/smelter interface (glowing elements, ambient heat signatures, analog gauges)

═══════════════════════════════════════════
CURRENT STATE (V2)
═══════════════════════════════════════════

We have a working dashboard at localhost:8765 with:
- Dark OLED base (#040408) with ambient radial gradients (amber, indigo, violet)
- Frosted glass panels with backdrop-blur: 24px
- Geist typography (SF Pro substitute for Windows)
- Pipeline visualization: Refinery / Production / Archive zones with animated bars
- Agent cards with "thermal signatures" — glow dots colored by score (hot gold 85+ → cool violet <30)
- Mini SVG sparklines for score history
- Live GPU monitoring (nvidia-smi)
- Evaluation log with pass/fail badges
- Smart diffing — only re-renders when structure changes, text values update smoothly
- Keyboard shortcuts: / to search, Ctrl+R to refresh, Esc to un-maximize panels
- Panel maximize/restore

WHAT'S MISSING / COULD BE ELEVATED:
- The layout is still a basic CSS grid (5 panels: Pipeline | Agents | Blueprints | Hardware | Evals)
- No real-time streaming — polls every 3 seconds via HTTP
- No "living" feel — the dashboard is static between updates
- No audio/sound design
- No 3D or perspective depth
- Limited interactivity beyond click-to-expand and filter
- No dark pattern or "crucible" atmosphere — it reads more "tech dashboard" than "forge control room"

═══════════════════════════════════════════
THE BRIEF
═══════════════════════════════════════════

Design a Mission Control interface that feels ALIVE. This is not just monitoring — it's commanding a living forge. The interface should have:

1. ATMOSPHERE & MATERIALITY
- The forge metaphor: heat, amber glow, cooling metal, sparks
- Consider audio-reactive or time-reactive ambient effects
- The background should NOT be static black — make it breathe
- Think about temperature as a design material: hot zones glow, cold zones recede
- Possibly: subtle particle effects, heat haze, chromatic aberration on edges
- Frosted glass everywhere — but different "temperatures" of glass

2. SPATIAL DEPTH
- Move beyond flat rectangles. Use Z-depth, parallax, perspective
- Consider a 3D isometric or perspective view of the pipeline
- Layers that cast soft shadows on layers below
- Elements that float at different depths
- A "forge core" visual element — the beating heart of the system

3. LIVING DATA
- Scores should animate like physical gauges, not just numbers
- The pipeline should show agents flowing THROUGH zones, not just counts
- Consider a timeline or process-flow visualization
- GPU data should pulse with actual load
- Network-like particle animations showing agent communication

4. INTERACTION MODEL
- Command palette (Cmd+K style) for quick actions: spawn agent, evaluate, checkpoint
- Gesture-based interactions: pinch to zoom pipeline, swipe between views
- Hover reveals in glass — information that appears to be "inside" the glass
- Magnetic cursor effects on interactive elements
- Haptic press feedback (scale: 0.97 on click)

5. SOUND DESIGN (optional but differentiating)
- Subtle ambient hum that changes pitch with system load
- Forge "clang" on agent promotion to production
- Thermal crackle on high GPU temps
- All sounds optional, off by default, with a mute toggle

6. TECHNICAL ASPIRATIONS
- WebSockets or SSE for true real-time streaming (no polling)
- Canvas/WebGL for the ambient background and particle effects
- GSAP for orchestrated motion sequences
- Three.js for any 3D elements (optional)
- All in a single HTML file (or minimal files) served by a lightweight Python backend
- Must work on Windows 10, Chrome/Edge, 1920x1080 and 2560x1440
- Dual GPU: RTX 3080 (10GB) + RTX 3070 Ti (8GB)

═══════════════════════════════════════════
REFERENCE AESTHETICS
═══════════════════════════════════════════
- Apple Vision Pro / visionOS glass materials
- Linear.app's precision and minimalism
- Cyberpunk 2077 UI (functional, glowing, diegetic)
- Iron Man's HUD / Jarvis interface
- High-end audio equipment (VU meters, analog warmth)
- Industrial forge/foundry control rooms
- NASA Mission Control (dense but readable)

═══════════════════════════════════════════
CONSTRAINTS
═══════════════════════════════════════════
- Single HTML file + Python backend (HTTP server serving JSON API)
- No React/Vue framework — vanilla JS for zero build step
- No npm install required — CDN-only dependencies (GSAP, Three.js CDN ok)
- Must render at 60fps on the RTX 3080
- Dark mode only
- Font: Geist (from Google Fonts CDN) as SF Pro substitute
- Backend: Python stdlib only (http.server), reads YAML state file + runs nvidia-smi

═══════════════════════════════════════════
YOUR TASK
═══════════════════════════════════════════

Generate a detailed design concept for the v3 Mission Control. Include:
1. A visual description — what does it look like? Paint a picture in words.
2. A layout architecture — what zones/panels exist and how do they relate spatially?
3. 3-5 signature interaction moments — what makes someone say "wow"?
4. A motion design language — how does it move, breathe, respond?
5. A color & material palette
6. A technical architecture sketch — how would you structure this in vanilla JS/CSS?
7. (Optional) ASCII wireframe of the layout

Don't write code. This is a creative concept document. Be specific, be bold, be unexpected. This dashboard should look like nothing else on the web.
