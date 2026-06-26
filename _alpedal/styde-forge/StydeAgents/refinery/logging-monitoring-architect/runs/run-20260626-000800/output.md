# Styde Forge — Observability & Monitoring Architecture

> **Generated:** 2026-06-26 00:08:00 UTC  
> **Agent:** logging-monitoring-architect · Styde Forge  
> **Scope:** End-to-end observability stack — traces, logs, metrics, dashboards, alerts, and error tracking for the Styde Forge platform.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [OpenTelemetry Tracing Setup](#2-opentelemetry-tracing-setup)
   - [2.1 Python SDK Instrumentation](#21-python-sdk-instrumentation)
   - [2.2 Automatic Instrumentation](#22-automatic-instrumentation)
   - [2.3 Custom Spans for Forge Pipelines](#23-custom-spans-for-forge-pipelines)
   - [2.4 Context Propagation (Correlation IDs)](#24-context-propagation-correlation-ids)
   - [2.5 Export Configuration (OTLP)](#25-export-configuration-otlp)
3. [Structured Logging with Correlation IDs](#3-structured-logging-with-correlation-ids)
   - [3.1 Logger Factory](#31-logger-factory)
   - [3.2 Correlation ID Middleware](#32-correlation-id-middleware)
   - [3.3 Log Format & Enrichment](#33-log-format--enrichment)
   - [3.4 Integration with OpenTelemetry](#34-integration-with-opentelemetry)
4. [Prometheus Metrics — RED Method](#4-prometheus-metrics--red-method)
   - [4.1 Metric Definitions](#41-metric-definitions)
   - [4.2 Instrumentation Decorators](#42-instrumentation-decorators)
   - [4.3 Metrics Endpoint](#43-metrics-endpoint)
   - [4.4 Exemplar Injection](#44-exemplar-injection)
5. [Grafana Dashboard JSON](#5-grafana-dashboard-json)
   - [5.1 Dashboard Structure](#51-dashboard-structure)
   - [5.2 Full Dashboard JSON](#52-full-dashboard-json)
6. [Alerting Rules with Runbooks](#6-alerting-rules-with-runbooks)
   - [6.1 Alert Definitions](#61-alert-definitions)
   - [6.2 Runbook Catalog](#62-runbook-catalog)
7. [Error Tracking Integration](#7-error-tracking-integration)
   - [7.1 Sentry Integration](#71-sentry-integration)
   - [7.2 Custom Error Context](#72-custom-error-context)
   - [7.3 Error Aggregation & Fingerprinting](#73-error-aggregation--fingerprinting)
8. [Deployment Checklist](#8-deployment-checklist)
9. [Full Reference Implementation](#9-full-reference-implementation)

---

## 1. Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         STYDE FORGE OBSERVABILITY                         │
│                                                                          │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐                  │
│  │   Traces     │   │    Logs      │   │   Metrics    │                  │
│  │ (OpenTelemetry)│  │ (structlog) │   │ (Prometheus) │                  │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘                  │
│         │                  │                  │                          │
│         │    Correlation   │                  │                          │
│         │◄────── ID ──────►│                  │                          │
│         │                  │                  │                          │
│  ┌──────┴──────────────────┴──────────────────┴───────┐                  │
│  │              OTLP Collector (gRPC)                  │                  │
│  │          localhost:4317 / localhost:4318            │                  │
│  └──────┬──────────────────┬──────────────────┬───────┘                  │
│         │                  │                  │                          │
│  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐                   │
│  │    Tempo     │  │    Loki      │  │ Prometheus   │                   │
│  │  (traces)    │  │  (logs)      │  │ (metrics)    │                   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                   │
│         │                  │                  │                          │
│  ┌──────┴──────────────────┴──────────────────┴───────┐                  │
│  │                   Grafana                          │                  │
│  │   Dashboards · Explore · Alerts · SLO Tracking     │                  │
│  └────────────────────────────────────────────────────┘                  │
│                                                                          │
│  ┌──────────────────────────────────────────────┐                        │
│  │         Error Tracking: Sentry                │                        │
│  │  (exceptions, crash reports, release health)  │                        │
│  └──────────────────────────────────────────────┘                        │
└──────────────────────────────────────────────────────────────────────────┘
```

### Design Principles

| Principle | Implementation |
|-----------|---------------|
| **Single source of truth** | Correlation ID links traces ↔ logs ↔ errors |
| **RED Method** | Rate, Errors, Duration for every service endpoint |
| **Code-first instrumentation** | Decorators + context managers, not sidecar config |
| **Zero-touch for developers** | Auto-instrumentation covers standard libraries |
| **Progressive disclosure** | WARN by default, DEBUG on demand, TRACE for deep dives |
| **Alert on symptoms, not causes** | SLO-based alerting with clear runbooks |

---

## 2. OpenTelemetry Tracing Setup

### 2.1 Python SDK Instrumentation

Create the core tracing module at `StydeAgents/observability/tracing.py`:

```python
"""
Styde Forge — OpenTelemetry Tracing Core.
Initializes the global TracerProvider, propagators, and exporters.
"""
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION, DEPLOYMENT_ENVIRONMENT
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.composite import CompositePropagator
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.baggage.propagation import W3CBaggagePropagator

# ── Resource (identifies this service in traces) ──────────────────────
RESOURCE = Resource.create({
    SERVICE_NAME: os.getenv("OTEL_SERVICE_NAME", "styde-forge"),
    SERVICE_VERSION: os.getenv("STYDE_FORGE_VERSION", "3.0.0"),
    DEPLOYMENT_ENVIRONMENT: os.getenv("DEPLOY_ENV", "development"),
    "forge.instance.id": os.getenv("FORGE_INSTANCE_ID", "local"),
})

# ── Propagator (W3C TraceContext + Baggage) ───────────────────────────
set_global_textmap(CompositePropagator([
    TraceContextTextMapPropagator(),
    W3CBaggagePropagator(),
]))


def init_tracing(
    otlp_endpoint: str | None = None,
    console_export: bool = False,
    sample_rate: float = 1.0,
) -> TracerProvider:
    """
    Initialize the OpenTelemetry TracerProvider with batched export.

    Args:
        otlp_endpoint: OTLP collector gRPC endpoint (default: localhost:4317)
        console_export: Emit spans to stdout for local dev
        sample_rate: Fraction of spans to sample (1.0 = all)
    """
    provider = TracerProvider(resource=RESOURCE)

    # ── OTLP gRPC exporter (production) ────────────────────────────────
    if otlp_endpoint is None:
        otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")

    otlp_exporter = OTLPSpanExporter(
        endpoint=otlp_endpoint,
        insecure=os.getenv("OTEL_EXPORTER_OTLP_INSECURE", "true") == "true",
    )
    provider.add_span_processor(
        BatchSpanProcessor(
            otlp_exporter,
            max_queue_size=2048,
            max_export_batch_size=512,
            schedule_delay_millis=5000,
            export_timeout_millis=30000,
        )
    )

    # ── Console exporter (development) ─────────────────────────────────
    if console_export or os.getenv("OTEL_CONSOLE_EXPORT", "false") == "true":
        provider.add_span_processor(
            BatchSpanProcessor(ConsoleSpanExporter())
        )

    trace.set_tracer_provider(provider)
    return provider


def get_tracer(name: str | None = None) -> trace.Tracer:
    """Get a named tracer. Defaults to the service name."""
    return trace.get_tracer(name or os.getenv("OTEL_SERVICE_NAME", "styde-forge"))
```

### 2.2 Automatic Instrumentation

Install the auto-instrumentation packages:

```bash
# Production dependencies
uv add opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-grpc

# Auto-instrumentation for common libraries
uv add opentelemetry-instrumentation-flask
uv add opentelemetry-instrumentation-requests
uv add opentelemetry-instrumentation-redis
uv add opentelemetry-instrumentation-sqlalchemy
uv add opentelemetry-instrumentation-httpx
uv add opentelemetry-instrumentation-logging
uv add opentelemetry-instrumentation-system-metrics
uv add opentelemetry-instrumentation-asgi        # for uvicorn / FastAPI
```

**Bootstrap auto-instrumentation** at application startup (`StydeAgents/observability/__init__.py`):

```python
"""
Observability bootstrap.
Import this module first to auto-instrument before any other imports.
"""
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor


def bootstrap_instrumentation():
    """Call once at application startup."""
    # HTTP clients
    RequestsInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()

    # Databases
    SQLAlchemyInstrumentor().instrument(
        enable_commenter=True,   # SQL comments with trace context
        commenter_options={},
    )
    RedisInstrumentor().instrument()

    # Log injection: attaches trace_id / span_id to log records
    LoggingInstrumentor().instrument(
        set_logging_format=True,
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )

    # System metrics (CPU, memory, GC)
    SystemMetricsInstrumentor().instrument()

    # Flask — instrument AFTER app creation
    # FlaskInstrumentor().instrument_app(app)
```

**Entry point** — wire everything in `Core/forge_main.py`:

```python
"""
Styde Forge main entry point with observability bootstrapping.
"""
import os
import sys

# ── 1. Bootstrap OpenTelemetry FIRST (before any library imports) ────
from StydeAgents.observability.tracing import init_tracing, get_tracer
init_tracing()

# ── 2. Auto-instrument all libraries ──────────────────────────────────
from StydeAgents.observability import bootstrap_instrumentation
bootstrap_instrumentation()

# ── 3. Now import application code ────────────────────────────────────
from Core.dashboard import run_dashboard
from Core.forge_engine import ForgeEngine

tracer = get_tracer("forge-engine")

def main():
    with tracer.start_as_current_span("forge.main") as span:
        span.set_attribute("forge.version", os.getenv("STYDE_FORGE_VERSION", "3.0.0"))
        span.set_attribute("forge.pid", os.getpid())

        engine = ForgeEngine()
        engine.start()
        run_dashboard(engine)

if __name__ == "__main__":
    main()
```

### 2.3 Custom Spans for Forge Pipelines

Decorate Forge pipeline stages with automatic tracing:

```python
"""
StydeAgents/observability/instrument.py
Decorators and context managers for business-logic tracing.
"""
import functools
import time
from typing import Callable, Any
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode


tracer = trace.get_tracer("styde-forge.business")


def traced(name: str | None = None, attributes: dict[str, Any] | None = None):
    """
    Decorator: wrap any function in a span.

    Usage:
        @traced("refinery.execute", {"agent.type": "svelte-component-kit"})
        def execute_agent(agent_config): ...
    """
    def decorator(func: Callable) -> Callable:
        span_name = name or f"{func.__module__}.{func.__qualname__}"

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(span_name) as span:
                if attributes:
                    for k, v in attributes.items():
                        span.set_attribute(k, str(v))
                span.set_attribute("code.function", func.__name__)
                span.set_attribute("code.module", func.__module__)

                try:
                    result = func(*args, **kwargs)
                    span.set_status(Status(StatusCode.OK))
                    return result
                except Exception as exc:
                    span.record_exception(exc)
                    span.set_status(Status(StatusCode.ERROR, str(exc)))
                    raise
        return wrapper
    return decorator


class TracedContext:
    """Context manager for pipeline stages."""

    def __init__(self, stage_name: str, **attributes):
        self.stage_name = stage_name
        self.attributes = attributes
        self._span = None
        self._start = None

    def __enter__(self):
        self._start = time.monotonic()
        self._span = tracer.start_span(self.stage_name)
        for k, v in self.attributes.items():
            self._span.set_attribute(k, str(v))
        return self._span

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._span is None:
            return
        duration_ms = (time.monotonic() - self._start) * 1000
        self._span.set_attribute("duration_ms", duration_ms)

        if exc_type is not None:
            self._span.record_exception(exc_val)
            self._span.set_status(Status(StatusCode.ERROR, str(exc_val)))
        else:
            self._span.set_status(Status(StatusCode.OK))
        self._span.end()


# ── Usage inside ForgeEngine ──────────────────────────────────────────
class ForgeEngine:
    def run_agent_pipeline(self, agent_config: dict) -> dict:
        """Execute a single agent through refinery → production → archive."""
        agent_name = agent_config["name"]

        with TracedContext("pipeline.execute",
                           agent_name=agent_name,
                           agent_stage=agent_config.get("stage", "refinery")):
            # Stage 1: Refinery
            with TracedContext("pipeline.refinery", agent_name=agent_name):
                result = self._run_refinery(agent_config)

            # Stage 2: Production
            with TracedContext("pipeline.production", agent_name=agent_name):
                result = self._run_production(result)

            # Stage 3: Archive
            with TracedContext("pipeline.archive", agent_name=agent_name):
                result = self._run_archive(result)

        return result
```

### 2.4 Context Propagation (Correlation IDs)

Correlation IDs flow automatically through W3C TraceContext headers. Propagate explicitly for async workers:

```python
"""
StydeAgents/observability/context.py
Utilities for explicit context propagation across threads, queues, and async.
"""
from opentelemetry import context, trace, baggage
from opentelemetry.trace.span import INVALID_SPAN


def extract_correlation_headers() -> dict[str, str]:
    """
    Extract current trace context as a dict for manual propagation.
    Use when enqueuing work to a background task queue.
    """
    current_span = trace.get_current_span()
    if current_span is INVALID_SPAN:
        return {}

    span_ctx = current_span.get_span_context()
    return {
        "traceparent": f"00-{span_ctx.trace_id:032x}-{span_ctx.span_id:016x}-{span_ctx.trace_flags:02x}",
        "tracestate": span_ctx.trace_state.to_header() if span_ctx.trace_state else "",
        "correlation_id": baggage.get_baggage("correlation_id", context.get_current()) or "",
    }


def inject_correlation_headers(headers: dict[str, str]) -> None:
    """
    Restore trace context from propagated headers.
    Use inside a background worker before processing.
    """
    from opentelemetry.propagate import extract
    ctx = extract(headers)
    context.attach(ctx)
```

### 2.5 Export Configuration (OTLP)

**docker-compose.yaml** fragment for the OTLP collector + Tempo:

```yaml
# Observability stack — add to existing docker-compose.yml
services:
  # ── OpenTelemetry Collector ──────────────────────────────────────────
  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.102.1
    command: ["--config=/etc/otel-collector-config.yaml"]
    volumes:
      - ./deploy/otel-collector-config.yaml:/etc/otel-collector-config.yaml
    ports:
      - "4317:4317"   # OTLP gRPC
      - "4318:4318"   # OTLP HTTP
      - "8889:8889"   # Prometheus exporter (collector metrics)
    depends_on:
      - tempo
      - loki
      - prometheus

  # ── Tempo (distributed tracing backend) ──────────────────────────────
  tempo:
    image: grafana/tempo:2.5.0
    command: ["-config.file=/etc/tempo.yaml"]
    volumes:
      - ./deploy/tempo.yaml:/etc/tempo.yaml
      - tempo_data:/var/tempo
    ports:
      - "3200:3200"   # Tempo query HTTP

  # ── Loki (log aggregation) ──────────────────────────────────────────
  loki:
    image: grafana/loki:3.1.0
    command: ["-config.file=/etc/loki/loki-config.yaml"]
    volumes:
      - ./deploy/loki-config.yaml:/etc/loki/loki-config.yaml
      - loki_data:/loki
    ports:
      - "3100:3100"

  # ── Prometheus ───────────────────────────────────────────────────────
  prometheus:
    image: prom/prometheus:v2.53.0
    volumes:
      - ./deploy/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./deploy/alerting-rules.yml:/etc/prometheus/alerting-rules.yml
      - ./deploy/runbooks:/etc/prometheus/runbooks
      - prometheus_data:/prometheus
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.path=/prometheus"
      - "--web.enable-remote-write-receiver"
    ports:
      - "9090:9090"

  # ── Alertmanager ────────────────────────────────────────────────────
  alertmanager:
    image: prom/alertmanager:v0.27.0
    volumes:
      - ./deploy/alertmanager.yml:/etc/alertmanager/alertmanager.yml
    ports:
      - "9093:9093"

  # ── Grafana ──────────────────────────────────────────────────────────
  grafana:
    image: grafana/grafana:11.1.0
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_ADMIN_PASSWORD:-admin}
      GF_INSTALL_PLUGINS: grafana-piechart-panel
    volumes:
      - ./deploy/grafana-dashboards:/etc/grafana/provisioning/dashboards
      - ./deploy/grafana-datasources.yml:/etc/grafana/provisioning/datasources/datasources.yml
      - grafana_data:/var/lib/grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus
      - loki
      - tempo

volumes:
  tempo_data:
  loki_data:
  prometheus_data:
  grafana_data:
```

**OTel Collector config** (`deploy/otel-collector-config.yaml`):

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 5s
    send_batch_size: 512
  memory_limiter:
    check_interval: 1s
    limit_mib: 512
  attributes:
    actions:
      - key: deployment.environment
        value: "${DEPLOY_ENV}"
        action: upsert

exporters:
  otlp/tempo:
    endpoint: tempo:4317
    tls:
      insecure: true
  prometheusremotewrite:
    endpoint: "http://prometheus:9090/api/v1/write"
    resource_to_telemetry_conversion:
      enabled: true
  loki:
    endpoint: "http://loki:3100/loki/api/v1/push"
  debug:
    verbosity: detailed

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch, attributes]
      exporters: [otlp/tempo, debug]
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [prometheusremotewrite]
    logs:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [loki, debug]
```

---

## 3. Structured Logging with Correlation IDs

### 3.1 Logger Factory

Use `structlog` for structured, JSON-formatted logs with automatic trace context.

```bash
uv add structlog python-json-logger
```

```python
"""
StydeAgents/observability/logging.py
Structured logging with correlation IDs and OpenTelemetry integration.
"""
import os
import sys
import logging
import structlog
from opentelemetry import trace


def add_trace_context(logger, method_name, event_dict):
    """
    structlog processor: inject trace_id, span_id, and correlation_id
    into every log record automatically.
    """
    span = trace.get_current_span()
    if span is not None:
        ctx = span.get_span_context()
        if ctx.is_valid:
            event_dict["trace_id"] = format(ctx.trace_id, "032x")
            event_dict["span_id"] = format(ctx.span_id, "016x")

    # Extract correlation_id from baggage (set by middleware or caller)
    from opentelemetry import baggage, context
    corr_id = baggage.get_baggage("correlation_id", context.get_current())
    if corr_id:
        event_dict["correlation_id"] = corr_id

    return event_dict


def add_service_context(logger, method_name, event_dict):
    """Inject service identity into every log line."""
    event_dict.setdefault("service", os.getenv("OTEL_SERVICE_NAME", "styde-forge"))
    event_dict.setdefault("environment", os.getenv("DEPLOY_ENV", "development"))
    event_dict.setdefault("instance", os.getenv("FORGE_INSTANCE_ID", "local"))
    return event_dict


def init_logging(
    log_level: str = "INFO",
    json_output: bool = True,
    pretty_print: bool = False,
):
    """
    Initialize structured logging for Styde Forge.

    Args:
        log_level: One of DEBUG, INFO, WARNING, ERROR, CRITICAL
        json_output: Emit JSON (production) vs. colored console (dev)
        pretty_print: Indent JSON for human readability
    """
    # ── Configure standard library logging ───────────────────────────
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Clear existing handlers
    root_logger.handlers.clear()

    if json_output:
        from pythonjsonlogger import jsonlogger
        handler = logging.StreamHandler(sys.stdout)
        fmt = "%(asctime)s %(name)s %(levelname)s %(message)s"
        formatter = jsonlogger.JsonFormatter(
            fmt=fmt,
            timestamp=True,
            json_ensure_ascii=False,
        )
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
    else:
        # Development: colored console output
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)-7s] %(name)s: %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        ))
        root_logger.addHandler(handler)

    # ── Configure structlog ──────────────────────────────────────────
    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        add_trace_context,
        add_service_context,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if json_output:
        structlog.configure(
            processors=shared_processors + [
                structlog.processors.JSONRenderer(
                    sort_keys=True,
                    indent=2 if pretty_print else None,
                ),
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
    else:
        structlog.configure(
            processors=shared_processors + [
                structlog.dev.ConsoleRenderer(colors=True),
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger()


# ── Global logger instance ──────────────────────────────────────────
log = init_logging(
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    json_output=os.getenv("LOG_JSON", "true") == "true",
    pretty_print=os.getenv("LOG_PRETTY", "false") == "true",
)
```

### 3.2 Correlation ID Middleware

Generated at the ingress point (HTTP request, CLI invocation, event) and propagated everywhere:

```python
"""
StydeAgents/observability/middleware.py
HTTP middleware for correlation ID injection and request logging.
"""
import uuid
from opentelemetry import baggage, context


class CorrelationIDMiddleware:
    """
    WSGI/ASGI middleware that:
    1. Reads or generates a correlation_id
    2. Sets it in OpenTelemetry baggage
    3. Attaches it to the response header
    4. Logs every request with timing

    Usage (Flask):
        app.wsgi_app = CorrelationIDMiddleware(app.wsgi_app)
    """

    HEADER_REQUEST_ID = "X-Request-ID"
    HEADER_CORRELATION_ID = "X-Correlation-ID"

    def __init__(self, app, logger=None):
        self.app = app
        self.logger = logger or structlog.get_logger("http")

    def __call__(self, environ, start_response):
        # ── Extract or generate correlation ID ──────────────────────
        correlation_id = (
            environ.get(f"HTTP_{self.HEADER_CORRELATION_ID.replace('-', '_').upper()}")
            or environ.get(f"HTTP_{self.HEADER_REQUEST_ID.replace('-', '_').upper()}")
            or str(uuid.uuid4())
        )

        # ── Inject into OpenTelemetry baggage ───────────────────────
        ctx = baggage.set_baggage("correlation_id", correlation_id)
        token = context.attach(ctx)

        # ── Request logging ─────────────────────────────────────────
        method = environ.get("REQUEST_METHOD", "UNKNOWN")
        path = environ.get("PATH_INFO", "/")
        start = time.monotonic()

        # ── Wrap response to capture status and inject header ───────
        def custom_start_response(status, headers, exc_info=None):
            headers.append((self.HEADER_CORRELATION_ID, correlation_id))
            return start_response(status, headers, exc_info)

        try:
            response = self.app(environ, custom_start_response)
            duration_ms = (time.monotonic() - start) * 1000

            self.logger.info(
                "http.request",
                method=method,
                path=path,
                correlation_id=correlation_id,
                duration_ms=round(duration_ms, 2),
            )
            return response
        except Exception:
            duration_ms = (time.monotonic() - start) * 1000
            self.logger.exception(
                "http.request.error",
                method=method,
                path=path,
                correlation_id=correlation_id,
                duration_ms=round(duration_ms, 2),
            )
            raise
        finally:
            context.detach(token)


# ── CLI correlation ID generator ────────────────────────────────────
def with_correlation_id(func):
    """
    Decorator for CLI commands: generates a correlation_id for the invocation.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        corr_id = str(uuid.uuid4())
        ctx = baggage.set_baggage("correlation_id", corr_id)
        token = context.attach(ctx)
        try:
            log.info("cli.invoke", correlation_id=corr_id, command=func.__name__)
            return func(*args, **kwargs)
        finally:
            context.detach(token)
    return wrapper
```

### 3.3 Log Format & Enrichment

Every log line emitted will look like this (JSON, production):

```json
{
  "timestamp": "2026-06-26T00:08:00.123456Z",
  "level": "info",
  "logger": "styde-forge.refinery",
  "event": "agent.execution.complete",
  "service": "styde-forge",
  "environment": "production",
  "instance": "forge-prod-01",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "correlation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "agent_name": "svelte-component-kit",
  "agent_stage": "refinery",
  "duration_ms": 1234.56,
  "output_size_bytes": 57925
}
```

### 3.4 Integration with OpenTelemetry

The `LoggingInstrumentor` (bootstrapped in Section 2.2) automatically injects `trace_id` and `span_id` into stdlib `logging.LogRecord` objects. Our `add_trace_context` structlog processor does the same for structlog. This means:

- **Every log line is traceable** — search Tempo by trace_id, then jump to correlated logs in Loki.
- **Logs appear as span events** in the trace waterfall (when using `log_to_span=True` in `LoggingInstrumentor`).
- **No manual plumbing** — developers just call `log.info(...)` and get correlation for free.

---

## 4. Prometheus Metrics — RED Method

The **RED Method** (Rate, Errors, Duration) is applied to every service, endpoint, and pipeline stage.

### 4.1 Metric Definitions

```python
"""
StydeAgents/observability/metrics.py
Prometheus metrics — RED Method applied to every service boundary.
"""
from prometheus_client import (
    Counter, Histogram, Gauge, Info, CollectorRegistry, generate_latest,
    CONTENT_TYPE_LATEST,
)
from prometheus_client.exposition import choose_encoder
import os

# ── Registry ────────────────────────────────────────────────────────
REGISTRY = CollectorRegistry(auto_describe=True)

# ── Service Info ────────────────────────────────────────────────────
SERVICE_INFO = Info(
    "styde_forge_service",
    "Service metadata",
    registry=REGISTRY,
)
SERVICE_INFO.info({
    "version": os.getenv("STYDE_FORGE_VERSION", "3.0.0"),
    "environment": os.getenv("DEPLOY_ENV", "development"),
})

# ──── RATE ──────────────────────────────────────────────────────────
# Count of requests/operations per service endpoint
REQUEST_COUNT = Counter(
    "styde_forge_requests_total",
    "Total number of requests processed",
    labelnames=["service", "endpoint", "method", "status_code"],
    registry=REGISTRY,
)

# Pipeline execution count
PIPELINE_EXECUTIONS = Counter(
    "styde_forge_pipeline_executions_total",
    "Total number of pipeline executions",
    labelnames=["agent_name", "stage", "status"],  # status: success|failure
    registry=REGISTRY,
)

# ──── ERRORS ────────────────────────────────────────────────────────
REQUEST_ERRORS = Counter(
    "styde_forge_request_errors_total",
    "Total number of failed requests",
    labelnames=["service", "endpoint", "method", "error_type"],
    registry=REGISTRY,
)

PIPELINE_ERRORS = Counter(
    "styde_forge_pipeline_errors_total",
    "Total number of pipeline failures by error class",
    labelnames=["agent_name", "stage", "error_class"],
    registry=REGISTRY,
)

# ──── DURATION ──────────────────────────────────────────────────────
REQUEST_DURATION = Histogram(
    "styde_forge_request_duration_seconds",
    "Request duration in seconds",
    labelnames=["service", "endpoint", "method"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0],
    registry=REGISTRY,
)

PIPELINE_DURATION = Histogram(
    "styde_forge_pipeline_duration_seconds",
    "Pipeline stage duration in seconds",
    labelnames=["agent_name", "stage"],
    buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0, 600.0],
    registry=REGISTRY,
)

# ──── SLO BURN RATE (supplementary) ─────────────────────────────────
SLO_BURN_RATE = Gauge(
    "styde_forge_slo_burn_rate",
    "Error budget burn rate (multiplier over baseline)",
    labelnames=["service", "window"],  # window: 1h, 6h, 24h
    registry=REGISTRY,
)

# ──── SYSTEM HEALTH ─────────────────────────────────────────────────
AGENTS_ACTIVE = Gauge(
    "styde_forge_agents_active",
    "Number of agents currently in each stage",
    labelnames=["stage"],  # refinery, production, archive
    registry=REGISTRY,
)

FORGE_QUEUE_DEPTH = Gauge(
    "styde_forge_queue_depth",
    "Number of items waiting in the forge queue",
    labelnames=["queue_name"],
    registry=REGISTRY,
)

EVALUATION_SCORE = Histogram(
    "styde_forge_evaluation_score",
    "Composite evaluation scores over time",
    buckets=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    registry=REGISTRY,
)
```

### 4.2 Instrumentation Decorators

```python
"""
StydeAgents/observability/metrics_decorators.py
Drop-in decorators to instrument any function with RED metrics.
"""
import time
import functools
from typing import Callable
from .metrics import (
    REQUEST_COUNT, REQUEST_ERRORS, REQUEST_DURATION,
    PIPELINE_EXECUTIONS, PIPELINE_ERRORS, PIPELINE_DURATION,
)


def red_http(service: str, endpoint: str, method: str = "GET"):
    """
    Decorator for HTTP handlers: records Rate, Errors, Duration.

    Usage:
        @app.route("/api/agents")
        @red_http("api", "/api/agents", "GET")
        def list_agents(): ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.monotonic()
            try:
                result = func(*args, **kwargs)
                duration = time.monotonic() - start

                # Extract status code from result (Flask tuple)
                status_code = "200"
                if isinstance(result, tuple):
                    status_code = str(result[1])

                REQUEST_COUNT.labels(
                    service=service,
                    endpoint=endpoint,
                    method=method,
                    status_code=status_code,
                ).inc()
                REQUEST_DURATION.labels(
                    service=service,
                    endpoint=endpoint,
                    method=method,
                ).observe(duration)

                return result
            except Exception as exc:
                duration = time.monotonic() - start
                error_type = type(exc).__name__

                REQUEST_COUNT.labels(
                    service=service,
                    endpoint=endpoint,
                    method=method,
                    status_code="500",
                ).inc()
                REQUEST_ERRORS.labels(
                    service=service,
                    endpoint=endpoint,
                    method=method,
                    error_type=error_type,
                ).inc()
                REQUEST_DURATION.labels(
                    service=service,
                    endpoint=endpoint,
                    method=method,
                ).observe(duration)
                raise
        return wrapper
    return decorator


def red_pipeline(agent_name: str, stage: str):
    """
    Decorator for pipeline stages: records RED metrics per agent/stage.

    Usage:
        @red_pipeline("svelte-component-kit", "refinery")
        def run_refinery(config): ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.monotonic()
            try:
                result = func(*args, **kwargs)
                duration = time.monotonic() - start

                PIPELINE_EXECUTIONS.labels(
                    agent_name=agent_name,
                    stage=stage,
                    status="success",
                ).inc()
                PIPELINE_DURATION.labels(
                    agent_name=agent_name,
                    stage=stage,
                ).observe(duration)

                return result
            except Exception as exc:
                duration = time.monotonic() - start

                PIPELINE_EXECUTIONS.labels(
                    agent_name=agent_name,
                    stage=stage,
                    status="failure",
                ).inc()
                PIPELINE_ERRORS.labels(
                    agent_name=agent_name,
                    stage=stage,
                    error_class=type(exc).__name__,
                ).inc()
                PIPELINE_DURATION.labels(
                    agent_name=agent_name,
                    stage=stage,
                ).observe(duration)
                raise
        return wrapper
    return decorator
```

### 4.3 Metrics Endpoint

Expose Prometheus metrics at `GET /metrics`:

```python
"""
Core/metrics_handler.py
HTTP handler for Prometheus metrics scraping.
"""
from http.server import BaseHTTPRequestHandler
from StydeAgents.observability.metrics import REGISTRY, generate_latest, CONTENT_TYPE_LATEST


class MetricsHandler(BaseHTTPRequestHandler):
    """Standalone metrics endpoint for Prometheus scraping."""

    def do_GET(self):
        if self.path == "/metrics":
            data = generate_latest(REGISTRY)
            self.send_response(200)
            self.send_header("Content-Type", CONTENT_TYPE_LATEST)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "healthy"}')
        else:
            self.send_response(404)
            self.end_headers()


def start_metrics_server(port: int = 9091):
    """Start a lightweight HTTP server for /metrics and /health."""
    from http.server import HTTPServer
    import threading

    server = HTTPServer(("0.0.0.0", port), MetricsHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server
```

**Prometheus scrape config** (`deploy/prometheus.yml`):

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    environment: "${DEPLOY_ENV:-development}"

rule_files:
  - "/etc/prometheus/alerting-rules.yml"

scrape_configs:
  - job_name: "styde-forge"
    scrape_interval: 10s
    static_configs:
      - targets: ["forge:9091"]
        labels:
          service: "styde-forge"

  - job_name: "otel-collector"
    scrape_interval: 15s
    static_configs:
      - targets: ["otel-collector:8889"]

  - job_name: "prometheus"
    scrape_interval: 10s
    static_configs:
      - targets: ["localhost:9090"]
```

### 4.4 Exemplar Injection

Link Prometheus metrics to trace IDs via exemplars:

```python
"""
Augment the RED decorator to include trace exemplars.
This allows "click to trace" from Grafana dashboards.
"""
from opentelemetry import trace


def _get_trace_exemplar() -> dict[str, str] | None:
    """Return current trace_id as a Prometheus exemplar, if available."""
    span = trace.get_current_span()
    if span is None:
        return None
    ctx = span.get_span_context()
    if not ctx.is_valid:
        return None
    return {"trace_id": format(ctx.trace_id, "032x")}


# Inside the red_http decorator, before .observe():
# exemplar = _get_trace_exemplar()
# if exemplar:
#     REQUEST_DURATION.labels(...).observe(duration, exemplar=exemplar)
# else:
#     REQUEST_DURATION.labels(...).observe(duration)
```

---

## 5. Grafana Dashboard JSON

### 5.1 Dashboard Structure

| Row | Title | Panels | Data Source |
|-----|-------|--------|-------------|
| 1 | **RED: HTTP Overview** | Request Rate, Error Rate, P50/P95/P99 Latency | Prometheus |
| 2 | **RED: Pipeline Health** | Pipeline Executions, Pipeline Errors, Pipeline Duration by Stage | Prometheus |
| 3 | **Agent Lifecycle** | Agents by Stage (gauge), Queue Depth, Evaluation Scores | Prometheus |
| 4 | **SLO Burn Rate** | Error budget burn rate (1h/6h/24h), remaining budget | Prometheus |
| 5 | **Traces** | Trace search links, slowest traces table | Tempo |
| 6 | **Logs** | Log volume, error log rate, recent errors table | Loki |
| 7 | **System** | CPU, memory, GC stats, open file descriptors | Prometheus |

### 5.2 Full Dashboard JSON

Save as `deploy/grafana-dashboards/styde-forge-observability.json`:

```json
{
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": { "type": "grafana", "uid": "-- Grafana --" },
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "target": { "limit": 100 },
        "type": "dashboard"
      }
    ]
  },
  "editable": true,
  "fiscalYearStartMonth": 0,
  "graphTooltip": 1,
  "id": null,
  "links": [],
  "panels": [
    {
      "collapsed": false,
      "gridPos": { "h": 1, "w": 24, "x": 0, "y": 0 },
      "id": 100,
      "panels": [],
      "title": "🔥 RED: HTTP Service Overview",
      "type": "row"
    },
    {
      "datasource": { "type": "prometheus", "uid": "prometheus" },
      "fieldConfig": {
        "defaults": {
          "color": { "mode": "palette-classic" },
          "custom": {
            "axisBorderShow": false,
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "requests / sec",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "line",
            "fillOpacity": 10,
            "gradientMode": "opacity",
            "hideFrom": { "legend": false, "tooltip": false, "viz": false },
            "insertNulls": false,
            "lineInterpolation": "smooth",
            "lineWidth": 2,
            "pointSize": 5,
            "scaleDistribution": { "type": "linear" },
            "showPoints": "auto",
            "spanNulls": false,
            "stacking": { "group": "A", "mode": "none" },
            "thresholdsStyle": { "mode": "off" }
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              { "color": "green", "value": null },
              { "color": "red", "value": 80 }
            ]
          },
          "unit": "reqps"
        },
        "overrides": []
      },
      "gridPos": { "h": 8, "w": 8, "x": 0, "y": 1 },
      "id": 1,
      "options": { "legend": { "calcs": ["mean", "max"], "displayMode": "table", "placement": "bottom", "showLegend": true }, "tooltip": { "mode": "multi", "sort": "desc" } },
      "targets": [
        {
          "datasource": { "type": "prometheus", "uid": "prometheus" },
          "editorMode": "code",
          "expr": "sum(rate(styde_forge_requests_total{status_code=~\"2..\"}[5m])) by (endpoint)",
          "legendFormat": "{{endpoint}}",
          "range": true,
          "refId": "A"
        }
      ],
      "title": "📈 Request Rate (2xx)",
      "type": "timeseries"
    },
    {
      "datasource": { "type": "prometheus", "uid": "prometheus" },
      "fieldConfig": {
        "defaults": {
          "color": { "mode": "thresholds" },
          "custom": {
            "axisBorderShow": false,
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "errors / sec",
            "axisPlacement": "auto",
            "drawStyle": "line",
            "fillOpacity": 20,
            "gradientMode": "opacity",
            "hideFrom": { "legend": false, "tooltip": false, "viz": false },
            "lineInterpolation": "smooth",
            "lineWidth": 2,
            "pointSize": 5,
            "scaleDistribution": { "type": "linear" },
            "showPoints": "auto",
            "spanNulls": false,
            "stacking": { "group": "A", "mode": "none" },
            "thresholdsStyle": { "mode": "line+area" }
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              { "color": "green", "value": null },
              { "color": "yellow", "value": 0.1 },
              { "color": "red", "value": 1.0 }
            ]
          },
          "unit": "reqps"
        },
        "overrides": []
      },
      "gridPos": { "h": 8, "w": 8, "x": 8, "y": 1 },
      "id": 2,
      "options": { "legend": { "calcs": ["mean", "max"], "displayMode": "table", "placement": "bottom", "showLegend": true }, "tooltip": { "mode": "multi", "sort": "desc" } },
      "targets": [
        {
          "datasource": { "type": "prometheus", "uid": "prometheus" },
          "editorMode": "code",
          "expr": "sum(rate(styde_forge_request_errors_total[5m])) by (endpoint, error_type)",
          "legendFormat": "{{endpoint}} - {{error_type}}",
          "range": true,
          "refId": "A"
        }
      ],
      "title": "⚠️ Error Rate",
      "type": "timeseries"
    },
    {
      "datasource": { "type": "prometheus", "uid": "prometheus" },
      "fieldConfig": {
        "defaults": {
          "color": { "mode": "palette-classic" },
          "custom": {
            "axisBorderShow": false,
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "seconds",
            "axisPlacement": "auto",
            "drawStyle": "line",
            "fillOpacity": 5,
            "gradientMode": "none",
            "hideFrom": { "legend": false, "tooltip": false, "viz": false },
            "lineInterpolation": "smooth",
            "lineWidth": 2,
            "pointSize": 5,
            "scaleDistribution": { "type": "linear" },
            "showPoints": "never",
            "spanNulls": false,
            "stacking": { "group": "A", "mode": "none" },
            "thresholdsStyle": { "mode": "off" }
          },
          "mappings": [],
          "thresholds": { "mode": "absolute", "steps": [{ "color": "green", "value": null }] },
          "unit": "s"
        },
        "overrides": [
          { "matcher": { "id": "byName", "options": "p50" }, "properties": [{ "id": "custom.lineStyle", "value": { "dash": [10, 5], "fill": "dash" } }] },
          { "matcher": { "id": "byName", "options": "p95" }, "properties": [{ "id": "custom.lineStyle", "value": { "dash": [3, 2], "fill": "dot" } }] },
          { "matcher": { "id": "byName", "options": "p99" }, "properties": [{ "id": "custom.lineWidth", "value": 1 }] }
        ]
      },
      "gridPos": { "h": 8, "w": 8, "x": 16, "y": 1 },
      "id": 3,
      "options": { "legend": { "calcs": [], "displayMode": "list", "placement": "bottom", "showLegend": true }, "tooltip": { "mode": "multi", "sort": "desc" } },
      "targets": [
        {
          "datasource": { "type": "prometheus", "uid": "prometheus" },
          "editorMode": "code",
          "expr": "histogram_quantile(0.50, sum(rate(styde_forge_request_duration_seconds_bucket[5m])) by (le, endpoint))",
          "legendFormat": "{{endpoint}} p50",
          "range": true,
          "refId": "A"
        },
        {
          "datasource": { "type": "prometheus", "uid": "prometheus" },
          "editorMode": "code",
          "expr": "histogram_quantile(0.95, sum(rate(styde_forge_request_duration_seconds_bucket[5m])) by (le, endpoint))",
          "legendFormat": "{{endpoint}} p95",
          "range": true,
          "refId": "B"
        },
        {
          "datasource": { "type": "prometheus", "uid": "prometheus" },
          "editorMode": "code",
          "expr": "histogram_quantile(0.99, sum(rate(styde_forge_request_duration_seconds_bucket[5m])) by (le, endpoint))",
          "legendFormat": "{{endpoint}} p99",
          "range": true,
          "refId": "C"
        }
      ],
      "title": "⏱️ Request Duration (p50/p95/p99)",
      "type": "timeseries"
    },
    {
      "collapsed": false,
      "gridPos": { "h": 1, "w": 24, "x": 0, "y": 9 },
      "id": 200,
      "panels": [],
      "title": "⚙️ RED: Forge Pipeline Health",
      "type": "row"
    },
    {
      "datasource": { "type": "prometheus", "uid": "prometheus" },
      "fieldConfig": {
        "defaults": {
          "color": { "mode": "palette-classic" },
          "custom": {
            "axisBorderShow": false,
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "line",
            "fillOpacity": 10,
            "gradientMode": "opacity",
            "hideFrom": { "legend": false, "tooltip": false, "viz": false },
            "lineInterpolation": "smooth",
            "lineWidth": 2,
            "pointSize": 5,
            "scaleDistribution": { "type": "linear" },
            "showPoints": "auto",
            "spanNulls": false,
            "stacking": { "group": "A", "mode": "none" },
            "thresholdsStyle": { "mode": "off" }
          },
          "mappings": [],
          "thresholds": { "mode": "absolute", "steps": [{ "color": "green", "value": null }] },
          "unit": "short"
        },
        "overrides": []
      },
      "gridPos": { "h": 8, "w": 12, "x": 0, "y": 10 },
      "id": 201,
      "options": { "legend": { "calcs": ["mean"], "displayMode": "table", "placement": "bottom", "showLegend": true }, "tooltip": { "mode": "multi", "sort": "desc" } },
      "targets": [
        {
          "datasource": { "type": "prometheus", "uid": "prometheus" },
          "editorMode": "code",
          "expr": "sum(rate(styde_forge_pipeline_executions_total{status=\"success\"}[15m])) by (agent_name, stage)",
          "legendFormat": "{{agent_name}} / {{stage}}",
          "range": true,
          "refId": "A"
        }
      ],
      "title": "📦 Pipeline Execution Rate (success)",
      "type": "timeseries"
    },
    {
      "datasource": { "type": "prometheus", "uid": "prometheus" },
      "fieldConfig": {
        "defaults": {
          "color": { "mode": "thresholds" },
          "custom": {
            "axisBorderShow": false,
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "drawStyle": "line",
            "fillOpacity": 20,
            "gradientMode": "opacity",
            "hideFrom": { "legend": false, "tooltip": false, "viz": false },
            "lineInterpolation": "smooth",
            "lineWidth": 2,
            "pointSize": 5,
            "scaleDistribution": { "type": "linear" },
            "showPoints": "auto",
            "spanNulls": false,
            "stacking": { "group": "A", "mode": "none" },
            "thresholdsStyle": { "mode": "line+area" }
          },
          "mappings": [],
          "thresholds": { "mode": "absolute", "steps": [{ "color": "green", "value": null }, { "color": "red", "value": 0.5 }] },
          "unit": "short"
        },
        "overrides": []
      },
      "gridPos": { "h": 8, "w": 12, "x": 12, "y": 10 },
      "id": 202,
      "options": { "legend": { "calcs": [], "displayMode": "table", "placement": "bottom", "showLegend": true }, "tooltip": { "mode": "multi", "sort": "desc" } },
      "targets": [
        {
          "datasource": { "type": "prometheus", "uid": "prometheus" },
          "editorMode": "code",
          "expr": "sum(rate(styde_forge_pipeline_errors_total[15m])) by (agent_name, error_class)",
          "legendFormat": "{{agent_name}} - {{error_class}}",
          "range": true,
          "refId": "A"
        }
      ],
      "title": "🐛 Pipeline Errors by Agent",
      "type": "timeseries"
    },
    {
      "datasource": { "type": "prometheus", "uid": "prometheus" },
      "fieldConfig": {
        "defaults": {
          "color": { "mode": "palette-classic" },
          "custom": {
            "axisBorderShow": false,
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "seconds",
            "axisPlacement": "auto",
            "drawStyle": "line",
            "fillOpacity": 5,
            "gradientMode": "none",
            "hideFrom": { "legend": false, "tooltip": false, "viz": false },
            "lineInterpolation": "smooth",
            "lineWidth": 2,
            "pointSize": 5,
            "scaleDistribution": { "type": "linear" },
            "showPoints": "never",
            "spanNulls": false,
            "stacking": { "group": "A", "mode": "none" },
            "thresholdsStyle": { "mode": "off" }
          },
          "mappings": [],
          "min": 0,
          "thresholds": { "mode": "absolute", "steps": [{ "color": "green", "value": null }] },
          "unit": "s"
        },
        "overrides": []
      },
      "gridPos": { "h": 8, "w": 12, "x": 0, "y": 18 },
      "id": 203,
      "options": { "legend": { "calcs": ["mean", "max"], "displayMode": "table", "placement": "bottom", "showLegend": true }, "tooltip": { "mode": "multi", "sort": "desc" } },
      "targets": [
        {
          "datasource": { "type": "prometheus", "uid": "prometheus" },
          "editorMode": "code",
          "expr": "histogram_quantile(0.95, sum(rate(styde_forge_pipeline_duration_seconds_bucket[15m])) by (le, agent_name, stage))",
          "legendFormat": "{{agent_name}} / {{stage}} (p95)",
          "range": true,
          "refId": "A"
        }
      ],
      "title": "⏱️ Pipeline Duration (p95) by Stage",
      "type": "timeseries"
    },
    {
      "datasource": { "type": "prometheus", "uid": "prometheus" },
      "fieldConfig": {
        "defaults": {
          "color": { "mode": "thresholds" },
          "mappings": [],
          "max": 100,
          "min": 0,
          "thresholds": {
            "mode": "absolute",
            "steps": [
              { "color": "green", "value": null },
              { "color": "yellow", "value": 60 },
              { "color": "orange", "value": 80 },
              { "color": "red", "value": 95 }
            ]
          },
          "unit": "percent"
        },
        "overrides": []
      },
      "gridPos": { "h": 8, "w": 6, "x": 12, "y": 18 },
      "id": 204,
      "options": { "orientation": "auto", "reduceOptions": { "values": false, "calcs": ["lastNotNull"] }, "showThresholdLabels": false, "showThresholdMarkers": true, "text": {} },
      "targets": [
        {
          "datasource": { "type": "prometheus", "uid": "prometheus" },
          "editorMode": "code",
          "expr": "sum(rate(styde_forge_pipeline_executions_total{status=\"success\"}[30m])) / sum(rate(styde_forge_pipeline_executions_total[30m])) * 100",
          "refId": "A"
        }
      ],
      "title": "🏆 Pipeline Success Rate (30m)",
      "type": "gauge"
    },
    {
      "datasource": { "type": "prometheus", "uid": "prometheus" },
      "fieldConfig": {
        "defaults": {
          "color": { "mode": "thresholds" },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              { "color": "green", "value": null },
              { "color": "yellow", "value": 1 },
              { "color": "orange", "value": 5 },
              { "color": "red", "value": 10 }
            ]
          },
          "unit": "short"
        },
        "overrides": [
          { "matcher": { "id": "byName", "options": "1h burn rate" }, "properties": [{ "id": "thresholds", "value": { "mode": "absolute", "steps": [{ "color": "green", "value": null }, { "color": "yellow", "value": 14.4 }, { "color": "red", "value": 100 }] } }] },
          { "matcher": { "id": "byName", "options": "6h burn rate" }, "properties": [{ "id": "thresholds", "value": { "mode": "absolute", "steps": [{ "color": "green", "value": null }, { "color": "yellow", "value": 6 }, { "color": "red", "value": 100 }] } }] }
        ]
      },
      "gridPos": { "h": 8, "w": 6, "x": 18, "y": 18 },
      "id": 205,
      "options": { "colorMode": "background", "graphMode": "area", "justifyMode": "auto", "orientation": "horizontal", "percentChangeColorMode": "standard", "reduceOptions": { "values": false, "calcs": ["lastNotNull"] }, "showPercentChange": false, "text": {}, "textMode": "auto", "wideLayout": true },
      "targets": [
        {
          "datasource": { "type": "prometheus", "uid": "prometheus" },
          "editorMode": "code",
          "expr": "styde_forge_slo_burn_rate{service=\"pipeline\", window=\"1h\"}",
          "refId": "A"
        },
        {
          "datasource": { "type": "prometheus", "uid": "prometheus" },
          "editorMode": "code",
          "expr": "styde_forge_slo_burn_rate{service=\"pipeline\", window=\"6h\"}",
          "refId": "B"
        }
      ],
      "title": "🔥 SLO Burn Rate",
      "type": "stat"
    },
    {
      "collapsed": false,
      "gridPos": { "h": 1, "w": 24, "x": 0, "y": 26 },
      "id": 300,
      "panels": [],
      "title": "🤖 Agent Lifecycle & System Health",
      "type": "row"
    },
    {
      "datasource": { "type": "prometheus", "uid": "prometheus" },
      "fieldConfig": {
        "defaults": {
          "color": { "mode": "palette-classic" },
          "custom": { "hideFrom": { "legend": false, "tooltip": false, "viz": false } },
          "mappings": [],
          "unit": "short"
        },
        "overrides": []
      },
      "gridPos": { "h": 8, "w": 8, "x": 0, "y": 27 },
      "id": 301,
      "options": { "displayLabels": ["name", "value"], "legend": { "displayMode": "table", "placement": "right", "showLegend": true, "values": ["value"] }, "pieType": "donut", "reduceOptions": { "values": false, "calcs": ["lastNotNull"] }, "tooltip": { "mode": "single", "sort": "none" } },
      "targets": [
        {
          "datasource": { "type": "prometheus", "uid": "prometheus" },
          "editorMode": "code",
          "expr": "styde_forge_agents_active",
          "legendFormat": "{{stage}}",
          "refId": "A"
        }
      ],
      "title": "🗂️ Agents by Stage",
      "type": "piechart"
    },
    {
      "datasource": { "type": "prometheus", "uid": "prometheus" },
      "fieldConfig": {
        "defaults": {
          "color": { "mode": "palette-classic" },
          "custom": {
            "axisBorderShow": false,
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "count",
            "axisPlacement": "auto",
            "drawStyle": "line",
            "fillOpacity": 10,
            "gradientMode": "opacity",
            "hideFrom": { "legend": false, "tooltip": false, "viz": false },
            "lineInterpolation": "smooth",
            "lineWidth": 2,
            "pointSize": 5,
            "scaleDistribution": { "type": "linear" },
            "showPoints": "auto",
            "spanNulls": false,
            "stacking": { "group": "A", "mode": "none" },
            "thresholdsStyle": { "mode": "line+area" }
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              { "color": "green", "value": null },
              { "color": "yellow", "value": 10 },
              { "color": "red", "value": 50 }
            ]
          },
          "unit": "short"
        },
        "overrides": []
      },
      "gridPos": { "h": 8, "w": 8, "x": 8, "y": 27 },
      "id": 302,
      "options": { "legend": { "calcs": ["lastNotNull", "max"], "displayMode": "table", "placement": "bottom", "showLegend": true }, "tooltip": { "mode": "multi", "sort": "desc" } },
      "targets": [
        {
          "datasource": { "type": "prometheus", "uid": "prometheus" },
          "editorMode": "code",
          "expr": "styde_forge_queue_depth",
          "legendFormat": "{{queue_name}}",
          "refId": "A"
        }
      ],
      "title": "📊 Forge Queue Depth",
      "type": "timeseries"
    },
    {
      "datasource": { "type": "prometheus", "uid": "prometheus" },
      "fieldConfig": {
        "defaults": {
          "color": { "mode": "thresholds" },
          "custom": {
            "axisBorderShow": false,
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "axisSoftMin": 0,
            "barAlignment": 0,
            "drawStyle": "line",
            "fillOpacity": 0,
            "gradientMode": "none",
            "hideFrom": { "legend": false, "tooltip": false, "viz": false },
            "lineInterpolation": "linear",
            "lineWidth": 1,
            "pointSize": 5,
            "scaleDistribution": { "type": "linear", "log": 2 },
            "showPoints": "auto",
            "spanNulls": false,
            "stacking": { "group": "A", "mode": "none" },
            "thresholdsStyle": { "mode": "off" }
          },
          "mappings": [],
          "max": 100,
          "min": 0,
          "thresholds": { "mode": "absolute", "steps": [{ "color": "green", "value": null }] },
          "unit": "none"
        },
        "overrides": []
      },
      "gridPos": { "h": 8, "w": 8, "x": 16, "y": 27 },
      "id": 303,
      "options": { "legend": { "calcs": ["mean", "lastNotNull"], "displayMode": "table", "placement": "bottom", "showLegend": true }, "tooltip": { "mode": "multi", "sort": "desc" } },
      "targets": [
        {
          "datasource": { "type": "prometheus", "uid": "prometheus" },
          "editorMode": "code",
          "expr": "histogram_quantile(0.50, rate(styde_forge_evaluation_score_bucket[15m]))",
          "legendFormat": "p50 evaluation score",
          "refId": "A"
        },
        {
          "datasource": { "type": "prometheus", "uid": "prometheus" },
          "editorMode": "code",
          "expr": "histogram_quantile(0.95, rate(styde_forge_evaluation_score_bucket[15m]))",
          "legendFormat": "p95 evaluation score",
          "refId": "B"
        }
      ],
      "title": "🎯 Agent Evaluation Scores",
      "type": "timeseries"
    },
    {
      "collapsed": false,
      "gridPos": { "h": 1, "w": 24, "x": 0, "y": 35 },
      "id": 400,
      "panels": [],
      "title": "🔍 Traces & Logs",
      "type": "row"
    },
    {
      "datasource": { "type": "tempo", "uid": "tempo" },
      "gridPos": { "h": 10, "w": 12, "x": 0, "y": 36 },
      "id": 401,
      "options": {},
      "targets": [
        {
          "datasource": { "type": "tempo", "uid": "tempo" },
          "queryType": "search",
          "refId": "A",
          "serviceName": "styde-forge",
          "spanName": "",
          "limit": 20,
          "minDuration": "100ms",
          "maxDuration": ""
        }
      ],
      "title": "🐢 Slowest Traces (>100ms)",
      "type": "traces"
    },
    {
      "datasource": { "type": "loki", "uid": "loki" },
      "fieldConfig": {
        "defaults": {
          "color": { "mode": "thresholds" },
          "custom": {
            "align": "auto",
            "cellOptions": { "type": "auto" },
            "filterable": true,
            "inspect": false
          },
          "mappings": [],
          "thresholds": { "mode": "absolute", "steps": [{ "color": "green", "value": null }] }
        },
        "overrides": []
      },
      "gridPos": { "h": 10, "w": 12, "x": 12, "y": 36 },
      "id": 402,
      "options": { "cellHeight": "sm", "footer": { "countRows": false, "fields": "", "reducer": ["sum"], "show": false } },
      "targets": [
        {
          "datasource": { "type": "loki", "uid": "loki" },
          "editorMode": "code",
          "expr": "{service=\"styde-forge\"} | json | level=~\"ERROR|CRITICAL\" | line_format \"{{.event}}: {{.error_message}}\"",
          "refId": "A"
        }
      ],
      "title": "📋 Recent Errors (Loki)",
      "type": "table"
    }
  ],
  "refresh": "30s",
  "schemaVersion": 39,
  "tags": ["styde-forge", "observability", "slo"],
  "templating": {
    "list": [
      {
        "current": { "selected": false, "text": "production", "value": "production" },
        "datasource": { "type": "prometheus", "uid": "prometheus" },
        "definition": "label_values(styde_forge_service, environment)",
        "hide": 0,
        "includeAll": false,
        "label": "Environment",
        "multi": false,
        "name": "environment",
        "options": [],
        "query": { "qryType": 1, "query": "label_values(styde_forge_service, environment)", "refId": "PrometheusVariableQueryEditor-VariableQuery" },
        "refresh": 1,
        "regex": "",
        "skipUrlSync": false,
        "sort": 0,
        "type": "query"
      }
    ]
  },
  "time": { "from": "now-1h", "to": "now" },
  "timepicker": {},
  "timezone": "browser",
  "title": "Styde Forge — Observability Dashboard",
  "uid": "styde-forge-observability",
  "version": 1,
  "weekStart": ""
}
```

**Grafana datasource provisioning** (`deploy/grafana-datasources.yml`):

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    uid: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    jsonData:
      timeInterval: "15s"
      exemplarTraceIdDestinations:
        - name: trace_id
          datasourceUid: tempo

  - name: Tempo
    type: tempo
    uid: tempo
    access: proxy
    url: http://tempo:3200
    jsonData:
      tracesToLogsV2:
        datasourceUid: loki
        spanStartTimeShift: "-1h"
        spanEndTimeShift: "1h"
        filterByTraceID: true
        filterBySpanID: false
        tags: [{ key: "service.name", value: "service" }]
      nodeGraph:
        enabled: true
      search:
        hide: false

  - name: Loki
    type: loki
    uid: loki
    access: proxy
    url: http://loki:3100
    jsonData:
      derivedFields:
        - name: trace_id
          matcherRegex: '"trace_id":"([a-f0-9]{32})"'
          url: '$${__value.raw}'
          datasourceUid: tempo
```

---

## 6. Alerting Rules with Runbooks

### 6.1 Alert Definitions

**`deploy/alerting-rules.yml`**:

```yaml
groups:
  # ──────────────────────────────────────────────────────────────────────
  # GROUP: RED Alerts (Rate, Errors, Duration)
  # ──────────────────────────────────────────────────────────────────────
  - name: styde_forge_red
    interval: 30s
    rules:

      # ── HIGH ERROR RATE ──────────────────────────────────────────
      - alert: HighHTTPErrorRate
        expr: |
          sum(rate(styde_forge_request_errors_total[5m])) by (service, endpoint)
          /
          sum(rate(styde_forge_requests_total[5m])) by (service, endpoint)
          > 0.05
        for: 5m
        labels:
          severity: critical
          category: red
          runbook: "runbooks/high-http-error-rate.md"
        annotations:
          summary: "High HTTP error rate on {{ $labels.endpoint }}"
          description: >
            Service {{ $labels.service }} endpoint {{ $labels.endpoint }}
            has an error rate of {{ $value | humanizePercentage }}
            over the last 5 minutes.
          dashboard: "styde-forge-observability"
          panel_ids: "2"

      # ── ELEVATED LATENCY ─────────────────────────────────────────
      - alert: HighHTTPLatency
        expr: |
          histogram_quantile(0.99,
            sum(rate(styde_forge_request_duration_seconds_bucket[5m])) by (le, endpoint)
          ) > 5.0
        for: 10m
        labels:
          severity: warning
          category: red
          runbook: "runbooks/high-http-latency.md"
        annotations:
          summary: "High P99 latency on {{ $labels.endpoint }}"
          description: >
            Endpoint {{ $labels.endpoint }} has P99 latency of
            {{ $value | humanizeDuration }} over the last 10 minutes
            (threshold: 5s).
          dashboard: "styde-forge-observability"
          panel_ids: "3"

      # ── PIPELINE FAILURE RATE ────────────────────────────────────
      - alert: HighPipelineFailureRate
        expr: |
          sum(rate(styde_forge_pipeline_errors_total[15m])) by (agent_name)
          /
          (
            sum(rate(styde_forge_pipeline_executions_total[15m])) by (agent_name)
            > 0
          )
          > 0.10
        for: 10m
        labels:
          severity: critical
          category: pipeline
          runbook: "runbooks/high-pipeline-failure-rate.md"
        annotations:
          summary: "High pipeline failure rate for agent {{ $labels.agent_name }}"
          description: >
            Agent {{ $labels.agent_name }} has a pipeline failure rate
            of {{ $value | humanizePercentage }} over the last 15 minutes.
          dashboard: "styde-forge-observability"
          panel_ids: "202,204"

      # ── PIPELINE TIMEOUT ─────────────────────────────────────────
      - alert: PipelineTimeout
        expr: |
          histogram_quantile(0.99,
            sum(rate(styde_forge_pipeline_duration_seconds_bucket[15m])) by (le, agent_name, stage)
          ) > 300
        for: 15m
        labels:
          severity: warning
          category: pipeline
          runbook: "runbooks/pipeline-timeout.md"
        annotations:
          summary: "Pipeline stage {{ $labels.stage }} is slow for {{ $labels.agent_name }}"
          description: >
            Agent {{ $labels.agent_name }} stage {{ $labels.stage }}
            has P99 duration of {{ $value | humanizeDuration }}
            (threshold: 5 minutes).
          dashboard: "styde-forge-observability"
          panel_ids: "203"

  # ──────────────────────────────────────────────────────────────────────
  # GROUP: SLO & Error Budget
  # ──────────────────────────────────────────────────────────────────────
  - name: styde_forge_slo
    interval: 60s
    rules:

      - alert: ErrorBudgetBurnRateHigh
        expr: |
          styde_forge_slo_burn_rate{window="1h"} > 14.4
          or
          styde_forge_slo_burn_rate{window="6h"} > 6.0
        for: 5m
        labels:
          severity: critical
          category: slo
          runbook: "runbooks/error-budget-burn.md"
        annotations:
          summary: "Error budget is burning too fast"
          description: >
            Burn rate: {{ $value }}x baseline. The 30-day error budget
            will be exhausted in hours at this rate.
            Service: {{ $labels.service }}, Window: {{ $labels.window }}.
          dashboard: "styde-forge-observability"
          panel_ids: "205"

      - alert: ErrorBudgetExhausted
        expr: |
          (
            1 - (
              sum(rate(styde_forge_pipeline_executions_total{status="success"}[30d]))
              /
              sum(rate(styde_forge_pipeline_executions_total[30d]))
            )
          ) > 0.01
        for: 5m
        labels:
          severity: critical
          category: slo
          runbook: "runbooks/error-budget-exhausted.md"
        annotations:
          summary: "Error budget exhausted for the rolling 30-day window"
          description: >
            Pipeline success rate has dropped below the 99% SLO target
            over the rolling 30-day window.
          dashboard: "styde-forge-observability"
          panel_ids: "204,205"

  # ──────────────────────────────────────────────────────────────────────
  # GROUP: System Health
  # ──────────────────────────────────────────────────────────────────────
  - name: styde_forge_system
    interval: 30s
    rules:

      - alert: ForgeInstanceDown
        expr: up{job="styde-forge"} == 0
        for: 2m
        labels:
          severity: critical
          category: infrastructure
          runbook: "runbooks/forge-instance-down.md"
        annotations:
          summary: "Styde Forge instance is DOWN"
          description: >
            Prometheus cannot scrape metrics from the forge instance.
            Instance may be crashed or unreachable.
          dashboard: "styde-forge-observability"

      - alert: QueueBacklogGrowing
        expr: styde_forge_queue_depth > 50
        for: 15m
        labels:
          severity: warning
          category: capacity
          runbook: "runbooks/queue-backlog.md"
        annotations:
          summary: "Forge queue depth exceeds 50 items"
          description: >
            Queue {{ $labels.queue_name }} has {{ $value }} items
            waiting. Check pipeline throughput and agent processing speed.
          dashboard: "styde-forge-observability"
          panel_ids: "302"

      - alert: HighMemoryUsage
        expr: process_resident_memory_bytes{job="styde-forge"} / 1e9 > 4
        for: 10m
        labels:
          severity: warning
          category: infrastructure
          runbook: "runbooks/high-memory-usage.md"
        annotations:
          summary: "Forge process memory exceeds 4 GB"
          description: >
            Memory usage: {{ $value | humanize }}GB.
            Check for memory leaks in agent pipelines.
          dashboard: "styde-forge-observability"
```

### 6.2 Runbook Catalog

**`deploy/runbooks/high-http-error-rate.md`**:

```markdown
# Runbook: High HTTP Error Rate

**Alert:** `HighHTTPErrorRate`
**Severity:** critical
**Category:** RED

---

## 1. Triage (5 min)

### Is this a real incident?
- [ ] Check Grafana dashboard (panel #2) — is error rate sustained beyond 5 minutes?
- [ ] Check if there's an ongoing deploy (`git log --oneline -5` on the forge host)
- [ ] Check downstream dependencies: Tempo/Loki/Prometheus healthy?

### Quick assessment
```bash
# Check recent errors in Loki
{service="styde-forge"} | json | level="ERROR" | line_format "{{.event}} {{.error_message}}"

# Check trace for a failing request (grab trace_id from a log line)
# Paste into Tempo Explore
```

## 2. Common Causes

| Symptom | Likely Cause | Action |
|---------|-------------|--------|
| `ConnectionError` or `TimeoutError` | Downstream service down | Check dependencies; restart if needed |
| `ValueError` / `KeyError` | Bad input data | Check agent config for malformed YAML/JSON |
| `MemoryError` | OOM in agent pipeline | Restart forge; increase memory limit |
| `PermissionError` | File system issue | Check disk space, file permissions |

## 3. Resolution Steps

### Step A: Restart the forge instance
```bash
systemctl restart styde-forge
# or
docker-compose restart forge
```

### Step B: Scale back if overloaded
```bash
# Reduce concurrent agent executions
export FORGE_MAX_CONCURRENCY=2
systemctl restart styde-forge
```

### Step C: Rollback recent deploy
```bash
cd /opt/styde-forge
git log --oneline -5
git revert <bad-commit-hash>
systemctl restart styde-forge
```

## 4. Escalation

If error rate persists after Steps A-C:
- **Primary on-call**: @forge-team via PagerDuty
- **Secondary**: @platform-eng via Slack #forge-alerts

## 5. Post-Incident

- [ ] Create a GitHub issue with the `incident` label
- [ ] Attach the trace_id and correlation_id of a representative failure
- [ ] Update this runbook if a new failure mode was discovered
```

**`deploy/runbooks/error-budget-burn.md`**:

```markdown
# Runbook: Error Budget Burning Too Fast

**Alert:** `ErrorBudgetBurnRateHigh`
**Severity:** critical
**Category:** SLO

---

## What This Means

The error budget for the **30-day rolling window** is being consumed at an
unsustainable rate. At the current burn rate, the budget will be exhausted
in hours, triggering the `ErrorBudgetExhausted` alert and freezing all
non-urgent deploys.

## Immediate Actions (< 10 min)

1. **Check the dashboard** — panels #204 (Pipeline Success Rate) and #205 (Burn Rate)
2. **Identify which agent(s) are failing** — sort by error rate in panel #202
3. **Pause non-critical agents**:
   ```bash
   curl -X POST http://forge:8765/api/agents/pause \
     -H "Content-Type: application/json" \
     -d '{"agent_name": "failing-agent-name"}'
   ```

## Root Cause Investigation

```bash
# Find the most common error class
curl -s http://prometheus:9090/api/v1/query \
  --data-urlencode 'query=topk(5, sum(rate(styde_forge_pipeline_errors_total[1h])) by (agent_name, error_class))'
```

## Recovery

- Fix the root cause (bug fix, config change, dependency update)
- Resume paused agents: `POST /api/agents/resume`
- Monitor burn rate for 1 hour to confirm recovery

## Escalation

- **Product Manager**: decide whether to pause all deploys
- **Platform Team**: if infrastructure is the root cause
```

---

## 7. Error Tracking Integration

### 7.1 Sentry Integration

```bash
uv add sentry-sdk
```

```python
"""
StydeAgents/observability/error_tracking.py
Sentry SDK initialization with OpenTelemetry linkage.
"""
import os
import sentry_sdk
from sentry_sdk.integrations.opentelemetry import OpenTelemetryIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.stdlib import StdlibIntegration
from sentry_sdk.integrations.excepthook import ExcepthookIntegration
from sentry_sdk.integrations.dedupe import DedupeIntegration
from sentry_sdk.integrations.modules import ModulesIntegration


def init_sentry(
    dsn: str | None = None,
    environment: str | None = None,
    traces_sample_rate: float = 0.1,
    profiles_sample_rate: float = 0.05,
):
    """
    Initialize Sentry error tracking with OpenTelemetry trace linkage.

    Args:
        dsn: Sentry DSN (defaults to SENTRY_DSN env var)
        environment: Deployment environment
        traces_sample_rate: Fraction of transactions sent to Sentry
        profiles_sample_rate: Fraction of transactions with profiling
    """
    dsn = dsn or os.getenv("SENTRY_DSN")
    if not dsn:
        raise ValueError("SENTRY_DSN environment variable or 'dsn' argument is required")

    sentry_sdk.init(
        dsn=dsn,
        environment=environment or os.getenv("DEPLOY_ENV", "development"),
        release=os.getenv("STYDE_FORGE_VERSION", "3.0.0"),
        traces_sample_rate=traces_sample_rate,
        profiles_sample_rate=profiles_sample_rate,
        attach_stacktrace=True,
        send_default_pii=False,
        max_breadcrumbs=100,
        integrations=[
            # Link Sentry errors to OpenTelemetry traces
            OpenTelemetryIntegration(),
            # Capture log records as breadcrumbs
            LoggingIntegration(level="INFO", event_level="ERROR"),
            StdlibIntegration(),
            ExcepthookIntegration(),
            DedupeIntegration(),
            ModulesIntegration(),
        ],
        _experiments={
            "continuous_profiling_auto_start": False,
        },
    )
```

### 7.2 Custom Error Context

```python
"""
Error context enrichment: attach correlation_id, agent context, and
trace links to every Sentry event automatically.
"""
import sentry_sdk
from opentelemetry import trace, baggage, context as otel_context


def capture_forge_error(
    exception: Exception,
    agent_name: str | None = None,
    pipeline_stage: str | None = None,
    extra_context: dict | None = None,
):
    """
    Report an error to Sentry with full Styde Forge context.

    Usage:
        try:
            run_pipeline()
        except Exception as exc:
            capture_forge_error(
                exc,
                agent_name="svelte-component-kit",
                pipeline_stage="refinery",
                extra_context={"input_config_hash": "abc123"},
            )
            raise
    """
    with sentry_sdk.push_scope() as scope:
        # ── Correlation ID ─────────────────────────────────────────
        corr_id = baggage.get_baggage("correlation_id", otel_context.get_current())
        if corr_id:
            scope.set_tag("correlation_id", corr_id)

        # ── Trace linkage ──────────────────────────────────────────
        span = trace.get_current_span()
        if span is not None:
            ctx = span.get_span_context()
            if ctx.is_valid:
                scope.set_tag("trace_id", format(ctx.trace_id, "032x"))
                scope.set_tag("span_id", format(ctx.span_id, "016x"))

        # ── Forge context ──────────────────────────────────────────
        if agent_name:
            scope.set_tag("agent.name", agent_name)
        if pipeline_stage:
            scope.set_tag("pipeline.stage", pipeline_stage)

        scope.set_tag("service", os.getenv("OTEL_SERVICE_NAME", "styde-forge"))
        scope.set_tag("environment", os.getenv("DEPLOY_ENV", "development"))

        # ── Extra structured data ──────────────────────────────────
        if extra_context:
            for key, value in extra_context.items():
                scope.set_extra(key, str(value)[:512])  # Truncate large values

        sentry_sdk.capture_exception(exception)
```

### 7.3 Error Aggregation & Fingerprinting

Prevent duplicate Sentry issues by custom fingerprinting:

```python
"""
Custom fingerprinting rules for Sentry events.
Group errors by (error_class, agent_name, pipeline_stage) instead of
stack trace alone. This prevents flooding Sentry with the same error
from different agents.
"""
from sentry_sdk import set_event


def before_send(event, hint):
    """
    Sentry before_send hook: customize fingerprint and add forge metadata.
    """
    if "exception" not in event:
        return event

    # Extract error class
    exception_data = event["exception"]["values"][0]
    error_type = exception_data.get("type", "UnknownError")

    # Extract forge metadata from tags
    tags = event.get("tags", {})
    agent_name = tags.get("agent.name", "unknown")
    pipeline_stage = tags.get("pipeline.stage", "unknown")

    # ── Custom fingerprint ─────────────────────────────────────────
    # Groups: (error_class, agent_name, pipeline_stage)
    event["fingerprint"] = [
        "styde-forge",
        error_type,
        agent_name,
        pipeline_stage,
    ]

    # ── Add forge metadata to event ────────────────────────────────
    event.setdefault("contexts", {})["forge"] = {
        "version": os.getenv("STYDE_FORGE_VERSION", "3.0.0"),
        "environment": os.getenv("DEPLOY_ENV", "development"),
    }

    return event


# Register the hook
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    before_send=before_send,
    # ... other config from init_sentry above
)
```

---

## 8. Deployment Checklist

| Step | Task | Command/File |
|------|------|-------------|
| 1 | Install Python dependencies | `uv sync` (all deps in pyproject.toml) |
| 2 | Set environment variables | Copy `.env.example` → `.env` |
| 3 | Start observability stack | `docker-compose -f docker-compose.obs.yml up -d` |
| 4 | Verify OTLP collector | `curl http://localhost:4318/v1/traces` → 200 |
| 5 | Verify Prometheus scraping | `curl http://localhost:9090/api/v1/targets` → forge target UP |
| 6 | Verify Tempo | `curl http://localhost:3200/ready` → "ready" |
| 7 | Verify Loki | `curl http://localhost:3100/ready` → "ready" |
| 8 | Import Grafana dashboard | Already provisioned via volume mount |
| 9 | Verify traces appear | Run a test agent, check Tempo in Grafana Explore |
| 10 | Verify logs appear | Check Loki in Grafana Explore for `{service="styde-forge"}` |
| 11 | Verify Sentry | Trigger a test error: `curl http://forge:8765/api/debug/error` |
| 12 | Set up alert routing | Configure Alertmanager → PagerDuty/Slack |

### Environment Variables (`.env.example`)

```bash
# ── Service Identity ──────────────────────────────────────────────────
OTEL_SERVICE_NAME=styde-forge
STYDE_FORGE_VERSION=3.0.0
DEPLOY_ENV=development          # development | staging | production
FORGE_INSTANCE_ID=local

# ── OpenTelemetry ─────────────────────────────────────────────────────
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
OTEL_EXPORTER_OTLP_INSECURE=true
OTEL_CONSOLE_EXPORT=false        # Set to true for local dev debugging

# ── Logging ───────────────────────────────────────────────────────────
LOG_LEVEL=INFO                   # DEBUG | INFO | WARNING | ERROR
LOG_JSON=true                    # Structured JSON output
LOG_PRETTY=false                 # Indent JSON for readability

# ── Sentry ────────────────────────────────────────────────────────────
SENTRY_DSN=https://<key>@sentry.io/<project>
SENTRY_TRACES_SAMPLE_RATE=0.1
```

### `pyproject.toml` dependencies section

```toml
[project]
name = "styde-forge"
version = "3.0.0"
requires-python = ">=3.11"
dependencies = [
    # ── Core ───────────────────────────────────────────────────────
    "pyyaml>=6.0",
    "structlog>=24.0",
    "python-json-logger>=2.0",

    # ── OpenTelemetry ──────────────────────────────────────────────
    "opentelemetry-api>=1.25",
    "opentelemetry-sdk>=1.25",
    "opentelemetry-exporter-otlp-proto-grpc>=1.25",
    "opentelemetry-instrumentation-flask>=0.46b0",
    "opentelemetry-instrumentation-requests>=0.46b0",
    "opentelemetry-instrumentation-redis>=0.46b0",
    "opentelemetry-instrumentation-sqlalchemy>=0.46b0",
    "opentelemetry-instrumentation-httpx>=0.46b0",
    "opentelemetry-instrumentation-logging>=0.46b0",
    "opentelemetry-instrumentation-system-metrics>=0.46b0",

    # ── Metrics ────────────────────────────────────────────────────
    "prometheus-client>=0.20",

    # ── Error Tracking ─────────────────────────────────────────────
    "sentry-sdk>=2.0",
]
```

---

## 9. Full Reference Implementation

### File Layout

```
Styde Forge/
├── Core/
│   ├── forge_main.py              # Entry point with observability bootstrap
│   ├── dashboard.py               # Existing dashboard (instrumented)
│   ├── forge_engine.py            # Pipeline engine (instrumented)
│   └── metrics_handler.py         # /metrics and /health HTTP handler
│
├── StydeAgents/
│   └── observability/
│       ├── __init__.py            # bootstrap_instrumentation()
│       ├── tracing.py             # init_tracing(), get_tracer()
│       ├── context.py             # extract/inject correlation headers
│       ├── logging.py             # init_logging(), structlog config
│       ├── middleware.py           # CorrelationIDMiddleware
│       ├── metrics.py             # Prometheus Counter/Histogram/Gauge defs
│       ├── metrics_decorators.py  # @red_http, @red_pipeline decorators
│       ├── instrument.py          # @traced, TracedContext
│       └── error_tracking.py      # Sentry init, capture_forge_error()
│
├── deploy/
│   ├── docker-compose.obs.yml     # OTel Collector, Tempo, Loki, Prometheus, Grafana
│   ├── otel-collector-config.yaml
│   ├── tempo.yaml
│   ├── loki-config.yaml
│   ├── prometheus.yml
│   ├── alerting-rules.yml
│   ├── alertmanager.yml
│   ├── grafana-datasources.yml
│   ├── grafana-dashboards/
│   │   └── styde-forge-observability.json
│   └── runbooks/
│       ├── high-http-error-rate.md
│       ├── high-http-latency.md
│       ├── high-pipeline-failure-rate.md
│       ├── pipeline-timeout.md
│       ├── error-budget-burn.md
│       ├── error-budget-exhausted.md
│       ├── forge-instance-down.md
│       ├── queue-backlog.md
│       └── high-memory-usage.md
│
├── pyproject.toml
└── .env.example
```

### Quick-Start Commands

```bash
# 1. Install dependencies
uv sync

# 2. Start the observability stack
docker-compose -f deploy/docker-compose.obs.yml up -d

# 3. Verify everything is healthy
curl http://localhost:4318/v1/traces       # OTel collector
curl http://localhost:9090/api/v1/targets  # Prometheus
curl http://localhost:3200/ready           # Tempo
curl http://localhost:3100/ready           # Loki
curl http://localhost:3000/api/health      # Grafana

# 4. Start Styde Forge with observability
python Core/forge_main.py

# 5. Open Grafana
open http://localhost:3000
# Login: admin / admin
# Dashboard: "Styde Forge — Observability Dashboard"
```

### Observability in Action: Trace Flow

```
1. User invokes agent pipeline
   │
   ├─ CorrelationIDMiddleware generates: X-Correlation-ID: a1b2c3d4...
   │  Sets baggage["correlation_id"] = "a1b2c3d4..."
   │
   ├─ Span "pipeline.execute" starts (trace_id = 4bf92f...)
   │  ├─ Span "pipeline.refinery" (agent=svelte-component-kit)
   │  │  ├─ Log: "agent.execution.start" {correlation_id, trace_id, span_id}
   │  │  ├─ HTTP call to external API (auto-instrumented by RequestsInstrumentor)
   │  │  └─ Log: "agent.execution.complete" {duration_ms: 1234}
   │  ├─ Span "pipeline.production"
   │  │  └─ ...
   │  └─ Span "pipeline.archive"
   │     └─ ...
   │
   ├─ RED metrics updated:
   │  styde_forge_pipeline_executions_total{agent_name=..., stage=..., status="success"} +1
   │  styde_forge_pipeline_duration_seconds{...}.observe(12.34)
   │
   └─ If error:
      ├─ Sentry event created (fingerprinted by agent+stage+error_class)
      ├─ Sentry event tagged with trace_id and correlation_id
      └─ Log: ERROR "pipeline.failed" {exception, trace_id, correlation_id}
```

**Correlation Chain** — from any point, navigate to all other signals:

```
Sentry Issue  →  tags.trace_id  →  Tempo trace  →  span events (logs)
                                                    ↓
                                               correlation_id  →  Loki logs
                                                                    ↓
                                                               trace_id → back to Tempo
```

---

> **Agent:** logging-monitoring-architect · Styde Forge  
> **Completed:** 2026-06-26 00:08:00 UTC  
> **Status:** Complete observability setup guide with production-ready code, dashboards, alerts, and runbooks.
