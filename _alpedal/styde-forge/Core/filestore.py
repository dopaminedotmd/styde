"""
Styde Forge File Storage System.
S3-compatible storage, presigned URLs, chunked uploads,
image/video processing pipelines, and CDN configuration.
"""
import hashlib
import json
import os
import re
import tempfile
import threading
import time
import uuid
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import BinaryIO, Optional
from urllib.parse import urlencode, urlparse

FORGE_ROOT = Path(__file__).resolve().parent.parent


# ─── Storage Provider ─────────────────────────────────────────────

class StorageProvider(Enum):
    S3 = "s3"
    MINIO = "minio"
    R2 = "r2"          # Cloudflare R2 (S3-compatible)
    GCS = "gcs"        # Google Cloud Storage
    LOCAL = "local"    # Filesystem fallback


class FileCategory(Enum):
    AVATAR = "avatar"           # User/agent profile images
    ARTIFACT = "artifact"       # Agent-generated content
    DATASET = "dataset"         # Training/evaluation datasets
    KNOWLEDGE = "knowledge"     # Knowledge base documents
    MEDIA = "media"             # Images/video/audio
    BACKUP = "backup"           # Checkpoints and state backups
    LOG = "log"                 # Execution logs
    TEMP = "temp"               # Temporary processing files


# ─── Bucket Structure ─────────────────────────────────────────────

BUCKET_STRUCTURE = {
    FileCategory.AVATAR: {
        "name": "styde-avatars",
        "lifecycle": {
            "noncurrent_days": 30,
            "abort_incomplete_days": 1,
        },
        "public_read": True,
        "variants": ["original", "thumb_64", "thumb_256"],
        "max_size_mb": 5,
    },
    FileCategory.ARTIFACT: {
        "name": "styde-artifacts",
        "lifecycle": {
            "expiration_days": 365,
            "noncurrent_days": 90,
            "abort_incomplete_days": 2,
        },
        "public_read": False,
        "max_size_mb": 100,
    },
    FileCategory.DATASET: {
        "name": "styde-datasets",
        "lifecycle": {
            "expiration_days": 730,
            "noncurrent_days": 180,
            "abort_incomplete_days": 7,
        },
        "public_read": False,
        "max_size_mb": 1024,
    },
    FileCategory.KNOWLEDGE: {
        "name": "styde-knowledge",
        "lifecycle": {
            "noncurrent_days": 365,
            "abort_incomplete_days": 1,
        },
        "public_read": False,
        "max_size_mb": 50,
    },
    FileCategory.MEDIA: {
        "name": "styde-media",
        "lifecycle": {
            "noncurrent_days": 60,
            "abort_incomplete_days": 3,
        },
        "public_read": True,
        "variants": ["original", "thumb_480", "thumb_1080", "webp"],
        "max_size_mb": 500,
    },
    FileCategory.BACKUP: {
        "name": "styde-backups",
        "lifecycle": {
            "expiration_days": 90,
            "noncurrent_days": 14,
        },
        "public_read": False,
        "max_size_mb": 10240,
    },
    FileCategory.LOG: {
        "name": "styde-logs",
        "lifecycle": {
            "expiration_days": 30,
            "noncurrent_days": 7,
        },
        "public_read": False,
        "max_size_mb": 10,
    },
    FileCategory.TEMP: {
        "name": "styde-temp",
        "lifecycle": {
            "expiration_days": 1,
        },
        "public_read": False,
        "max_size_mb": 500,
    },
}


# ─── Local Filesystem Backend ─────────────────────────────────────

class LocalStorageBackend:
    """Fallback storage backend using local filesystem.
    Mirrors S3 path structure: /{bucket}/{prefix}/{filename}
    """

    def __init__(self, root: Optional[Path] = None):
        self.root = root or FORGE_ROOT / "storage"
        self.root.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def _bucket_path(self, bucket: str) -> Path:
        bp = self.root / bucket
        bp.mkdir(parents=True, exist_ok=True)
        return bp

    def put(self, bucket: str, key: str, data: bytes, metadata: dict = None):
        path = self._bucket_path(bucket) / key
        path.parent.mkdir(parents=True, exist_ok=True)
        with self._lock:
            path.write_bytes(data)
        if metadata:
            meta_path = path.with_suffix(path.suffix + ".meta.json")
            meta_path.write_text(json.dumps(metadata), encoding="utf-8")

    def get(self, bucket: str, key: str) -> Optional[bytes]:
        path = self._bucket_path(bucket) / key
        if not path.exists():
            return None
        return path.read_bytes()

    def delete(self, bucket: str, key: str) -> bool:
        path = self._bucket_path(bucket) / key
        if not path.exists():
            return False
        path.unlink()
        meta_path = path.with_suffix(path.suffix + ".meta.json")
        if meta_path.exists():
            meta_path.unlink()
        return True

    def exists(self, bucket: str, key: str) -> bool:
        return (self._bucket_path(bucket) / key).exists()

    def list_prefix(self, bucket: str, prefix: str = "") -> list[dict]:
        bp = self._bucket_path(bucket) / prefix
        if not bp.exists():
            return []
        results = []
        for p in sorted(bp.rglob("*")):
            if p.is_file() and not p.suffix == ".meta.json":
                results.append({
                    "key": str(p.relative_to(self._bucket_path(bucket))),
                    "size": p.stat().st_size,
                    "modified": datetime.fromtimestamp(
                        p.stat().st_mtime, tz=timezone.utc
                    ).isoformat(),
                })
        return results

    def presigned_url(self, bucket: str, key: str, expires_in: int = 3600,
                      method: str = "GET") -> str:
        """Simulate presigned URL via local path reference."""
        path = self._bucket_path(bucket) / key
        if not path.exists() and method == "GET":
            return ""
        return f"file://{path.resolve()}?expires={int(time.time()) + expires_in}"

    def generate_key(self, category: FileCategory, filename: str,
                     prefix: str = "") -> str:
        """Generate a structured object key."""
        ts = datetime.now(timezone.utc).strftime("%Y/%m/%d")
        uid = uuid.uuid4().hex[:12]
        safe_name = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)
        parts = [category.value, ts]
        if prefix:
            parts.append(prefix)
        parts.append(f"{uid}_{safe_name}")
        return "/".join(parts)


# ─── Chunked Upload Manager ──────────────────────────────────────

class UploadSession:
    """Track a multi-part/chunked upload session."""

    def __init__(self, file_id: str, filename: str, total_size: int,
                 chunk_size: int = 5 * 1024 * 1024,  # 5MB default
                 category: FileCategory = FileCategory.ARTIFACT):
        self.file_id = file_id
        self.filename = filename
        self.total_size = total_size
        self.chunk_size = chunk_size
        self.total_chunks = (total_size + chunk_size - 1) // chunk_size
        self.category = category
        self.received_chunks: set[int] = set()
        self.chunk_hashes: dict[int, str] = {}
        self.created = datetime.now(timezone.utc)
        self.last_active = self.created
        self.completed = False
        self.upload_id = uuid.uuid4().hex[:16]

    @property
    def progress(self) -> float:
        if self.total_chunks == 0:
            return 1.0
        return len(self.received_chunks) / self.total_chunks

    @property
    def is_expired(self, max_idle_minutes: int = 60) -> bool:
        idle = (datetime.now(timezone.utc) - self.last_active).total_seconds()
        return idle > max_idle_minutes * 60


class ChunkedUploadManager:
    """Manages resumable chunked uploads with integrity verification."""

    def __init__(self, storage: LocalStorageBackend):
        self.storage = storage
        self._sessions: dict[str, UploadSession] = {}
        self._lock = threading.Lock()
        self._temp_dir = FORGE_ROOT / "storage" / ".chunks"
        self._temp_dir.mkdir(parents=True, exist_ok=True)
        # Start cleanup thread
        self._cleanup_thread = threading.Thread(
            target=self._cleanup_loop, daemon=True
        )
        self._cleanup_thread.start()

    def create_session(self, filename: str, total_size: int,
                       chunk_size: int = 5 * 1024 * 1024,
                       category: FileCategory = FileCategory.ARTIFACT
                       ) -> dict:
        """Initialize a new chunked upload session."""
        file_id = uuid.uuid4().hex[:24]
        session = UploadSession(
            file_id=file_id,
            filename=filename,
            total_size=total_size,
            chunk_size=chunk_size,
            category=category,
        )
        with self._lock:
            self._sessions[file_id] = session
        return {
            "upload_id": session.upload_id,
            "file_id": file_id,
            "chunk_size": chunk_size,
            "total_chunks": session.total_chunks,
            "filename": filename,
            "expires_in_minutes": 60,
        }

    def upload_chunk(self, file_id: str, chunk_index: int,
                     data: bytes) -> dict:
        """Upload a single chunk. Returns status."""
        session = self._get_session(file_id)
        if not session:
            return {"success": False, "error": "Session not found"}
        if session.completed:
            return {"success": False, "error": "Upload already completed"}
        if chunk_index >= session.total_chunks:
            return {"success": False, "error": f"Chunk {chunk_index} out of range"}

        chunk_hash = hashlib.sha256(data).hexdigest()
        chunk_path = self._temp_dir / file_id / f"chunk_{chunk_index:06d}"
        chunk_path.parent.mkdir(parents=True, exist_ok=True)
        chunk_path.write_bytes(data)

        with self._lock:
            session.received_chunks.add(chunk_index)
            session.chunk_hashes[chunk_index] = chunk_hash
            session.last_active = datetime.now(timezone.utc)

        return {
            "success": True,
            "chunk_index": chunk_index,
            "hash": chunk_hash,
            "received": len(session.received_chunks),
            "total": session.total_chunks,
            "progress": session.progress,
        }

    def complete_upload(self, file_id: str) -> dict:
        """Assemble all chunks into final file."""
        session = self._get_session(file_id)
        if not session:
            return {"success": False, "error": "Session not found"}
        if session.completed:
            return {"success": False, "error": "Already completed"}
        if len(session.received_chunks) != session.total_chunks:
            missing = sorted(
                set(range(session.total_chunks)) - session.received_chunks
            )
            return {
                "success": False,
                "error": f"Missing chunks: {missing[:10]}...",
                "missing_count": len(missing),
            }

        chunk_dir = self._temp_dir / file_id
        assembled = bytearray()
        final_hash = hashlib.sha256()

        for i in range(session.total_chunks):
            chunk_path = chunk_dir / f"chunk_{i:06d}"
            chunk_data = chunk_path.read_bytes()
            assembled.extend(chunk_data)
            final_hash.update(chunk_data)

        # Verify total size
        if len(assembled) != session.total_size:
            return {
                "success": False,
                "error": (
                    f"Size mismatch: expected {session.total_size}, "
                    f"got {len(assembled)}"
                ),
            }

        # Store final file
        key = self.storage.generate_key(session.category, session.filename)
        self.storage.put(
            BUCKET_STRUCTURE[session.category]["name"],
            key,
            bytes(assembled),
            metadata={
                "original_filename": session.filename,
                "total_size": session.total_size,
                "sha256": final_hash.hexdigest(),
                "upload_id": session.upload_id,
                "chunks": session.total_chunks,
            },
        )

        # Cleanup temp chunks
        import shutil
        shutil.rmtree(chunk_dir, ignore_errors=True)

        with self._lock:
            session.completed = True

        return {
            "success": True,
            "key": key,
            "bucket": BUCKET_STRUCTURE[session.category]["name"],
            "size": session.total_size,
            "sha256": final_hash.hexdigest(),
        }

    def get_status(self, file_id: str) -> Optional[dict]:
        """Get upload progress."""
        session = self._get_session(file_id)
        if not session:
            return None
        return {
            "file_id": file_id,
            "filename": session.filename,
            "total_chunks": session.total_chunks,
            "received_chunks": sorted(session.received_chunks),
            "progress": session.progress,
            "completed": session.completed,
            "created": session.created.isoformat(),
            "last_active": session.last_active.isoformat(),
        }

    def cancel_upload(self, file_id: str) -> bool:
        """Cancel and clean up an upload session."""
        with self._lock:
            session = self._sessions.pop(file_id, None)
        if not session:
            return False
        chunk_dir = self._temp_dir / file_id
        if chunk_dir.exists():
            import shutil
            shutil.rmtree(chunk_dir, ignore_errors=True)
        return True

    def _get_session(self, file_id: str) -> Optional[UploadSession]:
        with self._lock:
            return self._sessions.get(file_id)

    def _cleanup_loop(self):
        """Periodically clean expired sessions."""
        while True:
            time.sleep(300)  # every 5 minutes
            expired = []
            with self._lock:
                for fid, session in list(self._sessions.items()):
                    if session.is_expired:
                        expired.append(fid)
                for fid in expired:
                    del self._sessions[fid]
            for fid in expired:
                chunk_dir = self._temp_dir / fid
                if chunk_dir.exists():
                    import shutil
                    shutil.rmtree(chunk_dir, ignore_errors=True)


# ─── Image Processing Pipeline ───────────────────────────────────

class ImageProcessingPipeline:
    """Image/video processing pipeline with format conversion,
    resizing, thumbnailing, and optimization.
    Uses Pillow for images; ffmpeg for video.
    """

    SUPPORTED_IMAGE_FORMATS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff"}
    SUPPORTED_VIDEO_FORMATS = {".mp4", ".webm", ".mov", ".avi", ".mkv"}

    def __init__(self, storage: LocalStorageBackend):
        self.storage = storage
        self._has_pillow = self._check_pillow()
        self._has_ffmpeg = self._check_ffmpeg()

    def _check_pillow(self) -> bool:
        try:
            from PIL import Image
            return True
        except ImportError:
            return False

    def _check_ffmpeg(self) -> bool:
        import shutil
        return shutil.which("ffmpeg") is not None

    def process_image(self, bucket: str, key: str) -> list[dict]:
        """Process an image: generate all configured variants.
        Returns list of {variant, key, size, format} for each variant.
        """
        if not self._has_pillow:
            return [{"error": "Pillow not installed. Run: pip install Pillow"}]

        from PIL import Image as PILImage
        import io

        data = self.storage.get(bucket, key)
        if not data:
            return [{"error": f"File not found: {bucket}/{key}"}]

        ext = Path(key).suffix.lower()
        if ext not in self.SUPPORTED_IMAGE_FORMATS:
            return [{"error": f"Unsupported image format: {ext}"}]

        # Determine category from bucket name
        category = self._bucket_to_category(bucket)
        variants = BUCKET_STRUCTURE.get(category, {}).get("variants", [])

        results = []
        original_size = len(data)
        base_name = Path(key).stem
        base_dir = Path(key).parent

        for variant in variants:
            if variant == "original":
                continue

            try:
                img = PILImage.open(io.BytesIO(data))
                img = img.convert("RGB") if img.mode in ("RGBA", "P") else img

                if variant == "webp":
                    out_format = "WEBP"
                    out_ext = ".webp"
                    output = io.BytesIO()
                    img.save(output, format="WEBP", quality=85)
                    variant_key = str(base_dir / f"{base_name}{out_ext}")
                elif variant.startswith("thumb_"):
                    size = int(variant.split("_")[1])
                    img.thumbnail((size, size), PILImage.LANCZOS)
                    out_format = "WEBP"
                    out_ext = ".webp"
                    output = io.BytesIO()
                    img.save(output, format="WEBP", quality=80)
                    variant_key = str(base_dir / f"{base_name}_{variant}{out_ext}")
                else:
                    continue

                variant_data = output.getvalue()
                self.storage.put(bucket, variant_key, variant_data)

                results.append({
                    "variant": variant,
                    "key": variant_key,
                    "size": len(variant_data),
                    "original_size_pct": round(
                        (len(variant_data) / original_size) * 100, 1
                    ),
                    "format": out_format,
                })
            except Exception as e:
                results.append({"variant": variant, "error": str(e)})

        return results

    def process_video(self, bucket: str, key: str) -> list[dict]:
        """Generate video thumbnail and compressed variant."""
        if not self._has_ffmpeg:
            return [{"error": "ffmpeg not found. Install ffmpeg."}]

        import subprocess

        data = self.storage.get(bucket, key)
        if not data:
            return [{"error": f"File not found: {bucket}/{key}"}]

        ext = Path(key).suffix.lower()
        if ext not in self.SUPPORTED_VIDEO_FORMATS:
            return [{"error": f"Unsupported video format: {ext}"}]

        base_name = Path(key).stem
        base_dir = Path(key).parent

        # Write temp file for ffmpeg processing
        with tempfile.NamedTemporaryFile(
            suffix=ext, delete=False
        ) as tmp_in:
            tmp_in.write(data)
            tmp_in_path = tmp_in.name

        results = []

        try:
            # Generate thumbnail (first frame)
            thumb_path = tempfile.mktemp(suffix=".jpg")
            subprocess.run(
                ["ffmpeg", "-y", "-i", tmp_in_path,
                 "-vframes", "1", "-vf", "scale=480:-1",
                 thumb_path],
                capture_output=True, timeout=30,
            )
            thumb_data = Path(thumb_path).read_bytes()
            thumb_key = str(base_dir / f"{base_name}_thumb_480.jpg")
            self.storage.put(bucket, thumb_key, thumb_data)
            results.append({
                "variant": "thumb_480",
                "key": thumb_key,
                "size": len(thumb_data),
                "format": "JPEG",
            })
            os.unlink(thumb_path)

            # Compress video (h264, moderate bitrate)
            comp_path = tempfile.mktemp(suffix=".mp4")
            subprocess.run(
                ["ffmpeg", "-y", "-i", tmp_in_path,
                 "-c:v", "libx264", "-preset", "fast",
                 "-crf", "28", "-movflags", "+faststart",
                 comp_path],
                capture_output=True, timeout=120,
            )
            comp_data = Path(comp_path).read_bytes()
            comp_key = str(base_dir / f"{base_name}_compressed.mp4")
            self.storage.put(bucket, comp_key, comp_data)
            results.append({
                "variant": "compressed",
                "key": comp_key,
                "size": len(comp_data),
                "format": "H.264",
                "compression_ratio": round(
                    len(data) / len(comp_data), 2
                ),
            })
            os.unlink(comp_path)

        except Exception as e:
            results.append({"variant": "processing", "error": str(e)})
        finally:
            os.unlink(tmp_in_path)

        return results

    def _bucket_to_category(self, bucket_name: str) -> Optional[FileCategory]:
        for cat, cfg in BUCKET_STRUCTURE.items():
            if cfg["name"] == bucket_name:
                return cat
        return None


# ─── Presigned URL Service ───────────────────────────────────────

class PresignedURLService:
    """Generate presigned URLs for upload and download.
    Supports temporary access with configurable expiration.
    """

    def __init__(self, storage: LocalStorageBackend):
        self.storage = storage

    def generate_upload_url(self, filename: str,
                            category: FileCategory = FileCategory.ARTIFACT,
                            expires_in: int = 3600,
                            max_size_mb: Optional[int] = None,
                            content_types: list[str] = None) -> dict:
        """Generate a presigned URL for uploading a file."""
        key = self.storage.generate_key(category, filename)
        bucket = BUCKET_STRUCTURE[category]["name"]
        url = self.storage.presigned_url(
            bucket, key, expires_in=expires_in, method="PUT"
        )

        max_size = max_size_mb or BUCKET_STRUCTURE[category].get("max_size_mb", 100)

        return {
            "url": url,
            "key": key,
            "bucket": bucket,
            "method": "PUT",
            "expires_in": expires_in,
            "expires_at": (
                datetime.now(timezone.utc) + timedelta(seconds=expires_in)
            ).isoformat(),
            "max_size_mb": max_size,
            "allowed_content_types": content_types or [],
            "fields": {
                "key": key,
                "bucket": bucket,
                "X-Amz-Expires": str(expires_in),
            },
        }

    def generate_download_url(self, bucket: str, key: str,
                              expires_in: int = 3600,
                              filename: Optional[str] = None,
                              disposition: str = "inline") -> dict:
        """Generate a presigned URL for downloading a file."""
        url = self.storage.presigned_url(
            bucket, key, expires_in=expires_in, method="GET"
        )
        return {
            "url": url,
            "key": key,
            "bucket": bucket,
            "method": "GET",
            "expires_in": expires_in,
            "expires_at": (
                datetime.now(timezone.utc) + timedelta(seconds=expires_in)
            ).isoformat(),
            "response_content_disposition": (
                f"{disposition}; filename=\"{filename or Path(key).name}\""
            ),
        }

    def generate_multipart_urls(self, filename: str, total_size: int,
                                chunk_size: int = 5 * 1024 * 1024,
                                category: FileCategory = FileCategory.ARTIFACT,
                                expires_in: int = 3600) -> dict:
        """Generate presigned URLs for all chunks of a multipart upload."""
        key = self.storage.generate_key(category, filename)
        bucket = BUCKET_STRUCTURE[category]["name"]
        total_chunks = (total_size + chunk_size - 1) // chunk_size

        chunk_urls = []
        for i in range(total_chunks):
            chunk_key = f"{key}.part.{i:06d}"
            url = self.storage.presigned_url(
                bucket, chunk_key, expires_in=expires_in, method="PUT"
            )
            chunk_urls.append({
                "part_number": i + 1,
                "url": url,
                "start_byte": i * chunk_size,
                "end_byte": min((i + 1) * chunk_size, total_size) - 1,
            })

        return {
            "upload_id": uuid.uuid4().hex[:16],
            "key": key,
            "bucket": bucket,
            "total_parts": total_chunks,
            "chunk_size": chunk_size,
            "total_size": total_size,
            "expires_in": expires_in,
            "expires_at": (
                datetime.now(timezone.utc) + timedelta(seconds=expires_in)
            ).isoformat(),
            "chunk_urls": chunk_urls,
        }


# ─── CDN Service ─────────────────────────────────────────────────

class CDNService:
    """CloudFront CDN configuration for file delivery.
    Manages distributions, cache behaviors, and invalidations.
    """

    def __init__(self, storage: LocalStorageBackend):
        self.storage = storage
        self._config_path = FORGE_ROOT / "storage" / "cdn_config.json"
        self._config = self._load_config()

    def _load_config(self) -> dict:
        if self._config_path.exists():
            return json.loads(self._config_path.read_text(encoding="utf-8"))
        return {
            "distributions": {},
            "default_ttl": 86400,       # 24 hours
            "max_ttl": 604800,          # 7 days
            "default_root": "index.html",
            "price_class": "PriceClass_100",  # US/Europe only
        }

    def _save_config(self):
        self._config_path.parent.mkdir(parents=True, exist_ok=True)
        self._config_path.write_text(
            json.dumps(self._config, indent=2), encoding="utf-8"
        )

    def create_distribution(self, name: str, bucket_name: str,
                            comment: str = "") -> dict:
        """Register a CDN distribution configuration."""
        dist_id = f"E{uuid.uuid4().hex[:14].upper()}"

        distribution = {
            "id": dist_id,
            "name": name,
            "origin": bucket_name,
            "domain": f"{dist_id}.cloudfront.net",
            "status": "InProgress",
            "comment": comment,
            "created": datetime.now(timezone.utc).isoformat(),
            "cache_behaviors": {
                "default": {
                    "path_pattern": "*",
                    "ttl": self._config["default_ttl"],
                    "max_ttl": self._config["max_ttl"],
                    "compress": True,
                    "allowed_methods": ["GET", "HEAD"],
                    "forward_query_string": False,
                    "smooth_streaming": False,
                },
                "media": {
                    "path_pattern": "media/*",
                    "ttl": 604800,   # 7 days for media
                    "max_ttl": 2592000,  # 30 days
                    "compress": True,
                    "allowed_methods": ["GET", "HEAD", "OPTIONS"],
                    "forward_query_string": True,
                },
                "avatars": {
                    "path_pattern": "avatar/*",
                    "ttl": 31536000,  # 1 year for avatars
                    "max_ttl": 31536000,
                    "compress": True,
                    "allowed_methods": ["GET", "HEAD"],
                    "forward_query_string": False,
                },
            },
            "price_class": self._config["price_class"],
            "enabled": True,
        }

        self._config["distributions"][name] = distribution
        self._save_config()
        return distribution

    def invalidate(self, distribution_name: str, paths: list[str]) -> dict:
        """Create a cache invalidation request."""
        dist = self._config["distributions"].get(distribution_name)
        if not dist:
            return {"error": f"Distribution '{distribution_name}' not found"}

        invalidation_id = uuid.uuid4().hex[:24]
        invalidation = {
            "id": invalidation_id,
            "distribution": distribution_name,
            "paths": paths,
            "status": "InProgress",
            "created": datetime.now(timezone.utc).isoformat(),
            "caller_reference": f"forge-{invalidation_id}",
        }

        inval_path = FORGE_ROOT / "storage" / "cdn_invalidations.json"
        invalidations = []
        if inval_path.exists():
            invalidations = json.loads(
                inval_path.read_text(encoding="utf-8")
            )
        invalidations.append(invalidation)
        inval_path.write_text(
            json.dumps(invalidations, indent=2), encoding="utf-8"
        )

        return invalidation

    def update_cache_behavior(self, distribution_name: str,
                              path_pattern: str, ttl: int,
                              compress: bool = True) -> dict:
        """Update a cache behavior for a distribution."""
        dist = self._config["distributions"].get(distribution_name)
        if not dist:
            return {"error": f"Distribution '{distribution_name}' not found"}

        if path_pattern == "*":
            behavior_key = "default"
        else:
            # Find matching named behavior or create new
            for key, behavior in dist["cache_behaviors"].items():
                if behavior["path_pattern"] == path_pattern:
                    behavior_key = key
                    break
            else:
                behavior_key = f"custom_{uuid.uuid4().hex[:8]}"

        dist["cache_behaviors"][behavior_key] = {
            "path_pattern": path_pattern,
            "ttl": ttl,
            "max_ttl": max(ttl, self._config["max_ttl"]),
            "compress": compress,
            "allowed_methods": ["GET", "HEAD"],
            "forward_query_string": False,
        }

        self._save_config()
        return dist["cache_behaviors"][behavior_key]

    def list_distributions(self) -> list[dict]:
        return list(self._config["distributions"].values())

    def get_distribution(self, name: str) -> Optional[dict]:
        return self._config["distributions"].get(name)


# ─── File Storage Engine ─────────────────────────────────────────

class FileStorageEngine:
    """Top-level file storage orchestrator.
    Coordinates storage, uploads, processing, and CDN.
    """

    def __init__(self):
        self.storage = LocalStorageBackend()
        self.uploads = ChunkedUploadManager(self.storage)
        self.processor = ImageProcessingPipeline(self.storage)
        self.presigned = PresignedURLService(self.storage)
        self.cdn = CDNService(self.storage)

    # ── Basic operations ──────────────────────────────────────

    def upload_file(self, data: bytes, filename: str,
                    category: FileCategory = FileCategory.ARTIFACT,
                    prefix: str = "") -> dict:
        """Upload a file directly."""
        key = self.storage.generate_key(category, filename, prefix)
        bucket = BUCKET_STRUCTURE[category]["name"]
        self.storage.put(bucket, key, data)
        return {
            "key": key,
            "bucket": bucket,
            "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "category": category.value,
        }

    def download_file(self, bucket: str, key: str) -> Optional[bytes]:
        return self.storage.get(bucket, key)

    def delete_file(self, bucket: str, key: str) -> bool:
        return self.storage.delete(bucket, key)

    def list_files(self, category: FileCategory,
                   prefix: str = "") -> list[dict]:
        bucket = BUCKET_STRUCTURE[category]["name"]
        return self.storage.list_prefix(bucket, prefix)

    def get_file_info(self, bucket: str, key: str) -> Optional[dict]:
        data = self.storage.get(bucket, key)
        if not data:
            return None
        return {
            "key": key,
            "bucket": bucket,
            "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "extension": Path(key).suffix.lower(),
            "filename": Path(key).name,
        }

    # ── Upload via presigned URL ───────────────────────────────

    def request_upload(self, filename: str,
                       category: FileCategory = FileCategory.ARTIFACT,
                       expires_in: int = 3600) -> dict:
        return self.presigned.generate_upload_url(
            filename, category, expires_in
        )

    def request_download(self, bucket: str, key: str,
                         expires_in: int = 3600,
                         filename: Optional[str] = None) -> dict:
        return self.presigned.generate_download_url(
            bucket, key, expires_in, filename
        )

    # ── Chunked upload ─────────────────────────────────────────

    def start_chunked_upload(self, filename: str, total_size: int,
                             chunk_size: int = 5 * 1024 * 1024,
                             category: FileCategory = FileCategory.ARTIFACT
                             ) -> dict:
        return self.uploads.create_session(
            filename, total_size, chunk_size, category
        )

    def upload_chunk(self, file_id: str, chunk_index: int,
                     data: bytes) -> dict:
        return self.uploads.upload_chunk(file_id, chunk_index, data)

    def complete_chunked_upload(self, file_id: str) -> dict:
        return self.uploads.complete_upload(file_id)

    def cancel_chunked_upload(self, file_id: str) -> bool:
        return self.uploads.cancel_upload(file_id)

    def upload_status(self, file_id: str) -> Optional[dict]:
        return self.uploads.get_status(file_id)

    # ── Processing ─────────────────────────────────────────────

    def process_image(self, bucket: str, key: str) -> list[dict]:
        return self.processor.process_image(bucket, key)

    def process_video(self, bucket: str, key: str) -> list[dict]:
        return self.processor.process_video(bucket, key)

    def auto_process(self, bucket: str, key: str) -> list[dict]:
        """Auto-detect file type and process accordingly."""
        ext = Path(key).suffix.lower()
        if ext in ImageProcessingPipeline.SUPPORTED_IMAGE_FORMATS:
            return self.process_image(bucket, key)
        elif ext in ImageProcessingPipeline.SUPPORTED_VIDEO_FORMATS:
            return self.process_video(bucket, key)
        else:
            return [{"info": "No processing available for this file type"}]

    # ── CDN management ─────────────────────────────────────────

    def create_cdn_distribution(self, name: str, bucket_name: str,
                                comment: str = "") -> dict:
        return self.cdn.create_distribution(name, bucket_name, comment)

    def invalidate_cache(self, distribution_name: str,
                         paths: list[str]) -> dict:
        return self.cdn.invalidate(distribution_name, paths)

    def update_cache_ttl(self, distribution_name: str,
                         path_pattern: str, ttl: int) -> dict:
        return self.cdn.update_cache_behavior(
            distribution_name, path_pattern, ttl
        )

    def list_distributions(self) -> list[dict]:
        return self.cdn.list_distributions()

    # ── Storage analytics ──────────────────────────────────────

    def get_storage_usage(self) -> dict:
        """Calculate storage usage across all buckets."""
        usage = {}
        total_bytes = 0
        for category, cfg in BUCKET_STRUCTURE.items():
            bucket = cfg["name"]
            files = self.storage.list_prefix(bucket)
            bucket_bytes = sum(f["size"] for f in files)
            total_bytes += bucket_bytes
            usage[category.value] = {
                "bucket": bucket,
                "files": len(files),
                "size_bytes": bucket_bytes,
                "size_mb": round(bucket_bytes / (1024 * 1024), 2),
                "max_size_mb": cfg.get("max_size_mb", 0),
            }

        return {
            "buckets": usage,
            "total_files": sum(b["files"] for b in usage.values()),
            "total_size_bytes": total_bytes,
            "total_size_mb": round(total_bytes / (1024 * 1024), 2),
            "total_size_gb": round(total_bytes / (1024 * 1024 * 1024), 4),
        }

    def get_lifecycle_policies(self) -> dict:
        """Return configured lifecycle policies."""
        policies = {}
        for category, cfg in BUCKET_STRUCTURE.items():
            policies[cfg["name"]] = {
                "category": category.value,
                "rules": cfg["lifecycle"],
            }
        return policies


# ─── Singleton Engine ─────────────────────────────────────────────

_engine: Optional[FileStorageEngine] = None


def get_engine() -> FileStorageEngine:
    global _engine
    if _engine is None:
        _engine = FileStorageEngine()
    return _engine
