"""
Markdown stripper — converts markdown to plain text for Caveman Ultra mode.

Removes all formatting: headings, bold, italic, code fences, lists, links,
blockquotes, horizontal rules, tables. Keeps the text content.
"""
import re


def strip_markdown(text: str) -> str:
    """Convert markdown to plain text. Aggressive — removes ALL formatting."""
    if not text:
        return text

    # Remove code blocks (```...```) — preserve content, strip fences
    text = re.sub(r'```[\w]*\n([\s\S]*?)```', r'\1', text)

    # Remove inline code
    text = re.sub(r'`([^`]+)`', r'\1', text)

    # Remove images ![alt](url)
    text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', text)

    # Remove links [text](url) — keep text
    text = re.sub(r'\[([^\]]*)\]\([^)]+\)', r'\1', text)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Remove heading markers (#, ##, etc) but keep text
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)

    # Remove bold/italic markers
    text = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', text)
    text = re.sub(r'_{1,3}([^_]+)_{1,3}', r'\1', text)

    # Remove horizontal rules
    text = re.sub(r'^[-*_]{3,}\s*$', '', text, flags=re.MULTILINE)

    # Remove blockquote markers
    text = re.sub(r'^>\s?', '', text, flags=re.MULTILINE)

    # Remove list markers (-, *, +, 1.)
    text = re.sub(r'^[\s]*[-*+]\s+', '  ', text, flags=re.MULTILINE)
    text = re.sub(r'^[\s]*\d+\.\s+', '  ', text, flags=re.MULTILINE)

    # Remove table formatting (pipe characters in table rows)
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Skip separator lines (|---|---|)
        if re.match(r'^[\s|:|-]+$', stripped) and '|' in stripped:
            continue
        # Clean table rows: remove leading/trailing pipes, replace internal pipes with spaces
        if stripped.startswith('|') and stripped.endswith('|'):
            cells = [c.strip() for c in stripped.strip('|').split('|')]
            cleaned.append('  '.join(cells))
        else:
            cleaned.append(line)
    text = '\n'.join(cleaned)

    # Collapse multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Remove trailing whitespace on lines
    text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)

    return text.strip()


def is_markdown(text: str, threshold: float = 0.3) -> bool:
    """Heuristic: does this text look like markdown?

    Returns True if more than `threshold` fraction of non-empty lines
    contain markdown markers.
    """
    if not text:
        return False

    markers = [
        r'^#{1,6}\s',       # headings
        r'\*\*[^*]+\*\*',    # bold
        r'`[^`]+`',          # inline code
        r'```',              # code fence
        r'^[-*+]\s',         # unordered list
        r'^\d+\.\s',         # ordered list
        r'^>\s',             # blockquote
        r'\[.+\]\(.+\)',     # link
        r'^---\s*$',         # horizontal rule
        r'^\|.*\|$',         # table row
    ]

    lines = [l for l in text.split('\n') if l.strip()]
    if not lines:
        return False

    marked = 0
    for line in lines:
        if any(re.search(m, line) for m in markers):
            marked += 1

    return (marked / len(lines)) > threshold


def enforce_plain_text(text: str) -> str:
    """If text looks like markdown, strip it. Otherwise return as-is."""
    if is_markdown(text):
        return strip_markdown(text)
    return text
