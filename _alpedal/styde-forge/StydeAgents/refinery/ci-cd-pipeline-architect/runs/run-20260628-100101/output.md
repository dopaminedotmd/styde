ci-cd-pipeline-architect output
Pipeline design for: microservices-deployment-pipeline
github-actions workflow: ci-deploy.yml
name: CI/CD Pipeline
on:
  push:
    branches: [main, staging, dev]
  pull_request:
    branches: [main]
env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: validate required inputs
        run: |
          if [ -z "${{ github.event.inputs.task }}" ] && [ -z "${{ github.event_name }}" ]; then
            echo "No task specified. Checking task.md..."
            if [ -f task.md ]; then
              echo "Using task from task.md"
            else
              echo "ERROR: Neither inline task nor task.md found."
              echo "Format: provide a task inline, create task.md, or pass via workflow_dispatch inputs."
              exit 1
            fi
          fi
      - name: lint
        run: echo "linting..."
      - name: unit-test
        run: echo "running unit tests..."
      - name: type-check
        run: echo "type checking..."
  build-and-push:
    needs: [validate]
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [api-gateway, user-service, order-service]
    steps:
      - uses: actions/checkout@v4
      - name: set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      - name: login to ghcr
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - name: build and push
        uses: docker/build-push-action@v5
        with:
          context: ./services/${{ matrix.service }}
          file: ./services/${{ matrix.service }}/Dockerfile
          push: ${{ github.ref == 'refs/heads/main' }}
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/${{ matrix.service }}:${{ github.sha }}
  deploy-dev:
    needs: [build-and-push]
    if: github.ref == 'refs/heads/dev'
    runs-on: ubuntu-latest
    environment: dev
    steps:
      - name: deploy to dev
        run: echo "Deploying to dev environment..."
  deploy-staging:
    needs: [build-and-push]
    if: github.ref == 'refs/heads/staging'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: canary deploy 10%
        run: echo "Canary 10% -> smoke test -> 50% -> 100%"
      - name: integration test
        run: echo "running integration tests..."
  deploy-production:
    needs: [build-and-push]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: blue-green deploy
        run: |
          echo "Blue: v1 running, Green: v2 deploying"
          echo "health check on green"
          echo "swap load balancer to green"
          echo "keep blue as rollback target"
      - name: smoke test
        run: echo "smoke tests on production..."
      - name: rollback-on-failure
        if: failure()
        run: echo "Auto-rollback: swap load balancer back to blue"
env-promotion plan:
  dev:
    trigger: push to dev branch
    approval: none
    tests: unit + lint
  staging:
    trigger: push to staging branch
    approval: team lead
    tests: integration + e2e
    deploy: canary (10% -> 50% -> 100%)
  production:
    trigger: merge to main
    approval: QA + product owner
    deploy: blue-green
    rollback: automated on health check failure
rollback strategy:
  detect: health check endpoint fails 3 consecutive times within 30s
  action: revert load balancer to previous deployment slot
  notify: Slack #deploy-alerts with commit hash and failure reason
  post-mortem: create GitHub issue with full context
config.yaml blueprint validations:
requiredinputs:
  task:
    required: true
    fallback_chain:
      - prompt: "Check inline task from workflow_dispatch inputs"
      - file: "task.md"
      - example: "Describe your deployment task (e.g., deploy microservices to production with blue-green)"
    abort_on_empty: true
    abort_format: |
      Usage: provide a task field. Options:
        1. Pass via workflow_dispatch inputs
        2. Create a task.md in the blueprint root
        3. Edit the blueprint config.yaml requiredinputs.task.default
  env:
    required: true
    default: dev
    valid: [dev, staging, production]
  approval_mode:
    required: false
    default: auto
    valid: [auto, manual]