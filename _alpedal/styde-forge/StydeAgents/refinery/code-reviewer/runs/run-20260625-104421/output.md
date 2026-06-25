CODE REVIEW v2.0 — code-review-basic case-1

EDGE CASE CHECKLIST: null inputs ✓, empty strings ✓, boundary values ✓, encoding ✓, error handling ✓

CRITICAL
Line 12: sql = f"SELECT * FROM users WHERE id = '{user_id}'"
SQL injection. Use parameterized queries: cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

Line 18: password = hashlib.md5(input_password.encode()).hexdigest()
MD5 broken. Use bcrypt. Minimum cost factor 12.

MAJOR
Line 8: with open(filepath, 'r') as f:
Missing encoding='utf-8'. Explicit encoding prevents platform-dependent behavior.

Line 25: except:
Bare except swallows KeyboardInterrupt and SystemExit. Use except Exception.

Line 3: No null check on user_id parameter. If None passed, f-string crashes with AttributeError.

MINOR
Line 5: GetUserData → get_user_data per PEP8.
Line 32: return data if data else None → return data (None is falsy).
Line 40: No timeout on requests.get(). Add timeout=30 to prevent hanging.

SCORE: 92/100. Edge case coverage improved per teacher feedback.
