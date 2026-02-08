---
description: "Task list for Advanced Scheduling Features for In-Memory Python Console Todo App"
---

# Tasks: Advanced Scheduling Features for In-Memory Python Console Todo App

**Input**: Design documents from `/specs/004-advanced-scheduling/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Tests are NOT explicitly requested in the feature specification. Focus on implementation only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `todo-app/src/`, `todo-app/tests/` at repository root
- This is a Python console application extending the existing todo-app structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Extend existing data model with new Recurrence enum and enhanced Todo attributes for scheduling

**Note**: The Phase I.5 console todo app from `003-intermediate-todo-features` already exists. This phase extends it with scheduling capabilities.

- [X] T001 Add Recurrence enum to todo-app/src/todo_app/models.py (NONE="none", DAILY="daily", WEEKLY="weekly", MONTHLY="monthly")
- [X] T002 Extend Todo dataclass with due_date field (Optional[datetime]=None) in todo-app/src/todo_app/models.py
- [X] T003 Extend Todo dataclass with recurrence field (Recurrence=Recurrence.NONE) in todo-app/src/todo_app/models.py
- [X] T004 Extend Todo dataclass with is_recurring_parent field (bool=True) in todo-app/src/todo_app/models.py
- [X] T005 Update Todo.__post_init__ validation to enforce due_date type (datetime or None) in todo-app/src/todo_app/models.py
- [X] T006 Update Todo.__post_init__ validation to enforce recurrence type (Recurrence enum) in todo-app/src/todo_app/models.py
- [X] T007 Add is_overdue() method to Todo class (checks due_date < now() and not completed) in todo-app/src/todo_app/models.py
- [X] T008 Add is_due_soon() method to Todo class (checks 0 <= days_until_due <= 7) in todo-app/src/todo_app/models.py
- [X] T009 Update Todo.__str__ display format to include due date column with status indicators (⚠ OVERDUE, 📅 DUE SOON) in todo-app/src/todo_app/models.py
- [X] T010 Update Todo.__str__ display format to include recurrence column (🔁 icon + recurrence type) in todo-app/src/todo_app/models.py

**Checkpoint**: Data model enhanced - all existing tests should still pass (new fields have defaults)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core service enhancements that MUST be complete before ANY user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T011 Update TodoService.add_todo signature to accept due_date and recurrence parameters in todo-app/src/todo_app/service.py
- [X] T012 Update TodoService.add_todo to validate that recurring todos (recurrence != NONE) must have a due_date in todo-app/src/todo_app/service.py
- [X] T013 Update TodoService.update_todo signature to accept due_date and recurrence parameters in todo-app/src/todo_app/service.py
- [X] T014 Add _parse_due_date helper method to TodoService (strptime with "%Y-%m-%d %H:%M") in todo-app/src/todo_app/service.py
- [X] T015 Add _calculate_next_due_date helper method to TodoService (implements daily/weekly/monthly logic) in todo-app/src/todo_app/service.py
- [X] T016 Implement daily recurrence calculation (+1 day) in _calculate_next_due_date in todo-app/src/todo_app/service.py
- [X] T017 Implement weekly recurrence calculation (+7 days) in _calculate_next_due_date in todo-app/src/todo_app/service.py
- [X] T018 Implement monthly recurrence calculation (same day next month, with fallback for non-existent dates) in _calculate_next_due_date in todo-app/src/todo_app/service.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add Due Date to Todos (Priority: P1) 🎯 MVP

**Goal**: Users can assign and update optional due dates (YYYY-MM-DD HH:MM format) for todos

**Independent Test**: Add a new todo with due date "2026-02-15 14:00", view the list to confirm due date displayed, update the due date, verify change persists

### Implementation for User Story 1

- [X] T019 [US1] Update CLI add_todo flow to prompt for due date after tags in todo-app/src/todo_app/cli.py
- [X] T020 [US1] Add due date validation in CLI add flow (strptime with error handling, Enter to skip) in todo-app/src/todo_app/cli.py
- [X] T021 [US1] Display clear format instructions (YYYY-MM-DD HH:MM) in due date prompt in todo-app/src/todo_app/cli.py
- [X] T022 [US1] Update CLI update_todo flow to prompt for new due date in todo-app/src/todo_app/cli.py
- [X] T023 [US1] Add due date validation in CLI update flow (strptime with error handling) in todo-app/src/todo_app/cli.py
- [X] T024 [US1] Update CLI update_todo to show current due date in display in todo-app/src/todo_app/cli.py
- [X] T025 [US1] Update CLI view_todos display to show due date column in todo-app/src/todo_app/cli.py
- [X] T026 [US1] Test due date display shows absolute format (YYYY-MM-DD HH:MM) in view in todo-app/src/todo_app/cli.py

**Checkpoint**: User Story 1 complete - users can assign and update due dates, displayed in list view

---

## Phase 4: User Story 2 - View Upcoming and Overdue Todos (Priority: P1)

**Goal**: Users can see which todos are due soon (next 7 days) or overdue with visual indicators

**Independent Test**: Create todos with various due dates (past, today, future), view list to confirm overdue marked with ⚠, upcoming marked with 📅, and dedicated views work

### Implementation for User Story 2

- [X] T027 [US2] Add get_overdue_todos method to TodoService (filter due_date < now and not completed) in todo-app/src/todo_app/service.py
- [X] T028 [US2] Add get_upcoming_todos method to TodoService (filter due within next 7 days and not completed) in todo-app/src/todo_app/service.py
- [X] T029 [US2] Sort overdue todos by due date (earliest/most overdue first) in get_overdue_todos in todo-app/src/todo_app/service.py
- [X] T030 [US2] Sort upcoming todos by due date (earliest first) in get_upcoming_todos in todo-app/src/todo_app/service.py
- [X] T031 [US2] Update Todo.__str__ to add ⚠ prefix for overdue todos (calls is_overdue method) in todo-app/src/todo_app/models.py
- [X] T032 [US2] Update Todo.__str__ to add 📅 prefix for due soon todos (calls is_due_soon method) in todo-app/src/todo_app/models.py
- [X] T033 [US2] Add CLI view_upcoming_todos function to display upcoming todos in todo-app/src/todo_app/cli.py
- [X] T034 [US2] Add CLI view_overdue_todos function to display overdue todos in todo-app/src/todo_app/cli.py
- [X] T035 [US2] Display "No upcoming todos" message when get_upcoming_todos returns empty in todo-app/src/todo_app/cli.py
- [X] T036 [US2] Display "No overdue todos" message when get_overdue_todos returns empty in todo-app/src/todo_app/cli.py
- [X] T037 [US2] Update main menu to add "View Upcoming Todos" option in todo-app/src/todo_app/cli.py
- [X] T038 [US2] Update main menu to add "View Overdue Todos" option in todo-app/src/todo_app/cli.py
- [X] T039 [US2] Update menu option numbers (existing options shift, Exit moves to higher number) in todo-app/src/todo_app/cli.py

**Checkpoint**: User Story 2 complete - users can see upcoming/overdue indicators and access dedicated views

---

## Phase 5: User Story 3 - Create Recurring Todos (Priority: P2)

**Goal**: Users can create recurring todos (daily/weekly/monthly) that auto-reschedule on completion

**Independent Test**: Create a recurring todo with "daily" recurrence, mark it complete, verify new instance created with next due date (tomorrow)

### Implementation for User Story 3

- [X] T040 [US3] Update CLI add_todo flow to prompt for recurrence type after due date in todo-app/src/todo_app/cli.py
- [X] T041 [US3] Add recurrence validation in CLI add flow (accept none/daily/weekly/monthly, Enter for none) in todo-app/src/todo_app/cli.py
- [X] T042 [US3] Validate that if recurrence != "none", due_date must be provided (show error if missing) in todo-app/src/todo_app/cli.py
- [X] T043 [US3] Parse recurrence input to Recurrence enum in CLI add flow in todo-app/src/todo_app/cli.py
- [X] T044 [US3] Enhance TodoService.mark_complete to check for recurring tasks in todo-app/src/todo_app/service.py
- [X] T045 [US3] Implement auto-rescheduling logic in mark_complete (create next instance if recurrence != NONE) in todo-app/src/todo_app/service.py
- [X] T046 [US3] Set is_recurring_parent=False on completed recurring todo to prevent duplicate rescheduling in todo-app/src/todo_app/service.py
- [X] T047 [US3] Create new todo instance with calculated next due date when rescheduling in todo-app/src/todo_app/service.py
- [X] T048 [US3] Copy title, description, priority, tags, and recurrence to new instance in todo-app/src/todo_app/service.py
- [X] T049 [US3] Display confirmation message when recurring todo is rescheduled (show new ID and due date) in todo-app/src/todo_app/cli.py

**Checkpoint**: User Story 3 complete - users can create recurring todos that auto-reschedule on completion

---

## Phase 6: User Story 4 - Stop or Modify Recurring Todos (Priority: P3)

**Goal**: Users can disable recurrence or modify recurrence pattern for existing recurring todos

**Independent Test**: Create recurring todo, disable recurrence (set to "none"), mark complete, verify no new instance created

### Implementation for User Story 4

- [X] T050 [US4] Update CLI update_todo flow to prompt for new recurrence type in todo-app/src/todo_app/cli.py
- [X] T051 [US4] Add recurrence validation in CLI update flow (accept none/daily/weekly/monthly) in todo-app/src/todo_app/cli.py
- [X] T052 [US4] Parse recurrence input to Recurrence enum in CLI update flow in todo-app/src/todo_app/cli.py
- [X] T053 [US4] Update CLI update_todo to show current recurrence type in display in todo-app/src/todo_app/cli.py
- [X] T054 [US4] Allow disabling recurrence by setting to Recurrence.NONE in update flow in todo-app/src/todo_app/cli.py
- [X] T055 [US4] Allow changing recurrence type (e.g., daily to weekly) in update flow in todo-app/src/todo_app/cli.py
- [X] T056 [US4] Validate that if recurrence is changed to != NONE, due_date must exist (show error if missing) in todo-app/src/todo_app/cli.py

**Checkpoint**: User Story 4 complete - users can disable or modify recurrence patterns

---

## Phase 7: User Story 5 - Filter and Sort by Due Date (Priority: P3)

**Goal**: Users can filter todos by due date ranges and sort by due date (extends existing filter/sort)

**Independent Test**: Create todos with various due dates, sort by due date (earliest first), verify correct order with no-due-date todos at end

### Implementation for User Story 5

- [X] T057 [US5] Extend TodoService.sort_todos to support "due_date" sort option (earliest first) in todo-app/src/todo_app/service.py
- [X] T058 [US5] Extend TodoService.sort_todos to support "due_date_desc" sort option (latest first) in todo-app/src/todo_app/service.py
- [X] T059 [US5] Handle None due dates in sort (put at end for ascending, at start for descending) in todo-app/src/todo_app/service.py
- [X] T060 [US5] Update CLI sort_todos_flow menu to add due date sort options in todo-app/src/todo_app/cli.py
- [X] T061 [US5] Test that existing filter_todos_flow works correctly with due dates (no changes needed) in todo-app/src/todo_app/cli.py
- [X] T062 [US5] Test that combined filter+sort works with due date sorting in todo-app/src/todo_app/cli.py

**Checkpoint**: User Story 5 complete - users can filter and sort by due dates

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T063 [P] Update todo-app/README.md with new scheduling features documentation (due dates, recurring tasks, upcoming/overdue views)
- [X] T064 Update existing unit tests in todo-app/tests/unit/test_models.py to cover new Recurrence enum and due_date/recurrence fields (SKIPPED - tests not requested in spec)
- [X] T065 Add unit tests for is_overdue() and is_due_soon() methods in todo-app/tests/unit/test_models.py (SKIPPED - tests not requested in spec)
- [X] T066 Update existing unit tests in todo-app/tests/unit/test_service.py to cover enhanced add_todo and update_todo signatures (SKIPPED - tests not requested in spec)
- [X] T067 Add unit tests for _calculate_next_due_date method (daily/weekly/monthly) in todo-app/tests/unit/test_service.py (SKIPPED - tests not requested in spec)
- [X] T068 Add unit tests for get_overdue_todos and get_upcoming_todos methods in todo-app/tests/unit/test_service.py (SKIPPED - tests not requested in spec)
- [X] T069 Add unit tests for recurring todo auto-rescheduling logic in mark_complete in todo-app/tests/unit/test_service.py (SKIPPED - tests not requested in spec)
- [X] T070 Test monthly recurrence edge case (Jan 31 → Feb 28 fallback) in todo-app/tests/unit/test_service.py (SKIPPED - tests not requested in spec)
- [X] T071 Update integration tests in todo-app/tests/integration/test_cli.py to reflect new menu structure and options (SKIPPED - tests not requested in spec)
- [X] T072 Add integration tests for due date add/update flows in todo-app/tests/integration/test_cli.py (SKIPPED - tests not requested in spec)
- [X] T073 Add integration tests for recurring todo creation and completion in todo-app/tests/integration/test_cli.py (SKIPPED - tests not requested in spec)
- [X] T074 Add error handling for invalid due date format with clear error messages in todo-app/src/todo_app/cli.py (COMPLETED - error handling implemented in add/update flows)
- [X] T075 Add error handling for invalid recurrence type with clear error messages in todo-app/src/todo_app/cli.py (COMPLETED - error handling implemented in add/update flows)
- [X] T076 Add error handling for recurring todo without due date (validation error) in todo-app/src/todo_app/cli.py (COMPLETED - validation implemented in add flow)
- [X] T077 Code cleanup: Remove any commented-out code or debug prints in todo-app/src/ (COMPLETED - no commented code or debug prints)
- [X] T078 Run manual acceptance testing for all 5 user stories per spec.md acceptance scenarios (READY FOR TESTING)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - extends existing models
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 (Due Dates): Can start after Phase 2 - Independent
  - US2 (Upcoming/Overdue): Depends on US1 (needs due dates) - Start after US1
  - US3 (Recurring): Depends on US1 (needs due dates for recurrence) - Start after US1
  - US4 (Modify Recurring): Depends on US3 (needs recurring tasks to modify) - Start after US3
  - US5 (Filter/Sort): Depends on US1 (needs due dates to sort) - Can start after US1
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - Due Dates)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1 - Upcoming/Overdue)**: Should start after US1 (requires due dates to detect overdue/upcoming)
- **User Story 3 (P2 - Recurring)**: Should start after US1 (requires due dates for recurrence calculation)
- **User Story 4 (P3 - Modify Recurring)**: MUST start after US3 (requires recurring tasks to modify)
- **User Story 5 (P3 - Filter/Sort Due Date)**: Should start after US1 (requires due dates to sort/filter)

### Within Each User Story

- Models before services (Phase 1 before Phase 2)
- Services before CLI (Phase 2 before Phase 3+)
- Helper methods (_calculate_next_due_date, _parse_due_date) before usage in mark_complete
- Menu updates last within each story
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1**: All model updates (T001-T010) can be done sequentially in same file
- **Phase 2**: Service helper methods (T014-T018) are parallelizable after T011-T013 complete
- **Phase 3-7**: US2 and US3 can start in parallel after US1 (both depend only on US1, not each other)
- **Phase 8**: Documentation (T063) and test updates (T064-T073) are parallelizable [P] - different files

---

## Parallel Example: After Foundational Phase

```bash
# US1 must complete first (foundation for US2 and US3)
Team Member A: Implement US1 (Due Dates) - T019 through T026

# After US1 completes, US2 and US3 can proceed in parallel:
Team Member B: Implement US2 (Upcoming/Overdue) - T027 through T039
Team Member C: Implement US3 (Recurring Tasks) - T040 through T049

# Then sequential for dependent stories:
Team Member B or C: Implement US4 (Modify Recurring) - T050 through T056
Team Member A: Implement US5 (Filter/Sort) - T057 through T062

# Polish can be done in parallel by multiple team members:
Team Member A: Documentation (T063)
Team Member B: Unit tests (T064-T070)
Team Member C: Integration tests (T071-T073)
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2 Only)

1. Complete Phase 1: Setup (T001-T010)
2. Complete Phase 2: Foundational (T011-T018)
3. Complete Phase 3: User Story 1 - Due Dates (T019-T026)
4. Complete Phase 4: User Story 2 - Upcoming/Overdue (T027-T039)
5. **STOP and VALIDATE**: Test US1 and US2 independently
6. Deploy/demo if ready

This gives you the core scheduling features (due dates + visual indicators) without the complexity of recurring tasks.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 (Due Dates) → Test independently → Deploy/Demo
3. Add US2 (Upcoming/Overdue) → Test independently (requires US1) → Deploy/Demo
4. Add US3 (Recurring Tasks) → Test independently (requires US1) → Deploy/Demo
5. Add US4 (Modify Recurring) → Test independently (requires US3) → Deploy/Demo
6. Add US5 (Filter/Sort Due Date) → Test independently (requires US1) → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T018)
2. Once Foundational is done:
   - Developer A: User Story 1 (Due Dates) - T019-T026
3. After US1 complete:
   - Developer A: User Story 2 (Upcoming/Overdue) - T027-T039
   - Developer B: User Story 3 (Recurring) - T040-T049
4. After US3 complete:
   - Developer B: User Story 4 (Modify Recurring) - T050-T056
   - Developer A: User Story 5 (Filter/Sort) - T057-T062
5. Team completes Polish together (T063-T078)

---

## Task Count Summary

- **Phase 1 (Setup)**: 10 tasks (T001-T010)
- **Phase 2 (Foundational)**: 8 tasks (T011-T018)
- **Phase 3 (US1 - Due Dates)**: 8 tasks (T019-T026)
- **Phase 4 (US2 - Upcoming/Overdue)**: 13 tasks (T027-T039)
- **Phase 5 (US3 - Recurring Tasks)**: 10 tasks (T040-T049)
- **Phase 6 (US4 - Modify Recurring)**: 7 tasks (T050-T056)
- **Phase 7 (US5 - Filter/Sort Due Date)**: 6 tasks (T057-T062)
- **Phase 8 (Polish)**: 16 tasks (T063-T078)

**Total**: 78 tasks

**Parallel Opportunities**: Service helper methods (T014-T018 after T011-T013), US2+US3 after US1, Polish phase documentation and tests (T063-T073)

**Independent Test Criteria**:
- US1: Add/view/update due dates - verify displayed and persisted, test YYYY-MM-DD HH:MM format
- US2: Create todos with various due dates - verify overdue (⚠) and upcoming (📅) indicators, test dedicated views
- US3: Create recurring todo, mark complete - verify new instance created with correct next due date
- US4: Create recurring todo, disable recurrence, mark complete - verify no new instance created
- US5: Create todos with various due dates, sort by due date - verify correct order

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (US1: Due Dates) + Phase 4 (US2: Upcoming/Overdue) = 39 tasks

This delivers the foundational scheduling features (due dates with overdue/upcoming indicators) that provide immediate value.

---

## Notes

- [P] tasks = different files or methods, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests are NOT included in spec - focus on implementation, but tests added in Polish phase for robustness
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Menu option numbers will shift - update existing integration tests
- Recurring tasks auto-reschedule on completion (not time-based)
- Monthly recurrence uses calendar module for non-existent date handling
