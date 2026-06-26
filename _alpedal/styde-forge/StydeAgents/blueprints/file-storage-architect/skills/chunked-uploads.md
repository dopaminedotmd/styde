# Chunked and Resumable Uploads

Support large file uploads with chunking and resume capability.

## Chunk Protocol
1. Client initiates session: send filename + total size
2. Server returns upload_id, chunk_size, total_chunks
3. Client uploads chunks individually with index
4. Each chunk verified by SHA-256 hash
5. Client signals completion; server assembles final file

## Chunk Size
- Default: 5MB (configurable)
- Optimal for network interruptions
- Each chunk independently verifiable

## Resume Support
- Track received chunks per session
- Client queries status to find missing chunks
- Only missing chunks retransmitted
- Sessions expire after 60 minutes idle

## Integrity
- SHA-256 per chunk and final file
- Total size verification on assembly
- Temp files cleaned on completion or expiry
