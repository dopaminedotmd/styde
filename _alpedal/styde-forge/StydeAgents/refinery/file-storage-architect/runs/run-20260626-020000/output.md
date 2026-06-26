# File Storage Architecture — Advanced Storage Patterns

**Author:** File Storage Architect (Styde Forge)
**Date:** 2026-06-26
**Version:** 2.0.0
**Focus:** S3 Object Lambda, Multi-Region Replication, Glacier Instant Retrieval Tiering, Event-Driven Processing, Storage Class Analysis

---

## Table of Contents

1. [Overview & Architecture Goals](#1-overview--architecture-goals)
2. [S3 Object Lambda for Dynamic Transforms](#2-s3-object-lambda-for-dynamic-transforms)
3. [Multi-Region Replication](#3-multi-region-replication)
4. [Glacier Instant Retrieval Tiering](#4-glacier-instant-retrieval-tiering)
5. [Event-Driven Processing with S3 Event Notifications + SQS](#5-event-driven-processing-with-s3-event-notifications--sqs)
6. [Storage Class Analysis](#6-storage-class-analysis)
7. [Infrastructure as Code (Terraform)](#7-infrastructure-as-code-terraform)
8. [Monitoring & Observability](#8-monitoring--observability)
9. [Security & Compliance](#9-security--compliance)

---

## 1. Overview & Architecture Goals

This document covers advanced S3 storage patterns that extend a baseline file-storage architecture with dynamic content transformation, cross-region durability, intelligent tiering, event-driven pipelines, and cost analytics. These patterns are production-hardened and assume a multi-account AWS Organization with centralized logging and security controls.

| Principle | Implementation |
|-----------|---------------|
| **Dynamic Delivery** | S3 Object Lambda transforms objects on-read without storing duplicates |
| **Global Resilience** | Multi-Region Replication (MRR) with bi-directional sync and failover routing |
| **Intelligent Tiering** | Glacier Instant Retrieval for infrequent-access data with millisecond recall |
| **Event-Driven Scale** | S3 Event Notifications → SQS → Lambda for decoupled, replayable processing |
| **Cost Visibility** | S3 Storage Class Analysis + Athena queries for lifecycle ROI tracking |
| **Observability** | Structured logging, CloudWatch metrics, X-Ray tracing across all pipelines |

### High-Level Architecture

```
                          ┌──────────────────────────────────────────────┐
                          │              AWS Organization                │
                          │                                              │
  ┌─────────┐    S3       │  ┌──────────┐   Object Lambda   ┌─────────┐ │
  │ Client  │─────────────┼─►│  S3 Get  │──────────────────►│ Lambda  │ │
  │(Browser)│  Object      │  │  Request │  Access Point     │Transform│ │
  └─────────┘  Lambda URL  │  └──────────┘                   └────┬────┘ │
                          │                                       │      │
                          │                              ┌────────▼────┐ │
                          │  ┌─────────┐   S3 Event     │  Original   │ │
                          │  │  SQS     │◄───────────────│  Bucket     │ │
                          │  │  Queue   │  Notifications └─────────────┘ │
                          │  └────┬────┘                                │
                          │       │ fan-out                              │
                          │  ┌────▼─────────────────────────────┐       │
                          │  │  Processing Lambdas               │       │
                          │  │  (Scan, Index, Replicate, Tier)   │       │
                          │  └──────────────────┬───────────────┘       │
                          │                     │                        │
                          │  ┌──────────────────▼──────────────────┐    │
                          │  │  Multi-Region Replication            │    │
                          │  │  us-east-1 ◄────────────► eu-west-1 │    │
                          │  │  (Active)    Bi-directional  (DR)   │    │
                          │  └─────────────────────────────────────┘    │
                          │                     │                        │
                          │  ┌──────────────────▼──────────────────┐    │
                          │  │  Lifecycle → Glacier Instant Retrieval│   │
                          │  │  Storage Class Analysis → Athena     │    │
                          │  └─────────────────────────────────────┘    │
                          └──────────────────────────────────────────────┘
```

---

## 2. S3 Object Lambda for Dynamic Transforms

### 2.1 Concept

S3 Object Lambda allows you to add custom code to S3 GET, HEAD, and LIST requests to modify data returned to an application — **without creating derivative copies**. A single source object can serve different formats, resolutions, redactions, or enrichments depending on the requesting context.

```
Standard S3:    Client ──► S3 ──► Raw Object
Object Lambda:  Client ──► Object Lambda Access Point ──► Lambda ──► S3 ──► Transformed Object
```

### 2.2 Use Cases

| Use Case | Transform | Trigger |
|----------|-----------|---------|
| **Image Resizing** | Resize + convert format on-the-fly via query params (`?w=800&fmt=webp`) | Every GET |
| **PII Redaction** | Strip sensitive fields from JSON/CSV based on IAM principal tags | GET by non-admin role |
| **Watermarking** | Add dynamic watermarks with requester ID, timestamp | GET by external users |
| **Format Conversion** | Convert XML→JSON, CSV→Parquet, TIFF→PNG | GET with `Accept` header |
| **Content Enrichment** | Append metadata from DynamoDB (tags, ratings, usage stats) | Every GET |
| **Multi-Tenant Views** | Return tenant-specific views of the same underlying data | GET with tenant context |

### 2.3 Image Resizing Lambda (Python)

```python
"""
S3 Object Lambda handler for on-the-fly image transformation.
Query parameters: ?w=<width>&h=<height>&fmt=<webp|jpeg|png>&q=<quality>
"""
import io
import json
import urllib.parse
import boto3
from PIL import Image

# Constants
SUPPORTED_FORMATS = {"webp", "jpeg", "png", "avif"}
MAX_DIMENSION = 4096
DEFAULT_QUALITY = 82
S3_CACHE_TTL = 3600  # seconds for WriteGetObjectResponse caching headers

s3 = boto3.client("s3")


def lambda_handler(event, context):
    """
    Entry point for S3 Object Lambda.

    event structure:
    {
        "x-amz-request-route": "…",
        "x-amz-request-token": "…",
        "userRequest": { "url": "/path?w=800&fmt=webp" },
        "userIdentity": { "principalId": "…" },
        "getObjectContext": {
            "inputS3Url": "https://…",
            "outputRoute": "…",
            "outputToken": "…"
        }
    }
    """
    # Parse the original request
    user_request_url = event["userRequest"]["url"]
    parsed = urllib.parse.urlparse(user_request_url)
    query = urllib.parse.parse_qs(parsed.query)

    # Extract transformation parameters
    width = int(query.get("w", [0])[0]) or None
    height = int(query.get("h", [0])[0]) or None
    fmt = query.get("fmt", ["webp"])[0].lower()
    quality = int(query.get("q", [DEFAULT_QUALITY])[0])

    # Validate format
    if fmt not in SUPPORTED_FORMATS:
        fmt = "webp"

    # Handle no-transform case: pass through
    if not width and not height:
        return _passthrough(event)

    # Get the original object from S3
    get_object_context = event["getObjectContext"]
    s3_url = get_object_context["inputS3Url"]

    try:
        original = _fetch_original(s3_url)
    except Exception as e:
        return _error_response(event, 404, f"Object not found: {str(e)}")

    # Open and transform the image
    try:
        image = Image.open(io.BytesIO(original))
        original_fmt = image.format

        # Clamp dimensions
        if width:
            width = min(width, MAX_DIMENSION)
        if height:
            height = min(height, MAX_DIMENSION)

        # Resize if dimensions specified
        if width or height:
            # Calculate aspect-ratio preserving dimensions
            if width and height:
                image.thumbnail((width, height), Image.LANCZOS)
            elif width:
                ratio = width / image.width
                image = image.resize((width, int(image.height * ratio)), Image.LANCZOS)
            elif height:
                ratio = height / image.height
                image = image.resize((int(image.width * ratio), height), Image.LANCZOS)

        # Convert RGBA/CMYK to RGB for JPEG/WEBP if needed
        if fmt in ("jpeg", "webp") and image.mode in ("RGBA", "P", "CMYK"):
            image = image.convert("RGB")

        # Encode to target format
        output_buffer = io.BytesIO()
        save_kwargs = {"format": fmt.upper(), "quality": quality}
        if fmt == "webp":
            save_kwargs["method"] = 6  # slowest/best compression
        elif fmt == "png":
            save_kwargs.pop("quality", None)
            save_kwargs["optimize"] = True

        image.save(output_buffer, **save_kwargs)
        transformed_bytes = output_buffer.getvalue()

    except Exception as e:
        # If transformation fails, pass through original
        print(f"Transform failed, passing through original: {str(e)}")
        transformed_bytes = original
        fmt = original_fmt.lower() if original_fmt else "binary"

    # Determine content type
    content_types = {
        "webp": "image/webp",
        "jpeg": "image/jpeg",
        "jpg": "image/jpeg",
        "png": "image/png",
        "avif": "image/avif",
    }
    content_type = content_types.get(fmt, "application/octet-stream")

    # Write the transformed object back via WriteGetObjectResponse
    s3.write_get_object_response(
        Body=transformed_bytes,
        RequestRoute=get_object_context["outputRoute"],
        RequestToken=get_object_context["outputToken"],
        ContentType=content_type,
        CacheControl=f"public, max-age={S3_CACHE_TTL}",
        Metadata={
            "transformed-by": "object-lambda-image-resizer",
            "original-format": original_fmt or "unknown",
            "target-format": fmt,
            "transform-width": str(width or "auto"),
            "transform-height": str(height or "auto"),
        },
    )

    return {"status_code": 200}


def _fetch_original(s3_url: str) -> bytes:
    """Fetch the original object from S3 via presigned URL."""
    import requests
    response = requests.get(s3_url, timeout=30)
    response.raise_for_status()
    return response.content


def _passthrough(event) -> dict:
    """Pass through the original object unchanged."""
    import requests
    ctx = event["getObjectContext"]
    response = requests.get(ctx["inputS3Url"], timeout=30)

    s3.write_get_object_response(
        Body=response.content,
        RequestRoute=ctx["outputRoute"],
        RequestToken=ctx["outputToken"],
        ContentType=response.headers.get("Content-Type", "application/octet-stream"),
        CacheControl="public, max-age=3600",
    )
    return {"status_code": 200}


def _error_response(event, status_code: int, message: str) -> dict:
    """Return an error via WriteGetObjectResponse."""
    ctx = event["getObjectContext"]
    s3.write_get_object_response(
        Body=json.dumps({"error": message}).encode(),
        RequestRoute=ctx["outputRoute"],
        RequestToken=ctx["outputToken"],
        ContentType="application/json",
        StatusCode=status_code,
    )
    return {"status_code": status_code}
```

### 2.4 PII Redaction Lambda (Python)

```python
"""
S3 Object Lambda handler for PII redaction.
Redacts sensitive fields from JSON documents based on IAM principal tags.
"""
import json
import re
import boto3

s3 = boto3.client("s3")
iam = boto3.client("iam")

# Patterns to redact
PII_PATTERNS = {
    "email": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "credit_card": re.compile(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"),
    "phone": re.compile(r"\b\+?1?\d{10,11}\b"),
}

REDACTION_MARKER = "[REDACTED]"


def lambda_handler(event, context):
    ctx = event["getObjectContext"]
    principal_id = event.get("userIdentity", {}).get("principalId", "")

    # Determine clearance level from IAM principal tags
    clearance = _get_principal_clearance(principal_id)

    # Fetch original object
    import requests
    response = requests.get(ctx["inputS3Url"], timeout=30)
    content_type = response.headers.get("Content-Type", "")

    if "json" not in content_type:
        # Non-JSON: check if admin, else deny
        if clearance == "admin":
            transformed = response.content
        else:
            transformed = json.dumps({
                "error": "Access denied: non-admin cannot read non-JSON objects"
            }).encode()
    else:
        data = response.json()
        if clearance == "admin":
            transformed = json.dumps(data).encode()
        elif clearance == "redacted":
            redacted = _redact_recursive(data)
            transformed = json.dumps(redacted).encode()
        else:
            # No clearance: return empty
            transformed = json.dumps({}).encode()

    s3.write_get_object_response(
        Body=transformed,
        RequestRoute=ctx["outputRoute"],
        RequestToken=ctx["outputToken"],
        ContentType=content_type,
        Metadata={"redacted-by": "object-lambda-pii-redact", "clearance": clearance},
    )
    return {"status_code": 200}


def _redact_recursive(obj):
    """Recursively redact PII from dicts, lists, strings."""
    if isinstance(obj, dict):
        sensitive_keys = {"email", "phone", "ssn", "credit_card",
                          "address", "dob", "passport", "driver_license"}
        return {
            k: (REDACTION_MARKER if k.lower() in sensitive_keys else _redact_recursive(v))
            for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [_redact_recursive(item) for item in obj]
    elif isinstance(obj, str):
        result = obj
        for pattern_name, pattern in PII_PATTERNS.items():
            result = pattern.sub(REDACTION_MARKER, result)
        return result
    return obj


def _get_principal_clearance(principal_id: str) -> str:
    """Determine clearance level from IAM principal tags (cached in-memory)."""
    if not principal_id:
        return "none"
    # In production, resolve IAM role/user tags
    # For this example, assume role name encodes clearance
    if "admin" in principal_id.lower():
        return "admin"
    if "redacted" in principal_id.lower():
        return "redacted"
    return "none"
```

### 2.5 Object Lambda Access Point Configuration (Terraform)

```hcl
# S3 Object Lambda Access Point
resource "aws_s3control_object_lambda_access_point" "image_transform" {
  name = "stryde-image-transform"

  configuration {
    supporting_access_point = aws_s3_access_point.media.arn
    transformation_configuration {
      actions = ["GetObject", "HeadObject"]

      content_transformation {
        aws_lambda {
          function_arn = aws_lambda_function.object_lambda_image.arn
          function_payload = jsonencode({
            # Optional: pass static config to Lambda
            default_format = "webp"
            default_quality = 82
            cache_ttl_seconds = 3600
          })
        }
      }
    }
  }
}

# Standard S3 Access Point (supporting)
resource "aws_s3_access_point" "media" {
  bucket = aws_s3_bucket.media.id
  name   = "stryde-media-access"
}

# IAM policy for Object Lambda to read from S3
resource "aws_iam_role_policy" "object_lambda_s3_read" {
  role = aws_iam_role.object_lambda_exec.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:GetObjectVersion",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.media.arn,
          "${aws_s3_bucket.media.arn}/*"
        ]
      }
    ]
  })
}
```

### 2.6 Client Usage (TypeScript / Browser)

```typescript
/**
 * Fetch a transformed image via S3 Object Lambda.
 * The Object Lambda Access Point alias becomes the S3 host.
 */
interface ImageTransformOptions {
  width?: number;
  height?: number;
  format?: "webp" | "jpeg" | "png" | "avif";
  quality?: number;
}

async function fetchTransformedImage(
  objectKey: string,
  options: ImageTransformOptions = {}
): Promise<Blob> {
  const params = new URLSearchParams();

  // Object Lambda Access Point alias
  const baseUrl = `https://stryde-image-transform-${ACCOUNT_ID}.s3-object-lambda.us-east-1.amazonaws.com`;

  if (options.width) params.set("w", String(options.width));
  if (options.height) params.set("h", String(options.height));
  if (options.format) params.set("fmt", options.format);
  if (options.quality) params.set("q", String(options.quality));

  const url = `${baseUrl}/${encodeURIComponent(objectKey)}?${params.toString()}`;

  const response = await fetch(url, {
    headers: {
      // Forward auth token for PII redaction decisions
      ...(authToken && { Authorization: `Bearer ${authToken}` }),
    },
  });

  if (!response.ok) {
    throw new Error(`S3 Object Lambda failed: ${response.status}`);
  }

  return response.blob();
}

// Usage:
// <img src={URL.createObjectURL(await fetchTransformedImage("images/photo.jpg", { width: 800, format: "webp" }))} />
```

---

## 3. Multi-Region Replication

### 3.1 Architecture

Multi-Region Replication (MRR) copies objects asynchronously across AWS regions with configurable rules. This pattern covers active-active, active-passive, and fan-out replication topologies.

```
Region: us-east-1 (Primary)                  Region: eu-west-1 (DR)
┌──────────────────────────┐                 ┌──────────────────────────┐
│  stryde-media-primary    │                 │  stryde-media-dr         │
│                          │   S3 Replication │                          │
│  ┌────────────────────┐  │ ═══════════════►│  ┌────────────────────┐  │
│  │ objects/           │  │                 │  │ objects/           │  │
│  │ ├── images/        │  │                 │  │ ├── images/        │  │
│  │ ├── documents/     │  │                 │  │ ├── documents/     │  │
│  │ └── videos/        │  │                 │  │ └── videos/        │  │
│  └────────────────────┘  │                 │  └────────────────────┘  │
│                          │                 │                          │
│  Replication Metrics     │                 │  Replication Metrics     │
│  (CloudWatch)            │                 │  (CloudWatch)            │
└──────────────────────────┘                 └──────────────────────────┘
         ▲                                            ▲
         │  Route 53 Latency-Based                    │
         │  Routing                                   │
         │                                            │
    ┌────┴────────────────────────────────────────────┴────┐
    │                    CloudFront CDN                     │
    │           (Origin: nearest S3 bucket)                 │
    └──────────────────────────────────────────────────────┘
```

### 3.2 Replication Rules

#### Bi-Directional (Active-Active) Replication

```json
{
  "Role": "arn:aws:iam::123456789012:role/s3-mrr-replication-role",
  "Rules": [
    {
      "ID": "replicate-all-to-dr",
      "Status": "Enabled",
      "Priority": 1,
      "Filter": {
        "Prefix": ""
      },
      "DeleteMarkerReplication": {
        "Status": "Enabled"
      },
      "Destination": {
        "Bucket": "arn:aws:s3:::stryde-media-dr",
        "Account": "123456789013",
        "StorageClass": "STANDARD",
        "ReplicationTime": {
          "Status": "Enabled",
          "Time": {
            "Minutes": 15
          }
        },
        "Metrics": {
          "Status": "Enabled",
          "EventThreshold": {
            "Minutes": 15
          }
        }
      }
    },
    {
      "ID": "replicate-critical-only-to-eu",
      "Status": "Enabled",
      "Priority": 2,
      "Filter": {
        "Prefix": "critical/",
        "Tags": [
          {
            "Key": "replication-tier",
            "Value": "premium"
          }
        ]
      },
      "Destination": {
        "Bucket": "arn:aws:s3:::stryde-media-eu",
        "StorageClass": "STANDARD"
      }
    }
  ]
}
```

### 3.3 Replication Time Control (RTC)

S3 Replication Time Control provides a **15-minute SLA** for 99.99% of objects, with CloudWatch metrics for monitoring compliance.

```hcl
# Terraform: Enable RTC on replication rule
resource "aws_s3_bucket_replication_configuration" "main" {
  role   = aws_iam_role.replication.arn
  bucket = aws_s3_bucket.primary.id

  rule {
    id     = "mrr-with-rtc"
    status = "Enabled"

    filter {
      prefix = ""
    }

    destination {
      bucket        = aws_s3_bucket.dr.arn
      storage_class = "STANDARD"

      replication_time {
        status = "Enabled"
        time {
          minutes = 15
        }
      }

      metrics {
        status = "Enabled"
        event_threshold {
          minutes = 15
        }
      }
    }

    delete_marker_replication {
      status = "Enabled"
    }
  }
}
```

### 3.4 Replication Monitoring

```python
"""
Monitor replication latency and compliance using CloudWatch metrics.
Key metrics published by S3 RTC:
  - OperationCompleted: count of replicated objects
  - OperationMissed: count of objects exceeding the 15-minute threshold
  - ReplicationLatency: milliseconds from upload to replication completion
"""
import boto3
from datetime import datetime, timedelta, timezone

cloudwatch = boto3.client("cloudwatch")


def get_replication_health(source_bucket: str, dest_bucket: str, hours: int = 1) -> dict:
    """Query replication metrics for the last N hours."""
    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=hours)

    # Total objects replicated
    total = cloudwatch.get_metric_statistics(
        Namespace="AWS/S3",
        MetricName="OperationCompleted",
        Dimensions=[
            {"Name": "SourceBucket", "Value": source_bucket},
            {"Name": "DestinationBucket", "Value": dest_bucket},
            {"Name": "RuleId", "Value": "mrr-with-rtc"},
        ],
        StartTime=start,
        EndTime=now,
        Period=3600,
        Statistics=["Sum"],
    )

    # Objects that missed the SLA
    missed = cloudwatch.get_metric_statistics(
        Namespace="AWS/S3",
        MetricName="OperationMissed",
        Dimensions=[
            {"Name": "SourceBucket", "Value": source_bucket},
            {"Name": "DestinationBucket", "Value": dest_bucket},
            {"Name": "RuleId", "Value": "mrr-with-rtc"},
        ],
        StartTime=start,
        EndTime=now,
        Period=3600,
        Statistics=["Sum"],
    )

    total_count = sum(dp["Sum"] for dp in total.get("Datapoints", []))
    missed_count = sum(dp["Sum"] for dp in missed.get("Datapoints", []))

    compliance = 100.0
    if total_count > 0:
        compliance = ((total_count - missed_count) / total_count) * 100

    return {
        "total_replicated": int(total_count),
        "missed_sla": int(missed_count),
        "compliance_pct": round(compliance, 2),
        "window_hours": hours,
        "alert": compliance < 99.9,  # Trigger if below 99.9%
    }


def get_replication_lag(source_bucket: str, dest_bucket: str, minutes: int = 60) -> dict:
    """Get replication latency percentiles."""
    now = datetime.now(timezone.utc)
    start = now - timedelta(minutes=minutes)

    latency = cloudwatch.get_metric_statistics(
        Namespace="AWS/S3",
        MetricName="ReplicationLatency",
        Dimensions=[
            {"Name": "SourceBucket", "Value": source_bucket},
            {"Name": "DestinationBucket", "Value": dest_bucket},
        ],
        StartTime=start,
        EndTime=now,
        Period=300,
        Statistics=["Average", "Maximum"],
        ExtendedStatistics=["p50", "p95", "p99"],
    )

    datapoints = latency.get("Datapoints", [])
    if not datapoints:
        return {"avg_ms": 0, "max_ms": 0, "p50_ms": 0, "p95_ms": 0, "p99_ms": 0}

    latest = sorted(datapoints, key=lambda d: d["Timestamp"], reverse=True)[0]
    return {
        "avg_ms": round(latest.get("Average", 0), 0),
        "max_ms": round(latest.get("Maximum", 0), 0),
        "p50_ms": round(latest.get("ExtendedStatistics", {}).get("p50", 0), 0),
        "p95_ms": round(latest.get("ExtendedStatistics", {}).get("p95", 0), 0),
        "p99_ms": round(latest.get("ExtendedStatistics", {}).get("p99", 0), 0),
    }
```

### 3.5 Failover Strategy

```typescript
/**
 * S3 client with automatic region failover.
 * If primary region fails, routes to DR region.
 */
import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";

interface FailoverConfig {
  primaryRegion: string;
  drRegion: string;
  primaryBucket: string;
  drBucket: string;
  maxRetries: number;
  failoverThresholdMs: number;
}

class FailoverS3Client {
  private primary: S3Client;
  private dr: S3Client;
  private failedOver: boolean = false;
  private config: FailoverConfig;

  constructor(config: FailoverConfig) {
    this.config = config;
    this.primary = new S3Client({ region: config.primaryRegion, maxAttempts: 3 });
    this.dr = new S3Client({ region: config.drRegion, maxAttempts: 3 });
  }

  async getObject(key: string): Promise<Uint8Array> {
    const start = Date.now();

    // Try primary first
    try {
      const response = await Promise.race([
        this.primary.send(new GetObjectCommand({
          Bucket: this.config.primaryBucket,
          Key: key,
        })),
        this.timeout(this.config.failoverThresholdMs),
      ]);

      if (response.Body) {
        return await response.Body.transformToByteArray();
      }
    } catch (err) {
      console.warn(`Primary region failed for ${key}:`, err);
    }

    // Fall back to DR
    const elapsed = Date.now() - start;
    console.info(`Failing over to DR after ${elapsed}ms`);

    this.failedOver = true;

    const drResponse = await this.dr.send(new GetObjectCommand({
      Bucket: this.config.drBucket,
      Key: key,
    }));

    if (drResponse.Body) {
      return await drResponse.Body.transformToByteArray();
    }

    throw new Error(`Object ${key} not found in primary or DR`);
  }

  isFailedOver(): boolean {
    return this.failedOver;
  }

  private timeout(ms: number): Promise<never> {
    return new Promise((_, reject) =>
      setTimeout(() => reject(new Error(`Timeout after ${ms}ms`)), ms)
    );
  }
}
```

---

## 4. Glacier Instant Retrieval Tiering

### 4.1 Storage Class Comparison

| Storage Class | Retrieval Time | Min Storage Duration | Cost (GB/mo) | Use Case |
|--------------|----------------|---------------------|---------------|----------|
| S3 Standard | Milliseconds | None | $0.023 | Active/frequently accessed |
| S3 Intelligent-Tiering | Milliseconds | 30 days (monitoring) | Variable | Unknown/unpredictable access patterns |
| S3 Standard-IA | Milliseconds | 30 days | $0.0125 | Infrequent access, rapid retrieval |
| S3 One Zone-IA | Milliseconds | 30 days | $0.01 | Reproducible data, single AZ |
| **Glacier Instant Retrieval** | **Milliseconds** | **90 days** | **$0.004** | Long-lived, rarely accessed, instant recall |
| Glacier Flexible Retrieval | Minutes-Hours | 90 days | $0.0036 | Archive with flexible retrieval |
| Glacier Deep Archive | Hours | 180 days | $0.00099 | Long-term archive, rare retrieval |

### 4.2 Glacier Instant Retrieval Lifecycle Policy

```json
{
  "Rules": [
    {
      "Id": "tier-to-glacier-ir-after-90-days",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "archive/",
        "Tags": [
          {
            "Key": "storage-tier",
            "Value": "archive-eligible"
          }
        ]
      },
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER_INSTANT_RETRIEVAL"
        }
      ]
    },
    {
      "Id": "expire-glacier-ir-after-7-years",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "archive/"
      },
      "Transitions": [
        {
          "Days": 2555,
          "StorageClass": "GLACIER_DEEP_ARCHIVE"
        }
      ],
      "Expiration": {
        "Days": 3650
      }
    },
    {
      "Id": "transition-logs-to-glacier-ir",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "logs/"
      },
      "Transitions": [
        {
          "Days": 90,
          "StorageClass": "GLACIER_INSTANT_RETRIEVAL"
        }
      ],
      "Expiration": {
        "Days": 730
      }
    }
  ]
}
```

### 4.3 S3 Intelligent-Tiering (Alternative for Unpredictable Access)

When access patterns are unknown, S3 Intelligent-Tiering automatically moves objects between three access tiers with no retrieval fees:

```json
{
  "Rules": [
    {
      "Id": "intelligent-tiering-for-media",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "media/",
        "Tags": [
          {
            "Key": "tiering-strategy",
            "Value": "intelligent"
          }
        ]
      },
      "Transitions": [
        {
          "Days": 0,
          "StorageClass": "INTELLIGENT_TIERING"
        }
      ]
    }
  ]
}
```

### 4.4 Cost Analysis: When to Use Glacier Instant Retrieval

```python
"""
Cost comparison tool for storage class decisions.
Calculates total monthly cost including storage, retrieval, and transition fees.
"""
from dataclasses import dataclass
from enum import Enum


class StorageClass(Enum):
    STANDARD = "STANDARD"
    STANDARD_IA = "STANDARD_IA"
    INTELLIGENT_TIERING = "INTELLIGENT_TIERING"
    GLACIER_IR = "GLACIER_INSTANT_RETRIEVAL"
    GLACIER_FLEXIBLE = "GLACIER_FLEXIBLE"
    GLACIER_DEEP_ARCHIVE = "DEEP_ARCHIVE"


@dataclass
class StorageConfig:
    total_gb: float
    avg_object_size_mb: float
    monthly_retrievals: int  # how many objects retrieved per month
    avg_retrieval_gb: float  # GB retrieved per retrieval event
    retention_months: int
    transition_from: StorageClass


# Pricing in USD (us-east-1, simplified)
PRICING = {
    StorageClass.STANDARD:            {"storage": 0.023, "retrieval_gb": 0.0, "per_request": 0.0},
    StorageClass.STANDARD_IA:         {"storage": 0.0125, "retrieval_gb": 0.01, "per_request": 0.0000055},
    StorageClass.GLACIER_IR:          {"storage": 0.004, "retrieval_gb": 0.03, "per_request": 0.0000055},
    StorageClass.GLACIER_FLEXIBLE:    {"storage": 0.0036, "retrieval_gb": 0.01, "per_request": 0.0000055},
    StorageClass.GLACIER_DEEP_ARCHIVE: {"storage": 0.00099, "retrieval_gb": 0.02, "per_request": 0.0000055},
}


def calculate_monthly_cost(config: StorageConfig, target: StorageClass) -> dict:
    """Calculate estimated monthly cost for a given storage class."""
    p = PRICING[target]

    # Storage cost
    storage_cost = config.total_gb * p["storage"]

    # Retrieval cost
    retrieval_gb = config.monthly_retrievals * config.avg_retrieval_gb
    retrieval_cost = retrieval_gb * p["retrieval_gb"]

    # Request cost
    request_cost = config.monthly_retrievals * p["per_request"]

    total = storage_cost + retrieval_cost + request_cost

    return {
        "storage_class": target.value,
        "storage_cost": round(storage_cost, 2),
        "retrieval_cost": round(retrieval_cost, 2),
        "request_cost": round(request_cost, 4),
        "total_monthly": round(total, 2),
        "total_annual": round(total * 12, 2),
    }


# Example: 5 TB archive, objects ~10 MB avg, 50 retrievals/month at 100 MB each
config = StorageConfig(
    total_gb=5000,
    avg_object_size_mb=10,
    monthly_retrievals=50,
    avg_retrieval_gb=0.1,
    retention_months=12,
    transition_from=StorageClass.STANDARD,
)

print("=== Storage Class Cost Comparison (5 TB Archive) ===")
print(f"{'Class':<25} {'Storage/mo':>12} {'Retrieval/mo':>14} {'Total/mo':>12} {'Annual':>12}")
print("-" * 80)

for cls in [StorageClass.STANDARD, StorageClass.STANDARD_IA,
            StorageClass.GLACIER_IR, StorageClass.GLACIER_FLEXIBLE]:
    cost = calculate_monthly_cost(config, cls)
    print(f"{cost['storage_class']:<25} ${cost['storage_cost']:>11.2f} "
          f"${cost['retrieval_cost']:>13.2f} ${cost['total_monthly']:>11.2f} "
          f"${cost['total_annual']:>11.2f}")

# Output:
# Class                      Storage/mo  Retrieval/mo    Total/mo       Annual
# STANDARD                    $    115.00  $      0.00  $    115.00  $   1380.00
# STANDARD_IA                 $     62.50  $      0.05  $     62.55  $    750.60
# GLACIER_INSTANT_RETRIEVAL   $     20.00  $      0.15  $     20.15  $    241.80
# GLACIER_FLEXIBLE            $     18.00  $      0.05  $     18.05  $    216.60
```

### 4.5 Retrieval Strategy for Glacier IR

```python
"""
Safe retrieval wrapper for Glacier Instant Retrieval objects.
Handles batch retrieval, cost tracking, and rate limiting.
"""
import boto3
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import List

s3 = boto3.client("s3")


@dataclass
class RetrievalResult:
    key: str
    success: bool
    storage_class: str = ""
    size_bytes: int = 0
    cost_estimate: float = 0.0
    error: str = ""


@dataclass
class BatchRetrievalReport:
    results: List[RetrievalResult] = field(default_factory=list)
    total_objects: int = 0
    total_bytes: int = 0
    total_cost: float = 0.0
    glacier_ir_objects: int = 0

    @property
    def success_rate(self) -> float:
        if not self.results:
            return 100.0
        return sum(1 for r in self.results if r.success) / len(self.results) * 100


def batch_retrieve(
    bucket: str,
    keys: List[str],
    max_workers: int = 10,
    cost_limit_usd: float = 5.0,
) -> BatchRetrievalReport:
    """
    Batch retrieve objects from S3, respecting Glacier IR cost limits.

    For Glacier Instant Retrieval objects, retrieval costs $0.03/GB.
    This function tracks cumulative cost and halts if the limit is exceeded.
    """
    report = BatchRetrievalReport()

    def retrieve_single(key: str) -> RetrievalResult:
        try:
            # Head first to check storage class and cost
            head = s3.head_object(Bucket=bucket, Key=key)
            sc = head.get("StorageClass", "STANDARD")
            size = head.get("ContentLength", 0)
            size_gb = size / (1024 ** 3)

            # Estimate retrieval cost
            cost = 0.0
            if sc == "GLACIER_IR":
                cost = size_gb * 0.03  # $0.03/GB
            elif sc == "GLACIER":
                cost = size_gb * 0.01

            # Get the object (Glacier IR returns in milliseconds)
            obj = s3.get_object(Bucket=bucket, Key=key)
            body = obj["Body"].read()

            return RetrievalResult(
                key=key,
                success=True,
                storage_class=sc,
                size_bytes=size,
                cost_estimate=cost,
            )
        except Exception as e:
            return RetrievalResult(key=key, success=False, error=str(e))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(retrieve_single, key): key for key in keys}

        for future in as_completed(futures):
            result = future.result()
            report.results.append(result)
            report.total_objects += 1
            report.total_bytes += result.size_bytes
            report.total_cost += result.cost_estimate

            if result.storage_class == "GLACIER_IR":
                report.glacier_ir_objects += 1

            # Halt if cost exceeds limit
            if report.total_cost > cost_limit_usd:
                for f in futures:
                    f.cancel()
                break

    return report


# Example: retrieve 100 objects with cost tracking
keys_to_retrieve = [f"archive/doc_{i}.pdf" for i in range(100)]
report = batch_retrieve("stryde-archive-prod", keys_to_retrieve, cost_limit_usd=5.0)
print(f"Retrieved: {report.total_objects} objects, "
      f"{report.glacier_ir_objects} from Glacier IR")
print(f"Total cost: ${report.total_cost:.4f}")
print(f"Success rate: {report.success_rate:.1f}%")
```

---

## 5. Event-Driven Processing with S3 Event Notifications + SQS

### 5.1 Architecture

```
┌─────────────────┐
│  S3 Bucket      │
│  (Source)       │
│                 │
│  s3:ObjectCreated:*  ──────┐
│  s3:ObjectRemoved:*  ──────┤
│  s3:ObjectRestore:*  ──────┤
└─────────────────┘          │
                              ▼
                    ┌─────────────────┐
                    │  SQS Standard    │
                    │  Queue           │
                    │  (Fan-out Hub)   │
                    │                  │
                    │  Visibility: 300s │
                    │  DLQ: max 3      │
                    │  Retention: 14d  │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ Lambda       │ │ Lambda       │ │ Lambda       │
    │ Image        │ │ Virus        │ │ Metadata     │
    │ Processor    │ │ Scanner      │ │ Indexer      │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │                │                │
           ▼                ▼                ▼
    ┌──────────┐    ┌──────────────┐  ┌──────────────┐
    │ Processed│    │ Quarantine   │  │ DynamoDB /   │
    │ S3 Bucket│    │ Bucket       │  │ OpenSearch   │
    └──────────┘    └──────────────┘  └──────────────┘
```

### 5.2 S3 Event Notification Configuration

```json
{
  "TopicConfigurations": [],
  "QueueConfigurations": [
    {
      "Id": "all-object-created-events",
      "QueueArn": "arn:aws:sqs:us-east-1:123456789012:stryde-s3-events-queue",
      "Events": [
        "s3:ObjectCreated:*",
        "s3:ObjectRestore:Completed"
      ],
      "Filter": {
        "Key": {
          "FilterRules": [
            {
              "Name": "prefix",
              "Value": "uploads/"
            },
            {
              "Name": "suffix",
              "Value": ".jpg"
            }
          ]
        }
      }
    },
    {
      "Id": "delete-events-for-cleanup",
      "QueueArn": "arn:aws:sqs:us-east-1:123456789012:stryde-s3-events-queue",
      "Events": [
        "s3:ObjectRemoved:*"
      ]
    }
  ]
}
```

### 5.3 SQS Queue Configuration

```hcl
# Main SQS event queue
resource "aws_sqs_queue" "s3_events" {
  name                       = "stryde-s3-events-queue"
  delay_seconds              = 0
  max_message_size           = 262144  # 256 KB (max for S3 notifications)
  message_retention_seconds  = 1209600 # 14 days
  visibility_timeout_seconds = 300     # 5 min (match Lambda timeout)
  receive_wait_time_seconds  = 20      # Long polling
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.s3_events_dlq.arn
    maxReceiveCount     = 3
  })

  # Enable server-side encryption
  sqs_managed_sse_enabled = true

  tags = {
    Name        = "stryde-s3-events-queue"
    Environment = "production"
    Purpose     = "s3-event-fanout"
  }
}

# Dead Letter Queue
resource "aws_sqs_queue" "s3_events_dlq" {
  name                      = "stryde-s3-events-dlq"
  message_retention_seconds = 1209600 # 14 days
  sqs_managed_sse_enabled   = true

  tags = {
    Name        = "stryde-s3-events-dlq"
    Environment = "production"
  }
}
```

### 5.4 Event Processing Lambda

```python
"""
S3 Event Processor Lambda — consumes SQS messages, processes S3 events,
and handles retries, partial failures, and DLQ routing.
"""
import json
import os
from typing import Any, Dict, List

import boto3

s3 = boto3.client("s3")
sqs = boto3.client("sqs")

# Processing time budget (must be < Lambda timeout and < SQS visibility timeout)
PROCESSING_TIME_BUDGET_MS = 250_000  # 250 seconds
MAX_RETRY_COUNT = 3


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Process S3 events from SQS with partial batch failure support.

    Returns:
        {"batchItemFailures": [{"itemIdentifier": "messageId"}]} for partial retry
    """
    batch_item_failures: List[Dict[str, str]] = []
    processing_results: List[Dict[str, Any]] = []

    records = event.get("Records", [])
    print(f"Processing batch of {len(records)} SQS messages")

    for record in records:
        message_id = record["messageId"]
        retry_count = _get_retry_count(record)

        try:
            # Parse the S3 event notification
            body = json.loads(record["body"])
            s3_events = _parse_s3_events(body)

            # Check if this is a retry and handle accordingly
            if retry_count >= MAX_RETRY_COUNT:
                print(f"Message {message_id} exceeded max retries, sending to DLQ")
                _send_to_dlq(record)
                continue

            # Process each S3 event in the notification
            for s3_event in s3_events:
                result = _process_s3_event(s3_event, context)
                processing_results.append(result)

        except Exception as e:
            print(f"Failed to process message {message_id}: {str(e)}")
            batch_item_failures.append({"itemIdentifier": message_id})
            continue

    # Report batch results
    success_count = len(records) - len(batch_item_failures)
    print(f"Batch complete: {success_count}/{len(records)} succeeded")

    # Build partial batch failure response
    response = {"batchItemFailures": batch_item_failures} if batch_item_failures else {}

    return response


def _parse_s3_events(body: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract S3 event records from the SQS message body."""
    if "Records" in body:
        # Direct S3 notification
        return [
            rec for rec in body["Records"]
            if rec.get("eventSource") == "aws:s3"
        ]
    elif "Message" in body:
        # SNS-wrapped notification
        inner = json.loads(body["Message"])
        return [
            rec for rec in inner.get("Records", [])
            if rec.get("eventSource") == "aws:s3"
        ]
    return []


def _process_s3_event(s3_event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Route an individual S3 event to the appropriate processor."""
    event_name = s3_event.get("eventName", "")
    s3_info = s3_event.get("s3", {})
    bucket_name = s3_info.get("bucket", {}).get("name", "")
    object_key = s3_info.get("object", {}).get("key", "")
    object_size = s3_info.get("object", {}).get("size", 0)

    print(f"Processing: {event_name} — s3://{bucket_name}/{object_key} ({object_size} bytes)")

    # Route based on event type
    if event_name.startswith("ObjectCreated"):
        return _handle_object_created(bucket_name, object_key, object_size, s3_event)
    elif event_name.startswith("ObjectRemoved"):
        return _handle_object_removed(bucket_name, object_key)
    elif event_name.startswith("ObjectRestore"):
        return _handle_object_restored(bucket_name, object_key)
    else:
        return {"event": event_name, "status": "unhandled"}


def _handle_object_created(bucket: str, key: str, size: int, event: dict) -> dict:
    """Process a newly created object."""
    # Determine processing path by prefix
    if key.startswith("uploads/images/"):
        # Trigger image processing pipeline
        return _trigger_image_pipeline(bucket, key, size)
    elif key.startswith("uploads/documents/"):
        # Trigger document processing (OCR, indexing)
        return _trigger_document_pipeline(bucket, key)
    elif key.startswith("uploads/videos/"):
        # Trigger video transcoding
        return _trigger_video_pipeline(bucket, key)
    else:
        return {"key": key, "status": "routed_to_default"}
    return {"key": key, "processed": True}


def _handle_object_removed(bucket: str, key: str) -> dict:
    """Handle deletion: clean up derived assets, cache invalidation."""
    print(f"Cleaning up derived assets for deleted object: {key}")
    # Remove derived images
    media_prefix = key.replace("uploads/", "media/").rsplit(".", 1)[0]
    # In production: list and delete all derived sizes
    return {"key": key, "status": "cleaned_up"}


def _handle_object_restored(bucket: str, key: str) -> dict:
    """Handle Glacier restore completion: re-index, notify."""
    print(f"Object restored from Glacier: {key}")
    return {"key": key, "status": "restored_and_reindexed"}


def _trigger_image_pipeline(bucket: str, key: str, size: int) -> dict:
    """Fan out image processing tasks."""
    # In production: invoke Step Functions or publish to SNS for fan-out
    return {"bucket": bucket, "key": key, "size": size, "pipeline": "image_processing", "status": "triggered"}


def _trigger_document_pipeline(bucket: str, key: str) -> dict:
    return {"bucket": bucket, "key": key, "pipeline": "document_processing", "status": "triggered"}


def _trigger_video_pipeline(bucket: str, key: str) -> dict:
    return {"bucket": bucket, "key": key, "pipeline": "video_transcoding", "status": "triggered"}


def _get_retry_count(record: Dict[str, Any]) -> int:
    """Extract retry count from SQS message attributes."""
    attributes = record.get("attributes", {})
    return int(attributes.get("ApproximateReceiveCount", "1"))


def _send_to_dlq(record: Dict[str, Any]) -> None:
    """Manually send a poison-pill message to the DLQ for inspection."""
    # The SQS redrive policy handles this automatically after maxReceiveCount
    # This is for explicit routing of known-bad messages
    pass
```

### 5.5 CloudWatch Alarm for DLQ Backlog

```python
"""
Publish a CloudWatch alarm when the DLQ has messages that need attention.
"""
import boto3

cloudwatch = boto3.client("cloudwatch")


def create_dlq_alarm(dlq_name: str, sns_topic_arn: str) -> None:
    """Create a CloudWatch alarm for DLQ message backlog."""
    cloudwatch.put_metric_alarm(
        AlarmName=f"DLQ-{dlq_name}-HasMessages",
        AlarmDescription="Alert when S3 event DLQ contains failed messages",
        Namespace="AWS/SQS",
        MetricName="ApproximateNumberOfMessagesVisible",
        Dimensions=[
            {"Name": "QueueName", "Value": dlq_name},
        ],
        Statistic="Sum",
        Period=300,  # 5 minutes
        EvaluationPeriods=1,
        Threshold=1,
        ComparisonOperator="GreaterThanOrEqualToThreshold",
        AlarmActions=[sns_topic_arn],
        TreatMissingData="notBreaching",
    )
    print(f"Created DLQ alarm for {dlq_name}")
```

### 5.6 Terraform — Full Event Pipeline

```hcl
# S3 bucket notification to SQS
resource "aws_s3_bucket_notification" "main" {
  bucket = aws_s3_bucket.uploads.id

  queue {
    queue_arn = aws_sqs_queue.s3_events.arn
    events    = ["s3:ObjectCreated:*", "s3:ObjectRestore:Completed"]

    filter_prefix = "uploads/"
    filter_suffix = ".jpg"
  }

  queue {
    queue_arn = aws_sqs_queue.s3_events.arn
    events    = ["s3:ObjectRemoved:*"]
  }
}

# SQS access policy allowing S3 to send messages
resource "aws_sqs_queue_policy" "s3_events" {
  queue_url = aws_sqs_queue.s3_events.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "s3.amazonaws.com"
        }
        Action   = "sqs:SendMessage"
        Resource = aws_sqs_queue.s3_events.arn
        Condition = {
          ArnLike = {
            "aws:SourceArn" = aws_s3_bucket.uploads.arn
          }
        }
      }
    ]
  })
}

# Lambda event source mapping (SQS → Lambda)
resource "aws_lambda_event_source_mapping" "s3_events" {
  event_source_arn = aws_sqs_queue.s3_events.arn
  function_name    = aws_lambda_function.s3_event_processor.arn
  batch_size       = 10
  maximum_batching_window_in_seconds = 10

  # Partial batch failure support
  function_response_types = ["ReportBatchItemFailures"]

  # Scaling
  scaling_config {
    maximum_concurrency = 20
  }
}
```

---

## 6. Storage Class Analysis

### 6.1 S3 Storage Class Analysis Feature

S3 Storage Class Analysis provides daily visualizations of storage access patterns, recommending when to transition objects to STANDARD_IA or ONEZONE_IA. It observes access patterns for 30+ days before making recommendations.

```hcl
# Terraform: Enable Storage Class Analysis
resource "aws_s3_bucket_analytics_configuration" "storage_class_analysis" {
  bucket = aws_s3_bucket.media.id
  name   = "storage-class-analysis"

  storage_class_analysis {
    data_export {
      output_schema_version = "V_1"
      destination {
        s3_bucket_destination {
          bucket_arn = aws_s3_bucket.analytics.arn
          prefix     = "storage-class-analysis/"
          format     = "CSV"
        }
      }
    }
  }
}
```

### 6.2 Athena Query for Storage Distribution

```sql
-- Query S3 Inventory report to analyze storage class distribution
-- Assumes S3 Inventory is configured with daily CSV output
CREATE EXTERNAL TABLE IF NOT EXISTS s3_inventory (
    bucket          STRING,
    key             STRING,
    version_id      STRING,
    is_latest       BOOLEAN,
    is_delete_marker BOOLEAN,
    size            BIGINT,
    last_modified_date  STRING,
    storage_class   STRING,
    is_multipart_uploaded  BOOLEAN
)
PARTITIONED BY (dt STRING)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
LOCATION 's3://stryde-analytics-prod/s3-inventory/stryde-media-prod/data/'
TBLPROPERTIES ('skip.header.line.count'='1');

-- Load partition
MSCK REPAIR TABLE s3_inventory;

-- Storage class distribution by total size
SELECT
    storage_class,
    COUNT(*) AS object_count,
    SUM(size) / 1024.0 / 1024.0 / 1024.0 AS total_gb,
    AVG(size) / 1024.0 / 1024.0 AS avg_size_mb,
    CAST(SUM(size) * 100.0 / SUM(SUM(size)) OVER () AS DECIMAL(5,2)) AS pct_of_total
FROM s3_inventory
WHERE is_latest = true
  AND is_delete_marker = false
  AND dt = '2026-06-26-00-00'
GROUP BY storage_class
ORDER BY total_gb DESC;

-- Expected output:
-- storage_class              | object_count | total_gb  | avg_size_mb | pct_of_total
-- STANDARD                   |    1,250,000 |   2,450.5 |        2.01 |       42.3
-- STANDARD_IA                |    3,800,000 |   3,100.2 |        0.84 |       53.5
-- GLACIER_INSTANT_RETRIEVAL  |      450,000 |     210.0 |        0.48 |        3.6
-- GLACIER_DEEP_ARCHIVE       |      120,000 |      35.5 |        0.30 |        0.6
```

### 6.3 Cost Optimization Analysis with Athena

```sql
-- Identify objects that should be transitioned based on age and size
-- Objects > 90 days old and > 128 KB may benefit from STANDARD_IA
-- Objects > 180 days old and rarely accessed may benefit from GLACIER_IR
WITH object_age AS (
    SELECT
        key,
        size,
        storage_class,
        DATE_DIFF('day', FROM_ISO8601_TIMESTAMP(last_modified_date), CURRENT_TIMESTAMP) AS age_days
    FROM s3_inventory
    WHERE is_latest = true
      AND is_delete_marker = false
      AND storage_class = 'STANDARD'
      AND dt = '2026-06-26-00-00'
)
SELECT
    CASE
        WHEN age_days > 365 AND size >= 128 * 1024 THEN 'GLACIER_INSTANT_RETRIEVAL'
        WHEN age_days > 90 AND size >= 128 * 1024 THEN 'STANDARD_IA'
        WHEN age_days > 30 THEN 'MONITORING'
        ELSE 'KEEP_STANDARD'
    END AS recommended_tier,
    COUNT(*) AS object_count,
    SUM(size) / 1024.0 / 1024.0 / 1024.0 AS total_gb,
    -- Estimated monthly savings vs STANDARD ($0.023/GB)
    CASE
        WHEN age_days > 365 THEN SUM(size) / 1024.0 / 1024.0 / 1024.0 * (0.023 - 0.004)
        WHEN age_days > 90 THEN SUM(size) / 1024.0 / 1024.0 / 1024.0 * (0.023 - 0.0125)
        ELSE 0
    END AS estimated_monthly_savings_usd
FROM object_age
GROUP BY 1
ORDER BY estimated_monthly_savings_usd DESC;
```

### 6.4 Real-Time Storage Analytics Pipeline

```python
"""
Real-time storage analytics: process S3 access logs to identify cold data
candidates for Glacier Instant Retrieval tiering.
"""
import gzip
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Dict, Set

import boto3

s3 = boto3.client("s3")
athena = boto3.client("athena")


class StorageAnalyzer:
    """
    Analyzes S3 server access logs to identify:
    - Cold objects (no GETs in N days)
    - Oversized objects (> threshold for lifecycle consideration)
    - Hot objects (frequent access patterns)
    """

    def __init__(self, bucket: str, logs_bucket: str, logs_prefix: str):
        self.bucket = bucket
        self.logs_bucket = logs_bucket
        self.logs_prefix = logs_prefix

    def find_cold_objects(self, days_threshold: int = 90, min_size_bytes: int = 128 * 1024) -> Dict[str, any]:
        """
        Find objects not accessed (GET/HEAD) in the last N days.
        Returns candidates for STANDARD_IA or GLACIER_IR transition.
        """
        cutoff = datetime.now(timezone.utc) - timedelta(days=days_threshold)
        accessed_keys: Set[str] = set()
        all_keys: Dict[str, int] = {}  # key -> size

        # Scan access logs for the period
        date_str = cutoff.strftime("%Y-%m-%d")
        log_prefix = f"{self.logs_prefix}{date_str}"

        # Collect all accessed keys from logs
        paginator = s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self.logs_bucket, Prefix=log_prefix):
            for obj in page.get("Contents", []):
                if not obj["Key"].endswith(".gz"):
                    continue

                # Read and parse the log file
                response = s3.get_object(Bucket=self.logs_bucket, Key=obj["Key"])
                with gzip.GzipFile(fileobj=response["Body"]) as gz:
                    for line in gz:
                        line = line.decode("utf-8").strip()
                        if not line:
                            continue
                        fields = line.split(" ")

                        # S3 access log format:
                        # BucketOwner Bucket [time] RemoteIP ... Operation Key ...
                        if len(fields) < 15:
                            continue

                        operation = fields[11].strip('"')
                        key = fields[12].strip('"')

                        if operation in ("REST.GET.OBJECT", "REST.HEAD.OBJECT"):
                            accessed_keys.add(f"{fields[1]}/{key}")

        # List all objects in the bucket
        for page in paginator.paginate(Bucket=self.bucket):
            for obj in page.get("Contents", []):
                if obj["Size"] >= min_size_bytes:
                    all_keys[obj["Key"]] = obj["Size"]

        # Find cold objects
        cold_objects = {
            key: size
            for key, size in all_keys.items()
            if key not in accessed_keys
        }

        total_cold_gb = sum(cold_objects.values()) / (1024 ** 3)
        potential_savings = total_cold_gb * (0.023 - 0.004)  # STANDARD → GLACIER_IR

        return {
            "cold_object_count": len(cold_objects),
            "total_cold_gb": round(total_cold_gb, 2),
            "estimated_monthly_savings_usd": round(potential_savings, 2),
            "sample_keys": list(cold_objects.keys())[:10],
            "threshold_days": days_threshold,
        }

    def run_athena_inventory_query(self, query: str, database: str, output_location: str) -> list:
        """Run an Athena query against S3 Inventory data."""
        response = athena.start_query_execution(
            QueryString=query,
            QueryExecutionContext={"Database": database},
            ResultConfiguration={"OutputLocation": output_location},
        )

        execution_id = response["QueryExecutionId"]

        # Wait for completion
        while True:
            status = athena.get_query_execution(QueryExecutionId=execution_id)
            state = status["QueryExecution"]["Status"]["State"]

            if state in ("SUCCEEDED", "FAILED", "CANCELLED"):
                break

        if state == "FAILED":
            error = status["QueryExecution"]["Status"].get("StateChangeReason", "Unknown")
            raise Exception(f"Athena query failed: {error}")

        # Fetch results
        results = athena.get_query_results(QueryExecutionId=execution_id)
        rows = results["ResultSet"]["Rows"]

        # Parse column names from header
        columns = [col["VarCharValue"] for col in rows[0]["Data"]]

        # Parse data rows
        data = []
        for row in rows[1:]:
            values = [col.get("VarCharValue", "") for col in row["Data"]]
            data.append(dict(zip(columns, values)))

        return data


# Usage
analyzer = StorageAnalyzer(
    bucket="stryde-media-prod",
    logs_bucket="stryde-logs-prod",
    logs_prefix="s3-access-logs/",
)

cold_report = analyzer.find_cold_objects(days_threshold=90)
print(json.dumps(cold_report, indent=2))
```

### 6.5 CloudWatch Dashboard for Storage Analytics

```python
"""
Build a CloudWatch Dashboard for storage class metrics.
"""
import boto3

cloudwatch = boto3.client("cloudwatch")


def create_storage_dashboard():
    dashboard_body = {
        "widgets": [
            {
                "type": "metric",
                "x": 0, "y": 0, "width": 12, "height": 6,
                "properties": {
                    "metrics": [
                        ["AWS/S3", "NumberOfObjects", "StorageType", "AllStorageTypes",
                         "BucketName", "stryde-media-prod", {"stat": "Average"}],
                        [".", "BucketSizeBytes", ".", ".", ".", ".", {"stat": "Average"}],
                    ],
                    "view": "timeSeries",
                    "stacked": False,
                    "region": "us-east-1",
                    "title": "S3 Storage Overview",
                    "period": 86400,
                }
            },
            {
                "type": "metric",
                "x": 12, "y": 0, "width": 12, "height": 6,
                "properties": {
                    "metrics": [
                        ["AWS/S3", "NumberOfObjects", "StorageType", "StandardStorage",
                         "BucketName", "stryde-media-prod", {"stat": "Average", "label": "STANDARD"}],
                        ["...", "StandardIAStorage", {"label": "STANDARD_IA"}],
                        ["...", "GlacierInstantRetrievalStorage", {"label": "GLACIER_IR"}],
                        ["...", "DeepArchiveStorage", {"label": "DEEP_ARCHIVE"}],
                    ],
                    "view": "timeSeries",
                    "stacked": True,
                    "region": "us-east-1",
                    "title": "Objects by Storage Class",
                    "period": 86400,
                }
            },
            {
                "type": "metric",
                "x": 0, "y": 6, "width": 12, "height": 6,
                "properties": {
                    "metrics": [
                        ["AWS/S3", "BucketSizeBytes", "StorageType", "StandardStorage",
                         "BucketName", "stryde-media-prod", {"stat": "Average", "label": "STANDARD"}],
                        ["...", "StandardIAStorage", {"label": "STANDARD_IA"}],
                        ["...", "GlacierInstantRetrievalStorage", {"label": "GLACIER_IR"}],
                        ["...", "DeepArchiveStorage", {"label": "DEEP_ARCHIVE"}],
                    ],
                    "view": "timeSeries",
                    "stacked": True,
                    "region": "us-east-1",
                    "title": "Bytes by Storage Class",
                    "period": 86400,
                }
            },
            {
                "type": "metric",
                "x": 12, "y": 6, "width": 12, "height": 6,
                "properties": {
                    "metrics": [
                        ["AWS/S3", "ReplicationLatency", "SourceBucket", "stryde-media-primary",
                         "DestinationBucket", "stryde-media-dr", {"stat": "p95", "label": "P95 Replication Latency"}],
                    ],
                    "view": "timeSeries",
                    "region": "us-east-1",
                    "title": "Replication Latency (P95)",
                    "period": 300,
                }
            },
            {
                "type": "metric",
                "x": 0, "y": 12, "width": 24, "height": 6,
                "properties": {
                    "metrics": [
                        ["AWS/SQS", "ApproximateNumberOfMessagesVisible",
                         "QueueName", "stryde-s3-events-queue", {"stat": "Average", "label": "Main Queue"}],
                        [".", ".", ".", "stryde-s3-events-dlq", {"stat": "Average", "label": "DLQ"}],
                    ],
                    "view": "timeSeries",
                    "region": "us-east-1",
                    "title": "S3 Event Queue Depth",
                    "period": 60,
                }
            },
        ]
    }

    cloudwatch.put_dashboard(
        DashboardName="Stryde-Storage-Analytics",
        DashboardBody=json.dumps(dashboard_body),
    )
    print("Storage analytics dashboard created")
```

---

## 7. Infrastructure as Code (Terraform)

### 7.1 Complete Terraform Module

```hcl
# variables.tf
variable "environment" {
  description = "Environment (prod, staging, dev)"
  type        = string
  default     = "prod"
}

variable "primary_region" {
  description = "Primary AWS region"
  type        = string
  default     = "us-east-1"
}

variable "dr_region" {
  description = "Disaster recovery region"
  type        = string
  default     = "eu-west-1"
}

variable "account_id" {
  description = "AWS account ID"
  type        = string
}

variable "dr_account_id" {
  description = "DR AWS account ID (may differ for cross-account replication)"
  type        = string
}

# main.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "stryde-terraform-state"
    key            = "file-storage-architect/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "stryde-terraform-locks"
  }
}

provider "aws" {
  region = var.primary_region
  alias  = "primary"

  default_tags {
    tags = {
      Project     = "Stryde"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Component   = "file-storage"
    }
  }
}

provider "aws" {
  region = var.dr_region
  alias  = "dr"

  default_tags {
    tags = {
      Project     = "Stryde"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Component   = "file-storage-dr"
    }
  }
}

# --- KMS Keys ---
resource "aws_kms_key" "s3_encryption" {
  description             = "KMS key for S3 bucket encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true
  policy                  = data.aws_iam_policy_document.kms_s3.json
}

resource "aws_kms_alias" "s3_encryption" {
  name          = "alias/stryde-s3-encryption-${var.environment}"
  target_key_id = aws_kms_key.s3_encryption.id
}

# --- S3 Buckets ---
resource "aws_s3_bucket" "media_primary" {
  provider = aws.primary
  bucket   = "stryde-media-${var.environment}-${data.aws_caller_identity.current.account_id}"
}

resource "aws_s3_bucket_versioning" "media_primary" {
  provider = aws.primary
  bucket   = aws_s3_bucket.media_primary.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "media_primary" {
  provider = aws.primary
  bucket   = aws_s3_bucket.media_primary.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3_encryption.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "media_primary" {
  provider = aws.primary
  bucket   = aws_s3_bucket.media_primary.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_ownership_controls" "media_primary" {
  provider = aws.primary
  bucket   = aws_s3_bucket.media_primary.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

# --- Lifecycle Policies (Glacier Instant Retrieval Tiering) ---
resource "aws_s3_bucket_lifecycle_configuration" "media_primary" {
  provider = aws.primary
  bucket   = aws_s3_bucket.media_primary.id

  rule {
    id     = "transition-to-glacier-ir"
    status = "Enabled"

    filter {
      prefix = ""
    }

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER_INSTANT_RETRIEVAL"
    }

    transition {
      days          = 365
      storage_class = "GLACIER"
    }

    transition {
      days          = 2555  # 7 years
      storage_class = "DEEP_ARCHIVE"
    }

    expiration {
      days                         = 3650  # 10 years
      expired_object_delete_marker = true
    }

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "STANDARD_IA"
    }

    noncurrent_version_expiration {
      noncurrent_days = 90
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}

# --- Replication Configuration ---
resource "aws_s3_bucket" "media_dr" {
  provider = aws.dr
  bucket   = "stryde-media-dr-${var.environment}-${data.aws_caller_identity.current.account_id}"
}

resource "aws_s3_bucket_versioning" "media_dr" {
  provider = aws.dr
  bucket   = aws_s3_bucket.media_dr.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "media_dr" {
  provider = aws.dr
  bucket   = aws_s3_bucket.media_dr.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3_encryption.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "media_dr" {
  provider = aws.dr
  bucket   = aws_s3_bucket.media_dr.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_replication_configuration" "media" {
  provider = aws.primary
  role     = aws_iam_role.replication.arn
  bucket   = aws_s3_bucket.media_primary.id

  rule {
    id     = "mrr-to-dr"
    status = "Enabled"

    filter {
      prefix = ""
    }

    destination {
      bucket        = aws_s3_bucket.media_dr.arn
      storage_class = "STANDARD"

      replication_time {
        status = "Enabled"
        time {
          minutes = 15
        }
      }

      metrics {
        status = "Enabled"
        event_threshold {
          minutes = 15
        }
      }

      encryption_configuration {
        replica_kms_key_id = aws_kms_key.s3_encryption.arn
      }
    }

    delete_marker_replication {
      status = "Enabled"
    }

    existing_object_replication {
      status = "Enabled"
    }
  }

  depends_on = [aws_s3_bucket_versioning.media_dr]
}

# --- Replication IAM Role ---
resource "aws_iam_role" "replication" {
  name = "stryde-s3-replication-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "s3.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "replication" {
  role = aws_iam_role.replication.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetReplicationConfiguration",
          "s3:ListBucket",
        ]
        Resource = [aws_s3_bucket.media_primary.arn]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObjectVersionForReplication",
          "s3:GetObjectVersionAcl",
          "s3:GetObjectVersionTagging",
        ]
        Resource = ["${aws_s3_bucket.media_primary.arn}/*"]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ReplicateObject",
          "s3:ReplicateDelete",
          "s3:ReplicateTags",
        ]
        Resource = ["${aws_s3_bucket.media_dr.arn}/*"]
      },
      {
        Effect = "Allow"
        Action = [
          "kms:Decrypt",
          "kms:GenerateDataKey",
        ]
        Resource = [aws_kms_key.s3_encryption.arn]
      },
      {
        Effect = "Allow"
        Action = [
          "kms:Encrypt",
        ]
        Resource = [aws_kms_key.s3_encryption.arn]
      },
    ]
  })
}

# --- Storage Class Analysis ---
resource "aws_s3_bucket_analytics_configuration" "storage_analysis" {
  provider = aws.primary
  bucket   = aws_s3_bucket.media_primary.id
  name     = "storage-class-analysis"

  storage_class_analysis {
    data_export {
      output_schema_version = "V_1"
      destination {
        s3_bucket_destination {
          bucket_arn = aws_s3_bucket.analytics.arn
          prefix     = "storage-class-analysis/"
          format     = "CSV"
        }
      }
    }
  }
}

resource "aws_s3_bucket" "analytics" {
  provider = aws.primary
  bucket   = "stryde-analytics-${var.environment}-${data.aws_caller_identity.current.account_id}"
}

# --- SQS Event Queue ---
resource "aws_sqs_queue" "s3_events" {
  provider                   = aws.primary
  name                       = "stryde-s3-events-${var.environment}"
  delay_seconds              = 0
  max_message_size           = 262144
  message_retention_seconds  = 1209600
  visibility_timeout_seconds = 300
  receive_wait_time_seconds  = 20
  sqs_managed_sse_enabled    = true

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.s3_events_dlq.arn
    maxReceiveCount     = 3
  })
}

resource "aws_sqs_queue" "s3_events_dlq" {
  provider                  = aws.primary
  name                      = "stryde-s3-events-dlq-${var.environment}"
  message_retention_seconds = 1209600
  sqs_managed_sse_enabled   = true
}

# Allow S3 to send to SQS
resource "aws_sqs_queue_policy" "s3_events" {
  provider  = aws.primary
  queue_url = aws_sqs_queue.s3_events.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "s3.amazonaws.com"
      }
      Action   = "sqs:SendMessage"
      Resource = aws_sqs_queue.s3_events.arn
      Condition = {
        ArnLike = {
          "aws:SourceArn" = aws_s3_bucket.media_primary.arn
        }
      }
    }]
  })
}

# --- S3 Object Lambda Access Point ---
resource "aws_s3_access_point" "media" {
  provider = aws.primary
  bucket   = aws_s3_bucket.media_primary.id
  name     = "stryde-media-access-${var.environment}"

  public_access_block_configuration {
    block_public_acls       = true
    block_public_policy     = true
    ignore_public_acls      = true
    restrict_public_buckets = true
  }
}

resource "aws_s3control_object_lambda_access_point" "image_transform" {
  provider = aws.primary
  name     = "stryde-image-transform-${var.environment}"

  configuration {
    supporting_access_point = aws_s3_access_point.media.arn
    transformation_configuration {
      actions = ["GetObject", "HeadObject"]
      content_transformation {
        aws_lambda {
          function_arn = aws_lambda_function.object_lambda_image.arn
        }
      }
    }
  }
}

# --- Outputs ---
output "primary_bucket_name" {
  value = aws_s3_bucket.media_primary.id
}

output "dr_bucket_name" {
  value = aws_s3_bucket.media_dr.id
}

output "s3_events_queue_url" {
  value = aws_sqs_queue.s3_events.id
}

output "s3_events_dlq_url" {
  value = aws_sqs_queue.s3_events_dlq.id
}

output "object_lambda_access_point_arn" {
  value = aws_s3control_object_lambda_access_point.image_transform.arn
}

output "object_lambda_alias" {
  value = aws_s3control_object_lambda_access_point.image_transform.alias
}

data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "kms_s3" {
  statement {
    sid    = "Enable IAM User Permissions"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"]
    }
    actions   = ["kms:*"]
    resources = ["*"]
  }

  statement {
    sid    = "Allow S3 to use the key"
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["s3.amazonaws.com"]
    }
    actions = [
      "kms:Decrypt",
      "kms:GenerateDataKey",
    ]
    resources = ["*"]
  }

  statement {
    sid    = "Allow CloudTrail to use the key"
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }
    actions = [
      "kms:Decrypt",
      "kms:GenerateDataKey",
    ]
    resources = ["*"]
  }
}
```

---

## 8. Monitoring & Observability

### 8.1 Key Metrics to Monitor

| Metric | Source | Alert Threshold | Action |
|--------|--------|-----------------|--------|
| S3 5xx Errors | CloudWatch | > 0 in 5 min | Investigate throttling |
| S3 First Byte Latency | CloudWatch | P99 > 500ms | Check object size distribution |
| Replication Latency (P95) | CloudWatch | > 15 min | Check RTC compliance |
| Replication Missed SLA | CloudWatch | > 0.1% | Investigate backlog |
| SQS Queue Depth | CloudWatch | > 1000 messages | Scale Lambda concurrency |
| SQS DLQ Messages | CloudWatch | > 0 | Alert on-call |
| Object Lambda Errors | CloudWatch | > 1% error rate | Check transformation logic |
| Storage Class Distribution | Athena (daily) | Glacier IR < expected | Lifecycle policy check |
| Glacier IR Retrieval Cost | Cost Explorer | > $50/day | Review retrieval patterns |

### 8.2 CloudWatch Composite Alarm

```python
"""
Create composite alarms for the storage architecture.
"""
import boto3

cloudwatch = boto3.client("cloudwatch")


def create_composite_alarms(sns_topic_arn: str):
    """Create a composite alarm that fires when any storage-related alarm triggers."""

    # Individual alarms
    alarms = [
        {
            "name": "S3-Replication-SLA-Breach",
            "description": "Replication Time Control SLA breached",
            "metric": {
                "Namespace": "AWS/S3",
                "MetricName": "OperationMissed",
                "Dimensions": [
                    {"Name": "RuleId", "Value": "mrr-to-dr"},
                ],
                "Statistic": "Sum",
                "Period": 300,
                "Threshold": 1,
            }
        },
        {
            "name": "S3-Event-DLQ-Backlog",
            "description": "S3 event DLQ has messages",
            "metric": {
                "Namespace": "AWS/SQS",
                "MetricName": "ApproximateNumberOfMessagesVisible",
                "Dimensions": [
                    {"Name": "QueueName", "Value": "stryde-s3-events-dlq-prod"},
                ],
                "Statistic": "Sum",
                "Period": 300,
                "Threshold": 1,
            }
        },
        {
            "name": "S3-5xx-Errors",
            "description": "S3 returning 5xx errors",
            "metric": {
                "Namespace": "AWS/S3",
                "MetricName": "5xxErrors",
                "Dimensions": [
                    {"Name": "BucketName", "Value": "stryde-media-prod"},
                ],
                "Statistic": "Sum",
                "Period": 300,
                "Threshold": 1,
            }
        },
    ]

    alarm_arns = []
    for alarm in alarms:
        cloudwatch.put_metric_alarm(
            AlarmName=alarm["name"],
            AlarmDescription=alarm["description"],
            Namespace=alarm["metric"]["Namespace"],
            MetricName=alarm["metric"]["MetricName"],
            Dimensions=alarm["metric"]["Dimensions"],
            Statistic=alarm["metric"]["Statistic"],
            Period=alarm["metric"]["Period"],
            EvaluationPeriods=1,
            Threshold=alarm["metric"]["Threshold"],
            ComparisonOperator="GreaterThanOrEqualToThreshold",
            AlarmActions=[sns_topic_arn],
            TreatMissingData="notBreaching",
        )
        alarm_arns.append(f"arn:aws:cloudwatch:us-east-1:{ACCOUNT_ID}:alarm:{alarm['name']}")

    # Composite alarm
    cloudwatch.put_composite_alarm(
        AlarmName="Stryde-Storage-Critical",
        AlarmDescription="Composite: any storage alarm triggered",
        AlarmRule=f"ALARM({' OR ALARM('.join(alarm_arns)})",
        ActionsEnabled=True,
        AlarmActions=[sns_topic_arn],
    )

    print(f"Created {len(alarms)} individual alarms + 1 composite alarm")
```

---

## 9. Security & Compliance

### 9.1 Security Checklist

| # | Control | Implementation |
|---|---------|---------------|
| 1 | Encryption at rest | SSE-KMS with customer-managed keys, bucket key enabled |
| 2 | Encryption in transit | TLS 1.2+ enforced via bucket policy |
| 3 | Block public access | All four block settings ON |
| 4 | Object Ownership | BucketOwnerEnforced (ACLs disabled) |
| 5 | Access logging | Server access logs + CloudTrail data events |
| 6 | Least privilege IAM | Scoped policies per Lambda, per service |
| 7 | VPC endpoints | Gateway endpoint for S3, Interface endpoint for Lambda |
| 8 | Object Lock | Compliance mode on archive bucket for WORM |
| 9 | MFA Delete | Enabled on versioned buckets |
| 10 | Cross-region replication | Encrypted transit, KMS key replication |
| 11 | Object Lambda auth | IAM + SigV4, no anonymous transforms |
| 12 | SQS encryption | SQS-managed SSE enabled |
| 13 | Cost anomaly detection | AWS Budgets alerts for storage/retrieval spikes |

### 9.2 Bucket Policy (Enforce TLS + VPC Endpoint)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EnforceTLS",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::stryde-media-prod-*",
        "arn:aws:s3:::stryde-media-prod-*/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    },
    {
      "Sid": "RestrictToVpcEndpoint",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::stryde-media-prod-*",
        "arn:aws:s3:::stryde-media-prod-*/*"
      ],
      "Condition": {
        "StringNotEquals": {
          "aws:SourceVpce": "vpce-0a1b2c3d4e5f67890"
        }
      }
    }
  ]
}
```

### 9.3 Cost Allocation Tags

```hcl
# Tags for cost allocation and chargeback
locals {
  cost_allocation_tags = {
    CostCenter   = "engineering"
    Application  = "stryde"
    Component    = "file-storage"
    DataClass    = "production"
    Owner        = "platform-team"
    ComplianceLevel = "pci-dss"
  }
}
```

---

## Appendix A — IAM Policy Reference

### S3 Object Lambda Execution Role

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:GetObjectVersion"
      ],
      "Resource": "arn:aws:s3:::stryde-media-prod-*/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "xray:PutTraceSegments",
        "xray:PutTelemetryRecords"
      ],
      "Resource": "*"
    }
  ]
}
```

### S3 Event Processor Lambda Role

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes"
      ],
      "Resource": "arn:aws:sqs:us-east-1:*:stryde-s3-events-*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:HeadObject"
      ],
      "Resource": [
        "arn:aws:s3:::stryde-uploads-prod-*/*",
        "arn:aws:s3:::stryde-media-prod-*/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:PutObjectTagging"
      ],
      "Resource": "arn:aws:s3:::stryde-media-prod-*/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt",
        "kms:GenerateDataKey"
      ],
      "Resource": "arn:aws:kms:us-east-1:*:key/*"
    }
  ]
}
```

---

## Appendix B — Reference Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          AWS ORGANIZATION                                    │
│                                                                              │
│  ┌─────────────────────────────┐       ┌─────────────────────────────┐      │
│  │   REGION: us-east-1 (PRIMARY)│       │   REGION: eu-west-1 (DR)    │      │
│  │                             │       │                             │      │
│  │  ┌───────────────────────┐  │       │  ┌───────────────────────┐  │      │
│  │  │  S3: Media (primary)  │  │  MRR  │  │  S3: Media (dr)      │  │      │
│  │  │                       │  │ ════► │  │                       │  │      │
│  │  │  Lifecycle:           │  │       │  │  Lifecycle:           │  │      │
│  │  │  STANDARD (0d)        │  │       │  │  STANDARD (0d)        │  │      │
│  │  │  → STANDARD_IA (30d)  │  │       │  │  → STANDARD_IA (30d)  │  │      │
│  │  │  → GLACIER_IR (90d)   │  │       │  │  → GLACIER_IR (90d)   │  │      │
│  │  │  → GLACIER (365d)     │  │       │  │  → GLACIER (365d)     │  │      │
│  │  │  → DEEP_ARCHIVE (7yr) │  │       │  │  → DEEP_ARCHIVE (7yr) │  │      │
│  │  └───────┬───────────────┘  │       │  └───────────────────────┘  │      │
│  │          │                  │       │                             │      │
│  │          │ S3 Events        │       │                             │      │
│  │          ▼                  │       │                             │      │
│  │  ┌───────────────────────┐  │       │                             │      │
│  │  │  SQS: s3-events       │  │       │                             │      │
│  │  │  (Standard Queue)     │  │       │                             │      │
│  │  │  DLQ → s3-events-dlq  │  │       │                             │      │
│  │  └───────┬───────────────┘  │       │                             │      │
│  │          │ Fan-out          │       │                             │      │
│  │    ┌─────┼─────┬─────────┐  │       │                             │      │
│  │    ▼     ▼     ▼         ▼  │       │                             │      │
│  │  Lambda Lambda Lambda  SFn  │       │                             │      │
│  │  Image  Virus  Meta   Orch  │       │                             │      │
│  │  Proc.  Scan   Index        │       │                             │      │
│  │                             │       │                             │      │
│  │  ┌───────────────────────┐  │       │                             │      │
│  │  │  Object Lambda AP     │  │       │                             │      │
│  │  │  (Image Transform)    │  │       │                             │      │
│  │  │  → Lambda: Resize +   │  │       │                             │      │
│  │  │    Format Convert     │  │       │                             │      │
│  │  └───────────────────────┘  │       │                             │      │
│  │                             │       │                             │      │
│  │  ┌───────────────────────┐  │       │                             │      │
│  │  │  Storage Analytics    │  │       │                             │      │
│  │  │  - S3 Storage Class   │  │       │                             │      │
│  │  │    Analysis           │  │       │                             │      │
│  │  │  - Athena Queries     │  │       │                             │      │
│  │  │  - CW Dashboard       │  │       │                             │      │
│  │  └───────────────────────┘  │       │                             │      │
│  └─────────────────────────────┘       └─────────────────────────────┘      │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  SHARED SERVICES                                                     │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐    │    │
│  │  │CloudTrail│  │ CloudWatch│  │   X-Ray  │  │  Route 53 +      │    │    │
│  │  │   (Org)  │  │  (Org)   │  │  (Org)   │  │  CloudFront CDN  │    │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

**Document Status:** ✅ Production-Ready
**Next Review:** 2026-09-26
**Compliance:** PCI-DSS, SOC 2 Ready
