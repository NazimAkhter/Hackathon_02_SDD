# Monorepo Validation Checklist

**Purpose**: Verify monorepo structure is correctly initialized

**Date**: Run this after initializing a new monorepo

## Directory Structure

- [ ] Root `.git/` directory exists
- [ ] `.gitignore` file exists
- [ ] `README.md` exists at root
- [ ] Root `CLAUDE.md` exists

## Spec-Kit Configuration

- [ ] `.spec-kit/` directory exists
- [ ] `.spec-kit/config.yaml` exists and is valid YAML
- [ ] `.spec-kit/templates/` directory exists
- [ ] `.spec-kit/scripts/` directory exists

## Applications

- [ ] `apps/` directory exists
- [ ] `apps/frontend/` directory exists
- [ ] `apps/frontend/CLAUDE.md` exists
- [ ] `apps/frontend/README.md` exists
- [ ] `apps/backend/` directory exists
- [ ] `apps/backend/CLAUDE.md` exists
- [ ] `apps/backend/README.md` exists

## Specifications

- [ ] `specs/` directory exists
- [ ] `specs/features/` directory exists
- [ ] `specs/api/` directory exists
- [ ] `specs/api/endpoints/` subdirectory exists
- [ ] `specs/api/schemas/` subdirectory exists
- [ ] `specs/database/` directory exists
- [ ] `specs/database/entities/` subdirectory exists
- [ ] `specs/database/migrations/` subdirectory exists
- [ ] `specs/ui/` directory exists
- [ ] `specs/ui/components/` subdirectory exists
- [ ] `specs/ui/design-tokens/` subdirectory exists

## Content Validation

- [ ] Root CLAUDE.md contains monorepo-wide guidelines
- [ ] Frontend CLAUDE.md contains Next.js-specific rules
- [ ] Backend CLAUDE.md contains FastAPI-specific rules
- [ ] .gitignore excludes `.env` files
- [ ] .gitignore excludes `node_modules/`
- [ ] .gitignore excludes `__pycache__/`

## Optional Checks

- [ ] Frontend app initialized (package.json exists)
- [ ] Backend app initialized (pyproject.toml or requirements.txt exists)
- [ ] At least one feature spec exists in specs/features/

## Validation Result

**Status**: [ ] PASS / [ ] FAIL

**Notes**:

**Date Verified**:

**Verified By**:
