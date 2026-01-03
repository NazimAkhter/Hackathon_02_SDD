# Monorepo Structure Documentation

**Purpose**: Authoritative reference for monorepo folder organization

**Last Updated**: 2026-01-03

## Target Structure

```
{monorepo-name}/
├── .git/
├── .gitignore
├── README.md
├── CLAUDE.md
│
├── .spec-kit/
│   ├── config.yaml
│   ├── templates/
│   └── scripts/
│
├── apps/
│   ├── frontend/
│   │   ├── CLAUDE.md
│   │   ├── src/
│   │   ├── public/
│   │   ├── tests/
│   │   ├── package.json
│   │   ├── next.config.js
│   │   ├── tsconfig.json
│   │   ├── .env.example
│   │   └── README.md
│   │
│   └── backend/
│       ├── CLAUDE.md
│       ├── src/
│       ├── tests/
│       ├── pyproject.toml
│       ├── .env.example
│       └── README.md
│
└── specs/
    ├── features/
    │   └── {###-feature-name}/
    │       ├── spec.md
    │       ├── plan.md
    │       └── tasks.md
    │
    ├── api/
    │   ├── endpoints/
    │   ├── schemas/
    │   └── versioning.md
    │
    ├── database/
    │   ├── entities/
    │   ├── migrations/
    │   └── schema.md
    │
    └── ui/
        ├── components/
        ├── design-tokens/
        └── interactions.md
```

## Directory Purposes

**Root Level**:
- `.spec-kit/`: Spec-Kit Plus configuration and templates
- `apps/`: Deployable applications (frontend, backend, etc.)
- `specs/`: Centralized specifications

**Apps Structure**:
- Each app has own CLAUDE.md for context-specific rules
- Independent dependency management
- Separate build/run configurations

**Specs Structure**:
- `features/`: Feature specs organized by number
- `api/`: API contracts and endpoint definitions
- `database/`: Data model specifications
- `ui/`: Component and design specifications

## Key Principles

1. **Centralized Specifications**: Single source of truth in specs/
2. **Application Independence**: Each app maintains own dependencies
3. **Three-Tier CLAUDE.md**: Root, frontend, backend contexts
4. **Domain-Based Organization**: Specs organized by functional domain

## References

- See data-model.md for entity definitions
- See research.md for architectural decisions
- See contracts/directory-structure.md for validation rules
