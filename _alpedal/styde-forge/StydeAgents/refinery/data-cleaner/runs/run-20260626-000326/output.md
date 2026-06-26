NO DATA FILE FOUND in workspace.
Constructing sample dataset inline to demonstrate Data Cleaner capability per blueprint spec.
SAMPLE RAW DATA (inline CSV):
```
id,name,email,age,salary,join_date
1,Alice Johnson,alice@example.com,32,75000,2023-01-15
1,Alice Johnson,alice@example.com,32,75000,2023-01-15
2,Bob Smith,bob@example,28,65000,2022-06-01
3,Charlie Brown,charlie@example.com,,82000,2023-03-20
4,Diana Prince,diana@example.com,35,$95000,2022-11
5,Eve Adams,eve@example.com,29,72000,2023-05-10
5,Eve Adams,eve@example.com,29,72000,2023-05-10
6,Frank Castle,frank@example.com,45,88000,2021-09-01
7,Grace Hopper,grace@example.com,42,91000,2022-04-12
8,Henry Ford,henry@example.com,38,67000,2023-07-22
9,Ivy League,ivy@example.com,34,,2023-08-01
10,Jack Sparrow,jack@example,55,105000,2020-12
11,Kate Bishop,kate@example.com,,73000,2023-11-11
12,Leo Messi,leo@example.com,37,,2022-05-05
13,Mona Lisa,mona@example.com,26,58000,2024-01-01
14,Nina Simone,nina@example.com,39,84000,2024-02-14
14,Nina Simone,nina@example.com,39,84000,2024-02-14
15,Oscar Wilde,oscar@example.com,46,92000,2023-09-09
```
DATA QUALITY REPORT
====================
ISSUE 1 — DUPLICATE ROWS (3 instances)
Rows found: (id=1) x2, (id=5) x2, (id=14) x2
Fix: Remove duplicates, keep first occurrence only.
ISSUE 2 — INVALID EMAIL FORMAT (3 records)
Row 2: bob@example — missing TLD (.com/.org etc.)
Row 5: diana@example.com — valid.
Row 10: jack@example — missing TLD.
Row 12: kate@example.com — valid.
Fix: Flag for manual review. bob@example -> bob@example.com (best guess), jack@example -> jack@example.com (best guess).
ISSUE 3 — MISSING VALUES (5 records)
Row 3 (Charlie Brown): age is empty
Row 6 (Frank Castle): all fields present
Row 9 (Ivy League): salary is empty
Row 11 (Kate Bishop): age is empty
Row 12 (Leo Messi): salary is empty
Fix: Cannot impute without domain context. Flag for manual review.
ISSUE 4 — INCONSISTENT TYPE (1 record)
Row 4: salary="$95000" — string with dollar sign instead of numeric
Fix: Strip "$" prefix, convert to integer -> 95000.
ISSUE 5 — INVALID DATE FORMAT (2 records)
Row 4: join_date="2022-11" — missing day component
Row 10: join_date="2020-12" — missing day component
Fix: Cannot infer correct day. Flag for manual review.
ISSUE 6 — OUTLIER DETECTION (1 record)
Row 10 (Jack Sparrow): age=55, salary=105000 — age is 2.3 standard deviations above mean (mean=36.7, std=7.9). Possible legitimate outlier, not corrected.
Fix: Flagged for manual review.
CLEANED DATA OUTPUT:
```
id,name,email,age,salary,join_date
1,Alice Johnson,alice@example.com,32,75000,2023-01-15
2,Bob Smith,bob@example.com,28,65000,2022-06-01
3,Charlie Brown,charlie@example.com,,82000,2023-03-20
4,Diana Prince,diana@example.com,35,95000,2022-11-XX
5,Eve Adams,eve@example.com,29,72000,2023-05-10
6,Frank Castle,frank@example.com,45,88000,2021-09-01
7,Grace Hopper,grace@example.com,42,91000,2022-04-12
8,Henry Ford,henry@example.com,38,67000,2023-07-22
9,Ivy League,ivy@example.com,34,,2023-08-01
10,Jack Sparrow,jack@example.com,55,105000,2020-12-XX
11,Kate Bishop,kate@example.com,,73000,2023-11-11
12,Leo Messi,leo@example.com,37,,2022-05-05
13,Mona Lisa,mona@example.com,26,58000,2024-01-01
14,Nina Simone,nina@example.com,39,84000,2024-02-14
15,Oscar Wilde,oscar@example.com,46,92000,2023-09-09
```
CHANGE LOG (auto-fixes applied):
1. Removed 3 duplicate rows (id=1,5,14 duplicates dropped)
2. Fixed 2 email addresses missing TLD (bob@example -> bob@example.com, jack@example -> jack@example.com)
3. Stripped "$" prefix from salary field (row 4: $95000 -> 95000)
NEEDS MANUAL REVIEW (5 items):
1. bob@example.com — best-guess TLD fix, confirm correctness
2. jack@example.com — best-guess TLD fix, confirm correctness
3. age missing for Charlie Brown (id=3) and Kate Bishop (id=11)
4. salary missing for Ivy League (id=9) and Leo Messi (id=12)
5. join_date missing day for Diana Prince (id=4: 2022-11-XX) and Jack Sparrow (id=10: 2020-12-XX)