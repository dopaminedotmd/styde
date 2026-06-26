---
title: "_README — Agents Templates"
date: 2026-06-24
author: agy
tags: [area/OPS, status/APPROVED, author/AGY, type/TEMPLATE]
status: approved
---

# _README — Agents Templates

This directory contains templates for AI agents delivered to customers.

## Structure

Each template is a directory with:
- `prompt.md` — Agent system prompt. STERILE. No internal references.
- `tools.yaml` — API tools available to the agent
- `config.yaml` — Template for customer-specific configuration
- `tests/` — input.json + expected.json for testing

## Rules

- Nothing in templates/ references Hermes, ca-skills, obsidian, or any internal system
- All customer-specific data (email, folder IDs, max_cost) lives in config.yaml, NEVER in prompt.md
- ca-agent-builder uses these templates to generate agents/deployed/{customer}/

## Usage

1. ca-agent-builder reads the template for the correct agent type
2. Fills in customer-specific data from audit
3. Writes to agents/deployed/{customer}/{agent}/
4. Creates tests/input.json + expected.json from template
