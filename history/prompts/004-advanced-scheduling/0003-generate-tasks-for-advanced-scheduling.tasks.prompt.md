---
id: 0003
title: Generate Tasks For Advanced Scheduling
stage: tasks
date: 2026-02-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: 004-advanced-scheduling
branch: 004-advanced-scheduling
user: nazimakhter
command: /sp.tasks
labels: ["tasks", "task-breakdown", "implementation", "due-dates", "recurring-tasks", "scheduling"]
links:
  spec: specs/004-advanced-scheduling/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-advanced-scheduling/tasks.md
tests:
  - (none - task planning phase)
---

## Prompt

```text
(empty input - triggering task generation from planning artifacts)
```

## Response snapshot

Generated comprehensive tasks.md with **78 tasks** across **8 phases** for implementing advanced scheduling features (due dates and recurring tasks).

**Task Organization**:

1. **Phase 1: Setup (T001-T010)** - Extend Todo model
   - Add Recurrence enum (NONE, DAILY, WEEKLY, MONTHLY)
   - Extend Todo dataclass with due_date, recurrence, is_recurring_parent
   - Add is_overdue() and is_due_soon() methods
   - Update __str__() for due date and recurrence display

2. **Phase 2: Foundational (T011-T018)** - Enhance TodoService
   - Add due date parsing helper (_parse_due_date)
   - Add next due date calculation (_calculate_next_due_date)
   - Enhance add_todo and update_todo with new parameters
   - Add get_overdue_todos and get_upcoming_todos methods

3. **Phase 3: US1 Due Dates (T019-T026)** - 8 tasks
   - Add due date prompts to CLI add/update flows
   - Implement date input validation and error handling
   - Update view display to show due date column
   - Add manual tests for due date assignment

4. **Phase 4: US2 Upcoming/Overdue (T027-T039)** - 13 tasks
   - Add visual indicators (⚠ OVERDUE, 📅 DUE SOON)
   - Create dedicated upcoming and overdue view flows
   - Update __main__.py menu with options 6 and 7
   - Add tests for overdue detection and visual display

5. **Phase 5: US3 Recurring (T040-T049)** - 10 tasks
   - Add recurrence prompt to add_todo_flow
   - Implement auto-rescheduling in mark_complete
   - Add is_recurring_parent flag logic
   - Test daily/weekly/monthly recurrence patterns

6. **Phase 6: US4 Modify Recurring (T050-T056)** - 7 tasks
   - Add recurrence prompt to update_todo_flow
   - Support disabling recurrence (set to NONE)
   - Handle recurrence updates with tests

7. **Phase 7: US5 Filter/Sort (T057-T062)** - 6 tasks
   - Extend sort_todos with due_date options
   - Extend filter menus to include due date filters
   - Test combined filter+sort with due dates

8. **Phase 8: Polish (T063-T078)** - 16 tasks
   - Update integration tests
   - Add edge case tests (non-existent dates, duplicate rescheduling)
   - Update README documentation
   - Verify backward compatibility

**Implementation Strategy**:

- **MVP Scope**: 39 tasks (Setup + Foundational + US1 + US2)
  - Core due date functionality with upcoming/overdue views
  - Visual indicators for task urgency

- **Full Scope**: 78 tasks (all phases)
  - Includes recurring tasks, modify recurrence, filter/sort extensions

**Dependencies**:
- Setup → Foundational → US1, US2, US3 (parallel after Foundational)
- US3 → US4 (modify recurring depends on recurring implementation)
- US1 → US5 (filter/sort depends on due dates)
- All user stories → Polish

**Task Format**:
- Checklist format with unique IDs (T001-T078)
- Story labels ([US1], [US2], etc.) for traceability
- Parallel markers ([P]) for independent tasks
- File paths and acceptance criteria for each task
- Edge cases and test scenarios documented

**Key Technical Details**:
- Recurrence triggered on completion (not time-based)
- Overdue calculated at view time (not cached)
- Monthly edge case: last day of month fallback
- Duplicate prevention via is_recurring_parent flag
- Backward compatible (all new fields have defaults)

## Outcome

- ✅ Impact: Complete actionable task breakdown ready for implementation via /sp.implement command
- 🧪 Tests: Task planning phase - test tasks distributed across all phases (T026, T039, T049, T056, T062, T063-T078)
- 📁 Files: 1 file created (tasks.md with 78 tasks)
- 🔁 Next prompts: `/sp.implement` to execute MVP (39 tasks) or full scope (78 tasks)
- 🧠 Reflection: Tasks derived from spec.md, plan.md, and data-model.md. MVP scope focuses on due dates + upcoming/overdue views (highest value). Recurring tasks in separate phase for optional implementation. All tasks have clear acceptance criteria and file paths.

## Evaluation notes (flywheel)

- Failure modes observed: Prerequisites script failed (handled by direct artifact reads)
- Graders run and results (PASS/FAIL):
  - PASS: All tasks have unique IDs (T001-T078)
  - PASS: All tasks reference specific files
  - PASS: Dependencies clearly documented
  - PASS: MVP scope defined (39 tasks)
  - PASS: Story labels present ([US1]-[US5])
  - PASS: Edge cases covered (T072-T077)
  - PASS: Backward compatibility verified (T078)
- Prompt variant (if applicable): Standard /sp.tasks execution with empty input (artifact-driven)
- Next experiment (smallest change to try): None needed - task generation complete, ready for implementation phase
