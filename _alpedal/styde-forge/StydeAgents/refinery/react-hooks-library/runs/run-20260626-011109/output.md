// usePrevious.ts
import { useRef, useEffect } from 'react';
export function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T | undefined>(undefined);
  useEffect(() => {
    ref.current = value;
  }, [value]);
  return ref.current;
}
// useDebounce.ts
import { useState, useEffect } from 'react';
export function useDebounce<T>(value: T, delayMs: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);
  useEffect(() => {
    const id = setTimeout(() => setDebouncedValue(value), delayMs);
    return () => clearTimeout(id);
  }, [value, delayMs]);
  return debouncedValue;
}
export function useDebounceCallback<T extends (...args: any[]) => void>(
  callback: T,
  delayMs: number,
  deps: any[] = []
): T {
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const callbackRef = useRef<T>(callback);
  useEffect(() => { callbackRef.current = callback; }, [callback, ...deps]);
  useEffect(() => {
    return () => {
      if (timerRef.current !== null) clearTimeout(timerRef.current);
    };
  }, []);
  return ((...args: any[]) => {
    if (timerRef.current !== null) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(() => callbackRef.current(...args), delayMs);
  }) as T;
}
// useLocalStorage.ts
import { useState, useCallback } from 'react';
export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((prev: T) => T)) => void, () => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item !== null ? (JSON.parse(item) as T) : initialValue;
    } catch {
      return initialValue;
    }
  });
  const setValue = useCallback(
    (value: T | ((prev: T) => T)) => {
      setStoredValue((prev) => {
        const nextValue = value instanceof Function ? value(prev) : value;
        try {
          window.localStorage.setItem(key, JSON.stringify(nextValue));
        } catch (e) {
          console.warn(`useLocalStorage: failed to set key "${key}"`, e);
        }
        return nextValue;
      });
    },
    [key]
  );
  const removeValue = useCallback(() => {
    try {
      window.localStorage.removeItem(key);
      setStoredValue(initialValue);
    } catch (e) {
      console.warn(`useLocalStorage: failed to remove key "${key}"`, e);
    }
  }, [key, initialValue]);
  return [storedValue, setValue, removeValue];
}
// useMediaQuery.ts
import { useState, useEffect } from 'react';
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState<boolean>(() => {
    if (typeof window === 'undefined') return false;
    return window.matchMedia(query).matches;
  });
  useEffect(() => {
    const mql = window.matchMedia(query);
    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);
    mql.addEventListener('change', handler);
    return () => mql.removeEventListener('change', handler);
  }, [query]);
  return matches;
}
// useIntersectionObserver.ts
import { useRef, useState, useEffect, useMemo } from 'react';
interface UseIntersectionObserverOptions {
  threshold?: number | number[];
  root?: Element | Document | null;
  rootMargin?: string;
  freezeOnceVisible?: boolean;
}
export function useIntersectionObserver<T extends HTMLElement = HTMLElement>(
  options: UseIntersectionObserverOptions = {}
): { ref: React.RefCallback<T>; entry: IntersectionObserverEntry | null; isIntersecting: boolean } {
  const { threshold = 0, root = null, rootMargin = '0px', freezeOnceVisible = false } = options;
  const [entry, setEntry] = useState<IntersectionObserverEntry | null>(null);
  const frozenRef = useRef(false);
  const isIntersecting = entry?.isIntersecting ?? false;
  const ref = useCallback(
    (node: T | null) => {
      if (!node) return;
      if (freezeOnceVisible && frozenRef.current) return;
      const observer = new IntersectionObserver(
        ([e]) => {
          setEntry(e);
          if (freezeOnceVisible && e.isIntersecting) {
            frozenRef.current = true;
            observer.unobserve(node);
          }
        },
        { threshold, root, rootMargin }
      );
      observer.observe(node);
      return () => observer.disconnect();
    },
    [threshold, root, rootMargin, freezeOnceVisible]
  );
  return { ref, entry, isIntersecting };
}
// index.ts
export { usePrevious } from './usePrevious';
export { useDebounce, useDebounceCallback } from './useDebounce';
export { useLocalStorage } from './useLocalStorage';
export { useMediaQuery } from './useMediaQuery';
export { useIntersectionObserver } from './useIntersectionObserver';
// __tests__ / hooks.test.tsx
import { renderHook, act } from '@testing-library/react';
import { usePrevious } from '../usePrevious';
import { useDebounce, useDebounceCallback } from '../useDebounce';
import { useLocalStorage } from '../useLocalStorage';
import { useMediaQuery } from '../useMediaQuery';
describe('usePrevious', () => {
  it('returns undefined on first render', () => {
    const { result } = renderHook(() => usePrevious(0));
    expect(result.current).toBeUndefined();
  });
  it('returns previous value after update', () => {
    const { result, rerender } = renderHook((v: number) => usePrevious(v), { initialProps: 1 });
    rerender(2);
    expect(result.current).toBe(1);
    rerender(3);
    expect(result.current).toBe(2);
  });
});
describe('useDebounce', () => {
  jest.useFakeTimers();
  it('returns initial value immediately', () => {
    const { result } = renderHook(() => useDebounce('hello', 500));
    expect(result.current).toBe('hello');
  });
  it('delays value update', () => {
    const { result, rerender } = renderHook((v: string) => useDebounce(v, 500), { initialProps: 'a' });
    rerender('b');
    expect(result.current).toBe('a');
    act(() => { jest.advanceTimersByTime(500); });
    expect(result.current).toBe('b');
  });
  it('cancels previous timer on rapid updates', () => {
    const { result, rerender } = renderHook((v: string) => useDebounce(v, 500), { initialProps: 'a' });
    rerender('b');
    act(() => { jest.advanceTimersByTime(200); });
    rerender('c');
    act(() => { jest.advanceTimersByTime(200); });
    expect(result.current).toBe('a');
    act(() => { jest.advanceTimersByTime(300); });
    expect(result.current).toBe('c');
  });
});
describe('useLocalStorage', () => {
  beforeEach(() => {
    window.localStorage.clear();
  });
  it('returns initial value when key absent', () => {
    const { result } = renderHook(() => useLocalStorage('test', 'default'));
    expect(result.current[0]).toBe('default');
  });
  it('persists value across set', () => {
    const { result } = renderHook(() => useLocalStorage('test', 'default'));
    act(() => result.current[1]('hello'));
    expect(result.current[0]).toBe('hello');
    expect(JSON.parse(window.localStorage.getItem('test')!)).toBe('hello');
  });
  it('removes value and resets to initial', () => {
    const { result } = renderHook(() => useLocalStorage('test', 'default'));
    act(() => result.current[1]('hello'));
    act(() => result.current[2]());
    expect(result.current[0]).toBe('default');
    expect(window.localStorage.getItem('test')).toBeNull();
  });
});
describe('useMediaQuery', () => {
  it('returns false when query does not match', () => {
    window.matchMedia = jest.fn().mockImplementation((q: string) => ({
      matches: false,
      media: q,
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
    }));
    const { result } = renderHook(() => useMediaQuery('(min-width: 9999px)'));
    expect(result.current).toBe(false);
  });
  it('returns true when query matches', () => {
    window.matchMedia = jest.fn().mockImplementation((q: string) => ({
      matches: true,
      media: q,
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
    }));
    const { result } = renderHook(() => useMediaQuery('(max-width: 10px)'));
    expect(result.current).toBe(true);
  });
});
describe('useDebounceCallback', () => {
  jest.useFakeTimers();
  it('delays callback invocation', () => {
    const fn = jest.fn();
    const { result } = renderHook(() => useDebounceCallback(fn, 300));
    act(() => result.current());
    expect(fn).not.toHaveBeenCalled();
    act(() => { jest.advanceTimersByTime(300); });
    expect(fn).toHaveBeenCalledTimes(1);
  });
  it('cancels pending call on rapid invocations', () => {
    const fn = jest.fn();
    const { result } = renderHook(() => useDebounceCallback(fn, 300));
    act(() => result.current());
    act(() => { jest.advanceTimersByTime(100); });
    act(() => result.current());
    act(() => { jest.advanceTimersByTime(100); });
    expect(fn).not.toHaveBeenCalled();
    act(() => { jest.advanceTimersByTime(200); });
    expect(fn).toHaveBeenCalledTimes(1);
  });
});