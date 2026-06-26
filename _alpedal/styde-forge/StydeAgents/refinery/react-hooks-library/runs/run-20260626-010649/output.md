import { useState, useEffect, useRef, useCallback, useMemo } from 'react'
// ──────────────────────────────────────────────
// useDebounce
// ──────────────────────────────────────────────
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay)
    return () => clearTimeout(timer)
  }, [value, delay])
  return debouncedValue
}
export function useDebouncedCallback<T extends (...args: unknown[]) => unknown>(
  callback: T,
  delay: number,
  deps: unknown[] = []
): (...args: Parameters<T>) => void {
  const callbackRef = useRef(callback)
  callbackRef.current = callback
  return useCallback(
    (...args: Parameters<T>) => {
      const timer = setTimeout(() => callbackRef.current(...args), delay)
      return () => clearTimeout(timer)
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [delay, ...deps]
  )
}
// ──────────────────────────────────────────────
// useLocalStorage
// ──────────────────────────────────────────────
export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((prev: T) => T)) => void, () => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item !== null ? (JSON.parse(item) as T) : initialValue
    } catch {
      return initialValue
    }
  })
  const setValue = useCallback(
    (value: T | ((prev: T) => T)) => {
      setStoredValue((prev) => {
        const nextValue = value instanceof Function ? value(prev) : value
        try {
          window.localStorage.setItem(key, JSON.stringify(nextValue))
        } catch (e) {
          console.warn(`useLocalStorage: unable to write key "${key}"`, e)
        }
        return nextValue
      })
    },
    [key]
  )
  const removeValue = useCallback(() => {
    try {
      window.localStorage.removeItem(key)
      setStoredValue(initialValue)
    } catch (e) {
      console.warn(`useLocalStorage: unable to remove key "${key}"`, e)
    }
  }, [key, initialValue])
  return [storedValue, setValue, removeValue]
}
// ──────────────────────────────────────────────
// useMediaQuery
// ──────────────────────────────────────────────
export function useMediaQuery(query: string): boolean {
  const getMatches = useCallback(() => {
    if (typeof window === 'undefined') return false
    return window.matchMedia(query).matches
  }, [query])
  const [matches, setMatches] = useState<boolean>(getMatches)
  useEffect(() => {
    const mql = window.matchMedia(query)
    const handler = (e: MediaQueryListEvent) => setMatches(e.matches)
    mql.addEventListener('change', handler)
    return () => mql.removeEventListener('change', handler)
  }, [query])
  return matches
}
export function usePrefersReducedMotion(): boolean {
  return useMediaQuery('(prefers-reduced-motion: reduce)')
}
export function usePrefersDarkMode(): boolean {
  return useMediaQuery('(prefers-color-scheme: dark)')
}
// ──────────────────────────────────────────────
// useIntersectionObserver
// ──────────────────────────────────────────────
interface UseIntersectionObserverOptions extends IntersectionObserverInit {
  enabled?: boolean
}
export function useIntersectionObserver<T extends HTMLElement = HTMLElement>(
  options: UseIntersectionObserverOptions = {}
): [React.RefObject<T | null>, IntersectionObserverEntry | null] {
  const { enabled = true, threshold = 0, root = null, rootMargin = '0px' } = options
  const ref = useRef<T | null>(null)
  const [entry, setEntry] = useState<IntersectionObserverEntry | null>(null)
  useEffect(() => {
    if (!enabled || !ref.current) return
    const observer = new IntersectionObserver(
      ([observedEntry]) => {
        if (observedEntry) setEntry(observedEntry)
      },
      { threshold, root, rootMargin }
    )
    observer.observe(ref.current)
    return () => {
      observer.disconnect()
    }
  }, [enabled, threshold, root, rootMargin])
  return [ref, entry]
}
export function useIsVisible<T extends HTMLElement = HTMLElement>(
  options?: UseIntersectionObserverOptions
): [React.RefObject<T | null>, boolean] {
  const [ref, entry] = useIntersectionObserver<T>(options)
  const isVisible = useMemo(() => entry?.isIntersecting ?? false, [entry])
  return [ref, isVisible]
}
// ──────────────────────────────────────────────
// usePrevious
// ──────────────────────────────────────────────
export function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T | undefined>(undefined)
  useEffect(() => {
    ref.current = value
  })
  return ref.current
}
export function usePreviousWithInitial<T>(value: T, initialValue: T): T {
  const ref = useRef<T>(initialValue)
  useEffect(() => {
    ref.current = value
  })
  return ref.current
}
// ──────────────────────────────────────────────
// Hooks that compose other hooks
// ──────────────────────────────────────────────
export function useDebouncedLocalStorage<T>(
  key: string,
  initialValue: T,
  delay: number = 300
): [T, (value: T | ((prev: T) => T)) => void] {
  const [rawValue, setRawValue, removeValue] = useLocalStorage(key, initialValue)
  const debouncedValue = useDebounce(rawValue, delay)
  return [debouncedValue, setRawValue]
}
// ──────────────────────────────────────────────
// Tests (Vitest / @testing-library/react)
// ──────────────────────────────────────────────
/*
import { renderHook, act } from '@testing-library/react'
describe('useDebounce', () => {
  beforeEach(() => vi.useFakeTimers())
  afterEach(() => vi.useRealTimers())
  it('returns initial value immediately', () => {
    const { result } = renderHook(() => useDebounce('hello', 500))
    expect(result.current).toBe('hello')
  })
  it('debounces value changes', () => {
    const { result, rerender } = renderHook(
      ({ value }) => useDebounce(value, 500),
      { initialProps: { value: 'a' } }
    )
    rerender({ value: 'b' })
    expect(result.current).toBe('a')
    act(() => vi.advanceTimersByTime(500))
    expect(result.current).toBe('b')
  })
})
describe('useLocalStorage', () => {
  beforeEach(() => localStorage.clear())
  it('returns initial value when key is absent', () => {
    const { result } = renderHook(() => useLocalStorage('count', 0))
    expect(result.current[0]).toBe(0)
  })
  it('persists value to localStorage', () => {
    const { result } = renderHook(() => useLocalStorage('count', 0))
    act(() => result.current[1](42))
    expect(result.current[0]).toBe(42)
    expect(JSON.parse(localStorage.getItem('count')!)).toBe(42)
  })
  it('removes value from localStorage', () => {
    const { result } = renderHook(() => useLocalStorage('count', 0))
    act(() => result.current[1](42))
    act(() => result.current[2]())
    expect(result.current[0]).toBe(0)
    expect(localStorage.getItem('count')).toBeNull()
  })
})
describe('useMediaQuery', () => {
  it('returns false when media does not match', () => {
    window.matchMedia = vi.fn().mockImplementation((q: string) => ({
      matches: false,
      media: q,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
    }))
    const { result } = renderHook(() => useMediaQuery('(min-width: 1px)'))
    expect(result.current).toBe(false)
  })
})
describe('useIntersectionObserver', () => {
  it('returns ref and null entry initially', () => {
    const { result } = renderHook(() => useIntersectionObserver())
    expect(result.current[0].current).toBeNull()
    expect(result.current[1]).toBeNull()
  })
})
describe('usePrevious', () => {
  it('returns undefined on first render', () => {
    const { result } = renderHook(() => usePrevious(0))
    expect(result.current).toBeUndefined()
  })
  it('returns previous value after update', () => {
    const { result, rerender } = renderHook(
      ({ v }) => usePrevious(v),
      { initialProps: { v: 1 } }
    )
    rerender({ v: 2 })
    expect(result.current).toBe(1)
    rerender({ v: 3 })
    expect(result.current).toBe(2)
  })
})
describe('useDebouncedLocalStorage', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.useFakeTimers()
  })
  afterEach(() => vi.useRealTimers())
  it('returns stored value with debounced read', () => {
    const { result } = renderHook(() => useDebouncedLocalStorage('key', 'initial', 300))
    expect(result.current[0]).toBe('initial')
  })
})
*/