# Implementation Plan: Advanced Scheduling Features for In-Memory Python Console Todo App

**Branch**: `004-advanced-scheduling` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-advanced-scheduling/spec.md`

## Summary

Extend the Phase I.5 console todo app with due dates and recurring task capabilities. Primary requirements: (1) Optional due date/time assignment to todos with YYYY-MM-DD HH:MM format, (2) Visual indicators for overdue and upcoming tasks, (3) Recurring tasks (daily/weekly/monthly) that auto-reschedule on completion, (4) Dedicated views for upcoming and overdue todos, (5) Integration with existing priority/tags/search/filter/sort features.

Technical approach: Extend Todo dataclass with `due_date` (datetime | None) and `recurrence` (Recurrence enum) fields. Add service methods for overdue detection, upcoming filtering, and recurrence rescheduling logic. Update CLI flows to prompt for due dates and recurrence during add/update operations. Extend view formatting to show due date status indicators.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (datetime, enum); UV for package management
**Storage**: In-memory (dict-based) - no persistence
**Testing**: pytest (existing test infrastructure from Phase I.5)
**Target Platform**: Cross-platform console (Linux, macOS, Windows via WSL)
**Project Type**: Single project (console application)
**Performance Goals**: Instant response (<100ms) for all operations on lists up to 1000 todos
**Constraints**: In-memory only (data lost on exit), console-only interface, Python 3.13+ required, no external date parsing libraries
**Scale/Scope**: Single-user, session-scoped, up to 1000 todos per session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Principle I: Incremental Phase-By-Phase Development**
- ✅ PASS: This feature extends Phase I.5 (console app with intermediate features)
- ✅ PASS: No dependencies on future phases (II-V)
- ✅ PASS: Maintains console-only scope

**Principle II: Simplicity First**
- ✅ PASS: Uses Python standard library datetime (no external libraries)
- ✅ PASS: In-memory storage only (no database complexity)
- ✅ PASS: Simple recurrence model (3 types only: daily/weekly/monthly)

**Principle III: Strong Separation of Concerns**
- ✅ PASS: Scheduling logic contained in models and service layers
- ✅ PASS: CLI layer handles user interaction only
- ✅ PASS: Domain model remains independent of infrastructure

**Principle IV: Domain Model Reusability**
- ✅ PASS: Extends existing Todo model without breaking changes
- ✅ PASS: New fields (due_date, recurrence) have defaults (backward compatible)
- ✅ PASS: Model changes are additive, not breaking

**Principle V: Spec-Driven Development**
- ✅ PASS: Specification complete (spec.md)
- ✅ PASS: Following plan → tasks → implement workflow
- ✅ PASS: Acceptance criteria defined for all user stories

**Principle VI: Automated Testing at Each Phase**
- ✅ PASS: Unit tests planned for due date logic
- ✅ PASS: Unit tests planned for recurrence rescheduling
- ✅ PASS: Integration tests planned for CLI flows

**Principle VII: Version Control and Feature Branch Workflow**
- ✅ PASS: Feature branch 004-advanced-scheduling created
- ✅ PASS: Follows ###-feature-name pattern
- ✅ PASS: Will merge into 001-console-todo (main branch)

**Overall Constitution Check: ✅ PASS** - No violations, all gates passed

## Project Structure

### Documentation (this feature)

```text
specs/004-advanced-scheduling/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── checklists/          # Quality validation checklists
│   └── requirements.md
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
todo-app/
├── src/
│   └── todo_app/
│       ├── __init__.py
│       ├── __main__.py
│       ├── models.py        # Enhanced: Todo + Recurrence enum
│       ├── service.py       # Enhanced: scheduling methods
│       └── cli.py           # Enhanced: due date/recurrence prompts
└── tests/
    ├── unit/
    │   ├── test_models.py    # Enhanced: due date & recurrence tests
    │   └── test_service.py   # Enhanced: scheduling logic tests
    └── integration/
        ├── test_cli.py       # Enhanced: scheduling flow tests
        └── test_main.py      # Enhanced: menu tests
```

**Structure Decision**: Extends existing single project structure (todo-app/). All enhancements are additive to existing models.py, service.py, and cli.py files. No new modules required; scheduling logic integrated into existing architecture.

## Complexity Tracking

No constitution violations - this section intentionally left empty.

---

## Phase 0: Outline & Research

**Purpose**: Resolve all technical unknowns before designing the data model and implementation approach.

All research will be documented in `research.md`. Key decisions to research and document:

1. **Due Date Representation**: datetime object vs string storage
2. **Recurrence Model Design**: Enum vs rule-based approach
3. **Recurrence Trigger Point**: On completion vs time-based
4. **Overdue Detection Strategy**: View-time calculation vs cached state
5. **Date Input Validation**: strptime vs dateutil vs manual parsing
6. **Monthly Recurrence Edge Cases**: Handling non-existent dates (e.g., Jan 31 → Feb)
7. **Integration with Existing Features**: How due dates interact with existing filter/sort
8. **Display Format**: Human-readable date formatting (relative vs absolute)

Research tasks dispatched to resolve these decisions.

---

## Phase 1: Design & Contracts

**Purpose**: Design the data model, service contracts, and integration points based on research findings.

Artifacts to generate:
1. **data-model.md**: Enhanced Todo entity with due_date and recurrence fields, Recurrence enum definition, validation rules, state transitions
2. **quickstart.md**: Usage examples for adding due dates, creating recurring todos, viewing overdue/upcoming tasks
3. No API contracts needed (console-only application)

---

## Phase 2: Implementation Tasks

**Purpose**: Break down implementation into testable, executable tasks (generated by `/sp.tasks` command).

Expected task phases:
1. Setup: Extend data model with due_date and Recurrence enum
2. Foundational: Enhance service methods (add_todo, update_todo with due date parameters)
3. US1 (Due Dates): Due date prompts, validation, display
4. US2 (Upcoming/Overdue): Overdue detection, filtered views, visual indicators
5. US3 (Recurring): Recurrence creation, auto-rescheduling logic
6. US4 (Modify Recurring): Disable/modify recurrence
7. US5 (Filter/Sort): Extend existing filter/sort for due dates
8. Polish: Testing, documentation, integration validation

---

**Next Steps**:
1. Execute Phase 0 research (create research.md)
2. Execute Phase 1 design (create data-model.md, quickstart.md)
3. Re-validate Constitution Check post-design
4. Report completion and readiness for `/sp.tasks`
