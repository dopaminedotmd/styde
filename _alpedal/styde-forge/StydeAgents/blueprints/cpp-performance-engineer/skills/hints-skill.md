# Branch Hints Skill (__builtin_expect, likely/unlikely)
This skill defines branch hinting procedures for CPU branch predictor guidance. Load with skill_view(name='hints-skill').

## When to Use
Use __builtin_expect (GCC/Clang) or [[likely]]/[[unlikely]] attributes (C++20) on branches where one path is taken more than 95% of the time. The canonical case is error checking: if (error) [[unlikely]] { handle(); } — the compiler reorders the basic block so the hot fall-through path is contiguous and the cold error path is out of line (lower I-cache pollution). Also use on boundary checks in tight loops: if (i >= limit) [[unlikely]] break; and on feature-gate checks where a flag is set once per program start. The net effect is 1-3% IPC improvement on long-running loops with infrequent taken branches.

## When NOT to Use
Do NOT use branch hints on balanced branches (50/50 split) — the compiler may pessimize the unpredictable path. Do NOT use hints on every if in the program — marking more than 5-10% of branches dilutes the signal. Do NOT use hints without measuring the effect — at 10^6 iterations the improvement may be noise; only at 10^8+ does it become statistically significant. Do NOT use on forward-edge branches that already have static prediction (backward = taken, forward = not taken) — the predictor already handles that. Do NOT use [[unlikely]] on the first iteration of a loop — the loop header has its own prediction logic.

## Trade-offs
Branch hints only affect code layout and the static predictor (which the dynamic predictor overrides after ~10^4 dynamic executions). The primary benefit is I-cache packing: the cold path is placed out of line, reducing I-cache footprint of the hot path. On modern CPUs (Skylake+, Zen+) with tournament predictors and 10K+ entry BTB, the benefit is marginal for frequently executed branches — the predictor learns the distribution regardless. Hardware platforms differ: ARM Cortex-A does not support static hints; x86 respects them weakly. The actual performance impact rarely exceeds 3% and requires careful microbenchmarking to detect.

## Concrete Examples
Error checking in a hot loop:
```
for (size_t i = 0; i < count; ++i) {
  auto val = process(input[i]);
  if (__builtin_expect(has_error(val), 0)) [[unlikely]] {
    stats.errors++;
    log_error(val);
    continue;
  }
  accumulate(val);
}
// Compiler: error handler blocks placed after the loop, not interleaved
```

Feature gate:
```
thread_local bool cache_enabled = false;
void init_cache() { cache_enabled = true; }
if (cache_enabled) [[likely]] { return cached_lookup(key); }
else { return compute_lookup(key); }
```
