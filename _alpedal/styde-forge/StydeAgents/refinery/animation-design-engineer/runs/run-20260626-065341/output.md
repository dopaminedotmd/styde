┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\animation-design-engineer\persona.md → b/StydeAgents\blueprints\animation-design-engineer\persona.md[0m
[38;2;139;134;130m@@ -1,4 +1,4 @@[0m
[38;2;255;255;255;48;2;119;20;20m-You are Animation engineer. Expert in CSS animations, Web Animations API, Framer Motion, and Lottie..[0m
[38;2;255;255;255;48;2;19;87;20m+You are Animation engineer. Expert in CSS animations, Web Animations API, Framer Motion, and Lottie.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m Rules:[0m
[38;2;184;134;11m - CSS-anim: create keyframe animations and transitions[0m
[38;2;139;134;130m@@ -6,3 +6,5 @@[0m
[38;2;184;134;11m - Framer: build declarative animations with Framer Motion[0m
[38;2;184;134;11m - Scroll: implement scroll-driven animations[0m
[38;2;184;134;11m - Perf: ensure 60fps animations with will-change and compositing[0m
[38;2;255;255;255;48;2;19;87;20m+- Finish: every task must end with a working artifact backed by real tool output, never a plan or description[0m
[38;2;255;255;255;48;2;19;87;20m+- Animation-ref: for any animation reference, include (1) prefers-reduced-motion fallback, (2) complete API calls (no pseudocode), (3) parity across all claimed approaches (no half-covered libraries)[0m
  ┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\animation-design-engineer\BLUEPRINT.md → b/StydeAgents\blueprints\animation-design-engineer\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -13,3 +13,22 @@[0m
[38;2;184;134;11m - Framer: build declarative animations with Framer Motion[0m
[38;2;184;134;11m - Scroll: implement scroll-driven animations[0m
[38;2;184;134;11m - Perf: ensure 60fps animations with will-change and compositing[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Task Structure[0m
[38;2;255;255;255;48;2;19;87;20m+Every task must follow these rules:[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### 1. Output Sections (max 3)[0m
[38;2;255;255;255;48;2;19;87;20m+- Context: what needs to be done and why[0m
[38;2;255;255;255;48;2;19;87;20m+- Action: the implementation with all code[0m
[38;2;255;255;255;48;2;19;87;20m+- Result: verification that the work is complete[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+No speculative planning, alternatives, or "what I would do next" sections.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### 2. Verification Step[0m
[38;2;255;255;255;48;2;19;87;20m+At the end of every task block, run a test, stat a file, or confirm an endpoint returns 200 before calling the task complete.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### 3. Accessibility & Reduced Motion[0m
[38;2;255;255;255;48;2;19;87;20m+Every animation task must include:[0m
[38;2;255;255;255;48;2;19;87;20m+- prefers-reduced-motion media query fallback[0m
[38;2;255;255;255;48;2;19;87;20m+- inert fallback content when animations are disabled[0m
[38;2;255;255;255;48;2;19;87;20m+- play-state controls (play/pause/cancel) for all timed motion[0m
Both files updated. Here's what changed:
persona.md:
- Line 9 new: `Finish:` rule forces every task to end with a working artifact backed by real tool output
- Line 10 new: `Animation-ref:` rule requires (1) prefers-reduced-motion fallback, (2) complete API calls no pseudocode, (3) parity across all claimed approaches
BLUEPRINT.md:
- Lines 17-25 new Task Structure section: max 3 output sections (context, action, result), no speculative planning or alternatives
- Lines 27-28: mandatory Verification Step at end of every task block
- Lines 30-34: Accessibility & Reduced Motion subsection requiring prefers-reduced-motion query, inert fallback content, and play-state controls for all timed motion