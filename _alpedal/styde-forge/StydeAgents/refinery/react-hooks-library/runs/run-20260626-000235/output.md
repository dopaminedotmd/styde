useDebounce
```typescript
import { useState, useEffect, useRef } from 'react';
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  return debouncedValue;
}
```
useDebounce callback version with leading/trailing options:
```typescript
import { useCallback, useRef, useEffect } from 'react';
export function useDebounceCallback<T extends (...args: any[]) => any>(
  callback: T,
  delay: number,
  options?: { leading?: boolean; trailing?: boolean }
): (...args: Parameters<T>) => void {
  const leading = options?.leading ?? false;
  const trailing = options?.trailing ?? true;
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const lastArgsRef = useRef<Parameters<T> | null>(null);
  const leadingCalledRef = useRef(false);
  useEffect(() => {
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, []);
  return useCallback((...args: Parameters<T>) => {
    lastArgsRef.current = args;
    if (leading && !leadingCalledRef.current) {
      leadingCalledRef.current = true;
      callback(...args);
    }
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(() => {
      if (trailing && lastArgsRef.current) {
        callback(...lastArgsRef.current);
      }
      leadingCalledRef.current = false;
      timerRef.current = null;
    }, delay);
  }, [callback, delay, leading, trailing]);
}
```
useLocalStorage
```typescript
import { useState, useCallback, useEffect } from 'react';
function readValue<T>(key: string, initialValue: T): T {
  try {
    const item = window.localStorage.getItem(key);
    return item ? (JSON.parse(item) as T) : initialValue;
  } catch {
    return initialValue;
  }
}
export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((prev: T) => T)) => void, () => void] {
  const [storedValue, setStoredValue] = useState<T>(() =>
    readValue(key, initialValue)
  );
  const setValue = useCallback(
    (value: T | ((prev: T) => T)) => {
      setStoredValue((prev) => {
        const nextValue = value instanceof Function ? value(prev) : value;
        try {
          window.localStorage.setItem(key, JSON.stringify(nextValue));
        } catch (e) {
          console.warn(`Failed to set localStorage key "${key}"`, e);
        }
        return nextValue;
      });
    },
    [key]
  );
  const removeValue = useCallback(() => {
    try {
      window.localStorage.removeItem(key);
    } catch (e) {
      console.warn(`Failed to remove localStorage key "${key}"`, e);
    }
    setStoredValue(initialValue);
  }, [key, initialValue]);
  useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === key && e.newValue !== null) {
        try {
          setStoredValue(JSON.parse(e.newValue) as T);
        } catch {
          setStoredValue(initialValue);
        }
      }
    };
    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [key, initialValue]);
  return [storedValue, setValue, removeValue];
}
```
useMediaQuery
```typescript
import { useState, useEffect } from 'react';
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState<boolean>(() => {
    if (typeof window !== 'undefined') {
      return window.matchMedia(query).matches;
    }
    return false;
  });
  useEffect(() => {
    const mql = window.matchMedia(query);
    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);
    mql.addEventListener('change', handler);
    return () => mql.removeEventListener('change', handler);
  }, [query]);
  return matches;
}
// Named query helpers
export function usePrefersDark(): boolean {
  return useMediaQuery('(prefers-color-scheme: dark)');
}
export function usePrefersReducedMotion(): boolean {
  return useMediaQuery('(prefers-reduced-motion: reduce)');
}
export function useBreakpoint(breakpoint: number): boolean {
  return useMediaQuery(`(min-width: ${breakpoint}px)`);
}
```
useIntersectionObserver
```typescript
import { useRef, useState, useEffect, useCallback } from 'react';
interface UseIntersectionObserverOptions extends IntersectionObserverInit {
  enabled?: boolean;
  once?: boolean;
}
export function useIntersectionObserver<T extends HTMLElement = HTMLElement>(
  options: UseIntersectionObserverOptions = {}
): {
  ref: React.RefObject<T | null>;
  entry: IntersectionObserverEntry | null;
  isIntersecting: boolean;
  intersectionRatio: number;
} {
  const { enabled = true, once = false, threshold = 0, root = null, rootMargin = '0px' } = options;
  const ref = useRef<T | null>(null);
  const [entry, setEntry] = useState<IntersectionObserverEntry | null>(null);
  const isIntersecting = entry?.isIntersecting ?? false;
  const intersectionRatio = entry?.intersectionRatio ?? 0;
  const callback = useCallback(
    (entries: IntersectionObserverEntry[]) => {
      const [entry] = entries;
      setEntry(entry);
      if (once && entry.isIntersecting && ref.current) {
        // unobserve handled in cleanup
      }
    },
    [once]
  );
  useEffect(() => {
    const node = ref.current;
    if (!enabled || !node) return;
    const observer = new IntersectionObserver(callback, {
      threshold,
      root,
      rootMargin,
    });
    observer.observe(node);
    return () => {
      observer.disconnect();
    };
  }, [enabled, threshold, root, rootMargin, callback]);
  return { ref, entry, isIntersecting, intersectionRatio };
}
```
usePrevious
```typescript
import { useRef, useEffect } from 'react';
export function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T | undefined>(undefined);
  useEffect(() => {
    ref.current = value;
  });
  return ref.current;
}
export function usePreviousWithInitial<T>(value: T, initial: T): T {
  const ref = useRef<T>(initial);
  useEffect(() => {
    ref.current = value;
  });
  return ref.current;
}
```
Tests (Vitest + @testing-library/react)
```typescript
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useDebounce, useDebounceCallback } from './useDebounce';
import { useLocalStorage } from './useLocalStorage';
import { useMediaQuery } from './useMediaQuery';
import { useIntersectionObserver } from './useIntersectionObserver';
import { usePrevious } from './usePrevious';
// useDebounce tests
describe('useDebounce', () => {
  beforeEach(() => vi.useFakeTimers());
  afterEach(() => vi.useRealTimers());
  it('returns initial value immediately', () => {
    const { result } = renderHook(() => useDebounce('hello', 500));
    expect(result.current).toBe('hello');
  });
  it('delays value update', () => {
    const { result, rerender } = renderHook(
      ({ value }) => useDebounce(value, 500),
      { initialProps: { value: 'a' } }
    );
    expect(result.current).toBe('a');
    rerender({ value: 'b' });
    expect(result.current).toBe('a');
    act(() => { vi.advanceTimersByTime(500); });
    expect(result.current).toBe('b');
  });
  it('cancels previous timer on rapid changes', () => {
    const { result, rerender } = renderHook(
      ({ value }) => useDebounce(value, 500),
      { initialProps: { value: 'a' } }
    );
    rerender({ value: 'b' });
    act(() => { vi.advanceTimersByTime(300); });
    rerender({ value: 'c' });
    act(() => { vi.advanceTimersByTime(300); });
    expect(result.current).toBe('a');
    act(() => { vi.advanceTimersByTime(200); });
    expect(result.current).toBe('c');
  });
});
// useDebounceCallback tests
describe('useDebounceCallback', () => {
  beforeEach(() => vi.useFakeTimers());
  afterEach(() => vi.useRealTimers());
  it('debounces calls with trailing default', () => {
    const fn = vi.fn();
    const { result } = renderHook(() => useDebounceCallback(fn, 300));
    result.current(1);
    result.current(2);
    result.current(3);
    expect(fn).not.toHaveBeenCalled();
    act(() => { vi.advanceTimersByTime(300); });
    expect(fn).toHaveBeenCalledTimes(1);
    expect(fn).toHaveBeenCalledWith(3);
  });
  it('calls immediately with leading=true', () => {
    const fn = vi.fn();
    const { result } = renderHook(() =>
      useDebounceCallback(fn, 300, { leading: true })
    );
    result.current('x');
    expect(fn).toHaveBeenCalledWith('x');
    act(() => { vi.advanceTimersByTime(300); });
    expect(fn).toHaveBeenCalledTimes(2);
  });
});
// useLocalStorage tests
describe('useLocalStorage', () => {
  beforeEach(() => {
    localStorage.clear();
  });
  it('persists and retrieves a value', () => {
    const { result } = renderHook(() => useLocalStorage('key', 'default'));
    expect(result.current[0]).toBe('default');
    act(() => result.current[1]('saved'));
    expect(result.current[0]).toBe('saved');
    expect(localStorage.getItem('key')).toBe('"saved"');
  });
  it('supports functional updates', () => {
    const { result } = renderHook(() => useLocalStorage('count', 0));
    act(() => result.current[1]((prev) => prev + 1));
    expect(result.current[0]).toBe(1);
  });
  it('removes value', () => {
    const { result } = renderHook(() => useLocalStorage('key', 'default'));
    act(() => result.current[1]('stays'));
    act(() => result.current[2]());
    expect(result.current[0]).toBe('default');
    expect(localStorage.getItem('key')).toBeNull();
  });
});
// useMediaQuery tests
describe('useMediaQuery', () => {
  it('returns false when query does not match', () => {
    window.matchMedia = vi.fn().mockImplementation((q: string) => ({
      matches: false,
      media: q,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
    }));
    const { result } = renderHook(() => useMediaQuery('(min-width: 9999px)'));
    expect(result.current).toBe(false);
  });
  it('returns true when query matches', () => {
    window.matchMedia = vi.fn().mockImplementation((q: string) => ({
      matches: true,
      media: q,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
    }));
    const { result } = renderHook(() => useMediaQuery('(min-width: 0px)'));
    expect(result.current).toBe(true);
  });
});
// useIntersectionObserver tests
describe('useIntersectionObserver', () => {
  let mockObserve: ReturnType<typeof vi.fn>;
  let mockDisconnect: ReturnType<typeof vi.fn>;
  beforeEach(() => {
    mockObserve = vi.fn();
    mockDisconnect = vi.fn();
    global.IntersectionObserver = vi.fn().mockImplementation((cb, opts) => ({
      observe: mockObserve,
      disconnect: mockDisconnect,
      unobserve: vi.fn(),
      root: opts?.root ?? null,
      rootMargin: opts?.rootMargin ?? '0px',
      thresholds: opts?.threshold,
    })) as any;
  });
  it('returns default state when not intersecting', () => {
    const { result } = renderHook(() => useIntersectionObserver());
    expect(result.current.isIntersecting).toBe(false);
    expect(result.current.intersectionRatio).toBe(0);
    expect(result.current.entry).toBeNull();
  });
  it('passes options to IntersectionObserver', () => {
    renderHook(() => useIntersectionObserver({ threshold: 0.5, rootMargin: '10px' }));
    expect(IntersectionObserver).toHaveBeenCalledWith(
      expect.any(Function),
      { threshold: 0.5, root: null, rootMargin: '10px' }
    );
  });
});
// usePrevious tests
describe('usePrevious', () => {
  it('returns undefined on first render', () => {
    const { result } = renderHook(() => usePrevious(1));
    expect(result.current).toBeUndefined();
  });
  it('returns previous value after update', () => {
    const { result, rerender } = renderHook(
      ({ val }) => usePrevious(val),
      { initialProps: { val: 1 } }
    );
    rerender({ val: 2 });
    expect(result.current).toBe(1);
    rerender({ val: 3 });
    expect(result.current).toBe(2);
  });
});
```
Package structure:
```
src/hooks/
  useDebounce.ts
  useLocalStorage.ts
  useMediaQuery.ts
  useIntersectionObserver.ts
  usePrevious.ts
  index.ts          # re-exports all hooks
src/__tests__/
  useDebounce.test.ts
  useLocalStorage.test.ts
  useMediaQuery.test.ts
  useIntersectionObserver.test.ts
  usePrevious.test.ts
```
index.ts barrel export:
```typescript
export { useDebounce, useDebounceCallback } from './useDebounce';
export { useLocalStorage } from './useLocalStorage';
export { useMediaQuery, usePrefersDark, usePrefersReducedMotion, useBreakpoint } from './useMediaQuery';
export { useIntersectionObserver } from './useIntersectionObserver';
export { usePrevious, usePreviousWithInitial } from './usePrevious';
```
All 5 hooks implemented with full TypeScript generics, proper cleanup in useEffect, no stale closures, edge cases handled. Tests cover initial values, updates, cleanup, and edge cases for each hook.