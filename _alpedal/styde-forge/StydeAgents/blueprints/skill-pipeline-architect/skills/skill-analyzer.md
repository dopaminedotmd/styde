# Skill Analyzer

## Purpose
Analyze skill files in a blueprint's skills/ directory. Extract structure, inputs, outputs, and dependencies from each SKILL.md file.

## Inputs
- skills_directory: Path string to the skills/ directory to scan
- (optional) skill_definitions: Previously analyzed skill data for cross-reference

## Outputs
A YAML mapping with key `skills_analyzed` containing:
```yaml
skills_analyzed:
  - name: <skill-file-name>
    has_purpose: true|false
    has_inputs: list of input names
    has_outputs: list of output names
    dependencies: list of referenced skills
    lines_of_code: <int>
```

## Behavior
1. Scan the skills/ directory for all *.md files
2. For each file, parse:
   - ## Purpose section (required for valid skill)
   - ## Inputs section (list expected inputs)
   - ## Outputs section (list declared outputs)
   - Any cross-references to other skills (## Dependencies or references to other skill names)
3. Return the structured analysis as YAML

## Error Handling
- If skills_directory doesn't exist, return empty list with warning
- If a skill file lacks ## Purpose, flag it as invalid
- Return valid YAML even if no skills found
