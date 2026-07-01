# Profiling and Benchmarking Skill
This skill defines profiling and benchmarking procedures for C++ performance work. Load with skill_view(name='profile-skill').

## When to Use
Profile before any optimization. Without baseline measurements, optimization is guesswork. Use perf stat for hardware counter collection on Linux, VTune for hotspot/call-tree analysis on x86, Xcode Instruments on macOS, and Windows Performance Toolkit (WPT) on Windows. Microbenchmark any extracted hot loop with Google Benchmark or Catch2 Bench — pipe the results through statistical analysis (mean, median, MAD, CV). Profile at no less than 10^7 iterations or 1 second wall-clock minimum to stabilize counters. Use perf top or perf record -g for sampling-based hot-spot identification — this is the single most important profiling technique.

## When NOT to Use
Do NOT microbenchmark without disabling CPU frequency scaling (cpupower frequency-set -g performance). Do NOT profile debug builds — release builds with -O2 -march=native are the only valid targets. Do NOT use std::chrono for sub-microsecond measurement — use hardware cycle counters (__rdtsc on x86) or Google Benchmark's cycle clock. Do NOT draw conclusions from a single run — run 100+ iterations, discard warmup (first 3 runs), compute coefficient of variation. CV > 10% means the benchmark setup is flawed (page faults, context switches, thermal throttling).

## Trade-offs
perf stat requires root (or perf_event_paranoid <= 1). Sampling profilers introduce skid (sample point is a few instructions after the actual hotspot). Intel PT (Processor Trace) captures exact control flow but generates gigabytes of trace per second. RDTSC readings on modern CPUs show different values per core (TSC drift) — pin the thread to a single core with sched_setaffinity. Google Benchmark adds ~50 cycles of overhead per DoNotOptimize barrier — negligible for functions > 100 cycles, significant for tiny helpers.

## Concrete Examples
perf stat for cache analysis:
```
perf stat -e cycles,instructions,cache-references,cache-misses,branch-misses ./bench --benchmark_filter=simd
```

Google Benchmark harness:
```
static void BM_AddScalar(benchmark::State& state) {
  float a[1024], b[1024], c[1024];
  for (auto _ : state) {
    for (int i = 0; i < 1024; ++i) c[i] = a[i] + b[i];
    benchmark::DoNotOptimize(c);
  }
}
BENCHMARK(BM_AddScalar)->Iterations(10000);
```

Metrics table output:
```
Benchmark              Time      CPU     Iterations
BM_AddScalar/scalar  12.3 ns  12.3 ns  10000
BM_AddSIMD/simd       3.1 ns   3.1 ns  10000   (3.97x)
```
