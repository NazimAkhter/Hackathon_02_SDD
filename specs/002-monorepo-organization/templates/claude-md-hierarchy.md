# CLAUDE.md Hierarchy Documentation

**Version**: 1.0 | **Date**: 2026-01-03
**Feature**: 002-monorepo-organization

## Purpose

This document explains the hierarchical CLAUDE.md file structure used in the monorepo to provide context-specific instructions to Claude Code across different applications.

---

## Overview

The monorepo uses a **three-tier CLAUDE.md hierarchy** to enable Claude Code to understand both monorepo-wide conventions and application-specific patterns.

```
repository-root/
├── CLAUDE.md                    # Tier 1: Root (Monorepo-wide)
└── apps/
    ├── frontend/
    │   └── CLAUDE.md            # Tier 2: Frontend (Next.js)
    └── backend/
        └── CLAUDE.md            # Tier 2: Backend (FastAPI)
```

---

## Hierarchy Levels

### Tier 1: Root CLAUDE.md (`/CLAUDE.md`)

**Scope**: Entire monorepo
**Priority**: Highest (Level 1)
**Read By**: Claude Code in all contexts

**Purpose**:
- Define monorepo-wide conventions
- Document repository structure
- Specify Spec-Driven Development workflow
- Establish version control standards
- Define cross-referencing patterns

**Content Sections**:

1. **Project Overview**
   - Monorepo purpose and organization
   - Applications contained (frontend, backend)
   - Specification structure

2. **Repository Structure**
   ```
   monorepo/
   ├── apps/           # Applications
   ├── specs/          # Specifications
   └── .spec-kit/      # Spec-Kit Plus config
   ```

3. **Spec-Driven Development**
   - Workflow: spec → plan → tasks
   - Feature directory structure
   - Cross-domain specifications

4. **Version Control**
   - Branch naming: `###-feature-name`
   - Commit format: `<type>: <description>`
   - Feature branch workflow

5. **Specification Locations**
   - Features: `specs/features/`
   - API: `specs/api/`
   - Database: `specs/database/`
   - UI: `specs/ui/`

6. **Cross-Reference Patterns**
   - Relative path conventions
   - Bidirectional references

**Example Content**:
```markdown
# Claude Code Rules - Monorepo Root

This monorepo contains Next.js frontend and FastAPI backend applications with centralized Spec-Kit Plus specifications.

## Structure

- `apps/frontend/` - Next.js application
- `apps/backend/` - FastAPI application
- `specs/` - Centralized specifications
  - `features/` - Feature specs
  - `api/` - API contracts
  - `database/` - Data models
  - `ui/` - UI components

## Spec-Driven Development

Follow this workflow:
1. Create spec: `specs/features/###-name/spec.md`
2. Create plan: `plan.md`
3. Create tasks: `tasks.md`
4. Implement in apps/

## Version Control

- Feature branches: `###-feature-name`
- Commit format: `feat: description` or `fix: description`
```

---

### Tier 2: Application CLAUDE.md

#### Frontend CLAUDE.md (`/apps/frontend/CLAUDE.md`)

**Scope**: Next.js frontend application
**Priority**: Level 2 (when in `apps/frontend/`)
**Inherits From**: Root CLAUDE.md

**Purpose**:
- Next.js-specific patterns
- React component conventions
- Tailwind CSS styling patterns
- API client implementation
- Frontend testing strategies

**Content Sections**:

1. **Framework and Tools**
   - Next.js version and configuration
   - TypeScript settings
   - Package manager

2. **Directory Structure**
   ```
   src/
   ├── app/              # Next.js App Router
   ├── components/       # React components
   │   ├── ui/          # Reusable UI
   │   └── features/    # Feature-specific
   └── lib/             # Utilities and API clients
   ```

3. **Component Patterns**
   - Server Components vs Client Components
   - Prop TypeScript interfaces
   - Styling with Tailwind CSS
   - File naming conventions

4. **API Integration**
   - Base URL configuration
   - Fetch patterns for Server Components
   - SWR/React Query for Client Components
   - Error handling

5. **State Management**
   - React Context
   - Third-party libraries (Zustand, etc.)
   - Server state vs client state

6. **Testing**
   - Jest configuration
   - React Testing Library
   - Test file naming
   - Coverage requirements

**Example Content**:
```markdown
# Claude Code Rules - Frontend (Next.js)

## Framework

- Next.js 14+ with App Router
- TypeScript strict mode
- React Server Components by default

## Directory Structure

```
src/
├── app/           # Pages (App Router)
├── components/    # React components
└── lib/          # Utilities
```

## Component Patterns

**Server Components** (default):
```tsx
// app/todos/page.tsx
export default async function TodosPage() {
  const todos = await fetchTodos()
  return <TodoList todos={todos} />
}
```

**Client Components** (interactive):
```tsx
"use client"

export function TodoCard({ todo }: TodoCardProps) {
  const [isCompleted, setIsCompleted] = useState(todo.completed)
  // ...
}
```

## Styling

- Tailwind CSS for all styles
- No inline styles
- Use `cn()` utility for conditional classes

## API Integration

```typescript
// lib/api/todos.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL

export async function fetchTodos() {
  const res = await fetch(`${API_URL}/api/v1/todos`)
  return res.json()
}
```

## Testing

- Unit tests: `ComponentName.test.tsx`
- Run: `npm test`
- Coverage: `npm run test:coverage`
```

---

#### Backend CLAUDE.md (`/apps/backend/CLAUDE.md`)

**Scope**: FastAPI backend application
**Priority**: Level 2 (when in `apps/backend/`)
**Inherits From**: Root CLAUDE.md

**Purpose**:
- FastAPI-specific patterns
- SQLAlchemy ORM conventions
- API endpoint implementation
- Pydantic validation patterns
- Backend testing strategies

**Content Sections**:

1. **Framework and Tools**
   - FastAPI version
   - Python version
   - Pydantic version
   - Database ORM

2. **Directory Structure**
   ```
   src/
   ├── models/          # SQLAlchemy models
   ├── routes/          # API routes
   ├── services/        # Business logic
   ├── schemas/         # Pydantic schemas
   └── main.py          # App entry point
   ```

3. **API Design Patterns**
   - Endpoint naming conventions
   - Request/response models
   - Error handling
   - Status codes

4. **Database Patterns**
   - Model definitions
   - Relationships
   - Migrations with Alembic
   - Connection management

5. **Validation and Schemas**
   - Pydantic model patterns
   - Request validation
   - Response serialization

6. **Testing**
   - pytest configuration
   - Fixtures
   - Test database
   - Coverage requirements

**Example Content**:
```markdown
# Claude Code Rules - Backend (FastAPI)

## Framework

- FastAPI 0.104+
- Python 3.11+
- SQLAlchemy 2.0+
- Pydantic v2

## Directory Structure

```
src/
├── models/       # Database models
├── routes/       # API endpoints
├── services/     # Business logic
├── schemas/      # Pydantic models
└── main.py       # Entry point
```

## API Design

**Route Pattern**:
```python
from fastapi import APIRouter
from schemas import TodoCreate, TodoResponse

router = APIRouter(prefix="/api/v1/todos")

@router.post("/", response_model=TodoResponse)
async def create_todo(todo: TodoCreate):
    # Implementation
    pass
```

**Error Handling**:
```python
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="Todo not found")
```

## Database Models

**SQLAlchemy Pattern**:
```python
from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    completed = Column(Boolean, default=False)
```

## Pydantic Schemas

```python
from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str
    completed: bool = False

class TodoResponse(TodoCreate):
    id: int
```

## Testing

- pytest for all tests
- Test files: `test_*.py`
- Run: `pytest`
- Coverage: `pytest --cov`
```

---

## Context Resolution

### How Claude Code Reads CLAUDE.md Files

**Location-Based Context**:

1. **At Repository Root** (`/monorepo/`)
   - Reads: `/CLAUDE.md` only
   - Context: Monorepo-wide conventions

2. **In Frontend Directory** (`/monorepo/apps/frontend/`)
   - Reads: `/CLAUDE.md` + `/apps/frontend/CLAUDE.md`
   - Context: Monorepo conventions + Next.js patterns

3. **In Backend Directory** (`/monorepo/apps/backend/`)
   - Reads: `/CLAUDE.md` + `/apps/backend/CLAUDE.md`
   - Context: Monorepo conventions + FastAPI patterns

### Priority and Inheritance

**Rule**: Application CLAUDE.md inherits from and can override root CLAUDE.md

**Example**:

**Root CLAUDE.md**:
```markdown
## Code Style
- Use consistent indentation
- Follow language conventions
```

**Frontend CLAUDE.md**:
```markdown
## Code Style (inherits from root)
- Use consistent indentation (inherited)
- Follow language conventions (inherited)
- Use 2-space indentation for TypeScript/JSX (override)
- Use Prettier for formatting (addition)
```

**Backend CLAUDE.md**:
```markdown
## Code Style (inherits from root)
- Use consistent indentation (inherited)
- Follow language conventions (inherited)
- Use 4-space indentation for Python (override)
- Use Black for formatting (addition)
```

---

## Content Guidelines

### What Goes in Root CLAUDE.md

✅ **Include**:
- Repository structure and organization
- Monorepo-wide conventions
- Spec-Driven Development workflow
- Specification locations and cross-references
- Version control standards
- Shared principles applicable to all apps

❌ **Exclude**:
- Framework-specific patterns (Next.js, FastAPI)
- Language-specific conventions (TypeScript, Python)
- Application-specific tooling
- Implementation details

### What Goes in Application CLAUDE.md

✅ **Include**:
- Framework-specific patterns
- Application directory structure
- Language conventions
- API/database integration patterns
- Testing frameworks and patterns
- Build and deployment commands
- Environment variable usage

❌ **Exclude**:
- Monorepo-wide structure (defined in root)
- Spec-Kit Plus workflow (defined in root)
- Version control standards (defined in root)
- Other application's patterns

---

## Updating CLAUDE.md Files

### When to Update Root CLAUDE.md

- Adding new applications to monorepo
- Changing specification structure
- Updating version control standards
- Modifying Spec-Driven Development workflow
- Adding new spec domains (e.g., `specs/testing/`)

### When to Update Application CLAUDE.md

- Upgrading framework version
- Changing directory structure
- Adopting new libraries or patterns
- Updating testing strategies
- Modifying API integration patterns

---

## Validation Checklist

### Root CLAUDE.md Validation

- [ ] Documents all applications in monorepo
- [ ] Defines specification structure
- [ ] Explains Spec-Driven Development workflow
- [ ] Specifies version control standards
- [ ] Defines cross-referencing patterns
- [ ] No framework-specific details

### Application CLAUDE.md Validation

- [ ] Documents application directory structure
- [ ] Defines framework-specific patterns
- [ ] Specifies testing framework and commands
- [ ] Documents API/database integration
- [ ] Includes build and run commands
- [ ] References root CLAUDE.md for monorepo conventions

---

## Examples

### Complete Root CLAUDE.md

See template: [CLAUDE.md.root.template](./CLAUDE.md.root.template)

### Complete Frontend CLAUDE.md

See template: [CLAUDE.md.frontend.template](./CLAUDE.md.frontend.template)

### Complete Backend CLAUDE.md

See template: [CLAUDE.md.backend.template](./CLAUDE.md.backend.template)

---

## Troubleshooting

### Issue: Claude Code Not Following App Patterns

**Symptom**: Claude Code uses wrong framework patterns

**Diagnosis**: Check current working directory
```bash
pwd
# If at root, only root CLAUDE.md is read
```

**Solution**: Change to application directory
```bash
cd apps/frontend  # or apps/backend
# Now reads app-specific CLAUDE.md
```

---

### Issue: Conflicting Instructions

**Symptom**: Contradictory guidance from root and app CLAUDE.md

**Diagnosis**: Check for conflicting rules

**Solution**: Application CLAUDE.md should override with explicit note:
```markdown
## Code Style (overrides root)
Root specifies consistent indentation.
Frontend uses 2-space indentation (TypeScript convention).
```

---

### Issue: Duplicated Content

**Symptom**: Same content in root and application CLAUDE.md

**Diagnosis**: Root rules repeated in app files

**Solution**: Reference root instead of duplicating:
```markdown
# apps/frontend/CLAUDE.md

## Version Control
See root CLAUDE.md for branch naming and commit conventions.

## Frontend-Specific Conventions
- Component file naming: PascalCase
- Hook file naming: camelCase starting with "use"
```

---

## Best Practices

### ✅ DO:

- Keep root CLAUDE.md framework-agnostic
- Document application structure in app CLAUDE.md
- Use consistent section headings across files
- Reference root from app files when appropriate
- Update all relevant files when changing standards
- Include examples in application files

### ❌ DON'T:

- Duplicate monorepo conventions in app files
- Put framework-specific details in root file
- Create CLAUDE.md for non-application directories
- Use absolute paths (use relative paths)
- Contradict root guidelines without explicit override
- Omit CLAUDE.md from any application

---

## File Templates

### Root CLAUDE.md Template Structure

```markdown
# Claude Code Rules - Monorepo Root

## Project Overview
[Describe monorepo purpose and applications]

## Repository Structure
[Document directory layout]

## Spec-Driven Development
[Explain workflow: spec → plan → tasks]

## Version Control
[Define branch naming and commit format]

## Specification Organization
[Document specs/ structure and cross-references]
```

### Application CLAUDE.md Template Structure

```markdown
# Claude Code Rules - [Application Name]

## Framework
[Framework version and configuration]

## Directory Structure
[Application file organization]

## [Framework] Patterns
[Framework-specific conventions]

## API/Database Integration
[Backend/frontend integration patterns]

## Testing
[Testing framework and commands]

## Build and Run
[Development and production commands]
```

---

**Maintained by**: Development Team
**Last Updated**: 2026-01-03
**Related**: [Claude Code Workflow](./claude-code-workflow.md)
