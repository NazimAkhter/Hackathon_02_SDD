# Claude Code Workflow in Monorepo

**Version**: 1.0 | **Date**: 2026-01-03
**Feature**: 002-monorepo-organization

## Purpose

This document explains how to use Claude Code effectively in a monorepo containing Next.js frontend and FastAPI backend applications with centralized Spec-Kit Plus specifications.

---

## Overview

Claude Code is an AI-powered development assistant that reads your codebase context and helps with implementation. In a monorepo, Claude Code uses a hierarchical CLAUDE.md file system to understand project-wide conventions and application-specific patterns.

---

## CLAUDE.md Hierarchy

The monorepo uses a three-tier CLAUDE.md structure:

```
repository-root/
├── CLAUDE.md                    # Level 1: Root (priority 1)
├── apps/
│   ├── frontend/
│   │   └── CLAUDE.md            # Level 2: Frontend (priority 2)
│   └── backend/
│       └── CLAUDE.md            # Level 2: Backend (priority 3)
└── specs/                       # Centralized specifications
```

**Priority Order**:
1. **Root CLAUDE.md**: Monorepo-wide conventions (highest priority)
2. **App CLAUDE.md**: Application-specific patterns (overrides root when in app context)

**How Claude Code Reads Context**:
- When working at repository root: Reads only root CLAUDE.md
- When working in `apps/frontend/`: Reads root + frontend CLAUDE.md
- When working in `apps/backend/`: Reads root + backend CLAUDE.md

---

## Root CLAUDE.md (`/CLAUDE.md`)

**Purpose**: Define monorepo-wide conventions

**Content Sections**:
1. **Project Structure**: Directory organization
2. **Spec-Driven Development**: Workflow and methodology
3. **Version Control**: Branch naming, commit conventions
4. **Cross-Project Standards**: Shared coding standards
5. **Specification Locations**: Where to find specs/, API docs, entities

**Example**:
```markdown
# Claude Code Rules - Monorepo Root

## Project Structure

This is a monorepo with:
- `apps/frontend/` - Next.js application
- `apps/backend/` - FastAPI application
- `specs/` - Centralized specifications

## Spec-Driven Development

Follow spec → plan → tasks workflow:
1. Create feature spec in `specs/features/###-name/`
2. Reference API contracts in `specs/api/`
3. Reference entities in `specs/database/`
4. Reference UI components in `specs/ui/`

## Version Control

- Feature branches: `###-feature-name`
- Commit format: `<type>: <description>`
- Types: feat, fix, docs, refactor, test

## Cross-Reference Paths

From feature specs:
- API: `../../api/endpoints/[resource].yaml`
- Database: `../../database/entities/[entity].md`
- UI: `../../ui/components/[component].md`
```

---

## Frontend CLAUDE.md (`/apps/frontend/CLAUDE.md`)

**Purpose**: Next.js-specific patterns and conventions

**Content Sections**:
1. **Framework**: Next.js version and conventions
2. **Directory Structure**: App Router, components, lib
3. **Styling**: Tailwind CSS, design tokens
4. **State Management**: React Context, Zustand, etc.
5. **API Integration**: How to consume backend APIs
6. **Testing**: Jest, React Testing Library

**Example**:
```markdown
# Claude Code Rules - Frontend (Next.js)

## Framework

- Next.js 14+ with App Router
- TypeScript strict mode enabled
- React Server Components by default

## Directory Structure

```
src/
├── app/              # App Router pages
├── components/       # React components
│   ├── ui/          # Reusable UI components
│   └── features/    # Feature-specific components
└── lib/             # Utilities and API clients
```

## Component Patterns

- Use Server Components unless interactivity required
- Client Components: "use client" directive
- Colocate styles with components
- Props: TypeScript interfaces exported

## API Integration

- API base URL: `process.env.NEXT_PUBLIC_API_URL`
- Use `fetch` for Server Components
- Use SWR or React Query for Client Components
- API types: Generate from OpenAPI specs in `specs/api/`

## Styling

- Tailwind CSS for all styling
- Design tokens from `specs/ui/design-tokens/`
- No inline styles
- Use `cn()` utility for conditional classes

## Testing

- Unit tests: `*.test.tsx` alongside components
- Integration tests: `__tests__/` directory
- Run: `npm test`
```

---

## Backend CLAUDE.md (`/apps/backend/CLAUDE.md`)

**Purpose**: FastAPI-specific patterns and conventions

**Content Sections**:
1. **Framework**: FastAPI and Python version
2. **Directory Structure**: Models, routes, services
3. **Database**: ORM, migrations, connection
4. **API Design**: Endpoint patterns, validation
5. **Authentication**: JWT, OAuth2, etc.
6. **Testing**: pytest, coverage

**Example**:
```markdown
# Claude Code Rules - Backend (FastAPI)

## Framework

- FastAPI 0.104+
- Python 3.11+
- Pydantic v2 for data validation

## Directory Structure

```
src/
├── models/          # Database models (SQLAlchemy)
├── routes/          # API route handlers
├── services/        # Business logic
├── schemas/         # Pydantic request/response models
└── main.py          # Application entry point
```

## API Design

- Follow OpenAPI specs in `specs/api/endpoints/`
- Endpoint naming: `/api/v1/[resource]`
- Use Pydantic models for validation
- Return structured responses

**Example Route**:
```python
from fastapi import APIRouter
from schemas import TodoCreate, TodoResponse

router = APIRouter(prefix="/api/v1/todos")

@router.post("/", response_model=TodoResponse)
async def create_todo(todo: TodoCreate):
    # Implementation
    pass
```

## Database

- SQLAlchemy ORM
- Entity specs: `specs/database/entities/`
- Alembic for migrations
- Connection pooling enabled

## Error Handling

- Use FastAPI HTTPException
- Standard error codes:
  - 400: Bad Request
  - 401: Unauthorized
  - 404: Not Found
  - 500: Internal Server Error

## Testing

- pytest for all tests
- Test files: `test_*.py`
- Fixtures: `conftest.py`
- Run: `pytest`
- Coverage: `pytest --cov`
```

---

## Common Workflows

### Workflow 1: Implementing New Feature

**Scenario**: Implement "Todo Management" feature

**Steps**:

1. **Start at Repository Root**
   ```bash
   cd /path/to/monorepo
   ```
   Claude Code reads: `/CLAUDE.md` (monorepo conventions)

2. **Review Feature Specification**
   ```bash
   # Claude Code: Read specs/features/001-todo-management/spec.md
   ```
   Understand requirements, user stories, success criteria

3. **Review Technical Design**
   ```bash
   # Claude Code: Read specs/features/001-todo-management/plan.md
   ```
   Understand architecture, tech stack, file structure

4. **Check Cross-References**
   - API: `specs/api/endpoints/todos.yaml`
   - Database: `specs/database/entities/todo.md`
   - UI: `specs/ui/components/todo-card.md`

5. **Implement Backend First**
   ```bash
   cd apps/backend
   ```
   Claude Code reads: `/CLAUDE.md` + `/apps/backend/CLAUDE.md`

   - Create database model: `src/models/todo.py`
   - Create schemas: `src/schemas/todo.py`
   - Create routes: `src/routes/todos.py`
   - Create services: `src/services/todo_service.py`
   - Write tests: `tests/test_todos.py`

6. **Implement Frontend**
   ```bash
   cd ../frontend
   ```
   Claude Code reads: `/CLAUDE.md` + `/apps/frontend/CLAUDE.md`

   - Create API client: `src/lib/api/todos.ts`
   - Create components: `src/components/features/todos/`
   - Create pages: `src/app/todos/page.tsx`
   - Write tests: `src/components/features/todos/*.test.tsx`

7. **Integration Testing**
   ```bash
   cd ../..  # Back to root
   ```
   - Start backend: `cd apps/backend && uvicorn src.main:app`
   - Start frontend: `cd apps/frontend && npm run dev`
   - Test end-to-end functionality

---

### Workflow 2: Adding New API Endpoint

**Scenario**: Add `/api/v1/todos/:id/complete` endpoint

**Steps**:

1. **Update API Specification**
   ```bash
   # Edit specs/api/endpoints/todos.yaml
   ```
   Add new endpoint with request/response schemas

2. **Implement in Backend**
   ```bash
   cd apps/backend
   ```
   Claude Code context: Backend patterns from CLAUDE.md

   - Update route: `src/routes/todos.py`
   - Add service method: `src/services/todo_service.py`
   - Write tests: `tests/test_todos.py`

3. **Update Frontend**
   ```bash
   cd ../frontend
   ```
   Claude Code context: Frontend patterns from CLAUDE.md

   - Update API client: `src/lib/api/todos.ts`
   - Update component: `src/components/features/todos/TodoCard.tsx`

---

### Workflow 3: Creating New UI Component

**Scenario**: Build TodoCard component

**Steps**:

1. **Create Component Specification**
   ```bash
   # Create specs/ui/components/todo-card.md
   ```
   Document props, behavior, styling, accessibility

2. **Implement Component**
   ```bash
   cd apps/frontend
   ```
   Claude Code reads: Frontend CLAUDE.md (React patterns)

   - Create component: `src/components/features/todos/TodoCard.tsx`
   - Create styles: Use Tailwind (per CLAUDE.md)
   - Create tests: `TodoCard.test.tsx`

3. **Reference Entity Data**
   ```markdown
   # In component spec
   Props based on [Todo Entity](../../database/entities/todo.md)
   ```

---

### Workflow 4: Database Schema Update

**Scenario**: Add `priority` field to Todo entity

**Steps**:

1. **Update Entity Specification**
   ```bash
   # Edit specs/database/entities/todo.md
   ```
   Add priority field definition

2. **Update Backend Model**
   ```bash
   cd apps/backend
   ```
   Claude Code context: Backend CLAUDE.md (SQLAlchemy patterns)

   - Update model: `src/models/todo.py`
   - Create migration: `alembic revision -m "add_priority_to_todos"`
   - Update schemas: `src/schemas/todo.py`

3. **Update API Specification**
   ```bash
   # Edit specs/api/endpoints/todos.yaml
   ```
   Add priority field to request/response schemas

4. **Update Frontend**
   ```bash
   cd apps/frontend
   ```
   - Update TypeScript types
   - Update components to display priority

---

## Context Switching Best Practices

### When to Switch Directories

**Work at Root** when:
- Creating new specifications in `specs/`
- Updating repository-wide documentation
- Managing git branches and commits
- Coordinating cross-project changes

**Work in `apps/backend/`** when:
- Implementing API endpoints
- Creating database models
- Writing backend tests
- Managing Python dependencies

**Work in `apps/frontend/`** when:
- Building UI components
- Creating pages and routes
- Writing frontend tests
- Managing npm packages

### Context Awareness

Claude Code automatically adjusts context based on working directory:

```bash
# At root
pwd  # /monorepo
# Claude reads: /CLAUDE.md (monorepo conventions)

cd apps/backend
# Claude reads: /CLAUDE.md + /apps/backend/CLAUDE.md (backend patterns)

cd ../frontend
# Claude reads: /CLAUDE.md + /apps/frontend/CLAUDE.md (frontend patterns)
```

---

## Tips for Effective Claude Code Usage

### 1. Start with Specifications
Always review specs before coding:
```bash
# Read feature spec first
cat specs/features/001-todo-management/spec.md

# Then read plan
cat specs/features/001-todo-management/plan.md

# Then read tasks
cat specs/features/001-todo-management/tasks.md
```

### 2. Reference Cross-Domain Specs
When implementing, keep related specs open:
```bash
# Backend implementation references:
- API: specs/api/endpoints/todos.yaml
- Entity: specs/database/entities/todo.md

# Frontend implementation references:
- API: specs/api/endpoints/todos.yaml
- Component: specs/ui/components/todo-card.md
```

### 3. Use Relative Paths
Claude Code understands monorepo structure:
```bash
# From feature spec
API: ../../api/endpoints/todos.yaml
Entity: ../../database/entities/todo.md
```

### 4. Leverage CLAUDE.md Instructions
Each CLAUDE.md provides context-specific patterns:
- Root: Monorepo conventions
- Backend: FastAPI patterns, ORM usage
- Frontend: React patterns, Tailwind usage

### 5. Test in Context
Run tests in the appropriate directory:
```bash
# Backend tests
cd apps/backend
pytest

# Frontend tests
cd apps/frontend
npm test
```

---

## Troubleshooting

### Issue: Claude Code Not Following App Patterns

**Cause**: Working at root level instead of app directory

**Solution**:
```bash
cd apps/[frontend|backend]
# Now Claude reads app-specific CLAUDE.md
```

---

### Issue: Cannot Find Specifications

**Cause**: Using absolute paths instead of relative paths

**Solution**:
```markdown
# ❌ Wrong
/specs/api/endpoints/todos.yaml

# ✅ Correct
../../api/endpoints/todos.yaml
```

---

### Issue: Mixing Frontend and Backend Patterns

**Cause**: Claude Code reading wrong CLAUDE.md

**Solution**: Ensure you're in the correct directory
```bash
# Backend work
cd apps/backend  # Reads backend CLAUDE.md

# Frontend work
cd apps/frontend  # Reads frontend CLAUDE.md
```

---

## Integration with Spec-Kit Plus

### Running Spec-Kit Commands

Spec-Kit Plus commands work at repository root:

```bash
# At repository root
cd /monorepo

# Create new feature
sp.specify "Todo Management"

# Generate plan
sp.plan

# Generate tasks
sp.tasks

# All outputs go to specs/features/###-feature-name/
```

### Workflow Integration

1. **Specification Phase** (root):
   ```bash
   sp.specify "Feature Name"
   # Creates specs/features/###-feature-name/spec.md
   ```

2. **Planning Phase** (root):
   ```bash
   sp.plan
   # Creates plan.md with technical design
   ```

3. **Task Generation** (root):
   ```bash
   sp.tasks
   # Creates tasks.md with implementation tasks
   ```

4. **Implementation Phase** (apps):
   ```bash
   # Backend tasks
   cd apps/backend
   # Implement with Claude Code

   # Frontend tasks
   cd apps/frontend
   # Implement with Claude Code
   ```

---

## Example Session

Complete workflow example:

```bash
# 1. Create feature specification
cd /monorepo
sp.specify "User Authentication"
# Output: specs/features/002-user-authentication/spec.md

# 2. Generate plan
sp.plan
# Output: specs/features/002-user-authentication/plan.md

# 3. Generate tasks
sp.tasks
# Output: specs/features/002-user-authentication/tasks.md

# 4. Implement backend
cd apps/backend
# Claude Code reads: Root + Backend CLAUDE.md
# Create: src/models/user.py
# Create: src/routes/auth.py
# Create: tests/test_auth.py

# 5. Implement frontend
cd ../frontend
# Claude Code reads: Root + Frontend CLAUDE.md
# Create: src/components/features/auth/LoginForm.tsx
# Create: src/app/login/page.tsx
# Create: src/lib/api/auth.ts

# 6. Test integration
cd ../backend
uvicorn src.main:app

# In another terminal
cd apps/frontend
npm run dev

# 7. Commit feature
cd ../..  # Back to root
git add .
git commit -m "feat: implement user authentication"
```

---

## Best Practices Summary

✅ **DO**:
- Review specs before implementing
- Work in correct directory for context
- Use relative paths for cross-references
- Follow CLAUDE.md patterns
- Test in appropriate directory
- Create specs at repository root

❌ **DON'T**:
- Mix frontend and backend patterns
- Use absolute paths in specs
- Skip specification phase
- Work at root for implementation
- Ignore CLAUDE.md instructions

---

**Maintained by**: Development Team
**Last Updated**: 2026-01-03
**Related**: [CLAUDE.md Hierarchy](./claude-md-hierarchy.md)
