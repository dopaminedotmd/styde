# Move Semantics and RAII Skill
This skill defines move semantics and RAII procedures for C++ performance optimization. Load with skill_view(name='move-skill').

## When to Use
Move semantics apply when transferring ownership of a resource (heap memory, file handle, socket) from one object to another. Use std::move on rvalue references and when returning a local variable from a function (but do NOT std::move the return — that inhibits NRVO). Mark move constructors and move assignment operators as noexcept to enable efficient reallocation in std::vector. Use RAII for every resource: memory (std::unique_ptr, std::vector), mutex locks (std::lock_guard), file handles (custom RAII wrapper), sockets. Implement the rule of five explicitly (=default or user-defined) for any class that owns a resource. Provide a noexcept swap member and ADL swap overload.

## When NOT to Use
Do NOT std::move const references — const T&& binds to const T& (the move constructor is deleted for const T). Do NOT implement move semantics for trivial types (int, double, pointer) — copy elision handles them. Do NOT return std::move(local) from a function — it prevents NRVO and forces a move constructor call. Do NOT use std::move on a function argument that is itself a forwarding reference (T&&) — use std::forward instead. Do NOT use std::move when the source object must remain in a valid (non-destructed) state — post-move objects must be destructible and assignable, but otherwise unspecified.

## Trade-offs
Move replaces copy for expensive heap-allocated resources but changes observable behavior: post-move state is valid but unspecified (typically empty for containers, null for smart pointers). Debugging moved-from objects is harder than debugging copied objects. noexcept move constructors enable vector growth without copy fallback — without noexcept, std::vector falls back to copying on reallocation (2-3x slower for large elements). RAII eliminates resource leaks at the cost of reverse-order destruction (destructors fire in reverse construction order), which may close dependent resources too early.

## Concrete Examples
Rule of five for a resource-owning type:
```
class Buffer {
  int* data; size_t size;
public:
  Buffer(size_t n) : data(new int[n]), size(n) {}
  ~Buffer() { delete[] data; }
  Buffer(Buffer&& other) noexcept : data(std::exchange(other.data, nullptr)), size(other.size) {}
  Buffer& operator=(Buffer&& other) noexcept {
    if (this != &other) { delete[] data; data = std::exchange(other.data, nullptr); size = other.size; }
    return *this;
  }
  Buffer(const Buffer&) = delete;
  Buffer& operator=(const Buffer&) = delete;
  friend void swap(Buffer& a, Buffer& b) noexcept { std::swap(a.data, b.data); std::swap(a.size, b.size); }
};
```

noexcept on move enables vector growth:
```
std::vector<Buffer> v;
v.push_back(Buffer(1024)); // noexcept move: fast pointer-swap reallocation
```
