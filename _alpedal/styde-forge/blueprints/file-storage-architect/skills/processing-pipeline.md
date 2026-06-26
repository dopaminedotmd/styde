# Image and Video Processing Pipeline

Process uploaded media through configurable pipeline.

## Image Processing
Supported formats: JPEG, PNG, GIF, WebP, BMP, TIFF

### Variants
- Thumbnail 64px (WebP, q80): avatar tiny preview
- Thumbnail 256px (WebP, q80): avatar standard
- Thumbnail 480px (WebP, q80): video preview
- Thumbnail 1080px (WebP, q80): HD preview
- WebP (q85): full quality web format

## Video Processing
Supported formats: MP4, WebM, MOV, AVI, MKV

### Variants
- Thumbnail 480px (JPEG): first frame
- Compressed (H.264, CRF 28): reduced size

## Pipeline
1. Upload triggers auto-process
2. Detect file type by extension
3. Generate all configured variants
4. Store variants alongside original
5. Return variant keys and sizes
