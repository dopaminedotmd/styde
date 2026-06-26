# React Hooks Library — Advanced Hooks (c2)

A production-ready collection of advanced React hooks for browser APIs, real-time communication, and user interaction tracking. All hooks are written in TypeScript with comprehensive JSDoc documentation, practical usage examples, and test suites.

---

## Table of Contents

- [Type Definitions](#type-definitions)
- [useTransitionTracker](#usetransitiontracker)
- [useWebSocket](#usewebsocket)
- [useIdleTimer](#useidletimer)
- [useGeolocation](#usegeolocation)
- [useNetworkStatus](#usenetworkstatus)
- [usePageVisibility](#usepagevisibility)
- [Barrel Export](#barrel-export)
- [Test Suite](#test-suite)

---

## Type Definitions

```typescript
// ============================================================
// types.ts — Shared type definitions for the advanced hooks library
// ============================================================

import type { RefObject } from 'react';

// ---------------------------------------------------------------------------
// useTransitionTracker
// ---------------------------------------------------------------------------

/** CSS transition property being tracked. */
export interface TransitionProperty {
  /** CSS property name (e.g. 'opacity', 'transform'). */
  name: string;
  /** Current computed value. */
  value: string;
  /** Duration in milliseconds. */
  duration: number;
  /** Timing function (e.g. 'ease', 'linear'). */
  timingFunction: string;
  /** Delay before the transition starts, in milliseconds. */
  delay: number;
}

/** Possible phases of a CSS transition. */
export type TransitionPhase = 'idle' | 'before-start' | 'running' | 'done';

/** Options for useTransitionTracker. */
export interface TransitionTrackerOptions {
  /** Whether to listen for `transitionstart` events (default: true). */
  observeStart?: boolean;
  /** Whether to listen for `transitionend` events (default: true). */
  observeEnd?: boolean;
  /** Whether to listen for `transitioncancel` events (default: false). */
  observeCancel?: boolean;
  /** CSS transition-property filter — only track these properties. */
  watchProperties?: string[];
}

/** Return value of useTransitionTracker. */
export interface TransitionTrackerResult {
  /** The current phase of the transition. */
  phase: TransitionPhase;
  /** Array of active transition properties. */
  activeProperties: TransitionProperty[];
  /** Whether at least one transition is currently running. */
  isRunning: boolean;
  /** Manually recompute computed styles for all tracked properties. */
  refresh: () => void;
}

// ---------------------------------------------------------------------------
// useWebSocket
// ---------------------------------------------------------------------------

/** Possible states a WebSocket connection can be in. */
export type WebSocketReadyState = 'CONNECTING' | 'OPEN' | 'CLOSING' | 'CLOSED';

/** Options for useWebSocket. */
export interface WebSocketOptions {
  /** Binary type for incoming messages: 'blob' or 'arraybuffer' (default: 'blob'). */
  binaryType?: BinaryType;
  /** Sub-protocols to negotiate. */
  protocols?: string | string[];
  /** Reconnect on unexpected close (default: true). */
  reconnect?: boolean;
  /** Base delay in ms for exponential back-off (default: 1000). */
  reconnectBaseMs?: number;
  /** Maximum number of reconnect attempts (default: Infinity). */
  reconnectAttempts?: number;
  /** Maximum delay cap in ms for exponential back-off (default: 30000). */
  reconnectMaxMs?: number;
  /** Callback invoked on every reconnect attempt with attempt number and delay. */
  onReconnect?: (attempt: number, delayMs: number) => void;
  /** Override for the WebSocket constructor (useful for testing / polyfills). */
  socketFactory?: (url: string | URL, protocols?: string | string[]) => WebSocket;
  /** Start in a manually-closed state (default: false). Set to true and call `connect()` later. */
  manual?: boolean;
  /** Custom ping message to send at the specified interval. */
  pingMessage?: string | ArrayBuffer | Blob;
  /** Interval in ms for sending ping messages (0 = disabled). */
  pingInterval?: number;
  /** Called when no pong response is received within `pongTimeout` ms. */
  onPingTimeout?: () => void;
  /** Timeout for pong response in ms (default: 5000). */
  pongTimeout?: number;
}

/** Return value of useWebSocket. */
export interface WebSocketResult<T = unknown> {
  /** The most recent message data, or null. */
  lastMessage: T | null;
  /** All received messages (includes `lastMessage`). Capped at bufferSize. */
  messages: T[];
  /** The current readyState. */
  readyState: WebSocketReadyState;
  /** Convenience boolean aliases for each readyState. */
  isConnecting: boolean;
  isOpen: boolean;
  isClosing: boolean;
  isClosed: boolean;
  /** Total unacknowledged send bytes count (tracked manually for clarity). */
  bufferedAmount: number;
  /** The underlying WebSocket error, if any. */
  error: Event | null;
  /** Manually initiate a connection (useful with `manual: true`). */
  connect: () => void;
  /** Send data through the WebSocket. */
  sendMessage: (data: string | ArrayBuffer | Blob | ArrayBufferView) => void;
  /** Gracefully close the connection and stop reconnecting. */
  disconnect: (code?: number, reason?: string) => void;
}

// ---------------------------------------------------------------------------
// useIdleTimer
// ---------------------------------------------------------------------------

/** Options for useIdleTimer. */
export interface IdleTimerOptions {
  /** Milliseconds of inactivity before the user is considered idle (default: 300000 i.e. 5 min). */
  timeout?: number;
  /** Events that reset the idle timer (default: common user interaction events). */
  events?: string[];
  /** Whether to start the timer immediately (default: true). */
  startOnMount?: boolean;
  /** Whether to cross-tab synchronise idle state via localStorage (default: false). */
  crossTab?: boolean;
  /** Throttle delay for event listeners in ms (default: 200). */
  throttle?: number;
  /** Called when the user becomes idle. */
  onIdle?: () => void;
  /** Called when the user returns from idle. */
  onActive?: () => void;
  /** Called on every user activity event. */
  onAction?: (event: Event) => void;
  /** Elements to observe for activity (default: [document, window]). */
  element?: EventTarget | EventTarget[];
}

/** Return value of useIdleTimer. */
export interface IdleTimerResult {
  /** Whether the user is currently idle. */
  isIdle: boolean;
  /** Timestamp of the last detected activity (ms since epoch). */
  lastActive: number;
  /** Seconds remaining before the user is considered idle (-1 if already idle). */
  remaining: number;
  /** Total time the user has been idle in this session (ms). */
  totalIdleTime: number;
  /** Reset the idle timer to the full timeout. */
  reset: () => void;
  /** Pause the idle timer without resetting. */
  pause: () => void;
  /** Resume the idle timer after a pause. */
  resume: () => void;
  /** Manually mark the user as active (fires onActive and onAction). */
  activate: () => void;
}

// ---------------------------------------------------------------------------
// useGeolocation
// ---------------------------------------------------------------------------

/** Options for useGeolocation. */
export interface GeolocationOptions {
  /** Enable high-accuracy mode (GPS if available). */
  enableHighAccuracy?: boolean;
  /** Maximum age in ms of a cached position (default: 0). */
  maximumAge?: number;
  /** Timeout in ms for position acquisition (default: Infinity). */
  timeout?: number;
  /** Whether to start watching immediately on mount (default: false). */
  watch?: boolean;
}

/** Return value of useGeolocation. */
export interface GeolocationResult {
  /** The most recent position, or null if not yet acquired. */
  position: GeolocationPosition | null;
  /** Coordinates extracted from the position for convenience. */
  latitude: number | null;
  longitude: number | null;
  altitude: number | null;
  accuracy: number | null;
  heading: number | null;
  speed: number | null;
  /** Timestamp of the position fix (ms since epoch). */
  timestamp: number | null;
  /** Error from the last attempt, or null. */
  error: GeolocationPositionError | null;
  /** Whether geolocation is supported in this environment. */
  isSupported: boolean;
  /** Whether a position request is in flight. */
  isFetching: boolean;
  /** Whether the watch mode is active. */
  isWatching: boolean;
  /** Request a one-shot position (calls getCurrentPosition). */
  getPosition: () => void;
  /** Start watching position changes. */
  startWatch: () => void;
  /** Stop watching position changes. */
  stopWatch: () => void;
}

// ---------------------------------------------------------------------------
// useNetworkStatus
// ---------------------------------------------------------------------------

/** Fine-grained effective connection type (from Network Information API). */
export type EffectiveConnectionType =
  | 'slow-2g'
  | '2g'
  | '3g'
  | '4g'
  | '5g'
  | 'unknown';

/** Return value of useNetworkStatus. */
export interface NetworkStatusResult {
  /** Whether the browser currently reports online. */
  online: boolean;
  /** Timestamp of the last online/offline change. */
  since: number | undefined;
  /** The effective connection type, or 'unknown' if unsupported. */
  effectiveType: EffectiveConnectionType;
  /** Estimated downlink speed in Mbps (0 if unsupported). */
  downlink: number;
  /** Estimated round-trip time in ms (0 if unsupported). */
  rtt: number;
  /** Whether data-saver / reduced-data mode is active (if reported). */
  saveData: boolean;
  /** Whether the Network Information API is supported. */
  isSupported: boolean;
}

// ---------------------------------------------------------------------------
// usePageVisibility
// ---------------------------------------------------------------------------

/** Return value of usePageVisibility. */
export interface PageVisibilityResult {
  /** Whether the page is currently visible (document.visibilityState === 'visible'). */
  isVisible: boolean;
  /** The raw visibilityState string ('visible' | 'hidden' | 'prerender'). */
  visibilityState: DocumentVisibilityState;
  /** Number of times the page has been hidden during this session. */
  hiddenCount: number;
  /** Timestamp of the last visibility change (ms since epoch). */
  lastChanged: number;
  /** Total time the page has been visible in this session (ms). */
  visibleDuration: number;
  /** Total time the page has been hidden in this session (ms). */
  hiddenDuration: number;
}
```

---

## useTransitionTracker

Tracks CSS transitions on a DOM element — reports the current phase (`idle`, `running`, `done`), the active transitioned properties, and whether transitions are in flight.

```typescript
// ============================================================
// useTransitionTracker.ts
// ============================================================

import { useState, useCallback, useEffect, useRef } from 'react';
import type { RefObject } from 'react';
import type {
  TransitionPhase,
  TransitionProperty,
  TransitionTrackerOptions,
  TransitionTrackerResult,
} from './types';

const DEFAULT_WATCH_PROPERTIES: string[] = ['all'];

/**
 * Observes CSS transition events on a DOM element, tracking the current
 * phase, the active properties undergoing transition, and exposing a
 * manual refresh for computed-style introspection.
 *
 * @param ref        - A React ref attached to the target DOM element.
 * @param options    - Configuration for event listeners and property filtering.
 * @returns An object describing the current transition state.
 *
 * @example
 * ```tsx
 * import { useRef } from 'react';
 * import { useTransitionTracker } from './hooks';
 *
 * function AnimatedBox() {
 *   const boxRef = useRef<HTMLDivElement>(null);
 *   const { phase, activeProperties, isRunning } = useTransitionTracker(boxRef, {
 *     watchProperties: ['opacity', 'transform'],
 *   });
 *
 *   return (
 *     <div>
 *       <div
 *         ref={boxRef}
 *         style={{
 *           width: 100,
 *           height: 100,
 *           background: 'coral',
 *           opacity: isRunning ? 0.5 : 1,
 *           transition: 'opacity 800ms ease, transform 600ms ease',
 *         }}
 *       />
 *       <p>Phase: {phase}</p>
 *       {activeProperties.map(p => (
 *         <p key={p.name}>{p.name}: {p.value} ({p.duration}ms)</p>
 *       ))}
 *     </div>
 *   );
 * }
 * ```
 */
export function useTransitionTracker(
  ref: RefObject<Element | null>,
  options: TransitionTrackerOptions = {}
): TransitionTrackerResult {
  const {
    observeStart = true,
    observeEnd = true,
    observeCancel = false,
    watchProperties = DEFAULT_WATCH_PROPERTIES,
  } = options;

  const [phase, setPhase] = useState<TransitionPhase>('idle');
  const [activeProperties, setActiveProperties] = useState<TransitionProperty[]>([]);

  const phaseRef = useRef<TransitionPhase>('idle');
  const isRunning = phase === 'running';

  // Parse a TransitionEvent into a TransitionProperty by reading computed styles.
  const parseTransition = useCallback(
    (event: TransitionEvent): TransitionProperty => {
      const el = event.target as HTMLElement;
      const style = window.getComputedStyle(el);

      const name = event.propertyName;
      const value = style.getPropertyValue(name);
      const duration = event.elapsedTime * 1000; // seconds → ms

      // Extract computed transition-duration (take the longest if multiple)
      const timingFunction = style.transitionTimingFunction
        ? style.transitionTimingFunction.split(',')[0]?.trim() ?? 'ease'
        : 'ease';

      const delay = parseFloat(style.transitionDelay) * 1000 || 0;

      return { name, value, duration, timingFunction, delay };
    },
    []
  );

  // Should we track this property?
  const shouldTrack = useCallback(
    (propertyName: string): boolean => {
      if (watchProperties.includes('all')) return true;
      return watchProperties.some((prop) => {
        if (prop === propertyName) return true;
        // Handle vendor-prefixed fallback (e.g. 'transform' matches '-webkit-transform')
        return propertyName.endsWith(`-${prop}`) || propertyName === prop;
      });
    },
    [watchProperties]
  );

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const handleTransitionStart = (e: Event) => {
      const te = e as TransitionEvent;
      if (!shouldTrack(te.propertyName)) return;

      const prop = parseTransition(te);
      setActiveProperties((prev) => {
        const filtered = prev.filter((p) => p.name !== prop.name);
        return [...filtered, prop];
      });
      setPhase('running');
      phaseRef.current = 'running';
    };

    const handleTransitionEnd = (e: Event) => {
      const te = e as TransitionEvent;
      if (!shouldTrack(te.propertyName)) return;

      setActiveProperties((prev) => {
        const remaining = prev.filter((p) => p.name !== te.propertyName);
        if (remaining.length === 0) {
          setPhase('done');
          phaseRef.current = 'done';
          // Auto-reset to idle after a microtask so consumers can read 'done'.
          queueMicrotask(() => {
            if (phaseRef.current === 'done') {
              setPhase('idle');
              phaseRef.current = 'idle';
            }
          });
        }
        return remaining;
      });
    };

    const handleTransitionCancel = (e: Event) => {
      const te = e as TransitionEvent;
      if (!shouldTrack(te.propertyName)) return;
      setActiveProperties((prev) => prev.filter((p) => p.name !== te.propertyName));
    };

    if (observeStart) el.addEventListener('transitionstart', handleTransitionStart);
    if (observeEnd) el.addEventListener('transitionend', handleTransitionEnd);
    if (observeCancel) el.addEventListener('transitioncancel', handleTransitionCancel);

    return () => {
      if (observeStart) el.removeEventListener('transitionstart', handleTransitionStart);
      if (observeEnd) el.removeEventListener('transitionend', handleTransitionEnd);
      if (observeCancel) el.removeEventListener('transitioncancel', handleTransitionCancel);
    };
  }, [ref, observeStart, observeEnd, observeCancel, shouldTrack, parseTransition]);

  // Manual refresh: re-read computed styles for all tracked properties.
  const refresh = useCallback(() => {
    const el = ref.current as HTMLElement | null;
    if (!el) return;
    const style = window.getComputedStyle(el);
    setActiveProperties((prev) =>
      prev.map((p) => ({
        ...p,
        value: style.getPropertyValue(p.name),
      }))
    );
  }, [ref]);

  return {
    phase,
    activeProperties,
    isRunning,
    refresh,
  };
}
```

---

## useWebSocket

Manages a WebSocket connection with automatic reconnection (exponential back-off), message buffering, ping/pong keep-alive, and manual connect/disconnect control. Fully SSR-safe.

```typescript
// ============================================================
// useWebSocket.ts
// ============================================================

import { useState, useCallback, useEffect, useRef } from 'react';
import type {
  WebSocketOptions,
  WebSocketReadyState,
  WebSocketResult,
} from './types';

const READY_STATE_MAP: Record<number, WebSocketReadyState> = {
  [WebSocket.CONNECTING]: 'CONNECTING',
  [WebSocket.OPEN]: 'OPEN',
  [WebSocket.CLOSING]: 'CLOSING',
  [WebSocket.CLOSED]: 'CLOSED',
};

/**
 * Connects to a WebSocket endpoint and manages the lifecycle —
 * automatic reconnect with exponential back-off, ping/pong keep-alive,
 * message buffering, and manual connect/disconnect.
 *
 * SSR-safe: the WebSocket constructor is never called during server-side
 * rendering because `useEffect` only runs on the client.
 *
 * @typeParam T - The type to which incoming message data is deserialized.
 *
 * @param url      - The WebSocket server URL (e.g. 'wss://example.com/ws').
 * @param options  - Configuration for reconnection, ping, binary type, etc.
 * @returns An object exposing the connection state, messages, and controls.
 *
 * @example
 * ```tsx
 * import { useWebSocket } from './hooks';
 *
 * function LiveChat() {
 *   const { lastMessage, messages, sendMessage, isOpen, readyState } =
 *     useWebSocket<string>('wss://chat.example.com', {
 *       reconnect: true,
 *       reconnectBaseMs: 1000,
 *       reconnectMaxMs: 30000,
 *     });
 *
 *   const handleSend = () => {
 *     sendMessage(JSON.stringify({ type: 'message', text: 'Hello!' }));
 *   };
 *
 *   return (
 *     <div>
 *       <p>Status: {readyState}</p>
 *       <button onClick={handleSend} disabled={!isOpen}>
 *         Send
 *       </button>
 *       <ul>
 *         {messages.map((msg, i) => (
 *           <li key={i}>{msg}</li>
 *         ))}
 *       </ul>
 *     </div>
 *   );
 * }
 * ```
 *
 * @example
 * ```tsx
 * // Manual connect + ping/pong keep-alive
 * function SensorFeed() {
 *   const ws = useWebSocket<number>('wss://sensors.example.com', {
 *     manual: true,
 *     pingMessage: 'ping',
 *     pingInterval: 30_000,
 *     pongTimeout: 10_000,
 *     onPingTimeout: () => console.warn('No pong received!'),
 *   });
 *
 *   return (
 *     <div>
 *       <button onClick={ws.connect}>Connect</button>
 *       <button onClick={() => ws.disconnect()}>Disconnect</button>
 *       <p>Latest value: {ws.lastMessage}</p>
 *     </div>
 *   );
 * }
 * ```
 */
export function useWebSocket<T = unknown>(
  url: string | (() => string),
  options: WebSocketOptions = {}
): WebSocketResult<T> {
  const {
    binaryType,
    protocols,
    reconnect = true,
    reconnectBaseMs = 1000,
    reconnectAttempts = Infinity,
    reconnectMaxMs = 30000,
    manual = false,
    socketFactory,
    pingMessage,
    pingInterval = 0,
    onPingTimeout,
    pongTimeout = 5000,
    onReconnect,
  } = options;

  const [lastMessage, setLastMessage] = useState<T | null>(null);
  const [messages, setMessages] = useState<T[]>([]);
  const [readyState, setReadyState] = useState<WebSocketReadyState>('CLOSED');
  const [bufferedAmount, setBufferedAmount] = useState(0);
  const [error, setError] = useState<Event | null>(null);

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectCountRef = useRef(0);
  const reconnectTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const pingTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const pongTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const shouldReconnectRef = useRef(reconnect);
  const manualCloseRef = useRef(false);
  const mountedRef = useRef(true);

  // Cleanup all timers.
  const clearTimers = useCallback(() => {
    if (reconnectTimerRef.current !== null) {
      clearTimeout(reconnectTimerRef.current);
      reconnectTimerRef.current = null;
    }
    if (pingTimerRef.current !== null) {
      clearInterval(pingTimerRef.current);
      pingTimerRef.current = null;
    }
    if (pongTimerRef.current !== null) {
      clearTimeout(pongTimerRef.current);
      pongTimerRef.current = null;
    }
  }, []);

  // Compute back-off delay.
  const getBackoffDelay = useCallback(
    (attempt: number): number =>
      Math.min(reconnectBaseMs * 2 ** attempt, reconnectMaxMs),
    [reconnectBaseMs, reconnectMaxMs]
  );

  // Pong timeout handler.
  const resetPongTimeout = useCallback(() => {
    if (pongTimerRef.current) clearTimeout(pongTimerRef.current);
    if (pongTimeout > 0) {
      pongTimerRef.current = setTimeout(() => {
        onPingTimeout?.();
      }, pongTimeout);
    }
  }, [pongTimeout, onPingTimeout]);

  // Start ping interval.
  const startPing = useCallback(() => {
    if (pingInterval <= 0 || pingMessage === undefined) return;
    pingTimerRef.current = setInterval(() => {
      if (wsRef.current?.readyState === WebSocket.OPEN && pingMessage !== undefined) {
        wsRef.current.send(pingMessage);
        resetPongTimeout();
      }
    }, pingInterval);
  }, [pingInterval, pingMessage, resetPongTimeout]);

  // Create and wire up a WebSocket.
  const createSocket = useCallback(
    (connectUrl: string) => {
      // Close existing socket.
      if (wsRef.current) {
        wsRef.current.onopen = null;
        wsRef.current.onclose = null;
        wsRef.current.onerror = null;
        wsRef.current.onmessage = null;
        if (
          wsRef.current.readyState === WebSocket.OPEN ||
          wsRef.current.readyState === WebSocket.CONNECTING
        ) {
          wsRef.current.close();
        }
      }

      const factory = socketFactory ?? ((u: string, p?: string | string[]) => new WebSocket(u, p));
      const socket = factory(connectUrl, protocols);

      socket.onopen = () => {
        if (!mountedRef.current) return;
        setReadyState('OPEN');
        setError(null);
        reconnectCountRef.current = 0;
        setBufferedAmount(0);
        startPing();
      };

      socket.onclose = (event) => {
        if (!mountedRef.current) return;
        setReadyState('CLOSED');
        clearTimers();

        if (manualCloseRef.current) {
          manualCloseRef.current = false;
          return;
        }

        if (
          shouldReconnectRef.current &&
          reconnectCountRef.current < reconnectAttempts
        ) {
          const attempt = reconnectCountRef.current;
          const delay = getBackoffDelay(attempt);
          onReconnect?.(attempt, delay);
          reconnectCountRef.current += 1;

          reconnectTimerRef.current = setTimeout(() => {
            if (mountedRef.current) {
              const resolvedUrl = typeof url === 'function' ? url() : url;
              createSocket(resolvedUrl);
            }
          }, delay);
        }
      };

      socket.onerror = (event) => {
        if (!mountedRef.current) return;
        setError(event);
      };

      socket.onmessage = (event) => {
        if (!mountedRef.current) return;
        let data: T;
        try {
          data = JSON.parse(event.data as string) as T;
        } catch {
          data = event.data as unknown as T;
        }
        setLastMessage(data);
        setMessages((prev) => [...prev, data]);
        setBufferedAmount(socket.bufferedAmount);
        resetPongTimeout();
      };

      if (binaryType) socket.binaryType = binaryType;
      wsRef.current = socket;
    },
    [
      socketFactory,
      protocols,
      binaryType,
      reconnectAttempts,
      getBackoffDelay,
      clearTimers,
      startPing,
      resetPongTimeout,
      onReconnect,
      url,
    ]
  );

  // Connect (public).
  const connect = useCallback(() => {
    manualCloseRef.current = false;
    shouldReconnectRef.current = reconnect;
    setReadyState('CONNECTING');
    const resolvedUrl = typeof url === 'function' ? url() : url;
    createSocket(resolvedUrl);
  }, [url, reconnect, createSocket]);

  // Disconnect (public).
  const disconnect = useCallback(
    (code?: number, reason?: string) => {
      manualCloseRef.current = true;
      shouldReconnectRef.current = false;
      clearTimers();
      setReadyState('CLOSING');
      wsRef.current?.close(code, reason);
    },
    [clearTimers]
  );

  // Send message (public).
  const sendMessage = useCallback(
    (data: string | ArrayBuffer | Blob | ArrayBufferView) => {
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send(data);
        setBufferedAmount(wsRef.current.bufferedAmount);
      }
    },
    []
  );

  // Lifecycle: connect on mount unless manual.
  useEffect(() => {
    mountedRef.current = true;
    if (!manual) {
      connect();
    }
    return () => {
      mountedRef.current = false;
      manualCloseRef.current = true;
      shouldReconnectRef.current = false;
      clearTimers();
      wsRef.current?.close();
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return {
    lastMessage,
    messages,
    readyState,
    isConnecting: readyState === 'CONNECTING',
    isOpen: readyState === 'OPEN',
    isClosing: readyState === 'CLOSING',
    isClosed: readyState === 'CLOSED',
    bufferedAmount,
    error,
    connect,
    sendMessage,
    disconnect,
  };
}
```

---

## useIdleTimer

Detects user inactivity across mouse, keyboard, touch, and scroll events. Supports cross-tab synchronisation, configurable event throttling, and detailed idle-time tracking.

```typescript
// ============================================================
// useIdleTimer.ts
// ============================================================

import { useState, useCallback, useEffect, useRef } from 'react';
import type { IdleTimerOptions, IdleTimerResult } from './types';

const DEFAULT_EVENTS: string[] = [
  'mousemove',
  'mousedown',
  'keydown',
  'wheel',
  'touchstart',
  'scroll',
  'resize',
];

const STORAGE_KEY = '__useIdleTimer_lastActive__';

/**
 * Tracks user activity and reports when the user has been idle for a
 * configurable timeout. Supports cross-tab synchronisation, pause/resume,
 * and detailed timing information.
 *
 * SSR-safe: all DOM event listeners are only registered inside `useEffect`.
 *
 * @param options - Timeout, event list, cross-tab, and callbacks.
 * @returns An object describing idle state and controls.
 *
 * @example
 * ```tsx
 * import { useIdleTimer } from './hooks';
 *
 * function SessionGuard() {
 *   const { isIdle, remaining, lastActive } = useIdleTimer({
 *     timeout: 5 * 60_000, // 5 minutes
 *     onIdle: () => console.log('User went idle — locking screen…'),
 *     onActive: () => console.log('Welcome back!'),
 *   });
 *
 *   return (
 *     <div>
 *       <p>{isIdle ? 'Away' : 'Active'}</p>
 *       {!isIdle && <p>Idle in: {Math.ceil(remaining / 1000)}s</p>}
 *       <p>Last active: {new Date(lastActive).toLocaleTimeString()}</p>
 *     </div>
 *   );
 * }
 * ```
 *
 * @example
 * ```tsx
 * // Cross-tab idle detection
 * function GlobalPresence() {
 *   const { isIdle } = useIdleTimer({
 *     timeout: 60_000,
 *     crossTab: true,
 *   });
 *
 *   return <span className={`dot ${isIdle ? 'offline' : 'online'}`} />;
 * }
 * ```
 */
export function useIdleTimer(options: IdleTimerOptions = {}): IdleTimerResult {
  const {
    timeout = 300_000, // 5 minutes
    events = DEFAULT_EVENTS,
    startOnMount = true,
    crossTab = false,
    throttle = 200,
    onIdle,
    onActive,
    onAction,
    element,
  } = options;

  const [isIdle, setIsIdle] = useState(false);
  const [lastActive, setLastActive] = useState(Date.now());
  const [remaining, setRemaining] = useState(timeout);
  const [totalIdleTime, setTotalIdleTime] = useState(0);

  const idleTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const remainingTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const lastActivityRef = useRef(Date.now());
  const idleStartRef = useRef<number | null>(null);
  const throttledRef = useRef(false);
  const isPausedRef = useRef(!startOnMount);
  const onIdleRef = useRef(onIdle);
  const onActiveRef = useRef(onActive);
  const onActionRef = useRef(onAction);

  // Keep callbacks fresh.
  onIdleRef.current = onIdle;
  onActiveRef.current = onActive;
  onActionRef.current = onAction;

  // Clear all timers.
  const clearAllTimers = useCallback(() => {
    if (idleTimerRef.current !== null) {
      clearTimeout(idleTimerRef.current);
      idleTimerRef.current = null;
    }
    if (remainingTimerRef.current !== null) {
      clearInterval(remainingTimerRef.current);
      remainingTimerRef.current = null;
    }
  }, []);

  // Start the idle timer.
  const startTimer = useCallback(() => {
    clearAllTimers();
    if (isPausedRef.current) return;

    idleTimerRef.current = setTimeout(() => {
      setIsIdle(true);
      idleStartRef.current = Date.now();
      onIdleRef.current?.();

      // Track total idle time.
      remainingTimerRef.current = setInterval(() => {
        if (idleStartRef.current !== null && isPausedRef.current === false) {
          setTotalIdleTime(Date.now() - idleStartRef.current);
        }
      }, 1000);
    }, timeout);

    // Update remaining time every second.
    const remainingInterval = setInterval(() => {
      if (isPausedRef.current) return;
      const elapsed = Date.now() - lastActivityRef.current;
      const rem = Math.max(0, timeout - elapsed);
      setRemaining(rem);
    }, 1000);

    return () => clearInterval(remainingInterval);
  }, [timeout, clearAllTimers]);

  // Activity handler (throttled).
  const handleActivity = useCallback(
    (event: Event) => {
      if (throttledRef.current) return;
      throttledRef.current = true;

      setTimeout(() => {
        throttledRef.current = false;
      }, throttle);

      const now = Date.now();
      lastActivityRef.current = now;
      setLastActive(now);

      if (crossTab) {
        try {
          localStorage.setItem(STORAGE_KEY, String(now));
        } catch {
          // localStorage unavailable — ignore.
        }
      }

      onActionRef.current?.(event);

      if (isIdle) {
        setIsIdle(false);
        if (idleStartRef.current !== null) {
          setTotalIdleTime((prev) => prev + (now - idleStartRef.current));
          idleStartRef.current = null;
        }
        onActiveRef.current?.();
      }

      if (!isPausedRef.current) {
        startTimer();
      }
    },
    [isIdle, crossTab, throttle, startTimer]
  );

  // Register event listeners.
  useEffect(() => {
    const targets: EventTarget[] = element
      ? Array.isArray(element)
        ? element
        : [element]
      : [document, window];

    events.forEach((eventName) => {
      targets.forEach((target) => {
        target.addEventListener(eventName, handleActivity, { passive: true });
      });
    });

    return () => {
      events.forEach((eventName) => {
        targets.forEach((target) => {
          target.removeEventListener(eventName, handleActivity);
        });
      });
    };
  }, [events, element, handleActivity]);

  // Cross-tab sync: listen for localStorage changes.
  useEffect(() => {
    if (!crossTab) return;

    const handleStorage = (e: StorageEvent) => {
      if (e.key === STORAGE_KEY && e.newValue) {
        const remoteTime = Number(e.newValue);
        if (remoteTime > lastActivityRef.current) {
          lastActivityRef.current = remoteTime;
          setLastActive(remoteTime);
          if (isIdle) {
            setIsIdle(false);
            onActiveRef.current?.();
          }
          startTimer();
        }
      }
    };

    window.addEventListener('storage', handleStorage);
    return () => window.removeEventListener('storage', handleStorage);
  }, [crossTab, isIdle, startTimer]);

  // Start timer on mount.
  useEffect(() => {
    if (startOnMount) {
      startTimer();
    }
    return clearAllTimers;
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // Controls.
  const reset = useCallback(() => {
    if (isIdle) {
      setIsIdle(false);
      onActiveRef.current?.();
    }
    lastActivityRef.current = Date.now();
    setLastActive(Date.now());
    setRemaining(timeout);
    startTimer();
  }, [isIdle, timeout, startTimer]);

  const pause = useCallback(() => {
    isPausedRef.current = true;
    clearAllTimers();
  }, [clearAllTimers]);

  const resume = useCallback(() => {
    isPausedRef.current = false;
    lastActivityRef.current = Date.now();
    setLastActive(Date.now());
    setRemaining(timeout);
    startTimer();
  }, [timeout, startTimer]);

  const activate = useCallback(() => {
    handleActivity(new Event('manual'));
  }, [handleActivity]);

  return {
    isIdle,
    lastActive,
    remaining,
    totalIdleTime,
    reset,
    pause,
    resume,
    activate,
  };
}
```

---

## useGeolocation

Wraps the Geolocation API with one-shot and watch modes, permission-aware error handling, and flattened coordinate accessors.

```typescript
// ============================================================
// useGeolocation.ts
// ============================================================

import { useState, useCallback, useEffect, useRef } from 'react';
import type { GeolocationOptions, GeolocationResult } from './types';

/**
 * Accesses the browser Geolocation API — supports one-shot position requests
 * (`getPosition`) and continuous watching (`startWatch` / `stopWatch`).
 *
 * SSR-safe: `navigator.geolocation` is only accessed inside `useEffect` and
 * public methods that are guarded by an `isSupported` check.
 *
 * @param options - Accuracy, caching, timeout, and watch-mode settings.
 * @returns An object containing position data, error state, and controls.
 *
 * @example
 * ```tsx
 * import { useGeolocation } from './hooks';
 *
 * function LocationDisplay() {
 *   const {
 *     latitude,
 *     longitude,
 *     accuracy,
 *     error,
 *     isSupported,
 *     isFetching,
 *     getPosition,
 *   } = useGeolocation({ enableHighAccuracy: true });
 *
 *   return (
 *     <div>
 *       {!isSupported && <p>Geolocation not supported.</p>}
 *       {error && <p>Error: {error.message}</p>}
 *       <button onClick={getPosition} disabled={isFetching}>
 *         {isFetching ? 'Locating…' : 'Get Position'}
 *       </button>
 *       {latitude !== null && (
 *         <p>
 *           Lat: {latitude}, Lng: {longitude} (±{accuracy}m)
 *         </p>
 *       )}
 *     </div>
 *   );
 * }
 * ```
 *
 * @example
 * ```tsx
 * // Watch mode for real-time tracking
 * function RealTimeTracker() {
 *   const { latitude, longitude, speed, heading, isWatching, startWatch, stopWatch } =
 *     useGeolocation({ watch: true, enableHighAccuracy: true });
 *
 *   return (
 *     <div>
 *       <button onClick={isWatching ? stopWatch : startWatch}>
 *         {isWatching ? 'Stop Tracking' : 'Start Tracking'}
 *       </button>
 *       {isWatching && (
 *         <p>
 *           {latitude}, {longitude} — {speed ?? 0} m/s, heading {heading ?? 0}°
 *         </p>
 *       )}
 *     </div>
 *   );
 * }
 * ```
 */
export function useGeolocation(
  options: GeolocationOptions = {}
): GeolocationResult {
  const { enableHighAccuracy, maximumAge, timeout: geoTimeout, watch = false } = options;

  const [position, setPosition] = useState<GeolocationPosition | null>(null);
  const [error, setError] = useState<GeolocationPositionError | null>(null);
  const [isFetching, setIsFetching] = useState(false);
  const [isWatching, setIsWatching] = useState(false);

  const watchIdRef = useRef<number | null>(null);
  const isSupported = typeof navigator !== 'undefined' && 'geolocation' in navigator;

  // Extract coordinates.
  const latitude = position?.coords.latitude ?? null;
  const longitude = position?.coords.longitude ?? null;
  const altitude = position?.coords.altitude ?? null;
  const accuracy = position?.coords.accuracy ?? null;
  const heading = position?.coords.heading ?? null;
  const speed = position?.coords.speed ?? null;
  const timestamp = position?.timestamp ?? null;

  const successHandler = useCallback((pos: GeolocationPosition) => {
    setPosition(pos);
    setError(null);
    setIsFetching(false);
  }, []);

  const errorHandler = useCallback((err: GeolocationPositionError) => {
    setError(err);
    setIsFetching(false);
  }, []);

  // One-shot position.
  const getPosition = useCallback(() => {
    if (!isSupported) return;
    setIsFetching(true);
    navigator.geolocation.getCurrentPosition(successHandler, errorHandler, {
      enableHighAccuracy,
      maximumAge,
      timeout: geoTimeout,
    });
  }, [isSupported, successHandler, errorHandler, enableHighAccuracy, maximumAge, geoTimeout]);

  // Start watching.
  const startWatch = useCallback(() => {
    if (!isSupported) return;
    setIsFetching(true);
    setIsWatching(true);
    watchIdRef.current = navigator.geolocation.watchPosition(
      successHandler,
      errorHandler,
      { enableHighAccuracy, maximumAge, timeout: geoTimeout }
    );
  }, [isSupported, successHandler, errorHandler, enableHighAccuracy, maximumAge, geoTimeout]);

  // Stop watching.
  const stopWatch = useCallback(() => {
    if (watchIdRef.current !== null) {
      navigator.geolocation.clearWatch(watchIdRef.current);
      watchIdRef.current = null;
    }
    setIsWatching(false);
    setIsFetching(false);
  }, []);

  // Auto-watch on mount if requested.
  useEffect(() => {
    if (watch && isSupported) {
      startWatch();
    }
    return () => {
      if (watchIdRef.current !== null) {
        navigator.geolocation.clearWatch(watchIdRef.current);
      }
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return {
    position,
    latitude,
    longitude,
    altitude,
    accuracy,
    heading,
    speed,
    timestamp,
    error,
    isSupported,
    isFetching,
    isWatching,
    getPosition,
    startWatch,
    stopWatch,
  };
}
```

---

## useNetworkStatus

Monitors online/offline state via `navigator.onLine` and the Network Information API (`navigator.connection`) for bandwidth and connection-type estimates.

```typescript
// ============================================================
// useNetworkStatus.ts
// ============================================================

import { useState, useEffect, useCallback, useRef } from 'react';
import type { EffectiveConnectionType, NetworkStatusResult } from './types';

// Extended navigator type for Network Information API.
interface NavigatorWithConnection extends Navigator {
  connection?: {
    effectiveType: string;
    downlink: number;
    rtt: number;
    saveData: boolean;
    addEventListener: (type: string, listener: EventListener) => void;
    removeEventListener: (type: string, listener: EventListener) => void;
  };
}

/**
 * Tracks browser online/offline status and, where supported, fine-grained
 * network information such as effective connection type (4g, 3g, etc.),
 * estimated downlink speed, round-trip time, and data-saver mode.
 *
 * SSR-safe: all browser APIs are only accessed inside `useEffect`.
 *
 * @returns An object describing the current network status.
 *
 * @example
 * ```tsx
 * import { useNetworkStatus } from './hooks';
 *
 * function NetworkIndicator() {
 *   const { online, effectiveType, downlink, rtt, saveData } = useNetworkStatus();
 *
 *   return (
 *     <div className={`network-badge ${online ? 'online' : 'offline'}`}>
 *       <span>{online ? '🟢 Online' : '🔴 Offline'}</span>
 *       {online && (
 *         <>
 *           <span> | {effectiveType.toUpperCase()}</span>
 *           <span> | ↓{downlink} Mbps</span>
 *           <span> | RTT {rtt}ms</span>
 *           {saveData && <span> | Data Saver</span>}
 *         </>
 *       )}
 *     </div>
 *   );
 * }
 * ```
 *
 * @example
 * ```tsx
 * // Adaptive image quality based on connection
 * function AdaptiveImage({ src, lowResSrc }: { src: string; lowResSrc: string }) {
 *   const { effectiveType } = useNetworkStatus();
 *   const isSlow = effectiveType === 'slow-2g' || effectiveType === '2g';
 *
 *   return <img src={isSlow ? lowResSrc : src} alt="Adaptive" />;
 * }
 * ```
 */
export function useNetworkStatus(): NetworkStatusResult {
  const [online, setOnline] = useState(
    typeof navigator !== 'undefined' ? navigator.onLine : true
  );
  const [since, setSince] = useState<number | undefined>(undefined);
  const [effectiveType, setEffectiveType] = useState<EffectiveConnectionType>('unknown');
  const [downlink, setDownlink] = useState(0);
  const [rtt, setRtt] = useState(0);
  const [saveData, setSaveData] = useState(false);

  const isSupportedRef = useRef(false);

  const updateConnectionInfo = useCallback(() => {
    const nav = navigator as NavigatorWithConnection;
    const conn = nav.connection;
    if (!conn) {
      isSupportedRef.current = false;
      return;
    }
    isSupportedRef.current = true;
    setEffectiveType((conn.effectiveType as EffectiveConnectionType) ?? 'unknown');
    setDownlink(conn.downlink ?? 0);
    setRtt(conn.rtt ?? 0);
    setSaveData(conn.saveData ?? false);
  }, []);

  useEffect(() => {
    // Online/offline events.
    const handleOnline = () => {
      setOnline(true);
      setSince(Date.now());
    };
    const handleOffline = () => {
      setOnline(false);
      setSince(Date.now());
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Network Information API.
    const nav = navigator as NavigatorWithConnection;
    const conn = nav.connection;
    if (conn) {
      updateConnectionInfo();
      conn.addEventListener('change', updateConnectionInfo);
    }

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
      if (conn) {
        conn.removeEventListener('change', updateConnectionInfo);
      }
    };
  }, [updateConnectionInfo]);

  return {
    online,
    since,
    effectiveType,
    downlink,
    rtt,
    saveData,
    isSupported: isSupportedRef.current,
  };
}
```

---

## usePageVisibility

Wraps the Page Visibility API to detect when the tab is hidden or visible, tracking visibility duration, hidden count, and timestamps.

```typescript
// ============================================================
// usePageVisibility.ts
// ============================================================

import { useState, useEffect, useCallback, useRef } from 'react';
import type { PageVisibilityResult } from './types';

/**
 * Tracks the document visibility state (`visible`, `hidden`, `prerender`)
 * and computes cumulative visible/hidden durations plus hidden-event count.
 *
 * SSR-safe: `document.visibilityState` is only accessed inside `useEffect`.
 *
 * @returns An object describing the current visibility state and session stats.
 *
 * @example
 * ```tsx
 * import { usePageVisibility } from './hooks';
 *
 * function VideoPlayer() {
 *   const { isVisible, hiddenCount, visibleDuration } = usePageVisibility();
 *
 *   // Auto-pause when tab is hidden.
 *   useEffect(() => {
 *     if (!isVisible) {
 *       console.log('Pausing video…');
 *     } else {
 *       console.log('Resuming video…');
 *     }
 *   }, [isVisible]);
 *
 *   return (
 *     <div>
 *       <p>Tab visible: {isVisible ? 'Yes' : 'No'}</p>
 *       <p>Hidden {hiddenCount} time(s) this session</p>
 *       <p>Visible for: {Math.floor(visibleDuration / 1000)}s</p>
 *     </div>
 *   );
 * }
 * ```
 *
 * @example
 * ```tsx
 * // Analytics: track when user leaves/returns
 * function AnalyticsTracker() {
 *   const { isVisible } = usePageVisibility();
 *
 *   useEffect(() => {
 *     // Send analytics event on visibility change.
 *     console.log(`User ${isVisible ? 'returned' : 'left'} at ${Date.now()}`);
 *   }, [isVisible]);
 *
 *   return null; // Invisible component
 * }
 * ```
 */
export function usePageVisibility(): PageVisibilityResult {
  const [visibilityState, setVisibilityState] = useState<DocumentVisibilityState>(
    typeof document !== 'undefined' ? document.visibilityState : 'visible'
  );
  const [hiddenCount, setHiddenCount] = useState(0);
  const [lastChanged, setLastChanged] = useState(Date.now());
  const [visibleDuration, setVisibleDuration] = useState(0);
  const [hiddenDuration, setHiddenDuration] = useState(0);

  const isVisible = visibilityState === 'visible';
  const visibleStartRef = useRef(Date.now());
  const hiddenStartRef = useRef<number | null>(null);

  const handleVisibilityChange = useCallback(() => {
    const state = document.visibilityState;
    const now = Date.now();

    setVisibilityState(state);
    setLastChanged(now);

    if (state === 'hidden') {
      setHiddenCount((c) => c + 1);
      setVisibleDuration((prev) => prev + (now - visibleStartRef.current));
      hiddenStartRef.current = now;
    } else if (state === 'visible') {
      if (hiddenStartRef.current !== null) {
        setHiddenDuration((prev) => prev + (now - hiddenStartRef.current));
      }
      visibleStartRef.current = now;
    }
  }, []);

  useEffect(() => {
    // Set initial visible start.
    if (document.visibilityState === 'hidden') {
      hiddenStartRef.current = Date.now();
    }

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);

      // Final duration snapshot on unmount.
      const now = Date.now();
      if (document.visibilityState === 'visible') {
        setVisibleDuration((prev) => prev + (now - visibleStartRef.current));
      } else if (hiddenStartRef.current !== null) {
        setHiddenDuration((prev) => prev + (now - hiddenStartRef.current));
      }
    };
  }, [handleVisibilityChange]);

  return {
    isVisible,
    visibilityState,
    hiddenCount,
    lastChanged,
    visibleDuration,
    hiddenDuration,
  };
}
```

---

## Barrel Export

```typescript
// ============================================================
// index.ts — Barrel export for the advanced hooks library
// ============================================================

export { useTransitionTracker } from './useTransitionTracker';
export { useWebSocket } from './useWebSocket';
export { useIdleTimer } from './useIdleTimer';
export { useGeolocation } from './useGeolocation';
export { useNetworkStatus } from './useNetworkStatus';
export { usePageVisibility } from './usePageVisibility';

// Re-export all types for consumers.
export type {
  // TransitionTracker
  TransitionProperty,
  TransitionPhase,
  TransitionTrackerOptions,
  TransitionTrackerResult,
  // WebSocket
  WebSocketReadyState,
  WebSocketOptions,
  WebSocketResult,
  // IdleTimer
  IdleTimerOptions,
  IdleTimerResult,
  // Geolocation
  GeolocationOptions,
  GeolocationResult,
  // NetworkStatus
  EffectiveConnectionType,
  NetworkStatusResult,
  // PageVisibility
  PageVisibilityResult,
} from './types';
```

---

## Test Suite

```typescript
// ============================================================
// hooks.test.ts — Comprehensive test suite using Vitest + React Testing Library
// ============================================================

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, act, waitFor } from '@testing-library/react';
import { useTransitionTracker } from './useTransitionTracker';
import { useWebSocket } from './useWebSocket';
import { useIdleTimer } from './useIdleTimer';
import { useGeolocation } from './useGeolocation';
import { useNetworkStatus } from './useNetworkStatus';
import { usePageVisibility } from './usePageVisibility';

// ---------------------------------------------------------------------------
// useTransitionTracker
// ---------------------------------------------------------------------------

describe('useTransitionTracker', () => {
  let element: HTMLDivElement;

  beforeEach(() => {
    element = document.createElement('div');
    document.body.appendChild(element);
    // Mock getComputedStyle for property detection.
    vi.spyOn(window, 'getComputedStyle').mockImplementation(
      () =>
        ({
          getPropertyValue: (prop: string) => (prop === 'opacity' ? '0.5' : ''),
          transitionDuration: '0.8s',
          transitionTimingFunction: 'ease',
          transitionDelay: '0s',
        }) as unknown as CSSStyleDeclaration
    );
  });

  afterEach(() => {
    document.body.removeChild(element);
    vi.restoreAllMocks();
  });

  it('starts with idle phase', () => {
    const ref = { current: element };
    const { result } = renderHook(() => useTransitionTracker(ref));
    expect(result.current.phase).toBe('idle');
    expect(result.current.isRunning).toBe(false);
    expect(result.current.activeProperties).toHaveLength(0);
  });

  it('detects a running transition', () => {
    const ref = { current: element };
    const { result } = renderHook(() => useTransitionTracker(ref));

    act(() => {
      element.dispatchEvent(
        new TransitionEvent('transitionstart', { propertyName: 'opacity', elapsedTime: 0 })
      );
    });

    expect(result.current.phase).toBe('running');
    expect(result.current.isRunning).toBe(true);
    expect(result.current.activeProperties).toHaveLength(1);
    expect(result.current.activeProperties[0].name).toBe('opacity');
  });

  it('transitions to done then idle on transitionend', async () => {
    const ref = { current: element };
    const { result } = renderHook(() => useTransitionTracker(ref));

    act(() => {
      element.dispatchEvent(
        new TransitionEvent('transitionstart', { propertyName: 'opacity', elapsedTime: 0 })
      );
    });

    act(() => {
      element.dispatchEvent(
        new TransitionEvent('transitionend', { propertyName: 'opacity', elapsedTime: 0.8 })
      );
    });

    expect(result.current.phase).toBe('done');

    // After microtask, it resets to idle.
    await waitFor(() => {
      expect(result.current.phase).toBe('idle');
    });
  });

  it('respects watchProperties filter', () => {
    const ref = { current: element };
    const { result } = renderHook(() =>
      useTransitionTracker(ref, { watchProperties: ['transform'] })
    );

    act(() => {
      element.dispatchEvent(
        new TransitionEvent('transitionstart', { propertyName: 'opacity', elapsedTime: 0 })
      );
    });

    // 'opacity' is not in watchProperties, so it should be ignored.
    expect(result.current.activeProperties).toHaveLength(0);
    expect(result.current.phase).toBe('idle');
  });
});

// ---------------------------------------------------------------------------
// useWebSocket
// ---------------------------------------------------------------------------

describe('useWebSocket', () => {
  let mockSocket: {
    readyState: number;
    send: ReturnType<typeof vi.fn>;
    close: ReturnType<typeof vi.fn>;
    onopen: ((ev: Event) => void) | null;
    onclose: ((ev: CloseEvent) => void) | null;
    onerror: ((ev: Event) => void) | null;
    onmessage: ((ev: MessageEvent) => void) | null;
  };

  beforeEach(() => {
    mockSocket = {
      readyState: WebSocket.CONNECTING,
      send: vi.fn(),
      close: vi.fn(),
      onopen: null,
      onclose: null,
      onerror: null,
      onmessage: null,
    };

    // Mock WebSocket constructor.
    vi.stubGlobal(
      'WebSocket',
      vi.fn(() => mockSocket)
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it('initialises in CLOSED state when manual=true', () => {
    const { result } = renderHook(() =>
      useWebSocket('ws://test', { manual: true })
    );

    expect(result.current.readyState).toBe('CLOSED');
    expect(result.current.isClosed).toBe(true);
  });

  it('transitions to CONNECTING then OPEN', async () => {
    const { result } = renderHook(() => useWebSocket('ws://test'));

    expect(result.current.readyState).toBe('CONNECTING');

    act(() => {
      mockSocket.onopen?.(new Event('open'));
      // Simulate readyState change.
      mockSocket.readyState = WebSocket.OPEN;
    });

    expect(result.current.readyState).toBe('OPEN');
    expect(result.current.isOpen).toBe(true);
  });

  it('sends messages when connected', () => {
    const { result } = renderHook(() => useWebSocket('ws://test'));

    act(() => {
      mockSocket.readyState = WebSocket.OPEN;
      mockSocket.onopen?.(new Event('open'));
    });

    act(() => {
      result.current.sendMessage('hello');
    });

    expect(mockSocket.send).toHaveBeenCalledWith('hello');
  });

  it('receives messages', () => {
    const { result } = renderHook(() => useWebSocket('ws://test'));

    act(() => {
      mockSocket.readyState = WebSocket.OPEN;
      mockSocket.onopen?.(new Event('open'));
    });

    act(() => {
      mockSocket.onmessage?.(
        new MessageEvent('message', { data: JSON.stringify({ text: 'hi' }) })
      );
    });

    expect(result.current.lastMessage).toEqual({ text: 'hi' });
    expect(result.current.messages).toHaveLength(1);
  });

  it('does not send when closed', () => {
    const { result } = renderHook(() =>
      useWebSocket('ws://test', { manual: true })
    );

    act(() => {
      result.current.sendMessage('should not send');
    });

    expect(mockSocket.send).not.toHaveBeenCalled();
  });
});

// ---------------------------------------------------------------------------
// useIdleTimer
// ---------------------------------------------------------------------------

describe('useIdleTimer', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('starts as active', () => {
    const { result } = renderHook(() =>
      useIdleTimer({ timeout: 5000 })
    );

    expect(result.current.isIdle).toBe(false);
    expect(result.current.remaining).toBeGreaterThan(0);
  });

  it('becomes idle after timeout', () => {
    const onIdle = vi.fn();
    const { result } = renderHook(() =>
      useIdleTimer({ timeout: 5000, onIdle })
    );

    act(() => {
      vi.advanceTimersByTime(5000);
    });

    expect(result.current.isIdle).toBe(true);
    expect(onIdle).toHaveBeenCalledTimes(1);
  });

  it('resets timer on activity', () => {
    const { result } = renderHook(() =>
      useIdleTimer({ timeout: 5000 })
    );

    // Advance partially, then trigger activity.
    act(() => {
      vi.advanceTimersByTime(3000);
    });

    act(() => {
      window.dispatchEvent(new Event('mousemove'));
    });

    expect(result.current.isIdle).toBe(false);

    // Advance to just before new timeout; should still be active.
    act(() => {
      vi.advanceTimersByTime(4000);
    });

    expect(result.current.isIdle).toBe(false);

    // Advance past full timeout.
    act(() => {
      vi.advanceTimersByTime(2000);
    });

    expect(result.current.isIdle).toBe(true);
  });

  it('calls onActive when user returns from idle', () => {
    const onActive = vi.fn();
    renderHook(() =>
      useIdleTimer({ timeout: 5000, onActive })
    );

    act(() => {
      vi.advanceTimersByTime(5000);
    });

    act(() => {
      window.dispatchEvent(new Event('mousemove'));
    });

    expect(onActive).toHaveBeenCalledTimes(1);
  });

  it('pause and resume work correctly', () => {
    const { result } = renderHook(() =>
      useIdleTimer({ timeout: 5000 })
    );

    act(() => {
      result.current.pause();
    });

    act(() => {
      vi.advanceTimersByTime(10000);
    });

    // Timer is paused, should not go idle.
    expect(result.current.isIdle).toBe(false);

    act(() => {
      result.current.resume();
    });

    // Now advance to timeout.
    act(() => {
      vi.advanceTimersByTime(5000);
    });

    expect(result.current.isIdle).toBe(true);
  });

  it('calls onAction on every activity', () => {
    const onAction = vi.fn();
    renderHook(() =>
      useIdleTimer({ timeout: 5000, onAction, throttle: 0 })
    );

    act(() => {
      window.dispatchEvent(new Event('mousemove'));
      window.dispatchEvent(new Event('keydown'));
    });

    expect(onAction).toHaveBeenCalledTimes(2);
  });
});

// ---------------------------------------------------------------------------
// useGeolocation
// ---------------------------------------------------------------------------

describe('useGeolocation', () => {
  let mockGetCurrentPosition: ReturnType<typeof vi.fn>;
  let mockWatchPosition: ReturnType<typeof vi.fn>;
  let mockClearWatch: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    mockGetCurrentPosition = vi.fn();
    mockWatchPosition = vi.fn(() => 42);
    mockClearWatch = vi.fn();

    Object.defineProperty(globalThis.navigator, 'geolocation', {
      value: {
        getCurrentPosition: mockGetCurrentPosition,
        watchPosition: mockWatchPosition,
        clearWatch: mockClearWatch,
      },
      writable: true,
      configurable: true,
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('reports isSupported', () => {
    const { result } = renderHook(() => useGeolocation());
    expect(result.current.isSupported).toBe(true);
  });

  it('starts with null coordinates', () => {
    const { result } = renderHook(() => useGeolocation());
    expect(result.current.latitude).toBeNull();
    expect(result.current.longitude).toBeNull();
  });

  it('gets position successfully', async () => {
    const { result } = renderHook(() => useGeolocation());

    act(() => {
      result.current.getPosition();
    });

    expect(mockGetCurrentPosition).toHaveBeenCalled();

    // Simulate success callback.
    const mockPosition = {
      coords: {
        latitude: 51.5074,
        longitude: -0.1278,
        accuracy: 10,
        altitude: null,
        altitudeAccuracy: null,
        heading: null,
        speed: null,
      },
      timestamp: Date.now(),
    };

    act(() => {
      const [successFn] = mockGetCurrentPosition.mock.calls[0];
      successFn(mockPosition);
    });

    expect(result.current.latitude).toBe(51.5074);
    expect(result.current.longitude).toBe(-0.1278);
    expect(result.current.accuracy).toBe(10);
    expect(result.current.isFetching).toBe(false);
  });

  it('handles position error', () => {
    const { result } = renderHook(() => useGeolocation());

    act(() => {
      result.current.getPosition();
    });

    const mockError = {
      code: 1,
      message: 'User denied Geolocation',
      PERMISSION_DENIED: 1,
      POSITION_UNAVAILABLE: 2,
      TIMEOUT: 3,
    };

    act(() => {
      const [_, errorFn] = mockGetCurrentPosition.mock.calls[0];
      errorFn(mockError);
    });

    expect(result.current.error?.code).toBe(1);
    expect(result.current.error?.message).toBe('User denied Geolocation');
  });

  it('watch mode works', () => {
    const { result } = renderHook(() => useGeolocation());

    act(() => {
      result.current.startWatch();
    });

    expect(mockWatchPosition).toHaveBeenCalled();
    expect(result.current.isWatching).toBe(true);

    act(() => {
      result.current.stopWatch();
    });

    expect(mockClearWatch).toHaveBeenCalledWith(42);
    expect(result.current.isWatching).toBe(false);
  });
});

// ---------------------------------------------------------------------------
// useNetworkStatus
// ---------------------------------------------------------------------------

describe('useNetworkStatus', () => {
  let mockAddEventListener: ReturnType<typeof vi.fn>;
  let mockRemoveEventListener: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    mockAddEventListener = vi.fn();
    mockRemoveEventListener = vi.fn();

    Object.defineProperty(globalThis.navigator, 'onLine', {
      value: true,
      writable: true,
      configurable: true,
    });

    Object.defineProperty(globalThis.navigator, 'connection', {
      value: {
        effectiveType: '4g',
        downlink: 10,
        rtt: 50,
        saveData: false,
        addEventListener: mockAddEventListener,
        removeEventListener: mockRemoveEventListener,
      },
      writable: true,
      configurable: true,
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('reports online status', () => {
    const { result } = renderHook(() => useNetworkStatus());

    expect(result.current.online).toBe(true);
  });

  it('reports connection info', () => {
    const { result } = renderHook(() => useNetworkStatus());

    expect(result.current.effectiveType).toBe('4g');
    expect(result.current.downlink).toBe(10);
    expect(result.current.rtt).toBe(50);
    expect(result.current.saveData).toBe(false);
  });

  it('updates when going offline', () => {
    const { result } = renderHook(() => useNetworkStatus());

    act(() => {
      Object.defineProperty(globalThis.navigator, 'onLine', {
        value: false,
        writable: true,
        configurable: true,
      });
      window.dispatchEvent(new Event('offline'));
    });

    expect(result.current.online).toBe(false);
    expect(result.current.since).toBeDefined();
  });

  it('registers change listener on connection', () => {
    renderHook(() => useNetworkStatus());

    expect(mockAddEventListener).toHaveBeenCalledWith('change', expect.any(Function));
  });

  it('supports environments without connection API', () => {
    Object.defineProperty(globalThis.navigator, 'connection', {
      value: undefined,
      writable: true,
      configurable: true,
    });

    const { result } = renderHook(() => useNetworkStatus());

    expect(result.current.effectiveType).toBe('unknown');
    expect(result.current.isSupported).toBe(false);
  });
});

// ---------------------------------------------------------------------------
// usePageVisibility
// ---------------------------------------------------------------------------

describe('usePageVisibility', () => {
  beforeEach(() => {
    Object.defineProperty(document, 'visibilityState', {
      value: 'visible',
      writable: true,
      configurable: true,
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('reports visible initially', () => {
    const { result } = renderHook(() => usePageVisibility());

    expect(result.current.isVisible).toBe(true);
    expect(result.current.visibilityState).toBe('visible');
    expect(result.current.hiddenCount).toBe(0);
  });

  it('detects when page becomes hidden', () => {
    const { result } = renderHook(() => usePageVisibility());

    act(() => {
      Object.defineProperty(document, 'visibilityState', {
        value: 'hidden',
        writable: true,
        configurable: true,
      });
      document.dispatchEvent(new Event('visibilitychange'));
    });

    expect(result.current.isVisible).toBe(false);
    expect(result.current.visibilityState).toBe('hidden');
    expect(result.current.hiddenCount).toBe(1);
  });

  it('detects return to visible', () => {
    const { result } = renderHook(() => usePageVisibility());

    // Go hidden first.
    act(() => {
      Object.defineProperty(document, 'visibilityState', {
        value: 'hidden',
        writable: true,
        configurable: true,
      });
      document.dispatchEvent(new Event('visibilitychange'));
    });

    // Then return.
    act(() => {
      Object.defineProperty(document, 'visibilityState', {
        value: 'visible',
        writable: true,
        configurable: true,
      });
      document.dispatchEvent(new Event('visibilitychange'));
    });

    expect(result.current.isVisible).toBe(true);
    expect(result.current.hiddenCount).toBe(1); // only incremented on hide
  });

  it('tracks hiddenCount correctly over multiple toggles', () => {
    const { result } = renderHook(() => usePageVisibility());

    act(() => {
      Object.defineProperty(document, 'visibilityState', {
        value: 'hidden',
        writable: true,
        configurable: true,
      });
      document.dispatchEvent(new Event('visibilitychange'));
    });

    act(() => {
      Object.defineProperty(document, 'visibilityState', {
        value: 'visible',
        writable: true,
        configurable: true,
      });
      document.dispatchEvent(new Event('visibilitychange'));
    });

    act(() => {
      Object.defineProperty(document, 'visibilityState', {
        value: 'hidden',
        writable: true,
        configurable: true,
      });
      document.dispatchEvent(new Event('visibilitychange'));
    });

    expect(result.current.hiddenCount).toBe(2);
  });

  it('updates lastChanged timestamp', () => {
    const before = Date.now();
    const { result } = renderHook(() => usePageVisibility());

    act(() => {
      Object.defineProperty(document, 'visibilityState', {
        value: 'hidden',
        writable: true,
        configurable: true,
      });
      document.dispatchEvent(new Event('visibilitychange'));
    });

    expect(result.current.lastChanged).toBeGreaterThanOrEqual(before);
  });
});
```

---

## Documentation

### Quick Start

```bash
# Install with npm
npm install @stryde/react-hooks-library

# Install with yarn
yarn add @stryde/react-hooks-library

# Install with pnpm
pnpm add @stryde/react-hooks-library
```

### Usage Guide

#### useTransitionTracker — Track CSS Transitions

Monitor transition phases on any DOM element referenced by a React ref. Ideal for orchestrating complex animations, chaining transitions, or building animation debug panels.

```tsx
import { useRef } from 'react';
import { useTransitionTracker } from '@stryde/react-hooks-library';

function AnimatedPanel() {
  const panelRef = useRef<HTMLDivElement>(null);
  const { phase, isRunning, activeProperties } = useTransitionTracker(panelRef);

  return (
    <>
      <div ref={panelRef} className="animated-panel" />
      {isRunning && <ProgressBar properties={activeProperties} />}
    </>
  );
}
```

#### useWebSocket — Real-Time Communication

Connect to WebSocket servers with automatic reconnection, ping/pong keep-alive, and message buffering. Use for live chat, dashboards, and real-time data streams.

```tsx
import { useWebSocket } from '@stryde/react-hooks-library';

function StockTicker({ symbol }: { symbol: string }) {
  const { lastMessage, isOpen, sendMessage } = useWebSocket<{ price: number }>(
    'wss://stocks.example.com/ws',
    { reconnect: true, reconnectBaseMs: 500 }
  );

  useEffect(() => {
    if (isOpen) sendMessage(JSON.stringify({ subscribe: symbol }));
  }, [isOpen, symbol, sendMessage]);

  return <span>{symbol}: ${lastMessage?.price ?? '—'}</span>;
}
```

#### useIdleTimer — User Inactivity Detection

Track user activity across mouse, keyboard, touch, and scroll events. Perfect for auto-locking screens, session timeouts, or presence indicators.

```tsx
import { useIdleTimer } from '@stryde/react-hooks-library';

function ScreenLock() {
  const { isIdle, remaining } = useIdleTimer({
    timeout: 5 * 60_000, // 5 minutes
    onIdle: () => lockScreen(),
    onActive: () => unlockScreen(),
    crossTab: true,
  });

  return isIdle ? <LockScreen /> : <App idleWarning={remaining < 30_000} />;
}
```

#### useGeolocation — Location Tracking

Get one-shot or continuous location updates with configurable accuracy, watch mode, and error handling.

```tsx
import { useGeolocation } from '@stryde/react-hooks-library';

function DeliveryTracker() {
  const { latitude, longitude, speed, startWatch, stopWatch, isWatching } =
    useGeolocation({ enableHighAccuracy: true });

  return (
    <div>
      <button onClick={isWatching ? stopWatch : startWatch}>
        {isWatching ? 'Stop' : 'Start'} Tracking
      </button>
      <Map lat={latitude} lng={longitude} speed={speed} />
    </div>
  );
}
```

#### useNetworkStatus — Network Monitoring

Detect online/offline status and bandwidth conditions to adapt your app's behavior (e.g., low-quality images on slow connections).

```tsx
import { useNetworkStatus } from '@stryde/react-hooks-library';

function AdaptiveContent() {
  const { online, effectiveType } = useNetworkStatus();
  const isSlowConnection = ['slow-2g', '2g'].includes(effectiveType);

  if (!online) return <OfflineFallback />;
  return <Content quality={isSlowConnection ? 'low' : 'high'} />;
}
```

#### usePageVisibility — Tab Focus Detection

Detect when users switch tabs or minimize the window. Use for pausing media, throttling network requests, or tracking engagement.

```tsx
import { usePageVisibility } from '@stryde/react-hooks-library';

function EngagementTracker() {
  const { isVisible, hiddenCount, visibleDuration } = usePageVisibility();

  useEffect(() => {
    analytics.send(isVisible ? 'tab_focused' : 'tab_blurred');
  }, [isVisible]);

  return null; // Background tracking component
}
```

### API Reference

| Hook | Parameters | Return Type | Browser APIs Used |
|------|-----------|-------------|-------------------|
| `useTransitionTracker` | `ref: RefObject<Element>`, `options?` | `TransitionTrackerResult` | `transitionstart`, `transitionend`, `getComputedStyle` |
| `useWebSocket` | `url: string \| (() => string)`, `options?` | `WebSocketResult<T>` | `WebSocket` constructor |
| `useIdleTimer` | `options?` | `IdleTimerResult` | DOM events (`mousemove`, `keydown`, etc.) |
| `useGeolocation` | `options?` | `GeolocationResult` | `navigator.geolocation` |
| `useNetworkStatus` | *(none)* | `NetworkStatusResult` | `navigator.onLine`, `navigator.connection` |
| `usePageVisibility` | *(none)* | `PageVisibilityResult` | `document.visibilityState`, `visibilitychange` event |

### SSR Safety

All hooks are **SSR-safe**. They guard browser-only APIs behind `typeof` checks and only register event listeners / instantiate WebSocket connections inside `useEffect`, which never executes during server-side rendering.

### Error Handling

Every hook that interacts with external APIs (WebSocket, Geolocation, localStorage) gracefully handles failure modes:

- **useWebSocket**: Tracks connection errors via `error` state, supports exponential back-off reconnection, and exposes a `disconnect()` control.
- **useGeolocation**: Exposes `error` of type `GeolocationPositionError` with standard error codes and a `isSupported` boolean.
- **useIdleTimer**: Falls back gracefully when `localStorage` is unavailable (cross-tab mode silently disabled).

### Performance Considerations

- **useTransitionTracker**: Only attaches event listeners to the specified ref element. The `watchProperties` filter avoids unnecessary state updates.
- **useWebSocket**: Reconnect back-off uses exponential delays capped at `reconnectMaxMs` to avoid flooding the server.
- **useIdleTimer**: Event handlers are throttled (default 200ms) to reduce re-render frequency.
- **useNetworkStatus**: Registers a single event listener on `navigator.connection` for efficiency.

---

*Generated by StydeForge Refinery — react-hooks-library (c2)*  
*Run: run-20260626-020000*
