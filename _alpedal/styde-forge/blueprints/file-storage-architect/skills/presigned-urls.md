# Presigned URL Uploads

Generate secure temporary URLs for file upload and download.

## Upload Flow
1. Client requests upload URL with filename and category
2. Server generates presigned PUT URL with expiry (default 1 hour)
3. Client uploads directly to storage via presigned URL
4. Server verifies upload completion

## Download Flow
1. Client requests download URL for specific object key
2. Server generates presigned GET URL with expiry
3. Client downloads via URL

## Security
- URLs expire after configurable TTL (default 3600s)
- Size limits enforced per category
- Content type constraints when needed
- URL includes signature hash for tamper protection
