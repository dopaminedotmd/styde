# S3 Bucket Structure and Lifecycle Policies

Design S3-compatible bucket layouts with lifecycle rules.

## Bucket Layout
Organize by file category. Each bucket has a single purpose.
Buckets: styde-avatars, styde-artifacts, styde-datasets, styde-knowledge, styde-media, styde-backups, styde-logs, styde-temp.

## Key Structure
Use hierarchical prefixes: {category}/{year}/{month}/{day}/{uuid}_{filename}

## Lifecycle Rules
- Temporary files: expire after 1 day
- Logs: expire after 30 days
- Backups: expire after 90 days
- Datasets: expire after 2 years
- Media: noncurrent versions kept 60 days
- Artifacts: expire after 1 year, noncurrent kept 90 days

## Access Control
- Public read: avatars, media
- Private: artifacts, datasets, knowledge, backups, logs, temp
