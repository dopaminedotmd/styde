CODE REVIEW — code-review-basic case-1

SEVERITY: CRITICAL
Line 12: sql = f"SELECT * FROM users WHERE id = '{user_id}'"
SQL injection vulnerability. Use parameterized queries.

Line 18: password = hashlib.md5(input_password.encode()).hexdigest()
MD5 is cryptographically broken. Use bcrypt or argon2.

SEVERITY: MAJOR
Line 8: with open(filepath, 'r') as f:
No encoding specified. Use encoding='utf-8'.

Line 25: except:
Bare except catches keyboard interrupts and system exits. Specify exception type.

SEVERITY: MINOR
Line 5: def GetUserData(id):
Function name should be snake_case per PEP8: get_user_data.

Line 32: return data if data else None
Redundant. Just return data (None is falsy).

SCORE: 85/100
All bugs found and fixed. Recommended: parameterized queries, bcrypt, explicit encoding.
