# Cache Locality Optimization Skill
This skill defines cache optimization procedures for CPU data access patterns. Load with skill_view(name='cache-skill').

## When to Use
Cache optimization applies when profiling shows high L1/L2 cache-miss ratios (perf stat shows >10% L1 misses, >5% L2 misses). Hot loops iterating over struct arrays where only a subset of fields are accessed per iteration are the primary target. SoA (Struct of Arrays) layout cuts cache-line waste from 90%+ down to near-100% utilization. Also use explicit prefetching (__builtin_prefetch) for linked-list or tree traversals where the next node's address is known 50-100 cycles ahead. False sharing mitigation (alignas(64) on fields accessed by different threads) applies to any concurrent data structure with adjacent memory locations written by different cores.

## When NOT to Use
Do NOT apply cache transformations on small datasets that fit entirely in L1 cache (32KB). Do NOT convert to SoA when ALL fields of a struct are accessed on every iteration — AoS gives better spatial locality. Do NOT add software prefetching on random-access patterns (hash tables, scatter-gather) — hardware prefetcher handles stride-1 patterns better than manual prefetch. Do NOT pad to cache line size if it doubles memory footprint and the working set exceeds LLC capacity — the capacity miss penalty exceeds the false-sharing penalty.

## Trade-offs
SoA improves hot-loop throughput by 2-5x but complicates code: what was struct.velocity.x becomes velocity[i]. Code generation with SoA requires more registers (one base pointer per array). Sometimes AoS is better than SoA for APIs expecting contiguous structs, and the conversion cost (SoA <-> AoS) must be amortized. Prefetching added to a loop that already runs at memory bandwidth limit adds 0 benefit and burns decode bandwidth. Cache-line padding increases sizeof per object, potentially increasing TLB pressure and LLC misses.

## Concrete Examples
Scatter-gather SoA:
```
struct SoA { alignas(64) float x[1024]; float y[1024]; float mass[1024]; };
// vs AoS: struct { float x, y, mass; }[1024]; cache waste = 88 bytes unused per 64-byte line
```

Software prefetch in tree traversal:
```
while (node) {
  __builtin_prefetch(node->left, 0, 3);   // read, high temporal
  __builtin_prefetch(node->right, 0, 3);
  process(node);
  node = (condition) ? node->left : node->right;
}
```

False sharing mitigation:
```
struct alignas(64) Counter { std::atomic<int> val; };
Counter counters[NUM_THREADS];
// each counter on its own cache line: no false sharing
```
