# Template Metaprogramming Skill (CRTP, SFINAE, constexpr Dispatch)
This skill defines compile-time template metaprogramming procedures. Load with skill_view(name='tmp-skill').

## When to Use
CRTP (Curiously Recurring Template Pattern) provides static polymorphism — function calls resolved at compile time with zero vtable overhead. Use CRTP when you have multiple types sharing an interface and every call site knows the concrete type at compile time. SFINAE (Substitution Failure Is Not An Error) enables overloads that conditionally exist based on type traits — use it for generic utility libraries, serialization, and type-based dispatch before C++20 concepts. constexpr dispatch replaces runtime branches with compile-time resolution — use when the dispatch condition is known at compile time (template parameter, integral constant, static_assert condition). All three eliminate indirect branch penalties and enable full inlining.

## When NOT to Use
Do NOT use CRTP when runtime polymorphism is required (plugins, dynamically loaded modules, heterogeneous containers) — virtual dispatch is the correct tool. Do NOT use SFINAE when C++20 concepts are available — concepts produce clearer error messages, shorter code, and better IDE support. Do NOT chain SFINAE with enable_if on more than 3 overloads — tag dispatch (integral_constant of priority levels) is simpler. Do NOT use constexpr dispatch when the condition varies per call site at runtime — the code bloat from template instantiation exceeds any benefit. Do NOT use CRTP for interfaces with more than 10 methods — debug symbol size and compile time grow linearly with each derived type.

## Trade-offs
CRTP eliminates vtable but increases binary size via template instantiation — each derived type gets its own copy of every member function. SFINAE imposes significant compile-time cost (template argument deduction tries every candidate) and creates error messages that look like compiler internals. constexpr dispatch with if constexpr (C++17) is strictly better than enable_if for most cases — prefer it. Template metaprogramming reduces runtime to zero dispatch overhead but increases compile time 2-10x for heavy CRTP hierarchies. Header-only requirement (templates must be defined in headers) increases include dependencies. Debugging template code is harder due to inlining erasing stack frames.

## Concrete Examples
CRTP for arithmetic types:
```
template<typename D> struct VectorBase {
  D operator+(const D& rhs) const {
    D result = static_cast<const D&>(*this);
    for (int i = 0; i < 3; ++i) result.elems[i] += rhs.elems[i];
    return result;
  }
};
struct Vec3 : VectorBase<Vec3> { float elems[3]; };
```

if constexpr dispatch (C++17, replaces SFINAE):
```
template<typename T> auto process(T val) {
  if constexpr (std::is_arithmetic_v<T>) return val * 2;
  else if constexpr (std::is_same_v<T, std::string>) return val + val;
  else return val;
}
```
