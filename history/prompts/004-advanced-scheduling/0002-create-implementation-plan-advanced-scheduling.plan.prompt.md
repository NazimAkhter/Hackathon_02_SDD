---
id: 0002
title: Create Implementation Plan Advanced Scheduling
stage: plan
date: 2026-02-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: 004-advanced-scheduling
branch: 004-advanced-scheduling
user: nazimakhter
command: /sp.plan
labels: ["planning", "research", "data-model", "quickstart", "due-dates", "recurring-tasks"]
links:
  spec: specs/004-advanced-scheduling/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-advanced-scheduling/plan.md
  - specs/004-advanced-scheduling/research.md
  - specs/004-advanced-scheduling/data-model.md
  - specs/004-advanced-scheduling/quickstart.md
tests:
  - (none - planning phase)
---

## Prompt

```text
Advanced Features for In-Memory Python Console Todo App

Create:
- updated architecture sketch including due dates and recurring task logic
- data model extensions for due date, time, and recurrence rules
- command/menu updates for scheduling features
- workflow for integrating advanced features into existing app
- validation and testing approach

Decisions needing documentation:
- due date representation (datetime object vs string)
- recurrence model (enum vs rule-based)
- when recurrence is triggered (on completion vs time-based)
- reminder display logic (startup check vs periodic check)
- handling overdue and missed recurring tasks

Testing strategy:
- unit tests for due date assignment and updates
- recurrence rescheduling tests (daily, weekly, monthly)
- overdue task detection tests
- edge cases: no due date, invalid date input, past dates
- combined scenarios with priority, tags, and filters

Constraints:
- in-memory storage only
- console-based interaction
- must extend existing basic and intermediate features
- Python 3.13+ with UV

Output:
Clear implementation plan ready to break into tasks and execute via Claude Code
```

## Response snapshot

Created comprehensive implementation plan with **Phase 0 (Research)**, **Phase 1 (Design)**, and **Phase 2 (Task Planning)** artifacts.

**Planning Artifacts Generated**:

1. **plan.md**: High-level implementation plan
   - Summary: Extend Todo with due dates and recurring tasks
   - Technical context: Python 3.13+, datetime/enum, in-memory, pytest
   - Constitution check: ✅ All 7 principles passed
   - Project structure: Extends existing todo-app/ single project
   - Phases: 0 (Research), 1 (Design), 2 (Tasks - to be generated)

2. **research.md**: Resolved 9 technical unknowns
   - **Decision 1**: datetime object (not string) for type safety and comparisons
   - **Decision 2**: Recurrence enum (NONE, DAILY, WEEKLY, MONTHLY) for simplicity
   - **Decision 3**: Trigger recurrence on completion (not time-based) for user control
   - **Decision 4**: Calculate overdue at view time (not cached) for accuracy
   - **Decision 5**: strptime with "%Y-%m-%d %H:%M" format (no external parsing)
   - **Decision 6**: Last day of month fallback for non-existent dates (Jan 31 → Feb 28)
   - **Decision 7**: Extend existing filter/sort additively (backward compatible)
   - **Decision 8**: Absolute dates + visual indicators (⚠ OVERDUE, 📅 DUE SOON)
   - **Decision 9**: is_recurring_parent boolean flag to prevent duplicate rescheduling

3. **data-model.md**: Enhanced Todo entity specification
   - New Recurrence enum: NONE, DAILY, WEEKLY, MONTHLY
   - Enhanced Todo attributes:
     - `due_date: Optional[datetime] = None`
     - `recurrence: Recurrence = Recurrence.NONE`
     - `is_recurring_parent: bool = True`
   - New methods: `is_overdue()`, `is_due_soon()`
   - Updated `__str__()` with due date column and status indicators
   - Service methods: `_calculate_next_due_date()`, `get_overdue_todos()`, `get_upcoming_todos()`
   - Backward compatible: All new fields have defaults

4. **quickstart.md**: Usage examples and workflows
   - Basic usage: Adding todos with due dates
   - Creating recurring todos (daily/weekly/monthly)
   - Marking recurring todos complete (auto-reschedule demo)
   - Viewing upcoming/overdue todos
   - Updating due dates and disabling recurrence
   - Recurrence examples with edge cases (non-existent dates)
   - Filtering and sorting with due dates
   - Error handling examples
   - Common workflows (morning review, weekly planning, end-of-day)
   - Tips and limitations

**Key Design Decisions**:

- **Due Dates**: Optional datetime field, YYYY-MM-DD HH:MM format
- **Recurrence**: Simple 3-type enum (no complex patterns like iCalendar RRULE)
- **Trigger**: On completion (user marks complete) not time-based (no background jobs)
- **Overdue Detection**: Dynamic calculation at view time (always accurate)
- **Display**: Absolute dates + emoji indicators (⚠ for overdue, 📅 for due soon)
- **Monthly Edge Cases**: Use last day of month when target day doesn't exist
- **Duplicate Prevention**: is_recurring_parent flag prevents double-rescheduling
- **Integration**: Additive extensions to existing filter/sort (backward compatible)

**Constitution Compliance**: ✅ All principles passed

- **I. Incremental Phase-By-Phase**: Extends Phase I.5, no future phase dependencies
- **II. Simplicity First**: Standard library only (datetime, enum), no external libraries
- **III. Separation of Concerns**: Scheduling logic in models/service, CLI handles UI only
- **IV. Domain Model Reusability**: Additive changes (new fields have defaults), backward compatible
- **V. Spec-Driven Development**: Spec → plan → tasks workflow followed
- **VI. Automated Testing**: Unit and integration tests planned
- **VII. Feature Branch Workflow**: 004-advanced-scheduling branch created

**Technical Approach**:

- **Data Model**: Extend Todo dataclass with 3 new optional fields
- **Recurrence Logic**: Calculate next due date based on enum type + current due date
- **Overdue Detection**: `due_date < datetime.now() and not completed`
- **Due Soon Detection**: `0 <= (due_date - now).days <= 7 and not completed`
- **Auto-Rescheduling**: On `mark_complete()`, check recurrence and create new instance
- **Date Parsing**: `datetime.strptime(input, "%Y-%m-%d %H:%M")` with try/except for validation
- **Display Format**: `due_date.strftime("%Y-%m-%d %H:%M")` with emoji prefix for status

**File Changes Expected**:

- `todo-app/src/todo_app/models.py`: Add Recurrence enum, extend Todo dataclass, add is_overdue/is_due_soon methods
- `todo-app/src/todo_app/service.py`: Enhance add_todo/update_todo, add _calculate_next_due_date, get_overdue_todos, get_upcoming_todos, extend mark_complete with recurrence logic
- `todo-app/src/todo_app/cli.py`: Add due date prompts, recurrence prompts, upcoming/overdue views, extend filter/sort menus
- `todo-app/src/todo_app/__main__.py`: Update menu routing (add options 6, 7 for upcoming/overdue views)
- `todo-app/tests/unit/test_models.py`: Add due date and recurrence tests
- `todo-app/tests/unit/test_service.py`: Add scheduling logic tests
- `todo-app/tests/integration/test_cli.py`: Add scheduling flow tests

## Outcome

- ✅ Impact: Complete implementation plan with resolved technical unknowns, detailed data model, and usage examples ready for task breakdown
- 🧪 Tests: Planning phase - test strategy documented, unit/integration tests to be implemented
- 📁 Files: 4 files created (plan.md, research.md, data-model.md, quickstart.md)
- 🔁 Next prompts: `/sp.tasks` to generate executable task breakdown
- 🧠 Reflection: All 9 technical unknowns resolved through research (datetime vs string, enum vs rules, completion vs time-based, etc.). Data model extends Phase I.5 with backward-compatible additions. Quickstart provides comprehensive usage examples for validation.

## Evaluation notes (flywheel)

- Failure modes observed: Setup script line ending issues (handled by manual path resolution)
- Graders run and results (PASS/FAIL):
  - PASS: All constitution gates passed (7/7)
  - PASS: All technical unknowns resolved (9/9)
  - PASS: Data model backward compatible (new fields have defaults)
  - PASS: No external dependencies required (datetime, enum from stdlib)
  - PASS: Edge cases documented (non-existent dates, duplicate rescheduling, overdue detection)
- Prompt variant (if applicable): Standard /sp.plan execution with detailed user requirements
- Next experiment (smallest change to try): None needed - planning complete, ready for task generation
