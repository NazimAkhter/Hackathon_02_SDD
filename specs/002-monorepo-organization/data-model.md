# Data Model: Monorepo Directory Structure

**Feature**: 002-monorepo-organization | **Date**: 2026-01-03

## Overview

This document defines the entities (directories and files) that comprise the monorepo organizational structure. Unlike traditional data models with database entities, this model describes the filesystem structure.

## Core Entities

### 1. MonorepoRoot

**Purpose**: Top-level repository directory

**Attributes**:
- repository_name: string (e.g., "hackathon-todo")
- git_initialized: boolean
- has_readme: boolean
- has_root_claude_md: boolean

**Contains**:
- AppsContainer (1)
- SpecsRepository (1)
- SpecKitConfig (1)
- RootDocumentation (multiple files)

**Validation Rules**:
- Must contain .git directory
- Must contain README.md
- Must contain CLAUDE.md
- Must contain .gitignore

---

### 2. AppsContainer

**Purpose**: Container for all deployable applications

**Path**: /apps/

**Contains**:
- FrontendApp (1)
- BackendApp (1)
- Additional apps (0..n, future expansion)

**Validation Rules**:
- Must exist at repository root
- Must contain at least one application

---

### 3. FrontendApp

**Purpose**: Next.js frontend application

**Path**: /apps/frontend/

**Attributes**:
- framework: "Next.js"
- package_manager: "npm" | "yarn" | "pnpm"
- has_claude_md: boolean

**Contains**:
- src/ (source code)
- public/ (static assets)
- tests/ (test files)
- package.json
- next.config.js
- tsconfig.json
- CLAUDE.md

**Validation Rules**:
- Must contain package.json with Next.js dependency
- Must contain CLAUDE.md
- Must follow Next.js project structure conventions

---

### 4. BackendApp

**Purpose**: FastAPI backend application

**Path**: /apps/backend/

**Attributes**:
- framework: "FastAPI"
- python_version: "3.11+"
- has_claude_md: boolean

**Contains**:
- src/ (source code)
- tests/ (test files)
- pyproject.toml | requirements.txt
- CLAUDE.md

**Validation Rules**:
- Must contain dependency file (pyproject.toml or requirements.txt)
- Must contain CLAUDE.md with FastAPI guidance
- Must follow Python project structure conventions

---

### 5. SpecsRepository

**Purpose**: Centralized specification storage

**Path**: /specs/

**Contains**:
- FeaturesDirectory (1)
- ApiDirectory (1)
- DatabaseDirectory (1)
- UiDirectory (1)

**Validation Rules**:
- Must contain all four subdirectories
- Must be accessible from root

---

### 6. FeaturesDirectory

**Purpose**: Feature-specific specifications

**Path**: /specs/features/

**Contains**:
- FeatureSpec (multiple, named ###-feature-name/)

**Structure**:
Each feature contains:
- spec.md
- plan.md
- tasks.md
- checklists/ (optional)
- contracts/ (optional)

**Validation Rules**:
- Features numbered sequentially (001, 002, ...)
- Each feature must have spec.md at minimum

---

### 7. ApiDirectory

**Purpose**: API contract specifications

**Path**: /specs/api/

**Contains**:
- endpoints/ (OpenAPI/Swagger specs)
- schemas/ (request/response models)
- versioning.md

**Validation Rules**:
- API specs must be machine-readable (YAML/JSON)
- Must document all endpoints used by frontend and backend

---

### 8. DatabaseDirectory

**Purpose**: Database schema specifications

**Path**: /specs/database/

**Contains**:
- entities/ (entity definitions)
- migrations/ (migration plans)
- schema.md (overall schema documentation)

**Validation Rules**:
- Entity definitions must specify fields and relationships
- Schema must be technology-agnostic

---

### 9. UiDirectory

**Purpose**: UI/UX specifications

**Path**: /specs/ui/

**Contains**:
- components/ (component specs)
- design-tokens/ (colors, typography, spacing)
- interactions.md

**Validation Rules**:
- Component specs must define props and behavior
- Design tokens must be framework-agnostic

---

### 10. SpecKitConfig

**Purpose**: Spec-Kit Plus configuration

**Path**: /.spec-kit/

**Contains**:
- config.yaml
- templates/ (custom templates)
- scripts/ (automation scripts)

**Attributes**:
- specs_directory: path
- api_specs: path
- db_specs: path
- ui_specs: path

**Validation Rules**:
- config.yaml must be valid YAML
- Paths must reference existing directories

---

### 11. CLAUDEFile

**Purpose**: Claude Code context-specific instructions

**Locations**:
- /CLAUDE.md (root-level)
- /apps/frontend/CLAUDE.md
- /apps/backend/CLAUDE.md

**Attributes**:
- scope: "root" | "frontend" | "backend"
- priority: integer (root=1, app=2)

**Content Sections**:
- Project overview
- Development guidelines
- Framework-specific patterns
- Testing strategies
- Code style conventions

**Validation Rules**:
- Must exist at all three levels
- Must be markdown format
- Must not conflict with higher-priority rules

---

## Entity Relationships

```
MonorepoRoot
├── AppsContainer
│   ├── FrontendApp
│   │   └── CLAUDEFile (frontend)
│   └── BackendApp
│       └── CLAUDEFile (backend)
├── SpecsRepository
│   ├── FeaturesDirectory
│   ├── ApiDirectory
│   ├── DatabaseDirectory
│   └── UiDirectory
├── SpecKitConfig
└── CLAUDEFile (root)
```

---

## State Transitions

### Repository Initialization

1. Empty directory → MonorepoRoot (git init)
2. MonorepoRoot → + AppsContainer
3. MonorepoRoot → + SpecsRepository
4. MonorepoRoot → + SpecKitConfig
5. Each container → + required subdirectories
6. Each level → + CLAUDEFile

### Feature Addition

1. FeaturesDirectory → + new FeatureSpec (numbered)
2. FeatureSpec → + spec.md (specification phase)
3. FeatureSpec → + plan.md (planning phase)
4. FeatureSpec → + tasks.md (task breakdown phase)

### Application Addition

1. AppsContainer → + NewApp directory
2. NewApp → + framework files
3. NewApp → + CLAUDE.md
4. NewApp → + dependency files

---

## Validation Checklist

**MonorepoRoot**:
- [ ] .git directory exists
- [ ] README.md exists and documents structure
- [ ] CLAUDE.md exists with monorepo guidelines
- [ ] .gitignore excludes .env files

**AppsContainer**:
- [ ] apps/ directory exists
- [ ] Contains frontend/ and backend/
- [ ] Each app has CLAUDE.md

**SpecsRepository**:
- [ ] specs/ directory exists
- [ ] Contains features/, api/, database/, ui/
- [ ] Features are numbered sequentially

**SpecKitConfig**:
- [ ] .spec-kit/ directory exists
- [ ] config.yaml is valid YAML
- [ ] Paths reference existing directories

**Cross-Verification**:
- [ ] All CLAUDE.md files exist and are non-empty
- [ ] API specs match backend implementation capabilities
- [ ] Database specs referenced by backend models
- [ ] UI specs referenced by frontend components

---

**Phase 1 Complete** | Data model defines all directory and file entities
