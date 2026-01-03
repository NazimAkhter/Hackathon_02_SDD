---
id: 0002
title: Create monorepo architectural plan
stage: plan
date: 2026-01-03
surface: agent
model: claude-sonnet-4-5
feature: 002-monorepo-organization
branch: 002-monorepo-organization
user: developer
command: /sp.plan
labels: ["monorepo", "architecture", "planning", "research", "design"]
links:
  spec: specs/002-monorepo-organization/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-monorepo-organization/plan.md
 - specs/002-monorepo-organization/research.md
 - specs/002-monorepo-organization/data-model.md
 - specs/002-monorepo-organization/quickstart.md
 - specs/002-monorepo-organization/contracts/directory-structure.md
tests:
 - Constitution check passed (no violations)
 - Research decisions documented with rationale
 - Data model defines all directory entities
---

## Prompt

Create architectural plan for monorepo organization including:
- High-level architecture sketch
- Folder structure layout
- Specification organization plan
- Workflow for Spec-Kit Plus and Claude Code
- Guidelines for repo naming and documentation

Decisions needing documentation:
- Single vs multiple services per repo
- Shared vs per-app CLAUDE.md files
- Location of API, DB, and UI specs
- How frontend and backend share specifications
- Environment files and config management

Structure planning:
- .spec-kit/ configuration placement
- specs/ split into features, API, database, UI
- Dedicated frontend/ and backend/ app directories
- Root README and project-wide CLAUDE.md

Constraints:
- Next.js frontend + FastAPI backend
- GitHub-hosted monorepo
- Spec-Kit Plus and Claude Code as primary tools

## Response snapshot

Created comprehensive architectural plan with:
- Technical context and constitution check (PASS)
- Project structure with authoritative directory tree
- Phase 0 research: 7 key architectural decisions documented
  - Centralized specs/ vs distributed
  - Three-tier CLAUDE.md strategy
  - apps/ directory structure
  - Domain-based spec organization
  - Environment file management
  - Spec-Kit Plus integration
  - Documentation approach
- Phase 1 design artifacts:
  - data-model.md: 11 entities (directories/files)
  - quickstart.md: Developer onboarding guide
  - contracts/directory-structure.md: Authoritative layout

## Outcome

- Impact: Architectural foundation established for monorepo supporting Next.js and FastAPI with centralized specifications
- Tests: Constitution check passed, all research decisions validated
- Files: plan.md, research.md, data-model.md, quickstart.md, contracts/directory-structure.md
- Next prompts: /sp.tasks to create implementation tasks
- Reflection: Planning focused on organizational structure rather than code implementation. Three-tier CLAUDE.md approach enables context-specific AI assistance while maintaining centralized spec

s.

## Evaluation notes

- Failure modes observed: None - planning completed successfully
- Graders: Constitution check PASS, Research completeness PASS
- Prompt variant: Standard /sp.plan workflow with research-concurrent approach
- Next experiment: Proceed to task breakdown for implementation
