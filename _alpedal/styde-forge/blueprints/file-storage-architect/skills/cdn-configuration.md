# CDN Configuration

Configure CloudFront for fast content delivery.

## Distribution Design
- One distribution per bucket category
- Regional edge caches (PriceClass_100: US/Europe)
- Cache behaviors per path pattern

## Cache Behaviors
- Default (/*): 24h TTL, 7d max TTL, gzip compress
- Media (/media/*): 7d TTL, 30d max TTL, allow OPTIONS
- Avatars (/avatar/*): 1y TTL, 1y max TTL, browser cache

## Cache Invalidation
- On file update: invalidate specific paths
- Supports wildcard patterns (/media/*)
- Tracks invalidation requests with caller reference

## Security
- Signed URLs for private content
- Origin access identity for bucket access
- HTTPS enforcement
