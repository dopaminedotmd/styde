MISSING INPUT HANDLING: When a section's content cannot be determined from available input, the agent MUST:
  1. Inspect the filesystem for actual files and configs in the current project
  2. Run commands to discover tooling, frameworks, and project structure
  3. If inspection still produces no evidence, offer the user specific alternatives: paste relevant output, point to a file path, or provide an example of the format needed
  4. Aborting to generic defaults or boilerplate is FORBIDDEN
EVERY SECTION in the report must reference at least one concrete file path, command output, or observed behaviour from this specific project. If no evidence exists, state exactly what is missing and how the user can provide it. Do not emit default or placeholder content under any circumstance.
EVIDENCE SOURCES (priority order):
  - Real file contents read from disk (path must be absolute or relative to project root)
  - Output of actual commands run via terminal tool
  - Observed behaviour from live inspection (config files, directory structure, installed packages)
  - Only if all above fail: user-provided paste or file reference
VALIDATION: After drafting each section, verify at least one evidence anchor exists. If none does, the section must be rewritten or removed.