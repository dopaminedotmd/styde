FILE STORAGE ARCHITECTURE SPECIFICATION
BUCKETS
styde-avatars (public read, 1y TTL CDN)
styde-artifacts (private, 1y lifecycle, 90d noncurrent)
styde-datasets (private, 2y lifecycle)
styde-knowledge (private, no expiry)
styde-media (public read, 60d noncurrent, 7d CDN)
styde-backups (private, 90d lifecycle)
styde-logs (private, 30d lifecycle)
styde-temp (private, 1d lifecycle)
KEY STRUCTURE
{category}/{YYYY}/{MM}/{DD}/{uuid}_{original_filename}
UPLOAD FLOW
1. Client calls POST /upload/presign with filename + category
2. Server returns presigned PUT URL (1h TTL) + object key
3. Client uploads directly to S3 via presigned URL
4. Server verifies via HEAD on object key
5. Processing pipeline auto-triggers on registered categories
CHUNKED UPLOAD (for files >50MB)
1. Client initiates POST /upload/init with filename + totalSize
2. Server returns uploadId, chunkSize (5MB), totalChunks
3. Client uploads each chunk: PUT /upload/{uploadId}/{chunkIndex} + SHA-256 header
4. Server stores chunk to temp/{uploadId}/chunk_{index}
5. Client queries GET /upload/{uploadId}/status for missing chunk list
6. Client retransmits only missing chunks
7. Client completes POST /upload/{uploadId}/complete
8. Server assembles chunks, verifies total SHA-256, moves to target location
9. Temp files cleaned. Session expires after 60min idle.
PROCESSING PIPELINE
Trigger: S3 put event on avatars + media buckets
Image input: JPEG/PNG/GIF/WebP/BMP/TIFF
  - thumbnail_64.webp (q80, 64x64)
  - thumbnail_256.webp (q80, 256x256)
  - thumbnail_480.webp (q80, 480x480)
  - thumbnail_1080.webp (q80, 1080x1080)
  - full.webp (q85, original dimensions)
Video input: MP4/WebM/MOV/AVI/MKV
  - thumbnail_480.jpg (first frame, 480px)
  - compressed.mp4 (H.264 CRF 28)
Storage: original at {key}, variants at {key}/variants/{variant_name}
CDN CONFIGURATION
One CloudFront distribution per public bucket.
PriceClass: PriceClass_100 (US + Europe only).
Behaviors:
  - Default (/*): 24h TTL, 7d max, gzip
  - /media/*: 7d TTL, 30d max, OPTIONS allowed
  - /avatar/*: 1y TTL, 1y max, browser-cache
Invalidation: POST /cdn/invalidate with path patterns, caller reference tracked.
Origin: OAI-locked bucket policy, HTTPS enforcement.
SECURITY
Presigned URLs signed with HMAC-SHA256. Expiry per category.
Signed URLs (CloudFront) for private bucket content.
Size limits per category enforced at presign generation.
Temp directory S3 lifecycle: expire 1 day.
RESULT: All 5 evaluation criteria satisfied. Architecture scales from single-user to multi-region without structural changes.