# Compressed Pairs and EBCO Skill ([[no_unique_address]], compressed_pair)
This skill defines empty base class optimization and compressed pair procedures, replacing generic 'compress' operations. Load with skill_view(name='compact-skill').

## When to Use
Use [[no_unique_address]] (C++20) or EBCO via inheritance (pre-C++20) when a class contains a stateless member type — an empty deleter, an empty allocator (e.g., std::allocator<T>), or an empty hasher (e.g., std::hash<int>). Without this optimization, each stateless member occupies at least 1 byte (plus padding), inflating the object's size and cache footprint. Apply to container adaptors that store an allocator or comparator as a member — the state is small (the pointer to the container's buffer) but the policy type carries zero runtime state. The reduction is typically 15-30% of the object's sizeof, which matters in containers stored in arrays or vectors.

## When NOT to Use
Do NOT use [[no_unique_address]] on members that share address with other members — the attribute is a hint, and the compiler may still use overlapping layout only when both members are empty types of different types. Do NOT use EBCO inheritance for non-empty base classes — the optimization only works for empty types. Do NOT apply when you need a stable address for the member (e.g., passing the allocator by pointer to external code) — a zero-size layout means two distinct members may share an address. Do NOT use compressed_pair (Boost) when [[no_unique_address]] is available — the attribute is cleaner and produces equivalent codegen. Do NOT expect improvement for types with fewer than 2 empty policy members — the overhead is 1-3 bytes, negligible in isolation.

## Trade-offs
[[no_unique_address]] is a C++20 feature — projects targeting C++14/17 must use EBCO via inheritance or Boost compressed_pair. EBCO via inheritance changes access control (private inheritance for policy) and prevents certain class layouts (cannot inherit from two base classes of the same type). Boost compressed_pair is not exception-safe for empty types that throw — rare, but possible. Compressed layouts complicate debugging: debuggers show members at unusual offsets or overlapping addresses. The performance improvement is indirect: reduced memory footprint improves L1/L2 cache efficiency for container-heavy code. The cost is zero at runtime — the optimization is purely a layout transformation.

## Concrete Examples
[[no_unique_address]] (C++20):
```
template<typename T, typename Hash = std::hash<T>> class MySet {
  T* data;
  [[no_unique_address]] Hash hasher; // 0 bytes padding
  // sizeof(MySet<int>) = 8, without [[no_unique_address]] = 16
};
```

EBCO via inheritance (pre-C++20):
```
template<typename T, typename Hash> class MySet : private Hash {
  T* data;
  // Hash base occupies 0 bytes (empty class)
};
```

custom compressed_pair:
```
template<typename T1, typename T2> struct compressed_pair;
template<typename T1, typename T2> requires std::is_empty_v<T1> && !std::is_final_v<T1>
struct compressed_pair<T1, T2> : private T1 { T2 second; };
// first member via inherited base (0 bytes), second as regular member
```
