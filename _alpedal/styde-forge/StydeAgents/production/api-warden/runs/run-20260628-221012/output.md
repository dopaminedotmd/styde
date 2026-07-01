```python
#!/usr/bin/env python3
"""api-warden.py - Forge Dashboard /api/state endpoint monitor.
Monitors /api/state every N seconds, runs health checks, produces uptime
reports and latency histograms, and alerts on consecutive failures.
Usage:
    python api-warden.py                        # default config
    python api-warden.py --interval 30           # check every 30s
    python api-warden.py --endpoint http://...   # custom base URL
    python api-warden.py --alert-webhook http://...# external alert
    python api-warden.py --max-log 5000          # cap memory
"""
import argparse
import json
import os
import sys
import time
import signal
import logging
import threading
from collections import OrderedDict
from datetime import datetime, timezone
from http.client import HTTPConnection, HTTPSConnection
from urllib.parse import urlparse
# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DEFAULTS = {
    "interval": 60,
    "endpoint": None,       # resolved at runtime
    "timeout": 10,
    "max_log_entries": 10000,
    "histogram_buckets": [0, 50, 100, 200, 300, 400, 500],
    "consecutive_fail_threshold": 3,
    "alert_webhook": None,
    "alert_stderr": True,
    "expected_endpoint_path": "/api/state",
}
def resolve_endpoint(candidate):
    """Attempt recovery strategy before aborting.
    1. Use the candidate argument (from CLI / env).
    2. Fall back to env var STRYDEAPIURL.
    3. Fall back to http://localhost:8080.
    4. Raise.
    """
    urls = [candidate, os.environ.get("STRYDEAPIURL"), "http://localhost:8080"]
    for url in urls:
        if not url:
            continue
        url = url.rstrip("/") + DEFAULTS["expected_endpoint_path"]
        return url
    raise RuntimeError(
        "No endpoint URL available. "
        "Pass --endpoint, set STRYDEAPIURL env var, "
        "or ensure localhost:8080 is reachable."
    )
def parse_args(argv=None):
    p = argparse.ArgumentParser(description="API-Warden Forge monitor")
    p.add_argument("--interval", type=int, default=DEFAULTS["interval"],
                    help="Check interval in seconds (default: %d)" % DEFAULTS["interval"])
    p.add_argument("--endpoint", default=None,
                    help="Base URL for Forge dashboard (e.g. http://forge.example.com)")
    p.add_argument("--timeout", type=int, default=DEFAULTS["timeout"],
                    help="HTTP timeout in seconds (default: %d)" % DEFAULTS["timeout"])
    p.add_argument("--max-log", type=int, default=DEFAULTS["max_log_entries"],
                    help="Max uptime log entries before trimming (default: %d)" % DEFAULTS["max_log_entries"])
    p.add_argument("--fail-threshold", type=int, default=DEFAULTS["consecutive_fail_threshold"],
                    help="Consecutive failures before alert (default: %d)" % DEFAULTS["consecutive_fail_threshold"])
    p.add_argument("--alert-webhook", default=None,
                    help="Optional HTTP webhook URL for alerts")
    p.add_argument("--no-stderr-alert", action="store_true",
                    help="Disable stderr alert output")
    p.add_argument("--log-file", default=None,
                    help="Optional file path for uptime log output")
    return p.parse_args(argv)
def build_config(args):
    cfg = dict(DEFAULTS)
    cfg["interval"] = args.interval
    cfg["timeout"] = args.timeout
    cfg["max_log_entries"] = args.max_log
    cfg["consecutive_fail_threshold"] = args.fail_threshold
    cfg["alert_webhook"] = args.alert_webhook
    cfg["alert_stderr"] = not args.no_stderr_alert
    cfg["log_file"] = args.log_file
    cfg["endpoint"] = resolve_endpoint(args.endpoint)
    return cfg
# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)
logger = logging.getLogger("api-warden")
# ---------------------------------------------------------------------------
# Alert delivery — pluggable via extension point
# ---------------------------------------------------------------------------
class AlertDispatcher:
    """Pluggable alert delivery.
    Built-in: stderr logging, file logging, HTTP webhook.
    Extend by subclassing and overriding deliver(), then register.
    """
    def __init__(self, config):
        self._dispatchers = []
        if config["alert_stderr"]:
            self._dispatchers.append(StderrAlertDispatcher())
        if config["alert_webhook"]:
            self._dispatchers.append(WebhookAlertDispatcher(config["alert_webhook"], config["timeout"]))
        if config["log_file"]:
            self._dispatchers.append(FileAlertDispatcher(config["log_file"]))
    def dispatch(self, message):
        for d in self._dispatchers:
            try:
                d.deliver(message)
            except Exception as exc:
                logger.error("Alert dispatcher %s failed: %s", type(d).__name__, exc)
    def register(self, dispatcher):
        """Extension point: add custom AlertDispatcher implementations."""
        self._dispatchers.append(dispatcher)
class StderrAlertDispatcher:
    def deliver(self, message):
        print("ALERT: %s" % message, file=sys.stderr)
class FileAlertDispatcher:
    def __init__(self, path):
        self.path = path
    def deliver(self, message):
        with open(self.path, "a") as f:
            f.write("%s ALERT: %s\n" % (datetime.now(timezone.utc).isoformat(), message))
class WebhookAlertDispatcher:
    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout
    def deliver(self, message):
        body = json.dumps({"text": message, "source": "api-warden"}).encode("utf-8")
        parsed = urlparse(self.url)
        conn_cls = HTTPSConnection if parsed.scheme == "https" else HTTPConnection
        conn = conn_cls(parsed.netloc, timeout=self.timeout)
        try:
            conn.request("POST", parsed.path or "/", body=body,
                         headers={"Content-Type": "application/json"})
            resp = conn.getresponse()
            resp.read()
        finally:
            conn.close()
# ---------------------------------------------------------------------------
# Uptime log — bounded memory via capped OrderedDict (FIFO eviction)
# ---------------------------------------------------------------------------
class BoundedUptimeLog:
    """Thread-safe, memory-bounded chronlog with FIFO eviction."""
    def __init__(self, max_entries):
        self._max = max_entries
        self._lock = threading.Lock()
        # OrderedDict insertion-order = chronological; pop first on overflow
        self._entries = OrderedDict()
    def append(self, entry):
        with self._lock:
            key = entry["timestamp"]
            self._entries[key] = entry
            while len(self._entries) > self._max:
                self._entries.popitem(last=False)
    def all_entries(self):
        with self._lock:
            return list(self._entries.values())
    def clear(self):
        with self._lock:
            self._entries.clear()
# ---------------------------------------------------------------------------
# Latency histogram — unbounded counters but bounded number of buckets
# ---------------------------------------------------------------------------
class LatencyHistogram:
    """Bucketed latency distribution. Buckets are fixed-size; memory is O(buckets)."""
    def __init__(self, bucket_boundaries):
        self._buckets = sorted(bucket_boundaries)
        self._counts = {str(b): 0 for b in self._buckets}
        self._counts["+%d" % self._buckets[-1]] = 0
        self._lock = threading.Lock()
        self._total = 0
    def record(self, latency_ms):
        with self._lock:
            bucket = "+%d" % self._buckets[-1]
            for b in reversed(self._buckets):
                if latency_ms >= b:
                    bucket = str(b)
                    break
                # If latency < smallest bucket, it falls into the smallest
                if latency_ms < self._buckets[0]:
                    bucket = str(self._buckets[0])
            if bucket not in self._counts:
                bucket = str(self._buckets[0])
            self._counts[bucket] += 1
            self._total += 1
    def snapshot(self):
        with self._lock:
            return dict(self._counts), self._total
# ---------------------------------------------------------------------------
# Health check runner
# ---------------------------------------------------------------------------
class HealthCheckRunner:
    """Executes the five health checks against /api/state."""
    def __init__(self, base_url, timeout):
        self._base_url = base_url.rstrip("/")
        self._endpoint_path = DEFAULTS["expected_endpoint_path"]
        self._timeout = timeout
    def run(self):
        """Returns (passes: bool, details: dict)."""
        url = self._base_url + self._endpoint_path
        parsed = urlparse(url)
        conn_cls = HTTPSConnection if parsed.scheme == "https" else HTTPConnection
        host = parsed.netloc
        path = parsed.path or "/"
        if parsed.query:
            path += "?" + parsed.query
        result = {"timestamp": datetime.now(timezone.utc).isoformat(),
                   "status": "fail",
                   "response_time_ms": None,
                   "error": None,
                   "checks": {}}
        start = time.monotonic()
        try:
            conn = conn_cls(host, timeout=self._timeout)
            conn.request("GET", path, headers={"Accept": "application/json"})
            resp = conn.getresponse()
            elapsed_ms = round((time.monotonic() - start) * 1000, 1)
            result["response_time_ms"] = elapsed_ms
            # Check 1: HTTP Status
            status_ok = resp.status == 200
            result["checks"]["http_status"] = {"pass": status_ok,
                                                "expected": 200, "actual": resp.status}
            raw = resp.read()
            conn.close()
            # Check 2: JSON validity
            try:
                data = json.loads(raw)
                result["checks"]["json_valid"] = {"pass": True}
            except json.JSONDecodeError as e:
                result["checks"]["json_valid"] = {"pass": False,
                                                   "error": str(e),
                                                   "snippet": raw[:1024].decode("utf-8", errors="replace")}
                data = None
            # Check 3: Response time
            time_ok = elapsed_ms < 500
            result["checks"]["response_time"] = {"pass": time_ok,
                                                  "expected": "<500ms", "actual": "%sms" % elapsed_ms}
            # Check 4: Field completeness (expects the JSON to have any key)
            if data is not None and isinstance(data, dict):
                fields_present = list(data.keys())
                result["checks"]["field_completeness"] = {"pass": True,
                                                           "fields": fields_present}
            elif data is not None:
                result["checks"]["field_completeness"] = {"pass": True,
                                                           "fields": ["(non-dict JSON)"]}
            else:
                result["checks"]["field_completeness"] = {"pass": False,
                                                           "error": "No parseable JSON to inspect"}
            # Check 5: CORS headers
            cors_origin = resp.getheader("Access-Control-Allow-Origin")
            cors_methods = resp.getheader("Access-Control-Allow-Methods")
            cors_ok = cors_origin is not None
            result["checks"]["cors_headers"] = {"pass": cors_ok,
                                                 "Access-Control-Allow-Origin": cors_origin,
                                                 "Access-Control-Allow-Methods": cors_methods}
            all_pass = all(c["pass"] for c in result["checks"].values())
            result["status"] = "pass" if all_pass else "fail"
        except Exception as e:
            elapsed_ms = round((time.monotonic() - start) * 1000, 1)
            result["response_time_ms"] = elapsed_ms
            result["status"] = "down"
            result["error"] = "%s: %s" % (type(e).__name__, str(e))
        return result
# ---------------------------------------------------------------------------
# Main monitor loop
# ---------------------------------------------------------------------------
class APIMonitor:
    """Orchestrates periodic checks, logging, histogram, and alerting."""
    def __init__(self, config):
        self.config = config
        self.shutdown_event = threading.Event()
        self.runner = HealthCheckRunner(config["endpoint"], config["timeout"])
        self.log = BoundedUptimeLog(config["max_log_entries"])
        self.histogram = LatencyHistogram(config["histogram_buckets"])
        self.alert_dispatch = AlertDispatcher(config)
        self._consecutive_failures = 0
        self._lock = threading.Lock()
        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)
    def _handle_signal(self, signum, frame):
        sig_name = signal.Signals(signum).name
        logger.info("Received %s — initiating graceful shutdown", sig_name)
        self.shutdown_event.set()
    def _check_and_log(self):
        result = self.runner.run()
        self.log.append(result)
        if result["response_time_ms"] is not None and result["status"] != "down":
            self.histogram.record(result["response_time_ms"])
        status_char = "PASS" if result["status"] == "pass" else "FAIL" if result["status"] == "fail" else "DOWN"
        logger.info("[%s] %s | %sms | %s",
                     status_char,
                     self.config["endpoint"] + DEFAULTS["expected_endpoint_path"],
                     result["response_time_ms"] or "?",
                     result.get("error") or "")
        with self._lock:
            if result["status"] in ("fail", "down"):
                self._consecutive_failures += 1
            else:
                self._consecutive_failures = 0
            if self._consecutive_failures >= self.config["consecutive_fail_threshold"]:
                msg = ("%d consecutive failures on %s. Last error: %s" %
                       (self._consecutive_failures,
                        self.config["endpoint"] + DEFAULTS["expected_endpoint_path"],
                        result.get("error") or json.dumps(result["checks"])))
                self.alert_dispatch.dispatch(msg)
    def run_forever(self):
        logger.info("API-Warden starting — monitoring %s every %ds",
                     self.config["endpoint"] + DEFAULTS["expected_endpoint_path"],
                     self.config["interval"])
        logger.info("Alert threshold: %d consecutive failures",
                     self.config["consecutive_fail_threshold"])
        if self.config["alert_webhook"]:
            logger.info("Webhook alerting enabled: %s", self.config["alert_webhook"])
        if self.config["log_file"]:
            logger.info("File alerting enabled: %s", self.config["log_file"])
        # Initial check immediately
        self._check_and_log()
        while not self.shutdown_event.is_set():
            interrupted = self.shutdown_event.wait(timeout=self.config["interval"])
            if interrupted:
                break
            self._check_and_log()
        self._cleanup()
        logger.info("API-Warden stopped.")
    def _cleanup(self):
        """Resource cleanup: log summary."""
        hist, total = self.histogram.snapshot()
        log_count = len(self.log.all_entries())
        logger.info("Cleanup: %d log entries, %d histogram samples", log_count, total)
        if hist:
            logger.info("Latency histogram snapshot: %s", json.dumps(hist))
# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
def main(argv=None):
    args = parse_args(argv)
    config = build_config(args)
    monitor = APIMonitor(config)
    monitor.run_forever()
if __name__ == "__main__":
    main()
```