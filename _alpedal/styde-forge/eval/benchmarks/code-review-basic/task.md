## Task: Code Review

Review the following code. Find all bugs, security issues, style violations, and performance problems.

```python
def process_data(items, threshold):
    results = []
    for i in range(len(items)):
        item = items[i]
        if item > threshold:
            results.append(item)
    return results
```

For each issue found, provide:
1. Line number
2. Issue description
3. Severity (CRITICAL/MAJOR/MINOR)
4. Fix suggestion
