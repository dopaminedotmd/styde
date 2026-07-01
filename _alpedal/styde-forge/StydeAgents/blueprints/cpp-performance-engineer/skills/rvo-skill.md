# Return Value Optimization Skill (RVO, NRVO)
This skill defines copy elision and return value optimization procedures. Load with skill_view(name='rvo-skill').

## When to Use
RVO (Return Value Optimization) is mandatory since C++17 for prvalues (T(), std::string("foo")). NRVO (Named Return Value Optimization) is a compiler optimization for named local variables returned from a function. RVO eliminates the temporary entirely — the object is constructed directly in the caller's storage. Use RVO for factory functions and expression-style returns: return std::string("hello") is zero-copy since C++17. NRVO applies when a single named local variable is returned: std::string make() { std::string s; s += "hello"; return s; } — s is constructed directly in the caller's frame (zero-copy). Enable RVO/NRVO for types with expensive copies (std::string, std::vector, std::map, custom matrix types). The speedup is 2-5x for types with dynamic allocations, zero for small trivial types.

## When NOT to Use
Do NOT use std::move(local) in a return statement — this forces a move constructor call and prevents NRVO (the local is not eligible for elision if it is treated as an xvalue). Do NOT expect NRVO when returning different named objects from different branches: if (flag) return a; else return b; — NRVO cannot pick one. Do NOT expect RVO when returning through pointers or reference parameters — that is guaranteed copy elision only for prvalues. Do NOT rely on NRVO for pre-C++11 compilers or MSVC with /Od — the behavior is not portable. RVO/NRVO do NOT apply to returned function parameters: T f(T arg) { return arg; } — arg is an lvalue, this is a copy (or move if std::move'd).

## Trade-offs
NRVO is a "maybe" optimization — GCC performs it reliably at -O1, Clang at -O2, MSVC on most paths but not all. The only guaranteed zero-copy mechanism in standard C++ is RVO for prvalues (C++17). Relying on NRVO makes performance non-portable — write the canonical form (single named variable, return at end) and measure production builds. For hard guarantees, use out-parameters (T& out) or unique_ptr return (heap allocation, pointer copy). C++17 guaranteed copy elision makes RVO a semantic guarantee, not an optimization, which means you can return a move-only type (std::unique_ptr) from a factory without std::move. The As-If rule allows the compiler to apply NRVO even when the standard doesn't require it — but only measure, don't assume.

## Concrete Examples
NRVO enabled (single named return):
```
std::vector<int> make_big() {
  std::vector<int> v;
  v.reserve(100000);
  for (int i = 0; i < 100000; ++i) v.push_back(i);
  return v; // NRVO: v constructed directly in caller's storage
}
```

NRVO inhibited (std::move):
```
std::vector<int> make_bad() {
  std::vector<int> v;
  v.reserve(100000);
  return std::move(v); // inhibits NRVO, forces move ctor
}
```

C++17 guaranteed RVO (prvalue):
```
std::vector<int> make_good() {
  return std::vector<int>(100000); // mandatory RVO since C++17
}
```

Inspect assembly to verify: look for absence of std::vector<int>::vector(std::vector<int>&&) call in the return path.
