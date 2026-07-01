# debug_cookie.py
import re

# Exact regex from dashboard_auth.py
COOKIE_PAIR_RE = re.compile(
    r'\s*([^=;\s]+)\s*=\s*("(?:[^"\\]|\\.)*"|[^;]*)\s*(?:;|$)'
)

tests = [
    ('', {}),
    ('session_id=abc123', {'session_id': 'abc123'}),
    ('a=1; b=2', {'a': '1', 'b': '2'}),
    ('a=1; b="quoted;val"; c=3', {'a': '1', 'b': 'quoted;val', 'c': '3'}),
    (' session_id = abc123 ; csrf = def456 ', {'session_id': 'abc123', 'csrf': 'def456'}),
    ('a=; b=2', {'a': '', 'b': '2'}),
]

for inp, expected in tests:
    result = {}
    for m in COOKIE_PAIR_RE.finditer(inp):
        name = m.group(1)
        value = m.group(2)
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        result[name] = value
    status = 'PASS' if result == expected else 'FAIL'
    print(f'[{status}] {inp!r} => {result} (expected {expected})')
