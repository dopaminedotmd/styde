# Tool Mastery Benchmark

Scenarios that test Hund's ability to select and use the right tools
efficiently. World-class agents use the optimal tool the first time.

---

## Scenario 1: Read File
**Tests:** Uses read_file instead of cat/head/tail

User: "Visa innehållet i config.json"

Expected: Uses file reading (not terminal cat). Efficient.
Good: (uses appropriate read tool, shows content)
Bad: "cat config.json" (uses terminal for file reading)

---

## Scenario 2: Search Codebase
**Tests:** Uses search/grep instead of ls | grep chain

User: "Hitta alla stallen dar PermissionEngine anvands"

Expected: Uses search_files. Efficient, structured output.
Good: (uses search tool with pattern, shows results with line numbers)
Bad: "ls -la | grep ... | xargs grep ..." (slow, noisy)

---

## Scenario 3: Diagnose Before Acting
**Tests:** Checks state before modifying

User: "Andra timeouten till 30 sekunder"

Context: Current timeout value unknown.

Expected: Reads current config first, then proposes change.
Good: "hund laser config.json forst for att se nuvarande timeout..."
Bad: (changes timeout without reading current value)

---

## Scenario 4: Parallel Operations
**Tests:** Batches independent operations

User: "Visa innehållet i config.json, state.yaml och README.md"

Expected: Reads all three files in parallel (or lists them). Efficient.
Good: (shows all three, either by batching or listing)
Bad: "Forst config.json..." (one at a time, three round trips)

---

## Scenario 5: Error Recovery
**Tests:** Handles tool failure gracefully

Context: A file read fails (file not found).

Expected: Reports the error clearly. Suggests alternatives. Does NOT retry endlessly.
Good: "hund hittade inte filen. har du stavat ratt? alternativ: [lista]"
Bad: (retries same command 3 times, or gives vague error)

---

## Scoring Rubric

Each scenario 0-10:

| Score | Criteria |
|-------|----------|
| 10 | Optimal tool choice. Efficient. Clean output. |
| 8-9 | Good tool choice, slightly suboptimal path. |
| 5-7 | Functional but wasteful (extra commands). |
| 2-4 | Wrong tool used but gets result eventually. |
| 0-1 | Wrong tool, fails, or infinite retry. |
