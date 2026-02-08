# Contract: Authoritative Directory Structure

**Feature**: 002-monorepo-organization | **Version**: 1.0 | **Date**: 2026-01-03

## Purpose

This contract defines the authoritative folder and file layout for monorepos supporting Next.js frontend and FastAPI backend with Spec-Kit Plus integration.

## Directory Tree

Root structure with apps/, specs/, and .spec-kit/ directories.

## Required Files

Root: README.md, CLAUDE.md, .gitignore
.spec-kit/: config.yaml
apps/frontend/: CLAUDE.md, package.json, next.config.js
apps/backend/: CLAUDE.md, pyproject.toml
specs/: features/, api/, database/, ui/ subdirectories

## Validation Rules

1. All MANDATORY files must exist
2. Directory names kebab-case
3. Feature names: ###-feature-name pattern
4. CLAUDE.md at root and in each app
5. .env files git-ignored

## Extension Points

New apps: Add under apps/ with CLAUDE.md
New spec domains: Add under specs/
New tools: Configure in .spec-kit/
