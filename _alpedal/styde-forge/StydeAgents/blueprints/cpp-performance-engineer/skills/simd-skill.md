# SIMD Intrinsics Skill
This skill defines SIMD vectorization procedures using AVX2/AVX-512 (x86) and NEON (ARM). Load with skill_view(name='simd-skill').

## When to Use
SIMD is appropriate for tight loops processing contiguous arrays of primitive types (float, double, int32, int64, uint8) where each iteration performs the same operation independently. Ideal candidates: matrix multiplication, convolution, FFT butterfly stages, color space conversion, audio sample processing, and bulk arithmetic (add, mul, fused multiply-add). Use when loop trip count >= 64 elements and the operation is compute-bound (not memory-bound). Strongly prefer aligned memory (posix_memalign, _mm_malloc, alignas(64)) to use aligned load/store intrinsics (2x faster on some microarchitectures).

## When NOT to Use
Do NOT use SIMD on: (a) inherently serial algorithms where each iteration depends on the previous iteration's output (recurrence, prefix sum), (b) latency-sensitive code paths that execute once (setup, teardown) — the cost of loading vectors exceeds any benefit, (c) code that runs on heterogeneous hardware without a scalar fallback — AVX512 on Ryzen is emulated in microcode and slower than scalar, (d) branches inside the hot loop — unless masked operations (AVX512 mask registers) handle divergence cleanly, lane divergence kills throughput.

## Trade-offs
SIMD code is significantly harder to maintain than scalar code. It couples tightly to a specific ISA extension (AVX2 vs AVX-512 vs NEON vs SVE). Cross-platform portability requires three-way dispatch (AVX2/NEON/scalar) with runtime cpuid checks. Register pressure at 8 or 16 registers can spill to stack, negating gains. Remainder loops (tail elements not fitting a full vector) add complexity. Prefer compiler auto-vectorization hints (#pragma GCC ivdep, #pragma clang loop vectorize(enable)) before writing intrinsics manually — auto-vectorization covers 80% of cases.

## Concrete Examples
AVX2 float 4-wide add:
```
__m256 a = _mm256_load_ps(pa + i);
__m256 b = _mm256_load_ps(pb + i);
_mm256_store_ps(pc + i, _mm256_add_ps(a, b));
```

NEON float 4-wide add (same throughput, different intrinsic names):
```
float32x4_t a = vld1q_f32(pa + i);
float32x4_t b = vld1q_f32(pb + i);
vst1q_f32(pc + i, vaddq_f32(a, b));
```

Always tail-handle the remainder loop with scalar. Use if (N >= 8) for AVX2 float, then handle 0-7 elements with plain loops.
