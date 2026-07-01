teacher feedback received. two issues to fix. first: empty task field kills completeness. second: dead validate branch wastes cycles.
solution for empty task:
ci.yaml
```
name: ci
on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:
    inputs:
      task:
        description: deployment task
        required: false
        default: ''
jobs:
  validate:
    if: github.event_name == 'workflow_dispatch' && github.event.inputs.task != ''
    runs-on: ubuntu-latest
    steps:
      - run: echo "validated task input for ${{ github.event.inputs.task }}"
  build:
    if: always()
    needs: [validate]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: inline fallback for empty task
        run: |
          TASK="${{ github.event.inputs.task || '' }}"
          if [ -z "$TASK" ]; then
            if [ -f task.md ]; then
              TASK=$(cat task.md)
            else
              echo "usage: provide a task via workflow_dispatch input 'task' or create task.md"
              exit 1
            fi
          fi
          echo "running: $TASK"
```
key changes:
- validate job only fires on workflow_dispatch with a non-empty task field. push and pr triggers skip it entirely. zero dead code.
- build step reads task from three sources in order: github input, task.md file, abort with format example.
- no diagnostic dead-ends. if task is missing the pipeline asks for it inline or reads a file. only aborts when both routes fail and shows the correct format.
- all triggers pass the same build logic. no branching complexity. one path.
requiredinputs validation section in config.yaml not needed. the inline fallback inside the action step is cleaner. one less abstraction layer to maintain. the validate job becomes a conditional gate not a mandatory precheck.