# Cross-Reference Guide for Monorepo Specifications

**Version**: 1.0 | **Date**: 2026-01-03
**Feature**: 002-monorepo-organization

## Purpose

This guide defines the authoritative patterns for cross-referencing specifications across the four specification domains: features, API, database, and UI.

## Directory Context

All paths are relative to `specs/` directory:

```
specs/
├── features/
│   └── ###-feature-name/
│       └── spec.md              # Your starting point
├── api/
│   └── endpoints/
│       └── resource.yaml
├── database/
│   └── entities/
│       └── entity.md
└── ui/
    └── components/
        └── component.md
```

---

## Cross-Reference Patterns

### From Feature Spec to Other Domains

**Location**: `specs/features/001-example/spec.md`

**To API Endpoint**:
```markdown
## API Contract
See [Todo Endpoints](../../api/endpoints/todos.yaml)

Or inline reference:
- API: ../../api/endpoints/todos.yaml
```

**To Database Entity**:
```markdown
## Data Model
See [Todo Entity](../../database/entities/todo.md)

Or inline reference:
- Database: ../../database/entities/todo.md
```

**To UI Component**:
```markdown
## User Interface
See [TodoCard Component](../../ui/components/todo-card.md)

Or inline reference:
- UI: ../../ui/components/todo-card.md
```

**Complete Example**:
```markdown
# Feature Specification: Todo Management

## References

- **API Contract**: [Todo Endpoints](../../api/endpoints/todos.yaml)
- **Data Model**: [Todo Entity](../../database/entities/todo.md)
- **UI Components**:
  - [TodoCard](../../ui/components/todo-card.md)
  - [TodoForm](../../ui/components/todo-form.md)
  - [TodoList](../../ui/components/todo-list.md)
```

---

### From API Spec to Other Domains

**Location**: `specs/api/endpoints/todos.yaml`

**To Database Entity** (in YAML comments or separate docs):
```yaml
# API: Todo Endpoints
# Data Model: See ../../database/entities/todo.md

paths:
  /api/v1/todos:
    post:
      summary: Create todo
      # Schema matches Todo entity (../../database/entities/todo.md)
```

**To Feature**:
```yaml
# Used by features:
# - 001-todo-management (../../features/001-todo-management/spec.md)
```

---

### From Database Entity to Other Domains

**Location**: `specs/database/entities/todo.md`

**To Feature**:
```markdown
## Used By

- Feature: [Todo Management](../../features/001-todo-management/spec.md)
- API: [Todo Endpoints](../../api/endpoints/todos.yaml)
```

**To Related Entities**:
```markdown
## Relationships

- Belongs to [User](./user.md)
- Has many [TodoItems](./todo-item.md)
```

---

### From UI Component to Other Domains

**Location**: `specs/ui/components/todo-card.md`

**To Feature**:
```markdown
## Used By

- Feature: [Todo Management](../../features/001-todo-management/spec.md)
```

**To Design Tokens**:
```markdown
## Styling

Uses design tokens:
- Colors: [Color Tokens](../design-tokens/colors.md)
- Typography: [Typography Tokens](../design-tokens/typography.md)
- Spacing: [Spacing Tokens](../design-tokens/spacing.md)
```

**To Related Components**:
```markdown
## Composition

Contains:
- [IconButton](./icon-button.md)
- [Checkbox](./checkbox.md)
```

---

## Path Calculation Reference

### Common Relative Paths

From `features/###-name/spec.md`:
- To API: `../../api/endpoints/[endpoint].yaml`
- To Database: `../../database/entities/[entity].md`
- To UI: `../../ui/components/[component].md`

From `api/endpoints/[endpoint].yaml`:
- To Features: `../../features/###-name/spec.md`
- To Database: `../../database/entities/[entity].md`
- To Schemas: `../schemas/[type]/[schema].yaml`

From `database/entities/[entity].md`:
- To Features: `../../features/###-name/spec.md`
- To API: `../../api/endpoints/[endpoint].yaml`
- To Related Entity: `./[entity].md` (same directory)

From `ui/components/[component].md`:
- To Features: `../../features/###-name/spec.md`
- To Design Tokens: `../design-tokens/[token].md`
- To Related Component: `./[component].md` (same directory)

---

## Markdown Link Syntax

### Basic Link
```markdown
[Link Text](relative/path/to/file.md)
```

### Link with Section
```markdown
[Link Text](relative/path/to/file.md#section-heading)
```

### Inline Reference (without link)
```markdown
See: ../../api/endpoints/todos.yaml
```

### List of References
```markdown
## References

- API: [Todo Endpoints](../../api/endpoints/todos.yaml)
- Database: [Todo Entity](../../database/entities/todo.md)
- UI: [TodoCard](../../ui/components/todo-card.md)
```

---

## YAML Cross-Reference Syntax

### OpenAPI External References
```yaml
# Reference external schema file
components:
  schemas:
    Todo:
      $ref: '../schemas/todo.yaml'
```

### Comment-Based References
```yaml
# This endpoint implements the Todo entity specification
# Database: ../../database/entities/todo.md
# Feature: ../../features/001-todo-management/spec.md

paths:
  /api/v1/todos:
    get:
      summary: List todos
```

---

## Bidirectional Reference Pattern

Maintain bidirectional links for traceability.

### Example: Todo Feature

**In `features/001-todo-management/spec.md`**:
```markdown
## References

- API: [Todo Endpoints](../../api/endpoints/todos.yaml)
- Database: [Todo Entity](../../database/entities/todo.md)
- UI: [TodoCard](../../ui/components/todo-card.md)
```

**In `api/endpoints/todos.yaml`**:
```yaml
# Used by: ../../features/001-todo-management/spec.md
# Implements: ../../database/entities/todo.md
```

**In `database/entities/todo.md`**:
```markdown
## Used By

- Feature: [Todo Management](../../features/001-todo-management/spec.md)
- API: [Todo Endpoints](../../api/endpoints/todos.yaml)
```

**In `ui/components/todo-card.md`**:
```markdown
## Used By

- Feature: [Todo Management](../../features/001-todo-management/spec.md)

## Data Source

- Entity: [Todo](../../database/entities/todo.md)
```

---

## Validation Rules

### Path Validation

✅ **Valid**:
- `../../api/endpoints/todos.yaml` (relative, goes up 2 levels)
- `./user.md` (relative, same directory)
- `../design-tokens/colors.md` (relative, sibling directory)

❌ **Invalid**:
- `/api/endpoints/todos.yaml` (absolute from filesystem root)
- `~/specs/api/endpoints/todos.yaml` (home directory reference)
- `api/endpoints/todos.yaml` (missing `../`)

### Link Format Validation

✅ **Valid**:
```markdown
[Todo Entity](../../database/entities/todo.md)
[API Contract](../../api/endpoints/todos.yaml#paths)
```

❌ **Invalid**:
```markdown
[Todo Entity](database/entities/todo.md)  # Missing ../
[API Contract](/api/endpoints/todos.yaml) # Absolute path
```

---

## Use Cases and Examples

### Use Case 1: Creating New Feature Spec

**Task**: Document a new "User Authentication" feature

**Steps**:
1. Create `specs/features/002-user-authentication/spec.md`
2. Add API reference: `../../api/endpoints/auth.yaml`
3. Add entity reference: `../../database/entities/user.md`
4. Add UI references: `../../ui/components/login-form.md`

**Result**:
```markdown
# Feature Specification: User Authentication

## References

- **API Contract**: [Auth Endpoints](../../api/endpoints/auth.yaml)
- **Data Model**: [User Entity](../../database/entities/user.md)
- **UI Components**:
  - [LoginForm](../../ui/components/login-form.md)
  - [SignupForm](../../ui/components/signup-form.md)
```

---

### Use Case 2: Updating API Contract

**Task**: Modify Todo API endpoint

**Steps**:
1. Update `specs/api/endpoints/todos.yaml`
2. Check which features reference it
3. Update feature specs if contracts change
4. Verify database entity alignment

**Verification**:
```bash
# Search for references to todos.yaml
grep -r "todos.yaml" specs/features/
```

---

### Use Case 3: Designing UI Component

**Task**: Create TodoCard component spec

**Steps**:
1. Create `specs/ui/components/todo-card.md`
2. Reference entity: `../../database/entities/todo.md`
3. Reference design tokens: `../design-tokens/colors.md`
4. Reference features using this component

**Result**:
```markdown
# Component: TodoCard

## Data Model
Props based on [Todo Entity](../../database/entities/todo.md)

## Styling
Uses [Color Tokens](../design-tokens/colors.md)

## Used By
- [Todo Management](../../features/001-todo-management/spec.md)
```

---

## Tools and Automation

### Validating References

**Check broken links**:
```bash
# From repository root
find specs -name "*.md" -exec grep -H "\.\./\.\." {} \;
```

**Verify file existence**:
```bash
# Parse markdown links and check files exist
# (requires custom script or tool)
```

### IDE Support

**VS Code**:
- Install "Markdown All in One" extension
- Ctrl+Click to follow relative links
- Cmd+Shift+V for preview with working links

**JetBrains**:
- Built-in markdown support
- Ctrl+B to navigate to referenced file

---

## Common Pitfalls

### ❌ Wrong: Absolute Paths
```markdown
[Todo Entity](/specs/database/entities/todo.md)
```

### ✅ Correct: Relative Paths
```markdown
[Todo Entity](../../database/entities/todo.md)
```

---

### ❌ Wrong: Missing Directory Levels
```markdown
# From features/001-example/spec.md
[API](api/endpoints/todos.yaml)
```

### ✅ Correct: Proper Traversal
```markdown
[API](../../api/endpoints/todos.yaml)
```

---

### ❌ Wrong: One-Way References Only
```markdown
# Only feature spec references API, but API doesn't reference feature
```

### ✅ Correct: Bidirectional References
```markdown
# Feature spec references API
# API spec documents which features use it
```

---

## Reference Templates

### Feature Spec References Section
```markdown
## References

### Technical Contracts
- **API**: [Resource Endpoints](../../api/endpoints/resource.yaml)
- **Database**: [Entity Definition](../../database/entities/entity.md)

### User Interface
- [Component Name](../../ui/components/component.md)

### Related Features
- [Prerequisite Feature](../000-prerequisite/spec.md)
```

### API Endpoint References (YAML Comment)
```yaml
# API Endpoint: Resource Management
#
# References:
# - Feature: ../../features/001-resource-management/spec.md
# - Entity: ../../database/entities/resource.md
#
# Used By:
# - Frontend: apps/frontend (via OpenAPI client)
# - Backend: apps/backend (FastAPI implementation)
```

### Database Entity References
```markdown
## References

**Used By**:
- Feature: [Feature Name](../../features/001-feature/spec.md)
- API: [Endpoint](../../api/endpoints/resource.yaml)

**Relationships**:
- Parent: [ParentEntity](./parent-entity.md)
- Children: [ChildEntity](./child-entity.md)
```

### UI Component References
```markdown
## References

**Feature Context**:
- [Feature Name](../../features/001-feature/spec.md)

**Data Model**:
- [Entity](../../database/entities/entity.md)

**Design System**:
- [Colors](../design-tokens/colors.md)
- [Typography](../design-tokens/typography.md)
- [Spacing](../design-tokens/spacing.md)

**Composition**:
- [ChildComponent](./child-component.md)
```

---

## Maintenance Checklist

When creating or updating specs:

- [ ] All cross-references use relative paths
- [ ] Paths validated and files exist
- [ ] Bidirectional references maintained
- [ ] Section anchors correct (e.g., `#heading`)
- [ ] No absolute or home directory paths
- [ ] Related features linked
- [ ] API contracts aligned with entities
- [ ] UI components reference design tokens

---

**Maintained by**: Development Team
**Last Updated**: 2026-01-03
**Related**: [Spec Organization Guide](./spec-organization-guide.md)
