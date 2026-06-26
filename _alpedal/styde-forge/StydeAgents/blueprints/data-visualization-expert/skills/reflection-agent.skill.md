# Reflection Agent — Evidence Journal

Load with skill_view(name='reflection-agent'). This skill enforces the journal-and-verify discipline. Every task must produce an evidence trail before the agent declares completion.

## Journal Format

Before marking a task done, output a journal block with exactly three sections:

### 1. Read
List every file read during this task, with the source of truth path. If no files were read, state None.

### 2. Changed
List every file written or patched, with the operation type (write_file, patch, terminal). Include the old file hash or version if available.

### 3. Evidence
Produce verifiable proof for each changed file. At minimum one of:
- diff output (full or summary)
- read_file output of the updated content
- terminal command output confirming the change

## Anti-Hallucination Gate

Before emitting any claim of success, check:
- For each item in Changed, is there a corresponding entry in Evidence?
- Is the evidence raw tool output, not a paraphrase?
- If the answer to either is No, do not declare success. Read the file again or re-run the verification command.

## Verification Proportionality

- 1-5 line change: single diff command
- 6-20 line change: read_file of relevant section
- 21-50 line change: read_file of whole file or functional test
- 51+ line change: standalone verification script or test run
