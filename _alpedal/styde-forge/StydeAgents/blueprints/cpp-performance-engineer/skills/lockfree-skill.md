# Lock-Free Data Structures Skill
This skill defines lock-free concurrent data structure implementation procedures. Load with skill_view(name='lockfree-skill').

## When to Use
Lock-free structures are appropriate when contention on a mutex-protected structure exceeds 30% (measured via perf stat -e context-switches or mutex::try_lock failure rate). They shine in read-mostly workloads (one writer, many readers) and in real-time contexts where a blocked thread is unacceptable. Use std::atomic with the weakest valid memory ordering — consume for dependent loads (rarely supported; fall back to acquire), acquire for reads, release for writes, acq_rel for RMW, seq_cst only for memory barriers that must be total. Common patterns: Treiber stack, Michael-Scott queue, symmetric transfer queue (SPSC), left-right pattern for RCU-like reads.

## When NOT to Use
Do NOT implement lock-free for structures larger than a few words — CAS on a pointer is atomic; CAS on a 256B struct is not. Do NOT use lock-free when the critical section is long (file I/O, network, memory allocation) — the spinning consumer wastes CPU. Do NOT write lock-free code on platforms lacking 16-byte double-word CAS (mcx16cmp16 on x86, DWORD CAS on ARM) without padding to the next power of two. Do NOT use lock-free in code that runs on SPARC or Itanium without extensive testing — memory model quirks cause SI. Profiling against a simple mutex baseline is mandatory: a naive spinlock often beats a clever lock-free structure.

## Trade-offs
Lock-free structures eliminate priority inversion and convoying but introduce ABA problems (mitigated by tagged pointers, hazard pointers, or epoch-based reclamation). Memory reclamation is the hardest part: hazard pointers require per-thread retired lists and a scan threshold; epoch-based reclamation (RCU-ish) batches frees but delays reclamation until all readers pass the epoch. Lock-free code is significantly harder to review and test: thread sanitizer detects fewer races in lock-free code than in mutex code. Performance under low contention is often worse than a simple spinlock (more atomic RMW ops). Under high contention (16+ threads on 8 cores), lock-free can be 3-10x faster.

## Concrete Examples
Hazard pointer guard pattern:
```
struct HPGuard { std::atomic<void*>* hp; void* ptr; };
auto guarded_load(Node* p) {
  hp->store(p, std::memory_order_release);
  auto val = p->next.load(std::memory_order_acquire);
  // hazard pointer protects p from reclamation
  return val;
}
```

Michael-Scott queue enqueue:
```
Node* n = new Node(v);
Node* tail_old = tail.load();
while (!tail.compare_exchange_weak(tail_old->next, n));
tail.compare_exchange_strong(tail_old, n); // non-atomic store to tail is okay
```
