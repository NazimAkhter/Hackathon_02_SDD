# Quick Start: Monorepo Organization Setup

**Feature**: 002-monorepo-organization | **Date**: 2026-01-03

## Overview

This guide walks through setting up a monorepo for Next.js and FastAPI with Spec-Kit Plus integration.

## 1. Initialize Repository

Create directory structure:
- apps/frontend/ (Next.js)
- apps/backend/ (FastAPI)
- specs/features/, specs/api/, specs/database/, specs/ui/
- .spec-kit/

## 2. Setup CLAUDE.md Files

Create three files:
- /CLAUDE.md (monorepo guidelines)
- /apps/frontend/CLAUDE.md (Next.js patterns)
- /apps/backend/CLAUDE.md (FastAPI patterns)

## 3. Install Applications

Frontend: Use create-next-app in apps/frontend/
Backend: Create pyproject.toml with FastAPI in apps/backend/

## 4. Configure Environment

Create .env.example files in each app directory
Document all required environment variables

## 5. Verification

Check all directories exist
Verify CLAUDE.md files at three levels
Test apps run independently

## Resources

See data-model.md for full structure specification
See contracts/directory-structure.md for authoritative layout
