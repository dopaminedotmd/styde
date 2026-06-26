State Management Architect ready.
No specific task was given beyond demonstrating the role. Here is my assessment of what a State Management Architect delivers:
Zustand stores for client state. Selectors prevent re-renders. persist middleware for hydration. subscribeWithSelector for fine-grained subscriptions. Immer middleware for nested immutable updates (dev.middleware).
TanStack Query for server cache. queryKey convention: [domain, id, filters]. staleTime > 0 prevents refetch spam. optimistic updates via onMutate with rollback in onError. infinite scrolling via useInfiniteQuery + cursor pagination.
Jotai atoms for shared primitive state. atomWithStorage for localStorage binding. splitAtom for dynamic lists. Derived atoms compute from raw atoms without manual memo. loadable pattern for async atoms.
Choice rule: server data goes in Query. UI state (modals, toggles) goes in Zustand. Derived/atomic values go in Jotai. Avoid mixing domains in one store — split by concern.
Available to design or implement specific state architecture on request. Give me a file path or a component name and I will produce the corresponding store, query hooks, or atom factories.