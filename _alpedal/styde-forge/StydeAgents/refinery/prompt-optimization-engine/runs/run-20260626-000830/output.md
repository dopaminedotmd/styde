PROMPT OPTIMIZATION ENGINE ACTIVE.
Blueprint: Prompt Optimization Engine (ai-opt v1)
Domain: AI optimization
Vector: 3 optimization channels identified
OPTIMIZATION FRAME
Channel 1: DSPy Signature
- Map input/output structure as DSPy module
- Signature: prompt_messy -> optimized_prompt
- Teleprompter: BootstrapFewShotWithRandomSearch
- Iterations: 5-20 rounds, select best via validation score
Channel 2: Compression
- Remove redundant instruction tokens (~40% shrinkage typical)
- Convert multi-sentence instructions to imperative single-line commands
- Strip politeness markers, hedging, meta-commentary
- Target: under 50% original length while retaining precision
Channel 3: CoT Structure
- Add reasoning scaffold: define -> decompose -> verify
- Wrap critical reasoning steps with  markers
- Append final-answer delimiter for clean output extraction
BENCHMARK PROTOCOL
Metric suite:
A) Accuracy hit rate on held-out test set
B) Token efficiency (prompt + response tokens per correct output)
C) Output format compliance (exact match rate)
D) Inference cost (estimated $ per 1000 runs)
Run 5 variants, select winner by composite score.
DELIVERABLE
1. Optimized prompt template (compressed + structured)
2. Few-shot example bank (3 positive, 1 negative edge case)
3. DSPy config block (signature + teleprompter params)
4. Benchmark script targeting the 4 metrics above
Ready to execute on any target prompt. Feed raw prompt, receive optimized variant with benchmark.