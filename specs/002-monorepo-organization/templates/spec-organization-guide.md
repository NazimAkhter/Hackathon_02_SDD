# Specification Organization Guide

**Version**: 1.0 | **Date**: 2026-01-03
**Feature**: 002-monorepo-organization

## Purpose

This guide explains how to organize specifications across four domains in the monorepo: features, API, database, and UI.

## Directory Structure

```
specs/
├── features/           # Business capability specifications
├── api/               # API contract specifications
├── database/          # Data model specifications
└── ui/                # UI/UX specifications
```

## Domain Organization

### 1. Features Directory (`specs/features/`)

**Purpose**: Feature-specific specifications following Spec-Driven Development workflow

**Structure**:
```
features/
└── ###-feature-name/
    ├── spec.md           # User scenarios, requirements, success criteria
    ├── plan.md           # Technical design and architecture
    ├── tasks.md          # Implementation tasks
    ├── checklists/       # Quality validation checklists
    └── contracts/        # Feature-specific contracts
```

**Naming Convention**:
- Three-digit prefix: `001-`, `002-`, `003-`
- Kebab-case feature name: `user-authentication`, `todo-management`
- Full example: `001-user-authentication/`

**When to Use**:
- New business capabilities or user-facing features
- Multi-component functionality spanning frontend and backend
- Features following spec → plan → tasks workflow

**Example**:
```
features/001-todo-management/
├── spec.md          # Todo CRUD requirements
├── plan.md          # FastAPI + PostgreSQL design
└── tasks.md         # 15 implementation tasks
```

---

### 2. API Directory (`specs/api/`)

**Purpose**: API contract specifications shared between frontend and backend

**Structure**:
```
api/
├── endpoints/          # OpenAPI/Swagger specifications
│   ├── auth.yaml
│   ├── todos.yaml
│   └── users.yaml
├── schemas/           # Shared data models
│   ├── request/
│   └── response/
└── versioning.md      # API versioning strategy
```

**Content Guidelines**:
- Use OpenAPI 3.0+ format for all endpoints
- Document request/response schemas
- Include error codes and handling
- Specify authentication requirements
- Define rate limits and pagination

**When to Use**:
- Documenting RESTful or GraphQL endpoints
- Defining request/response contracts
- Establishing API versioning strategy
- Documenting authentication flows

**Cross-References**:
- Feature specs reference API endpoints: `See ../../api/endpoints/todos.yaml`
- Backend implements contracts defined here
- Frontend consumes according to these specs

**Example**:
```yaml
# api/endpoints/todos.yaml
paths:
  /api/v1/todos:
    post:
      summary: Create new todo
      requestBody:
        $ref: '../schemas/request/todo-create.yaml'
      responses:
        '201':
          $ref: '../schemas/response/todo.yaml'
```

---

### 3. Database Directory (`specs/database/`)

**Purpose**: Data model specifications independent of database technology

**Structure**:
```
database/
├── entities/          # Entity definitions
│   ├── user.md
│   ├── todo.md
│   └── category.md
├── migrations/        # Migration plans (not SQL)
│   └── 001-initial-schema.md
└── schema.md          # Overall schema documentation
```

**Entity Template**:
```markdown
# Entity: Todo

## Attributes
- id: uuid (primary key)
- title: string (required, max 255)
- completed: boolean (default false)
- user_id: uuid (foreign key)
- created_at: timestamp
- updated_at: timestamp

## Relationships
- Belongs to User
- Has many TodoItems

## Validation
- title: Required, non-empty
- user_id: Must reference existing user

## Indexes
- user_id (for user's todos query)
- created_at (for chronological sorting)
```

**When to Use**:
- Defining domain entities and relationships
- Planning database migrations
- Documenting validation rules
- Specifying indexes and constraints

**Technology-Agnostic**:
- Don't specify PostgreSQL vs MongoDB
- Focus on entities, attributes, relationships
- Implementation chooses database technology

**Cross-References**:
- Feature specs reference entities: `See ../../database/entities/todo.md`
- Backend models implement these specifications
- API schemas align with entity attributes

---

### 4. UI Directory (`specs/ui/`)

**Purpose**: UI/UX specifications independent of framework

**Structure**:
```
ui/
├── components/        # Component specifications
│   ├── buttons/
│   ├── forms/
│   └── layouts/
├── design-tokens/     # Design system
│   ├── colors.md
│   ├── typography.md
│   └── spacing.md
└── interactions.md    # User interaction patterns
```

**Component Template**:
```markdown
# Component: TodoCard

**Type**: Presentational

## Purpose
Display a single todo item with actions.

## Props
- todo: Todo (required)
- onToggle: (id: string) => void
- onDelete: (id: string) => void

## Behavior
- Clicking checkbox toggles completion
- Strikethrough when completed
- Delete button shows on hover
- Confirmation modal before delete

## Styling
- Background: white (light), gray-800 (dark)
- Border: 1px solid gray-200
- Border-radius: 8px
- Padding: 16px

## Accessibility
- Keyboard navigation (Tab, Enter, Space)
- ARIA labels for actions
- Screen reader announcements
```

**When to Use**:
- Documenting reusable components
- Defining design system tokens
- Specifying user interaction patterns
- Establishing accessibility requirements

**Framework-Agnostic**:
- Don't specify React vs Vue implementation
- Focus on behavior, props, styling
- Implementation chooses UI framework

**Cross-References**:
- Feature specs reference components: `See ../../ui/components/todo-card.md`
- Frontend implements according to specs
- Design tokens used across all components

---

## Workflow Integration

### Spec-Driven Development Flow

1. **Specification Phase**: Create feature spec in `features/###-feature-name/spec.md`
2. **Planning Phase**:
   - Design architecture in `plan.md`
   - Reference API contracts in `api/endpoints/`
   - Reference entities in `database/entities/`
   - Reference components in `ui/components/`
3. **Task Breakdown**: Generate `tasks.md` with cross-references
4. **Implementation**: Build according to specs across domains

### Creating New Specifications

**New Feature**:
```bash
specs/features/004-notifications/
├── spec.md
├── plan.md
└── tasks.md
```

**New API Endpoint**:
```bash
specs/api/endpoints/notifications.yaml
```

**New Entity**:
```bash
specs/database/entities/notification.md
```

**New Component**:
```bash
specs/ui/components/notification-toast.md
```

---

## Cross-Referencing Strategy

### Relative Paths

From feature spec to other domains:
- API: `../../api/endpoints/example.yaml`
- Database: `../../database/entities/example.md`
- UI: `../../ui/components/example.md`

From API spec to database:
- `../../database/entities/todo.md`

From UI component to design tokens:
- `../design-tokens/colors.md`

### Markdown Links

```markdown
## References

- **API Contract**: [Todo Endpoints](../../api/endpoints/todos.yaml)
- **Data Model**: [Todo Entity](../../database/entities/todo.md)
- **UI Component**: [TodoCard](../../ui/components/todo-card.md)
```

### Bidirectional References

**In Feature Spec**:
```markdown
This feature uses the TodoCard component (see ../../ui/components/todo-card.md)
```

**In Component Spec**:
```markdown
Used by features: 001-todo-management
```

---

## Validation Checklist

Before marking spec complete:

- [ ] Feature spec exists in `features/###-name/`
- [ ] API endpoints documented in `api/endpoints/`
- [ ] Entities defined in `database/entities/`
- [ ] UI components specified in `ui/components/`
- [ ] Cross-references are valid relative paths
- [ ] All domains reference correct version
- [ ] No technology-specific implementation details in specs

---

## Best Practices

### DO:
✅ Use relative paths for cross-references
✅ Keep specs technology-agnostic
✅ Document validation rules and constraints
✅ Include accessibility requirements in UI specs
✅ Version API endpoints explicitly
✅ Number features sequentially

### DON'T:
❌ Mix implementation code with specifications
❌ Use absolute paths for cross-references
❌ Duplicate specifications across domains
❌ Skip validation rules in entity specs
❌ Omit error handling in API specs
❌ Use framework-specific terms in UI specs

---

## Examples

See `specs/002-monorepo-organization/examples/` for complete examples:

- Feature: `examples/001-example-feature/spec.md`
- API: `examples/api/endpoints/example.yaml`
- Database: `examples/database/entities/example-entity.md`
- UI: `examples/ui/components/example-component.md`

---

**Maintained by**: Development Team
**Last Updated**: 2026-01-03
**Related**: [Cross-Reference Guide](./cross-reference-guide.md)
