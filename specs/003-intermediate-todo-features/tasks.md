---
description: "Task list for Intermediate Features for In-Memory Python Console Todo App"
---

# Tasks: Intermediate Features for In-Memory Python Console Todo App

**Input**: Design documents from `/specs/003-intermediate-todo-features/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Tests are NOT explicitly requested in the feature specification. Focus on implementation only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `todo-app/src/`, `todo-app/tests/` at repository root
- This is a Python console application using the existing todo-app structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Extend existing data model with new Priority enum and enhanced Todo attributes

**Note**: The basic console todo app from `001-console-todo` already exists. This phase extends it.

- [X] T001 Add Priority enum to todo-app/src/todo_app/models.py (HIGH=1, MEDIUM=2, LOW=3)
- [X] T002 Extend Todo dataclass with priority field (default=Priority.MEDIUM) in todo-app/src/todo_app/models.py
- [X] T003 Extend Todo dataclass with tags field (default=empty list) in todo-app/src/todo_app/models.py
- [X] T004 Update Todo.__post_init__ validation to enforce Priority type in todo-app/src/todo_app/models.py
- [X] T005 Update Todo.__post_init__ validation to normalize tags (lowercase, trim, dedupe) in todo-app/src/todo_app/models.py
- [X] T006 Update Todo.__str__ display format to include priority and tags columns in todo-app/src/todo_app/models.py

**Checkpoint**: Data model enhanced - all existing tests should still pass (new fields have defaults)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core service enhancements that MUST be complete before ANY user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Update TodoService.add_todo signature to accept priority and tags parameters in todo-app/src/todo_app/service.py
- [X] T008 Update TodoService.update_todo signature to accept priority and tags parameters in todo-app/src/todo_app/service.py
- [X] T009 Add helper method _normalize_tags to TodoService in todo-app/src/todo_app/service.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Assign Priority to Todos (Priority: P1) 🎯 MVP

**Goal**: Users can assign and update priority levels (high, medium, low) for todos

**Independent Test**: Add a new todo with priority "high", view the list to confirm priority is displayed, update the priority to "low", verify the change persists

### Implementation for User Story 1

- [X] T010 [US1] Update CLI add_todo flow to prompt for priority after description in todo-app/src/todo_app/cli.py
- [X] T011 [US1] Add priority validation in CLI add flow (accept high/medium/low, Enter for default) in todo-app/src/todo_app/cli.py
- [X] T012 [US1] Update CLI update_todo flow to prompt for new priority in todo-app/src/todo_app/cli.py
- [X] T013 [US1] Add priority validation in CLI update flow in todo-app/src/todo_app/cli.py
- [X] T014 [US1] Update CLI view_todos display to show priority column in todo-app/src/todo_app/cli.py
- [X] T015 [US1] Update main menu help text to reflect new priority feature in todo-app/src/todo_app/cli.py

**Checkpoint**: User Story 1 complete - users can assign and update priority, displayed in list view

---

## Phase 4: User Story 2 - Tag Todos with Categories (Priority: P1)

**Goal**: Users can assign and update multiple tags/categories for todos

**Independent Test**: Create a todo with tags "work, meeting", view to confirm tags displayed, update to add "urgent" tag, verify change persists

### Implementation for User Story 2

- [X] T016 [US2] Update CLI add_todo flow to prompt for tags (comma-separated) after priority in todo-app/src/todo_app/cli.py
- [X] T017 [US2] Add tags parsing logic in CLI add flow (split on comma, normalize) in todo-app/src/todo_app/cli.py
- [X] T018 [US2] Update CLI update_todo flow to prompt for new tags in todo-app/src/todo_app/cli.py
- [X] T019 [US2] Add tags parsing logic in CLI update flow in todo-app/src/todo_app/cli.py
- [X] T020 [US2] Update CLI view_todos display to show tags column (truncate if > 20 chars) in todo-app/src/todo_app/cli.py

**Checkpoint**: User Story 2 complete - users can assign and update tags, displayed in list view

---

## Phase 5: User Story 3 - Search Todos by Keyword (Priority: P2)

**Goal**: Users can search todos by keyword (case-insensitive, searches title and description)

**Independent Test**: Create 5 todos with distinct titles/descriptions, search for "grocery", verify only matching todos returned

### Implementation for User Story 3

- [X] T021 [US3] Add search_todos method to TodoService (case-insensitive, searches title + description) in todo-app/src/todo_app/service.py
- [X] T022 [US3] Add CLI search_todos function to prompt for keyword in todo-app/src/todo_app/cli.py
- [X] T023 [US3] Add keyword validation in CLI search flow (reject empty) in todo-app/src/todo_app/cli.py
- [X] T024 [US3] Display search results or "No matching todos found" message in todo-app/src/todo_app/cli.py
- [X] T025 [US3] Add "Search Todos" option (6) to main menu in todo-app/src/todo_app/cli.py
- [X] T026 [US3] Update menu option numbers (Exit moves to 9) in todo-app/src/todo_app/cli.py

**Checkpoint**: User Story 3 complete - users can search by keyword and see results

---

## Phase 6: User Story 4 - Filter Todos by Status, Priority, or Category (Priority: P2)

**Goal**: Users can filter the todo list by completion status, priority level, or category tag

**Independent Test**: Create 5 todos with varying statuses, priorities, and tags; filter by status "incomplete"; verify only incomplete todos shown

### Implementation for User Story 4

- [X] T027 [P] [US4] Add filter_by_status method to TodoService in todo-app/src/todo_app/service.py
- [X] T028 [P] [US4] Add filter_by_priority method to TodoService in todo-app/src/todo_app/service.py
- [X] T029 [P] [US4] Add filter_by_tag method to TodoService in todo-app/src/todo_app/service.py
- [X] T030 [US4] Add CLI filter_todos function with sub-menu (1=status, 2=priority, 3=tag) in todo-app/src/todo_app/cli.py
- [X] T031 [US4] Add filter by status flow (prompt complete/incomplete) in todo-app/src/todo_app/cli.py
- [X] T032 [US4] Add filter by priority flow (prompt high/medium/low) in todo-app/src/todo_app/cli.py
- [X] T033 [US4] Add filter by tag flow (prompt tag name) in todo-app/src/todo_app/cli.py
- [X] T034 [US4] Display filtered results or "No todos match the selected filter" message in todo-app/src/todo_app/cli.py
- [X] T035 [US4] Add "Filter Todos" option (7) to main menu in todo-app/src/todo_app/cli.py

**Checkpoint**: User Story 4 complete - users can filter by status, priority, or tag

---

## Phase 7: User Story 5 - Sort Todos (Priority: P3)

**Goal**: Users can sort the todo list by priority, creation date, or alphabetically by title

**Independent Test**: Create todos with mixed priorities, sort by priority, verify order is high → medium → low

### Implementation for User Story 5

- [X] T036 [US5] Add sort_todos method to TodoService (accepts sort_by parameter) in todo-app/src/todo_app/service.py
- [X] T037 [US5] Implement priority sort (HIGH=1 → MEDIUM=2 → LOW=3) in sort_todos in todo-app/src/todo_app/service.py
- [X] T038 [US5] Implement date sort (newest first and oldest first options) in sort_todos in todo-app/src/todo_app/service.py
- [X] T039 [US5] Implement alphabetical sort (case-insensitive by title) in sort_todos in todo-app/src/todo_app/service.py
- [X] T040 [US5] Add CLI sort_todos function with sub-menu (1=priority, 2=date newest, 3=date oldest, 4=alphabetical) in todo-app/src/todo_app/cli.py
- [X] T041 [US5] Display sorted results in todo-app/src/todo_app/cli.py
- [X] T042 [US5] Add "Sort Todos" option (8) to main menu in todo-app/src/todo_app/cli.py

**Checkpoint**: User Story 5 complete - users can sort by priority, date, or alphabetically

---

## Phase 8: User Story 6 - Combined Filter and Sort (Priority: P3)

**Goal**: Users can apply a filter and then sort the filtered results

**Independent Test**: Create 10 todos with mixed statuses and priorities, filter by status "incomplete", then sort by priority, verify only incomplete todos shown and ordered correctly

### Implementation for User Story 6

- [X] T043 [US6] Add CLI filter_and_sort_todos function in todo-app/src/todo_app/cli.py
- [X] T044 [US6] Implement filter selection flow (reuse filter menu from US4) in todo-app/src/todo_app/cli.py
- [X] T045 [US6] Implement sort selection flow (reuse sort menu from US5) in todo-app/src/todo_app/cli.py
- [X] T046 [US6] Apply filter, then apply sort to filtered results in todo-app/src/todo_app/cli.py
- [X] T047 [US6] Display combined filter+sort results in todo-app/src/todo_app/cli.py
- [X] T048 [US6] Update main menu to indicate option 7 now supports combined filter and sort in todo-app/src/todo_app/cli.py

**Checkpoint**: User Story 6 complete - users can filter and sort in a single operation

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T049 [P] Update todo-app/README.md with new feature documentation (priority, tags, search, filter, sort)
- [ ] T050 Update existing unit tests in todo-app/tests/unit/test_models.py to cover new Priority enum and tags field
- [ ] T051 Update existing unit tests in todo-app/tests/unit/test_service.py to cover new service methods
- [ ] T052 Update integration tests in todo-app/tests/integration/test_cli.py to reflect new menu structure (9 options)
- [ ] T053 Update integration tests in todo-app/tests/integration/test_main.py to test new CLI flows
- [X] T054 Add error handling for invalid priority and tag inputs across all CLI functions in todo-app/src/todo_app/cli.py
- [X] T055 Code cleanup: Remove any commented-out code or debug prints in todo-app/src/
- [X] T056 Run manual acceptance testing for all 6 user stories per spec.md acceptance scenarios

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - extends existing models
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - US1 (Priority): Can start after Phase 2 - Independent
  - US2 (Tags): Can start after Phase 2 - Independent
  - US3 (Search): Can start after Phase 2 - Independent (uses base Todo fields)
  - US4 (Filter): Depends on US1 and US2 (needs priority and tags data) - Start after US1+US2
  - US5 (Sort): Depends on US1 (needs priority data) - Start after US1
  - US6 (Filter+Sort): Depends on US4 and US5 - Start after US4+US5
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - Priority)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1 - Tags)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2 - Search)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2 - Filter)**: Should start after US1 and US2 (needs priority and tags to filter meaningfully)
- **User Story 5 (P3 - Sort)**: Should start after US1 (needs priority for sort-by-priority)
- **User Story 6 (P3 - Filter+Sort)**: MUST start after US4 and US5 (combines both features)

### Within Each User Story

- Models before services (Phase 1 before Phase 2)
- Services before CLI (Phase 2 before Phase 3+)
- Menu updates last within each story
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1**: All model updates (T001-T006) can be done sequentially in same file
- **Phase 2**: All service updates (T007-T009) can be done sequentially in same file
- **Phase 3-8**: US1, US2, US3 can start in parallel after Phase 2 (different features, independent)
- **Phase 4 (US4)**: Filter methods (T027-T029) are parallelizable [P] - different methods
- **Phase 9**: Documentation (T049) and test updates (T050-T053) are parallelizable [P] - different files

---

## Parallel Example: Setup Phase

```bash
# Phase 1 tasks are sequential (same file):
Task T001: Add Priority enum
Task T002: Extend Todo with priority field
Task T003: Extend Todo with tags field
Task T004: Update validation for priority
Task T005: Update validation for tags
Task T006: Update __str__ display format
```

## Parallel Example: After Foundational Phase

```bash
# US1, US2, US3 can proceed in parallel:
Team Member A: Implement US1 (Priority) - T010 through T015
Team Member B: Implement US2 (Tags) - T016 through T020
Team Member C: Implement US3 (Search) - T021 through T026

# Then coordinate:
Team Member A+B: Implement US4 (Filter) - needs US1+US2 done
Team Member A: Implement US5 (Sort) - needs US1 done
Team Member A+B: Implement US6 (Filter+Sort) - needs US4+US5 done
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T009)
3. Complete Phase 3: User Story 1 - Priority (T010-T015)
4. Complete Phase 4: User Story 2 - Tags (T016-T020)
5. **STOP and VALIDATE**: Test US1 and US2 independently
6. Deploy/demo if ready

This gives you the core organizational features (priority + tags) without the complexity of search/filter/sort.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 (Priority) → Test independently → Deploy/Demo
3. Add US2 (Tags) → Test independently → Deploy/Demo
4. Add US3 (Search) → Test independently → Deploy/Demo
5. Add US4 (Filter) → Test independently (requires US1+US2) → Deploy/Demo
6. Add US5 (Sort) → Test independently (requires US1) → Deploy/Demo
7. Add US6 (Filter+Sort) → Test independently (requires US4+US5) → Deploy/Demo
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T009)
2. Once Foundational is done:
   - Developer A: User Story 1 (Priority) - T010-T015
   - Developer B: User Story 2 (Tags) - T016-T020
   - Developer C: User Story 3 (Search) - T021-T026
3. After US1+US2 complete:
   - Developer A: User Story 4 (Filter) - T027-T035
   - Developer B: User Story 5 (Sort) - T036-T042
4. After US4+US5 complete:
   - Developer A or B: User Story 6 (Filter+Sort) - T043-T048
5. Team completes Polish together (T049-T056)

---

## Task Count Summary

- **Phase 1 (Setup)**: 6 tasks (T001-T006)
- **Phase 2 (Foundational)**: 3 tasks (T007-T009)
- **Phase 3 (US1 - Priority)**: 6 tasks (T010-T015)
- **Phase 4 (US2 - Tags)**: 5 tasks (T016-T020)
- **Phase 5 (US3 - Search)**: 6 tasks (T021-T026)
- **Phase 6 (US4 - Filter)**: 9 tasks (T027-T035)
- **Phase 7 (US5 - Sort)**: 7 tasks (T036-T042)
- **Phase 8 (US6 - Filter+Sort)**: 6 tasks (T043-T048)
- **Phase 9 (Polish)**: 8 tasks (T049-T056)

**Total**: 56 tasks

**Parallel Opportunities**: 3 filter methods (T027-T029), 4 documentation/test updates (T049-T053)

**Independent Test Criteria**:
- US1: Add/view/update priority - verify displayed and persisted
- US2: Add/view/update tags - verify displayed and persisted
- US3: Create multiple todos, search keyword - verify matching results
- US4: Create diverse todos, apply filter - verify correct subset
- US5: Create diverse todos, apply sort - verify correct order
- US6: Create diverse todos, filter then sort - verify both applied correctly

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (US1: Priority) + Phase 4 (US2: Tags) = 20 tasks

This delivers the foundational organization features (priority and tags) that enable meaningful task categorization.

---

## Notes

- [P] tasks = different files or methods, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests are NOT included (not requested in spec) - focus on implementation
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Menu option numbers shift from 6 to 9 - update tests and user documentation
