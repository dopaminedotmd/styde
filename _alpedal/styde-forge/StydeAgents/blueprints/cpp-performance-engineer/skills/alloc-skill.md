# Memory Allocator Strategies Skill
This skill defines custom memory allocator design procedures (arena, pool, slab). Load with skill_view(name='alloc-skill').

## When to Use
Custom allocators apply when malloc/free overhead dominates the execution profile (measured by perf stat -e page-faults, context-switches on heavy allocation workloads). Use a linear arena (bump pointer) for frame-update allocations: every particle, bullet, or UI element is freed simultaneously at frame end. Use a fixed-size pool for objects created and destroyed frequently (network connections, particle slots, event objects). Use a slab allocator (Boost.Pool, jemalloc, tcmalloc) when allocating mixed sizes up to ~512 bytes in a hot path. Custom allocators reduce per-allocation latency from ~100ns (malloc) to ~3-10ns (bump or pool) because no system calls, no lock contention, and no free-list coalescing overhead.

## When NOT to Use
Do NOT bypass malloc for large allocations (>64KB) — mmap in the kernel handles them better than a userspace slab. Do NOT use a linear arena if only a subset of objects need early freeing (leaks memory until arena reset). Do NOT use a pool for variable-size allocations — you must round up to the nearest slot size, wasting up to 50% memory. Do NOT implement a custom allocator as the first optimization — profile first: most applications are fine with malloc. Do NOT use custom allocators in shared libraries or plugin systems where deallocation happens in a different code unit (the allocator must be matched to the deallocator).

## Trade-offs
Custom allocators improve throughput but complicate debugging: AddressSanitizer cannot track arena allocations, Valgrind sees them as leaks, and memory profilers report incomplete stacks. Arena resets invalidate all pointers into the arena — any dangling reference causes use-after-free. Pool free-lists fragment internally (truly freed slots become external fragmentation). Slab allocators trade 5-15% memory overhead for 3-10x speed. Ownership semantics change: an arena-allocated object cannot be individually deleted, which conflicts with RAII patterns. Document all custom allocator lifetimes clearly in code.

## Concrete Examples
Linear arena:
```
class Arena {
  char* begin; char* cur; char* end;
public:
  template<typename T> T* alloc(size_t n = 1) {
    size_t bytes = sizeof(T) * n;
    bytes = (bytes + alignof(T) - 1) & ~(alignof(T) - 1);
    if (cur + bytes > end) return nullptr;
    T* ptr = reinterpret_cast<T*>(cur);
    cur += bytes;
    return ptr;
  }
  void reset() { cur = begin; }
};
```

Fixed-size pool:
```
template<typename T> class Pool {
  union Slot { T obj; Slot* next; };
  Slot* head = nullptr;
  std::vector<Slot*> blocks;
  static constexpr int BLOCK = 1024;
public:
  T* acquire() {
    if (!head) {
      blocks.push_back(new Slot[BLOCK]);
      for (int i = 0; i < BLOCK-1; ++i) blocks.back()[i].next = &blocks.back()[i+1];
      blocks.back()[BLOCK-1].next = nullptr;
      head = blocks.back();
    }
    T* p = &head->obj;
    head = head->next;
    return new (p) T();
  }
  void release(T* p) {
    p->~T();
    auto* s = reinterpret_cast<Slot*>(p);
    s->next = head; head = s;
  }
};
```
