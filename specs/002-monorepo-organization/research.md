# Research: Monorepo Organization for Full-Stack Projects

**Feature**: 002-monorepo-organization | **Date**: 2026-01-03
**Phase**: 0 (Research) | **Status**: Complete

## Research Questions

1. What are best practices for monorepo folder organization?
2. How should CLAUDE.md files be structured in a monorepo context?
3. Where should API, database, and UI specifications live?
4. How do Next.js and FastAPI projects coexist in a monorepo?
5. How should environment files and configuration be managed?
6. What is the optimal Spec-Kit Plus integration pattern?

---

## Decision 1: Centralized vs. Distributed Specifications

**Context**: Specifications need a storage location.

**Decision**: Centralized specs/ directory at repository root

**Rationale**:
- Single source of truth for all specifications
- Cross-functional teams can access same specs
- Spec-Kit Plus tooling works best with centralized location
- Enables specification versioning independent of application code

**Alternatives Considered**:
- Distributed in apps: Rejected due to duplication
- Mixed approach: Rejected due to inconsistency

**Implementation**:
specs/ with subdirectories for features, api, database, ui

---

## Decision 2: Multi-Level CLAUDE.md Strategy

**Context**: Need context-specific Claude Code instructions.

**Decision**: Three-tier CLAUDE.md hierarchy (root, frontend, backend)

**Rationale**:
- Root CLAUDE.md: Monorepo-wide conventions
- App CLAUDE.md: Framework-specific patterns
- Claude Code reads hierarchically

**Alternatives Considered**:
- Single root only: Rejected, too mixed
- App-level only: Rejected, no shared conventions

---

## Decision 3: Apps Directory Structure

**Context**: Need organization for Next.js and FastAPI apps.

**Decision**: apps/ container with frontend/ and backend/ subdirectories

**Rationale**:
- Clear separation of deployable applications
- Supports future expansion
- Each app maintains framework conventions

---

## Decision 4: Specification Organization by Domain

**Context**: Organize specs within specs/ directory.

**Decision**: Domain-based (features, API, database, UI)

**Rationale**:
- Features: Business capabilities
- API: Technical contracts
- Database: Data models
- UI: Component specifications
- Enables independent evolution

---

## Decision 5: Environment and Configuration

**Context**: Manage environment variables.

**Decision**: App-specific .env files with root .env.example

**Rationale**:
- Each app manages own environment
- Root documents all variables
- Security through .gitignore

---

## Decision 6: Spec-Kit Plus Integration

**Context**: Configure Spec-Kit Plus for monorepo.

**Decision**: Root-level .spec-kit/ directory

**Rationale**:
- Centralized configuration
- Points to specs/ directory
- Custom templates and scripts

---

## Decision 7: Documentation

**Context**: Developer onboarding.

**Decision**: Root README.md with app-specific READMEs

**Rationale**:
- Comprehensive overview at root
- Detailed instructions in each app
- Workflow documentation

---

## Summary

All research questions resolved. Key decisions documented with rationale and alternatives. Ready for Phase 1 design artifacts.
